AUTHOR = 'Leo'
SITENAME = "Leo's blog"
SITESUBTITLE = 'A nook to hoard my manuscripts.'
SITEURL = 'http://localhost:8000'

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

# Umami statistic
# turn off umami when developing
UMAMI_STATISTIC = False
UMAMI_WEB_ID = "b508982a-f7bf-4c24-a948-8de93b0cb81d"

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10
SUMMARY_MAX_LENGTH = 100

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# 导出时不删除的文件
OUTPUT_RETENTION = [".git", ".gitignore", "favicon.ico", "robots.txt", "map.html", "archives", "search.html"]

# md与jupyter两种布局
MARKUP = ("md", "ipynb")
IPYNB_MARKUP_USE_FIRST_CELL = True

PLUGIN_PATHS = ['plugins']
from pelican_jupyter import markup as nb_markup
PLUGINS = [nb_markup, 'pelican-toc', 'render_math', 'sitemap', 'replacer',
           'neighbors', 'pelican-bookshelf', 'search']
IGNORE_FILES = [".ipynb_checkpoints"]
IPYNB_SKIP_CSS=True

THEME = "themes/attila"
DIRECT_TEMPLATES  = ['index', 'authors', 'categories', 'tags', 'archives', 'search']

# article modified time
SHOW_MODIFIED_TIME = False
# default articles cover
HEADER_COVER = "https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNwFfSnZ1Pc1osKbni/root/content"
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
             ("破橱簏", "https://boulder-eoraptor-e45.notion.site/093af471f4f749628fd4ddc244a6b08d?v=3ec2eda75795443bb9530c901685a54b&pvs=4"),
             ("Tags", SITEURL + "/tags.html"),
             ("About", SITEURL + "/pages/about.html")]

# Author info
AUTHORS_BIO = {
  "leo": {
    "name": "Leo",
    "cover": "https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuUZNJKuT3c_gI4Jh/root/content",
    "image": "https://cravatar.cn/avatar/95e31f6808fafa1f8ef3313b6f0b10e6?s=800",
    "website": SITEURL,
    "github": "Tseing",
    "location": "Tientsin",
    "email": "im.yczeng@outlook.com",
    "bio": "A biochemist who doesn't know about classical literature isn't a good programmer. Cool, huh?"
  }
}

# MathJax(3.2.0)
MATH_JAX = {"source": "'https://lf26-cdn-tos.bytecdntp.com/cdn/expire-1-M/mathjax/3.2.0/es5/tex-mml-chtml.js'"}

# sitemap
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.5,
        "indexes": 0.8,
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

    'TOC_INCLUDE_TITLE':  'false',   # If 'true' include title in toc
}

# pelican-search
STORK_INPUT_OPTIONS = {
    "html_selector": ".post-content",
    "exclude_html_selector": "script, pre, .toc-nav, .math",
    "minimum_index_ideographic_substring_length": 2,
}

STORK_OUTPUT_OPTIONS = {
    "excerpts_per_result": 1
}

# code replace to
REPLACES = (
    (u'{warn begin}', u'<div class="warn-info"><p><i class="fa fa-exclamation-circle"></i>&ensp;<b>Warning</b>&emsp;'),
    (u'{warn end}', u'</p></div>'),
    (u'{note begin}', u'<div class="note-info"><p><i class="fa fa-sticky-note"></i>&ensp;<b>Note</b>&emsp;'),
    (u'{note end}', u'</p></div>'),
    (u'{location}', u"<span class='fa-stack fa-1x'><i class='fa fa-map-o fa-stack-1x'></i><i class='fa fa-map-marker fa-stack-1x'></i></span>"),
)

# import lightgallery
# markdown extensions
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight',
                                           'use_pygments': False,
                                           'lang_prefix': '',},
        'markdown.extensions.extra': {},
        'markdown.extensions.tables': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.md_in_html': {},
        'lightgallery': {},
        'markdown_link_attr_modifier': {
            'new_tab': 'on',
            'no_referrer': 'off',
            'auto_title': 'off',
        },
    },
    'output_format': 'html5',
}

CSS_OVERRIDE = ['theme/css/plugins.css', 'theme/css/bookshelf.css']

# bookshelf plugin
BOOKSHELF = {"INFOS": ["出版年", "页数", "定价", "ISBN"],
             "SAVE_TO_MD": False,
             "WAIT_TIME": 2}