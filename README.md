# My blog
Powered by `Pelican 4.8.0` & `Python 3.9.10`

# 常见问题

## Jinja2

`Jinja2`在生成页面时报错，安装`Jinja2==3.0.2`可以解决

## pelicanconf.py

生成页面时`output`文件夹中的所有项目会被删除覆盖，导致git仓库失效，务必在`pelicanconf.py`中添加`OUTPUT_RETENTION = [".git"]`

# To Do

- [ ] google ajax 和 google fonts访问速度过慢
- [ ] 菜单栏
- [ ] 搜索
- [ ] SSR订阅