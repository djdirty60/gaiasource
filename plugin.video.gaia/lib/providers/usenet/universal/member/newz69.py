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

# https://newz69.keagaming.com/apihelp
# Most TV searches from newz.py do not work. Try "South Park" and "Walking Dead" instead.

from lib.providers.core.newz import ProviderNewznab

class Provider(ProviderNewznab):

	_Link	= ['https://newz69.keagaming.com']

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProviderNewznab.initialize(self,
			name					= 'Newz69',
			description				= '{name} is a usenet indexer based on {fork}. The API contains many English titles, but is also a great source for other European languages. {name} offers free accounts. {name}\'s API has a number of bugs and timeout issues and should therefore not be the first choice for a usenet indexer',
			rank					= 3,

			link					= Provider._Link,

			supportShowTitle		= False,

			supportPackShowTvdb		= False,

			supportPackSeasonTitle	= False,

			supportSpecialTitle		= False,
		)
