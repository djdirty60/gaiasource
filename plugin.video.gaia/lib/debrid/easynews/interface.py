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

from lib.debrid import base
from lib.debrid.easynews import core
from lib.modules import tools
from lib.modules import interface

class Interface(base.Interface):

	##############################################################################
	# CONSTRUCTOR
	##############################################################################

	def __init__(self):
		base.Interface.__init__(self)
		self.mDebrid = core.Core()

	##############################################################################
	# ACCOUNT
	##############################################################################

	def account(self):
		interface.Loader.show()
		valid = False
		title = core.Core.Name + ' ' + interface.Translation.string(33339)
		if self.mDebrid.accountEnabled():
			account = self.mDebrid.account(cached = False)
			if account:
				valid = interface.Translation.string(33341) if self.mDebrid.accountValid() else interface.Translation.string(33342)
				user = account['user']
				email = account['email']
				type = account['type']
				status = account['status'].capitalize()
				version = str(account['version'])

				date = account['expiration']['date']
				days = str(account['expiration']['remaining'])

				loyaltyDate = account['loyalty']['time']['date']
				loyaltyPoints = '%.3f' % account['loyalty']['points']

				total = account['usage']['total']['size']['description']
				remaining = account['usage']['remaining']['size']['description'] + (' (%.1f%%)' % account['usage']['remaining']['percentage'])
				consumed = account['usage']['consumed']['size']['description'] + (' (%.1f%%)' % account['usage']['consumed']['percentage'])
				consumedWeb = account['usage']['consumed']['web']['size']['description'] + (' (%.1f%%)' % account['usage']['consumed']['web']['percentage'])
				consumedNntp = account['usage']['consumed']['nntp']['size']['description'] + (' (%.1f%%)' % account['usage']['consumed']['nntp']['percentage'])
				consumedNntpUnlimited = account['usage']['consumed']['nntpunlimited']['size']['description'] + (' (%.1f%%)' % account['usage']['consumed']['nntpunlimited']['percentage'])

				items = []

				items = []

				# Information
				items.append({
					'title' : 33344,
					'items' : [
						{ 'title' : 33340, 'value' : valid },
						{ 'title' : 32303, 'value' : user },
						{ 'title' : 32304, 'value' : email },
						{ 'title' : 33343, 'value' : type },
						{ 'title' : 33389, 'value' : status },
						{ 'title' : 33359, 'value' : version },
					]
				})

				# Expiration
				items.append({
					'title' : 33345,
					'items' : [
						{ 'title' : 33346, 'value' : date },
						{ 'title' : 33347, 'value' : days }
					]
				})

				# Loyalty
				items.append({
					'title' : 33750,
					'items' : [
						{ 'title' : 33346, 'value' : loyaltyDate },
						{ 'title' : 33349, 'value' : loyaltyPoints }
					]
				})

				# Usage
				items.append({
					'title' : 33228,
					'items' : [
						{ 'title' : 33497, 'value' : total },
						{ 'title' : 33367, 'value' : remaining },
						{ 'title' : 33754, 'value' : consumed },
						{ 'title' : 33751, 'value' : consumedWeb },
						{ 'title' : 33752, 'value' : consumedNntp },
						{ 'title' : 33753, 'value' : consumedNntpUnlimited },
					]
				})

				# Dialog
				interface.Loader.hide()
				interface.Dialog.information(title = title, items = items)
			else:
				interface.Loader.hide()
				interface.Dialog.confirm(title = title, message = interface.Translation.string(33352) % core.Core.Name)
		else:
			interface.Loader.hide()
			interface.Dialog.confirm(title = title, message = interface.Translation.string(33351) % core.Core.Name)

		return valid

	def accountAuthentication(self, help = True, settings = True):
		return self.mDebrid.accountInstance()._authenticate(functionVerify = self.mDebrid.accountAuthenticationVerify, help = help, settings = settings)
