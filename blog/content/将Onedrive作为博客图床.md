Title: 将 OneDrive 作为博客图床
Slug: blog02
Date: 2022-07-14
Category: 碎碎念
Tags: blog, OneDrive
Author: Leo
Summary: 在 Linux 使用 ZFile 同步管理 OneDrive 文件，通过 Microsoft API 生成图片链接
Cover: https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuUZNJKuT3c_gI4Jh/root/content

在个人博客中，图片是不可或缺的，而生成图片的直链后才能在`.md`文件中使用，因此通常又需要图床等额外工具。由于国内市场的图床工具良莠不齐，没有精力仔细挑选，还有就是把数据交在他们的手中多少有些不放心。想到订阅 Microsoft Office 时附赠了 1 TB 的 OneDrive 容量，正好可以利用起来。使用 OneDrive 作为图床的好处就在于数据在自己的手中，不用担心某天突然挂掉，还有就是在多平台（Windows、iPad 和 Android）都有 OneDrive 应用，很方便同步。但是很遗憾，由于国内的环境，OneDrive 的网页版是打不开的，这就不能通过网页版直接生成图片链接，必须『绕道通行』。

Windows 系统自带 OneDrive 应用，可以直接使用桌面应用进行文件同步，借助 [Img Share](https://github.com/Richasy/Img-Share) 生成图片链接。Img Share 后来被 [Picture Share](https://apps.microsoft.com/store/detail/picture-share/9PHWZ3QL0HN3?hl=en-us&gl=US) 代替，在 Microsoft Store 中就可以直接下载到。Picture Share 十分容易上手，界面简洁且功能齐全，具体的设置方法可以参考[这篇文章](https://wzblog.fun/posts/b036879a/)。

但是写博客的工作环境是 Linux 系统，Linux 系统中没有 OneDrive 应用和上述 UWP 应用，也就不能使用上面的方法。本文就将介绍如何在 Linux 系统下使用 OneDrive 作为个人博客的图床并使用ZFile同步云盘文件。

### OneDrive 文件链接的生成方式

OneDrive 的网页应用直接提供了嵌入代码，可以直接贴在文章中。但因为科学上网时上传速度相当感人，使用起来还是太过麻烦。虽然无法访问 OneDrive 网页，但 OneDrive 在国内的其他功能都是正常的，包括生成的分享链接，所以直接借用官方API生成链接的方案是可行的。发现有人已经写好了[相关项目](https://github.com/harrisoff/onedrive-image-hosting)，点开项目右侧的链接登录自己的OneDrive后直接插入`.md`就可以啦。
```
![图片名称](https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuUZNJKuT3c_gI4Jh/root/content)
```

### 安装 ZFile
[ZFile](https://github.com/zhaojun1998/zfile) 是一款在线网盘程序，支持包括 OneDrive 在内的多种存储源。ZFile 可以代替其他平台的 OneDrive 应用来管理云盘中的文件，实现同步、上传、下载等功能。ZFile 也能生成文件直链插入文章，但是这个功能需要云服务器，抱着能省则省的态度，就等以后再折腾，这里仅使用 ZFile 来管理 OneDrive。

在 Linux 系统使用 ZFile 首先需要安装依赖：

```bash
# Debian 10
apt update && apt install -y apt-transport-https software-properties-common ca-certificates dirmngr gnupg
wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add -
add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/
apt update && apt install -y adoptopenjdk-8-hotspot-jre
```

下载 ZFile:

```
export ZFILE_INSTALL_PATH=~/zfile
mkdir -p $ZFILE_INSTALL_PATH && cd $ZFILE_INSTALL_PATH
wget https://c.jun6.net/ZFILE/zfile-release.war
unzip zfile-release.war && rm -rf zfile-release.war
chmod +x $ZFILE_INSTALL_PATH/bin/*.sh
```

`ZFILE_INSTALL_PATH`指定了安装路径，可以自行修改。

### 启动并配置 ZFile

```
 ~/zfile/bin/start.sh       # 启动项目
 ~/zfile/bin/stop.sh        # 停止项目
 ~/zfile/bin/restart.sh     # 重启项目
```

启动项目后，默认开放在 8080 端口，使用`localhost:8080`进入 ZFile：
![注册/登录界面](https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuUeZko02sAbyr5jh/root/content)首次开启时需要注册管理员账号，登录进入系统后，首先配置存储源，选择存储策略为`OneDrive`，启用文件操作。
![配置存储源](https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuUUBsSGYxpEV6Frp/root/content)点击链接登录 OneDrive 账号获取令牌，填写完成后即可保存设置。![获取令牌](https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuUPS4i5g5F_-nR4T/root/content)设置成功后在存储源中就可以看见 OneDrive 标志，并且显示刷新成功，这样 ZFile 就已经正常工作了。![存储源列表](https://api.onedrive.com/v1.0/shares/s!AtseC45rsRhNuUSMlwPi40T-1Um4/root/content)

### 使用 ZFile 管理 OneDrive

在地址栏中输入`localhost:8080`进入存储界面，在这里就理应能够看到 OneDrive 中存储的文件了，可以使用其他设备辅助测试是否能够正常上传或删除文件。

如果有一台 VPS，在 VPS 上启动 ZFile 后，通过`vps-ip:[port]`也能进入同样的管理界面。只需要将图片文件上传至 OneDrive，使用ZFile就可以得到文件的直链，不止是图片，这种方法还可以在`.md`中插入音频或是视频文件，甚至搭建个人下载站，而且完全不占用服务器存储。值得注意的是，ZFile获得的文件『直链』并不是真正的直链，而是经过一次转发，可能会影响访问速度。![ZFile获取直链流程](https://storage.live.com/items/4D18B16B8E0B1EDB!7369?authkey=ALYpzW-ZQ_VBXTU)因为 ZFile 向 OneDrive 请求得到是预览链接或临时下载链接`1drv.com/...`，该链接在一段时间后就会失效，也不能直接用作图床。当用户每次访问ZFile直链`vps-ip:[port]/...`时，实际得到的都是Z File 转发得到的 OneDrive 临时链接。