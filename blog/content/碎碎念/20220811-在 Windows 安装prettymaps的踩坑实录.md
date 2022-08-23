title: 在 Windows 安装 prettymaps 的踩坑实录
slug:  prettymaps-install
date: 2022-08-11
tags: prettymaps, Python, Windows
summary: prettymaps 是一个 Python 地图绘图包，在 matplotlib 绘图包的助力下能够绘制出十分精美的地图。但是 prettymaps 在 Windows 下的安装十分恼人，这篇笔记记录下了安装过程中的常见错误。


`prettymaps` 是一个 Python 地图绘图包，能够使用 OpenStreetMap 的地图数据，在 `matplotlib` 绘图包的助力下能够绘制出十分精美、极具艺术感的地图。但是 `prettymaps` 在 Windows 下的安装十分恼人，这篇笔记记录下了安装过程中的常见错误。

## 尝试直接使用 pip 安装

在项目的 [Github 仓库](https://github.com/marceloprates/prettymaps)中，作者提供的方法是直接通过 `pip install prettymaps` 安装，但是在 Windows 设备上貌似不起作用。命令行信息提示在安装 `Fiona` 时发生错误，错误信息如下：

```
  Using cached Fiona-1.8.21.tar.gz (1.0 MB)
  Preparing metadata (setup.py) ... error
  error: subprocess-exited-with-error

  × python setup.py egg_info did not run successfully.
  │ exit code: 1
  ╰─> [1 lines of output]
      A GDAL API version must be specified. Provide a path to gdal-config using a GDAL_CONFIG environment variable or use a GDAL_VERSION environment variable.
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.

note: This is an issue with the package mentioned above, not pip.
hint: See above for details.
```

这里我们需要先明确一下 `prettymaps` 的依赖：

```
- prettymaps
╰─> - Fiona
    ╰─> - GDAL
```

再根据错误信息，也就是在安装 `Fiona` 依赖时调用的 `GDAL` 未正确配置，我的设备上没有安装 `GDAL`，所以需要先安装 `GDAL`。

## 安装 GDAL core（不推荐）

可以先尝试直接 `pip install gdal`，不出意外的话会有以下错误：

```
extensions/gdalconst_wrap.c(2703): fatal error C1083: 无法打开包括文件: “gdal.h”: No such file or directory
extensions/gdal_array_wrap.cpp(2829): fatal error C1083: 无法打开包括文件: “gdal.h”: No such file or directory
extensions/gnm_wrap.cpp(2820): fatal error C1083: 无法打开包括文件: “gdal.h”: No such file or directory
extensions/ogr_wrap.cpp(2838): fatal error C1083: 无法打开包括文件: “gdal.h”: No such file or directory
extensions/osr_wrap.cpp(2879): fatal error C1083: 无法打开包括文件: “cpl_string.h”: No such file or directory
extensions/gdal_wrap.cpp(2883): fatal error C1083: 无法打开包括文件: “cpl_port.h”: No such file or directory
```

这是因为 Windows 缺少 Linux 自带的 GDAL core，一个解决方法就是在 Windows 上安装 GDAL core。因为这个过程无比繁琐，而且我不是 GIS 从业者，没有使用其他依赖于 GDAL core 软件的需要，所以我最后没有采取这种方法。

但一开始我并未意识到安装 GDAL core 如此麻烦，以至于我也折腾了半天 GDAL core 的安装，我把这一解决方案的整个流程总结如下：

`安装 GDAL core` ⇨ `安装 GDAL bindings` ⇨ `设置 GDAL core 环境变量` ⇨ `安装 Fiona`

安装 GDAL core 与 bindings，可以前往 [GISInternals](https://www.gisinternals.com/release.php) 下载安装文件。因为我的设备上安装了 Visual Studio 2017，我就选择了 MSVC 2017 x64 版本。

![GISInternals首页](https://storage.live.com/items/4D18B16B8E0B1EDB!7531?authkey=ALYpzW-ZQ_VBXTU)

要下载 GDAL core 和 bindings 两个安装文件，其中 bindings 需要与自己的 Python 版本匹配，下载完成后先安装 core 再安装 bindings。

![GISInternals下载文件](https://storage.live.com/items/4D18B16B8E0B1EDB!7533?authkey=ALYpzW-ZQ_VBXTU)

安装完成后，使用 pip 可以查询到 `GDAL` 的安装信息：

```python-repl
>>> pip list
Package           Version
----------------- -------
GDAL              3.5.1
```

此时已经在 Python 中安装了 `GDAL`，但还需要配置环境变量后才能安装 `Fiona`。详细步骤可以参考[这篇文章](https://zhuanlan.zhihu.com/p/141226948)。


## 使用 .whl 文件安装（推荐）

`GDAL` 与 `Fiona` 不能直接通过 pip 安装是因为缺少 GDAL core，在不安装 GDAL core 的情况下，可以使用预编译的 `.whl` 安装这两个依赖。UCI 的 [Python 拓展包仓库](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)提供了这两个依赖的 `.whl` 文件。

![GDAL下载页面](https://storage.live.com/items/4D18B16B8E0B1EDB!7530?authkey=ALYpzW-ZQ_VBXTU)

要注意文件名中的两个参数，cp 指 Python 版本，win 字段指 CPU 架构，也就是常说的 32 位或 64 位系统。因此我选择的就是 `GDAL‑3.4.3‑cp39‑cp39‑win_amd64.whl`。

将下载文件移入 Python 安装目录下的 `Scripts` 文件夹中，在该文件夹中打开终端，能过以下命令尝试安装：

```python-repl
>>> pip install GDAL-3.4.3-cp39-cp39-win_amd64.whl
ERROR: Could not install packages due to an OSError: [Errno 22] Invalid argument
```

出现这个错误时我寻找了大量解决方法，当然，这个错误也没法解决，这纯粹是安装文件的问题。这个隐藏的坑浪费我大量时间，后来我发现将安装文件换成`3.3.3`版本，就能成功安装了。

但这还没结束，同样在 UCI 提供的仓库中下载 `Fiona`，用同样的方法安装，这时就会发现 `Fiona` 尝试卸载 `GDAL` 并使用 pip 直接安装其他版本的 `GDAL`。当然，结局就会和上面的情况一样，用 pip 直接安装是安装不上 `GDAL` 的。

这是因为这里还有一个隐藏的大坑，就是 `GDAL` 与 `Fiona` 的版本必须匹配，否则就会自动重新下载。经过大量尝试，Python 版本为 `3.9.10` 的条件下，可以使用 `GDAL==3.3.2` 与 `Fiona==1.8.20`，这两个版本在 UCI 提供的仓库中都没有，我把下载链接放在后文。

安装好这两个依赖后，就可以直接使用 `pip install prettymaps` 安装 `prettymaps` 了。在 Python 交互模式下输入 `import prettymaps`，若无错误信息，就成功安装好 `prettymaps` 了。

## 总结

Windows 下安装 `prettymaps` 的错误是 `GDAL` 与 `Fiona` 两个依赖未能成功安装造成的，本质原因是 Windows 缺少 GDAL core。

由于以上原因在 Windows 下未能成功安装 `prettymaps` 的推荐解决步骤如下：

1. 安装 [GDAL-3.3.2-cp39-cp39-win_amd64.whl](http://1drv.stdfirm.com/u/s!AtseC45rsRhNunGGuDYayQdVADT3?e=RAJEsi)
2. 安装 [Fiona-1.8.20-cp39-cp39-win_amd64.whl](http://1drv.stdfirm.com/u/s!AtseC45rsRhNunAkPiG4AOb9V8yi?e=fAgNhp)
3. `pip install prettymaps`

{warn begin}本文最后更新于 2022 年 08 月 11 日，请确定内容是否过时。{warn end}

---

## References

- [Python中GDAL的安装 - 知乎](https://zhuanlan.zhihu.com/p/32224877)
- [windows10 环境中安装GDAL及其python绑定 - 知乎](https://zhuanlan.zhihu.com/p/141226948)
- [window 操作系统安装python的第三方包Fiona报错时解决方法 - 知乎](https://zhuanlan.zhihu.com/p/389235808)
