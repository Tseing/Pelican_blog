title: 把博客站点交给了 Cloudflare 托管
slug: cloudflare-dns-of-blog
date: 2023-10-31
tags: Cloudflare, DNS, Nginx, Blog

因为博客域名是在阿里云购买的，先前一直顺理成章地用着阿里云的 DNS 解析。阿里云的 DNS 解析在各方面的体验都很不错，例如修改配置后就能很快更新、配置平台访问速度快、站点不会被国内的运营商污染等等，这些优点反过来可是说尽是 Cloudflare 的缺点。

但由于 Cloudflare 为网站提供的各种免费服务十分诱人，加之我想利用 Cloudflare 的 CDN 搭建博客图床，终究是把站点交给了 Cloudflare 管理。本文记录了从阿里云迁移站点的过程和一些必要的 Nginx 配置。

## Cloudflare 注册站点

打开 [Cloudflare 官网](https://www.cloudflare-cn.com/)，注册帐号后选择添加站点，输入域名后点击继续。

![!Cloudflare](https://storage.live.com/items/4D18B16B8E0B1EDB!11535?authkey=ALYpzW-ZQ_VBXTU)

按需选择计划，对于普通的小站点来说，Free 计划足矣。点击继续后，Cloudflare 会检测站点目前已有的部分 DNS 记录，其余未检测出的记录日后再手动添加，最关键的是检查域名指向服务器 IP 地址的 A 记录是否正确。

![!DNS records](https://storage.live.com/items/4D18B16B8E0B1EDB!11536?authkey=ALYpzW-ZQ_VBXTU)

在「代理状态」一列可以选择该 DNS 记录是否使用 Cloudflare 的 CDN，激活后图标显示一朵黄色的云。Cloudflare 的 CDN 在国内速度很慢，一直被称为减速 CDN，所以我都选择「仅 DNS」。此前我也担心 Cloudflare 的 DNS 解析会不会也像其 CDN 一样龟速，幸好解析速度并不慢，我的担心是多虑了。

提交 DNS 记录后，Cloudflare 会提示删除阿里云的 DNS 服务器，以 Cloudflare 的 DNS 服务器代替之，接着就转到阿里云的控制中心操作。

## 更换 DNS 服务器

登录[阿里云](https://www.aliyun.com)，进入控制台。在云解析 DNS - 域名解析下找到迁移的域名，在解析设置中保存了站点的 DNS 记录。将记录备份，后续要将所有记录导入 Cloudflare。站点交由 Cloudflare 解析后，阿里云中的解析设置也会失效，所以也在解析设置中将所有解析都停用。

![!aliyun DNS records](https://storage.live.com/items/4D18B16B8E0B1EDB!11537?authkey=ALYpzW-ZQ_VBXTU)

在阿里云控制台中来到域名控制台 - 域名列表，选择域名的管理 - DNS 管理 - DNS 修改 - 修改 DNS 服务器，将 Cloudflare 提供的两个 DNS 服务器地址填入其中。

![!DNS server](https://storage.live.com/items/4D18B16B8E0B1EDB!11538?authkey=ALYpzW-ZQ_VBXTU)

修改 DNS 服务器一般需要 24-48 h 生效，生效后 Cloudflare 会发送邮件通知。如果迟迟没有收到邮件，也可以到 Cloudflare 手动验证网站。验证成功后 Cloudflare 会指引是否开启 Brotli 压缩等功能，按需选择即可。至此，站点已经交由 Cloudflare 托管。如果站点是由 Nginx 搭建的，那么就还需要考虑 Nginx 的 SSL 设置是否与 Cloudflare 兼容。

## Nginx 中的 SSL 相关配置

![!Cloudflare SSL](https://storage.live.com/items/4D18B16B8E0B1EDB!11539?authkey=ALYpzW-ZQ_VBXTU)

在 Cloudflare 的 SSL/TLS 设置界面可以看到，用户访问由 Cloudflare 托管的站点的过程中有 3 个实体，根据实体间通信安全等级的不同可以分为 4 种模式：

1. 关闭：浏览器-Cloudflare 间和 Cloudflare-服务器间都使用 HTTP；
2. 灵活：浏览器-Cloudflare 间使用 HTTPS，Cloudflare-服务器间使用 HTTP；
3. 完全：浏览器-Cloudflare 间和 Cloudflare-服务器间都使用 HTTPS，需要 SSL 证书；
4. 完全（严格）：浏览器-Cloudflare 间和 Cloudflare-服务器间都使用 HTTPS，需要非自签名 SSL 证书。

现在的站点一般都使用了 HTTPS<del>，还在使用 HTTP 的站长快去申请个 SSL 证书吧</del>，同时通过 Nginx 将访问 80 端口的 HTTP 流量强制重定向到 HTTPS 入口。若使用这样的 Nginx 配置又开启的「灵活」模式，用户发起访问请求后，Cloudflare 使用 HTTP 交由 Nginx，Nginx 告知用户重定向为 HTTPS，但Cloudflare 仍使用 HTTP 与 Nginx 通信，该过程无限循环，出现 **301 重定向次数过多**。

为了保证站点的安全性和避免以上问题，推荐配置好站点的 HTTPS 后，在 Cloudflare 的 SSL/TLS 中<dot>使用完全或完全（严格）两种模式。</dot>

最后附上我的 Nginx 配置供参考：

```nginx
server {
    listen                              443 ssl http2;
    server_name                         leonis.cc;
    root                                /home/Leo/web/blog;

    # SSL 配置
    ssl_certificate                     /etc/nginx/cert/leonis.cc.cer;
    ssl_certificate_key                 /etc/nginx/cert/leonis.cc.key;
    ssl_session_timeout                 5m;
    ssl_ciphers                         ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
    ssl_protocols                       TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers           on;

    location / {
        index index.html;
    }
}

server {
    listen                              80;
    server_name                         leonis.cc
    # 重定向至 HTTPS，开启 Cloudflare 完全模式后不会访问 80 端口，也不会用上此处的重定向
    rewrite ^/(.*)$ https://leonis.cc:443/$1 permanent;
}
```

## 后记

Cloudflare 总体来说还是很好用的，提供了很多有意思的功能，很便利地就能体验，免去了自己动手配置的烦恼。Cloudflare 的不足仅在于在国内有时访问不畅，添加 DNS 记录后也要等比较长的时间才会更新到国内网络上，若能接受这两点，Cloudflare 的可玩性还是比其他平台更高的。