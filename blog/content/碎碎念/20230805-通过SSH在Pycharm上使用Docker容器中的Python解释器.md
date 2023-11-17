title: 通过 SSH 在 Pycharm 上使用 Docker 容器中的 Python 解释器
slug: connect-docker-container-by-pycharm
date: 2023-08-05
tags: Docker, Linux, Mindspore, SSH, Pycharm, Python

配置工程的运行环境一直是一件麻烦事，尽管 Anaconda 等工具提供的虚拟环境能够提够相对隔离的 Python 环境，但在调用更为底层硬件资源时难免会遇到冲突。例如我所遇到的情况是，需要使用的 Mindspore 最高仅支持 CUDA 11.6，而设备上已经安装了 CUDA 11.8，卸载又担心导致先前的项目出问题，这样冲突就只能靠 Docker 来解决了。

我的解决方案很简单，直接从 Docker Hub 上拉取 CUDA 11.6 的 Mindspore 镜像，镜像中已经做好了相应的配置且与宿主机的环境隔离，运行该镜像的容器后就可以运行工程代码。但通过 Docker 运行容器呈现出的内容并非图形化的，都是以命令行形式在终端上展示、交互，调试代码时很不方便。那么是否能用 IDE 连接容器中的 Python 解释器，在图形化界面里调试代码呢？

巧的是 Pycharm 的确提供这个功能，在选择项目的解释器时的确可以选择 Docker，不巧的是在 Pycharm 的工作逻辑中，该配置项<dot>只能选择镜像，而不能选择容器</dot>。点击运行代码后，Pycharm 先用所选择的镜像构建一个临时容器，再用该容器中的解释器来运行代码。

运行 Docker 容器更为通用的方法是使用 `docker run` 命令，该命令还可以接收很多其他复杂的参数，例如通过 `docker run --gpus all` 挂载 GPU 等。Pycharm 略过这个配置项就导致生成的容器存在多多少少的问题，例如无法调用 GPU、没有挂载硬盘等等。

那么是否有通过 IDE 使用容器中的解释器调试代码的方法呢？有的，那就是<dot>不使用 Pycharm，而使用 JetBrains Gateway 连接解释器</dot>。虽说有些标题党，但 Gateway 与 Pycharm 毕竟是同一家公司的产品，且 Gateway 集成了 Pycharm 的 IDE，完成能达到使用要求。尽管 Gateway 还在 Beta 版本，我试用了很久仍觉得十分好用，我认为这大概是最「优雅」的 Docker 环境使用方式。

在宿主机上安装 Gateway 后，通过 SSH 连接到容器内，Gateway 会在容器中下载后台程序。宿主机上的操作都会经由 SSH 通过后台在容器中执行，所产生的反馈也由 SSH 传达并渲染到宿主机的界面上。所以使用 Gateway 调试、运行容器中代码的感觉就几乎和在本地一样，尽管无声的来去之间已经在 SSH 上交换了无数数据。如果能通过 SSH 连接远程服务器，同样也可以使用 Gateway 调试，十分便捷。

下文就以 Mindspore 为例，介绍在 Linux 上配置 Docker 容器的 SSH 服务并使用 Gateway 连接容器中解释器的方法。Mindspore 是相当麻烦的 AI 框架，如果 Mindspore 都能装上，相信 Pytorch 和 TensorFlow 之类用户友好的框架就完全不成问题了。

## 安装 JetBrains Gateway

