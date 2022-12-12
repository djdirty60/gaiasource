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

from lib.modules.tools import CreScrapers
from lib.providers.core.external import ProviderExternalUnstructured

class Provider(ProviderExternalUnstructured):

	Name = CreScrapers.Name
	Rank = 4
	Settings = True

	IdAddon = CreScrapers.IdAddon
	IdParent = CreScrapers.IdParent
	IdSettings = CreScrapers.IdParent
	IdLibrary = CreScrapers.IdLibrary
	IdGaia = CreScrapers.IdGaia

	Path = ['lib', IdLibrary, 'sources']

	# TheCrew does not have a subfolder with its own name.
	# This causes import clashes if other external providers are also enabled.
	Restructure = [
		['lib', 'resources', 'lib'],
		['lib', IdLibrary],
	]
