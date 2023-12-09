title: Cloudflare + Backblaze 实现免费的博客图床方案
slug: deploy-backblaze-image-hosting
date: 2023-11-17
tags: Cloudflare, Blog

图床一直是困扰 Markdown 以及静态博客用户的麻烦事，[Ln's Blog](https://weilining.github.io/177.html) 总结了一些免费图床服务，还分别列出了测试链接，可以比较主观地比较各图床的速度，也可以判断在所处网络环境下该图床是否可用。

我对图床的要求只有访问速度可靠、数据受控几点，遗憾的是尝试过的众多图床服务都不能满足我的要求，唯一适合我的方案只能是使用 OSS 搭建图床。于是我调查了阿里、腾迅等多家厂商提供的 OSS 服务，极复杂的收费规则首先就劝退了我。

辗转之下我发现了 Backblaze 提供的存储服务，B2 云存储提供 10 GB 的免费空间，同时 Cloudflare 与 Backblaze 之间的流量不计费，用作为图床是完全足够了，就算超出免费额度，$0.006 GB/Month 的价格也很合适。

使用 Backblaze B2 作为图床的唯一要求就是拥有一条托管在 Cloudflare 上的域名。若不知道如何将域名转移到 Cloudflare 上，可以参考先前写的[迁移教程](https://leonis.cc/sui-sui-nian/2023-10-31-cloudflare-dns-of-blog.html)，完成后就可以按照本文的步骤操作了。

## 创建桶

![!Backblaze homepage](https://storage.live.com/items/4D18B16B8E0B1EDB!12725?authkey=ALYpzW-ZQ_VBXTU)

打开 [Backblaze 官网](https://www.backblaze.com/)很容易就能找到 B2 Cloud Storage 产品，完成注册与邮箱验证后，登录即可免费创建 B2 云存储的桶。

![!Create Bucket](https://storage.live.com/items/4D18B16B8E0B1EDB!12726?authkey=ALYpzW-ZQ_VBXTU)

{note begin}Backblaze 提供的部分机翻中文根本看不懂，建议在网站的右下角切换语言为英文。{note end}

选择 `Create a Bucket`，在 Bucket Unique Name 一栏填入桶名称，桶名决定了源站的 URL，应尽可能复杂避免被他人猜测到。若源站 URL 泄露，绕过 Cloudflare 的直接访问就会产生额外流量了。其余项如下图保持默认即可：

![!Bucket config](https://storage.live.com/items/4D18B16B8E0B1EDB!12727?authkey=ALYpzW-ZQ_VBXTU)

创建完成后，选择 `Upload / Download` 尝试在桶中上传一张图片，查看图片的详细信息，其中 Friendly URL 一项就是生成的图片链接。

![!Image URL](https://storage.live.com/items/4D18B16B8E0B1EDB!12729?authkey=ALYpzW-ZQ_VBXTU)

以 `f000.backblazeb2.com/file/a-complicated-name/hokciu.jpg` 为例，图片链接可以都分成以下几个部分：

|       主机名        |  后缀  |         桶名         |   图片路径   |
| :-----------------: | :----: | :------------------: | :----------: |
| `f000.backblze.com` | `file` | `a-complicated-name` | `hokciu.jpg` |

因为 Friendly URL 中包含了桶名，不宜直接引用。假设想要将链接改写为 `img.leonis.cc/hokciu.jpg`，显然要修改主机名、隐藏固定的后缀和桶名，再拼接上图片路径，URL 的改写就通过 Cloudflare 实现。

## 添加 DNS 记录

改写的目标 URL 必须使用 Cloudflare CDN，打开 Cloudflare 控制台，添加名称为 `img` 目标为 `f000.backblazeb2.com` 的 CNAME 记录，并<dot>将代理状态设为打开</dot>。待 DNS 记录生效后，就实现了 `img.leonis.cc` → `f000.backblazeb2.com` 的跳转。

![!DNS record](https://storage.live.com/items/4D18B16B8E0B1EDB!12730?authkey=ALYpzW-ZQ_VBXTU)

## 配置转换规则

同样在 Cloudflare 控制台中，找到 `规则` - `转换规则` 页面并创建新规则，填写规则自定义名称后就来处理 URL 的转换问题。

第一次接触 Cloudflare 的转换规则功能时，我被界面上各个选项弄得很迷糊，所以我在这里介绍一下转换规则各个功能的使用方法，读者理解了就能根据自己的想法配置图片链接了。

<dot>规则页面上的「传入请求」是指访客对托管站点发起的请求</dot>，例如访客所浏览的页面上有一条 `img.leonis.cc/hokciu.jpg` 链接，该请求先进入到 Cloudflare 的服务器，再根据设定的规则前往 `f000.backblazeb2.com/file/a-complicated-name/hokciu.jpg` 取出图片资源，最终呈现在页面上。

前文为了表述简单，说的是将 `f000.backblazeb2.com/*` 改为 `img.leonis.cc/*`，实则是我们要设定一个规则，让访客能通过 `img.leonis.cc/*` 到 `f000.backblazeb2.com/*` 中取得需要的图片。

在规则页面中的设置项可以参考下图：

![!Transform rule](https://storage.live.com/items/4D18B16B8E0B1EDB!12731?authkey=ALYpzW-ZQ_VBXTU)

该规则筛选得到所有主机名为 `img.leonis.cc` 的请求，将其 URL 重写到 `concat("/file/a-complicated-name", http.request.uri.path)`，也就是把所有对 `img.leonis.cc/*` 的请求指向 `img.leonis.cc/file/a-complicated-name/*`。而因为 `img.leonis.cc` 已经通过 CNAME 指向了 `f000.backblazeb2.com`，最终请求都到达 `f000.backblazeb2.com/file/a-complicated-name/*` 并取得图片资源。

上述请求过程可以表示成

```txt
GET: https://img.leonis.cc/hokciu.jpg
→ https://img.leonis.cc/file/a-complicated-name/hokciu.jpg
→ https://f000.backblazeb2.com/file/a-complicated-name/hokciu.jpg
```

需要注意的是，因为这里使用的是**重写**（rewrite）而非**重定向**（redirect），请求的改变发生在服务端而非客户端，<dot>整个过程中用户都不会看见 URL 发生变化</dot>，所以也就达到了隐藏桶名的目的。

若设置全部无误，这时候就可以通过 `https://img.leonis.cc/example.jpg` 打开先前上传的图片了，由于 Backblaze 只支持 HTTPS，若打开 `http://img.leonis.cc/example.jpg` 则会弹出无效页面，用户体验不太好，所以接下来我们还需要通过 Cloudflare 页面规则完成 HTTPS 重写和缓存的相关设置。

## 设置页面规则

回到 Backblaze 找到 Bucket Settings 一项，在 Bucket Info 中填入 `{"cache-control":"max-age=720000"}`，该项将 Cloudflare 回到源站获取资源的周期设定为 720000 s，用于避免回源次数过多导致加载速度过慢。当然，该周期过长也会导致源文件更改后不能及时更新，可以按自己的需求更改。

![!Bucket cache](https://storage.live.com/items/4D18B16B8E0B1EDB!12732?authkey=ALYpzW-ZQ_VBXTU)

在 Cloudflare 中打开 `规则` - `页面规则`，新建一条页面规则，在 URL 一栏中填入 `img.leonis.cc/*`，按下图设置设置缓存和 HTTPS 即可。

![!Page rule](https://storage.live.com/items/4D18B16B8E0B1EDB!12733?authkey=ALYpzW-ZQ_VBXTU)

{note begin}暂时不确定边缘缓存 TTL 和缓存级别两个设置项有什么作用，发现在未设置时图片就能命中缓存。不过既然官方文档提到了这两项配置就先给开启了，回头找找有没有详细些的资料。{note end}

再打开样例图片的链接，查看浏览器的开发者工具，在响应头中有一项 `cd-cache-status`，其值若为 `HIT`，则表示 Cloudflare 命中了缓存，该图片是由缓存中取出的。

![!Cache response](https://storage.live.com/items/4D18B16B8E0B1EDB!12734?authkey=ALYpzW-ZQ_VBXTU)

至此关于 Backblaze + Cloudflare 的图床就设置完了，接下来还可以借助 PicGo 等第三方工具更方便地上传图片并获取图片链接，这部分内容可以根据章节标题向后文寻找。

## 整合静态资源

由于博客通常会使用到包括图片、字体在内的多种静态资源，我希望将他们都整合到相同的子域名下。当某些静态资源由于各种原由突然挂掉的时候<del>（说的就是 jsDelivr 和 Google Fonts）</del>，我就可以直接在 Cloudflare 控制台上将其指向备用服务而不用去网页中一个个修改引用的链接，在管理维护上更方便。如果读者没有此需求，就可以完整跳过这一节了。

![!URL design](https://storage.live.com/items/4D18B16B8E0B1EDB!12735?authkey=ALYpzW-ZQ_VBXTU)

在我的设想中，所有静态资源都由 `cdn.leonis.cc` 分发，通过 URL 路径转向不同的子域名取得目标资源，后面就以图片资源为例实现这个构想。

#### 添加 CDN 子域名

先在 Cloudflare 中添加子域名 `cdn.leonis.cc` 的 DNS 记录，暂时任意设置一个解析目标，能让 Cloudflare 获取缓存即可。

#### 处理 URL 重定向

接着要实现对 URL 路径的处理，例如将 `cdn.leonis.cc/img/*` 重定向到 `img.leonis.cc/*`，这种重定向可以通过 Cloudflare 规则功能下的页面规则或重定向规则实现。

若使用**页面规则**，可以使用下图中的方案，用通配符实现 URL 解析：

![!Page rule](https://storage.live.com/items/4D18B16B8E0B1EDB!12736?authkey=ALYpzW-ZQ_VBXTU)

该方案的一个小缺点在于无法将规则应用于 `cdn.leonis.cc/img` 等不带后一个 `/` 的页面。使用**重定向规则**可以解决这个问题，但重定向规则中的正则匹配是收费功能，无法批量处理，每种后缀都必须添加一条规则，配置方案可以参考下图：

![!Redirect rule](https://storage.live.com/items/4D18B16B8E0B1EDB!12737?authkey=ALYpzW-ZQ_VBXTU)

表达式 `concat("https://img.leonis.cc", substring(http.request.uri.path, 4))` 中的 `substring()` 用于除去 `/img/*` 的前 4 个字符，若是用于处理 `/js/*` 等不同的 URL 则需要根据字符数量更改该数值。以上两种方案各有优劣，读者可以根据自己的需求选择。

## 设置防盗链

防盗链是用于屏蔽其他站点对静态资源引用的常用手段，倒不是不愿意分享资源，至少本站内的各种照片都可随意使用，而是个人站点的服务容量有限，很难做到再向外提供服务。除此以外，设置防盗链对于避免流量被恶意浪费也很有必要。防盗链的功能可以通过 Cloudflare 的防火墙规则实现，打开 `安全性` - `WAF` 页面即可创建规则。

防盗链功能一般通过请求头中的 `Referer` 字段判断是否允许请求，例如允许自己的站点引用图片（**Referer 为本站** `leonis.cc`），不允许他人的站点引用图片（**Referer 为外站** `bing.com`）。另外还有一种**没有 Referer** 的情况，例如直接打开图片、在各种 Markdown 编辑器中使用图片都属于这一类。

为了不影响正常使用，我使用的防盗链规则是<dot>允许无 Referer 与白名单站点访问</dot>。很棘手的是，Cloudflare 没有提供判断有无 Referer 的功能，所以我使用了比较曲折的方法实现该方案。

首先新建一条防火墙规则，对于静态资源的 URL，阻止所有 Referer 中包含 `"http"` 的请求：

![!WAF rule](https://storage.live.com/items/4D18B16B8E0B1EDB!12738?authkey=ALYpzW-ZQ_VBXTU)

{note begin}该规则实际上阻止了所有具有 Referer 的请求，由于无法使用通配符才用 `"http"` 作为匹配内容。需要注意的是，没有 Referer 的请求不在该匹配范围内，设置后仍可访问。{note end}

再新建一条规则，这条规则用于根据 Referer 放行请求，作用等同于白名单，设置项如下：

![!Whitelist](https://storage.live.com/items/4D18B16B8E0B1EDB!12739?authkey=ALYpzW-ZQ_VBXTU)

设置生效后可以发现，先前的图片链接可以直接打开，却不能在其他网站上引用了。Cloudflare 阻止了白名单以外站点的引用请求，在防火墙事件中还可以查看阻止请求的来源 IP 等具体信息。

![!Blocking](https://storage.live.com/items/4D18B16B8E0B1EDB!12740?authkey=ALYpzW-ZQ_VBXTU)

{note begin}后来发现在 Cloudflare 控制台中的 `Scrape Shield` 页面中有一项 **Hotlink 保护**功能，一键即可开启防盗链，在 `Configuration Rules` 中添加规则即为白名单，该配置方案更简单，以上 WAF 方案也留作参考。{note end}

## PicGo 设置

若每次上传图片都要打开 Backblaze 网站终归还是很麻烦，好在 PicGo 能够让整个过程自动化。PicGo 还提供了丰富的插件，可以实现自定义文件路径、文件名哈希化等功能。

设置 PicGo 作为 Backblaze 的图片上传工具，需要先打开 Backblaze Buckets 页面，在桶信息中记录下 `Endpoint` 的内容：

![!Endpoint](https://storage.live.com/items/4D18B16B8E0B1EDB!12741?authkey=ALYpzW-ZQ_VBXTU)

再在页面中找到 `Application Keys` 界面，选择 `Add a New Application Key`，填入 key 的名字：

![!Key config](https://storage.live.com/items/4D18B16B8E0B1EDB!12743?authkey=ALYpzW-ZQ_VBXTU)

在 `Duration` 一项可以设置 key 的有效期，过期后需要重新申请。选择提交后，页面就会给出生成的 `keyID` 和 `applicationKey`，将内容复制保存下来，一凡离开该页面就再也无法查看了。

![!Generated key](https://storage.live.com/items/4D18B16B8E0B1EDB!12744?authkey=ALYpzW-ZQ_VBXTU)

安装好 PicGo 后，搜索并安装 s3 插件，打开 Amazon S3 的设置界面，填入先前保存下的信息，我的设置如下：

```json
"aws-s3": {
    "accessKeyID": "Backblaze keyID",
    "secretAccessKey": "Backblaze applicationKey",
    "endpoint": "https://s3.us-west-000.backblazeb2.com",
    "bucketName": "a-complicated-name",
    "uploadPath": "{year}/{month}/{sha256}.{extName}",
    "urlPrefix": "https://cdn.leonis.cc/img/"
}
```

其中比较关键的是 `accessKeyID`、`secretAccessKey`、`endpoint` 三项，确保填写正确，另外不要忘了在 endpoint 前加上 `https://`。其余项则用于自定义图片路径和得到的 URL，具体配置可以参考[插件仓库](https://github.com/wayjam/picgo-plugin-s3)中的说明。

到这里就大功告成了，下面两张图片都存放在 Backblaze 上，一张是前文手动上传的示例图片，另一张则是通过 PicGo 上传。关于图片的加载速度和链接，不用我多说，诸君查看这两张图片即可自明。

![!PicGo demo](https://cdn.leonis.cc/img/2023/11/9c341684e296247e896e1f4131fc36f8da3e897335572206adc8774849f2fa8b.jpg)

![!Demo](https://cdn.leonis.cc/img/hokciu.jpg)

---

## References

- [Deliver Public Backblaze B2 Content Through Cloudflare CDN](https://www.backblaze.com/docs/cloud-storage-deliver-public-backblaze-b2-content-through-cloudflare-cdn)
- [Backblaze B2 + CloudFlare 搭建图床 - Mitsea Blog](https://blog.mitsea.com/67b8601211284a25b68bb8afe65b80a7/)
- [使用 Backblaze B2 + Cloudflare CDN + PicGo 实现可自定义域名的 10G 免费图床解决方案 - winer's Blog](https://blog.winer.website/archives/use_blackblaze_b2_and_cloudflare_cdn_to_bulid_a_free_oss.html)