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

from lib.providers.core.base import ProviderBase
from lib.modules.network import Networker

class ProviderPremium(ProviderBase):

	Popularity = 1 # Premium provider's default popularity.

	def __init__(self, **kwargs):
		ProviderBase.__init__(self, **kwargs)

	##############################################################################
	# INITIALIZE
	##############################################################################

	def initialize(self,
		core		= None,
		propagate	= True,
		**kwargs
	):
		self.mCore = core
		self.mDomain = Networker.linkDomain(link = self.mCore.link(), subdomain = False, topdomain = True, ip = True)

		if propagate:
			if not 'name' in kwargs: kwargs['name'] = core.name()
			if not 'accountOther' in kwargs: kwargs['accountOther'] = ProviderBase.AccountInputCustom
			ProviderBase.initialize(self, **kwargs)

	##############################################################################
	# ENABLED
	##############################################################################

	def enabledInternal(self):
		return self.mCore.accountEnabled() and self.mCore.accountValid()

	##############################################################################
	# ACCOUNT
	##############################################################################

	def accountVerify(self):
		return self.mCore.accountVerify()

	def accountCustomEnabled(self):
		try: return self.mCore.accountEnabled()
		except: return False

	def accountSettingsLabel(self):
		try: return self.mCore.accountLabel()
		except: return None

	def accountCustomDialog(self):
		try: return self.mCore.accountAuthentication(settings = False)
		except: return None

	##############################################################################
	# CORE
	##############################################################################

	def core(self, copy = False):
		return self.mCore.clone() if copy else self.mCore

	##############################################################################
	# DOMAIN
	##############################################################################

	def domain(self):
		return self.mDomain

	##############################################################################
	# RESULT
	##############################################################################

	def resultAdd(self, stream):
		try:
			stream.sourcePopularitySet(ProviderPremium.Popularity)
			stream.accessTypeMemberSet(True)
			stream.accessTypeDirectSet(True)
			ProviderBase.resultAdd(self, stream)
		except: self.logError()

	##############################################################################
	# PROCESS
	##############################################################################

	# Can be overwritten by subclasses if the popularity should be lower.
	def processSourcePopularity(self, value, item, details = None, entry = None):
		return ProviderPremium.Popularity
