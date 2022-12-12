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

from lib.providers.core.html import ProviderHtml, Html, HtmlMain, HtmlLink, HtmlDiv, HtmlHeading5, HtmlListItem
from lib.modules.tools import Regex

class Provider(ProviderHtml):

	_Link					= ['https://bitsearch.to']
	_Path					= 'search'

	_CategoryMovie			= [2, 1] # 2 = Movies, 1 = Other
	_CategoryShow			= [3, 1] # 3 = TV, 1 = Other

	_LimitApproval			= 5000

	_ParameterQuery			= 'q'
	_ParameterSort			= 'sort'
	_ParameterSeeds			= 'seeders'
	_ParameterCategory		= 'category'
	_ParameterPage			= 'page'
	_ParameterSafety		= 'safety' # Does not seem to work at the moment.

	_AttributeContainer		= 'container'
	_AttributeResult		= 'search-result'
	_AttributeInfo			= 'info'
	_AttributeLinks			= 'links'
	_AttributeStats			= 'stats'
	_AttributeTitle			= 'title'
	_AttributePages			= 'pagination'
	_AttributeDisabled		= 'disabled'

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProviderHtml.initialize(self,
			name						= 'BitSearch',
			description					= '{name} is a new {container} site. The site contains results in various languages, but most of them are in English. {name} has many and high-quality results with good metadata.',
			rank						= 5,
			performance					= ProviderHtml.PerformancePoor,

			link						= Provider._Link,

			supportMovie				= True,
			supportShow					= True,
			supportPack					= True,

			offsetStart					= 1,
			offsetIncrease				= 1,

			formatEncode				= ProviderHtml.FormatEncodePlus,

			# Some rare titles like "Xtreme Martial Arts" are often added without a year.
			# Search without the year, since BitSearch is important and typically contains torrents that are not on other sites.
			queryMovie					= ProviderHtml.TermTitle,

			searchQuery					= {
											ProviderHtml.RequestMethod : ProviderHtml.RequestMethodGet,
											ProviderHtml.RequestPath : Provider._Path,
											ProviderHtml.RequestData : {
												Provider._ParameterQuery	: ProviderHtml.TermQuery,
												Provider._ParameterCategory	: ProviderHtml.TermCategory,
												Provider._ParameterPage		: ProviderHtml.TermOffset,
												Provider._ParameterSort		: Provider._ParameterSeeds,
											},
										},
			searchCategoryMovie			= Provider._CategoryMovie,
			searchCategoryShow			= Provider._CategoryShow,

			# They added a new "container" at the top to download their mobile app.
			#extractOptimizeData		= [HtmlMain(), HtmlDiv(class_ = Provider._AttributeContainer)],
			extractOptimizeData			= [HtmlMain()],

			extractList					= HtmlListItem(class_ = Provider._AttributeResult),
			extractLink					= [HtmlDiv(class_ = Provider._AttributeLinks), HtmlLink(href_ = ProviderHtml.ExpressionMagnet, extract = Html.AttributeHref)],
			extractFileName				= [HtmlDiv(class_ = Provider._AttributeInfo), HtmlHeading5(class_ = Provider._AttributeTitle), HtmlLink()], # Extract the link, since there can be a checkmark icon next to the file name.
			extractFileSize				= [HtmlDiv(class_ = Provider._AttributeInfo), HtmlDiv(class_ = Provider._AttributeStats), HtmlDiv(index = 1)],
			extractSourceTime			= [HtmlDiv(class_ = Provider._AttributeInfo), HtmlDiv(class_ = Provider._AttributeStats), HtmlDiv(index = 4)],
			extractSourceSeeds			= [HtmlDiv(class_ = Provider._AttributeInfo), HtmlDiv(class_ = Provider._AttributeStats), HtmlDiv(index = 2)],
			extractSourceLeeches		= [HtmlDiv(class_ = Provider._AttributeInfo), HtmlDiv(class_ = Provider._AttributeStats), HtmlDiv(index = 3)],
			extractSourceApproval		= [HtmlDiv(class_ = Provider._AttributeInfo), HtmlDiv(class_ = Provider._AttributeStats), HtmlDiv(index = 0)],
		)

	##############################################################################
	# PROCESS
	##############################################################################

	def processOffset(self, data, items):
		try:
			next = self.extractHtml(data, [HtmlDiv(class_ = Provider._AttributePages), HtmlLink(index = -1, extract = Html.AttributeClass)])
			if not next or Provider._AttributeDisabled in next: return ProviderHtml.Skip
		except: self.logError()

	def processSourceApproval(self, value, item, details = None, entry = None):
		result = ProviderHtml.ApprovalDefault
		try:
			if value:
				value = value.lower()
				multiplier = 1
				if 'b' in value: multiplier = 1000000000
				elif 'm' in value: multiplier = 1000000
				elif 'k' in value: multiplier = 1000
				value = Regex.extract(data = value, expression = '(\d+(?:\.\d+)?)')
				value = float(value) * multiplier
				result += (1 - result) * max(0, min(1, (float(value) / Provider._LimitApproval)))
		except: self.logError()
		return result
