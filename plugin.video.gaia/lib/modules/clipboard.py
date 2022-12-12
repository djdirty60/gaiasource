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

from lib.modules.tools import Logger, Platform
from lib.modules.interface import Translation, Format, Dialog
from lib.modules.external import Importer

class Clipboard(object):

	Error = True

	@classmethod
	def __message(self, id, value, type = None):
		if not type: type = 33035
		type = Translation.string(type).lower()

		message = ''
		if not id is None: message += Format.bold((Translation.string(id) % type) + ':' + Format.newline())
		message += Format.italic(Format.split(value))
		return message

	@classmethod
	def __module(self):
		return Importer.modulePyperClip()

	@classmethod
	def copy(self, value, notify = False, type = None):
		if not value: return False

		try:
			# On certain systems (eg: iOS) the "platform" module in pyperclip fails.
			# Only import here and not globally, to save time because pyperclip takes about 300ms to load.
			self.__module().copy(value)
			id = 33033
		except:
			id = None
			if Platform.systemTypeLinux():
				if Clipboard.Error: # Only print this error once.
					Clipboard.Error = False
					Logger.log('For copying to clipboard on Linux, xsel, xclip, or wl-clipboard must be installed. On Debian/Ubuntu this can be done with: "sudo apt install xsel", "sudo apt install xclip", or "sudo apt install wl-clipboard"', prefix = True, type = Logger.TypeError)

		if notify is True:
			title = Translation.string(33032)
			message = self.__message(id = id, value = value, type = type)
			Dialog.confirm(title = title, message = message)

		return True

	@classmethod
	def paste(self, notify = False, type = None):
		try:
			# Only import here and not globally, to save time because pyperclip takes about 300ms to load.
			value = self.__module().paste()
			if notify == True:
				title = Translation.string(33032)
				message = self.__message(id = 33034, value = value, type = type)
				Dialog.confirm(title = title, message = message)
			return value
		except:
			return None

	@classmethod
	def copyLink(self, value, notify = False):
		type = Translation.string(33381).lower()
		return self.copy(value = value, notify = notify, type = type)

	@classmethod
	def pasteLink(self, notify = False):
		type = Translation.string(33381).lower()
		return self.paste(notify = notify, type = type)

	@classmethod
	def copyName(self, value, notify = False):
		type = Translation.string(33390).lower()
		return self.copy(value = value, notify = notify, type = type)
