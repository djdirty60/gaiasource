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

# https://github.com/SickChill/SickChill/blob/master/sickbeard/providers/thepiratebay.py
# NB: if this provider changes, check/update Torrentz Version 1, it uses the same code.

class Provider(ProviderJson):

	_Link				= {
							ProviderJson.Version1 : ['https://apibay.org'],
							ProviderJson.Version2 : ['https://pirateproxy.buzz'],
							ProviderJson.Version3 : ['https://tpb19.ukpass.co'],
							ProviderJson.Version4 : ['https://tpb.sadzawka.tk', 'https://thepiratebay.d4.re', 'https://baypirated.site', 'https://piratenow.xyz', 'https://tpbay.win'],
						}
	_Path				= {
							ProviderJson.Version1 : 'q.php',
							ProviderJson.Version2 : 'newapi/q.php',
							ProviderJson.Version3 : 'apibay/q.php',
							ProviderJson.Version4 : 'api.php?url=/q.php',
						}
	_Query				= {
							ProviderJson.Version1 : '%s?%s=%s&%s=%s',
							ProviderJson.Version2 : '%s?%s=%s&%s=%s',
							ProviderJson.Version3 : '%s?%s=%s&%s=%s',
							ProviderJson.Version4 : '%s?%s=%s%%26%s=%s', # URL-encode "&", since the URL is passed as a parameter, otherwise the category is ignored.
						}

	_LimitOffset		= 100 # The maximum number of results returned by a query.

	# Using multiple categories (eg: cat=201,202,207) does work, but the results are limited to 100 items.
	_CategoryMovie		= ['201', '202', '207', '209'] # 201 = Movies, 202 = Movies DVDR, 207 = HD Movies, 209 = 3D
	_CategoryShow		= ['205', '208'] # 205 = TV Shows, 208 = HD TV Shows

	_ParameterQuery		= 'q'
	_ParameterCategory	= 'cat'

	_AttributeUploader	= 'username'
	_AttributeName		= 'name'
	_AttributeSize		= 'size'
	_AttributeHash		= 'info_hash'
	_AttributeTime		= 'added'
	_AttributeStatus	= 'status'
	_AttributeSeeds		= 'seeders'
	_AttributeLeeches	= 'leechers'
	_AttributeImdb		= 'imdb'
	_AttributeVip		= 'vip'
	_AttributeTrusted	= 'trusted'
	_AttributeMember	= 'member'

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self):
		version = self.customVersion()
		id = self.customSearchId()
		category = self.customCategory()

		ProviderJson.initialize(self,
			name					= 'APIBay',
			description				= '{name} is the backend {container} API used by ThePirateBay. The API contains results in various languages, but most of them are in English. Searches are conducted using the title. The API is fast and reliable, but does not support paging and will therefore not always return all the results that are available. Version %s is the official API, but the other versions work in the same way.' % ProviderJson.Version1,
			rank					= 5,
			performance				= ProviderJson.PerformanceExcellent,

			link					= Provider._Link[version],

			customVersion			= 4,
			customSearch			= {
										ProviderJson.SettingsDefault		: ProviderJson.CustomSearchTitle,
										ProviderJson.SettingsDescription	: 'Search {name} using the title or the IMDb ID. Not all files have an associated ID and searching by title might therefore return more results. Searching by title is slower and can return incorrect results. The title will be used if no ID is available.',
									},
			customCategory			= {
										ProviderJson.SettingsDefault		: True,
										ProviderJson.SettingsDescription	: '{name} returns a maximum of %d results per request. {name} has subcategories that can be searched together with a single request or can be searched separately with multiple requests. Searching categories separately might return more results, but can also increase the scraping time.' % Provider._LimitOffset,
									},
			customVerified			= True,

			supportMovie			= True,
			supportShow				= True,
			supportPack				= True,

			# Important to manually create the GET URL for version 4.
			# Since version 4 already has a ? in the URL, Networker will append the GET parameters with a &.
			#searchQuery				= {
			#							ProviderJson.RequestPath : path,
			#							ProviderJson.RequestData : {
			#								Provider._ParameterQuery	: Provider.TermIdImdb if id else Provider.TermQuery,
			#								Provider._ParameterCategory	: ProviderJson.TermCategory,
			#							},
			#						},
			searchQuery				= [
										Provider._Query[version] % (Provider._Path[version], Provider._ParameterQuery, Provider.TermIdImdb if id else Provider.TermQuery, Provider._ParameterCategory, ProviderJson.TermCategory),
										Provider._Query[version] % (Provider._Path[version], Provider._ParameterQuery, Provider.TermQuery, Provider._ParameterCategory, ProviderJson.TermCategory),
									],

			searchCategoryMovie		= Provider._CategoryMovie if category else ','.join(Provider._CategoryMovie),
			searchCategoryShow		= Provider._CategoryShow if category else ','.join(Provider._CategoryShow),

			extractHash				= Provider._AttributeHash,
			extractReleaseUploader	= Provider._AttributeUploader,
			extractFileName			= Provider._AttributeName,
			extractFileSize			= Provider._AttributeSize,
			extractSourceTime		= Provider._AttributeTime,
			extractSourceApproval	= Provider._AttributeStatus,
			extractSourceSeeds		= Provider._AttributeSeeds,
			extractSourceLeeches	= Provider._AttributeLeeches,
		)

	##############################################################################
	# PROCESS
	##############################################################################

	def processBefore(self, item):
		expectedImdb = self.parameterIdImdb()
		if expectedImdb:
			try: currentImdb = item[Provider._AttributeImdb]
			except: currentImdb = None
			if currentImdb and not currentImdb == expectedImdb: return ProviderJson.Skip

	def processHash(self, value, item, details = None, entry = None):
		# If no results are found, a single link with a 0s hash is returned. Skip it.
		if value == '0000000000000000000000000000000000000000': return ProviderJson.Skip
		else: return value

	def processSourceApproval(self, value, item, details = None, entry = None):
		if self.customVerified():
			if not value == Provider._AttributeVip and not value == Provider._AttributeTrusted: return ProviderJson.Skip
		if value == Provider._AttributeVip: return ProviderJson.ApprovalExcellent
		elif value == Provider._AttributeTrusted: return ProviderJson.ApprovalGood
		elif value == Provider._AttributeMember: return ProviderJson.ApprovalBad
		else: return ProviderJson.ApprovalDefault
