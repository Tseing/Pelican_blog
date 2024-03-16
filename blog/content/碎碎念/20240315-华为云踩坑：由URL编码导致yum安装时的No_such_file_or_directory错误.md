title: 华为云踩坑：由 URL 编码导致 yum 安装时的 No such file or directory 错误
slug: yum-install-name-error-caused-by-url-encode
date: 2024-03-15
tags: Linux, BMS, EulerOS, Proxy, Bug

最近想要在华为云的 BMS 上部署一个 Web 应用，咨询了华为的工程师后，得到了可行的明确答复。那么首先就需要安装 Nginx，在安装 Nginx 所需的依赖遇到了 `[Errno 2] No such file or directory` 的错误，一层层查找后发现这可能是一个由代理设置引起 URL 编码错误而导致的 bug。由于网络上几乎没有找到任何相关的资料，就把整个过程留下来作为记录。

首先从安装 Nginx 所需的依赖开始：

```shell
$ sudo yum -y install gcc gcc-c++ make libtool zlib zlib-devel openssl openssl-devel pcre pcre-devel
...
Error:
 Problem: package pcre-devel-8.32-15.1.h6.aarch64 requires libpcre16.so.0()(64bit), but none of the providers can be installed
  - package pcre-devel-8.32-15.1.h6.aarch64 requires libpcre32.so.0()(64bit), but none of the providers can be installed
  - package pcre-devel-8.32-15.1.h6.aarch64 requires libpcrecpp.so.0()(64bit), but none of the providers can be installed
  - cannot install both pcre-8.32-15.1.h1.aarch64 and pcre-8.42-4.h3.eulerosv2r8.aarch64
  - cannot install both pcre-8.32-15.1.h6.aarch64 and pcre-8.42-4.h3.eulerosv2r8.aarch64
  - cannot install the best candidate for the job
```

竟然提示没有找到可用的包，按理来说 BMS 已经配置了华为官方的源，既不会有网络问题也不会缺失 pcre-devel 这样的常见包。于是我开始排查 yum 源的问题，先检查设备的系统和架构：

```shell
$ uname -m
aarch64
$ cat /etc/os-release
NAME="EulerOS"
VERSION="2.0 (SP8)"
ID="euleros"
ID_LIKE="rhel fedora centos"
VERSION_ID="2.0"
PRETTY_NAME="EulerOS 2.0 (SP8)"
ANSI_COLOR="0;31"
```

可以看到操作系统是华为的 EulerOS 2.0 (SP8)，架构是 aarch64。再检查默认的 yum 源：

```shell
$ sudo cat /etc/yum.repos.d/EulerOS.repo
[euler-base]
name=EulerOS-2.0SP8 base
baseurl=http://mirrors.huaweicloud.com/euler/2.3/os/aarch64/
enabled=1
gpgcheck=1
gpgkey=http://mirrors.huaweicloud.com/euler/2.3/os/RPM-GPG-KEY-EulerOS
```

仔细看默认的 yum 源，系统版本明明是 `2.0 (SP8)`，URL 却指向了 `2.3`。测试直接替换后的链接 `http://mirrors.huaweicloud.com/euler/2.8/os/aarch64/` 可达，那么就尝试改为使用该 yum 源。

## 更换 yum 源

这里的修改很简单，我就没有额外备份，使用 vim 直接编辑文件 `/etc/yum.repos.d/EulerOS.repo` 并保存，修改后的 yum 源信息为

```toml
[euler-base]
name=EulerOS-2.0SP8 base
baseurl=http://mirrors.huaweicloud.com/euler/2.8/os/aarch64/
enabled=1
gpgcheck=1
gpgkey=http://mirrors.huaweicloud.com/euler/2.8/os/RPM-GPG-KEY-EulerOS
```

通过以下命令更新 yum 源：

