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

from lib.providers.core.html import ProviderHtml, Html, HtmlResults, HtmlResult, HtmlLink, HtmlDiv, HtmlSpan, HtmlBold, HtmlTableCell, HtmlAny

class Provider(ProviderHtml):

	_Link					= ['http://rutor.info', 'http://rutor.is', 'http://zerkalo-rutor.org']
	_Mirror					= ['http://rutororg-mirror.ru']
	_Unblock				= {ProviderHtml.UnblockFormat4 : 'rutor'}

	_Path					= 'search/%s/0/000/2/%s'

	_AttributeContainer		= 'index'
	_AttributeSeeds			= 'green'
	_AttributeLeeches		= 'red'

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProviderHtml.initialize(self,
			name					= 'Rutor',
			description				= '{name} is one of the oldest and most well-known open {container} sites from Russia. The site contains results in various languages, but most of them are in Italian.',
			rank					= 4,
			performance				= ProviderHtml.PerformanceGood,

			link					= Provider._Link,
			mirror					= Provider._Mirror,
			unblock					= Provider._Unblock,

			offsetStart				= 0,
			offsetIncrease			= 1,

			formatEncode			= ProviderHtml.FormatEncodeQuote,

			searchQuery				= Provider._Path % (ProviderHtml.TermOffset, ProviderHtml.TermQuery),

			extractOptimizeData		= HtmlDiv(id_ = Provider._AttributeContainer),
			extractList				= [HtmlResults(index = 0, start = 1)],
			extractLink				= [HtmlResult(index = 1), HtmlLink(href_ = ProviderHtml.ExpressionMagnet, extract = Html.AttributeHref)],
			extractFileName			= [HtmlResult(index = 1)],
			extractFileSize			= [HtmlResult(index = 3)],
			extractSourceTime		= [HtmlResult(index = 0)],
			extractSourceSeeds		= [HtmlResult(index = 4), HtmlSpan(class_ = Provider._AttributeSeeds)],
			extractSourceLeeches	= [HtmlResult(index = 4), HtmlSpan(class_ = Provider._AttributeLeeches)],
		)

	##############################################################################
	# PROCESS
	##############################################################################

	def processOffset(self, data, items):
		try:
			last = self.extractHtml(data, [HtmlBold(index = 0), HtmlAny(index = -1, extract = Html.ParseTag)])
			if not last == Html.TagLink: return ProviderHtml.Skip
		except: self.logError()

	def processItem(self, item):
		try:
			cells = self.extractHtml(item, [HtmlTableCell()])
			if len(cells) < 5: item.insert(2, self.create(Html.TagTableCell)) # Some items do not have a comment column.
		except: self.logError()
		return item
