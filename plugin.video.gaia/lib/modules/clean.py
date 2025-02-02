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

class Genre(object):

	Genres = None

	@classmethod
	def translate(self, genre, language):
		if Genre.Genres is None:
			Genre.Genres = {
				'bg' : {
					'Action' : u'\u0415\u043a\u0448\u044a\u043d',
					'Adventure' : u'\u041f\u0440\u0438\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435',
					'Animation' : u'\u0410\u043d\u0438\u043c\u0430\u0446\u0438\u044f',
					'Biography' : u'Biography',
					'Comedy' : u'\u041a\u043e\u043c\u0435\u0434\u0438\u044f',
					'Crime' : u'\u041a\u0440\u0438\u043c\u0438\u043d\u0430\u043b\u0435\u043d',
					'Documentary' : u'\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u043b\u0435\u043d',
					'Drama' : u'\u0414\u0440\u0430\u043c\u0430',
					'Family' : u'\u0421\u0435\u043c\u0435\u0435\u043d',
					'Fantasy' : u'\u0424\u0435\u043d\u0442\u044a\u0437\u0438',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0418\u0441\u0442\u043e\u0440\u0438\u0447\u0435\u0441\u043a\u0438',
					'Horror' : u'\u0423\u0436\u0430\u0441',
					'Music ' : u'\u041c\u0443\u0437\u0438\u043a\u0430',
					'Musical' : u'Musical',
					'Mystery' : u'\u041c\u0438\u0441\u0442\u0435\u0440\u0438\u044f',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0420\u043e\u043c\u0430\u043d\u0441',
					'Science Fiction' : u'\u041d\u0430\u0443\u0447\u043d\u0430\u002d\u0444\u0430\u043d\u0442\u0430\u0441\u0442\u0438\u043a\u0430',
					'Sci-Fi' : u'\u041d\u0430\u0443\u0447\u043d\u0430\u002d\u0444\u0430\u043d\u0442\u0430\u0441\u0442\u0438\u043a\u0430',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0422\u0440\u0438\u043b\u044a\u0440',
					'War' : u'\u0412\u043e\u0435\u043d\u0435\u043d',
					'Western' : u'\u0423\u0435\u0441\u0442\u044a\u0440\u043d',
				},
				'cs' : {
					'Action' : u'\u0041\u006b\u010d\u006e\u00ed',
					'Adventure' : u'\u0044\u006f\u0062\u0072\u006f\u0064\u0072\u0075\u017e\u006e\u00fd',
					'Animation' : u'\u0041\u006e\u0069\u006d\u006f\u0076\u0061\u006e\u00fd',
					'Biography' : u'Biography',
					'Comedy' : u'\u004b\u006f\u006d\u0065\u0064\u0069\u0065',
					'Crime' : u'\u004b\u0072\u0069\u006d\u0069',
					'Documentary' : u'\u0044\u006f\u006b\u0075\u006d\u0065\u006e\u0074\u00e1\u0072\u006e\u00ed',
					'Drama' : u'\u0044\u0072\u0061\u006d\u0061',
					'Family' : u'\u0052\u006f\u0064\u0069\u006e\u006e\u00fd',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0079',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0048\u0069\u0073\u0074\u006f\u0072\u0069\u0063\u006b\u00fd',
					'Horror' : u'\u0048\u006f\u0072\u006f\u0072',
					'Music ' : u'\u0048\u0075\u0064\u0065\u0062\u006e\u00ed',
					'Musical' : u'Musical',
					'Mystery' : u'\u004d\u0079\u0073\u0074\u0065\u0072\u0069\u00f3\u007a\u006e\u00ed',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0074\u0069\u0063\u006b\u00fd',
					'Science Fiction' : u'\u0056\u011b\u0064\u0065\u0063\u006b\u006f\u0066\u0061\u006e\u0074\u0061\u0073\u0074\u0069\u0063\u006b\u00fd',
					'Sci-Fi' : u'\u0056\u011b\u0064\u0065\u0063\u006b\u006f\u0066\u0061\u006e\u0074\u0061\u0073\u0074\u0069\u0063\u006b\u00fd',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0054\u0068\u0072\u0069\u006c\u006c\u0065\u0072',
					'War' : u'\u0056\u00e1\u006c\u0065\u010d\u006e\u00fd',
					'Western' : u'\u0057\u0065\u0073\u0074\u0065\u0072\u006e',
				},
				'da' : {
					'Action' : u'\u0041\u0063\u0074\u0069\u006f\u006e',
					'Adventure' : u'\u0045\u0076\u0065\u006e\u0074\u0079\u0072',
					'Animation' : u'\u0041\u006e\u0069\u006d\u0061\u0074\u0069\u006f\u006e',
					'Biography' : u'Biography',
					'Comedy' : u'\u004b\u006f\u006d\u0065\u0064\u0069\u0065',
					'Crime' : u'\u004b\u0072\u0069\u006d\u0069\u006e\u0061\u006c\u0069\u0074\u0065\u0074',
					'Documentary' : u'\u0044\u006f\u0063\u0075\u006d\u0065\u006e\u0074\u0061\u0072\u0079',
					'Drama' : u'\u0044\u0072\u0061\u006d\u0061',
					'Family' : u'\u0046\u0061\u006d\u0069\u006c\u0069\u0065',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0079',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0048\u0069\u0073\u0074\u006f\u0072\u0069\u0065 ',
					'Horror' : u'\u0047\u0079\u0073\u0065\u0072',
					'Music ' : u'\u004d\u0075\u0073\u0069\u006b',
					'Musical' : u'Musical',
					'Mystery' : u'\u004d\u0079\u0073\u0074\u0065\u0072\u0069\u0075\u006d',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0074\u0069\u006b',
					'Science Fiction' : u'\u0053\u0063\u0069\u002d\u0066\u0069',
					'Sci-Fi' : u'\u0053\u0063\u0069\u002d\u0066\u0069',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0054\u0068\u0072\u0069\u006c\u006c\u0065\u0072',
					'War' : u'\u004b\u0072\u0069\u0067',
					'Western' : u'\u0057\u0065\u0073\u0074\u0065\u0072\u006e',
				},
				'de' : {
					'Action' : u'\u0041\u0063\u0074\u0069\u006f\u006e',
					'Adventure' : u'\u0041\u0062\u0065\u006e\u0074\u0065\u0075\u0065\u0072',
					'Animation' : u'\u0041\u006e\u0069\u006d\u0061\u0074\u0069\u006f\u006e',
					'Biography' : u'Biography',
					'Comedy' : u'\u004b\u006f\u006d\u00f6\u0064\u0069\u0065',
					'Crime' : u'\u004b\u0072\u0069\u006d\u0069',
					'Documentary' : u'\u0044\u006f\u006b\u0075\u006d\u0065\u006e\u0074\u0061\u0072\u0066\u0069\u006c\u006d',
					'Drama' : u'\u0044\u0072\u0061\u006d\u0061',
					'Family' : u'\u0046\u0061\u006d\u0069\u006c\u0069\u0065',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0079',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0048\u0069\u0073\u0074\u006f\u0072\u0069\u0065',
					'Horror' : u'\u0048\u006f\u0072\u0072\u006f\u0072',
					'Music ' : u'\u004d\u0075\u0073\u0069\u006b',
					'Musical' : u'Musical',
					'Mystery' : u'\u004d\u0079\u0073\u0074\u0065\u0072\u0079',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u004c\u006f\u0076\u0065\u0073\u0074\u006f\u0072\u0079',
					'Science Fiction' : u'\u0053\u0063\u0069\u0065\u006e\u0063\u0065 \u0046\u0069\u0063\u0074\u0069\u006f\u006e',
					'Sci-Fi' : u'\u0053\u0063\u0069\u0065\u006e\u0063\u0065 \u0046\u0069\u0063\u0074\u0069\u006f\u006e',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0054\u0068\u0072\u0069\u006c\u006c\u0065\u0072',
					'War' : u'\u004b\u0072\u0069\u0065\u0067\u0073\u0066\u0069\u006c\u006d',
					'Western' : u'\u0057\u0065\u0073\u0074\u0065\u0072\u006e',
				},
				'el' : {
					'Action' : u'\u0394\u03c1\u03ac\u03c3\u03b7',
					'Adventure' : u'\u03a0\u03b5\u03c1\u03b9\u03c0\u03ad\u03c4\u03b5\u03b9\u03b1',
					'Animation' : u'\u039a\u03b9\u03bd\u03bf\u03cd\u03bc\u03b5\u03bd\u03b1 \u03a3\u03c7\u03ad\u03b4\u03b9\u03b1',
					'Biography' : u'\u0392\u03b9\u03bf\u03b3\u03c1\u03b1\u03c6\u03b9\u03ba\u03ae',
					'Comedy' : u'\u039a\u03c9\u03bc\u03c9\u03b4\u03af\u03b1',
					'Crime' : u'\u0391\u03c3\u03c4\u03c5\u03bd\u03bf\u03bc\u03b9\u03ba\u03ae',
					'Documentary' : u'\u039d\u03c4\u03bf\u03ba\u03c5\u03bc\u03b1\u03bd\u03c4\u03ad\u03c1',
					'Drama' : u'\u0394\u03c1\u03ac\u03bc\u03b1',
					'Family' : u'\u039f\u03b9\u03ba\u03bf\u03b3\u03b5\u03bd\u03b5\u03b9\u03b1\u03ba\u03ae',
					'Fantasy' : u'\u03a6\u03b1\u03bd\u03c4\u03b1\u03c3\u03af\u03b1\u03c2',
					'Game-Show' : u'\u03a4\u03b7\u03bb\u03b5\u03c0\u03b1\u03b9\u03c7\u03bd\u03af\u03b4\u03b9',
					'History' : u'\u0399\u03c3\u03c4\u03bf\u03c1\u03b9\u03ba\u03ae',
					'Horror' : u'\u03a4\u03c1\u03cc\u03bc\u03bf\u03c5',
					'Music ' : u'\u039c\u03bf\u03c5\u03c3\u03b9\u03ba\u03ae',
					'Musical' : u'Musical',
					'Mystery' : u'\u039c\u03c5\u03c3\u03c4\u03b7\u03c1\u03af\u03bf\u03c5',
					'News' : u'\u0395\u03b9\u03b4\u03ae\u03c3\u03b5\u03b9\u03c2',
					'Reality-TV' : u'\u03a1\u03b9\u03ac\u03bb\u03b9\u03c4\u03c5',
					'Romance' : u'\u03a1\u03bf\u03bc\u03b1\u03bd\u03c4\u03b9\u03ba\u03ae',
					'Science Fiction' : u'\u0395\u03c0\u002e \u03a6\u03b1\u03bd\u03c4\u03b1\u03c3\u03af\u03b1\u03c2',
					'Sci-Fi' : u'\u0395\u03c0\u002e \u03a6\u03b1\u03bd\u03c4\u03b1\u03c3\u03af\u03b1\u03c2',
					'Sport' : u'\u0391\u03b8\u03bb\u03b7\u03c4\u03b9\u03ba\u03ae',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0398\u03c1\u03af\u03bb\u03b5\u03c1',
					'War' : u'\u03a0\u03bf\u03bb\u03b5\u03bc\u03b9\u03ba\u03ae',
					'Western' : u'\u0393\u03bf\u03c5\u03ad\u03c3\u03c4\u03b5\u03c1\u03bd',
				},
				'es' : {
					'Action' : u'\u0041\u0063\u0063\u0069\u00f3\u006e',
					'Adventure' : u'\u0041\u0076\u0065\u006e\u0074\u0075\u0072\u0061',
					'Animation' : u'\u0041\u006e\u0069\u006d\u0061\u0063\u0069\u00f3\u006e',
					'Biography' : u'Biography',
					'Comedy' : u'\u0043\u006f\u006d\u0065\u0064\u0069\u0061',
					'Crime' : u'\u0043\u0072\u0069\u006d\u0065\u006e',
					'Documentary' : u'\u0044\u006f\u0063\u0075\u006d\u0065\u006e\u0074\u0061\u006c',
					'Drama' : u'\u0044\u0072\u0061\u006d\u0061',
					'Family' : u'\u0046\u0061\u006d\u0069\u006c\u0069\u0061',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u00ed\u0061',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0048\u0069\u0073\u0074\u006f\u0072\u0069\u0061',
					'Horror' : u'\u0054\u0065\u0072\u0072\u006f\u0072',
					'Music ' : u'\u004d\u00fa\u0073\u0069\u0063\u0061',
					'Musical' : u'Musical',
					'Mystery' : u'\u004d\u0069\u0073\u0074\u0065\u0072\u0069\u006f',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0063\u0065',
					'Science Fiction' : u'\u0043\u0069\u0065\u006e\u0063\u0069\u0061 \u0066\u0069\u0063\u0063\u0069\u00f3\u006e',
					'Sci-Fi' : u'\u0043\u0069\u0065\u006e\u0063\u0069\u0061 \u0066\u0069\u0063\u0063\u0069\u00f3\u006e',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0053\u0075\u0073\u0070\u0065\u006e\u0073\u0065',
					'War' : u'\u0047\u0075\u0065\u0072\u0072\u0061',
					'Western' : u'\u0057\u0065\u0073\u0074\u0065\u0072\u006e',
				},
				'fr' : {
					'Action' : u'\u0041\u0063\u0074\u0069\u006f\u006e',
					'Adventure' : u'\u0041\u0076\u0065\u006e\u0074\u0075\u0072\u0065',
					'Animation' : u'\u0041\u006e\u0069\u006d\u0061\u0074\u0069\u006f\u006e',
					'Biography' : u'Biography',
					'Comedy' : u'\u0043\u006f\u006d\u00e9\u0064\u0069\u0065',
					'Crime' : u'\u0043\u0072\u0069\u006d\u0065',
					'Documentary' : u'\u0044\u006f\u0063\u0075\u006d\u0065\u006e\u0074\u0061\u0069\u0072\u0065',
					'Drama' : u'\u0044\u0072\u0061\u006d\u0065',
					'Family' : u'\u0046\u0061\u006d\u0069\u006c\u0069\u0061\u006c',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0074\u0069\u0071\u0075\u0065',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0048\u0069\u0073\u0074\u006f\u0069\u0072\u0065',
					'Horror' : u'\u0048\u006f\u0072\u0072\u0065\u0075\u0072',
					'Music ' : u'\u004d\u0075\u0073\u0069\u0071\u0075\u0065',
					'Musical' : u'Musical',
					'Mystery' : u'\u004d\u0079\u0073\u0074\u00e8\u0072\u0065',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0063\u0065',
					'Science Fiction' : u'\u0053\u0063\u0069\u0065\u006e\u0063\u0065\u002d\u0046\u0069\u0063\u0074\u0069\u006f\u006e',
					'Sci-Fi' : u'\u0053\u0063\u0069\u0065\u006e\u0063\u0065\u002d\u0046\u0069\u0063\u0074\u0069\u006f\u006e',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0054\u0068\u0072\u0069\u006c\u006c\u0065\u0072',
					'War' : u'\u0047\u0075\u0065\u0072\u0072\u0065',
					'Western' : u'\u0057\u0065\u0073\u0074\u0065\u0072\u006e',
				},
				'he' : {
					'Action' : u'\u05d0\u05e7\u05e9\u05df',
					'Adventure' : u'\u05d4\u05e8\u05e4\u05ea\u05e7\u05d0\u05d5\u05ea',
					'Animation' : u'\u05d0\u05e0\u05d9\u05de\u05e6\u05d9\u05d4',
					'Biography' : u'Biography',
					'Comedy' : u'\u05e7\u05d5\u05de\u05d3\u05d9\u05d4',
					'Crime' : u'\u05e4\u05e9\u05e2',
					'Documentary' : u'\u05d3\u05d5\u05e7\u05d5\u05de\u05e0\u05d8\u05e8\u05d9',
					'Drama' : u'\u05d3\u05e8\u05de\u05d4',
					'Family' : u'\u05de\u05e9\u05e4\u05d7\u05d4',
					'Fantasy' : u'\u05e4\u05e0\u05d8\u05d6\u05d9\u05d4',
					'Game-Show' : u'Game-Show',
					'History' : u'\u05d4\u05e1\u05d8\u05d5\u05e8\u05d9\u05d4',
					'Horror' : u'\u05d0\u05d9\u05de\u05d4',
					'Music ' : u'\u05de\u05d5\u05e1\u05d9\u05e7\u05d4',
					'Musical' : u'Musical',
					'Mystery' : u'\u05de\u05e1\u05ea\u05d5\u05e8\u05d9\u05df',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u05e8\u05d5\u05de\u05e0\u05d8\u05d9',
					'Science Fiction' : u'\u05de\u05d3\u05e2 \u05d1\u05d3\u05d9\u05d5\u05e0\u05d9',
					'Sci-Fi' : u'\u05de\u05d3\u05e2 \u05d1\u05d3\u05d9\u05d5\u05e0\u05d9',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u05de\u05d5\u05ea\u05d7\u05df',
					'War' : u'\u05de\u05dc\u05d7\u05de\u05d4',
					'Western' : u'\u05de\u05e2\u05e8\u05d1\u05d5\u05df',
				},
				'hu' : {
					'Action' : u'\u0041\u006b\u0063\u0069\u00f3',
					'Adventure' : u'\u004b\u0061\u006c\u0061\u006e\u0064',
					'Animation' : u'\u0041\u006e\u0069\u006d\u00e1\u0063\u0069\u00f3\u0073',
					'Biography' : u'Biography',
					'Comedy' : u'\u0056\u00ed\u0067\u006a\u00e1\u0074\u00e9\u006b',
					'Crime' : u'\u0042\u0171\u006e\u00fc\u0067\u0079\u0069',
					'Documentary' : u'\u0044\u006f\u006b\u0075\u006d\u0065\u006e\u0074\u0075\u006d',
					'Drama' : u'\u0044\u0072\u00e1\u006d\u0061',
					'Family' : u'\u0043\u0073\u0061\u006c\u00e1\u0064\u0069',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0079',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0054\u00f6\u0072\u0074\u00e9\u006e\u0065\u006c\u006d\u0069',
					'Horror' : u'\u0048\u006f\u0072\u0072\u006f\u0072',
					'Music ' : u'\u005a\u0065\u006e\u0065\u0069',
					'Musical' : u'Musical',
					'Mystery' : u'\u0052\u0065\u006a\u0074\u00e9\u006c\u0079',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0074\u0069\u006b\u0075\u0073',
					'Science Fiction' : u'\u0053\u0063\u0069\u002d\u0046\u0069',
					'Sci-Fi' : u'\u0053\u0063\u0069\u002d\u0046\u0069',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0054\u0068\u0072\u0069\u006c\u006c\u0065\u0072',
					'War' : u'\u0048\u00e1\u0062\u006f\u0072\u00fa\u0073',
					'Western' : u'\u0057\u0065\u0073\u0074\u0065\u0072\u006e',
				},
				'it' : {
					'Action' : u'\u0041\u007a\u0069\u006f\u006e\u0065',
					'Adventure' : u'\u0041\u0076\u0076\u0065\u006e\u0074\u0075\u0072\u0061',
					'Animation' : u'\u0041\u006e\u0069\u006d\u0061\u007a\u0069\u006f\u006e\u0065',
					'Biography' : u'Biography',
					'Comedy' : u'\u0043\u006f\u006d\u006d\u0065\u0064\u0069\u0061',
					'Crime' : u'\u0043\u0072\u0069\u006d\u0065',
					'Documentary' : u'\u0044\u006f\u0063\u0075\u006d\u0065\u006e\u0074\u0061\u0072\u0069\u006f',
					'Drama' : u'\u0044\u0072\u0061\u006d\u006d\u0061',
					'Family' : u'\u0046\u0061\u006d\u0069\u0067\u006c\u0069\u0061',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0079',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0053\u0074\u006f\u0072\u0069\u0061',
					'Horror' : u'\u0048\u006f\u0072\u0072\u006f\u0072',
					'Music ' : u'\u004d\u0075\u0073\u0069\u0063\u0061',
					'Musical' : u'Musical',
					'Mystery' : u'\u004d\u0069\u0073\u0074\u0065\u0072\u006f',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0063\u0065',
					'Science Fiction' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0063\u0069\u0065\u006e\u007a\u0061',
					'Sci-Fi' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0063\u0069\u0065\u006e\u007a\u0061',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0054\u0068\u0072\u0069\u006c\u006c\u0065\u0072',
					'War' : u'\u0047\u0075\u0065\u0072\u0072\u0061',
					'Western' : u'\u0057\u0065\u0073\u0074\u0065\u0072\u006e',
				},
				'ja' : {
					'Action' : u'\u30a2\u30af\u30b7\u30e7\u30f3',
					'Adventure' : u'\u30a2\u30c9\u30d9\u30f3\u30c1\u30e3\u30fc',
					'Animation' : u'\u30a2\u30cb\u30e1\u30fc\u30b7\u30e7\u30f3',
					'Biography' : u'Biography',
					'Comedy' : u'\u30b3\u30e1\u30c7\u30a3',
					'Crime' : u'\u72af\u7f6a',
					'Documentary' : u'\u30c9\u30ad\u30e5\u30e1\u30f3\u30bf\u30ea\u30fc',
					'Drama' : u'\u30c9\u30e9\u30de',
					'Family' : u'\u30d5\u30a1\u30df\u30ea\u30fc',
					'Fantasy' : u'\u30d5\u30a1\u30f3\u30bf\u30b8\u30fc',
					'Game-Show' : u'Game-Show',
					'History' : u'\u5c65\u6b74',
					'Horror' : u'\u30db\u30e9\u30fc',
					'Music ' : u'\u97f3\u697d',
					'Musical' : u'Musical',
					'Mystery' : u'\u8b0e',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u30ed\u30de\u30f3\u30b9',
					'Science Fiction' : u'\u30b5\u30a4\u30a8\u30f3\u30b9\u30d5\u30a3\u30af\u30b7\u30e7\u30f3',
					'Sci-Fi' : u'\u30b5\u30a4\u30a8\u30f3\u30b9\u30d5\u30a3\u30af\u30b7\u30e7\u30f3',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u30b9\u30ea\u30e9\u30fc',
					'War' : u'\u6226\u4e89',
					'Western' : u'\u897f\u6d0b',
				},
				'ko' : {
					'Action' : u'\uc561\uc158',
					'Adventure' : u'\ubaa8\ud5d8',
					'Animation' : u'\uc560\ub2c8\uba54\uc774\uc158',
					'Biography' : u'Biography',
					'Comedy' : u'\ucf54\ubbf8\ub514',
					'Crime' : u'\ubc94\uc8c4',
					'Documentary' : u'\ub2e4\ud050\uba58\ud130\ub9ac',
					'Drama' : u'\ub4dc\ub77c\ub9c8',
					'Family' : u'\uac00\uc871',
					'Fantasy' : u'\ud310\ud0c0\uc9c0',
					'Game-Show' : u'Game-Show',
					'History' : u'\uc5ed\uc0ac',
					'Horror' : u'\uacf5\ud3ec',
					'Music ' : u'\uc74c\uc545',
					'Musical' : u'Musical',
					'Mystery' : u'\ubbf8\uc2a4\ud130\ub9ac',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\ub85c\ub9e8\uc2a4',
					'Science Fiction' : u'\u0053\u0046',
					'Sci-Fi' : u'\u0053\u0046',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\uc2a4\ub9b4\ub7ec',
					'War' : u'\uc804\uc7c1',
					'Western' : u'\uc11c\ubd80',
				},
				'nl' : {
					'Action' : u'\u0041\u0063\u0074\u0069\u0065',
					'Adventure' : u'\u0041\u0076\u006f\u006e\u0074\u0075\u0075\u0072',
					'Animation' : u'\u0041\u006e\u0069\u006d\u0061\u0074\u0069\u0065',
					'Biography' : u'Biography',
					'Comedy' : u'\u004b\u006f\u006d\u0065\u0064\u0069\u0065',
					'Crime' : u'\u004d\u0069\u0073\u0064\u0061\u0061\u0064',
					'Documentary' : u'\u0044\u006f\u0063\u0075\u006d\u0065\u006e\u0074\u0061\u0069\u0072\u0065',
					'Drama' : u'\u0044\u0072\u0061\u006d\u0061',
					'Family' : u'\u0046\u0061\u006d\u0069\u006c\u0069\u0065',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0069\u0065',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0048\u0069\u0073\u0074\u006f\u0072\u0069\u0073\u0063\u0068',
					'Horror' : u'\u0048\u006f\u0072\u0072\u006f\u0072',
					'Music ' : u'\u004d\u0075\u007a\u0069\u0065\u006b',
					'Musical' : u'Musical',
					'Mystery' : u'\u004d\u0079\u0073\u0074\u0065\u0072\u0069\u0065',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0074\u0069\u0065\u006b',
					'Science Fiction' : u'\u0053\u0063\u0069\u0065\u006e\u0063\u0065\u0066\u0069\u0063\u0074\u0069\u006f\u006e',
					'Sci-Fi' : u'\u0053\u0063\u0069\u0065\u006e\u0063\u0065\u0066\u0069\u0063\u0074\u0069\u006f\u006e',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0054\u0068\u0072\u0069\u006c\u006c\u0065\u0072',
					'War' : u'\u004f\u006f\u0072\u006c\u006f\u0067',
					'Western' : u'\u0057\u0065\u0073\u0074\u0065\u0072\u006e',
				},
				'pl' : {
					'Action' : u'\u0041\u006b\u0063\u006a\u0061',
					'Adventure' : u'\u0050\u0072\u007a\u0079\u0067\u006f\u0064\u006f\u0077\u0079',
					'Animation' : u'\u0041\u006e\u0069\u006d\u0061\u0063\u006a\u0061',
					'Biography' : u'Biography',
					'Comedy' : u'\u004b\u006f\u006d\u0065\u0064\u0069\u0061',
					'Crime' : u'\u004b\u0072\u0079\u006d\u0069\u006e\u0061\u0142',
					'Documentary' : u'\u0044\u006f\u006b\u0075\u006d\u0065\u006e\u0074\u0061\u006c\u006e\u0079',
					'Drama' : u'\u0044\u0072\u0061\u006d\u0061\u0074',
					'Family' : u'\u0046\u0061\u006d\u0069\u006c\u0069\u006a\u006e\u0079',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0079',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0048\u0069\u0073\u0074\u006f\u0072\u0079\u0063\u007a\u006e\u0079',
					'Horror' : u'\u0048\u006f\u0072\u0072\u006f\u0072',
					'Music ' : u'\u004d\u0075\u007a\u0079\u0063\u007a\u006e\u0079',
					'Musical' : u'Musical',
					'Mystery' : u'\u0054\u0061\u006a\u0065\u006d\u006e\u0069\u0063\u0061',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0073',
					'Science Fiction' : u'\u0053\u0063\u0069\u002d\u0046\u0069',
					'Sci-Fi' : u'\u0053\u0063\u0069\u002d\u0046\u0069',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0054\u0068\u0072\u0069\u006c\u006c\u0065\u0072',
					'War' : u'\u0057\u006f\u006a\u0065\u006e\u006e\u0079',
					'Western' : u'\u0057\u0065\u0073\u0074\u0065\u0072\u006e',
				},
				'pt' : {
					'Action' : u'\u0041\u00e7\u00e3\u006f',
					'Adventure' : u'\u0041\u0076\u0065\u006e\u0074\u0075\u0072\u0061',
					'Animation' : u'\u0041\u006e\u0069\u006d\u0061\u00e7\u00e3\u006f',
					'Biography' : u'Biography',
					'Comedy' : u'\u0043\u006f\u006d\u00e9\u0064\u0069\u0061',
					'Crime' : u'\u0043\u0072\u0069\u006d\u0065',
					'Documentary' : u'\u0044\u006f\u0063\u0075\u006d\u0065\u006e\u0074\u00e1\u0072\u0069\u006f',
					'Drama' : u'\u0044\u0072\u0061\u006d\u0061',
					'Family' : u'\u0046\u0061\u006d\u00ed\u006c\u0069\u0061',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0069\u0061',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0048\u0069\u0073\u0074\u00f3\u0072\u0069\u0061',
					'Horror' : u'\u0054\u0065\u0072\u0072\u006f\u0072',
					'Music ' : u'\u004d\u00fa\u0073\u0069\u0063\u0061',
					'Musical' : u'Musical',
					'Mystery' : u'\u004d\u0069\u0073\u0074\u00e9\u0072\u0069\u006f',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0063\u0065',
					'Science Fiction' : u'\u0046\u0069\u0063\u00e7\u00e3\u006f \u0063\u0069\u0065\u006e\u0074\u00ed\u0066\u0069\u0063\u0061',
					'Sci-Fi' : u'\u0046\u0069\u0063\u00e7\u00e3\u006f \u0063\u0069\u0065\u006e\u0074\u00ed\u0066\u0069\u0063\u0061',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0054\u0068\u0072\u0069\u006c\u006c\u0065\u0072',
					'War' : u'\u0047\u0075\u0065\u0072\u0072\u0061',
					'Western' : u'\u0046\u0061\u0072\u006f\u0065\u0073\u0074\u0065',
				},
				'ro' : {
					'Action' : u'\u0041\u0063\u021b\u0069\u0075\u006e\u0065',
					'Adventure' : u'\u0041\u0076\u0065\u006e\u0074\u0075\u0072\u0069',
					'Animation' : u'\u0041\u006e\u0069\u006d\u0061\u0163\u0069\u0065',
					'Biography' : u'Biography',
					'Comedy' : u'\u0043\u006f\u006d\u0065\u0064\u0069\u0065',
					'Crime' : u'\u0043\u0072\u0069\u006d\u0103',
					'Documentary' : u'\u0044\u006f\u0063\u0075\u006d\u0065\u006e\u0074\u0061\u0072',
					'Drama' : u'\u0044\u0072\u0061\u006d\u0103',
					'Family' : u'\u0046\u0061\u006d\u0069\u006c\u0069\u0065',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0079',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0049\u0073\u0074\u006f\u0072\u0069\u0063',
					'Horror' : u'\u0048\u006f\u0072\u0072\u006f\u0072',
					'Music ' : u'\u004d\u0075\u007a\u0069\u0063\u0103',
					'Musical' : u'Musical',
					'Mystery' : u'\u004d\u0069\u0073\u0074\u0065\u0072',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0074\u0069\u0063',
					'Science Fiction' : u'\u0053\u0046',
					'Sci-Fi' : u'\u0053\u0046',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0054\u0068\u0072\u0069\u006c\u006c\u0065\u0072',
					'War' : u'\u0052\u0103\u007a\u0062\u006f\u0069',
					'Western' : u'\u0057\u0065\u0073\u0074\u0065\u0072\u006e',
				},
				'ru' : {
					'Action' : u'\u0431\u043e\u0435\u0432\u0438\u043a',
					'Adventure' : u'\u043f\u0440\u0438\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f',
					'Animation' : u'\u043c\u0443\u043b\u044c\u0442\u0444\u0438\u043b\u044c\u043c',
					'Biography' : u'Biography',
					'Comedy' : u'\u043a\u043e\u043c\u0435\u0434\u0438\u044f',
					'Crime' : u'\u043a\u0440\u0438\u043c\u0438\u043d\u0430\u043b',
					'Documentary' : u'\u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u043b\u044c\u043d\u044b\u0439',
					'Drama' : u'\u0434\u0440\u0430\u043c\u0430',
					'Family' : u'\u0441\u0435\u043c\u0435\u0439\u043d\u044b\u0439',
					'Fantasy' : u'\u0444\u044d\u043d\u0442\u0435\u0437\u0438',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0438\u0441\u0442\u043e\u0440\u0438\u044f',
					'Horror' : u'\u0443\u0436\u0430\u0441\u044b',
					'Music ' : u'\u043c\u0443\u0437\u044b\u043a\u0430',
					'Musical' : u'Musical',
					'Mystery' : u'\u0434\u0435\u0442\u0435\u043a\u0442\u0438\u0432',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u043c\u0435\u043b\u043e\u0434\u0440\u0430\u043c\u0430',
					'Science Fiction' : u'\u0444\u0430\u043d\u0442\u0430\u0441\u0442\u0438\u043a\u0430',
					'Sci-Fi' : u'\u0444\u0430\u043d\u0442\u0430\u0441\u0442\u0438\u043a\u0430',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0442\u0440\u0438\u043b\u043b\u0435\u0440',
					'War' : u'\u0432\u043e\u0435\u043d\u043d\u044b\u0439',
					'Western' : u'\u0432\u0435\u0441\u0442\u0435\u0440\u043d',
				},
				'sl' : {
					'Action' : u'\u0041\u006b\u0063\u0069\u006a\u0061',
					'Adventure' : u'\u0041\u0076\u0061\u006e\u0074\u0075\u0072\u0061',
					'Animation' : u'\u0041\u006e\u0069\u006d\u0061\u0063\u0069\u006a\u0061',
					'Biography' : u'Biography',
					'Comedy' : u'\u041a\u043e\u043c\u0435\u0064\u0069\u006a\u0061',
					'Crime' : u'\u041a\u0072\u0069\u006d\u0069\u006e\u0061\u006c\u006e\u0069',
					'Documentary' : u'\u0044\u006f\u006b\u0075\u006d\u0065\u006e\u0074\u0061\u0072\u006e\u0069',
					'Drama' : u'\u0044\u0072\u0430\u043c\u0430',
					'Family' : u'\u0044\u0072\u0075\u017e\u0069\u006e\u0073\u006b\u0069',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0074\u0069\u006b\u0061',
					'Game-Show' : u'Game-Show',
					'History' : u'\u005a\u0067\u006f\u0064\u006f\u0076\u0069\u006e\u0073\u006b\u0069',
					'Horror' : u'\u0047\u0072\u006f\u007a\u006c\u006a\u0069\u0076\u006b\u0061',
					'Music ' : u'\u0047\u006c\u0061\u007a\u0062\u0065\u006e\u0069',
					'Musical' : u'Musical',
					'Mystery' : u'\u004d\u0069\u0073\u0074\u0065\u0072\u0069\u006a\u0061',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0074\u0069\u006b\u0061',
					'Science Fiction' : u'\u005a\u006e\u0061\u006e\u0073\u0074\u0076\u0065\u006e\u0061 \u0066\u0061\u006e\u0074\u0061\u0073\u0074\u0069\u006b\u0061',
					'Sci-Fi' : u'\u005a\u006e\u0061\u006e\u0073\u0074\u0076\u0065\u006e\u0061 \u0066\u0061\u006e\u0074\u0061\u0073\u0074\u0069\u006b\u0061',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0422\u0072\u0069\u006c\u0065\u0072',
					'War' : u'\u0056\u006f\u006a\u006e\u006f\u002d\u0070\u006f\u006c\u0069\u0074\u0069\u010d\u006e\u0069',
					'Western' : u'\u0057\u0065\u0073\u0074\u0065\u0072\u006e',
				},
				'sr' : {
					'Action' : u'\u0410\u043a\u0446\u0438\u043e\u043d\u0438',
					'Adventure' : u'\u0410\u0432\u0430\u043d\u0442\u0443\u0440\u0438\u0441\u0442\u0438\u0447\u043a\u0438',
					'Animation' : u'\u0426\u0440\u0442\u0430\u043d\u0438',
					'Biography' : u'Biography',
					'Comedy' : u'\u041a\u043e\u043c\u0435\u0434\u0438\u0458\u0430',
					'Crime' : u'\u041a\u0440\u0438\u043c\u0438',
					'Documentary' : u'\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u0440\u043d\u0438',
					'Drama' : u'\u0414\u0440\u0430\u043c\u0430',
					'Family' : u'\u041f\u043e\u0440\u043e\u0434\u0438\u0447\u043d\u0438',
					'Fantasy' : u'\u0424\u0430\u043d\u0442\u0430\u0441\u0442\u0438\u043a\u0430',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0418\u0441\u0442\u043e\u0440\u0438\u0458\u0441\u043a\u0438',
					'Horror' : u'\u0425\u043e\u0440\u043e\u0440',
					'Music ' : u'\u041c\u0443\u0437\u0438\u0447\u043a\u0438',
					'Musical' : u'Musical',
					'Mystery' : u'\u041c\u0438\u0441\u0442\u0435\u0440\u0438\u0458\u0430',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0409\u0443\u0431\u0430\u0432\u043d\u0438',
					'Science Fiction' : u'\u041d\u0430\u0443\u0447\u043d\u0430 \u0444\u0430\u043d\u0442\u0430\u0441\u0442\u0438\u043a\u0430',
					'Sci-Fi' : u'\u041d\u0430\u0443\u0447\u043d\u0430 \u0444\u0430\u043d\u0442\u0430\u0441\u0442\u0438\u043a\u0430',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0422\u0440\u0438\u043b\u0435\u0440',
					'War' : u'\u0420\u0430\u0442\u043d\u0438',
					'Western' : u'\u0412\u0435\u0441\u0442\u0435\u0440\u043d',
				},
				'sv' : {
					'Action' : u'\u0041\u0063\u0074\u0069\u006f\u006e',
					'Adventure' : u'\u00c4\u0076\u0065\u006e\u0074\u0079\u0072',
					'Animation' : u'\u0041\u006e\u0069\u006d\u0065\u0072\u0061\u0074',
					'Biography' : u'Biography',
					'Comedy' : u'\u004b\u006f\u006d\u0065\u0064\u0069',
					'Crime' : u'\u004b\u0072\u0069\u006d\u0069\u006e\u0061\u006c',
					'Documentary' : u'\u0044\u006f\u006b\u0075\u006d\u0065\u006e\u0074\u00e4\u0072',
					'Drama' : u'\u0044\u0072\u0061\u006d\u0061',
					'Family' : u'\u0046\u0061\u006d\u0069\u006c\u006a',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0079',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0048\u0069\u0073\u0074\u006f\u0072\u0069\u0073\u006b',
					'Horror' : u'\u0053\u006b\u0072\u00e4\u0063\u006b',
					'Music ' : u'\u004d\u0075\u0073\u0069\u0063',
					'Musical' : u'Musical',
					'Mystery' : u'\u004d\u0079\u0073\u0074\u0069\u006b',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0074\u0069\u006b',
					'Science Fiction' : u'\u0053\u0063\u0069\u0065\u006e\u0063\u0065 \u0046\u0069\u0063\u0074\u0069\u006f\u006e',
					'Sci-Fi' : u'\u0053\u0063\u0069\u0065\u006e\u0063\u0065 \u0046\u0069\u0063\u0074\u0069\u006f\u006e',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0054\u0068\u0072\u0069\u006c\u006c\u0065\u0072',
					'War' : u'\u004b\u0072\u0069\u0067',
					'Western' : u'\u0056\u00e4\u0073\u0074\u0065\u0072\u006e',
				},
				'tr' : {
					'Action' : u'\u0041\u006b\u0073\u0069\u0079\u006f\u006e',
					'Adventure' : u'\u004d\u0061\u0063\u0065\u0072\u0061',
					'Animation' : u'\u0041\u006e\u0069\u006d\u0061\u0073\u0079\u006f\u006e',
					'Biography' : u'Biography',
					'Comedy' : u'\u004b\u006f\u006d\u0065\u0064\u0069',
					'Crime' : u'\u0053\u0075\u00e7',
					'Documentary' : u'\u0042\u0065\u006c\u0067\u0065\u0073\u0065\u006c',
					'Drama' : u'\u0044\u0072\u0061\u006d',
					'Family' : u'\u0041\u0069\u006c\u0065',
					'Fantasy' : u'\u0046\u0061\u006e\u0074\u0061\u0073\u0074\u0069\u006b',
					'Game-Show' : u'Game-Show',
					'History' : u'\u0054\u0061\u0072\u0069\u0068',
					'Horror' : u'\u004b\u006f\u0072\u006b\u0075',
					'Music ' : u'\u004d\u00fc\u007a\u0069\u006b',
					'Musical' : u'Musical',
					'Mystery' : u'\u0047\u0069\u007a\u0065\u006d',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u0052\u006f\u006d\u0061\u006e\u0074\u0069\u006b',
					'Science Fiction' : u'\u0042\u0069\u006c\u0069\u006d\u002d\u004b\u0075\u0072\u0067\u0075',
					'Sci-Fi' : u'\u0042\u0069\u006c\u0069\u006d\u002d\u004b\u0075\u0072\u0067\u0075',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u0047\u0065\u0072\u0069\u006c\u0069\u006d',
					'War' : u'\u0053\u0061\u0076\u0061\u015f',
					'Western' : u'\u0056\u0061\u0068\u015f\u0069 \u0042\u0061\u0074\u0131',
				},
				'zh' : {
					'Action' : u'\u52a8\u4f5c',
					'Adventure' : u'\u5192\u9669',
					'Animation' : u'\u52a8\u753b',
					'Biography' : u'Biography',
					'Comedy' : u'\u559c\u5267',
					'Crime' : u'\u72af\u7f6a',
					'Documentary' : u'\u7eaa\u5f55',
					'Drama' : u'\u5267\u60c5',
					'Family' : u'\u5bb6\u5ead',
					'Fantasy' : u'\u5947\u5e7b',
					'Game-Show' : u'Game-Show',
					'History' : u'\u5386\u53f2',
					'Horror' : u'\u6050\u6016',
					'Music ' : u'\u97f3\u4e50',
					'Musical' : u'Musical',
					'Mystery' : u'\u60ac\u7591',
					'News' : u'News',
					'Reality-TV' : u'Reality-TV',
					'Romance' : u'\u7231\u60c5',
					'Science Fiction' : u'\u79d1\u5e7b',
					'Sci-Fi' : u'\u79d1\u5e7b',
					'Sport' : u'Sport',
					'Talk-Show' : u'Talk-Show',
					'Thriller' : u'\u60ca\u609a',
					'War' : u'\u6218\u4e89',
					'Western' : u'\u897f\u90e8',
				},
			}

		if language in Genre.Genres:
			for key, value in Genre.Genres[language].items():
				genre = genre.replace(key, value)

		return genre

class Title(object):

	@classmethod
	def clean(self, title):
		if not title: return None
		import re
		title = re.sub('&#(\d+);', '', title)
		title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
		title = title.replace('&quot;', '\"').replace('&amp;', '&')
		title = re.sub('\n|(\[.+?\])|(\(.+?\))|\s(vs|v\.)\s|[\.,_\-\?\!:;"\']', '', title).lower()
		return title
