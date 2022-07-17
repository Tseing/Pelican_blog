AUTHOR = 'Leo'
SITENAME = "Leo's blog"
SITEURL = 'https://tseing.github.io'
#Developing url
# SITEURL = 'http://localhost:8000'

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
OUTPUT_RETENTION = [".git", "favicon.ico", ".xml"]

# md与jupyter两种布局
MARKUP = ("md", "ipynb")

from pelican_jupyter import markup as nb_markup
PLUGINS = [nb_markup, 'render_math', 'sitemap']
IGNORE_FILES = [".ipynb_checkpoints"]
IPYNB_SKIP_CSS=True

THEME = "themes/attila"

# default cover
HEADER_COVER = "https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuUy2Lur0PVrUfO1O/root/content"

HOME_COVER = "https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuUt5yF-Mt9dOuNEh/root/content"

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
    }
}