title: 使用 Pelican 发布文章的流程
slug: blog01
date: 2022-07-12
tags: blog, Pelican
summary: 如何使用 Pelican 在搭建在 Github Pages 上的博客发布文章

## Articles or Pages?

Pelican 中有 articles 与 pages 的概念，在创建页面时应当首先区分二者。

- **articles** 指具有时间戳的内容，例如博客文章等，直接创建在`content`文件夹中。
- **pages** 指与时间无关、展示固定内容的页面，需要创建在`content/pages`文件夹下

## 撰写文章

### Jupyter Notebook 方式

Jupyter Notebook 能够保存下代码的输入与输出信息，特别适合用于展示程序输出的图形。首先在`content`目录中创建`.nbdata`与`.ipynb`的同名文件。`.nbdata`文件中保存了文章的结构信息，而`.ipynb`使用 Jupyter Notebook 保存了文章的具体内容。

```
title: # 文章标题
slug: # 文章地址
date: # 时间
category: # 类别
tags: # 标签
author: # 作者
summary: # 概要

# 其他不常用信息
modified: # 修改时间
keywords: # 仅用于html内容
authors: # 多作者
lang: # 语言
translation: # 是否属于译文
status: # draft, hidden, or published
```

### Markdown 方式

使用 Markdown 语言是写博客最为简单普遍的方式，在`content`文件夹中创建`.md`文件，在开始部分首先输入与`.nbdata`相同的文章信息后，就可以直接开始撰写正文。

## 生成静态网页

在撰写文章后，进入虚拟环境，在`blog`文件夹中使用`Pelican`生成`.html`文件。

```sh
source ./venv/bin/activate
pelican content -s publishconf.py
```

最后将`output`文件夹同步至 Github 中`<username>.github.io`仓库即完成文章的发布。

## 发布

使用终端在`output`文件夹中输入`python -m pelican.server`可以开启本地服务器，默认端口为 8000，通过`localhost:8000`访问。

测试完成后将内容推送至 Github:

```sh
git add .
git commit
git push
```

## 克隆与同步

由于我有 Windows 与 Linux 两个平台的设备，所以需要在两个平台上同步博客的内容，方便我在任意设备上都可以写文章。

在终端中使用`git clone --recursive`命令克隆仓库，`git clone`命令只会克隆主仓库，导致子模块失效，`--recursive`能递归地克隆包括子模块在内的整个仓库。使用`git pull --recurse-submodules`命令能够拉取包含子模块在内的全部更新，即可完成同步。

---

## References

- [Pelican Settings Document](https://docs.getpelican.com/en/latest/settings.html)
- [Pelican + GitHubPages 搭建个人博客 · Zodiac Wang](https://zodiac911.github.io/blog/static-blog.html#%E7%B3%BB%E7%BB%9F%E8%A6%81%E6%B1%82)