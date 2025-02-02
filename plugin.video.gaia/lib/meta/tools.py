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

from lib.meta.data import MetaData
from lib.meta.image import MetaImage

from lib.modules.tools import Media, Language, Country, Tools, Converter, Regex, Logger, System, Settings, Selection, Kids, Time
from lib.modules.interface import Context, Directory, Icon, Format, Translation, Skin, Font
from lib.modules.convert import ConverterTime
from lib.modules.theme import Theme
from lib.modules.concurrency import Lock
from lib.modules.video import Recap, Review, Extra, Deleted, Making, Director, Interview, Explanation

class MetaTools(object):

	Instance				= None
	Lock					= Lock()

	DetailEssential			= 'essential'
	DetailStandard			= 'standard'
	DetailExtended			= 'extended'
	Details					= [DetailEssential, DetailStandard, DetailExtended]

	ProviderImdb			= 'imdb'
	ProviderTmdb			= 'tmdb'
	ProviderTvdb			= 'tvdb'
	ProviderTvmaze			= 'tvmaze'
	ProviderTrakt			= 'trakt'
	ProviderFanart			= 'fanart'

	StreamVideo				= 'video'
	StreamAudio				= 'audio'
	StreamSubtitle			= 'subtitle'
	StreamDuration			= 'duration'
	StreamCodec				= 'codec'
	StreamAspect			= 'aspect'
	StreamWidth				= 'width'
	StreamHeight			= 'height'
	StreamChannels			= 'channels'
	StreamLanguage			= 'language'

	RatingImdb				= 'imdb'
	RatingTmdb				= 'tmdb'
	RatingTvdb				= 'tvdb'
	RatingTrakt				= 'trakt'
	RatingTvmaze			= 'tvmaze'
	RatingMetacritic		= 'metacritic'
	RatingAverage			= 'average'
	RatingAverageWeighted	= 'averageweighted'
	RatingAverageLimited	= 'averagelimited'
	RatingDefault			= RatingAverageWeighted
	RatingProviders			= [RatingImdb, RatingTmdb, RatingTvdb, RatingTrakt, RatingTvmaze, RatingMetacritic]
	RatingVotes				= 10 # Default vote count if there is a rating by no vote count (eg Metacritic or Tvmaze).

	TimeUnreleased			= 10800 # 3 hours.
	TimeFuture				= 86400 # 1 day.

	###################################################################
	# CONSTRUCTOR
	###################################################################

	def __init__(self):
		self.mSettingsDetail = Settings.getString('metadata.general.detail').lower()
		self.mSettingsLanguage = Language.settingsCustom('metadata.location.language')
		self.mSettingsCountry = Country.settings('metadata.location.country')

		self.mMetaAllowed = ['genre', 'country', 'year', 'episode', 'season', 'sortepisode', 'sortseason', 'episodeguide', 'showlink', 'top250', 'setid', 'tracknumber', 'rating', 'userrating', 'watched', 'playcount', 'overlay', 'cast', 'castandrole', 'director', 'mpaa', 'plot', 'plotoutline', 'title', 'originaltitle', 'sorttitle', 'duration', 'studio', 'tagline', 'writer', 'tvshowtitle', 'premiered', 'status', 'set', 'setoverview', 'tag', 'imdbnumber', 'code', 'aired', 'credits', 'lastplayed', 'album', 'artist', 'votes', 'path', 'trailer', 'dateadded', 'mediatype', 'dbid']
		self.mMetaNonzero = ['genre', 'country', 'year', 'episodeguide', 'showlink', 'top250', 'cast', 'castandrole', 'director', 'mpaa', 'plot', 'plotoutline', 'title', 'originaltitle', 'sorttitle', 'duration', 'studio', 'tagline', 'writer', 'tvshowtitle', 'premiered', 'status', 'set', 'setoverview', 'tag', 'imdbnumber', 'aired', 'credits', 'path', 'trailer', 'dateadded', 'mediatype']
		self.mMetaExclude = ['userrating', 'watched', 'playcount', 'overlay', 'duration', 'title']

		self.mStudioIgnore = [
			'Duplass Brothers Productions',
			'Double Dare You Productions',
			'Square Peg',
			'Secret Engine',
			'Tango Entertainment',
			'Rosetory',
			'Carnival Films',
			'Imagenation Abu Dhabi FZ',
			'Lost City',
			'AGC Studios',
			'Spooky Pictures',
			'Divide / Conquer',
			'Palm Drive Productions',
			'Municipal Pictures',
			'Brooksfilms Ltd.',
			'Mass Animation',
			'Cinesite Animation',
			'HB Wink Animation',
			'Aniventure',
			'Align',
			'GFM Animation',
			'Flying Tigers Entertainment',
			'Blazing Productions',
			'BoulderLight Pictures',
			'SSS Entertainments',
			'mm2 Asia',
			'Post Film',
			'Burn Later Productions',
			'American High',
			'Atlas Industries',
			'Hantz Motion Pictures',
			'Greendale Productions',
			'BlazNick Wechsler Productions',
			'Barry Linen Motion Pictures',
			'Jackson Pictures',
			'Komplizen Film',
			'Fabula',
			'Shoebox Films',
			'Topic Studios',
			'Elevated Films',
			'Involving Pictures',
			'Zero Gravity Management',
			'The Solution',
			'Lightstream Entertainment',
			'Bento Box Entertainment',
			'Buck & Millie Productions',
			'Wilo Productions',
			'Big Indie Pictures',
			'BCDF Pictures',
			'Vertical Entertainment',
			'Mister Smith Entertainment',
			'Federal Films',
			'Convergent Media',
			'South Australian Film Corporation',
			'Stan Australia',
			'Deeper Water',
			'Rogue Star Productions',
			'Smoke House Pictures',
			'Grand Illusion Films',
			'Saban Films',
			'Paper Street Pictures',
			'Film Bridge International',
			'Forma Pro Films',
			'Altit Media Group',
			'Evolution Pictures',
			'Metrol Technology',
			'Kreo Films FZ',
			'Kreo Films',
			'Trigger Films',
			'GFM films',
			'GFM Films',
			'Red Production',
			'The Walk-Up Company',
		]
		self.mStudioReplacePartial = {
			'(20th century)(?!\sfox)' : 'Twentieth Century Fox',
			'(20th century)' : 'Twentieth Century',
		}
		self.mStudioReplaceFull = {
			'^amazon(?:$|\s*prime|\s*video)?' : 'Amazon', # Amazon Prime Video
			'history\s*[\(\[\{]?canada[\)\]\}]?' : 'History (CA)', # History Canada
			'sony\s*liv' : 'Sony Pictures Television International', # SonyLIV
			'^film4\s*productions?$' : 'Film4', # Film4
			'^twentieth\s*century\s*fox\s*studios?$' : 'Twentieth Century Fox Film',
			'^big\s*beach$' : 'Big Beach Films',
			'^searchlight\s*pictures$' : 'Fox Searchlight Pictures', # Searchlight
			'^syndication$' : 'Syndicated', # Syndication (means it was released to multiple TV stations back in the day)
		}

		self.mTimeCurrent = Time.timestamp()
		self.mTimeClock = Time.format(timestamp = self.mTimeCurrent, format = Time.FormatTime, local = True)

		from lib.modules.playback import Playback
		self.mItemPlayback = Playback.instance()
		self.mItemPlayable = not System.originPlugin()
		self.mItemContext = Context.enabled()

		self.mHideAll = False
		self.mHideRelease = False
		hide = Settings.getInteger('navigation.general.hide')
		if hide == 1: self.mHideRelease = True
		elif hide == 2: self.mHideAll = True

		self.mPageMovie = Settings.getInteger('navigation.page.movie')
		self.mPageShow = Settings.getInteger('navigation.page.show')
		self.mPageEpisode = Settings.getInteger('navigation.page.episode')
		self.mPageFlatten = Settings.getInteger('navigation.page.flatten')
		self.mPageMixed = Settings.getInteger('navigation.page.mixed')
		self.mPageSearch = Settings.getInteger('navigation.page.search')

		self.mShowDirect = Settings.getBoolean('navigation.show.direct')
		self.mShowExtra = Settings.getBoolean('navigation.show.extra')
		self.mShowFlatten = Settings.getBoolean('navigation.show.flatten')

		self.mShowSeries = not self.mShowFlatten and Settings.getBoolean('navigation.show.series')

		self.mShowInterleave = Settings.getBoolean('navigation.show.interleave')
		self.mShowInterleaveSupplementary = Settings.getBoolean('navigation.show.interleave.supplementary')
		self.mShowInterleaveUnofficial = Settings.getBoolean('navigation.show.interleave.unofficial')
		self.mShowInterleaveDuration = Settings.getInteger('navigation.show.interleave.duration')
		if self.mShowInterleaveDuration == 1: self.mShowInterleaveDuration = 0.25
		elif self.mShowInterleaveDuration == 2: self.mShowInterleaveDuration = 0.5

		self.mShowSpecial = Settings.getBoolean('navigation.show.special')
		self.mShowSpecialSeason = Settings.getBoolean('navigation.show.special.season') if self.mShowSpecial else False
		self.mShowSpecialEpisode = Settings.getBoolean('navigation.show.special.episode') if self.mShowSpecial else False

		self.mShowFuture = Settings.getBoolean('navigation.show.future')
		self.mShowFutureSeason = Settings.getBoolean('navigation.show.future.season') if self.mShowFuture else False
		self.mShowFutureEpisode = Settings.getBoolean('navigation.show.future.episode') if self.mShowFuture else False

		self.mShowCounterEnabled = Settings.getBoolean('navigation.show.counter')
		self.mShowCounterSpecial = Settings.getBoolean('navigation.show.counter.special')
		self.mShowCounterUnwatched = Settings.getBoolean('navigation.show.counter.unwatched')
		self.mShowCounterLimit = Settings.getBoolean('navigation.show.counter.limit')

		self.mLabelForce = Settings.getInteger('metadata.label.force')
		if self.mLabelForce == 2: self.mLabelForce = not Skin.supportLabelCustom(default = True)
		else: self.mLabelForce = bool(self.mLabelForce)

		self.mLabelDetailEnabled = Settings.getBoolean('metadata.detail.enabled')
		self.mLabelDetailLevel = Settings.getInteger('metadata.detail.level')
		self.mLabelDetailPlacement = Settings.getInteger('metadata.detail.placement')
		self.mLabelDetailDecoration = Settings.getInteger('metadata.detail.decoration')
		self.mLabelDetailStyle = Settings.getInteger('metadata.detail.style')
		self.mLabelDetailColor = Settings.getInteger('metadata.detail.color')

		self.mLabelPlayEnabled = Settings.getBoolean('metadata.detail.play')
		self.mLabelPlayThreshold = Settings.getInteger('metadata.detail.play.threshold')

		self.mLabelProgressEnabled = Settings.getBoolean('metadata.detail.progress')
		self.mLabelRatingEnabled = Settings.getBoolean('metadata.detail.rating')

		self.mLabelAirEnabled = Settings.getBoolean('metadata.detail.air')
		self.mLabelAirZone = Settings.getInteger('metadata.detail.air.zone') if self.mLabelAirEnabled else None
		self.mLabelAirFormat = Settings.getInteger('metadata.detail.air.format') if self.mLabelAirEnabled else None
		self.mLabelAirFormatDay = Settings.getInteger('metadata.detail.air.format.day') if self.mLabelAirEnabled else None
		self.mLabelAirFormatTime = Settings.getInteger('metadata.detail.air.format.time') if self.mLabelAirEnabled else None

		self.mDirectory = Directory()

		self.mThemeFanart = Theme.fanart()
		self.mThemeBanner = Theme.banner()
		self.mThemePoster = Theme.poster()
		self.mThemeThumb = Theme.thumbnail()
		self.mThemeNextBanner = Theme.nextBanner()
		self.mThemeNextPoster = Theme.nextPoster()

		ratingsUser = [False, None, True]
		ratingsMovie = [MetaTools.RatingImdb, MetaTools.RatingTmdb, MetaTools.RatingTrakt, MetaTools.RatingMetacritic, MetaTools.RatingAverage, MetaTools.RatingAverageWeighted, MetaTools.RatingAverageLimited]
		ratingsShow = [MetaTools.RatingImdb, MetaTools.RatingTmdb, MetaTools.RatingTrakt, MetaTools.RatingTvmaze, MetaTools.RatingAverage, MetaTools.RatingAverageWeighted, MetaTools.RatingAverageLimited]

		self.mRatingMovieMain = MetaTools.RatingDefault
		try: self.mRatingMovieMain = ratingsMovie[Settings.getInteger('metadata.rating.movie')]
		except: self.mRatingMovieMain = MetaTools.RatingDefault
		try: self.mRatingMovieFallback = ratingsMovie[Settings.getInteger('metadata.rating.movie.fallback')]
		except: self.mRatingMovieFallback = MetaTools.RatingDefault
		try: self.mRatingMovieUser = ratingsUser[Settings.getInteger('metadata.rating.movie.user')]
		except: self.mRatingMovieUser = None

		self.mRatingShowMain = MetaTools.RatingDefault
		try: self.mRatingShowMain = ratingsShow[Settings.getInteger('metadata.rating.show')]
		except: self.mRatingShowMain = MetaTools.RatingDefault
		try: self.mRatingShowFallback = ratingsShow[Settings.getInteger('metadata.rating.show.fallback')]
		except: self.mRatingShowFallback = MetaTools.RatingDefault
		try: self.mRatingShowUser = ratingsUser[Settings.getInteger('metadata.rating.show.user')]
		except: self.mRatingShowUser = None

	# Use a singleton, since it is more efficient to initialize the settings and other variables only once.
	# Especially if the functions are called multiple times in a loop.
	@classmethod
	def instance(self):
		if MetaTools.Instance is None:
			MetaTools.Lock.acquire()
			if MetaTools.Instance is None: MetaTools.Instance = MetaTools()
			MetaTools.Lock.release()
		return MetaTools.Instance

	##############################################################################
	# RESET
	##############################################################################

	@classmethod
	def reset(self, settings = True, full = True):
		if settings:
			MetaTools.Instance = None

		if full:
			from lib.meta.cache import MetaCache
			from lib.meta.image import MetaImage
			from lib.meta.provider import MetaProvider
			from lib.meta.processors.fanart import MetaFanart
			from lib.meta.providers.tvdb import MetaTvdb

			MetaCache.reset(settings = settings)
			MetaImage.reset(settings = settings)
			MetaProvider.reset(settings = settings)
			MetaFanart.reset(settings = settings)
			MetaTvdb.reset(settings = settings)

	###################################################################
	# SETTINGS
	###################################################################

	def settingsLanguage(self):
		return self.mSettingsLanguage

	def settingsCountry(self):
		return self.mSettingsCountry

	def settingsPageMovie(self):
		return self.mPageMovie

	def settingsPageShow(self):
		return self.mPageShow

	def settingsPageEpisode(self):
		return self.mPageEpisode

	def settingsPageFlatten(self):
		return self.mPageFlatten

	def settingsPageMixed(self):
		return self.mPageMixed

	def settingsPageSearch(self):
		return self.mPageSearch

	def settingsShowFlatten(self):
		return self.mShowFlatten

	def settingsShowSeries(self):
		return self.mShowSeries

	def settingsShowInterleave(self):
		return self.mShowInterleave

	def settingsShowInterleaveSupplementary(self):
		return self.mShowInterleaveSupplementary

	def settingsShowInterleaveUnofficial(self):
		return self.mShowInterleaveUnofficial

	def settingsShowInterleaveDuration(self):
		return self.mShowInterleaveDuration

	def settingsShowSpecial(self):
		return self.mShowSpecial

	def settingsShowSpecialSeason(self):
		return self.mShowSpecialSeason

	def settingsShowSpecialEpisode(self):
		return self.mShowSpecialEpisode

	def settingsDetail(self):
		return self.mSettingsDetail

	@classmethod
	def settingsDetailSet(self, detail):
		Settings.set('metadata.general.detail', detail.capitalize())

	@classmethod
	def settingsDetailShow(self, settings = False):
		from lib.modules.window import WindowMetadata
		WindowMetadata.show(wait = True)
		if settings: Settings.launch(id = 'metadata.general.detail')

	###################################################################
	# NETWORK
	##################################################################

	# Create a "Accept-Language" HTTP header, to return metadata in a specifc language.
	# Eg: IMDb uses the public IP address (eg: VPN) if this header is not set, and might return some titles in another unwanted language.
	def headerLanguage(self, weighted = True, wildcard = True, structured = True):
		from lib.modules.network import Networker

		language = []
		language.append(self.settingsLanguage())
		language.extend(Language.settingsCode())
		language = Tools.listUnique([i for i in language if i])

		return Networker.headersAcceptLanguage(language = language, country = self.settingsCountry(), weighted = weighted, wildcard = wildcard, structured = structured)

	###################################################################
	# MEDIA
	###################################################################

	@classmethod
	def media(self, metadata):
		if Tools.isArray(metadata): metadata = metadata[0]
		if 'episode' in metadata: return Media.TypeEpisode
		elif 'season' in metadata: return Media.TypeSeason
		elif 'tvshowtitle' in metadata: return Media.TypeShow
		else: return Media.TypeMovie

	###################################################################
	# COMMAND
	###################################################################

	def command(self, metadata, media = None, action = None, video = None, mixed = None, submenu = None, increment = False):
		force = False
		if media == Media.TypeSeason and not 'season' in metadata: # Series menu.
			media = Media.TypeShow
			submenu = True
			force = True

		if submenu is None: submenu = self.submenu(media = media, mixed = mixed, force = force)

		if not action:
			if not video is None: action = 'streamsVideo'
			elif submenu: action = 'episodesRetrieve'
			elif media == Media.TypeSpecialExtra: action = 'seasonsExtras'
			elif media == Media.TypeShow: action = 'seasonsRetrieve'
			elif media == Media.TypeSeason: action = 'episodesRetrieve'
			if not action: action = 'scrape'

		parameters = {}
		if action == 'scrape' or action == 'seasonsExtras': parameters['metadata'] = metadata
		if mixed and submenu: parameters['limit'] = self.mPageMixed

		for attribute in ['imdb', 'tmdb', 'tvdb', 'title', 'tvshowtitle', 'year', 'premiered', 'season', 'episode']:
			try: parameters[attribute] = metadata[attribute]
			except: pass

		# Season offset for "Next Page" of flattened show menus.
		# NB: Make the season/episode number floats, since Python allows -0.0, but a negative zero is not possible for integers.
		# -0.0 is used to indicate the offset for the Specials season.
		if submenu or force:
			if self.submenuFlatten(media = media, force = force) and self.mPageFlatten == 0: # Flattened show menus.
				parameters['season'] = -1 * float((metadata['season'] if 'season' in metadata else 0) + int(increment))
				try: del parameters['episode']
				except: pass
			else: # Submenus for mixed episode menus.
				parameters['season'] = -1 * float(metadata['season'] if 'season' in metadata else 1)
				parameters['episode'] = -1 * float(metadata['episode'] + int(increment))

		# Season recaps and extras.
		if 'query' in metadata: parameters['title'] = parameters['tvshowtitle'] = metadata['query']
		if not video is None: parameters['video'] = video
		parameters['media'] = Media.TypeEpisode if media == Media.TypeSpecialRecap or media == Media.TypeSpecialExtra else media

		return System.command(action = action, parameters = parameters)

	###################################################################
	# MIXED
	###################################################################

	def mixed(self, metadata):
		if not Tools.isArray(metadata): metadata = [metadata]
		titles = [meta['tvshowtitle'] for meta in metadata if 'tvshowtitle' in meta and meta['tvshowtitle']]
		titles = Tools.listUnique(titles)

		# Sometimes different episodes of the same season have different show titles.
		# Eg: 'Hollywood Medium with Tyler Henry' vs 'Hollywood Medium'
		result = []
		for title in titles:
			found = False
			for i in result:
				if title in i or i in title:
					found = True
					break
			if not found: result.append(title)

		return len(result) > 1

	###################################################################
	# SUBMENU
	###################################################################

	def submenu(self, media, mixed, force = False):
		return self.submenuFlatten(media = media, force = force) or self.submenuDirect(media = media, mixed = mixed)

	def submenuFlatten(self, media, force = False):
		return media == Media.TypeShow and (force or self.mShowFlatten)

	def submenuDirect(self, media, mixed):
		return media == Media.TypeEpisode and mixed and not self.mShowDirect

	###################################################################
	# LABEl
	###################################################################

	def label(self, metadata, media = None, future = None, mixed = False, extend = True):
		if not media: media = self.media(metadata = metadata)

		if media == Media.TypeSeason:
			try: title = metadata['title']
			except: title = None
			try: year = metadata['year']
			except: year = None
			try: season = metadata['season']
			except: season = None
			series = season is None and not 'season' in metadata
			label = Media.title(type = media, title = title, year = year, season = season, series = series, special = True)
		elif media == Media.TypeEpisode:
			try: title = metadata['title']
			except: title = None
			try: year = metadata['year']
			except: year = None
			try: season = metadata['season']
			except: season = None
			try: episode = metadata['episode']
			except: episode = None
			label = Media.title(type = media, title = title, year = year, season = season, episode = episode)
		else:
			try: year = metadata['year']
			except: year = None
			try: title = metadata['title']
			except:
				try: title = metadata['originaltitle']
				except:
					try: title = metadata['tvshowtitle']
					except: title = None

			label = Media.title(type = media, title = title, year = year)
			if not label: label = title

		if mixed and (media == Media.TypeSeason or media == Media.TypeEpisode):
			try: title = metadata['tvshowtitle']
			except: title = None

			# Always add the title.
			# Eg: The first episode's title of the show "1883" is also "1883".
			#if title and not title in label and not label in title: label = '%s - %s' % (title, label)
			if title: label = '%s - %s' % (title, label)

		if extend:
			# Show airing details.
			if 'labelBefore' in metadata and metadata['labelBefore']: label = metadata['labelBefore'] + ' ' + label
			if 'labelAfter' in metadata and metadata['labelAfter']: label = label + ' ' + metadata['labelAfter']

		if not future is None and not future is True:
			if future > -MetaTools.TimeUnreleased: label = Format.fontItalic(label)
			if future >= MetaTools.TimeFuture: label = Format.fontLight(label)

		if media == Media.TypeEpisode and season == 0:
			if not 'story' in metadata or not metadata['story']: label = Format.fontItalic(label)

		return label

	###################################################################
	# STREAM
	###################################################################

	@classmethod
	def stream(self, duration = None, videoCodec = None, videoAspect = None, videoWidth = None, videoHeight = None, audioCodec = None, audioChannels = None, audioLanguage = None, subtitleLanguage = None):
		# https://alwinesch.github.io/group__python__xbmcgui__listitem.html#ga99c7bf16729b18b6378ea7069ee5b138

		video = {}
		if duration: video[MetaTools.StreamDuration] = duration
		if videoCodec: video[MetaTools.StreamCodec] = videoCodec
		if videoAspect: video[MetaTools.StreamAspect] = videoAspect
		if videoWidth: video[MetaTools.StreamWidth] = videoWidth
		if videoHeight: video[MetaTools.StreamHeight] = videoHeight

		audio = {}
		if audioCodec: audio[MetaTools.StreamCodec] = audioCodec
		if audioChannels: audio[MetaTools.StreamChannels] = audioChannels
		if audioLanguage: audio[MetaTools.StreamLanguage] = audioLanguage

		subtitle = {}
		if subtitleLanguage: audio[MetaTools.StreamLanguage] = subtitleLanguage

		return {MetaTools.StreamVideo : video, MetaTools.StreamAudio : audio, MetaTools.StreamSubtitle : subtitle}

	###################################################################
	# ITEM
	###################################################################

	def items(self,
		metadatas,

		media = None,
		kids = None,

		item = None,
		stream = None,
		properties = None,
		playable = None,
		mixed = None,
		submenu = None,
		next = None,
		recap = None,
		extra = None,

		context = None,
		contextAdd = None,
		contextMode = None,
		contextLibrary = None,
		contextPlaylist = None,
		contextShortcutCreate = None,
		contextShortcutDelete = None,

		hide = False,
		hideSearch = False,
		hideRelease = False,
		hideWatched = False,

		label = True,
		command = True,
		clean = True,
		images = True,
	):
		if media is None: media = self.media(metadata = metadatas)
		if mixed is None: mixed = self.mixed(metadata = metadatas) if (media == Media.TypeSeason or media == Media.TypeEpisode) else False
		if submenu is None: submenu = self.submenu(media = media, mixed = mixed)
		folder = submenu or (media == Media.TypeShow or media == Media.TypeSeason)

		seasons = []
		items = []
		itemRecap = None
		itemExtra = None

		for metadata in metadatas:
			try:
				item = self.item(
					metadata = metadata,

					media = media,
					kids = kids,

					stream = stream,
					properties = properties,
					playable = playable,
					mixed = mixed,
					submenu = submenu,

					context = context,
					contextAdd = contextAdd,
					contextMode = contextMode,
					contextLibrary = contextLibrary,
					contextPlaylist = contextPlaylist,
					contextShortcutCreate = contextShortcutCreate,
					contextShortcutDelete = contextShortcutDelete,

					hide = hide,
					hideSearch = hideSearch,
					hideRelease = hideRelease,
					hideWatched = hideWatched,

					label = label,
					command = command,
					clean = clean,
					images = images
				)
				if item:
					if 'season' in metadata: seasons.append(metadata['season'])
					items.append([item['command'], item['item'], folder])

					# Add here instead of after the loop, since recaps/extras have to be inserted between episodes for flattened menus.
					# Insert AFTER the episode item() above was created, since we want to use the cleaned metadata with the watched status.
					if recap or extra:
						cleaned = Tools.update(Tools.copy(metadata), item['metadata'])
						if recap:
							item = self.itemRecap(metadata = cleaned, media = media, kids = kids, mixed = mixed)
							if item: itemRecap = (len(items) - 1, item)
						if extra:
							item = self.itemExtra(metadata = cleaned, media = media, kids = kids, mixed = mixed)
							if item: itemExtra = (len(items) + 1, item)
			except: Logger.error()

		# If special episodes are interleaved, make sure the recap/extra is placed before/after all interleaved specials.
		offset = 0
		if itemRecap:
			index = itemRecap[0]
			for i in range(index, -1, -1):
				if seasons[i] == 0: index -= 1
			items.insert(index, itemRecap[1])
			offset = 1
		if itemExtra:
			index = itemExtra[0]
			for i in range(index, len(seasons)):
				if seasons[i] == 0: index += 1
			items.insert(index + offset, itemExtra[1])

		if next:
			itemNext = self.itemNext(metadata = metadatas, media = media, kids = kids)
			if itemNext: items.append(itemNext)

		return items

	def itemsExtra(self,
		metadata,
		kids = None,
		item = None,
		label = True,
		command = True,
		clean = True,
		images = True
	):
		label = Translation.string(32055)
		media = Media.TypeEpisode
		query = metadata['tvshowtitle']

		for i in ['episode', 'premiered', 'genre', 'rating', 'userrating', 'votes', 'duration']:
			try: del metadata[i]
			except: pass

		items = []
		videos = [Review, Extra, Deleted, Making, Director, Interview, Explanation]
		for video in videos:
			try:
				if video.enabled():
					metadata['query'] = query
					metadata['duration'] = video.Duration
					metadata['title'] = metadata['originaltitle'] = metadata['tagline'] = label + ' ' + Translation.string(video.Label)
					metadata['plot'] = Translation.string(video.Description) % (str(metadata['season']), query)

					item = self.item(
						metadata = metadata,

						media = Media.TypeSpecialExtra,
						kids = kids,

						contextMode = Context.ModeVideo,

						video = video.Id,
						label = metadata['title'],
						command = command,
						clean = clean,
						images = images
					)
					if item: items.append([item['command'], item['item'], False])
			except: Logger.error()

		return items

	'''
		clean:
			True: Clean the metadata before adding it to the item.
			False: Do not clean the metadata before adding it to the item. This assumes that the "metadata" parameter wass already cleaned.
			Dictionary: An already cleaned metadata dictionary. Can be used to avoid cleaning and already cleaned dictionary.
		stream:
			dictionary created by stream().
		properties:
			dictionary with custom properties.
		mixed:
			Whether or not the seasons/episodes are from different shows.
		extend:
			Add extra info to the label or plot.
			Should mostly be used with items in a menu, but not items in the player.
		images:
			True: Extract images from the metadata and add them to the item.
			False: Do not extract images from the metadata and do not add them to the item.
			Dictionary: Use already extracted images and add them to the item.
		context:
			True: Add a context menu to the item.
			False: Do not add a context menu to the item.
			None: Use the settings to determine wether or not to add a context menu to the item.
	'''
	def item(self,
		metadata,

		media = None,
		kids = None,

		item = None,
		stream = None,
		properties = None,
		playable = None,
		video = None,
		mixed = False,
		submenu = False,

		context = None, # If False, do not create a context menu.
		contextAdd = None, # Add the context to the list item. Otherwise the context menu iss just returned.
		contextMode = None, # The type of context menu to create.
		contextCommand = None, # The link/command for the context menu.
		contextLibrary = None, # The link/command to add to the library. If True, uses contextCommand.
		contextPlaylist = None, # Wether or not to allow the item to be queued to the playlist.
		contextSource = None, # The stream source dictionary for stream list items.
		contextOrion = None, # Orion identifiers for stream list items.
		contextShortcutId = None, # The ID to use for the shortcut.
		contextShortcutLabel = None, # The default label to use for the shortcut.
		contextShortcutLocation = None, # The root location for the shortcuts.
		contextShortcutCreate = None, # Wether or not to allow a shortcut to be created for the item.
		contextShortcutDelete = None, # Wether or not to allow a shortcut to be deleted for the item.

		hide = False,
		hideSearch = False,
		hideRelease = False,
		hideWatched = False,

		extend = True,
		extendLabel = True,
		extendPlot = True,

		label = True,
		command = True,
		clean = True,
		images = True,
		content = True
	):
		mediaOriginal = media
		if not media: media = mediaOriginal = self.media(metadata = metadata)

		# Hide special seasons and episodes.
		if (media == Media.TypeSeason or media == Media.TypeEpisode) and not self.mShowSpecialSeason and metadata['season'] == 0: return None
		elif media == Media.TypeEpisode and not self.mShowSpecialEpisode and metadata['episode'] == 0: return None

		if not extend:
			extendLabel = extend
			extendPlot = extend

		future = None
		if content:
			# Hide future seasons and episodes.
			future = self.itemFuture(metadata = metadata, media = media) if (media == Media.TypeSeason or media == Media.TypeEpisode) else None
			if future is True:
				future = None
			else:
				if (media == Media.TypeSeason and not self.mShowFutureSeason) or (media == Media.TypeEpisode and not self.mShowFutureEpisode):
					if future is None: return None # No release date.
					if future > -MetaTools.TimeUnreleased: return None # Released in the past 3 hours or sometime in the future.

			self.cleanEmpty(metadata = metadata) # This is also done later in clean(), but remove here already before calling itemPlayback().

		if not item: item = self.itemCreate()

		if content:
			# Add missing attributes.
			# Will be removed by clean(), but added to commands and context.
			self.itemShow(media = media, item = item, metadata = metadata)

			# Must be before clean() and setInfo().
			self.itemPlayback(media = media, item = item, metadata = metadata)

			# Must be before setInfo() and itemPlot().
			# Must be after itemPlayback().
			self.itemDetail(media = media, item = item, metadata = metadata)

			# Must be before setInfo().
			self.itemDate(media = media, item = item, metadata = metadata)

			# Must be before setInfo().
			self.itemPlot(media = media, item = item, metadata = metadata, extend = extendPlot)

			if hide:
				if not hideSearch: # Always show watched items in the search menu.
					try: watched = metadata['playcount'] > 0
					except: watched = False
					if watched:
						if (hideRelease and self.mHideRelease) or (not hideRelease and self.mHideAll): return None
						if hideWatched and (not 'progress' in metadata or not metadata['progress']): return None # Skip episodes marked as watched for the unfinished list.

		# Must be done before the title/label is changed below.
		if command is True: command = self.command(media = media, metadata = metadata, video = video, mixed = mixed, submenu = submenu)
		elif not command: command = None
		elif command: item.setPath(command)

		if clean is True: cleaned = self.clean(media = media, metadata = metadata)
		elif Tools.isDictionary(clean): cleaned = clean
		else: cleaned = metadata

		# Adding Label or Label2 to the ListItem does not work.
		# Instead of the label, the title set in setInfo() is used.
		# This is most likley a skin bug (including the default Kodi skin), since skins seem to not check if there is a label, but only always just pick the title.
		# The only way to use a custom title seems to be to replace the title attribute.
		# Note that this will propagate to all places where the ListItem is used. Eg: The Kodi info dialog will show the custom label instead of the title and might eg have 2 years in the label.
		if label:
			if label is True: label = self.label(metadata = metadata, media = mediaOriginal, future = future, mixed = mixed, extend = extendLabel)

			# Use original, since we can pass docu/short in.
			# Always force for seasons, since a few seasons have their own title and we do not want to have naming inconsistencies.
			# Eg: Breaking Bad's special season has an English title "Minisodes".
			# Update: not needed anymore, since the setting "metadata.title.layout" is now enabled by default.
			if self.mLabelForce: cleaned['title'] = label

			item.setLabel(label)

		# NB: call setInfo() first, before any of the other functions below.
		# Otherwise Kodi might replace values set by the other functions with the values from setInfo().
		# For instance, setInfo() will replace the values set by setCast(), and then actor thumbnails do not show in the Kodi info dialog.
		item.setInfo(type = 'video', infoLabels = cleaned)

		self.itemId(item = item, metadata = metadata)
		self.itemVoting(item = item, metadata = metadata)
		self.itemCast(item = item, metadata = metadata)
		self.itemStream(item = item, stream = stream)
		self.itemProperty(item = item, properties = properties, playable = playable)

		images = self.itemImage(item = item, media = media, metadata = metadata, images = images, video = video)

		if context is False:
			context = None
		else:
			if contextMode is None and not content: contextMode = Context.ModeStream
			context = self.itemContext(item = item, context = context, add = contextAdd, mode = contextMode, media = mediaOriginal, kids = kids, video = video, command = contextCommand if contextCommand else command, library = contextLibrary, playlist = contextPlaylist, source = contextSource, metadata = metadata, orion = contextOrion, shortcutId = contextShortcutId, shortcutLabel = contextShortcutLabel, shortcutLocation = contextShortcutLocation, shortcutCreate = contextShortcutCreate, shortcutDelete = contextShortcutDelete)

		return {'item' : item, 'command' : command, 'context' : context, 'metadata' : cleaned, 'images' : images}

	# ListItem passed to Kodi's player.
	def itemPlayer(self,
		metadata,

		media = None,
		kids = None,

		item = None,
		stream = None,
		properties = None,

		label = False,
		command = True,
		clean = True,
		images = True
	):
		return self.item(
			metadata = metadata,

			media = media,
			kids = kids,

			item = item,
			stream = stream,
			properties = properties,
			playable = True,
			mixed = False,

			context = False,

			hide = False,
			extend = False,

			label = label,
			command = command,
			clean = clean,
			images = images
		)

	def itemCreate(self):
		return self.mDirectory.item()

	def itemShow(self, media, metadata, item):
		if media == Media.TypeShow or media == Media.TypeSeason:
			if not 'tvshowtitle' in metadata and 'title' in metadata: metadata['tvshowtitle'] = metadata['title']
			if not 'tvshowyear' in metadata and 'year' in metadata: metadata['tvshowyear'] = metadata['year']

		# For Gaia Eminence.
		if media == Media.TypeEpisode:
			item.setProperty('GaiaShowNumber', Media.number(metadata = metadata))
			item.setProperty('GaiaShowStory', str(int(metadata['season'] > 0 or ('story' in metadata and metadata['story']))))
			if 'special' in metadata and metadata['special']: item.setProperty('GaiaShowSpecial', '-'.join(metadata['special']))
		elif media == Media.TypeSpecialExtra or media == Media.TypeSpecialRecap:
			item.setProperty('GaiaShowExtra', '1')

	def itemDetail(self, media, metadata, item):
		if self.mLabelDetailEnabled:
			details = False
			if self.mLabelDetailLevel == 0: details = Media.typeMovie(media) or media == Media.TypeEpisode
			elif self.mLabelDetailLevel == 1: details = Media.typeMovie(media) or media == Media.TypeSeason or media == Media.TypeEpisode
			elif self.mLabelDetailLevel == 2: details = Media.typeMovie(media) or media == Media.TypeShow or media == Media.TypeSeason or media == Media.TypeEpisode

			if details:
				values = []

				color = None
				if self.mLabelDetailColor == 1: color = Format.colorPrimary()
				elif self.mLabelDetailColor == 2: color = Format.colorSecondary()
				elif self.mLabelDetailColor == 3: color = True

				if self.mLabelPlayEnabled:
					try: playcount = metadata['playcount']
					except: playcount = None
					if not playcount: playcount = 0
					if playcount >= self.mLabelPlayThreshold:
						values.append((32006, Font.IconWatched, Format.colorExcellent() if color is True else color, str(playcount)))

				if self.mLabelProgressEnabled and 'progress' in metadata and not metadata['progress'] is None:
					values.append((32037, Font.IconProgress, Format.colorPoor() if color is True else color, '%.0f%%' % (metadata['progress'] * 100.0)))

				if self.mLabelRatingEnabled and 'userrating' in metadata and not metadata['userrating'] is None:
					values.append((35187, Font.IconRating, Format.colorMedium() if color is True else color, '%.1f' % metadata['userrating']))

				if Media.typeTelevision(media) and self.mLabelAirEnabled and 'airs' in metadata:
					try: airTime = metadata['airs']['time']
					except: airTime = None
					try: airDay = metadata['airs']['day'][0]
					except: airDay = None
					try: airZone = metadata['airs']['zone']
					except: airZone = None

					if airTime and airDay:
						if airZone:
							if self.mLabelAirZone == 1: zoneTo = airZone
							elif self.mLabelAirZone == 2: zoneTo = Time.ZoneUtc
							else: zoneTo = Time.ZoneLocal

							if self.mLabelAirFormatTime == 0: formatOutput = '%I:%M %p'
							elif self.mLabelAirFormatTime == 1: formatOutput = '%H:%M'

							abbreviate = self.mLabelAirFormatDay == 1
							airTime = Time.convert(stringTime = airTime, stringDay = airDay, zoneFrom = airZone, zoneTo = zoneTo, abbreviate = abbreviate, formatOutput = formatOutput)
							if airDay:
								airDay = airTime[1]
								airTime = airTime[0]

						air = []
						if airDay: air.append(airDay)
						if airTime: air.append(airTime)
						if air:
							if self.mLabelAirFormat == 0: air = airTime
							elif self.mLabelAirFormat == 1: air = airDay
							elif self.mLabelAirFormat == 2: air = air = ' '.join(air)
							values.append((35032, Font.IconCalendar, Format.colorSpecial() if color is True else color, air))

				if values:
					if self.mLabelDetailDecoration == 0: values = [Format.fontColor(i[3], color = i[2]) for i in values]
					elif self.mLabelDetailDecoration == 1: values = [Format.fontColor('%s: %s' % (Translation.string(i[0]), i[3]), color = i[2]) for i in values]
					elif self.mLabelDetailDecoration == 2: values = [Format.fontColor('%s: %s' % (Translation.string(i[0])[0], i[3]), color = i[2]) for i in values]
					elif self.mLabelDetailDecoration == 3: values = ['%s %s' % (Format.fontColor(Font.icon(i[1]), color = i[2]), i[3]) for i in values]

					values = Format.iconJoin(values)
					if self.mLabelDetailPlacement == 0 or self.mLabelDetailPlacement == 1:
						color = Format.colorDisabled()
						values = Format.fontColor('[', color = color) + values + Format.fontColor(']', color = color)

					if self.mLabelDetailStyle == 1: values = Format.fontBold(values)
					elif self.mLabelDetailStyle == 2: values = Format.fontItalic(values)
					elif self.mLabelDetailStyle == 3: values = Format.fontLight(values)

					if self.mLabelDetailPlacement == 0: attribute = 'labelBefore'
					elif self.mLabelDetailPlacement == 1: attribute = 'labelAfter'
					elif self.mLabelDetailPlacement == 2: attribute = 'plotBefore'
					elif self.mLabelDetailPlacement == 3: attribute = 'plotAfter'
					metadata[attribute] = values

	def itemDate(self, media, metadata, item):
		# For Gaia Eminence.
		# These are needed to use sorting in the menus.
		# date/SORT_METHOD_DATE seems to be broken and does not return the correct order.
		# dateadded/SORT_METHOD_DATEADDED can correctly sort by date.
		if 'premiered' in metadata and metadata['premiered']: date = metadata['premiered']
		elif 'aired' in metadata and metadata['aired']: date = metadata['aired']
		else: date = None

		if date:
			# Needs to be set in a specific format.
			dated = ConverterTime(date, format = '%Y-%m-%d')
			metadata['date'] = dated.string(format = '%d.%m.%Y')
			metadata['dateadded'] = dated.string(format = '%Y-%m-%d %H:%M:%S')

			if media == Media.TypeSeason or media == Media.TypeEpisode:
				year = Regex.extract(data = date, expression = '(\d{4})')
				if year: metadata['year'] = int(year)

	def itemPlot(self, media, metadata, item, extend = True):
		if extend:
			if 'plotBefore' in metadata and metadata['plotBefore']:
				if not 'plot' in metadata or not metadata['plot']: metadata['plot'] = metadata['plotBefore']
				else: metadata['plot'] = metadata['plotBefore'] + '\n\n' + metadata['plot']
			if 'plotAfter' in metadata and metadata['plotAfter']:
				if not 'plot' in metadata or not metadata['plot']: metadata['plot'] = metadata['plotAfter']
				else: metadata['plot'] = metadata['plot'] + '\n\n' + metadata['plotAfter']

	def itemId(self, metadata, item):
		try:
			ids = {}
			imdb = None
			for id in ['imdb', 'tmdb', 'tvdb']:
				if id in metadata and metadata[id]:
					ids[id] = metadata[id]
					if id == 'imdb': imdb = metadata[id]
			item.setUniqueIDs(ids, 'imdb')
			if imdb: metadata['imdbnumber'] = imdb
		except: Logger.error()

	def itemFuture(self, metadata, media = None):
		if 'status' in metadata and MetaData.statusExtract(metadata['status']) == MetaData.StatusEnded: return True

		time = None
		if not time and 'aired' in metadata: time = metadata['aired']
		if not time and 'premiered' in metadata: time = metadata['premiered']

		if not time:
			# Trakt sometimes returns new/unaired seasons that or not yet on TVDb, and also sometimes vice versa.
			# These seasons seem to not have a premiered/aired date, year, or even the number of episodes aired.
			# Make them italic to inidcate that they are unaired.
			# Update: Sometimes the year and airs attributes are available.
			if media == Media.TypeSeason:
				if not 'year' in metadata:
					try: episodes = metadata['airs']['episodes']
					except: episodes = None
					if not episodes: return MetaTools.TimeFuture
			if media == Media.TypeSeason or media == Media.TypeEpisode:
				if (not 'rating' in metadata or not metadata['rating']) and (not 'votes' in metadata or not metadata['votes']):
					# If no rating, votes or images.
					images = False
					if MetaImage.Attribute in metadata and metadata[MetaImage.Attribute]:
						for k, v in metadata[MetaImage.Attribute].items():
							if not Tools.isDictionary(v) and v:
								images = True
								break
					if not images: return MetaTools.TimeFuture

			return None

		time = Time.timestamp(fixedTime = time + ' ' + self.mTimeClock, format = Time.FormatDateTime)
		if not time: return None

		return time - self.mTimeCurrent

	def itemVoting(self, metadata, item):
		try:
			if 'voting' in metadata:
				for i in [MetaTools.RatingImdb, MetaTools.RatingTmdb, MetaTools.RatingTvdb]:
					if i in metadata['voting']['rating']:
						rating = metadata['voting']['rating'][i]
						if not rating is None and i in metadata['voting']['votes']:
							votes = metadata['voting']['votes'][i]
							if votes is None: votes = 0
							item.setRating(i, rating, votes, False)
		except: Logger.error()

	def itemImage(self, media, metadata, item, images = True, video = None):
		if Tools.isDictionary(images):
			return MetaImage.set(item = item, images = images)
		elif images:
			if media == Media.TypeSeason and not 'season' in metadata: media = Media.TypeShow # Series menu.

			if video is None: return MetaImage.setMedia(media = media, data = metadata, item = item)
			elif video == Recap.Id: return MetaImage.setRecap(data = metadata, item = item)
			else: return MetaImage.setExtra(data = metadata, item = item)
		return None

	def itemCast(self, metadata, item):
		# There is a bug in Kodi when setting a ListItem in the Player.
		# When setting the cast, the name/role/order is added correctly, but for some unknown reason the thumbnail is removed.
		# This only happens in Kodi's player. The cast thumbnails are correct when creating a directory or showing the movie/show info dialog.
		# To replicate the problem, add this to player.py:
		#	self.item.setCast([{'name' : 'vvv', 'role' : 'uuu', 'thumbnail' : 'https://image.tmdb.org/t/p/w185/gwQ5MfY68BvvyIbef3kr2XPilTx.jpg'}])
		#	self.updateInfoTag(self.item)
		#	tools.Time.sleep(1)
		#	tools.System.executeJson(method = 'Player.GetItem', parameters = {'playerid' : interface.Player().id(), 'properties':['cast']})
		# The RPC returns:
		#	{"id":1,"jsonrpc":"2.0","result":{"item":{"cast":[{"name":"vvv","order":-1,"role":"uuu"}],"label":"The Shawshank Redemption","type":"movie"}}}
		# The name/role/order is returned, but the thumbnail is missing.
		# This is most likley also the reason why the cast thumbnails do not show up in Kodi Kore or Yatse, since both probably use the RPC.
		# Various attempts were made to solve the problem, but without any success:
		#	1. Removing the cast/castandrole attributes before setting item.setInfo() and only use item.setCast().
		#	2. Setting the thumbnail as a HTTP URL, local file path, special:// path, URL-encoded image:// path, or <thumb>https://...</thumb>.
		#	3. Inserting the actor and thumbnail into Kodi's local DB (MyVideosXXX.db), in case the RPC retrieves the thumbnail from there.
		#	4. Using differnt attributes (thumbnail/thumb/photo/image) in the dictionaries set with item.setCast().
		# Maybe this will be fixed in Kodi 20 with the new functions/classes:
		#	self.item.setCast([xbmc.Actor('vvv', 'role', order=1, thumbnail='https://image.tmdb.org/t/p/w185/gwQ5MfY68BvvyIbef3kr2XPilTx.jpg')])

		if 'cast' in metadata:
			cast = metadata['cast']
			if cast:
				if Tools.isDictionary(cast[0]):
					castDetail = cast
				else:
					try: multi = Tools.isArray(cast[0]) and len(cast[0]) > 1
					except: multi = False
					if multi: castDetail = [{'name' : i[0], 'role' : i[1]} for i in cast]
					else: castDetail = [{'name' : i} for i in cast]

				# There is a bug in Kodi that the thumbnails are not shown, even if they were set.
				item.setCast(castDetail)

	def itemStream(self, stream, item):
		if stream:
			for type, data in stream.items():
				item.addStreamInfo(type, data)

	def itemProperty(self, properties, item, playable = None):
		if not properties: properties = {}
		if not 'IsPlayable' in properties:
			if playable is None: playable = self.mItemPlayable
			properties['IsPlayable'] = 'true' if playable else 'false'
		item.setProperties(properties)

	def itemPlayback(self, media, metadata, item):
		try: idImdb = metadata['imdb']
		except: idImdb = None
		try: idTmdb = metadata['tmdb']
		except: idTmdb = None
		try: idTvdb = metadata['tvdb']
		except: idTvdb = None
		try: idTrakt = metadata['trakt']
		except: idTrakt = None
		try: season = metadata['extra']['season']
		except:
			try: season = metadata['season']
			except: season = None
		try: episode = metadata['extra']['episode']
		except:
			try: episode = metadata['episode']
			except: episode = None

		# Series menu.
		if media == Media.TypeSeason and not 'season' in metadata: media = Media.TypeShow

		playback = self.mItemPlayback.retrieve(media = media, imdb = idImdb, tmdb = idTmdb, tvdb = idTvdb, trakt = idTrakt, season = season, episode = episode, adjust = self.mItemPlayback.AdjustSettings)
		count = playback['history']['count']['total']
		time = playback['history']['time']['last']
		progress = playback['progress']
		rating = playback['rating']

		# Do not use overlay/watched attribute, since Kodi (or maybe the Kodi skin) resets the playcount to 1, even if playcount is higher than 1.
		# https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/GUIListItem.h
		#metadata['overlay'] = 5 if count else 4

		metadata['playcount'] = count

		if time: metadata['lastplayed'] = Time.format(time, format = Time.FormatDateTime)

		# Resume/Progress
		# Do not set TotalTime, otherwise Kodi shows a resume popup dialog when clicking on the item, instead of going directly to scraping.
		# item.setProperty('TotalTime', str(metadata['duration']))
		# For some skins (eg: skin.eminence.2) the TotalTime has to be set for a different progress icon to show (25%, 50%, 75%).
		# Without TotalTime, the skins justs shows the default 25% icon.
		if progress:
			# Not listed under the Python docs, but listed under the infolabels docs.
			# Do not add, since Kodi throws a warning in the log: Unknown Video Info Key "percentplayed"
			#metadata['percentplayed'] = progress * 100

			if not media == Media.TypeShow and not media == Media.TypeSeason:
				if 'duration' in metadata and metadata['duration']: resume = progress * metadata['duration']
				else: resume = progress * (3600 if Media.typeTelevision(media) else 7200)
				item.setProperty('ResumeTime', str(int(resume)))

			# Used by the context menu to add a "Clear Progress" option.
			if not media == Media.TypeShow and not media == Media.TypeSeason: metadata['progress'] = progress

		if rating: metadata['userrating'] = rating

		if Media.typeTelevision(media):
			seasonsTotal = None
			episodesTotal = None
			episodesWatched = None
			episodesUnwatched = None

			if 'pack' in metadata and metadata['pack']:
				pack = metadata['pack']
				if season is None and episode is None:
					key = 'total' if self.mShowCounterSpecial else 'main'
					seasonsTotal = pack['count']['season'][key]
					episodesTotal = pack['count']['episode'][key]
				elif episode is None:
					seasonsTotal = 1
					for i in pack['seasons']:
						if i['number'] == season:
							episodesTotal = i['count']
							break
				else:
					seasonsTotal = 1
					episodesTotal = 1

			episodesWatched = playback['history']['count']['main']['unique'] if ('main' in playback['history']['count'] and not self.mShowCounterSpecial) else playback['history']['count']['unique']
			if not episodesWatched: episodesWatched = 0
			if episodesTotal: episodesUnwatched = episodesTotal - episodesWatched

			if self.mShowCounterEnabled:
				if not seasonsTotal is None: item.setProperty('TotalSeasons', str(seasonsTotal))
				if not episodesTotal is None: item.setProperty('TotalEpisodes', str(episodesTotal))
				if not episodesWatched is None: item.setProperty('WatchedEpisodes', str(episodesWatched))
				if not episodesUnwatched is None and self.mShowCounterUnwatched:
					if self.mShowCounterLimit: episodesUnwatched = min(99, episodesUnwatched)
					item.setProperty('UnWatchedEpisodes', str(episodesUnwatched))

				# Set this to allow the context menu to add "Mark As Unwatched" for partially watched shows/seasons.
				metadata['count'] = {
					'season' : {'total' : seasonsTotal},
					'episode' : {'total' : episodesTotal, 'watched' : episodesWatched, 'unwatched' : episodesUnwatched},
				}

			# For shows and seasons, only mark as watched if all episodes were watched.
			# If some episodes are watched and some are unwatched, add a resume time to indicate there are still some unwatched episodes.
			if media == Media.TypeShow or media == Media.TypeSeason:
				if episodesUnwatched and episodesUnwatched > 0:
					metadata['playcount'] = None
				else:
					count, remaining = self.mItemPlayback.count(media = media, imdb = idImdb, tmdb = idTmdb, tvdb = idTvdb, trakt = idTrakt, season = season, episode = episode, specials = self.mShowCounterSpecial, metadata = metadata, history = playback['history'])
					metadata['playcount'] = count

				if episodesWatched and episodesUnwatched: item.setProperty('ResumeTime', str(1))

	def itemContext(self,
		item,

		add = None,
		context = None,
		mode = None,

		media = None,
		kids = None,
		video = None,

		command = None,
		library = None,
		playlist = None,

		source = None,
		metadata = None,
		orion = None,

		shortcutId = None,
		shortcutLabel = None,
		shortcutLocation = None,
		shortcutCreate = None,
		shortcutDelete = None
	):
		# NB: Do not pass the cleaned metadata, since we need to extract the raw YouTube trailer URL, not the already created Gaia plugin command.
		menu = self.context(context = context, mode = mode, media = media, kids = kids, video = video, command = command, library = library, playlist = playlist, source = source, metadata = metadata, orion = orion, shortcutId = shortcutId, shortcutLabel = shortcutLabel, shortcutLocation = shortcutLocation, shortcutCreate = shortcutCreate, shortcutDelete = shortcutDelete)
		if menu and (add or add is None): item.addContextMenuItems(menu.menu(full = True))
		return menu

	def itemNext(self, metadata = None, media = None, kids = None, link = None, item = None):
		try:
			if link is None:
				if not Tools.isArray(metadata): metadata = [metadata]
				linkFallback = None
				for value in reversed(metadata): # Do reverse, since in flattened show menus the 'next' attribute might be different for each episode.
					# Do not check if 'next' has a value, since scanning should stop after the first (or rather last) 'next' has been found.
					# in episodes.py 'next' can be set to None to avoid a 'Next Page' to be show in flattened show menus if we are on the last page no more seasons).
					#if 'next' in value and value['next']:
					if 'next' in value:
						linkFallback = value['next']
						if not self.mShowInterleave or not 'season' in value or not value['season'] == 0: # Skip interleaved special episodes.
							link = value['next']
							break
				if not link: link = linkFallback

			if link:
				if not item: item = self.itemCreate()
				if not media: media = self.media(metadata = metadata[0])

				title = Format.fontItalic(32306)
				item.setLabel(title)
				item.setInfo(type = 'video', infoLabels = {'title' : title, 'tagline' : Translation.string(35317), 'plot' : Translation.string(35318)})

				icon = Icon.pathIcon(icon = 'next.png', default = 'DefaultFolder.png')
				images = {
					MetaImage.TypePoster : self.mThemeNextPoster,
					MetaImage.TypeThumb : icon,
					MetaImage.TypeFanart : self.mThemeFanart,
					MetaImage.TypeLandscape : self.mThemeFanart,
					MetaImage.TypeBanner : self.mThemeNextBanner,
					MetaImage.TypeClearlogo : icon,
					MetaImage.TypeClearart : icon,
					MetaImage.TypeDiscart : self.mThemeNextPoster,
					MetaImage.TypeIcon : icon,
				}
				MetaImage.set(item = item, images = images)

				if link and link.startswith(System.plugin()):
					command = link # Flattened show menus.
				else:
					parameters = {'link' : link, 'media' : media}
					if not kids is None: parameters['kids'] = kids
					if media == Media.TypeShow or media == Media.TypeSeason: action = 'showsRetrieve'
					elif media == Media.TypeEpisode: action = 'episodesRetrieve'
					else: action = 'moviesRetrieve'
					command = System.command(action = action, parameters = parameters)

				return [command, item, True]
		except: Logger.error()
		return None

	def itemRecap(self, metadata, media = None, kids = None, mixed = None):
		try:
			if media is None: media = self.media(metadata = metadata)
			if mixed is None: mixed = self.mixed(metadata = metadata) if (media == Media.TypeSeason or media == Media.TypeEpisode) else False

			if media == Media.TypeEpisode and not mixed:
				if self.mShowExtra and Recap.enabled():
					if Tools.isArray(metadata): metadata = metadata[0]
					season = metadata['season'] - 1
					episode = metadata['episode'] - 1
					if season > 0 and episode == 0:
						# Ensures that the Recaps are automatically marked as watched if the first episode in the season was watched.
						metadataReuse = {i : metadata[i] for i in ['playcount', 'watched', 'overlay', 'lastplayed', 'date', 'dateadded'] if i in metadata}
						metadataReuse['extra'] = {'season' : metadata['season'], 'episode' : metadata['episode']}

						metadataCurrent = metadata['seasonCurrent'] if 'seasonCurrent' in metadata else None
						metadataPrevious = metadata['seasonPrevious'] if 'seasonPrevious' in metadata else None
						metadataNext = metadata['seasonNext'] if 'seasonNext' in metadata else None
						metadata = Tools.copy(metadataPrevious if metadataPrevious else metadataCurrent)
						if not metadata: return None

						if metadataCurrent and MetaImage.Attribute in metadataCurrent: MetaImage.update(media = MetaImage.MediaSeason, images = Tools.copy(metadataCurrent[MetaImage.Attribute]), data = metadata)
						if metadataCurrent and MetaImage.Attribute in metadataCurrent and MetaImage.MediaShow in metadataCurrent[MetaImage.Attribute]: MetaImage.update(media = MetaImage.MediaSeason, images = metadataCurrent[MetaImage.Attribute][MetaImage.MediaShow], data = metadata, category = MetaImage.MediaShow)
						if metadataPrevious and MetaImage.Attribute in metadataPrevious: MetaImage.update(media = MetaImage.MediaSeason, images = metadataPrevious[MetaImage.Attribute], data = metadata, category = MetaImage.IndexPrevious)
						if metadataNext and MetaImage.Attribute in metadataNext: MetaImage.update(media = MetaImage.MediaSeason, images = metadataNext[MetaImage.Attribute], data = metadata, category = MetaImage.IndexNext)

						for i in ['episode', 'premiered', 'aired', 'genre', 'duration', 'airs', 'voting', 'rating', 'votes', 'userrating', 'labelBefore', 'labelAfter', 'plotBefore', 'plotAfter']:
							try: del metadata[i]
							except: pass
						metadata.update(metadataReuse)

						title = metadata['tvshowtitle'] if 'tvshowtitle' in metadata else metadata['title']
						label = Regex.replace(data = Translation.string(35362) % '', expression = '\s+', replacement = ' ', all = True)

						metadata['query'] = title
						metadata['duration'] = Recap.Duration
						metadata['title'] = metadata['originaltitle'] = label
						metadata['tagline'] = Translation.string(35362) % str(metadata['season'])
						metadata['plot'] = Translation.string(35456) % (str(metadata['season']), title)

						item = self.item(
							metadata = metadata,

							media = Media.TypeSpecialRecap,
							kids = kids,

							contextMode = Context.ModeVideo,

							video = Recap.Id,
							label = label,
						)
						return [item['command'], item['item'], False]
		except: Logger.error()
		return None

	def itemExtra(self, metadata, media = None, kids = None, mixed = None):
		try:
			if media is None: media = self.media(metadata = metadata)
			if mixed is None: mixed = self.mixed(metadata = metadata) if (media == Media.TypeSeason or media == Media.TypeEpisode) else False

			if media == Media.TypeEpisode and not mixed:
				if self.mShowExtra and Recap.enabled():
					if Tools.isArray(metadata): metadata = metadata[-1]
					season = metadata['season']
					if season > 0:
						ended = True

						# If the current last episode has not been aired yet, do not show extras.
						if ended:
							try: premiered = metadata['aired']
							except:
								try: premiered = metadata['premiered']
								except: premiered = None
							if premiered and Time.timestamp(fixedTime = premiered, format = Time.FormatDate) > Time.timestamp(): ended = False

						# If the current last episode is lower than the available episodes in the season, do not show extras.
						if ended and 'pack' in metadata and metadata['pack']:
							found = False
							for i in metadata['pack']['seasons']:
								if i['number'] == metadata['season']:
									found = True
									last = max([j['number'] for j in i['episodes']])
									if metadata['episode'] < last: ended = False
									break

							# Sometimes the new unaired season does not form part of the pack data.
							if not found and season > max([i['number'] for i in metadata['pack']['seasons']]): ended = False

						if ended:
							# Ensures that the Extras are automatically marked as watched if the last episode in the season was watched.
							metadataReuse = {i : metadata[i] for i in ['playcount', 'watched', 'overlay', 'lastplayed', 'date', 'dateadded'] if i in metadata}
							metadataReuse['extra'] = {'season' : metadata['season'], 'episode' : metadata['episode']}

							metadataCurrent = metadata['seasonCurrent'] if 'seasonCurrent' in metadata else None
							metadataPrevious = metadata['seasonPrevious'] if 'seasonPrevious' in metadata else None
							metadataNext = metadata['seasonNext'] if 'seasonNext' in metadata else None
							metadata = Tools.copy(metadataCurrent if metadataCurrent else metadataNext)
							if not metadata: return None

							if metadataCurrent and MetaImage.Attribute in metadataCurrent: MetaImage.update(media = MetaImage.MediaSeason, images = Tools.copy(metadataCurrent[MetaImage.Attribute]), data = metadata)
							if metadataCurrent and MetaImage.Attribute in metadataCurrent and MetaImage.MediaShow in metadataCurrent[MetaImage.Attribute]: MetaImage.update(media = MetaImage.MediaSeason, images = metadataCurrent[MetaImage.Attribute][MetaImage.MediaShow], data = metadata, category = MetaImage.MediaShow)
							if metadataPrevious and MetaImage.Attribute in metadataPrevious: MetaImage.update(media = MetaImage.MediaSeason, images = metadataPrevious[MetaImage.Attribute], data = metadata, category = MetaImage.IndexPrevious)
							if metadataNext and MetaImage.Attribute in metadataNext: MetaImage.update(media = MetaImage.MediaSeason, images = metadataNext[MetaImage.Attribute], data = metadata, category = MetaImage.IndexNext)

							for i in ['episode', 'premiered', 'aired', 'genre', 'duration', 'airs', 'voting', 'rating', 'votes', 'userrating', 'labelBefore', 'labelAfter', 'plotBefore', 'plotAfter']:
								try: del metadata[i]
								except: pass
							metadata.update(metadataReuse)

							title = metadata['tvshowtitle'] if 'tvshowtitle' in metadata else metadata['title']
							label = Regex.replace(data = Translation.string(35791) % '', expression = '\s+', replacement = ' ', all = True)

							metadata['title'] = metadata['originaltitle'] = label
							metadata['tagline'] = Translation.string(35791) % str(metadata['season'])
							metadata['plot'] = Translation.string(35649) % (str(metadata['season']), title)

							item = self.item(
								metadata = metadata,

								media = Media.TypeSpecialExtra,
								kids = kids,

								label = label,
							)
							return [item['command'], item['item'], True]
		except: Logger.error()
		return None

	###################################################################
	# DIRECTORY
	###################################################################

	def directories(self, metadatas, media = None, kids = None):
		items = []
		for metadata in metadatas:
			try:
				item = self.directory( media = media, kids = kids, metadata = metadata)
				if item: items.append([item['command'], item['item'], True])
			except: Logger.error()
		return items

	def directory(self, metadata = None, media = None, kids = None, link = None, item = None, context = None):
		try:
			if not item: item = self.itemCreate()
			if not link and 'link' in metadata: link = metadata['link']

			try: media = metadata['media']
			except: pass

			name = metadata['name']
			item.setLabel(name)

			if metadata['image'].startswith('http'): icon = thumb = poster = banner = metadata['image']
			else: icon, thumb, poster, banner = Icon.pathAll(icon = metadata['image'], default = self.mThemeThumb)
			images = {
				MetaImage.TypePoster : poster,
				MetaImage.TypeThumb : thumb,
				MetaImage.TypeFanart : self.mThemeFanart,
				MetaImage.TypeLandscape : self.mThemeFanart,
				MetaImage.TypeBanner : banner,
				MetaImage.TypeClearlogo : icon,
				MetaImage.TypeClearart : icon,
				MetaImage.TypeDiscart : poster,
				MetaImage.TypeIcon : icon,
			}
			MetaImage.set(item = item, images = images)

			parameters = {'media' : media}
			if link: parameters['link']= link
			if not kids is None: parameters['kids']= kids
			command = System.command(action = metadata['action'], parameters = parameters)

			context = self.itemContext(item = item, context = context, mode = Context.ModeGeneric, media = media, kids = kids, command = command, library = link, shortcutLabel = name, shortcutCreate = True)

			return {'item' : item, 'command' : command, 'context' : context, 'images' : images}
		except: Logger.error()
		return None

	###################################################################
	# CONTEXT
	###################################################################

	def context(self,
		context = None,
		mode = None,

		media = None,
		kids = None,
		video = None,

		command = None,
		library = None,
		playlist = None,

		source = None,
		metadata = None,
		orion = None,

		shortcutId = None,
		shortcutLabel = None,
		shortcutLocation = None,
		shortcutCreate = None,
		shortcutDelete = None,
	):
		if context is None: context = self.mItemContext
		if context:
			if metadata:
				if not mode: mode = Context.ModeItem
				if not media: media = self.media(metadata = metadata)
				if not command: command = self.command(metadata = metadata)
			else:
				if not mode: mode = Context.ModeGeneric

			return Context(
				mode = mode,
				media = media,
				kids = kids,
				video = video,

				link = command,
				library = library,
				playlist = playlist,

				source = source,
				metadata = metadata,
				orion = orion,

				shortcutId = shortcutId,
				shortcutLabel = shortcutLabel,
				shortcutLocation = shortcutLocation,
				shortcutCreate = shortcutCreate,
				shortcutDelete = shortcutDelete,
			)
		return None

	###################################################################
	# CLEAN
	###################################################################

	'''
		exclude:
			True: Attributes that should be removed even if they are officially supported by Kodi. Uses the default exclude attributes. This is useful if the skin should be forced (eg: streams directory - do not show the movie title, but use the custom createrd label instead).
			List: Attributes that should be removed even if they are officially supported by Kodi.
		studio:
			True: If no studio is specified in the metadata, add an empty string as the studio. This prevents some skins (eg: Aeon Nox) from showing thumbnails instead of of the stuio logo for certain views.
			False: If no studio is specified in the metadata, leave it as is and do not add an empty string.
	'''
	def clean(self, metadata, media = None, exclude = None, studio = True):
		if not metadata: return None
		if Tools.isString(metadata): metadata = Converter.jsonFrom(metadata)
		else: metadata = Tools.copy(metadata) # Create a copy, since we do not want to edit the outside dictionary passed to this function.
		self.cleanEmpty(metadata = metadata)

		if media is None: media = self.media(metadata = metadata)

		# Do not replace if already set (eg: video.py -> playing trailers in cinematic mode).
		if not 'mediatype' in metadata or not metadata['mediatype']:
			if Media.typeMovie(media): metadata['mediatype'] = 'movie'
			elif media == Media.TypeShow: metadata['mediatype'] = 'tvshow'
			elif media == Media.TypeSeason: metadata['mediatype'] = 'season'
			elif media == Media.TypeEpisode: metadata['mediatype'] = 'episode'
			elif media == Media.TypeSpecialRecap: metadata['mediatype'] = 'episode'
			elif media == Media.TypeSpecialExtra: metadata['mediatype'] = 'episode'

		# Do before cleaning the metadata, since we need the IDs.
		self.cleanTrailer(metadata = metadata, media = media)

		# Do before cleaning the metadata, since we need the 'voting'.
		self.cleanVoting(metadata = metadata)

		# Filter out non-existing/custom keys.
		# Otherise there are tons of errors in Kodi 18 log.
		allowed = self.mMetaAllowed
		if exclude:
			if not Tools.isArray(exclude): exclude = self.mMetaExclude
			allowed = [i for i in allowed if not i in exclude]
		metadata = {k : v for k, v in metadata.items() if k in allowed}

		try: metadata['duration'] = int(metadata['duration'])
		except: pass
		try: metadata['year'] = int(metadata['year'])
		except: pass

		# Do this before data is saved to the MetaCache.
		# Otherwise a bunch of regular expressions are called every time the menu is loaded.
		#self.cleanPlot(metadata = metadata)

		self.cleanCountry(metadata = metadata)
		self.cleanCast(metadata = metadata)
		self.cleanCrew(metadata = metadata)
		self.cleanStudio(metadata = metadata, empty = studio)

		return metadata

	def cleanEmpty(self, metadata):
		# Remove values with '0', otherwise they will show up as '0' in the Kodi info dialog.
		# This is legacy code. Once all values were updated to properly use None instead, this function can be removed.
		for key in self.mMetaNonzero:
			try:
				if metadata[key] == '0': del metadata[key]
			except: pass

	@classmethod
	def cleanSeason(self, metadata):
		for i in ['seasonCurrent', 'seasonPrevious', 'seasonNext']:
			try: del metadata[i]
			except: pass

	def cleanPlot(self, metadata):
		try:
			if 'plot' in metadata:
				plot = original = metadata['plot']
				if plot:
					# Some plots end with a URL.
					plot = Regex.remove(data = plot, expression = '.{10,}\.(\s*(?:[a-z\d\s\-\,\;\:\\\']*)(?:https?:\/\/|www\.).*?$)', group = 1)

					# Some plots end with "see full summary".
					plot = Regex.remove(data = plot, expression = '.{10,}(see\s*full\s*summary.*$)', group = 1).strip()

					# Some plots are cut off and do not end with a full stop.
					if Regex.match(data = plot, expression = '[a-z\d]$'): plot += ' ...'

					metadata['plot'] = plot
		except: Logger.error()

	def cleanCountry(self, metadata):
		try:
			# Change country codes to names.
			if 'country' in metadata and metadata['country']: metadata['country'] = [Country.name(i) if len(i) <= 3 else i for i in metadata['country']]
		except: Logger.error()

	def cleanVoting(self, metadata):
		'''
			The rating is calculated twice:
				1. Once the metadata is retrieved the first time and before it is saved to the MetaCache.
				   This ensures there is always a rating/votes if the metadata dictionary is used/passed elsewhere where is does not get cleaned first.
				2. Every time the metadata gets cleaned, that is every time amenu is loaded.
				   This has the advantage of not having to re-retrieve metadata (invalidating the metadata in MetaCache due to the 'settings' property) if the user changes the rating settings.
				   Another advantage is that we can later add code to retrieve the user's ratings from Trakt and overlaying it (similar to the playcount, watched, progress).
				   Then if the user casts a new vote, the rating can be dynamically added and reculated once the menu iss loaded, without having to re-retrieve metadata before saving it to MetaCache.
		'''
		voting = self.voting(metadata = metadata)
		if voting:
			for i in ['rating', 'userrating', 'votes']:
				if i in voting and not voting[i] is None: metadata[i] = voting[i]

	def cleanCast(self, metadata):
		try:
			for i in ['cast', 'castandrole']:
				if i in metadata:
					cast = metadata[i]
					if not cast: del metadata[i]
					elif cast and Tools.isDictionary(cast[0]): metadata[i] = [(j['name'], j['role']) for j in cast]
		except: Logger.error()

	def cleanCrew(self, metadata):
		try:
			for i in ['director', 'writer']:
				if i in metadata:
					crew = metadata[i]
					if crew:
						if Tools.isDictionary(crew[0]): metadata[i] = [j['name'] for j in crew]
						elif Tools.isArray(crew[0]): metadata[i] = [j[0] for j in crew]
					else: del metadata[i]
		except: Logger.error()

	def cleanStudio(self, metadata, empty = True):
		try:
			# Some studio names are not detected and no logos are shown in the menus (eg: Aeon Nox).
			if 'studio' in metadata and metadata['studio']:
				studios = None

				# Kodi documentation states that the studio attribute can be a string or a list.
				# However, with a list, some skins can for insatnce not set the studio logo (eg: Aeon Nox).
				if Tools.isArray(metadata['studio']):
					# These currently do not have logos in resource.images.studios.white.
					# Try picking another studio if possible.
					studios = [i for i in metadata['studio'] if not i in self.mStudioIgnore]
				else:
					studios = [metadata['studio']]

				if studios:
					for key, value in self.mStudioReplacePartial.items():
						for i in range(len(studios)):
							studios[i] = Regex.replace(data = studios[i], expression = key, replacement = value, group = 1)
					for key, value in self.mStudioReplaceFull.items():
						for i in range(len(studios)):
							if Regex.match(data = studios[i], expression = key):
								studios[i] = value

				# Studio logos do not work if there are multiple studios.
				if studios: metadata['studio'] = studios[0]

			# Some skins, like Aeon Nox (List View), show the poster in the menu when there is no studio.
			# This looks ugly, so set an empty studio.
			# Do not use space or empty string, since it will be ignored by the skin.
			# Do not use a string that contains visible characters (eg: '0'), since some view types (eg: Aeon Nox - Icons) will show the studio as text if no icon is availble.
			if empty and not 'studio' in metadata: metadata['studio'] = '\u200c'
		except: Logger.error()

	@classmethod
	def cleanTrailer(self, metadata, media = None):
		trailer = {}
		if media is None: media = self.media(metadata = metadata)

		trailer['video'] = 'trailer'
		trailer['media'] = media
		try:
			if metadata['imdb']: trailer['imdb'] = metadata['imdb']
		except: pass
		try:
			if metadata['tmdb']: trailer['tmdb'] = metadata['tmdb']
		except: pass
		try:
			if metadata['tvdb']: trailer['tvdb'] = metadata['tvdb']
		except: pass
		try: trailer['title'] = metadata['tvshowtitle']
		except: trailer['title'] = metadata['title']
		try: trailer['year'] = metadata['year']
		except: pass
		try: trailer['season'] = metadata['season']
		except: pass
		try: trailer['link'] = metadata['trailer']
		except: pass

		metadata['trailer'] = System.command(action = 'streamsVideo', parameters = trailer)

	###################################################################
	# VOTING
	###################################################################

	def voting(self, metadata):
		if not 'voting' in metadata: return None

		settingMain = None
		settingFallback = None
		settingUser = None
		if Media.typeTelevision(self.media(metadata = metadata)):
			settingMain = self.mRatingShowMain
			settingFallback = self.mRatingShowFallback
			settingUser = self.mRatingShowUser
		else:
			settingMain = self.mRatingMovieMain
			settingFallback = self.mRatingMovieFallback
			settingUser = self.mRatingMovieUser

		voting = metadata['voting']
		result = self.votingCalculate(setting = settingMain, voting = voting)
		if not result:
			result = self.votingCalculate(setting = settingFallback, voting = voting)
			if not result:
				result = self.votingCalculate(setting = MetaTools.RatingDefault, voting = voting)

		if not settingUser is False:
			rating = self.votingUser(voting = voting)
			if rating:
				if not result: result = {}
				result['userrating'] = rating
				if settingUser: result['rating'] = rating

		return result

	def votingUser(self, voting):
		if 'user' in voting:
			voting = voting['user']
			for provider in MetaTools.RatingProviders:
				if provider in voting:
					rating = voting[provider]
					if rating: return rating
		return None

	def votingCalculate(self, setting, voting):
		if setting in MetaTools.RatingProviders: return self.votingProvider(voting = voting, provider = setting)
		elif setting == MetaTools.RatingAverage: return self.votingAverage(voting = voting)
		elif setting == MetaTools.RatingAverageWeighted: return self.votingAverageWeighted(voting = voting)
		elif setting == MetaTools.RatingAverageLimited: return self.votingAverageLimited(voting = voting)
		else: return None

	def votingProvider(self, voting, provider):
		if provider in voting['rating'] and voting['rating'][provider]: return {'rating' : voting['rating'][provider], 'votes' : voting['votes'][provider]}
		else: return None

	def votingExtract(self, voting):
		result = {'rating' : [], 'votes' : []}

		for provider in MetaTools.RatingProviders:
			if provider in voting['rating']:
				rating = voting['rating'][provider]
				if rating:
					votes = 0
					if provider in voting['votes']: votes = voting['votes'][provider]
					result['rating'].append(rating)
					result['votes'].append(votes if votes else MetaTools.RatingVotes)

		return result

	def votingAverage(self, voting):
		result = self.votingExtract(voting = voting)
		if not result['rating']: return None
		result['rating'] = sum(result['rating']) / len(result['rating'])
		result['votes'] = sum(result['votes'])
		return result

	def votingAverageWeighted(self, voting):
		result = self.votingExtract(voting = voting)
		if not result['rating']: return None

		votes = sum(result['votes'])
		rating = 0
		for i in range(len(result['rating'])):
			rating += result['rating'][i] * result['votes'][i]
		rating /= float(votes)

		result['rating'] = rating
		result['votes'] = votes
		return result

	def votingAverageLimited(self, voting):
		result = self.votingExtract(voting = voting)
		if not result['rating']: return None

		# If the highest votes are more than 1000, limit it to twice the 2nd highest.
		# Example:
		#	Before: IMDb=100200 | TMDb=5000 | Trakt=100
		#	After: IMDb=10000 | TMDb=5000 | Trakt=100
		votesHighest = max(result['votes'])
		try: votesLimit = sorted(result['votes'])[-2]
		except: votesLimit = votesHighest
		votesLimit = (votesLimit * 2) if (votesHighest > 1000 and votesLimit > 500) else votesHighest

		votes = 0
		rating = 0
		for i in range(len(result['rating'])):
			vote = min(result['votes'][i], votesLimit)
			rating += result['rating'][i] * vote
			votes += vote
		rating /= float(votes)

		result['rating'] = rating
		result['votes'] = sum(result['votes'])
		return result

	###################################################################
	# KIDS
	###################################################################

	@classmethod
	def kidsOnly(self, kids):
		return kids == Selection.TypeInclude

	def kidsFilter(self, kids, items):
		if self.kidsOnly(kids = kids): items = [item for item in items if 'mpaa' in item and Kids.allowed(item['mpaa'])]
		return items

	###################################################################
	# FILTER
	###################################################################

	def filterKids(self, items, kids):
		return self.kidsFilter(kids = kids, items = items)

	def filterRelease(self, items, unknown = False, date = None, days = 0, hours = 0):
		result = []
		if date: date = Time.integer(str(date))
		else: date = Time.integer(Time.past(days = days, hours = hours, format = Time.FormatDate))

		for item in items:
			release = None
			if not release:
				try: release = item['aired']
				except: pass
			if not release:
				try: release = item['premiered']
				except: pass
			if not release:
				try: release = '%d-01-01' % item['year']
				except: pass

			if not release and unknown: result.append(item)
			elif release and Time.integer(release) <= date: result.append(item)

		return result

	def filterDuplicate(self, items):
		duplicates = {'imdb' : [], 'tmdb' : [], 'tvdb' : [], 'trakt' : []}
		result = []
		for item in items:
			found = False
			for id in duplicates.keys():
				if id in item and item[id]:
					if item[id] in duplicates[id]: found = True
					else: duplicates[id].append(item[id])
			if not found: result.append(item)
		return result

	def filterLimit(self, items, limit = True):
		if limit: return items[:50 if limit is True else limit]
		else: return items

	def filterNumber(self, items, season = None, episode = None, single = False):
		if Tools.isArray(items) and not season is None and not episode is None:
			season = abs(season)
			episode = abs(episode)

			number = [x for x, y in enumerate(items) if y['season'] == season and y['episode'] == episode]
			if not number: number = [x for x, y in enumerate(items) if y['season'] == season + 1 and (y['episode'] == 0 or y['episode'] == 1)]
			if number:
				number = number[-1]
				if self.mShowInterleave:
					if single: items = [y for x, y in enumerate(items) if x == number or y['season'] == 0]
					else: items = [y for x, y in enumerate(items) if x >= number or y['season'] == 0]
				else:
					if single: items = [y for x, y in enumerate(items) if x == number]
					else: items = [y for x, y in enumerate(items) if x >= number]

		return items

	###################################################################
	# PACK
	###################################################################

	@classmethod
	def pack(self, show = None, season = None, episode = None, extended = True, idImdb = None, idTmdb = None, idTvdb = None, idTrakt = None):
		try:
			# Trakt sometimes has more specials than TVDb.
			# Eg: Game of Thrones: TVDb has 53 specials, Trakt has 236 specials.
			if extended:
				from lib.modules.tools import Matcher
			if extended is True:
				from lib.modules import trakt as Trakt

				entries = []
				if show: entries.append(show)
				if season: entries.append(season[0])
				if episode: entries.append(episode[0])

				for entry in entries:
					if not idImdb: idImdb = entry.idTrakt()
					if not idTmdb: idTmdb = entry.idTmdb()
					if not idTvdb: idTvdb = entry.idTvdb()
					if not idTrakt: idTrakt = entry.idTrakt()

				if not idImdb and not idTrakt:
					ids = self.idShow(idImdb = idImdb, idTmdb = idTmdb, idTvdb = idTvdb, idTrakt = idTrakt)
					if 'trakt' in ids: idTrakt = ids['trakt']
					if 'imdb' in ids: idImdb = ids['imdb']

				if idTrakt or idImdb: extended = Trakt.getTVSeasonSummary(id = idTrakt or idImdb, season = 0, full = True, cache = False)

			# Determine the number of episodes per season to estimate season pack episode sizes.
			counts = {} # Do not use a list, since not all seasons are labeled by number. Eg: MythBusters
			episodes = []

			if show:
				season = show.season(sort = True)
				episode = show.episode(sort = True)

			if season:
				if not Tools.isArray(season): season = [season]
				for i in season:
					i = i.episode(sort = True)
					if i: episodes.extend(i)

			if episode:
				if not Tools.isArray(episode): episode = [episode]
				if episode: episodes.extend(episode)

			temp = []
			seen = set()
			for i in episodes:
				number = i.number(format = MetaData.FormatUniversal)
				if not number in seen:
					seen.add(number)
					temp.append(i)
			seasons = {}
			episodes = temp
			for i in episodes:
				number = i.numberSeason()
				if not number in counts: counts[number] = 0
				counts[number] += 1
				if not number in seasons: seasons[number] = []
				seasons[number].append(i)

			if not seasons and show:
				i = show.season()
				if i:
					for j in i:
						number = j.numberSeason()
						counts[number] = 0
						seasons[number] = []

			time = Time.timestamp()
			seasonItems = []
			for number, item in seasons.items():
				if item:
					releases = []
					episodeItems = {}
					for i in item:
						release = i.releaseDateFirst(format = MetaData.FormatTimestamp)
						releases.append(release if release else 0)
						episodeNumber = i.numberEpisode()
						episodeItems[episodeNumber] = {
							'title' : i.title(),
							'number' : episodeNumber,
							'duration' : i.duration(),
							'released' : release,
						}
					if number == 0 and Tools.isArray(extended):
						for i in extended:
							episodeNumber = i.get('number')
							episodeTitle = i.get('title')
							episodeDuration = i.get('runtime')
							if episodeDuration: episodeDuration *= 60
							episodePremiered = i.get('first_aired')
							if episodePremiered: episodePremiered = Time.timestamp(fixedTime = episodePremiered, iso = True)

							if episodeNumber in episodeItems:
								# TVDb often has missing duration and release dates.
								# Use Trakt values instead.
								# Compare titles and not episode numbers, since TVDb and Trakt specials sometimes do not have the same order.
								found = False
								if episodeTitle:
									for key, value in episodeItems.items():
										if value['title'] and Matcher.levenshtein(episodeTitle, value['title'][0], ignoreCase = True, ignoreSpace = True, ignoreNumeric = False, ignoreSymbol = True) > 0.99:
											if not value['duration']: value['duration'] = episodeDuration
											if not value['released']: value['released'] = episodePremiered
											found = True
											break

								# If both titles are missing, fall back to the episode number.
								if not found:
									episodeItem = episodeItems[episodeNumber]
									if not episodeItem['title']:
										if not episodeItem['duration']: episodeItem['duration'] = episodeDuration
										if not episodeItem['released']: episodeItem['released'] = episodePremiered

							else:
								episodeItems[episodeNumber] = {
									'title' : [episodeTitle],
									'number' : episodeNumber,
									'duration' : episodeDuration,
									'released' : episodePremiered,
								}

					episodeItems = list(episodeItems.values())
					episodeItems = Tools.listSort(episodeItems, key = lambda x : x['number'])

					counts[number] = 0
					seasons[number] = []
					for i in episodeItems:
						counts[number] += 1
						seasons[number].append(i['number'])

					# In case an episode does not have a duration, use the mean duration of other episodes as replacement.
					duration = []
					missing = 0
					for i in episodeItems:
						if i['duration']: duration.append(i['duration'])
						else: missing += 1
					total = sum(duration)
					valid = len(duration)
					duration = total
					if missing and valid: duration += int(total / float(valid)) * missing
					if not duration: duration = None

					seasonItems.append({
						'number' : number,
						'count' : len(episodeItems),
						'duration' : {'total' : duration, 'mean' : duration if duration is None else int(duration / float(len(episodeItems)))},
						'status' : MetaData.StatusEnded if len(releases) > 1 and releases[-1] > 0 and max(releases) < time else MetaData.StatusContinuing, # TVDb only has a status for shows, but not for seasons. Calculate the status based on the episode release dates.
						'released' : episodeItems[0]['released'] if episodeItems else None,
						'ended' : episodeItems[-1]['released'] if episodeItems else None,
						'episodes' : sorted(episodeItems, key = lambda i : i['number']),
					})
				else:
					seasonItems.append({
						'number' : number,
						'count' : 0,
						'duration' : {'total' : None, 'mean' : None},
						'status' : None,
						'released' : None,
						'ended' : None,
						'episodes' : [],
					})
			seasonItems.sort(key = lambda i : i['number'])

			countEpisodeTotal = sum(list(counts.values()))
			countSeasonTotal = len(counts.keys())
			try: countMeanTotal = int(round(float(countEpisodeTotal) / len(counts.keys())))
			except: countMeanTotal = 0 # If counts is empty

			countSpecial = 0
			if 0 in counts:
				countSpecial = counts[0]
				del counts[0]

			countEpisodeMain = sum(list(counts.values()))
			countSeasonMain = len(counts.keys())
			try: countMeanMain = int(round(float(countEpisodeMain) / len(counts.keys())))
			except: countMeanMain = 0 # If counts is empty

			if show and season is None and episode is None:
				return {
					'count' : {
						'season' : {'total' : countSeasonTotal, 'main' : countSeasonMain},
					},
					'status' : show.status(),
					'seasons' : seasonItems,
				}
			else:
				temp = [i['duration']['total'] for i in seasonItems if i['duration']['total']]
				count = sum([i['count'] for i in seasonItems if i['count']])
				durationShowTotal = sum(temp)
				if not durationShowTotal: durationShowTotal = None
				durationMeanTotal = durationShowTotal if durationShowTotal is None else int(durationShowTotal / float(count))
				temp = [i['duration']['total'] for i in seasonItems if i['duration']['total'] and not i['number'] == 0]
				count = sum([i['count'] for i in seasonItems if i['count'] and not i['number'] == 0])
				durationShowMain = sum(temp)
				if not durationShowMain: durationShowMain = None
				durationMeanMain = durationShowMain if durationShowMain is None else int(durationShowMain / float(count))
				return {
					'count' : {
						'season' : {'total' : countSeasonTotal, 'main' : countSeasonMain},
						'episode' : {'total' : countEpisodeTotal, 'main' : countEpisodeMain},
						'mean' : {'total' : countMeanTotal, 'main' : countMeanMain},
						'special' : countSpecial,
					},
					'duration' : {
						'show' : {'total' : durationShowTotal, 'main' : durationShowMain},
						'mean' : {'total' : durationMeanTotal, 'main' : durationMeanMain},
					},
					'status' : show.status() if show else None,
					'seasons' : seasonItems,
				}
		except: Logger.error()
		return None

	###################################################################
	# ID
	###################################################################

	@classmethod
	def _idCache(self, function, **kwargs):
		from lib.modules.cache import Cache
		return Cache.instance().cache(None, Cache.TimeoutWeek1, None, function, **kwargs)

	@classmethod
	def idMovie(self, idImdb = None, idTmdb = None, idTvdb = None, idTrakt = None, title = None, year = None, cache = True):
		if cache:
			# Do these separately, otherwise if this function is called with different ID-combination, it will not use the cached result.
			# Eg: the function is called 1st with only an IMDb ID, and a 2nd time with an IMDb and TMDb ID.
			result = None
			if not result and idImdb: result = self._idCache(function = self.idMovie, idImdb = idImdb, cache = False)
			if not result and idTmdb: result = self._idCache(function = self.idMovie, idTmdb = idTmdb, cache = False)
			if not result and idTrakt: result = self._idCache(function = self.idMovie, idTrakt = idTrakt, cache = False)
			if not result and idTvdb: result = self._idCache(function = self.idMovie, idTvdb = idTvdb, cache = False)
			if not result and title: result = self._idCache(function = self.idMovie, title = title, year = year, cache = False)
			return result

		result = {}
		lookup = False

		# Search Trakt by ID.
		try:
			if not result or not 'imdb' in result or not result['imdb']:
				if idImdb or idTmdb or idTvdb or idTrakt:
					from lib.modules import trakt
					lookup = True
					data = trakt.SearchMovie(imdb = idImdb, tmdb = idTmdb, tvdb = idTvdb, trakt = idTrakt, single = True, full = False, cache = False)
					if data and 'movie' in data:
						ids = data['movie'].get('ids')
						if ids:
							ids = {k : str(v) for k, v in ids.items() if v}
							if ids: Tools.update(result, ids, none = False)
		except: Logger.error()

		# Search TMDb by ID.
		# Do this after Trakt, since it only returns the IMDb/TMDb ID.
		try:
			if not result or not 'imdb' in result or not result['imdb']:
				if idImdb or idTmdb:
					from lib.modules.network import Networker
					from lib.modules.account import Tmdb
					key = Tmdb().key()
					lookup = True
					if idTmdb:
						link = 'https://api.themoviedb.org/3/movie/%s/external_ids' % idTmdb
						data = Networker().requestJson(method = Networker.MethodGet, link = link, data = {'api_key' : key})
						if data:
							id = data.get('imdb_id')
							if id: Tools.update(result, {'imdb' : id}, none = False)
					elif idImdb:
						link = 'https://api.themoviedb.org/3/find/%s' % idImdb
						data = Networker().requestJson(method = Networker.MethodGet, link = link, data = {'api_key' : key, 'external_source' : 'imdb_id'})
						if data and 'movie_results' in data and data['movie_results']:
							id = data['movie_results'][0].get('id')
							if id: Tools.update(result, {'tmdb' : id}, none = False)
		except: Logger.error()

		if not lookup and title:

			# Search Trakt by title.
			try:
				if not result or not 'imdb' in result or not result['imdb']:
					from lib.modules import trakt
					data = trakt.SearchMovie(title = title, year = year, single = True, full = False, cache = False)
					if data and 'movie' in data:
						ids = data['movie'].get('ids')
						if ids:
							result = {}
							ids = {k : str(v) for k, v in ids.items() if v}
							if ids: Tools.update(result, ids, none = False)
			except: Logger.error()

			# Search TMDb by title.
			# Do this after Trakt, since it only returns the IMDb ID.
			try:
				if not result or not 'imdb' in result or not result['imdb']:
					from lib.modules.account import Tmdb
					from lib.modules.network import Networker
					from lib.modules.clean import Title
					key = Tmdb().key()
					query = Title.clean(title)
					link = 'https://api.themoviedb.org/3/search/movie'
					data = Networker().requestJson(method = Networker.MethodGet, link = link, data = {'api_key' : key, 'query' : query, 'year' : year})
					if data and 'results' in data:
						data = data['results']
						for i in data:
							if (query == Title.clean(i['title']) or query == Title.clean(i['original_title'])):
								release = Regex.extract(data = i['release_date'], expression = '(\d{4})-', group = 1)
								if release: release = int(release)
								if not year or year == release:
									link = 'https://api.themoviedb.org/3/movie/%s/external_ids' % str(i['id'])
									data = Networker().requestJson(method = Networker.MethodGet, link = link, data = {'api_key' : key})
									if data:
										id = data.get('imdb_id')
										if id: Tools.update(result, {'imdb' : id, 'tmdb' : str(data.get('id'))}, none = False)
									break
			except: Logger.error()

		return result if result else None

	@classmethod
	def idShow(self, idImdb = None, idTmdb = None, idTvdb = None, idTrakt = None, title = None, year = None, cache = True):
		if cache:
			# Do these separately, otherwise if this function is called with different ID-combination, it will not use the cached result.
			# Eg: the function is called 1st with only an IMDb ID, and a 2nd time with an IMDb and TVDb ID.
			result = None
			if not result and idImdb: result = self._idCache(function = self.idShow, idImdb = idImdb, cache = False)
			if not result and idTvdb: result = self._idCache(function = self.idShow, idTvdb = idTvdb, cache = False)
			if not result and idTrakt: result = self._idCache(function = self.idShow, idTrakt = idTrakt, cache = False)
			if not result and idTmdb: result = self._idCache(function = self.idShow, idTmdb = idTmdb, cache = False)
			if not result and title: result = self._idCache(function = self.idShow, title = title, year = year, cache = False)
			return result

		result = {}
		manager = None
		lookup = False

		# Search TVDb by ID.
		# Search TVDb before Trakt, since Trakt sometimes returns multiple shows.
		try:
			if not result or not 'tvdb' in result or not result['tvdb']:
				if idImdb or idTvdb: # TVDb does not have the Trakt ID.
					if manager is None:
						from lib.meta.manager import MetaManager
						manager = MetaManager(provider = MetaManager.ProviderTvdb)
					lookup = True
					data = manager.search(idImdb = idImdb, idTvdb = idTvdb, idTrakt = idTrakt, media = MetaData.MediaShow, limit = 1, cache = False)
					if data:
						result = {}
						ids = data.id()
						if ids: Tools.update(result, ids, none = False)
		except: Logger.error()

		# Search Trakt by ID.
		# Trakt can sometimes return multiple shows for the same IMDb ID.
		# Eg: For "TVF Pitchers" Trakt returns
		#	{"trakt":100814,"slug":"tvf-pitchers-2015","tvdb":298807,"imdb":"tt4742876","tmdb":63180}
		#	{"trakt":185757,"slug":"tvf-pitchers-2015-185757","tvdb":298868,"imdb":"tt4742876","tmdb":63180}
		try:
			if not result or not 'tvdb' in result or not result['tvdb']:
				if idImdb or idTvdb or idTrakt:
					from lib.modules import trakt
					lookup = True
					data = trakt.SearchTVShow(imdb = idImdb, tmdb = idTmdb, tvdb = idTvdb, trakt = idTrakt, single = True, full = False, cache = False)
					if data and 'show' in data:
						ids = data['show'].get('ids')
						if ids:
							result = {}
							ids = {k : str(v) for k, v in ids.items() if v}
							if ids: Tools.update(result, ids, none = False)
		except: Logger.error()

		if not lookup and title:

			# Search TVDb by title.
			try:
				if not result or not 'tvdb' in result or not result['tvdb']:
					from lib.modules.clean import Title
					if manager is None:
						from lib.meta.manager import MetaManager
						manager = MetaManager(provider = MetaManager.ProviderTvdb)
					query = Title.clean(title)
					years = [year, year + 1, year - 1] if year else [None]
					found = False
					for i in years:
						data = manager.search(query = query, year = i, media = MetaData.MediaShow, cache = False)
						if data:
							for j in data:
								if query == Title.clean(j.titleOriginal(selection = MetaData.SelectionSingle)) and (not year or j.year() in years):
									result = {}
									ids = j.id()
									if ids:
										Tools.update(result, ids, none = False)
										found = True
										break
							if found: break
			except: Logger.error()

			# Search Trakt by title.
			try:
				if not result or not 'tvdb' in result or not result['tvdb']:
					from lib.modules import trakt
					data = trakt.SearchTVShow(title = title, year = year, single = True, full = False, cache = False)
					if data and 'show' in data:
						ids = data['show'].get('ids')
						if ids:
							result = {}
							ids = {k : str(v) for k, v in ids.items() if v}
							if ids: Tools.update(result, ids, none = False)
			except: Logger.error()

		return result if result else None
