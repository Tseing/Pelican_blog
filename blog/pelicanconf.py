AUTHOR = 'Leo'
SITENAME = "Leo's blog"
# SITEURL = 'https://tseing.github.io'
#Test url
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
OUTPUT_RETENTION = [".git", "favicon.ico"]

# md与jupyter两种布局
MARKUP = ("md", "ipynb")

from pelican_jupyter import markup as nb_markup
PLUGINS = [nb_markup, 'render_math']
IGNORE_FILES = [".ipynb_checkpoints"]
IPYNB_SKIP_CSS=True

THEME = "themes/attila"
# HOME_COVER = r"./themes/attila/static/images/wp2717211-nasa-hd-wallpaper.jpg"
HOME_COLOR = 'black'

# 侧边菜单栏，手动列举更好排序
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = [("碎碎念", SITEURL + "/category/sui-sui-nian.html"),
             ("故纸堆", SITEURL + "/category/gu-zhi-dui.html"),
             ("在路上", SITEURL + "/category/zai-lu-shang.html"),
             ("山墙边", SITEURL + "/pages/shan-qiang-bian.html"),
             ("Tags", SITEURL + "/tags.html"),
             ("About me", SITEURL + "/pages/about.html")]

