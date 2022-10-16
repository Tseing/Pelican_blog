title: 用 Markdown 创作 pptx 的尝试
slug:  generate-ppt-by-marp
date: 2022-09-27
tags: Marp, Markdown
summary: 总是遇到一些时候，一个又一个的 presentation 接踵而来，制作幻灯片就变成了令人头疼的事情。Marp 是一款支持使用 Markdown 语法生成 pptx 的工具，使用它或许可以解放双手。

Marp 的全称是 Markdown Presentation Ecosystem，专门用于制作各种展示的演示文稿，除 pptx 外，Marp 还可以输出 pdf 和 html 格式，Marp 输出的 html 文件特别有意思，值得一试！但是 html 中的图片依赖于相对路径，真正用于 presentation 还是 pptx 的 slide 更为方便。

## 安装

[Marp 官网](https://marp.app/#get-started)提供了 Marp for VS Code 与 Marp CLI 两个版本，相信会命令行的用户也不用看这篇文章了，所以我选择了 Marp for VS Code。直接在 VS Code 中搜索拓展 Marp for VS Code，下载安装即可。

安装完成后打开拓展设置，将 `Markdown > Marp:Export Type` 修改为 `pptx`，输出文件格式就默认为 pptx（若要调试 CSS 样式，输出 html 更为方便），其余设置按需修改。

接下来测试一下 Marp 的功能是否正常，新建一个 `.md` 文件，内容如下：

```markdown
---
marp: true
---

# Hello, Marp!

pptx by Marp
```

接着点击右上角的 `打开侧边预览` 按钮，或使用快捷键 `Ctrl+K V` （摁下 Ctrl+K 后再摁 V）打开预览界面。点击右上角 Marp 的图标，选择 `Toggle Marp Feature For Current Markdown` 后理应出现像下图一样的幻灯片预览。

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7652?authkey=ALYpzW-ZQ_VBXTU)

有的朋友会发现仍然是 Markdown 文档的样式，而非幻灯片分页的形式，这可能是因为之前安装了其他的 Markdown 预览插件。最简单的方法就是使用 VS Code 自带的预览工具，以我的 Markdown Preview Enhanced 插件为例，在它的插件设置中找到 `Hide Default VSCode Markdown Preview Button`，取消取定，重新启动后就会看见右上角有两个预览图标，一个是 VS Code 默认预览，另一个是 Markdown Preview Enhanced 插件，使用默认预览就能正常显示了。

## 创作幻灯片

Marp 中比较特殊的语法可以参考[官方文档](https://github.com/marp-team/marp-vscode)与[博客 CAI](https://caizhiyuan.gitee.io/categories/skills/20200730-marp.html)，其他语法与 Markdown 无异。

全局的样式定义在主题 CSS 文件中，有时候需要修改单独页面的主题，Marp 提供了局部样式的方式：

```html
<style scoped>
    <!-- Your style Here.
    Such as: -->
    p{
        font-size: 30px;
    }
</style>
```

Marp 使用与 Markdown 相同的方式插入图片，例如

```markdown
![img](url) ![img](url)

---

![img](url)
![img](url)
```

若将两个以上插入图片的语句写在同一行，那么两张图片会被包装在同一个 `<p></p>` 标签中，也就类似于在文本框中插入两张图片，若宽度足够，两张图片会左右排列在同一行。

若用第二种方式，也就是将两个以上插入图片的语句分行书写，那么各个图片在各自的 `<p></p>` 标签中，也就是分行排列。

正是因为图片在 `<p>` 标签中，继承了 `text-align: left` 的属性，也就是左侧对齐。对于我而言，图片居中更为重要，所以在样式文件中加入以下代码：

```css
img[alt~="center"] {
    display: block;
    margin: 0px auto;
}
```

在撰写文章时，使用 `![center](url)` 就能使图片居中了。但是因为 `display: block` 属性，居中的同时就不能左右排列两张图片了，所以欲使两张图片并排共同居中可能还要想点办法<del>（为什么要用 Markdown 做排版软件做的事 ..•˘_˘•.. ）</del>。


## 一个我创建的模版

Marp 中的样式是由 CSS 文件定义的，因此只要会使用 CSS，就能创建自己的主题。我制作了一个适用于各种汇报和答辩的 slide 主题，主题项目已经发布到 Github 了， [<i class="fa fa-github fa-lg"></i> Marp-Theme-NKU](https://github.com/Tseing/Marp-Theme-NKU) 仓库页面有更详细的介绍和安装方法。

![page1](https://storage.live.com/items/4D18B16B8E0B1EDB!7687?authkey=ALYpzW-ZQ_VBXTU)
![page2](https://storage.live.com/items/4D18B16B8E0B1EDB!7688?authkey=ALYpzW-ZQ_VBXTU)
![page3](https://storage.live.com/items/4D18B16B8E0B1EDB!7689?authkey=ALYpzW-ZQ_VBXTU)
![page4](https://storage.live.com/items/4D18B16B8E0B1EDB!7690?authkey=ALYpzW-ZQ_VBXTU)
![page5](https://storage.live.com/items/4D18B16B8E0B1EDB!7691?authkey=ALYpzW-ZQ_VBXTU)