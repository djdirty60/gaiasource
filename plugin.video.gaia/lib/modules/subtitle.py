# -*- coding: utf-8 -*-

'''
	Gaia Add-on
	Copyright (C) 2016 Gaia

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from lib.modules.tools import Tools, System, Time, Logger, Settings, Language, File, Converter

class Subtitle(object):

	Link = 'http://api.opensubtitles.org/xml-rpc'
	Connection = None
	Token = None
	Cache = {}
	Retry = 3

	##############################################################################
	# RESET
	##############################################################################

	@classmethod
	def reset(self, settings = True):
		Subtitle.Connection = None
		Subtitle.Token = None
		Subtitle.Cache = {}

	##############################################################################
	# GENERAL
	##############################################################################

	@classmethod
	def log(self, message):
		Logger.log('[OPENSUBTITLES] %s' % message)

	##############################################################################
	# ACCOUNT
	##############################################################################

	@classmethod
	def account(self):
		from lib.modules.account import Opensubtitles
		return Opensubtitles()

	@classmethod
	def verify(self, username = None, password = None):
		if self._connection(username = username, password = password, internal = True) and self._token(): return True
		else: return False

	##############################################################################
	# PREPARE
	##############################################################################

	@classmethod
	def prepare(self):
		from xmlrpc.client import ServerProxy

	##############################################################################
	# SEARCH
	##############################################################################

	@classmethod
	def search(self, language, imdb, title = None, season = None, episode = None, retry = Retry):
		try:
			if Tools.isArray(language):
				if Tools.isDictionary(language[0]): language = [i[Language.Code][Language.CodeStream] for i in language]
				language = ','.join(language)

			cacheId = self._cacheId(language, imdb, season, episode)
			cacheData = self._cache(id = cacheId)
			if cacheData: return cacheData

			connection = self._connection()
			token = self._token()
			if connection and token:
				parameters = {'sublanguageid': language}
				if imdb: parameters['imdbid'] = imdb.replace('tt', '')
				elif title: parameters['query'] = title
				if season: parameters['season'] = season
				if episode: parameters['episode'] = episode

				for i in range(retry): # Sometimes the connection fails with a HTTP 503 error. Retry a few times.
					try:
						data = connection.SearchSubtitles(token, [parameters])
						break
					except:
						self.log('Search failure. Retrying request.')
						Time.sleep(2)

				if not self._error(data = data):
					data = self.process(data = data['data'])
					self._cacheSet(id = cacheId, data = data)
					return data
		except: Logger.error()
		return None

	##############################################################################
	# DOWNLOAD
	##############################################################################

	@classmethod
	def download(self, subtitle, retry = Retry):
		try:
			id = subtitle['id']
			cacheId = self._cacheId(id)
			cacheData = self._cache(id = cacheId)
			if cacheData: return cacheData

			connection = self._connection()
			token = self._token()
			if connection and token:
				parameters = [id,]
				data = None
				for i in range(retry): # Sometimes the connection fails with a HTTP 503 error. Retry a few times.
					try:
						data = connection.DownloadSubtitles(token, parameters)
						break
					except:
						self.log('Download failure. Retrying request.')
						Time.sleep(2)

				if not self._error(data = data):
					data = data['data'][0]['data']
					data = Converter.base64From(data)

					import zlib
					data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)

					# Certain languages (eg: Chinese, Hebrew, etc) have to be decoded so that they can be correctly encoded with UTF-8.
					# The encoding is not known, and the data returned by OpenSubtitles does not seem to indicate the encoding.
					# Detect the encoding automatically (best guess).
					encoding = Converter.encodingDetect(data)
					subtitle['decoded'] = None
					if encoding:
						try:
							data = data.decode(encoding)
							subtitle['decoded'] = True
						except:
							Logger.error()
							subtitle['decoded'] = False

					# Add the language code to the filename (with a dot), because Kodi uses this format to detect the language from SRT files.
					# Kodi will remove the code and symbols before displaying it in the Kodi player interface.
					# NB: Do not append the language to the end (eg: filename.eng.srt).
					# In most cases it works, but if the filename contains certain keywords, they will be used as language instead of the last keyword.
					# Eg: "No Time To Die ...srt" will be detected as Norwegian (first word "No").
					# Use the fallback code if available. Kodi cannot detect some variation codes (eg: ZHT). Use the main language code instead.
					# It seems that Kodi can also not detect any other language/country variatios (eg: zh-TW, zh-Hant, zh_TW, zhtw)
					# https://github.com/xbmc/xbmc/issues/15308
					try: language = subtitle['language'][Language.Fallback]
					except: language = subtitle['language'][Language.Code][Language.CodeStream]
					path = '%s.%s.srt' % (language.upper(), subtitle['name'])

					path = System.temporary(directory = 'subtitles', file = path)
					File.writeNow(path, Converter.unicode(data))
					subtitle['path'] = path

					self._cacheSet(id = cacheId, data = subtitle)

			return subtitle
		except: Logger.error()
		return None

	##############################################################################
	# CONNECTION
	##############################################################################

	@classmethod
	def _connection(self, username = None, password = None, internal = False, retry = Retry):
		if Subtitle.Connection is None:
			data = None

			account = self.account()
			if username is None: username = account.dataUsername()
			if password is None: password = account.dataPassword()

			if not internal or (username and password): # If not internal (aka verify), try without credentials, maybe it works like in the past.
				from lib.modules.vpn import Vpn
				if Vpn.killRequest():
					from xmlrpc.client import ServerProxy
					Subtitle.Connection = ServerProxy(Subtitle.Link, verbose = 0)
					for i in range(retry): # Sometimes the connection fails with a HTTP 503 error. Retry a few times.
						# Anonymous login not working anymore.
						#token = Subtitle.Connection.LogIn('', '', 'en', 'XBMC_Subtitles_v1')
						try:
							data = Subtitle.Connection.LogIn(username if username else '', password if password else '', 'en', 'XBMC_Subtitles_v1')
							break
						except:
							self.log('Login failure. Retrying request.')
							Time.sleep(2)

			if self._error(data = data, token = True, notifications = not internal): Subtitle.Connection = False
			elif data and 'token' in data: self._tokenSet(data['token'])

		return Subtitle.Connection

	@classmethod
	def _error(self, data, token = False, notifications = True):
		if not data:
			self._notification(error = 35862, notifications = notifications)
			return False

		error = None
		status = data['status'].lower() if 'status' in data else None

		# If invalid credentials are provided, a token is returned which is not usable. Always check the status.
		# Always try to login first, even without an account. In case anonymous logins are enabled again.
		if (token and not 'token' in data) or (status and 'unauthorized' in status):
			error = 35685 if self.account().authenticated() else 35684

		if error:
			self._notification(error = error, notifications = notifications)
			return True
		else:
			return False

	@classmethod
	def _notification(self, error, notifications = True):
		if notifications and Settings.getInteger('playback.subtitle.notifications') > 0:
			from lib.modules.interface import Dialog
			Dialog.notification(title = 35145, message = error, icon = Dialog.IconError)

	##############################################################################
	# PROCESS
	##############################################################################

	@classmethod
	def process(self, data, integrated = False, universal = True):
		if Tools.isArray(data): return [self.process(data = i, integrated = integrated, universal = universal) for i in data]

		result = {}

		try:
			result['id'] = data['id'] if integrated else data['IDSubtitleFile']
		except:
			Logger.error()
			result['id'] = None

		try:
			result['name'] = data['name'] if integrated else data['MovieReleaseName']
		except:
			Logger.error()
			result['name'] = None

		try:
			result['language'] = data['language'] if integrated else data['SubLanguageID']
			if not Tools.isDictionary(result['language']): result['language'] = Language.language(result['language'], variation = True)
		except:
			Logger.error()
			result['language'] = None
		if universal and not result['language']: result['language'] = Language.universal()

		try:
			result['disc'] = int(data['SubSumCD'])
		except:
			if not integrated: Logger.error()
			result['disc'] = None

		try:
			result['format'] = data['SubFormat'].upper()
		except:
			if not integrated: Logger.error()
			result['format'] = None

		try:
			result['rating'] = 1.0 if integrated else (float(data['SubRating']) / 10.0)
		except:
			Logger.error()
			result['rating'] = None

		try:
			result['votes'] = int(data['SubSumVotes'])
		except:
			if not integrated: Logger.error()
			result['votes'] = None

		try:
			result['downloads'] = int(data['SubDownloadsCnt'])
		except:
			if not integrated: Logger.error()
			result['downloads'] = None

		try:
			result['defective'] = bool(int(data['SubBad']))
		except:
			if not integrated: Logger.error()
			result['defective'] = None

		try:
			result['automatic'] = bool(int(data['SubAutoTranslation']))
		except:
			if not integrated: Logger.error()
			result['automatic'] = None

		try:
			result['impaired'] = data['impaired'] if integrated else bool(int(data['SubHearingImpaired']))
		except:
			Logger.error()
			result['impaired'] = None

		try:
			result['foreign'] = data['forced'] if integrated else bool(int(data['SubForeignPartsOnly']))
		except:
			Logger.error()
			result['foreign'] = None

		try:
			result['trusted'] = bool(int(data['SubFromTrusted']))
		except:
			if not integrated: Logger.error()
			result['trusted'] = None

		try:
			result['featured'] = bool(int(data['SubFeatured']))
		except:
			if not integrated: Logger.error()
			result['featured'] = None

		try:
			result['default'] = data['default'] if integrated else False
		except:
			Logger.error()
			result['default'] = None

		result['integrated'] = integrated

		return result

	##############################################################################
	# TOKEN
	##############################################################################

	@classmethod
	def _token(self):
		return Subtitle.Token

	@classmethod
	def _tokenSet(self, token):
		Subtitle.Token = token

	##############################################################################
	# CACHE
	##############################################################################

	@classmethod
	def _cache(self, id):
		if id:
			try: return Subtitle.Cache[id]
			except: pass
		return None

	@classmethod
	def _cacheSet(self, id, data):
		if id:
			Subtitle.Cache[id] = Tools.copy(data)
			return True
		return False

	@classmethod
	def _cacheId(self, *args):
		return '_'.join([str(i) for i in args])
