# -*- coding: utf-8 -*-
"""`tldextract` accurately separates the gTLD or ccTLD (generic or country code
top-level domain) from the registered domain and subdomains of a URL.

    >>> import tldextract

    >>> tldextract.extract('http://forums.news.cnn.com/')
    ExtractResult(subdomain='forums.news', domain='cnn', suffix='com')

    >>> tldextract.extract('http://forums.bbc.co.uk/') # United Kingdom
    ExtractResult(subdomain='forums', domain='bbc', suffix='co.uk')

    >>> tldextract.extract('http://www.worldbank.org.kg/') # Kyrgyzstan
    ExtractResult(subdomain='www', domain='worldbank', suffix='org.kg')

`ExtractResult` is a namedtuple, so it's simple to access the parts you want.

    >>> ext = tldextract.extract('http://forums.bbc.co.uk')
    >>> (ext.subdomain, ext.domain, ext.suffix)
    ('forums', 'bbc', 'co.uk')
    >>> # rejoin subdomain and domain
    >>> '.'.join(ext[:2])
    'forums.bbc'
    >>> # a common alias
    >>> ext.registered_domain
    'bbc.co.uk'

Note subdomain and suffix are _optional_. Not all URL-like inputs have a
subdomain or a valid suffix.

    >>> tldextract.extract('google.com')
    ExtractResult(subdomain='', domain='google', suffix='com')

    >>> tldextract.extract('google.notavalidsuffix')
    ExtractResult(subdomain='google', domain='notavalidsuffix', suffix='')

    >>> tldextract.extract('http://127.0.0.1:8080/deployed/')
    ExtractResult(subdomain='', domain='127.0.0.1', suffix='')

If you want to rejoin the whole namedtuple, regardless of whether a subdomain
or suffix were found:

    >>> ext = tldextract.extract('http://127.0.0.1:8080/deployed/')
    >>> # this has unwanted dots
    >>> '.'.join(ext)
    '.127.0.0.1.'
    >>> # join part only if truthy
    >>> '.'.join(part for part in ext if part)
    '127.0.0.1'
"""

import collections
import logging
import os
from functools import wraps

from externals import idna

from .cache import DiskCache, get_cache_dir
from .remote import IP_RE, SCHEME_RE, looks_like_ip
from .suffix_list import get_suffix_lists

LOG = logging.getLogger("tldextract")


CACHE_TIMEOUT = os.environ.get("TLDEXTRACT_CACHE_TIMEOUT")

PUBLIC_SUFFIX_LIST_URLS = (
    "https://publicsuffix.org/list/public_suffix_list.dat",
    "https://raw.githubusercontent.com/publicsuffix/list/master/public_suffix_list.dat",
)


class ExtractResult(collections.namedtuple("ExtractResult", "subdomain domain suffix")):
    """namedtuple of a URL's subdomain, domain, and suffix."""

    # Necessary for __dict__ member to get populated in Python 3+
    __slots__ = ()

    @property
    def registered_domain(self):
        """
        Joins the domain and suffix fields with a dot, if they're both set.

        >>> extract('http://forums.bbc.co.uk').registered_domain
        'bbc.co.uk'
        >>> extract('http://localhost:8080').registered_domain
        ''
        """
        if self.domain and self.suffix:
            return self.domain + "." + self.suffix
        return ""

    @property
    def fqdn(self):
        """
        Returns a Fully Qualified Domain Name, if there is a proper domain/suffix.

        >>> extract('http://forums.bbc.co.uk/path/to/file').fqdn
        'forums.bbc.co.uk'
        >>> extract('http://localhost:8080').fqdn
        ''
        """
        if self.domain and self.suffix:
            # self is the namedtuple (subdomain domain suffix)
            return ".".join(i for i in self if i)
        return ""

    @property
    def ipv4(self):
        """
        Returns the ipv4 if that is what the presented domain/url is

        >>> extract('http://127.0.0.1/path/to/file').ipv4
        '127.0.0.1'
        >>> extract('http://127.0.0.1.1/path/to/file').ipv4
        ''
        >>> extract('http://256.1.1.1').ipv4
        ''
        """
        if not (self.suffix or self.subdomain) and IP_RE.match(self.domain):
            return self.domain
        return ""


