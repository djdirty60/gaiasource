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

from lib.providers.core.tele import ProviderTele
from lib.providers.core.html import HtmlDiv

class Provider(ProviderTele):

	_Link	= ['https://zetorrents.io']

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProviderTele.initialize(self,
			name					= 'ZeTorrents',
			description				= '{name} is less-known open {container} site from France. The site contains results in various languages, but most of them are in French. {name} requests subpages in order to extract the magnet link and other metadata, which substantially increases scraping time.',
			rank					= 3,
			status					= ProviderTele.StatusDead, # Website does not exist anymore.

			link					= Provider._Link,

			searchQuery				= ProviderTele.Path3,

			extractOptimizeData		= HtmlDiv(class_ = ProviderTele.AttributeContainer3),
			extractOptimizeDetails	= HtmlDiv(class_ = ProviderTele.AttributeContainer3),
		)
