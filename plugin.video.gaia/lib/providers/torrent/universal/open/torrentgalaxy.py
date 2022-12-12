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

from lib.providers.core.html import ProviderHtml, Html, HtmlResultsDiv, HtmlResultDiv, HtmlLink, HtmlDiv, HtmlFont, HtmlListUnordered, HtmlListItem
from lib.modules.tools import Regex

class Provider(ProviderHtml):

	_Link					= ['https://torrentgalaxy.to', 'https://torrentgalaxy.mx', 'https://torrentgalaxy.su']
	_Mirror					= ['https://proxygalaxy.pw']
	_Unblock				= {ProviderHtml.UnblockFormat1 : 'torrentgalaxy', ProviderHtml.UnblockFormat2 : 'torrentgalaxy', ProviderHtml.UnblockFormat3 : 'torrentgalaxy', ProviderHtml.UnblockFormat4 : 'torrentgalaxy'}
	_Path					= 'torrents.php'

	_LimitApproval			= 1000

	# Subcategories
	#_CategoryMovie			= ['c1', 'c3', 'c4', 'c42', 'c45', 'c46'] # c1 = Movies SD, c3 = Movies 4K, c4 = Movies Packs, c42 = Movies HD, c45 = Movies CAM/TS, c46 = Movies Bollywood
	#_CategoryShow			= ['c5', 'c6', 'c41'] # c5 = Shows SD, c6 = Shows Packs, c41 = Shows HD
	_CategoryMovie			= 'Movies'
	_CategoryShow			= 'TV'

	_ParameterQuery			= 'search'
	_ParameterCategory		= 'parent_cat'
	_ParameterPage			= 'page'
	_ParameterSort			= 'sort'
	_ParameterSeeds			= 'seeders'
	_ParameterOrder			= 'order'
	_ParameterDescending	= 'desc'
	_ParameterPorn			= 'nox'

	_AttributeMain			= 'main'
	_AttributeTable			= 'tgxtable'
	_AttributePages			= 'pager'
	_AttributePage			= 'page-item'

	_ExpressionDisabled		= '(disabled)'
	_ExpressionVerified		= '(verified\s*by)'

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProviderHtml.initialize(self,
			name						= 'TorrentGalaxy',
			description					= '{name} is a well-known {container} site. The site contains results in various languages, but most of them are in English. {name} has many high-quality results with good metadata.',
			rank						= 5,
			performance					= ProviderHtml.PerformanceGood,

			link						= Provider._Link,
			mirror						= Provider._Mirror,
			unblock						= Provider._Unblock,

			customVerified				= True,

			supportMovie				= True,
			supportShow					= True,
			supportPack					= True,

			offsetStart					= 0,
			offsetIncrease				= 1,

			formatEncode				= ProviderHtml.FormatEncodePlus,

			searchQuery					= {
											ProviderHtml.RequestMethod : ProviderHtml.RequestMethodGet,
											ProviderHtml.RequestPath : Provider._Path,
											ProviderHtml.RequestData : {
												Provider._ParameterQuery	: ProviderHtml.TermQuery,
												Provider._ParameterCategory	: ProviderHtml.TermCategory,
												Provider._ParameterPage		: ProviderHtml.TermOffset,
												Provider._ParameterSort		: Provider._ParameterSeeds,
												Provider._ParameterOrder	: Provider._ParameterDescending,
												Provider._ParameterPorn		: 1,
											},
										},
			searchCategoryMovie			= Provider._CategoryMovie,
			searchCategoryShow			= Provider._CategoryShow,

			extractOptimizeData			= HtmlDiv(id_ = Provider._AttributeMain), # To detect the last page in processOffset().
			extractList					= [HtmlResultsDiv(class_ = Provider._AttributeTable, start = 1)],
			extractLink					= [HtmlResultDiv(index = 4), HtmlLink(href_ = ProviderHtml.ExpressionMagnet, extract = Html.AttributeHref)],
			extractFileName				= [HtmlResultDiv(index = 3), HtmlLink(extract = Html.AttributeTitle)], # File name from inner text can be cut off (...).
			extractFileSize				= [HtmlResultDiv(index = 7)],
			extractReleaseUploader		= [HtmlResultDiv(index = 6)],
			extractSourceTime			= [HtmlResultDiv(index = 11)],
			extractSourceSeeds			= [HtmlResultDiv(index = 10), HtmlFont(index = 0)],
			extractSourceLeeches		= [HtmlResultDiv(index = 10), HtmlFont(index = 1)],
			extractSourceApproval		= [HtmlResultDiv(index = 9)],
		)

	##############################################################################
	# PROCESS
	##############################################################################

	def processOffset(self, data, items):
		try:
			next = str(self.extractHtml(data, [HtmlListUnordered(id_ = Provider._AttributePages), HtmlListItem(class_ = Provider._AttributePage, index = -1, extract = Html.AttributeClass)]))
			if Regex.match(data = next, expression = Provider._ExpressionDisabled): return ProviderHtml.Skip
		except: self.logError()

	def processBefore(self, item):
		if self.customVerified():
			try:
				verified = self.extractHtml(item, [HtmlResultDiv(index = 1, extract = Provider._ExpressionVerified)])
				if not verified: return ProviderHtml.Skip
			except: self.logError()

	def processSourceApproval(self, value, item, details = None, entry = None):
		result = ProviderHtml.ApprovalDefault
		try:
			value = float(value.replace(',', ''))
			result += ((1 - result) * (value / Provider._LimitApproval))
		except: pass
		return result