```shell
$ sudo yum clean all            # 清除旧 yum 源缓存
$ sudo yum makecache            # 生成新 yum 源缓存
$ sudo yum repolist             # 检查 yum 源连接状态
EulerOS-2.0SP8 local repo for internal use          0.0  B/s |   0  B     00:00
EulerOS-2.0SP8 base                                 7.4 MB/s |  17 MB     00:02
Failed to synchronize cache for repo 'base', ignoring this repo.
Last metadata expiration check: 0:00:06 ago on Fri 15 Mar 2024 09:54:47 AM CST.
repo id                           repo name                              status
euler-base                        EulerOS-2.0SP8 base                    16,599
```

上述信息中的 Fail 指示 `EulerOS-2.0SP8 local repo for internal use` 这个源不可用，看名字应该是内部使用的 yum 源，在此处没有影响。列举出的 repolist 中有 `EulerOS-2.0SP8 base` 一项，说明更改后的源已经可用。

## [Errno 2] No such file or directory

再次尝试安装 Nginx 的依赖：

```shell
$ sudo yum -y install gcc gcc-c++ make libtool zlib zlib-devel openssl openssl-devel pcre pcre-devel
...
(19/29): gcc-c++-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm         6.2 MB/s | 7.4 MB     00:01
...
[Errno 2] No such file or directory: '/var/cache/dnf/euler-base-85cc05102200a8ac/packages/gcc-c++-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm'
The downloaded packages were saved in cache until the next successful transaction.
You can remove cached packages by executing 'dnf clean packages'.
```

提示 `[Errno 2] No such file or directory`，没有找到 `gcc-c++` 的 RPM 文件，奇怪的是在安装输出的信息中分明提示已经成功下载了 `gcc-c++`。

错误信息中指引了一个文件目录 `/var/cache/dnf/euler-base-85cc05102200a8ac/packages/`，不妨检查一下其中的文件：

```shell
$ sudo ls /var/cache/dnf/euler-base-85cc05102200a8ac/packages/
cpp-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm                  make-4.2.1-10.h3.eulerosv2r8.aarch64.rpm
gcc-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm                  openssl-1.1.1-3.h31.eulerosv2r8.aarch64.rpm
gcc-c%2b%2b-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm          openssl-devel-1.1.1-3.h31.eulerosv2r8.aarch64.rpm
gcc-gfortran-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm         openssl-libs-1.1.1-3.h31.eulerosv2r8.aarch64.rpm
keyutils-libs-devel-1.5.10-8.h4.eulerosv2r8.aarch64.rpm         pcre2-devel-10.32-3.h1.eulerosv2r8.aarch64.rpm
krb5-devel-1.16.1-21.h1.eulerosv2r8.aarch64.rpm                 pcre2-utf16-10.32-3.h1.eulerosv2r8.aarch64.rpm
libcom_err-devel-1.44.3-1.h4.eulerosv2r8.aarch64.rpm            pcre2-utf32-10.32-3.h1.eulerosv2r8.aarch64.rpm
libgfortran-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm          pcre-8.42-4.h3.eulerosv2r8.aarch64.rpm
libgomp-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm              pcre-cpp-8.42-4.h3.eulerosv2r8.aarch64.rpm
libkadm5-1.16.1-21.h1.eulerosv2r8.aarch64.rpm                   pcre-devel-8.42-4.h3.eulerosv2r8.aarch64.rpm
libselinux-devel-2.8-4.h2.eulerosv2r8.aarch64.rpm               pcre-utf16-8.42-4.h3.eulerosv2r8.aarch64.rpm
libsepol-devel-2.8-2.eulerosv2r8.aarch64.rpm                    pcre-utf32-8.42-4.h3.eulerosv2r8.aarch64.rpm
libstdc%2b%2b-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm        zlib-1.2.11-14.h4.eulerosv2r8.aarch64.rpm
libstdc%2b%2b-devel-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm  zlib-devel-1.2.11-14.h4.eulerosv2r8.aarch64.rpm
libverto-devel-0.3.0-6.h1.eulerosv2r8.aarch64.rpm
```

