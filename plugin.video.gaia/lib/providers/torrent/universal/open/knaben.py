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

# https://knaben.eu/rss/
# NB: Do not use the API/RSS-feed, because:
#	1. Some missing attrributes (eg seeds/leeches)
#	2. Results limited to 400 links without paging.
#	3. Returned data is XML with inner CDATA, HTML, and text. Makes it more difficult to process.

from lib.providers.core.html import ProviderHtml, Html, HtmlLink, HtmlDiv, HtmlResultsTable, HtmlResult
from lib.modules.tools import Regex, Converter

class Provider(ProviderHtml):

	_Link					= ['https://knaben.eu', 'https://knaben.xyz', 'https://knaben.cc', 'https://knaben.org']
	_Path					= 'search/%s/%s/%s/%s'

	_CategoryMovie			= ['3000000', '6000000'] # Movies = 3000000, Anime = 6000000
	_CategoryShow			= ['2000000', '6000000'] # TV = 2000000, Anime = 6000000

	_ParameterSeeds			= 'seeders'

	_CookieFilter			= 'filter'
	_CookieSearch			= 'search'
	_CookieFast				= 'fast'
	_CookieLive				= 'live'
	_CookieUnsafe			= 'unsafe'
	_CookieAdult			= 'hideXXX'

	_AttributeMain			= 'invisdiv'
	_AttributeTable			= 'caption-top'
	_AttributePages			= 'pageNumbers'

	_ExpressionType			= '(?:^|\s|\-|:|>|\/)\s*(video|movie|tv|show|episode|hd|4k|3d|hdr|x264|x265|other|foreign)'
	_ExpressionSize			= '(\d+)\s'

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		# Live search is slower, but returns more links, especially for newer content.
		#cookies = {Provider._CookieSearch : Provider._CookieFast}
		cookies = {Provider._CookieSearch : Provider._CookieLive}

		if not self.customVerified(): cookies[Provider._CookieUnsafe] = True
		if not self.customAdult(): cookies[Provider._CookieAdult] = True
		cookies = Converter.quoteTo(Converter.jsonTo(cookies))

		ProviderHtml.initialize(self,
			name						= 'Knaben',
			description					= '{name} is a less-known {container} site that indexes other {container} sites. The site contains results in various languages, but most of them are in English. {name} has many links that are unusable and are therefore excluded from the results.',
			rank						= 3,
			performance					= ProviderHtml.PerformanceGood,

			link						= Provider._Link,

			customVerified				= True,
			customAdult					= True,

			supportMovie				= True,
			supportShow					= True,
			supportPack					= True,

			offsetStart					= 1,
			offsetIncrease				= 1,

			formatEncode				= ProviderHtml.FormatEncodeQuote,

			searchQuery					= {
											ProviderHtml.RequestMethod : ProviderHtml.RequestMethodGet,
											ProviderHtml.RequestPath : Provider._Path % (ProviderHtml.TermQuery, ProviderHtml.TermCategory, ProviderHtml.TermOffset, Provider._ParameterSeeds),
											ProviderHtml.RequestCookies : {Provider._CookieFilter : cookies},
										},
			searchCategoryMovie			= Provider._CategoryMovie,
			searchCategoryShow			= Provider._CategoryShow,

			#extractOptimizeData			= HtmlDiv(id_ = Provider._AttributeMain), # Layout was changed. No parent div can be uniquely identified anymore.
			extractList					= HtmlResultsTable(class_ = Provider._AttributeTable),
			extractLink					= [HtmlResult(index = 1), HtmlLink(href_ = ProviderHtml.ExpressionMagnet, extract = Html.AttributeHref)],
			extractFileName				= [HtmlResult(index = 1), HtmlLink(extract = Html.ParseTextNested)],
			extractFileSize				= [HtmlResult(index = 2, extract = [Html.AttributeTitle, Provider._ExpressionSize])],
			extractSourceTime			= [HtmlResult(index = 3, extract = Html.AttributeTitle)],
			extractSourceSeeds			= [HtmlResult(index = 4, extract = Html.ParseTextNested)],
			extractSourceLeeches		= [HtmlResult(index = 5, extract = Html.ParseTextNested)],
		)

	##############################################################################
	# PROCESS
	##############################################################################

	# No way to detect the last page anymore.
	'''def processOffset(self, data, items):
		try:
			next = self.extractHtml(data, [HtmlDiv(class_ = Provider._AttributePages), HtmlLink(index = -1, extract = Html.AttributeHref)])
			if not next: return ProviderHtml.Skip
		except: self.logError()'''

	def processBefore(self, item):
		type = self.extractHtml(item, [HtmlResult(index = 0, extract = Html.ParseTextNested)])
		if not type or not Regex.match(data = type, expression = Provider._ExpressionType): return ProviderHtml.Skip

	def processLink(self, value, item, details = None, entry = None):
		# A lot of the entries (eg 1337x, RuTracker, etc) do not have a magnet, but a HTTP link that resolves to a magnet.
		return value if value else ProviderHtml.Skip
