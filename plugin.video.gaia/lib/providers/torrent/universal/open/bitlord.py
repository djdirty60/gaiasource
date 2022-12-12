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

from lib.providers.core.json import ProviderJson

class Provider(ProviderJson):

	_Link					= ['https://bitlordsearch.com']
	_Path					= 'get_list'

	_LimitOffset			= 1000

	_CategoryMovie			= '3'
	_CategoryShow			= '4'

	_ParameterQuery			= 'query'
	_ParameterOffset		= 'offset'
	_ParameterLimit			= 'limit'
	_ParameterDescending	= 'desc'
	_ParameterSeeds			= 'seeds'
	_ParameterAll			= '4'
	_ParameterTrue			= 'true'
	_ParameterFalse			= 'false'
	_ParameterSort			= 'filters[field]'
	_ParameterOrder			= 'filters[sort]'
	_ParameterTime			= 'filters[time]'
	_ParameterCategory		= 'filters[category]'
	_ParameterPorn			= 'filters[adult]'
	_ParameterSpam			= 'filters[risky]'

	_AttributeList			= 'content'
	_AttributId				= 'id'
	_AttributeLink			= 'magnet'
	_AttributeName			= 'name'
	_AttributeSize			= 'size'
	_AttributeTime			= 'age'
	_AttributeSeeds			= 'seeds'
	_AttributeLeeches		= 'peers'

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		ProviderJson.initialize(self,
			name					= 'BitLord',
			description				= '{name} is a {container} indexer that scrapes other sites. The site contains results in various languages, but most of them are in English. {name} has missing or inaccurate file sizes.',
			rank					= 4,
			performance				= ProviderJson.PerformanceExcellent,

			link					= Provider._Link,

			accountAuthentication	= {
										ProviderJson.ProcessMode : ProviderJson.AccountModeScrape,
										ProviderJson.ProcessRequest : {
											ProviderJson.RequestMethod : ProviderJson.RequestMethodGet,
										},
										ProviderJson.ProcessExtract : {
											ProviderJson.RequestCookies : ProviderJson.RequestCookiePhp,
											ProviderJson.RequestHeaders : {
												ProviderJson.RequestHeaderRequestToken : ['token\s*:\s*(.*?)(?:$|\s|,)', '%s\s*\+?=\s*[\'"](.*?)[\'";]'],
											},
										},
									},

			customSpam				= True,

			supportMovie			= True,
			supportShow				= True,
			supportPack				= True,

			offsetStart				= 0,
			offsetIncrease			= Provider._LimitOffset,

			formatEncode			= ProviderJson.FormatEncodeNone,

			searchQuery				= {
										ProviderJson.RequestMethod : ProviderJson.RequestMethodPost,
										ProviderJson.RequestPath : Provider._Path,
										ProviderJson.RequestData : {
											Provider._ParameterQuery	: ProviderJson.TermQuery,
											Provider._ParameterCategory	: ProviderJson.TermCategory,
											Provider._ParameterOffset	: ProviderJson.TermOffset,
											Provider._ParameterLimit	: Provider._LimitOffset,
											Provider._ParameterSort		: Provider._ParameterSeeds,
											Provider._ParameterOrder	: Provider._ParameterDescending,
											Provider._ParameterTime		: Provider._ParameterAll,
											Provider._ParameterPorn		: Provider._ParameterFalse,
											Provider._ParameterSpam		: Provider._ParameterFalse if self.customSpam() else Provider._ParameterTrue,
										},
									},
			searchCategoryMovie		= Provider._CategoryMovie,
			searchCategoryShow		= Provider._CategoryShow,

			extractList				= Provider._AttributeList,
			extractLink				= Provider._AttributeLink,
			extractIdLocal			= Provider._AttributId,
			extractFileName			= Provider._AttributeName,
			extractFileSize			= Provider._AttributeSize,
			extractSourceTime		= Provider._AttributeTime,
			extractSourceSeeds		= Provider._AttributeSeeds,
			extractSourceLeeches	= Provider._AttributeLeeches,
		)

	##############################################################################
	# PROCESS
	##############################################################################

	def processFileSize(self, value, item, details = None, entry = None):
		# BitLord scrapes other torrent sites.
		# The file size is opten missing or given in different units (MB vs GB).
		try:
			value = float(value)
			if value > 0:
				if value < 75: value = value * 1073741824
				else: value = value * 1048576
				return int(value)
		except: pass
		return None
