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

# https://usenet-crawler.com/apihelp

from lib.providers.core.newz import ProviderNewznab

class Provider(ProviderNewznab):

	_Link	= ['https://usenet-crawler.com']

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProviderNewznab.initialize(self,
			name					= 'UsenetCrawler',
			description				= '{name} is a usenet indexer based on {fork}. The API contains many English titles, but is also a great source for other European languages. {name} offers free accounts. {name} has few results and should therefore not be the first choice for a usenet indexer.',
			rank					= 4,
			status					= ProviderNewznab.StatusDead,

			link					= Provider._Link,

			# Packs might not seem to work with the test queries. Try with "24", "The Witcher", and "Doctor Who" and it should work.
		)
