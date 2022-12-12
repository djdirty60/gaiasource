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

from lib.modules.database import Database
from lib.modules.tools import Settings, Time, System
from lib.modules.interface import Format, Translation, Dialog, Loader, Directory

class Shortcuts(Database):

	Name = 'shortcuts' # The name of the file. Update version number of the database structure changes.

	ParameterId = 'shortcutId'
	ParameterLocation = 'shortcutLocation'

	LocationDialog = 'dialog'
	LocationMain = 'main'
	LocationTools = 'tools'
	LocationMovies = 'movies'
	LocationMoviesFavourites = 'moviesfavourites'
	LocationShows = 'shows'
	LocationShowsFavourites = 'showsfavourites'
	LocationDocumentaries = 'documentaries'
	LocationDocumentariesFavourites = 'documentariesfavourites'
	LocationShorts = 'shorts'
	LocationShortsFavourites = 'shortsfavourites'

	def __init__(self):
		Database.__init__(self, Shortcuts.Name)

	@classmethod
	def enabled(self):
		return Settings.getBoolean('navigation.general.shortcut')

	@classmethod
	def direct(self, link):
		parameters = System.commandResolve(command = link)
		return parameters and 'action' in parameters and (parameters['action'].startswith('scrape') or parameters['action'].startswith('play'))

	@classmethod
	def parameterize(self, link, location, id):
		return '%s&%s=%s&%s=%s' % (link, Shortcuts.ParameterId, str(id), Shortcuts.ParameterLocation, location)

	@classmethod
	def process(self, parameters):
		if self.enabled():
			id = parameters.get(Shortcuts.ParameterId)
			if not id == None:
				location = parameters.get(Shortcuts.ParameterLocation)
				self().update(id = id, location = location)

	def _initialize(self):
		self._createAll('''
			CREATE TABLE IF NOT EXISTS %s
			(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				link TEXT,
				name TEXT,
				time INTEGER,
				count INTEGER,
				UNIQUE(link)
			);
			''',
			[Shortcuts.LocationDialog, Shortcuts.LocationMain, Shortcuts.LocationTools, Shortcuts.LocationMovies, Shortcuts.LocationMoviesFavourites, Shortcuts.LocationShows, Shortcuts.LocationShowsFavourites, Shortcuts.LocationDocumentaries, Shortcuts.LocationDocumentariesFavourites, Shortcuts.LocationShorts, Shortcuts.LocationShortsFavourites]
		)

	def insert(self, location, link, name):
		self._insert('''
			INSERT INTO %s
			(link, name, time, count)
			VALUES
			(?, ?, ?, 0);
			'''
			% location,
			parameters = (link, name, Time.timestamp())
		)

	def update(self, location, id):
		self._update('UPDATE %s SET count = count + 1 WHERE id = %s;' % (location, str(id)))

	def delete(self, location, id):
		self._delete('DELETE FROM %s WHERE id = %s;' % (location, str(id)))

	def retrieveSingle(self, location, id):
		return self._selectSingle('SELECT id, link, name, time, count FROM %s WHERE id = %s;' % (location, str(id)))

	def retrieve(self, location):
		return self._select('SELECT id, link, name, time, count FROM %s ORDER BY count DESC;' % location)

	def open(self, location, id):
		self.update(location = location, id = id)
		link = self.retrieveSingle(location = location, id = id)[1] # Do not unprepare here, otherwise shortcuts directly to movies/espideos don't work.
		if self.direct(link): # Run plugin directly if it searches videos (that is a movie/episode), otherwise an empty window shows in the background.
			System.executePlugin(command = link)
		else: # All other windows must be forcefully refreshed.
			System.window(command = link, sleep = 1, refresh = True)

	def show(self, location = None, id = None, link = None, name = None, create = False, delete = False):
		items = [Format.bold(35135)]
		if create: items.append(Format.bold(35120))
		if delete: items.append(Format.bold(35134))

		Loader.hide()
		choice = Dialog.select(title = 35119, items = items)
		if choice >= 0:
			if choice == 0: self.showOpen()
			elif choice == 1:
				if create: self.showCreate(link = link, name = name)
				else: self.showDelete(id = id, location = location)

	def showCreate(self, link, name = None, refresh = False):
		items = [
			Format.bold(35525),
			Format.bold(35121),
			Format.bold(35137),
			Format.bold(35122),
			Format.bold(35123),
			Format.bold(35124),
			Format.bold(35125),
			Format.bold(35126),
			Format.bold(35127),
			Format.bold(35128),
			Format.bold(35129),
		]
		choice = Dialog.select(title = 35130, items = items)
		if choice >= 0:
			if choice == 0: location = Shortcuts.LocationDialog
			elif choice == 1: location = Shortcuts.LocationMain
			elif choice == 2: location = Shortcuts.LocationTools
			elif choice == 3: location = Shortcuts.LocationMovies
			elif choice == 4: location = Shortcuts.LocationMoviesFavourites
			elif choice == 5: location = Shortcuts.LocationShows
			elif choice == 6: location = Shortcuts.LocationShowsFavourites
			elif choice == 7: location = Shortcuts.LocationDocumentaries
			elif choice == 8: location = Shortcuts.LocationDocumentariesFavourites
			elif choice == 9: location = Shortcuts.LocationShorts
			elif choice == 10: location = Shortcuts.LocationShortsFavourites

			if not name or name == '': name = Translation.string(35131)
			name = Dialog.input(title = 35132, type = Dialog.InputAlphabetic, default = name)
			if not name or name == '': name = Translation.string(35131)

			self.insert(location = location, link = link, name = name)
			if refresh: Directory.refresh()
			Dialog.notification(title = 35119, message = Translation.string(35133) % items[choice], icon = Dialog.IconSuccess)

	def showDelete(self, location, id, refresh = True):
		self.delete(location = location, id = id)
		if refresh: Directory.refresh()
		Dialog.notification(title = 35119, message = Translation.string(35136), icon = Dialog.IconSuccess)

	def showOpen(self):
		location = [
			(35525, Shortcuts.LocationDialog),
			(35121, Shortcuts.LocationMain),
			(35137, Shortcuts.LocationTools),
			(35122, Shortcuts.LocationMovies),
			(35123, Shortcuts.LocationMoviesFavourites),
			(35125, Shortcuts.LocationShows),
			(35124, Shortcuts.LocationShowsFavourites),
			(35126, Shortcuts.LocationDocumentaries),
			(35127, Shortcuts.LocationDocumentariesFavourites),
			(35128, Shortcuts.LocationShorts),
			(35129, Shortcuts.LocationShortsFavourites),
		]
		items = []
		ids = []
		locations = []
		for l in location:
			entries = self.retrieve(location = l[1])
			label = Format.bold(Translation.string(l[0]) + ': ')
			for entry in entries:
				items.append(label + entry[2])
				ids.append(entry[0])
				locations.append(l[1])
		choice = Dialog.select(title = 35130, items = items)
		if choice >= 0: self.open(location = locations[choice], id = ids[choice])
