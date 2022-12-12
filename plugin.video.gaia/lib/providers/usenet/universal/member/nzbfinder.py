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

from lib.providers.core.newz import ProvideNzedb

class Provider(ProvideNzedb):

	_Link	= ['https://nzbfinder.ws']

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProvideNzedb.initialize(self,
			name					= 'NZBFinder',
			description				= '{name} is a well-known usenet indexer based on {fork}. The API contains many English titles, but is also a great source for other European languages. {name} offers both free and premium accounts. The API has limited movie, show and season pack functionality.',
			rank					= 5,

			link					= Provider._Link,

			# Returns indiviual episodes, but not packs when searching with ID.
			# Returns nothing with query.
			supportPackShow			= False,

			# Throws an error when season is not present.
			supportPackShowImdb		= False,
			supportPackShowTvdb		= False,

			# Throws an error when "ep=0".
			supportPackSeasonImdb	= False,
			supportPackSeasonTvdb	= False,
			supportPackSeasonTitle	= False,

			# Does not support the "attrs" parameter, but only the "extended" parameter.
			supportAttributes		= False,
		)
