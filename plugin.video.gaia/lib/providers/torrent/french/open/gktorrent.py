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

class Provider(ProviderTele):

	# Do not use https://gktorrent.fr.
	# Although the SHA1 hash can be extracted for some movies, other movies and many shows have a MD5 hash.
	# Hence, too unreliable, and we do not want to generate magnet links with incorrect hashes.

	_Link		= ['https://gktorrents.net', 'https://gktorrent.pw', 'https://gktorrent.io', 'https://gktorrent.co', 'https://gktorrent.net', 'https://gktorrent.tv', 'https://gktorrent.biz', 'https://gktorrent9.fr']
	_Mirror		= ['https://twitter.com/GkTorrents']
	_Unblock	= {ProviderTele.UnblockFormat4 : 'gktorrent'}

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProviderTele.initialize(self,
			name		= 'GkTorrent',
			description	= '{name} is less-known open {container} site from France. The site contains results in various languages, but most of them are in French. {name} requests subpages in order to extract the magnet link and other metadata, which substantially increases scraping time.',
			rank		= 3,

			link		= Provider._Link,
			mirror		= Provider._Mirror,
			unblock		= Provider._Unblock,

			searchQuery	= ProviderTele.Path3,
		)
