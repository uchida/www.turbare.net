#!/usr/bin/env python
# -*- coding: utf-8 -*- #

SITENAME = u'turbare.net'
SITEURL = 'http://127.0.0.1:8000'

AUTHOR = u'Akihiro Uchida'
AUTHOR_URL = 'index.html'
AUTHOR_SAVE_AS = ''

INDEX_URL = 'weblog/index.html'
INDEX_SAVE_AS = 'weblog/index.html'
ARTICLE_URL = 'weblog/{slug}.html'
ARTICLE_SAVE_AS = 'weblog/{slug}.html'
ARTICLE_LANG_URL = 'weblog/{slug}-{lang}.html'
ARTICLE_LANG_SAVE_AS = 'weblog/{slug}-{lang}.html'
TAG_URL = 'weblog/tag/{slug}.html'
CATEGORY_URL = 'weblog/cat/{slug}.html'
CATEGORY_SAVE_AS = 'weblog/cat/{slug}.html'
TAG_URL = 'weblog/tag/{slug}.html'
TAG_SAVE_AS = 'weblog/tag/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

# locale and date
DEFAULT_LANG = 'ja'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
TIMEZONE = 'Asia/Tokyo'

PAGES_ON_MENU = []
DISPLAY_PAGES_ON_MENU = True

# Blogroll
#LINKS =  (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
#          ('Python.org', 'http://python.org'),
#          ('Jinja2', 'http://jinja.pocoo.org'),
#          ('You can modify those links in your config file', '#'),)
#
## Social widget
SOCIAL = (('github', 'https://github.com/uchida'),
          ('twitter', 'https://twitter.com/auchida'),)

DEFAULT_PAGINATION = 3

STATIC_PATHS = [
    'extra/robots.txt',
    'extra/favicon.ico',
    'extra/public_key.asc',
]

EXTRA_PATH_METADATA = { 
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/public_key.asc': {'path': 'public_key.asc'},
}

IGNORE_FILES = ['.#*']

# theme
THEME = 'theme'
USE_MATHJAX = True

# import plugins
PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = [
	'assets',
	'myplugins.jp_textjoin',
	'myplugins.global_license_on_page',
	'myplugins.rst2html5',
]

ASSET_CONFIG = (('COMPASS_CONFIG', {'environment': ':production', 'line_comments': False}),)

# setting for global_license
LICENSE = '<a href="http://creativecommons.org/licenses/by/4.0/" rel="license">CC-BY 4.0</a>'
