# -*- coding: utf-8 -*-

'''
	Gaia Add-on
	Copyright (C) 2016 Gaia

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from lib.modules.tools import Settings, Logger, Time, Subprocess, System
from lib.modules.external import Importer
from lib.modules.concurrency import Lock

class CloudflareException(Exception):

	def __init__(self, exception, scraper, message = 'Cloudflare Error'):
		super(CloudflareException, self).__init__(message)
		self.exception = exception
		self.scraper = scraper
		try: self.response = scraper.response
		except: self.response = None
		try: self.cookies = scraper.cookies.get_dict()
		except: self.cookies = None

class Cloudflare(object):

	EngineNative = 'native' # Pure Python - no additional modules required.
	EngineV8 = 'v8' # Not supported. Requires C++ code to be compiled to usue the Python module "v8eval".
	EngineJs2py = 'js2py' # Pure Python - requires "js2py", "pyjsparser", and optionally "tzlocal" and "pytz"
	EngineNodejs = 'nodejs' # External system call.
	EngineChakra = 'chakracore' # Requires external library (.so, .dylib, .dll) which is imported and called from Python.
	Engines = [ # Order according to the priority of picking one.
		{'type' : EngineJs2py,	'name' : 'Js2Py',	'reliable' : True,	'message' : None},
		{'type' : EngineNodejs,	'name' : 'NodeJs',	'reliable' : True,	'message' : 35701},
		{'type' : EngineChakra,	'name' : 'Chakra',	'reliable' : True,	'message' : 35702},
		{'type' : EngineV8,		'name' : 'V8',		'reliable' : True,	'message' : 35703},
		{'type' : EngineNative,	'name' : 'Native',	'reliable' : False,	'message' : None},
	]

	Links = [
		'http://kat.tv',
		'https://www2.yggtorrent.ch',
		'https://soap2day.is',
		'https://iptorrents.eu',
		'https://arma-models.ru',
		'https://yggtorrent.si',
		'https://www.extreme-down.ninja',
		'https://www.spigotmc.org',
		'https://rlsbb.ru',

		'https://bt4g.org/search/dummy',
		'https://btmet.com',
		'https://btmulu.com',
		'https://demonoid.is/files/?query=dummy',
		'https://ext.to/search/?q=dummy',
		'https://idope.se',
		'https://www.torrentfunk.com/all/torrents/dummy.html',
		'https://www.magnetdl.com/d/dummy/',
		'https://torrentquest.com/search/?q=dummy',
	]

	Headers = [
		'cf-request-id',
		'cf-ray',
	]

	DelayMinimum = 1
	DelayMaximum = 3

	# Must correspond with settings option.
	RetryMinimum = 1
	RetryMaximum = 10

	ReuseLock = Lock()
	ReuseScrapers = {}

	Timeout = 30

	# Must be the same as in network.py.
	# Must have the same values as in settings.xml.
	ValidateStrict				= 3	# Full verification. If anything is wrong with the SSL, the request will fail.
	ValidateModerate			= 2	# Strict verification. Like ValidateStrict, but allows expired and incorrect-domain SSL.
	ValidateLenient				= 1	# Lenient verification. Like ValidateModerate, but uses the old insecure TLSv1 which avoids certain SSL errors (eg: sslv3 alert handshake failure).
	ValidateNone				= 0	# Not implemented yet. Not sure if it can be switched off completley. Currently will fall back to ValidateLenient.

	def __init__(self, engine = None, validate = ValidateStrict, reuse = True):
		self.mEngine = engine
		self.mValidate = validate
		self.mReuse = reuse

	##############################################################################
	# RESET
	##############################################################################

	@classmethod
	def reset(self, settings = True):
		Cloudflare.ReuseScrapers = {}

	##############################################################################
	# GENERAL
	##############################################################################

	@classmethod
	def enabled(self):
		return self._settingsEnabled()

	@classmethod
	def settingsEngine(self, settings = True):
		from lib.modules.interface import Loader, Format, Translation, Dialog
		Loader.show()
		labels = []
		cloudflare = Cloudflare()
		engine = self._engine()
		for item in Cloudflare.Engines:
			if engine == item['type']: support = Format.fontColor(32301, Format.colorExcellent())
			elif cloudflare.supported(engine = item['type']): support = Format.fontColor(35696, Format.colorGood())
			else: support = Format.fontColor(35454, Format.colorBad())
			reliable = Translation.string(35698 if item['reliable'] else 35697)
			labels.append('%s [%s]: %s' % (Format.fontBold(item['name']), reliable, support))
		Loader.hide()
		choice = Dialog.select(title = 35690, items = labels)
		if choice >= 0:
			Loader.show()
			supported = cloudflare.supported(engine = Cloudflare.Engines[choice]['type'])
			Loader.hide()
			if supported:
				Loader.hide()
				Settings.set('network.cloudflare.engine', Cloudflare.Engines[choice]['name'])
			else:
				message = Translation.string(35700)
				if Cloudflare.Engines[choice]['message']: message += ' ' + Translation.string(Cloudflare.Engines[choice]['message'])
				Dialog.confirm(title = 35690, message = message)
		if settings: Settings.launch('network.cloudflare.engine')

	@classmethod
	def _settingsEnabled(self):
		return Settings.getBoolean('network.cloudflare.enabled')

	@classmethod
	def _settingsEngine(self):
		return Settings.getString('network.cloudflare.engine')

	@classmethod
	def _settingsRetry(self):
		return Settings.getInteger('network.cloudflare.retry')

	@classmethod
	def _engine(self, engine = None, name = False):
		if engine is None: engine = self._settingsEngine()
		engine = engine.lower()

		result = Cloudflare.EngineNative
		for item in Cloudflare.Engines:
			if item['type'] in engine or engine in item['type']:
				result = item['type']
				break

		if name:
			for item in Cloudflare.Engines:
				if result == item['type']:
					return item['name']
			return None
		else:
			return result

	def _scraper(self, engine = None, certificate = None, link = None, domain = None):
		if certificate is None: certificate = self.mValidate
		if certificate <= Cloudflare.ValidateModerate:
			urllib3 = Importer.moduleUrllib3()
			urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
		cloudscraper = self.module()
		interpreter = self._engine(engine)

		scraper = None
		if self.mReuse:
			domain = self._scraperDomain(link = link, domain = domain)
			Cloudflare.ReuseLock.acquire()
			if not engine in Cloudflare.ReuseScrapers: Cloudflare.ReuseScrapers[engine] = {}
			if not domain in Cloudflare.ReuseScrapers[engine]: Cloudflare.ReuseScrapers[engine][domain] = []
			if Cloudflare.ReuseScrapers[engine][domain]: scraper = Cloudflare.ReuseScrapers[engine][domain].pop()
			Cloudflare.ReuseLock.release()

		if not scraper: scraper = cloudscraper.create_scraper(interpreter = interpreter, ssl_verify = certificate)

		return scraper, domain

	def _scraperReuse(self, scraper, engine = None, link = None, domain = None):
		if self.mReuse: Cloudflare.ReuseScrapers[engine][self._scraperDomain(link = link, domain = domain)].append(scraper)

	def _scraperDomain(self, link = None, domain = None):
		if domain:
			return domain
		elif link:
			from lib.modules.network import Networker
			return Networker.linkDomain(link = link, subdomain = False, topdomain = True, ip = True, scheme = False)
		return None

	@classmethod
	def _verify(self, certificate):
		return certificate >= Cloudflare.ValidateStrict

	@classmethod
	def _timeout(self):
		return Cloudflare.Timeout

	# The time to sleep between retries. Higher number of retries has a shorter delay than less retries.
	@classmethod
	def _delay(self, retry = None):
		if retry is None: retry = self._settingsRetry()
		delay = (((retry - Cloudflare.RetryMinimum) / float(Cloudflare.RetryMaximum - Cloudflare.RetryMinimum) ) * (Cloudflare.DelayMaximum - Cloudflare.DelayMinimum) + Cloudflare.DelayMinimum)
		delay = Cloudflare.DelayMaximum + Cloudflare.DelayMinimum - delay # Inverse range
		return delay

	@classmethod
	def _error(self, description, link):
		Logger.error('Cloudflare ' + description + ' [' + link + ']')

	@classmethod
	def module(self):
		return Importer.moduleCloudScraper()

	@classmethod
	def prepare(self):
		self.module()

	@classmethod
	def initialize(self):
		cloudflare = Cloudflare()
		if not Settings.getString('network.cloudflare.engine'):
			for item in Cloudflare.Engines:
				if cloudflare.supported(engine = item['type']):
					Settings.set('network.cloudflare.engine', item['name'])
					break

	# Detect whether or not the engine is supported on the current system.
	def supported(self, engine = None):
		if engine is None: engine = self.mEngine
		engine = self._engine(engine)

		if engine == Cloudflare.EngineNative:
			return True
		elif engine == Cloudflare.EngineV8:
			try:
				import v8eval
				v8eval.V8()
				return True
			except:
				return False
		elif engine == Cloudflare.EngineJs2py:
			try:
				js2py = Importer.moduleJs2Py()
				js2py.eval_js('')
				return True
			except:
				return False
		elif engine == Cloudflare.EngineNodejs:
			try:
				return True if Subprocess.output(['node', '-v']) else False
			except:
				return False
		elif engine == Cloudflare.EngineChakra:
			try:
				import os
				import ctypes.util
				for library in ['libChakraCore.so', 'libChakraCore.dylib', 'ChakraCore.dll']:
					if os.path.isfile(os.path.join(os.getcwd(), library)):
						if os.path.join(os.getcwd(), library):
							return True
				if ctypes.util.find_library('ChakraCore'): return True
				return False
			except:
				return False
		return False

	# Verify a single link, or calculate the percentage of bypasses with predefined links.
	def verify(self, link = None, engine = None, retry = None, timeout = None, certificate = None, notification = False, settings = False):
		from lib.modules.interface import Loader, Format, Translation, Dialog

		if link:
			response = self.request(link = link, engine = engine, retry = retry, timeout = timeout, certificate = certificate)
			return True if (response and not self.blocked(response = response)) else False
		else:
			if notification:
				Dialog.notification(title = 35689, message = 35699, icon = Dialog.IconInformation)
				Loader.show()

			cloudscraper = self.module()
			ranks = []
			for link in Cloudflare.Links:
				if System.aborted(): break

				scraper, domain = self._scraper(engine = engine, certificate = certificate)
				if retry is None: retry = self._settingsRetry()
				if timeout is None: timeout = self._timeout()
				delay = self._delay(retry = retry)

				rank = 0
				for i in range(retry):
					if System.aborted(): break

					try:
						response = scraper.get(link, timeout = timeout)
						if not self.blocked(response = response):
							rank = max(0, 1 - (i * 0.1)) # Give lower rank if it is a retry.
							break
					except cloudscraper.exceptions.CloudflareException:
						self._error('Cloudflare Error - Retry ' + str(i + 1), link)
						if i < retry - 1: Time.sleep(delay)
					except Exception as error:
						self._error('Unknown Error', link)
						break
				ranks.append(rank)
				Time.sleep(delay)

			percent = sum(ranks) / len(ranks)

			if notification:
				colors = Format.colorGradientIncrease(100)
				label = Format.font(str(int(percent * 100)) + '%', bold = True, color = colors[int(round(percent * 99))])
				message = (Translation.string(35693) % label) + ' '
				if percent == 1: message += Translation.string(35694)
				else: message += Translation.string(35695)
				Loader.hide()
				Dialog.confirm(title = 35689, message = message)
			if settings: Settings.launch('network.cloudflare.verification')

			return percent

	# Either set a HTTP code and reponse headers dictionary, or pass in the urllib2/requests response/error object.
	@classmethod
	def blocked(self, code = None, headers = None, response = None):
		if not response is None:
			if code is None:
				try: code = response.getcode()
				except: code = response.status_code
			if headers is None:
				try: headers = response.info().dict
				except: headers = response.headers
		if code in [301, 307, 308, 429, 503]:
			for header in headers:
				if header.lower() in Cloudflare.Headers:
					return True
		return False

	# Sometimes the bypass fails, but when retyring again it works.
	# This is due to new Cloudflare V2 challenges, which are currently returned +-80% of the time, whereas the other 20% returns old/solvable challenges.
	def request(self, link, method = None, headers = None, data = None, engine = None, retry = None, timeout = None, certificate = None, redirect = True, log = True):
		# Old bypasser.
		#cfscrape = Importer.moduleCfScrape()
		#scraper = cfscrape.CloudflareScraper()
		#response = scraper.request(method = method, url = link, headers = headers, data = data, timeout = timeout, verify = certificate)

		if log: Logger.log('Trying to bypass Cloudflare [' + link + ']')
		cloudscraper = self.module()

		if certificate is None: certificate = self.mValidate

		scraper, domain = self._scraper(engine = engine, certificate = certificate, link = link)

		if retry is None: retry = self._settingsRetry()
		if timeout is None: timeout = self._timeout()

		delay = self._delay(retry = retry)

		for i in range(retry):
			try:
				scraper.request(method = 'GET' if method is None else method, url = link, headers = headers, data = data, timeout = timeout, verify = self._verify(certificate), allow_redirects = redirect)
				break
			except cloudscraper.exceptions.CloudflareException as error:
				if log: self._error('Cloudflare Error - Retry ' + str(i + 1), link)
				if i < retry - 1: Time.sleep(delay)
				else: raise CloudflareException(error, scraper)
			except Exception as error:
				if log: self._error('Unknown Error', link)
				raise CloudflareException(error, scraper)

		# NB: scraper.response.cookies does not return all of the cookies.
		# Not entirley sure why, but maybe only the cookies of the last request are returned, and not all the cookies in the chain or redirection.
		# Use session.cookies to return ALL cookies.
		try: response = scraper.response
		except: response = None
		try: cookies = scraper.cookies.get_dict()
		except: cookies = None

		self._scraperReuse(scraper = scraper, engine = engine, domain = domain)

		return {'response' : response, 'cookies' : cookies}
