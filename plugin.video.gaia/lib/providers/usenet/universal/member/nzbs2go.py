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

# https://tabula-rasa.pw/apihelp

from lib.providers.core.newz import ProviderNntmux

class Provider(ProviderNntmux):

	_Link	= ['https://nzbs2go.com']

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProviderNntmux.initialize(self,
			name					= 'NZBs2GO',
			description				= '{name} is a usenet indexer based on {fork}. The API contains many English titles, but is also a great source for other European languages. {name} offers both free and premium accounts. {name} has few results, search problems with shows, packs, and special episodes, and should therefore not be the first choice for a usenet indexer.',
			rank					= 3,
			status					= ProviderNntmux.StatusDead, # Domain goes to a lading page.

			link					= Provider._Link,

			# Does not support IMDb for shows, specials, and packs.
			supportShowImdb			= False,

			# Does not support searching with title and season/episode.
			supportShowTitle		= False,

			# Returns individual episodes instead of packs when searching by ID.
			supportPackShowImdb		= False,
			supportPackShowTvdb		= False,

			# Throws an HTTP error when searching by ID and "ep=0".
			supportPackSeasonImdb	= False,
			supportPackSeasonTvdb	= False,

			# Throws HTTP error when searching by ID and "season=0".
			supportSpecialImdb		= False,
			supportSpecialTvdb		= False,

			# Does not support the "attrs" parameter, but only the "extended" parameter.
			supportAttributes		= False,
		)
