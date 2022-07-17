# My blog

Powered by `Pelican 4.8.0` & `Python 3.9`

# 常见问题

## Jinja2

`Jinja2`在生成页面时报错，安装`Jinja2==3.0.2`可以解决

## pelicanconf.py

生成页面时`output`文件夹中的所有项目会被删除覆盖，导致git仓库失效，务必在`pelicanconf.py`中添加`OUTPUT_RETENTION = [".git"]`

## 部分网页资源在 Firefox 上失效

部分字体、图标在 Firefox 浏览器上无法正常加载，按 F12 可见错误`已拦截跨源请求`。若在`localhost：8000`开放，需要手动输入为`http://localhost:8000`。

## 使用相对路径的网页资源失效

原因在于`html`文件中调用相对路径的行为是不准确的。例如文件结构如下，若在`pelicanconf.py`中将图片的相对路径会写为`"/images/cover.jpg"`，结果就是`index.html`页面可以显示，而`page.html`调用时不存在`pages/images/cover.jpg`文件。推荐做法是在`pelicanconf.py`设置`SITEURL`，使用`SITEURL + "相对路径"`指向文件。

```
output
├── index.html
├── pages
│      └── page.html
└── images
       └── cover.jpg
```

## 模版文件中的 {{ SITEURL }} 失效

务必在`pelicanconf.py`与`publishconf.py`中都添加`SITEURL`，解决一部分路径问是。其余未解决，暂时用 Github Pages 地址代替。

# To Do

- [x] google ajax 和 google fonts访问速度过慢
- [x] 菜单栏
- [ ] 搜索
- [x] SSR订阅
- [x] 资料页面
- [x] sitemap