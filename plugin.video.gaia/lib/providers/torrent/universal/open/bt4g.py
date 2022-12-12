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

from lib.providers.core.html import ProviderHtml, Html, HtmlLink, HtmlDiv, HtmlSpan, HtmlMain, HtmlBold, HtmlListUnordered, HtmlListItem

class Provider(ProviderHtml):

	_Link					= ['https://bt4g.org']
	_Unblock				= {ProviderHtml.UnblockFormat2 : 'bt4g', ProviderHtml.UnblockFormat3 : 'bt4g'}
	_Path					= 'movie/search/%s/%s/%s' # The "movie" category is actually the "video" category containing both movies and shows.

	_ParameterSort			= 'byseeders'

	_AttributeContainer		= 'container'
	_AttributeRow			= 'row'
	_AttributeColumn		= 'col'
	_AttributeSize			= 'red-pill'
	_AttributeSeeds			= 'seeders'
	_AttributeLeeches		= 'leechers'
	_AttributePages			= 'pagination'
	_AttributeActive		= 'active'

	_ExpressionLink			= 'magnet/' + ProviderHtml.ExpressionSha

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProviderHtml.initialize(self,
			name					= 'BT4G',
			description				= '{name} is a well-known {container} site. The site contains results in various languages, but most of them are in English. {name} has strong Cloudflare protection that might not be bypassable and cause scraping to fail.',
			rank					= 3,
			performance				= ProviderHtml.PerformanceGood - ProviderHtml.PerformanceStep,
			status					= ProviderHtml.StatusImpaired, # Cloudflare.

			link					= Provider._Link,
			unblock					= Provider._Unblock,

			supportMovie			= True,
			supportShow				= True,
			supportPack				= True,

			offsetStart				= 1,
			offsetIncrease			= 1,

			formatEncode			= ProviderHtml.FormatEncodeQuote,

			searchQuery				= Provider._Path % (ProviderHtml.TermQuery, Provider._ParameterSort, ProviderHtml.TermOffset),

			extractOptimizeData		= HtmlMain(),
			extractList				= [HtmlDiv(class_ = Provider._AttributeContainer), HtmlDiv(class_ = Provider._AttributeRow, start = 2, recursive = False), HtmlDiv(class_ = Provider._AttributeColumn), HtmlDiv(start = 1)],
			extractHash				= [HtmlLink(href_ = Provider._ExpressionLink, extract = Provider._ExpressionLink)],
			extractFileName			= [HtmlLink(href_ = Provider._ExpressionLink, extract = Html.AttributeTitle)],
			extractFileSize			= [HtmlBold(class_ = Provider._AttributeSize)],
			extractSourceTime		= [HtmlSpan(index = 1, recursive = False), HtmlBold()],
			extractSourceSeeds		= [HtmlBold(id_ = Provider._AttributeSeeds)],
			extractSourceLeeches	= [HtmlBold(id_ = Provider._AttributeLeeches)],
		)

	##############################################################################
	# PROCESS
	##############################################################################

	def processOffset(self, data, items):
		try:
			next = self.extractHtml(data, [HtmlListUnordered(class_ = Provider._AttributePages), HtmlListItem(index = -1, extract = Html.AttributeClass)])
			if not next or Provider._AttributeActive in next: return ProviderHtml.Skip
		except: self.logError()