class TLDExtract:
    """A callable for extracting, subdomain, domain, and suffix components from
    a URL."""

    # TODO: Agreed with Pylint: too-many-arguments
    def __init__(  # pylint: disable=too-many-arguments
        self,
        cache_dir=get_cache_dir(),
        suffix_list_urls=PUBLIC_SUFFIX_LIST_URLS,
        fallback_to_snapshot=True,
        include_psl_private_domains=False,
        extra_suffixes=(),
        cache_fetch_timeout=CACHE_TIMEOUT,
    ):
        """
        Constructs a callable for extracting subdomain, domain, and suffix
        components from a URL.

        Upon calling it, it first checks for a JSON in `cache_dir`.
        By default, the `cache_dir` will live in the tldextract directory.

        You can disable the caching functionality of this module  by setting `cache_dir` to False.

        If the cached version does not exist (such as on the first run), HTTP request the URLs in
        `suffix_list_urls` in order, until one returns public suffix list data. To disable HTTP
        requests, set this to something falsy.

        The default list of URLs point to the latest version of the Mozilla Public Suffix List and
        its mirror, but any similar document could be specified. Local files can be specified by
        using the `file://` protocol. (See `urllib2` documentation.)

        If there is no cached version loaded and no data is found from the `suffix_list_urls`,
        the module will fall back to the included TLD set snapshot. If you do not want
        this behavior, you may set `fallback_to_snapshot` to False, and an exception will be
        raised instead.

        The Public Suffix List includes a list of "private domains" as TLDs,
        such as blogspot.com. These do not fit `tldextract`'s definition of a
        suffix, so these domains are excluded by default. If you'd like them
        included instead, set `include_psl_private_domains` to True.

        You can pass additional suffixes in `extra_suffixes` argument without changing list URL

        cache_fetch_timeout is passed unmodified to the underlying request object
        per the requests documentation here:
        http://docs.python-requests.org/en/master/user/advanced/#timeouts

        cache_fetch_timeout can also be set to a single value with the
        environment variable TLDEXTRACT_CACHE_TIMEOUT, like so:

        TLDEXTRACT_CACHE_TIMEOUT="1.2"

        When set this way, the same timeout value will be used for both connect
        and read timeouts
        """
        suffix_list_urls = suffix_list_urls or ()
        self.suffix_list_urls = tuple(
            url.strip() for url in suffix_list_urls if url.strip()
        )

        self.fallback_to_snapshot = fallback_to_snapshot
        if not (self.suffix_list_urls or cache_dir or self.fallback_to_snapshot):
            raise ValueError(
                "The arguments you have provided disable all ways for tldextract "
                "to obtain data. Please provide a suffix list data, a cache_dir, "
                "or set `fallback_to_snapshot` to `True`."
            )

        self.include_psl_private_domains = include_psl_private_domains
        self.extra_suffixes = extra_suffixes
        self._extractor = None

        self.cache_fetch_timeout = cache_fetch_timeout
        self._cache = DiskCache(cache_dir)
        if isinstance(self.cache_fetch_timeout, str):
            self.cache_fetch_timeout = float(self.cache_fetch_timeout)

    def __call__(self, url, include_psl_private_domains=None):
        """
        Takes a string URL and splits it into its subdomain, domain, and
        suffix (effective TLD, gTLD, ccTLD, etc.) component.

        >>> extract = TLDExtract()
        >>> extract('http://forums.news.cnn.com/')
        ExtractResult(subdomain='forums.news', domain='cnn', suffix='com')
        >>> extract('http://forums.bbc.co.uk/')
        ExtractResult(subdomain='forums', domain='bbc', suffix='co.uk')
        """

        netloc = (
            SCHEME_RE.sub("", url)
            .partition("/")[0]
            .partition("?")[0]
            .partition("#")[0]
            .split("@")[-1]
            .partition(":")[0]
            .strip()
            .rstrip(".")
        )

        labels = netloc.split(".")

        translations = [_decode_punycode(label) for label in labels]
        suffix_index = self._get_tld_extractor().suffix_index(
            translations, include_psl_private_domains=include_psl_private_domains
        )

        suffix = ".".join(labels[suffix_index:])
        if not suffix and netloc and looks_like_ip(netloc):
            return ExtractResult("", netloc, "")

        subdomain = ".".join(labels[: suffix_index - 1]) if suffix_index else ""
        domain = labels[suffix_index - 1] if suffix_index else ""
        return ExtractResult(subdomain, domain, suffix)

    def update(self, fetch_now=False):
        """Force fetch the latest suffix list definitions."""
        self._extractor = None
        self._cache.clear()
        if fetch_now:
            self._get_tld_extractor()

    @property
    def tlds(self):
        """
        Returns the list of tld's used by default

        This will vary based on `include_psl_private_domains` and `extra_suffixes`
        """
        return list(self._get_tld_extractor().tlds())

    def _get_tld_extractor(self):
        """Get or compute this object's TLDExtractor. Looks up the TLDExtractor
        in roughly the following order, based on the settings passed to
        __init__:

        1. Memoized on `self`
        2. Local system _cache file
        3. Remote PSL, over HTTP
        4. Bundled PSL snapshot file"""

        if self._extractor:
            return self._extractor

        public_tlds, private_tlds = get_suffix_lists(
            cache=self._cache,
            urls=self.suffix_list_urls,
            cache_fetch_timeout=self.cache_fetch_timeout,
            fallback_to_snapshot=self.fallback_to_snapshot,
        )

        if not any([public_tlds, private_tlds, self.extra_suffixes]):
            raise ValueError("No tlds set. Cannot proceed without tlds.")

        self._extractor = _PublicSuffixListTLDExtractor(
            public_tlds=public_tlds,
            private_tlds=private_tlds,
            extra_tlds=list(self.extra_suffixes),
            include_psl_private_domains=self.include_psl_private_domains,
        )
        return self._extractor


