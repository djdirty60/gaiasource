# -*- coding: utf-8 -*-

'''
	Gaia Add-on
	Copyright (C) 2016 Gaia

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from lib.modules.tools import Media

class MetaTmdb(object):

	LinkMovie		= 'https://themoviedb.org/movie/%s'
	LinkShow		= 'https://themoviedb.org/tv/%s'
	LinkSeason		= 'https://themoviedb.org/tv/%s/season/%d'
	LinkEpisode		= 'https://themoviedb.org/tv/%s/season/%d/episode/%d'

	##############################################################################
	# GENERAL
	##############################################################################

	@classmethod
	def link(self, media = None, id = None, season = None, episode = None, metadata = None):
		if metadata:
			try:
				media = Media.TypeShow if 'tvshowtitle' in metadata or 'season' in metadata else Media.TypeMovie
				id = metadata['id']['tmdb']
				season = metadata['season']
				episode = metadata['episode']
			except: pass

		if id:
			if Media.typeTelevision(media):
				if not episode is None: return MetaTmdb.LinkEpisode % (id, season, episode)
				elif not season is None: return MetaTmdb.LinkSeason % (id, season)
				else: return MetaTmdb.LinkShow % id
			else:
				return MetaTmdb.LinkMovie % id

		return None
