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

from lib.providers.core.newz import ProviderNewznab

class Provider(ProviderNewznab):

	_Link	= ['https://api.nzbgeek.info']

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProviderNewznab.initialize(self,
			name					= 'NZBgeek',
			description				= '{name} is a well-known usenet indexer based on {fork}. The API contains many English titles, but is also a great source for other European languages. {name} offers both trial and premium accounts.',
			rank					= 5,

			link					= Provider._Link,

			# Does not support IMDb for shows, specials, and packs.
			supportShowImdb			= False,

			# Returns indiviual episodes, but not packs.
			supportPackShowTvdb		= False,

			# Returns special episode (S08E00) with ID and "ep=0" or using a title.
			supportPackSeasonImdb	= False,
			supportPackSeasonTvdb	= False,
			supportPackSeasonTitle	= False,
		)
