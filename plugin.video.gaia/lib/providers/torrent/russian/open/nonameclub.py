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

from lib.providers.core.html import ProviderHtml, Html, HtmlResults, HtmlResult, HtmlTable, HtmlLink, HtmlUnderlined

class Provider(ProviderHtml):

	_Link					= ['https://nnmclub.to', 'https://nnm-club.me', 'https://nnm-club.ro']
	_Mirror					= ['https://torrends.to/proxy/nnm-club']

	_PathForum				= 'forum'
	_PathTracker			= 'tracker.php'

	# NoNameClub has a connection limit.
	# If there are too many concurrent connections to the server, the are dropped/aborted.
	# This is important when requesting subpages.
	# 7 is still to high. The last few requests, out of the 50 detail links in thew table, are dropped.
	# This probably indicates there is rather a rate limit instead of a fixed number of concurrent connection limit.
	# 5 seems to work well, even with multiple pack queries.
	_LimitRequests			= 5

	_LimitApproval			= 5

	_ParameterQuery			= 'nm'
	_ParameterCategory		= 'shc'
	_ParameterForum			= 'shf'
	_ParameterSpeed			= 'shs'
	_ParameterThanks		= 'sht'
	_ParameterUploader		= 'sha'
	_ParameterRating		= 'shr'
	_ParameterSort			= 'o'
	_ParameterSeeds			= '10'
	_ParameterOrder			= 's'
	_ParameterDescending	= '2'
	_ParameterActive		= 'a'
	_ParameterMine			= 'my'
	_ParameterSeeding		= 'sd'
	_ParameterNew			= 'n'
	_ParameterApproved		= 'ta'
	_ParameterSource		= 'sns'
	_ParameterStatus		= 'sds'
	_ParameterIgnore		= '-1'
	_ParameterYes			= '1'
	_ParameterNo			= '0'

	_AttributeTable			= 'tablesorter'
	_AttributeForum			= 'forumline'
	_AttributeDetails		= 'btTbl'

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProviderHtml.initialize(self,
			name					= 'NoNameClub',
			description				= '{name} is well-known open {container} site from Russia. The site contains results in various languages, but most of them are in Russian. {name} does not support paging and results might therefore be limited.',
			rank					= 3,
			performance				= ProviderHtml.PerformanceBad,

			link					= Provider._Link,
			mirror					= Provider._Mirror,

			requestCount			= Provider._LimitRequests,

			formatEncode			= ProviderHtml.FormatEncodePlus,
			formatSet				= ProviderHtml.FormatSetWin1251, # Does not work with UTF-8 encoding, which ends up with a different URL-encoded query than the website.

			searchQuery				= {
										ProviderHtml.RequestMethod : ProviderHtml.RequestMethodPost,
										ProviderHtml.RequestPath : [Provider._PathForum, Provider._PathTracker],
										ProviderHtml.RequestData : {
											Provider._ParameterQuery	: ProviderHtml.TermQuery,
											Provider._ParameterSort		: Provider._ParameterSeeds,
											Provider._ParameterOrder	: Provider._ParameterDescending,
											Provider._ParameterUploader	: Provider._ParameterYes,
											Provider._ParameterRating	: Provider._ParameterYes,
											Provider._ParameterCategory	: Provider._ParameterNo,
											Provider._ParameterForum	: Provider._ParameterNo,
											Provider._ParameterSpeed	: Provider._ParameterNo,
											Provider._ParameterThanks	: Provider._ParameterNo,
											Provider._ParameterActive	: Provider._ParameterNo,
											Provider._ParameterMine		: Provider._ParameterNo,
											Provider._ParameterSeeding	: Provider._ParameterNo,
											Provider._ParameterNew		: Provider._ParameterNo,
											Provider._ParameterApproved	: Provider._ParameterIgnore,
											Provider._ParameterSource	: Provider._ParameterIgnore,
											Provider._ParameterStatus	: Provider._ParameterIgnore,
										},
									},

			extractList				= [HtmlResults(class_ = Provider._AttributeTable)],
			extractDetails			= [HtmlResult(index = 1), HtmlLink(extract = Html.AttributeHref)],
			extractLink				= [ProviderHtml.Details, HtmlTable(class_ = Provider._AttributeForum), HtmlTable(class_ = Provider._AttributeDetails), HtmlLink(href_ = ProviderHtml.ExpressionMagnet, extract = Html.AttributeHref)],
			extractFileName			= [HtmlResult(index = 1), HtmlLink()],
			extractFileSize			= [HtmlResult(index = 4), HtmlUnderlined()],
			extractSourceTime		= [HtmlResult(index = 8), HtmlUnderlined()],
			extractSourceApproval	= [HtmlResult(index = 9), HtmlUnderlined()],
			extractSourceSeeds		= [HtmlResult(index = 5)],
			extractSourceLeeches	= [HtmlResult(index = 6)],
			extractReleaseUploader	= [HtmlResult(index = 2)],
		)

	##############################################################################
	# PROCESS
	##############################################################################

	def processDetails(self, value, item):
		return [Provider._PathForum, value] if value else value

	def processSourceApproval(self, value, item, details = None, entry = None):
		result = ProviderHtml.ApprovalDefault
		try: result += ((1 - result) * (float(value) / Provider._LimitApproval))
		except: pass
		return result