TLD_EXTRACTOR = TLDExtract()


@wraps(TLD_EXTRACTOR.__call__)
def extract(
    url, include_psl_private_domains=False
):  # pylint: disable=missing-function-docstring
    return TLD_EXTRACTOR(url, include_psl_private_domains=include_psl_private_domains)


@wraps(TLD_EXTRACTOR.update)
def update(*args, **kwargs):  # pylint: disable=missing-function-docstring
    return TLD_EXTRACTOR.update(*args, **kwargs)


class _PublicSuffixListTLDExtractor:
    """Wrapper around this project's main algo for PSL
    lookups.
    """

    def __init__(
        self, public_tlds, private_tlds, extra_tlds, include_psl_private_domains=False
    ):
        # set the default value
        self.include_psl_private_domains = include_psl_private_domains
        self.public_tlds = public_tlds
        self.private_tlds = private_tlds
        self.tlds_incl_private = frozenset(public_tlds + private_tlds + extra_tlds)
        self.tlds_excl_private = frozenset(public_tlds + extra_tlds)

    def tlds(self, include_psl_private_domains=None):
        """Get the currently filtered list of suffixes."""
        if include_psl_private_domains is None:
            include_psl_private_domains = self.include_psl_private_domains

        return (
            self.tlds_incl_private
            if include_psl_private_domains
            else self.tlds_excl_private
        )

    def suffix_index(self, lower_spl, include_psl_private_domains=None):
        """Returns the index of the first suffix label.
        Returns len(spl) if no suffix is found
        """
        tlds = self.tlds(include_psl_private_domains)
        length = len(lower_spl)
        for i in range(length):
            maybe_tld = ".".join(lower_spl[i:])
            exception_tld = "!" + maybe_tld
            if exception_tld in tlds:
                return i + 1

            if maybe_tld in tlds:
                return i

            wildcard_tld = "*." + ".".join(lower_spl[i + 1 :])
            if wildcard_tld in tlds:
                return i

        return length


def _decode_punycode(label):
    lowered = label.lower()
    looks_like_puny = lowered.startswith("xn--")
    if looks_like_puny:
        try:
            return idna.decode(label.encode("ascii")).lower()
        except (UnicodeError, IndexError):
            pass
    return lowered
