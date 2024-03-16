# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://leonis.cc'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feed.xml'
FEED_MAX_ITEMS = 20
# CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Update SITEURL for publishing
MENUITEMS = [("碎碎念", SITEURL + "/category/sui-sui-nian.html"),
             ("故纸堆", SITEURL + "/category/gu-zhi-dui.html"),
             ("在路上", SITEURL + "/category/zai-lu-shang.html"),
             ("山墙边", SITEURL + "/pages/shan-qiang-bian.html"),
             ("破橱簏", "https://neodb.social/users/Leo/"),
             ("Tags", SITEURL + "/tags.html"),
             ("About", SITEURL + "/pages/about.html")]

UMAMI_STATISTIC = True
# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""