title: 在不安装 Anaconda 的条件下安装 RDKit
slug:  install-rdkit
date: 2022-10-13
tags: Python, RDKit
summary: RDKit 是一款十分常用的化学信息包，但由于它不是纯粹的 Python 包，不能直接使用 pip 安装。官网上给出最方便的安装方法是要使用 Anaconda，而 Anaconda 的臃肿令我很难喜欢上它，因此偏要在 在不安装 Anaconda 的条件下安装 RDKit。
status: hidden

## 准备工作

参考 RDKit 官网的[安装指南](https://rdkit.org/docs/Install.html#windows)，在 Windows 下安装 RDKit 需要以下依赖：

- python 3.6+
- numpy
- Pillow

这些依赖的安装十分简单，不需要在这里介绍了，但除此以外还需要安装一些软件：

- Microsoft Visual C++：C/C++ 的 IDE，[下载链接](https://visualstudio.microsoft.com/vs/community/)
- CMake：[下载链接](http://www.cmake.org/cmake/resources/software.html)
- Boost：[下载链接](http://sourceforge.net/projects/boost/files/boost-binaries/)

### 安装 Boost

Microsoft Visual 和 CMake 都好安装，只是 Boost 比较麻烦。下载 Boost 压缩包后将其挪到安装的路径并解压。使用命令行进入解压得到的文件夹，使用 `setx BOOST_ROOT D:\boost_1_80_0` 设定环境变量，接着运行 `bootstrap.bat`。

![bootstrap](https://storage.live.com/items/4D18B16B8E0B1EDB!7768?authkey=ALYpzW-ZQ_VBXTU)

然后在目录中就生成了 `b2.exe`，使用 `b2.exe --address-model=64` 命令编译 Boost，其中 `--address-model=64` 参数指安装在 64位系统下。输出以下信息即表示安装成功：

```
The Boost C++ Libraries were successfully built!

The following directory should be added to compiler include paths:

    D:\boost_1_80_0

The following directory should be added to linker library paths:

    D:\boost_1_80_0\stage\lib
```

### 下载 RDKit 源代码

在 RDKit 仓库中的 [releases 页面](https://github.com/rdkit/rdkit/releases)下载选定版本，将文件解压后复制其中的 `rdkit` 文件夹，粘贴至需要放置的路径下。

### 安装 PostgreSQL

RDKit 许多功能也依赖于 PostgreSQL 数据库，但不知为什么官网的依赖中没有写明。直接在 PostgreSQL 官网下载安装包后安装至选定路径，唯一的要求是版本在 9.1 之上。

## 设定环境变量

在设定环境变量前，首先确定一下各个依赖的路径，我的设置是这样的：

- Python：`D:\Python39`
- RDKit：`E:\Py39Lib\RDKit`
- Boost：`D:\boost_1_80_0`
- PostgreSQL：`D:\PostgreSQL\9.5`

那么根据官方文档的说明，需要保证

- `D:\Python39` 在环境变量中
- `E:\Py39Lib\RDKit\lib` ？
- `D:\boost_1_80_0\libs` 在环境变量中
- `E:\Py39Lib\RDKit` 在 PATHONPATH 中

添加环境变量的步骤也很简单，添加路径至 PATH 变量下即可。在系统变量中也有 PATHONPATH 变量，按相应的要求添加即可。可以使用 `python -m site` 命令检查是否将目录添加到了 PATHONPATH。

## 建立工程文件

1. 在 `E:\Py39Lib\rdkit` 中创建名为 `build` 的文件夹，使用命令行进入该文件夹；
2. 运行 CMake，使用命令为 `cmake -DRDK_BUILD_PYTHON_WRAPPERS=ON -DBOOST_ROOT=D:\boost_1_80_0 -DRDK_BUILD_INCHI_SUPPORT=ON -DRDK_BUILD_AVALON_SUPPORT=ON -DRDK_BUILD_PGSQL=ON -DPostgreSQL_ROOT="D:\PostgreSQL\9.5" -G"Visual Studio 15 2017" ..`。注意其中的路径参数以及 Visual Studio 版本都需要按自己电脑的环境设置。这个步骤需要从 GitHub 与 Google 服务上下载文件，需要预先检查好网络的通联状态。
3. `C:/Windows/Microsoft.NET/Framework64/v4.0.30319/MSBuild.exe /m:4 /p:Configuration=Release INSTALL.vcxproj`

Windows 装不上 pthread，遂放弃。