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

from lib.modules import tools
from lib.modules import network

class Core(object):

	# Modes
	ModeTorrent = 'torrent'
	ModeUsenet = 'usenet'
	ModeHoster = 'hoster'

	ErrorUnknown = 'unknown'
	ErrorUnavailable = 'unavailable'
	ErrorExternal = 'external'
	ErrorCancel = 'cancel'
	ErrorSelection = 'selection' # No file selected from list of items.
	ErrorPack = 'pack' # No file can be found in the pack that matches the title and year/season/episode.

	Exclusions = ('.txt', '.nfo', '.srt', '.nzb', '.torrent', '.rtf', '.exe', '.zip', '.7z', '.rar', '.par', '.pdf', '.doc', '.docx', '.ini', '.lnk', '.csvs', '.xml', '.html', '.json', '.jpg', '.jpeg', '.png', '.tiff', '.gif', '.bmp', '.md5', '.sha')

	##############################################################################
	# CONSTRUCTOR
	##############################################################################

	def __init__(self, id, name, link):
		self.mId = id
		self.mName = name
		self.mLink = link

	def clone(self):
		return self.__class__()

	##############################################################################
	# RESET
	##############################################################################

	@classmethod
	def reset(self, settings = True):
		pass

	##############################################################################
	# COMPONENTS
	##############################################################################

	@classmethod
	def interface(self):
		from lib.debrid.debrid import Debrid
		return Debrid._instance(id = self.Id, type = Debrid.TypeInterface)

	@classmethod
	def handle(self):
		from lib.debrid.debrid import Debrid
		return Debrid._instance(id = self.Id, type = Debrid.TypeHandle)

	##############################################################################
	# GENERAL
	##############################################################################

	def id(self):
		return self.mId

	def name(self):
		return self.mName

	def link(self):
		return self.mLink

	##############################################################################
	# ACCOUNT
	##############################################################################

	# Virtual
	def accountEnabled(self):
		return False

	# Virtual
	def accountValid(self):
		return False

	def accountAuthentication(self, settings = False):
		self.interface().accountAuthentication(settings = settings)

	##############################################################################
	# SERVICES
	##############################################################################

	# Virtual
	def servicesList(self, onlyEnabled = False):
		return []

	##############################################################################
	# ADD
	##############################################################################

	@classmethod
	def addError(self, error = ErrorUnknown):
		return self.addResult(error = error if error else Core.ErrorUnknown)

	@classmethod
	def addResult(self, error = None, id = None, link = None, notification = None, items = None, category = None, extra = None, loader = None, new = None, strict = False):
		if error is None:
			# Link can be to an external Kodi addon.
			if not link or (not network.Networker.linkIs(link) and not link.startswith('plugin:')):
				if strict and items and 'files' in items and items['files']: error = Core.ErrorPack
				else: error = Core.ErrorUnknown

		result = {
			'success' : (error is None),
			'error' : error,
			'id' : id,
			'link' : link,
			'items' : items,
			'notification' : notification,
			'category' : category,
			'loader' : loader,
			'new' : new,
		}
		if extra:
			for key, value in extra.items():
				result[key] = value
		return result

	##############################################################################
	# DELETE
	##############################################################################

	# Virtual
	def deletePlayback(self, id, pack = None, category = None):
		pass

	##############################################################################
	# CACHED
	##############################################################################

	@classmethod
	def cachedModes(self):
		return {}

	# Virtual
	def cached(self, id, timeout = None, callback = None, sources = None):
		pass

	##############################################################################
	# STREAMING
	##############################################################################

	def streaming(self, mode):
		if tools.Settings.getInteger('stream.general.handle') == 2:
			if tools.Settings.getInteger('stream.general.handle.%s' % mode) == 0: return False

		setting = tools.Settings.getInteger('stream.gaia.handle')
		if setting == 2:
			if tools.Settings.getInteger('stream.gaia.handle.%s' % mode) >= 1: return True
		elif setting >= 1:
			return True

		return False

	def streamingTorrent(self):
		return self.streaming(Core.ModeTorrent)

	def streamingUsenet(self):
		return self.streaming(Core.ModeUsenet)

	def streamingHoster(self):
		return self.streaming(Core.ModeHoster)
