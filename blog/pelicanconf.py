AUTHOR = 'Leo'
SITENAME = "Leo's blog"
SITESUBTITLE = 'A nook to hoard my manuscripts.'
SITEURL = 'https://tseing.github.io'
# Developing url
# SITEURL = 'http://localhost:8000'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh-CN'

DEFAULT_DATE_FORMAT = '%Y年 %b%d日'

ARTICLE_URL = '{category}/{date:%Y}-{date:%m}-{date:%d}-{slug}.html'
ARTICLE_SAVE_AS = '{category}/{date:%Y}-{date:%m}-{date:%d}-{slug}.html'

USE_FOLDER_AS_CATEGORY = True
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Select hljs theme
COLOR_SCHEME_CSS = 'atom-one-light.min.css'

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# 导出时不删除的文件
OUTPUT_RETENTION = [".git", "favicon.ico", "googleee5bb3f0889ddb20.html", "BingSiteAuth.xml"]

# md与jupyter两种布局
MARKUP = ("md", "ipynb")

PLUGIN_PATHS = ['plugins']
from pelican_jupyter import markup as nb_markup
PLUGINS = [nb_markup, 'pelican-toc', 'render_math', 'sitemap', 'replacer']
IGNORE_FILES = [".ipynb_checkpoints"]
IPYNB_SKIP_CSS=True

THEME = "themes/attila"

# default articles cover
HEADER_COVER = "https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuU3h7utB_z6MEPLq/root/content"

# default theme cover
# HOME_COVER = "https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuU50-T6H01shIvBa/root/content"
HOME_COVER = "https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNunLc0Y-tTns1SGA5/root/content"

# 侧边菜单栏，手动列举更好排序
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = [("碎碎念", SITEURL + "/category/sui-sui-nian.html"),
             ("故纸堆", SITEURL + "/category/gu-zhi-dui.html"),
             ("在路上", SITEURL + "/category/zai-lu-shang.html"),
             ("山墙边", SITEURL + "/pages/shan-qiang-bian.html"),
             ("Tags", SITEURL + "/tags.html"),
             ("About", SITEURL + "/pages/about.html")]

# Author info
AUTHORS_BIO = {
  "leo": {
    "name": "Leo",
    "cover": "https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuUZNJKuT3c_gI4Jh/root/content",
    "image": SITEURL + "/images/avatar.jpeg",
    "website": SITEURL,
    "github": "Tseing",
    "location": "Tientsin",
    "email": "im.yczeng@outlook.com",
    "bio": "A biochemist who doesn't know about artificial intelligence isn't a good programmer. Cool, huh?"
  }
}

# sitemap
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.5,
        "indexes": 0.5,
        "pages": 0.5
    },
    "changefreqs": {
        "articles": "daily",
        "indexes": "daily",
        "pages": "monthly"
    },
    "exclude": ["tag/", "category/"]
}

# toc
TOC = {
    'TOC_HEADERS'       : '^h[2-3]', # What headers should be included in
                                     # the generated toc
                                     # Expected format is a regular expression

    'TOC_RUN'           : 'true',    # Default value for toc generation,
                                     # if it does not evaluate
                                     # to 'true' no toc will be generated

    'TOC_INCLUDE_TITLE':  'false',     # If 'true' include title in toc
}

# code replace to
REPLACES = (
    (u'{warn begin}', u'<div class="warn-info"><p><i class="fa fa-exclamation-circle"></i>&ensp;<b>Warning</b>&emsp;'),
    (u'{warn end}', u'</p></div>'),
    (u'{note begin}', u'<div class="note-info"><p><i class="fa fa-sticky-note"></i>&ensp;<b>Note</b>&emsp;'),
    (u'{note end}', u'</p></div>'),
    (u'{location}', u"<span class='fa-stack fa-1x'><i class='fa fa-map-o fa-stack-1x'></i><i class='fa fa-map-marker fa-stack-1x'></i></span>"),
    (u'{photo}', u"<i class='fa fa-camera fa-lg'></i>&emsp;")
)

# import lightgallery

# markdown extensions
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight',
                                           'use_pygments': False,
                                           'lang_prefix': '',},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'lightgallery': {},
    },
    'output_format': 'html5',
}

CSS_OVERRIDE = ['theme/css/plugins.css']