title: 为 Pelican 博客设置 Lightbox 效果
slug:  pelican-lightbox
date: 2022-08-17
tags: Blog, Pelican, Markdown, JavaScript
summary: 如何像社交媒体上发布的图片一样，让博客文章中的图片也能点击放大呢？使用 JavaScript 插件，在博客文章中添加这种 Lightbox 效果，再加上配套的 Python-Markdown 的拓展插件，让 Markdown 写作中的图片效果设置变得更加自由。

Markdown 语法简洁而高效，使用 Markdown 撰写博客文章是十分通行的做法。若要在文章中插入图片，需要使用 `![标题](URL)` 语法，Pelican 博客引擎将文章中的 `[标题](URL)` 转换为 html 标签 `<img alt="标题" src="URL">`，就生成了用于发布的静态网页。

这样生成的网页中，图片大小由 CSS 文件决定。设定的图片尺寸如果太小，难以看清图片细节，尺寸如果太大就会占据较大版面，也十分影响阅读。

各类社交网站上的常规做法是，使用 CSS 文件决定合适的缩略图尺寸，点击缩略图后放大图片。点击缩略图放大的效果就像在暗室中使用的放映机，这个效果就被称为 Lightbox。

Lightbox 功能非常常用，因在网上有大量现成的插件，具有 Lightbox 功能的 Pelican 插件包括 [photos](https://github.com/pelican-plugins/photos) 和 [Gallery](https://github.com/getpelican/pelican-plugins/tree/master/gallery) 等。但是它们并不是纯粹的 Lightbox 插件，还具有图片处理、读取 EXIF 信息等功能，我觉得太「重」。

## 轻量的 lightgallery-markdown

兜兜转转之下，我找到了一个实现 Lightbox 功能的 [Python-Markdown 拓展](https://github.com/g-provost/lightgallery-markdown)。其实原理也很简单，这个拓展能将 `![!标题](URL)` 转换为以下代码：

```html
<div class="lightgallery">
    <a href="URL" data-sub-html="标题">
      <img alt="标题" src="URL" />
    </a>
</div>
```

再在 [lightgallery.js](https://github.com/sachinchoolur/lightgallery.js) 的作用下就能实现 Lightbox 功能。所以只要是使用 Python-Markdown 作为 html 生成器的博客都可以使个方法设置 Lightbox 效果。

## 安装 Python-Markdown 拓展

Pelican 提供了 Python-Markdown 拓展的接口，先使用 `pip install lightgallery` 安装 lightgallery-markdown，并在 `pelicanconf.py` 中添加

``` python
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'lightgallery': {},
    },
    'output_format': 'html5',
}
```

## 部署 lightgallery.js

在 [lightgallery.js 项目仓库](https://github.com/sachinchoolur/lightgallery.js)中下载以下文件并放置到相应位置：

- `dist/js/lightgallery.min.js`&emsp;→&emsp;`themes/{theme_name}/static/js/`
- `dist/css/lightgallery.min.css`&emsp;→&emsp;`themes/{theme_name}/css/`
- `dist/fonts/lg.*`&emsp;→&emsp;`themes/{theme_name}/font/`
- `dist/img/loading.gif`&emsp;→&emsp;`themes/{theme_name}/images/`

{warn begin}由于文件目录结构不同，需要将 `lightgallery.min.css` 中的字体、图片路径修改为相应路径。{warn end}

修改 `themes/{theme_name}/templates/base.html`，在其中添加以下代码

```html
<!-- 引入.css与.js文件-->
<link href="{{ SITEURL }}/{{ THEME_STATIC_DIR }}/css/lightgallery.min.css" type="text/css" rel="stylesheet" />
<script type="text/javascript" src="{{ SITEURL }}/{{ THEME_STATIC_DIR }}/js/lightgallery.min.js"></script>
<!-- 图片计数 -->
<script>
  var elements = document.getElementsByClassName("lightgallery");
  for(var i=0; i<elements.length; i++) {
     lightGallery(elements[i]);
  }
</script>
```

到了这里，已经在博客上添加了 Lightbox 功能，但还缺少最重要的放大缩小功能。

## 添加 lightgallery.js 插件

下载 [lg-zoom.js](https://github.com/sachinchoolur/lg-zoom.js)，将 `dist/lg_zoom.min.js` 移入 `themes/{theme_name}/static/js/`。同样在主题的 `base.html` 中引入该 JavaScript 文件即可生效。lightgallery.js 项目还具有许多插件，都可以通过这样简单的方法使其生效。

## 一些小修改

若将图片标题留空，如 `![!](URL)`，lightgallery.js 不会渲染查看图片时下方的图片信息，界面十分清爽舒服。但是这么一来，每次导出网页时Pelican 都会给出 `WARNING: Empty alt attribute for image content`。

于是修改 `lightgallery.js` 文件，修改以下代码块：

```javascript
if (typeof subHtml !== 'undefined' && subHtml !== null) {
            if (subHtml === '') {
                _lgUtils2.default.addClass(this.outer.querySelector(this.s.appendSubHtmlTo), 'lg-empty-html');
            } else {
                _lgUtils2.default.removeClass(this.outer.querySelector(this.s.appendSubHtmlTo), 'lg-empty-html');
            }
        }
```

将判断条件修改为：

```javascript
if (subHtml === '' || subHtml === 'NoCaption')
```

这时只要是标题设置为 `"NoCaption"` 的图片就不会显示下方信息栏，Pelican 也不会因为缺少标题而给出警告。

{note begin}`lightgallery.min.js` 经过压缩，体积较小，加载速度更快，但代码可读性较差，不便于修改，可以先修改 `lightgallery.js` 再压缩为 `lightgallery.min.js`。{note end}

## Demo 🥳

![!{photo}135 mm&emsp;f/5.6&emsp;1/125&emsp;ISO-800&emsp;Photo by Leo](https://storage.live.com/items/4D18B16B8E0B1EDB!7545?authkey=ALYpzW-ZQ_VBXTU)

{warn begin}本文最后更新于 2022 年 08 月 17 日，请确定内容是否过时。{warn end}
