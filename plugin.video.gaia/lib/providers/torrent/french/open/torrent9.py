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

	_Link		= {
					ProviderTele.Version1 : ['https://torrent9.gg', 'https://torrent9.is', 'https://torrent9.to', 'https://torrent9.site', 'https://torrent09.uno'],
					ProviderTele.Version2 : ['https://torrent9.so', 'https://torrent9.cz'],
				}
	_Unblock	= {
					ProviderTele.Version1 : {ProviderTele.UnblockFormat1 : 'torrent9'},
					ProviderTele.Version2 : {ProviderTele.UnblockFormat4 : 'torrent9'},
				}

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		version = self.customVersion()
		if version == ProviderTele.Version1:
			offsetIncrease	= 1
			formatEncode	= ProviderTele.FormatEncodeMinus
			query			= ProviderTele.Path2
		elif version == ProviderTele.Version2:
			offsetIncrease	= True
			formatEncode	= ProviderTele.FormatEncodeQuote
			query			= ProviderTele.Path3

		ProviderTele.initialize(self,
			name					= 'Torrent9',
			description				= '{name} is well-known open {container} site from France. The site contains results in various languages, but most of them are in French. {name} requests subpages in order to extract the magnet link and other metadata, which substantially increases scraping time.',
			rank					= 3,

			link					= Provider._Link[version],
			unblock					= Provider._Unblock[version],

			customVersion			= 2,

			offsetStart				= 1,
			offsetIncrease			= offsetIncrease,

			formatEncode			= formatEncode,

			searchQuery				= query,

			extractOptimizeData		= HtmlDiv(class_ = ProviderTele.AttributeContainer2),
			extractOptimizeDetails	= HtmlDiv(class_ = ProviderTele.AttributeDetails2),
		)
