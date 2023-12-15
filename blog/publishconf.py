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
             ("破橱簏", "https://boulder-eoraptor-e45.notion.site/093af471f4f749628fd4ddc244a6b08d?v=3ec2eda75795443bb9530c901685a54b&pvs=4"),
             ("Tags", SITEURL + "/tags.html"),
             ("About", SITEURL + "/pages/about.html")]

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

UMAMI_STATISTIC = True
# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""