在 [JetBrains Gateway 官网](https://www.jetbrains.com/remote-development/gateway/)下载压缩包，解压后挪到 `/opt` 目录下，在终端中可以用 `/opt/Gateway/bin/gateway.sh` 启动。

```sh
# 在官网上可以找到最新版的下载链接
$ wget https://download.jetbrains.com/idea/gateway/JetBrainsGateway-2023.2.tar.gz?_gl=1*1b4kr34*_ga*MTkzNDYxNzI1MS4xNjc2Njg1NzQx*_ga_9J976DJZ68*MTY5MTE0NTQwMy4yMC4xLjE2OTExNDc2NzkuNTguMC4w -O Gateway.tar.gz
$ tar -zxvf Gateway.tar.gz
$ sudo mv -f JetBrainsGateway-232.8660.185 /opt/Gateway
```

亦可以通过 Gateway 的欢迎界面创建桌面图标：

![!创建图标](https://storage.live.com/items/4D18B16B8E0B1EDB!9928?authkey=ALYpzW-ZQ_VBXTU)

## 配置容器 SSH

#### 拉取镜像

```sh
# 从 Docker Hub 上拉取需要的镜像（Ubuntu X86）
$ docker pull mindspore/mindspore-gpu-11.6:2.0.0-alpha
```

#### 构建镜像

在空文件夹中新建 Dockerfile 文件，内容如下：

```docker
# 使用前一步骤拉取的镜像作为基础镜像
FROM mindspore/mindspore-gpu-cuda11.6:2.0.0-alpha

# 切换到 root 用户
USER root

# 设置 root 用户密码为 12345（连接 SSH 时使用）
RUN echo "root:12345"|chpasswd

# 安装 vim supervisor openssh-server
RUN apt-get update && \
    apt-get install -y vim supervisor openssh-server

# 修改 SSH 设置，允许使用 root 用户连接
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# 设置 supervisor，将 SSH 作为其子进程，用 supervisor 管理 SSH 服务
RUN echo -e \
"[supervisord]\n\
nodaemon=true\n\
\n\
[program:sshd]\n\
command=/usr/sbin/sshd -D\n\
autostart=true\n\
autorestart=true\n\
startsecs=3\n" > /etc/supervisor/conf.d/sshd.conf

# 在 Ubuntu 需要创建该文件夹
RUN mkdir -p /var/run/sshd

# 将 /usr/bin/supervisord -c /etc/supervisor/supervisord.conf 命令作为容器启动的入口，即让 supervisor 启动 SSH
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
```

{warn begin}在 Ubuntu 系统下，使用 `/usr/sbin/sshd -D` 命令启动 SSH 服务会出现错误，提示找不到文件夹 `Missing privilege separation directory: /var/run/sshd`，我检索到的解决方法是用 `mkdir -p /var/run/sshd` 创建该文件夹，所以在 Dockerfile 中加上了这行命令。我不确定其他系统是否有这个错误，文末附上了关于这个错误的两个链接。{warn end}

用终端进入 Dockerfile 所在文件夹，用下列命令构建镜像：

```sh
$ docker build -t ms:200a-cu116 .
```

完成后使用 `docker image ls` 就能看到构建的镜像：

```sh
$ docker image ls
REPOSITORY                         TAG                 IMAGE ID            CREATED             SIZE
ms                                 200a-cu116          f9029d1ecae2        5 seconds ago       10.7 GB
mindspore/mindspore-gpu-cuda11.6   2.0.0-alpha         01db14982624        6 months ago        10.5 GB
```

## 连接容器解释器

```sh
$ docker run -d -p 2222:22 -v /dev/shm:/dev/shm -v /home/code:/home/code --name=work --runtime=nvidia ms:200a-cu116
```

- `-d` 参数使容器在后台运行，不打开终端；
- `-p 2222:22` 参数令容器的 `22` 端口（默认的 SSH 端口）映射到宿主机的 `2222` 端口；
- `-v` 参数是将本地的硬盘路径挂载到容器中，其中 `-v /dev/shm:/dev/shm` 是 Mindspore 的要求，`-v /home/code:/home/code` 则是将工程文件挂载到容器里，这两个目录双向同步；
- `--runtime=nvidia` 参数使容器能够使用宿主机的 GPU 硬件。

{info begin}有时运行调用 GPU 资源的容器会遇到问题，提示 `Error response from daemon: Unknown runtime specified nvidia`。而我则是更换了内核和驱动版本后，尝试重启容器时出现了类似的错误，提示 `Error response from daemon: Cannot restart container or invalid runtime name: nvdia`，暂时还不确定原因。在 [GitHub](https://github.com/NVIDIA/nvidia-docker/issues/838) 上有关于该问题的讨论，其中的方法都可以尝试一下，将 `--runtime=nvidia` 参数替换为 `--gpus all` 普遍可以解决问题。{info end}

容器运行后可以在终端尝试用 SSH 连接容器，输入 `yes` 再输入用户密码（前文 Dockerfile 中设置为 `12345`）后若能成功连接就表示 SSH 服务正常。

```sh
$ ssh root@127.0.0.1 -p 2222
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
```

还可以在连接上的终端中输入 `nvidia-smi` 检查容器是否连接上 GPU 硬件。

如果在这一步中，没有显示 SSH 成功连接的提示，多半是因为容器中的 SSH 服务没有成功启动。用 `docker exec -it work /bin/bash` 进入容器的交互界面，用 `service ssh status` 检查服务是否已经启动。

![!登录](https://storage.live.com/items/4D18B16B8E0B1EDB!9929?authkey=ALYpzW-ZQ_VBXTU)

确保容器一切正常后，打开 Gateway，选择 `New Connection`，输入用户名、IP 地址和端口号，选择 `Check Connection and Continue`，Gateway 使用 SHH 成功连接后就可以选择需要的 IDE。

![!选择 IDE](https://storage.live.com/items/4D18B16B8E0B1EDB!9930?authkey=ALYpzW-ZQ_VBXTU)

不知道为什么 Linux 上可选择的 IDE 这么少，好在可以通过从官网手动下载安装包的方式安装。例如[下载 Pycharm](https://www.jetbrains.com/pycharm/download/?section=linux) 的安装包后，选择 `Installation options` - `Upload installer file`，Gateway 就会在远端（容器中）安装指定的 IDE。

{warn begin}目前 Gateway 的远端只支持 Linux 系统，所以下载的 IDE 安装包也应为 Linux 版本，这与上文构建的 Linux 镜像匹配。{warn end}

![!解释器](https://storage.live.com/items/4D18B16B8E0B1EDB!9931?authkey=ALYpzW-ZQ_VBXTU)

进入 IDE 后需要选择 Python 解释器，注意此时 Gateway 已经连接到容器，local 指的也是容器内，所以要选择的解释器正是本地解释器。Gateway 检测到的 Python 路径可能不正确，需要额外确认一下。在 Docker 中一般直接使用系统的 Python，不需要使用 Anaconda 一类的虚拟环境，可以通过以下命设查找系统 Python 路径：

```sh
$ which python
/usr/local/bin/python
```

一切设置都正确的话，Gateway 就能读取到 Python 中的包了，此时无论运行还是调试代码，所使用的也都是容器中的 Python。在 Gateway 中打开终端，进入的也是容器中的终端，在终端中检查 Mindspore 是否成功安装：

```sh
$ python -c "import mindspore;mindspore.set_context(device_target='GPU');mindspore.run_check()"
MindSpore version: 2.0.0a0
The result of multiplication calculation is correct, MindSpore has been installed successfully!
```

输出上述信息即表示在 GPU 平台上成功安装 Mindspore。

## 容器的关闭与重启

创建容器时指定了 `-d` 参数，容器只在后台运行，一般也不需要关闭。如果需要开关容器，以下列出一些常用的 Docker 命令：

```sh
# 列出所有容器，可以查询容器的运行状态、名称和 ID 等信息
$ docker ps -a

# 关闭指定容器，停止容器中的进程，内容不会消失
$ docker stop {容器名称或 ID}

# 重启容器，例如创建容器时已经指定了运行参数 -d，重启的容器同样在后台运行
$ docker restart {容器名称或 ID}

# 删除容器，若删除失败需要确定容易是否在运行
$ docker rm {容器名称或 ID}
```
---

## References

- [用 ssh 连接 docker 容器 - 博客园](https://www.cnblogs.com/jesse131/p/13543308.html)
- [安装使用 supervisor 来启动服务 - 博客园](https://www.cnblogs.com/laolieren/p/launch_service_with_supervisor.html)
- [如何让操作系统为 ubuntu 的 docker 容器在启动时自动重启 sshd 服务? - 知乎](https://www.zhihu.com/question/436422410/answer/1647611960)
- [Bug #45234 “Missing privilege separation directory: /var/run/ssh...” - Launchpad](https://bugs.launchpad.net/ubuntu/+source/openssh/+bug/45234)
- [Missing privilege separation directory: /var/run/sshd - GitHub](https://github.com/ansible/ansible-container/issues/141)