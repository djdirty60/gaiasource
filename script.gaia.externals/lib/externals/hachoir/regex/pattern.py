from externals.hachoir.core.tools import makePrintable
from externals.hachoir.regex import RegexEmpty, parse, createString


class Pattern:
    """
    Abstract class used to define a pattern used in pattern matching
    """

    def __init__(self, user):
        self.user = user


class StringPattern(Pattern):
    """
    Static string pattern
    """

    def __init__(self, text, user=None):
        Pattern.__init__(self, user)
        self.text = text

    def __str__(self):
        return makePrintable(self.text, 'ASCII')

    def __repr__(self):
        return "<StringPattern '%s'>" % self


class RegexPattern(Pattern):
    """
    Regular expression pattern
    """

    def __init__(self, regex, user=None):
        Pattern.__init__(self, user)
        self.regex = parse(regex)
        self._compiled_regex = None

    def __str__(self):
        return makePrintable(str(self.regex), 'ASCII')

    def __repr__(self):
        return "<RegexPattern '%s'>" % self

    def match(self, data):
        return self.compiled_regex.match(data)

    def _getCompiledRegex(self):
        if self._compiled_regex is None:
            self._compiled_regex = self.regex.compile(python=True)
        return self._compiled_regex
    compiled_regex = property(_getCompiledRegex)


class PatternMatching:
    """
    Fast pattern matching class: match multiple patterns at the same time.

    Create your patterns:

    >>> p=PatternMatching()
    >>> p.addString("a")
    >>> p.addString("b")
    >>> p.addRegex("[cd]e")

    Search patterns:

    >>> for item in p.search("a b ce"):
    ...    print(item)
    ...
    (0, 1, <StringPattern 'a'>)
    (2, 3, <StringPattern 'b'>)
    (4, 6, <RegexPattern '[cd]e'>)
    """

    def __init__(self):
        self.string_patterns = []
        self.string_dict = {}
        self.regex_patterns = []
        self._need_commit = True

        # Following attributes are generated by _commit() method
        self._regex = None
        self._compiled_regex = None
        self._max_length = None

    def commit(self):
        """
        Generate whole regex merging all (string and regex) patterns
        """
        if not self._need_commit:
            return
        self._need_commit = False
        length = 0
        regex = None
        for item in self.string_patterns:
            if regex:
                regex |= createString(item.text)
            else:
                regex = createString(item.text)
            length = max(length, len(item.text))
        for item in self.regex_patterns:
            if regex:
                regex |= item.regex
            else:
                regex = item.regex
            length = max(length, item.regex.maxLength())
        if not regex:
            regex = RegexEmpty()
        self._regex = regex
        self._compiled_regex = regex.compile(python=True)
        self._max_length = length

    def addString(self, magic, user=None):
        item = StringPattern(magic, user)
        if item.text in self.string_dict:
            # Skip duplicates
            return
        self.string_patterns.append(item)
        self.string_dict[item.text] = item
        self._need_commit = True

    def addRegex(self, regex, user=None):
        item = RegexPattern(regex, user)
        if item.regex.maxLength() is None:
            raise ValueError(
                "Regular expression with no maximum size has forbidden")
        self.regex_patterns.append(item)
        self._need_commit = True

    def getPattern(self, data):
        """
        Get pattern item matching data.
        Raise KeyError if no pattern does match it.
        """
        # Try in string patterns
        try:
            return self.string_dict[data]
        except KeyError:
            pass

        # Try in regex patterns
        for item in self.regex_patterns:
            if item.match(data):
                return item
        raise KeyError("Unable to get pattern item")

    def search(self, data):
        """
        Search patterns in data.
        Return a generator of tuples: (start, end, item)
        """
        if not self.max_length:
            # No pattern: returns nothing
            return
        for match in self.compiled_regex.finditer(data):
            item = self.getPattern(match.group(0))
            yield (match.start(0), match.end(0), item)

    def __str__(self):
        return makePrintable(str(self.regex), 'ASCII')

    def _getAttribute(self, name):
        self.commit()
        return getattr(self, name)

    def _getRegex(self):
        return self._getAttribute("_regex")
    regex = property(_getRegex)

    def _getCompiledRegex(self):
        return self._getAttribute("_compiled_regex")
    compiled_regex = property(_getCompiledRegex)

    def _getMaxLength(self):
        return self._getAttribute("_max_length")
    max_length = property(_getMaxLength)


if __name__ == "__main__":
    import doctest
    import sys
    failure, nb_test = doctest.testmod()
    if failure:
        sys.exit(1)
