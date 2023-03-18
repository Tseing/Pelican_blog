title: Pelican + Nginx 在服务器上搭载静态博客
slug: deploy-pelican-by-nginx
date: 2023-02-13
tags: Blog, Pelican, Nginx, Linux
summary: 去年购置了一个服务器，由于后来太忙，一直没有时间折腾，终于有一段空闲的时间了，就尝试把我的 Pelican Blog 从 GitHub Pages 搬迁到服务器上，再通过 Nginx 部署我的站点。

去年黑色星期五低价购置了一个海外服务器，由于后来太忙，一直没有时间折腾，终于有一段空闲的时间了。想到的我博客一直部署在 GitHub Pages 上，访问速度慢不说，还会由于各种的原因时常无法连接，所以动手把它搬到自己的服务器上吧。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8514?authkey=ALYpzW-ZQ_VBXTU)

上图是我的部署方案，首先使用 Pelican（或其他静态博客生成器）在本地生成静态网页，再将静态网页 push 到 GitHub 仓库，这两步也是在 GitHub Pages 上部署、更新博客的步骤，所以对我而言没有额外的负担。

接着在服务器上 pull 静态网页，然后使用 Nginx 作为 HTTP 服务器就可以通过域名或是公网 IP 访问到网站了。虽然 Pelican 也自带有 HTTP 服务器，可以不使用 Nginx，但我觉得它的性能和通用性方面不够好，而且我主要在 PC 上写文章，在服务器上安装 Pelican 并在服务器上生成静态网页未免太繁琐。

最后为了便于管理服务器上的文件和排查问题，可以使用 SFTP 直接上传和下载服务器文件。

{warn begin}在境内服务器上部署网站必须经过 TCP 备案，否则会被拦截或是限流，引起非常多的麻烦。{warn end}

## 配置 Nginx

在 Debian 系统上可以使用以下命令安装 Nginx：

```bash
# Debian
$ sudo apt install nginx
```

安装完成后可 `nginx -v` 检查 Nginx 的版本。使用 `http://服务器 IP` 访问 Web 服务器，不出意外的话，会出现如下页面，提示已经成功安装了 Nginx：

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8515?authkey=ALYpzW-ZQ_VBXTU)

如果没有出现 Nginx 的欢迎页面，就需要检查服务器防火墙的设置，由于各个系统的防火墙设置不同，这里就不给出设置的方法了。

然后需要在 `/etc/nginx/sites-available` 中建立我们站点的 Nginx 配置:

```bash
$ cd /etc/nginx/sites-available
$ sudo touch blog
```

在 Nginx 设计中，在 `sites-available` 目录下存放站点的配置文件，并将其链接到 `sites-enabled` 目录下。`sites-enabled` 目录下存放了启用站点的配置，若要关闭该站点的配置，删除该链接即可。

通过以下命令进入 `sites-enabled` 并建立软链接：

```bash
$ cd /etc/nginx/sites-enabled
$ ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/blog
```

接着再回到 `sites-available` 中，使用 `vim blog` 编辑配置，粘贴以下内容：

```nginx
server {
    listen       80;
    server_name  _;
    root         /home/Leo/web/blog;

    location / {
    };
}
```

其中 `listen 80` 指监听 80 端口，也就是 HTTP 服务的端口，`server_name` 是网站的 url 地址，如果需要通过域名访问，例如填入 `example.com` 即可，`root` 是静态站点的文件目录，在该目录下存放了站点的 HTML 和 CSS 文件，`location` 设置了网站路由，不需要修改。

最后需要将同一文件夹内 `default` 文件中的所有内容都注释掉。

## 从 GitHub pull 静态网页

在本地电脑上，使用 Pelican（或其他静态网页生成器）生成静态网页，Pelican 的命令是 `pelican content -s publishconf.py`，然后就会生成 `output` 文件夹，只需要将该文件夹 push 到 GitHub 仓库中，这里的操作十分简单，也不展开介绍了。

在服务器中进入 `root` 文件夹，也就是 `/home/Leo/web/blog` 中，

```bash
git init
git remote add origin https://github.com/Tseing/tseing.github.io.git
git pull origin master
```

使用 `sudo git init` 初始化后，从链接的 GitHub 仓库中 pull 静态文件。最后使用 `sudo nginx -s reload` 重启 Nginx 服务，在 `http://服务器 IP` 上就能看到博客页面啦。

可以把在服务器上发布文章的流程总结为以下几步：

1. 在本地使用 Markdown 撰写文章；
2. 使用 Pelican 生成静态网页；
3. 将生成的静态网页 push 至 GitHub 仓库；
4. 连接服务器，在相应目录下 pull GitHub 仓库中的更新。

这样的流程比较繁琐，每次更新都需要连接到服务器上操作，要简化这样的流程并实现自动化部署就需要借助 webhook 的功能。简单来说，在 GitHub 仓库设置中开启 webhook，用户对仓库执行每个动作（这里为 push）后，仓库都会向目标服务器发送一段 JSON 报文（回调），那么服务器只需要一直运行着监听该报文的脚本，一旦收到 push 成功的报文就执行 pull 操作。这样就简化了工作流程，push 静态网页后，服务器上的内容也会自动更新。

webhook 脚本可以使用不同语言实现，例如 PHP、JavaScript 和 Python 等等。但是考虑了服务器的性能，我不打算在服务器上配置过于重的环境。于是我选择了基于 Go 语言的 [<i class="fa fa-github"></i> adnanh/webhook](https://github.com/adnanh/webhook)，十分轻量，配置的方法也很简单，可以参考[这篇文章](https://www.cnblogs.com/pingyeaa/p/12777626.html)。

{warn begin}旧版 webhook 存在一些令人困恼的 bug，例如无法读取相对路径，请使用最新版本。{warn end}

## 关闭 GitHub Pages

在一切部署工作都完成之后，也是时候和 GitHub Pages 说再见了。避免搜索引擎抓取数据时出现大量重复网页，所以就关闭原来 GitHub Pages 上的博客吧。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8516?authkey=ALYpzW-ZQ_VBXTU)

> <p class="cite">Hello world!</p>  
> —— *From my server*

---

## References

- [使用 Nginx 搭建静态网站 - 简书](https://www.jianshu.com/p/87e26e644a5a)
- [nginx 配置详解 - 博客园](https://www.cnblogs.com/jenkin1991/p/8301983.html)