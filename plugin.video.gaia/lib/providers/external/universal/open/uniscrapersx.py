# -*- coding: utf-8 -*-

"""
	Gaia Addon

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
"""

from lib.modules.tools import UniScrapers
from lib.providers.core.external import ProviderExternalStructured

class Provider(ProviderExternalStructured):

	Name = UniScrapers.Name
	Rank = 3
	Settings = True

	IdAddon = UniScrapers.IdAddon
	IdLibrary = UniScrapers.IdLibrary
	IdGaia = UniScrapers.IdGaia

	Module = 'universalscrapers' # Module name to import.
