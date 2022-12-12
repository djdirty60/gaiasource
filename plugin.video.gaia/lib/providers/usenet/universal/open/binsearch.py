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

from lib.providers.core.usenet import ProviderUsenetHtml
from lib.providers.core.html import Html, HtmlResults, HtmlResult, HtmlForm, HtmlInput, HtmlLink
from lib.modules.tools import Regex

class Provider(ProviderUsenetHtml):

	_Link					= ['https://binsearch.info']
	_PathDownload			= '/?action=nzb&%s=on'

	_LimitOffset			= 250

	_ParameterQuery			= 'q'
	_ParameterOffset		= 'min'
	_ParameterLimit			= 'max'
	_ParameterLimitAge		= 'adv_age'
	_ParameterLimitSize		= 'xminsize'
	_ParameterDate			= 'date'
	_ParameterFormat		= 'postdate'
	_ParameterSort			= 'adv_sort'

	_AttributeResults		= 'r2'
	_AttributeSubject		= 's'
	_AttributeDescription	= 'd'
	_AttributeMenu			= 'xMenuT'

	_ExpressionNext			= '(>|&gt;)'
	_ExpressionSize			= 'size\s*:\s*(.+?)(?:$|,)'
	_ExpressionParts		= 'parts\s*available:\s*(\d+)\s*\/\s*(\d+)'

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		query = {
			Provider._ParameterQuery	: ProviderUsenetHtml.TermQuery,
			Provider._ParameterOffset	: ProviderUsenetHtml.TermOffset,
			Provider._ParameterLimit	: Provider._LimitOffset,
			Provider._ParameterSort		: Provider._ParameterDate,
			Provider._ParameterFormat	: Provider._ParameterDate,
		}

		age = self.customTime(days = True)
		if age: query[Provider._ParameterLimitAge] = age
		size = self.customSize()
		if size: query[Provider._ParameterLimitSize] = size

		ProviderUsenetHtml.initialize(self,
			name						= 'Binsearch',
			description					= '{name} is one of the oldest open usenet indexers. {name} has mostly incomplete {containers}, duplicate results, missing metadata, and incorrect file sizes, and should therefore be avoided if possible.',
			rank						= 1,
			performance					= ProviderUsenetHtml.PerformanceMedium - ProviderUsenetHtml.PerformanceStep,

			link						= Provider._Link,

			customIncomplete			= True,

			supportMovie				= True,
			supportShow					= True,
			supportPack					= True,

			offsetStart					= 0,
			offsetIncrease				= Provider._LimitOffset,

			formatEncode				= ProviderUsenetHtml.FormatEncodePlus,

			searchQuery					= {
											ProviderUsenetHtml.RequestMethod : ProviderUsenetHtml.RequestMethodGet,
											ProviderUsenetHtml.RequestData : query,
										},

			extractParser				= ProviderUsenetHtml.ParserHtml5, # Contains many unclosed tags. Use lenient parsing.
			extractOptimizeData			= HtmlForm(), # To detect the last page in processOffset().
			extractList					= [HtmlResults(id_ = Provider._AttributeResults, start = 1)],
			extractLink					= [HtmlResult(index = 1), HtmlInput(extract = Html.AttributeName)],
			extractIdLocal				= [HtmlResult(index = 1), HtmlInput(extract = Html.AttributeName)],
			extractFileName				= [HtmlResult(index = 2), Html(class_ = Provider._AttributeSubject)],
			extractFileSize				= [HtmlResult(index = 2), Html(class_ = Provider._AttributeDescription, extract = Provider._ExpressionSize)],
			extractReleaseUploader		= [HtmlResult(index = 3)],
			extractSourceTime			= [HtmlResult(index = 5)],
		)

	##############################################################################
	# PROCESS
	##############################################################################

	def processOffset(self, data, items):
		try:
			pages = self.extractHtml(data, [Html(class_ = Provider._AttributeMenu, index = -1), HtmlLink(index = -1, extract = Html.ParseText)])
			if pages:
				next = False
				for page in pages:
					if page == Provider._ExpressionNext:
						next = True
						break
				if not next: return ProviderUsenetHtml.Skip
		except: pass

	def processBefore(self, item):
		if self.customIncomplete():
			try:
				parts = self.extractHtml(item, [HtmlResult(index = 2), Html(class_ = Provider._AttributeDescription, extract = Html.ParseText)])
				parts = Regex.extract(data = parts, expression = Provider._ExpressionParts, group = None, all = True)[0]
				if int(parts[0]) < int(parts[1]): return ProviderUsenetHtml.Skip
			except: pass

	def processLink(self, value, item, details = None, entry = None):
		if not value: return ProviderUsenetHtml.Skip
		return self.linkCurrent(path = Provider._PathDownload % value)
