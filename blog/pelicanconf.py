AUTHOR = 'Leo'
SITENAME = "Leo's blog"
SITESUBTITLE = 'A nook to hoard my manuscripts.'
# SITEURL = 'https://tseing.github.io'
#Developing url
SITEURL = 'http://localhost:8000'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh-CN'

DEFAULT_DATE_FORMAT = '%Y年 %b%d日'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

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
PLUGINS = [nb_markup, 'pelican_toc', 'render_math', 'sitemap']
IGNORE_FILES = [".ipynb_checkpoints"]
IPYNB_SKIP_CSS=True

THEME = "themes/attila"

# default articles cover
HEADER_COVER = "https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuU3h7utB_z6MEPLq/root/content"

# default theme cover
HOME_COVER = "https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuU50-T6H01shIvBa/root/content"

# 侧边菜单栏，手动列举更好排序
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = [("碎碎念", SITEURL + "/category/sui-sui-nian.html"),
             ("故纸堆", SITEURL + "/category/gu-zhi-dui.html"),
             ("在路上", SITEURL + "/category/zai-lu-shang.html"),
             ("山墙边", SITEURL + "/pages/shan-qiang-bian.html"),
             ("Tags", SITEURL + "/tags.html"),
             ("About me", SITEURL + "/pages/about.html")]

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
    "bio": "This is the place for a small biography with max 200 characters. Well, now 100 are left. Cool, hugh?"
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