可以看到下载的 29 个文件都在其中，从中寻找报错的 `gcc-c++`，看到文件名时恍然大悟，`gcc-c++` 被转义成了 `gcc-c%2b%2b`。同样带有 `+` 的 `libstdc++` 和 `libstdc++-devel` 两个安装文件也都被用 `%2b` 转义，用未转义前的名称自然无法寻找到这些文件。

起初以为这是 yum 在处理特殊符号时 URL 编码的 bug，但在互联网上用关键词检索找不到任何相关的信息。仔细一想，yum 是无数 Linux 平台上默认的包管理器，怎么可能犯这么低级的错误，况且在安装这么常见的依赖时就能引发的 bug 理应很快就被修复了。

在许久漫无目的地寻找后，偶然发现了 GitHub 上的一篇 [<i class="fa-brands fa-github"></i> Issue](https://github.com/tmatilai/vagrant-proxyconf/issues/129)，大意是说代理软件应当支持识别 `yum.conf` 中的 URL 编码，否则会导致一些问题。这倒提醒了我，会不会是代理导致的问题呢？

## 修改 yum 源代理

设备可能带有华为用来日常管理维护设备的内部默认代理，不宜擅自修改，最好是仅修改 yum 源所使用的代理，不影响其他服务的运作。同样用 vim 修改 `/etc/yum.repos.d/EulerOS.repo` 文件的内容，仅在最后添加一行：

```toml
[euler-base]
name=EulerOS-2.0SP8 base
baseurl=http://mirrors.huaweicloud.com/euler/2.8/os/aarch64/
enabled=1
gpgcheck=1
gpgkey=http://mirrors.huaweicloud.com/euler/2.8/os/RPM-GPG-KEY-EulerOS
proxy=_none_
```

然后用同样的操作尝试更新 yum 源：

```shell
$ sudo yum clean all
$ sudo yum makecache
EulerOS-2.0SP8 local repo for internal use                          0.0  B/s |   0  B     00:00
EulerOS-2.0SP8 base                                                 0.0  B/s |   0  B     00:01
Failed to synchronize cache for repo 'base', ignoring this repo.
Failed to synchronize cache for repo 'euler-base', ignoring this repo.
Metadata cache created.
```

发现禁止源 `EulerOS-2.0SP8 base` 使用代理后，就无法连接上源仓库了。可以确定华为云上的 BMS 确实设置有供 yum 安装所使用的特殊代理，文件名的 URL 编码异常可能由该代理导致，从而引起 `[Errno 2] No such file or directory` 的错误。

## 解决方案

由于华为云 BMS 获取 yum 源仓库必须通过默认代理，不能通过取消代理解决该问题。那么就只能通过最朴素、最直接的方法解决这个问题了——手动改文件名。注意核对 cache 文件目录，手动将文件名中的 `%2b` 改回为 `+`，我这里有 `gcc-c%2b%2b` `libstdc%2b%2b` `libstdc%2b%2b-devel` 三个文件需要修改：

```shell
$ cd /var/cache/dnf/
$ sudo mv ./euler-base-85cc05102200a8ac/packages/gcc-c%2b%2b-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm ./euler-base-85cc05102200a8ac/packages/gcc-c++-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm
$ sudo mv ./euler-base-85cc05102200a8ac/packages/libstdc%2b%2b-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm ./euler-base-85cc05102200a8ac/packages/libstdc++-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm
$ sudo mv ./euler-base-85cc05102200a8ac/packages/libstdc%2b%2b-devel-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm ./euler-base-85cc05102200a8ac/packages/libstdc++-devel-7.3.0-20190804.h29.eulerosv2r8.aarch64.rpm
```

然后再尝试原先的安装命令，就发现先前提示无法找到的安装包能够成功安装上了。

---

## References

- [为 yum 源配置代理 - GitBook](https://pshizhsysu.gitbook.io/linux/yum/wei-yum-yuan-pei-zhi-dai-li)
- [如何知道你是否使用了代理服务器？ - Linux 中国](https://linux.cn/article-15657-1.html)