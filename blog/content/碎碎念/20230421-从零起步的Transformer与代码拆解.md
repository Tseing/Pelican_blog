title: 从零起步的 Transformer 与代码拆解
slug: transformer-from-scratch
date: 2023-04-21
tags: Python, PyTorch, Transformer

自 Google 的论文 [Attention Is All You Need](https://arxiv.org/abs/1706.03762) 发布后，几年内涌现了大量基于 Transformer 的模型，俨然形成了 Transformer 横扫人工智能领域的态势。

网络上也出现了大量解读论文或是讲解 Transformer 的文章，其中也不乏许多高水平人工智能从业者的解读。虽然有些可以称得上是高屋建瓴，但相当大部分难以避免地落入了知识的诅咒（curse of knowledge），起码在我初开始了解 Transformer 时难以读懂这些文章。

随着 Transformer 广泛应用到各领域，学习 Transformer 也成了一门「显学」。尽管我已经能读懂一些更深层次的 Transformer 剖析，但我还是未找见一篇合我心意的入门文章，所以我希望能撰写一篇小文章，以初学者的角度来讲解 Transformer，是为序。

## 楔子

Transformer 是设计用于 NLP 的一种模型，尽管目前 Transformer 所能完成的任务已经大大扩展，但这里还是以最原始的翻译任务为例。

在翻译任务中，所需要的数据包括原始语句与目标语句，也就是 Transformer 原论文中所指的「input」和「output」，因为名字太容易混淆，还是将其原始语句与目标语句或是「source」与「target」。

假设 source 为 `你好，世界！`，target 为 `Hello, world!`，完成这个中译英任务首先要将文本转化为利于模型处理的数值，这一步称为词嵌入（embedding）。

常见的词嵌入方法有 word2vec 等等，在这里不做介绍。词嵌入步骤大致的流程是先将 `你好，世界！` 转化为 `<start> 你好 ， 世界 ！ <end>`，每个「词」都用空格划分开，其中 `<start>` 与 `<end>` 分别表示文本的起讫，这些「词」在 NLP 通常称为「token」。接着再为每个 token 分配索引，例如 `<start>` 为 `1`，`<end>`为 `0`，照这个思路，文本就可以转换为 `[1 2 3 4 5 0]` 的表示。当然这是很简单的做法，实际上，每个 token 都会被转化为指定维度的向量，用这一连串向量就可以表示文本。

将上述过程抽象出来，在词嵌入后，可以得到 source 的表示 $\boldsymbol{X}=(\boldsymbol{x}_1,\boldsymbol{x}_2,\cdots,\boldsymbol{x}_t)$ 与 target 的表示 $\boldsymbol{Y}=(\boldsymbol{y}_1,\boldsymbol{y}_2,\cdots,\boldsymbol{y}_t)$，其中 $\boldsymbol{x}_i$ 与 $\boldsymbol{y}_i$ 都是指定维度 $d$ 的向量。

那么如何使用 $\boldsymbol{X}$ 与 $\boldsymbol{Y}$ 完成翻译任务呢？

**第一种**是使用 RNN 方法，使用当前的 source token $\boldsymbol{x}_t$ 与前一步中生成的 token $\hat{\boldsymbol{y}}_{t-1}$ 生成下一个 token，逐个生成直至句子末尾：

$$\hat{\boldsymbol{y}}_t=f(\hat{\boldsymbol{y}}_{t-1},\boldsymbol{x}_t)$$

**第二种**是使用卷积的方法，定义一个窗口长度再通过小范围中的几个 $\boldsymbol{x}_i$ 计算输出：

$$\hat{\boldsymbol{y}}_t=f(\boldsymbol{x}_{t-1},\boldsymbol{x}_t,\boldsymbol{x}_{t+1})$$

可以看出，<dot>RNN 很难学习到全局的信息</dot>，而<dot>卷积方法只能学习到小范围的局部信息</dot>。

所以 Transformer 给出了**第三种**方法，也就是自注意力方法。自注意力机制让模型就当前的 source token $\boldsymbol{x}_t$ 与 $\boldsymbol{X}$ 中其他 token 的关系给出输出 $\hat{\boldsymbol{y}}_t$：

$$\hat{\boldsymbol{y}}_t=f(\boldsymbol{x}_t, \boldsymbol{X})$$

## Transformer 结构

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!7721?authkey=ALYpzW-ZQ_VBXTU)

标准 Transformer 的结构如上图所示，大致分为左侧的 Encoder 与右侧的 Decoder 两个部分。Inputs 与 Outputs 分别是上文所说的 source 与 target，Output Probabilities 是模型输出的各 token 概率，取其中最大概率的 token 就能组织成模型输出结果。

### 位置编码

Transformer 并没有采用 RNN 与卷积方法所使用的序列处理 token 的方法，因而能够实现并行计算并且很大程度上缓解了长期依赖问题（顺序处理长序列容易丢失多个步骤前的信息）。文本中多个 token 间显然有前后的顺序关系，Transformer 使用位置编码的方式来处理顺序信息。

source 与 target 送入模型，经过常规的词嵌入过程后，还需要在得到的矩阵上加上位置编码，论文将位置编码定义为

$$\mathrm{PE}_{(\mathrm{pos},2i)}=\sin(\mathrm{pos}/10000^{2i/d_\mathrm{model}})$$

$$\mathrm{PE}_{(\mathrm{pos},2i+1)}=\cos(\mathrm{pos}/10000^{2i/d_\mathrm{model}})$$

Transformer 将 $\mathrm{pos}$ 位置映射为 $d_\mathrm{model}$ 维的向量，向量中的第 $i$ 个元素即按上式计算。位置编码的计算公式是构造出的经验公式，不必深究，当然也有许多文章分析了如此构造的原因，这里从略。

### Encoder 与 Decoder

许多完成 seq2seq 任务的模型都采用了 encoder-decoder 模式，Transformer 也不例外。简单来说，encoder 将输入编码得到一个中间变量，decoder 解码该中间变量得到输出。

在 Transformer 中，source 与 target 分别送入 encoder 与 decoder，encoder 计算得到的中间结果再送入 decoder 中与 target 输入进行计算，得到最后的结果，这就是所谓「编码-解码」的工作方式。

从 Transformer 的结构图中可以看出，模型具有 $N$ 层 encoder 与 decoder 层。其中，encoder 与 decoder 都具有相同的多头注意力层（Multi-Head Attention）、前馈层（Feed Forward）。encoder 与 decoder 的不同在于 decoder 多了一个多头注意力层，在这一层中，encoder 的输出与 decoder 的输入计算注意力。

还可以注意到，在 encoder 与 decoder 中，每一层后都有一个 Add & Norm 层，用于归一化计算结果。Add & Norm 层的计算方式是将前一层的输入与前一层的输出相加，然后归一化，可以表示为 $\mathrm{LayerNorm}(\boldsymbol{x}+\mathrm{Sublayer}(\boldsymbol{x}))$。

#### Attention 机制

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8803?authkey=ALYpzW-ZQ_VBXTU)

数据进入 encoder 与 decoder 的内部，首先要通过注意力机制进行计算，这也是 Transformer 的核心。

文章中将所使用的注意力称为缩放点积注意力（scaled dot-product attention），定义为

$$\mathrm{Attention}(\boldsymbol{Q},\boldsymbol{K},\boldsymbol{V}) = \mathrm{Softmax}\left(\frac{\boldsymbol{Q}\boldsymbol{K}^\top}{\sqrt{d_k}}\right)\boldsymbol{V}$$

其中 $\boldsymbol{Q}_{n\times d_k}$、$\boldsymbol{K}_{m\times d_k}$、$\boldsymbol{V}_{m\times d_v}$ 分别是若干向量 $\boldsymbol{q}\in\mathbb{R}^{d_k}$、$\boldsymbol{k}\in\mathbb{R}^{d_k}$、$\boldsymbol{v}\in\mathbb{R}^{d_v}$ 组成的矩阵。

单看矩阵的乘法稍显复杂，不妨先用向量说明计算步骤。通过以下方式可以从输入 $\boldsymbol{x}$ 得到向量 $\boldsymbol{q}$、$\boldsymbol{k}$、$\boldsymbol{v}$：

$$\boldsymbol{q}=\boldsymbol{x}\boldsymbol{W}^Q,\,\boldsymbol{k}=\boldsymbol{x}\boldsymbol{W}^K,\,\boldsymbol{v}=\boldsymbol{x}\boldsymbol{W}^V$$

其中，$\boldsymbol{W}^Q$、$\boldsymbol{W}^K$、$\boldsymbol{W}^V$ 分别表示相应的权重矩阵。$\boldsymbol{q}$ 代表 query，$\boldsymbol{k}$ 代表 key，$\boldsymbol{v}$ 代表 value，目的是<dot>用 query 去寻找更匹配的 key-value 对</dot>。

因为数量积可以表示两向量的相似程度，一种简单的做法是使用 $\boldsymbol{q}$ 与若干个 $\boldsymbol{k}$ 计算数量积，将其作为匹配分数：

$$\mathrm{score}=\boldsymbol{q}\cdot \boldsymbol{k}_i=\boldsymbol{q}\boldsymbol{k}^\top_i$$

但这样的「注意力」太过于简单，Google 从上述的数量积出发，设计了更为可靠的注意力：

$$\mathrm{Attention}(\boldsymbol{q},\boldsymbol{k}_i,\boldsymbol{v}_i)=\frac 1 Z\sum_i\exp\left(\frac{\boldsymbol{q}\boldsymbol{k}^\top_i}{\sqrt{d_k}}\right)\boldsymbol{v}_i$$

首先，式中 $1/Z\sum_i x_i$ 形式的部分是 Softmax 函数的简写，Softmax 函数由下式定义：

$$\mathrm{Softmax}(x_i)=\frac{\exp(x_i)}{\sum_j\exp(x_j)}$$

Softmax 函数的作用是将若干数值 $x_i$ 归一化，得到的 $\mathrm{Softmax}(x_i)$ 具有

- $\sum_i\mathrm{Softmax}(x_i)=1$
- $\mathrm{Softmax}(x_i)\in[0, 1]$

两点性质，所以与概率具有相似的特征，可以用作概率处理。

其次，式中新增的 $\sqrt{d_k}$ 用于调节内积 $\boldsymbol{q}\boldsymbol{k}^\top_i$ 的大小。当若干内积的大小过于悬殊时，Softmax 函数很容易将其推向 $0$ 或 $1$ 的边界值，这样的数值处理起来没什么意义。

最后，再次回忆 Transformer 的注意力机制是用 query 去寻找更匹配的 key-value 对。那么上式的意义就很了然了，就是将 query 与各个 key 的匹配分数转化为各个概率，再按各个概率取各个 key 所对应的 value，组合各 value 分量即得到注意力。

以具有两个 value 的情况为例，需要得到的中间量 $\boldsymbol{z}$（理解为注意力亦可）可以通过下式计算：

$$\begin{align}
    \boldsymbol{z}_1=\theta_{11}\boldsymbol{v}_1+\theta_{12}\boldsymbol{v}_2\\
    \boldsymbol{z}_2=\theta_{21}\boldsymbol{v}_1+\theta_{22}\boldsymbol{v}_2
\end{align}$$

权值 $\theta_{ij}$（即上文所说概率）通过下式得到：

$$\theta_{ij}=\mathrm{Softmax}\left(\frac{\boldsymbol{q}_i\boldsymbol{k}^\top_j}{\sqrt{d_k}}\right)$$

将上述运算转为矩阵形式会简洁许多：

$$
\begin{pmatrix}
    \boldsymbol{z}_1 \\
    \boldsymbol{z}_2
\end{pmatrix}=
\begin{pmatrix}
    \theta_{11} & \theta_{12} \\
    \theta_{21} & \theta_{22}
\end{pmatrix}
\begin{pmatrix}
    \boldsymbol{v}_1 \\
    \boldsymbol{v}_2
\end{pmatrix}\\
$$

可以记作 $\boldsymbol{Z}=\boldsymbol{\theta}\boldsymbol{V}$，也就是

$$\mathrm{Attention}(\boldsymbol{Q},\boldsymbol{K},\boldsymbol{V}) = \mathrm{Softmax}\left(\frac{\boldsymbol{Q}\boldsymbol{K}^\top}{\sqrt{d_k}}\right)\boldsymbol{V}$$

#### Multi-Head Attention

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8803?authkey=ALYpzW-ZQ_VBXTU)

前一节中解释了 Transformer 中的缩放点积注意力，但在模型中实际并非通过上述方式直接计算，而是通过多头注意力的方式计算注意力。

如上图所示，多头注意力同样是在计算缩放点积注意力，但与纯粹缩放点积注意力的不同之处在于多头注意力将多个注意力计算步骤叠加了起来。

叠加的次数为 $h$，即代表 head，多少个 head 表示需要进行多少次叠加计算。矩阵 $\boldsymbol{Q}$、$\boldsymbol{K}$、$\boldsymbol{V}$ 进入多头注意力计算步骤后，首先要分别在第 $i$ 个 head 中进行线性变换并计算注意力：

$$\mathrm{head}_i=\mathrm{Attention}(\boldsymbol{Q}\boldsymbol{W}^Q_i,\boldsymbol{K}\boldsymbol{W}^K_i,\boldsymbol{V}\boldsymbol{W}^V_i)$$

其中 $\boldsymbol{W}^Q_i\in\mathbb{R}^{d_\mathrm{model}\times d_k}$，$\boldsymbol{W}^K_i\in\mathbb{R}^{d_\mathrm{model}\times d_k}$，$\boldsymbol{W}^V_i\in\mathbb{R}^{d_\mathrm{model}\times d_v}$，注意不同 head 中的线性变换并不同，输出也不同。然后将所有输出 $\mathrm{head}_i$ 拼合在一起，经线性变换后作为注意力：

$$\mathrm{MultiHead}(\boldsymbol{Q},\boldsymbol{K},\boldsymbol{V})=\mathrm{Concat}(\mathrm{head}_1,\mathrm{head}_2,\cdots,\mathrm{head}_h)\boldsymbol{W}^O$$

其中 $\boldsymbol{W}^O\in\mathbb{R}^{hd_v\times d_\mathrm{model}}$。

注意这个过程中数据维数的变化 $d_\mathrm{model}$ 为单头注意力中模型所处理的维数，$\boldsymbol{W}^Q_i$，$\boldsymbol{W}^K_i$，$\boldsymbol{W}^V_i$ 的线性变换将 query、key 的维数从 $d_\mathrm{model}$ 提升到 $d_v$，将 value 的维数从 $d_\mathrm{model}$ 提升至 $d_v$。最后的 $\boldsymbol{W}^O$ 又将拼合起来维数为 $hd_v$ 的注意力转换为模型所处理的维数 $d_\mathrm{model}$。这些线性变换矩阵 $\boldsymbol{W}_i$ 实际上就是模型训练过程中需要学习的一部分参数。

至于为什么要用多头的方式计算注意力，这就是个很复杂的问题了。就我的理解而言，由于每个 head 中的线性变换矩阵 $\boldsymbol{W}_i$，多头注意力实际上是将 query、key、value 映射到不同的子空间中，在多个不同的子空间中寻找与 query 最匹配的 key-value。由于不同子空间中具有不同方面的信息，最后将其拼接起来作为结果，这样可以更多地从多个方面捕获数据中的信息。

#### Feed-Forward 层

在多头注意力层之后，就是前馈层，前馈层只在位置方向上计算，所以原文描述其为 position-wise。进入前馈层的数据在该层中先做 1 次线性变换，维度升高，再经过 RELU 激活函数，最后再做 1 次线性变换，维度降低，输入与输出前馈层的维度相同。上述过程可以表示为

$$\mathrm{FFN}(\boldsymbol{x})=\max(0,\boldsymbol{x}\boldsymbol{W}_1+b_1)\boldsymbol{W}_2+b_2$$

RELU 激活函数定义为

$$\mathrm{ReLU}(x)=x^+=\max(0,x)$$

即式中的 $\max$，按原文中的例子，$\boldsymbol{W}_1$ 使 $\boldsymbol{x}$ 由 512 维升高到 2048 维，$\boldsymbol{W}_2$ 使 $\boldsymbol{x}$ 计算由 2048 维再降至 512 维，升维与降维的过程也是为了更好地获得数据中的信息。

### Transformer 计算步骤

Transformer 模型大致就由上述的几个层连接在一起构成，但或许还是觉得朦朦胧胧，比如究竟什么才是 query、key、value 等等。不妨再来看看 Transformer 的结构图，这一次已熟知大部分模块的工作原理了，所以只看数据流入与流出各模块的路线。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!7721?authkey=ALYpzW-ZQ_VBXTU)

作为 source 的 $\boldsymbol{X}$ 与作为 target 的 $\boldsymbol{Y}$ 分别从下方的左右两侧进入模型。$\boldsymbol{X}$ 与 $\boldsymbol{Y}$ 都要经过词嵌入并加上位置编码，按以下方式更新：

$$
\begin{align}
    \boldsymbol{X}&\leftarrow\mathrm{Embedding}(\boldsymbol{X})+\mathrm{PE}(\boldsymbol{X})\\
    \boldsymbol{Y}&\leftarrow\mathrm{Embedding}(\boldsymbol{Y})+\mathrm{PE}(\boldsymbol{Y})
\end{align}
$$

接着 $\boldsymbol{X}$ 与 $\boldsymbol{Y}$ 分别进入 encoder 与 decoder，可以注意到数据分作 4 条路线，这意味着将数据复制 4 次。先看进入多头注意力层的 3 条数据，以 encoder 为例，在这一层中就是在计算

$$\mathrm{Attention}(\boldsymbol{X},\boldsymbol{X},\boldsymbol{X})$$

不言自明，在这里的 query、key、value 三者都是 $\boldsymbol{X}$，是在 $\boldsymbol{X}$ 内部计算注意力，因此称其为**自注意力**（self-attention）。

在后续的 Add & Norm 层中，计算

$$\boldsymbol{X}\leftarrow\mathrm{LayerNorm}(\boldsymbol{X}+\mathrm{Attention}(\boldsymbol{X},\boldsymbol{X},\boldsymbol{X}))$$

在前馈层与后续的 Add & Norm 层输的输出结果也可想而知：

$$\boldsymbol{X}\leftarrow\mathrm{LayerNorm}(\boldsymbol{X}+\max(0,\boldsymbol{X}\boldsymbol{W}_1+b_1)\boldsymbol{W}_2+b_2)$$

这里的 $\boldsymbol{X}$ 分作两路进入到 decoder 中，在 decoder 的该多头注意力层中，query 与 key 为 $\boldsymbol{X}$，而 value 为类似步骤得到的 $\boldsymbol{Y}$，该层的输出为

$$\boldsymbol{Z}=\mathrm{Attention}(\boldsymbol{X},\boldsymbol{X},\boldsymbol{Y})$$

这也是 decoder 与 encoder 的关键不同。输出结果 $\boldsymbol{Z}$ 完成后续的计算过程后，就得到各 token 的概率，用各 token 替换即可得到模型输出的文本结果。

{note begin}有兴趣的读者不妨根据各矩阵的形状尝试计算一下各个变量的维度在 Transformer 在各步骤中是如何变化的，一定会对 Transformer 的计算过程收获更深的了解。{note end}

## 代码拆解

有了对 Transformer 原理的基本认识，就可以动手实现一个 Transformer 了，通过代码更深入了解 Transformer 的一些细节。这里使用 PyTorch 搭建一个标准的 Transformer，参考代码见 [<i class="fa fa-github"></i> aladdinpersson / Machine-Learning-Collection ](https://github.com/aladdinpersson/Machine-Learning-Collection/blob/master/ML/Pytorch/more_advanced/transformer_from_scratch/transformer_from_scratch.py)。

代码中的各模块如下图所示，接下来对各模块逐个拆解。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8825?authkey=ALYpzW-ZQ_VBXTU)

### PositionEmbedding

```py
import math
import torch
import torch.nn as nn


class PositionEmbedding(nn.Module):
    def __init__(self, d_model, max_len=1000):
        # d_model 为模型处理数据的维数，即公式中 d_k
        # max_len 表示模型处理的最大 token 数量
        super(PositionEmbedding, self).__init__()

        # 生成大小为 max_len * d_model 的零矩阵
        pe = torch.zeros(max_len, d_model)
        # 生成大小为 max_len * 1 的位置矩阵
        position = torch.arange(max_len).unsqueeze(1)
        # 计算位置编码
        div_term = torch.exp(torch.arange(0, d_model, 2) * - (math.log(10000.0) / d_model))
        x = position * div_term
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = self.pe[:, :x.size(1)]
        return x
```

首先实现位置编码模块。在 PyTorch 中，用于搭建神经网络的模块都要继承 `nn.Module`，PyTorch 会通过 `__call__()` 调用模块的 `forward()` 的方法进行前向传播。简单来讲就是，`PositionEmbedding(x)` 的功能等同于 `PositionEmbedding.forward(x)`，但不能使用 `PositionEmbedding.forward(x)`，因为 PyTorch 做了许多条件的判定和优化。

`torch.arange(num)` 的功能类似于 Python 中的 `range(num)`，用于生成文本各 token 的顺序位置索引。`unsqueeze(dim)` 会令 Tensor 在指定的维度 `dim` 上扩张 1 维，这里是为了使 `pe` 与 `position` 两个矩阵的维度对齐，例如：

```python-repl
>>> torch.arange(5)
tensor([0, 1, 2, 3, 4])
>>> torch.arange(5).unsqueeze(0)
tensor([[0, 1, 2, 3, 4]])
>>> torch.arange(5).unsqueeze(1)
tensor([[0],
        [1],
        [2],
        [3],
        [4]])
>>> torch.arange(5).size()
torch.Size([5])
>>> torch.arange(5).unsqueeze(0).size()
torch.Size([1, 5])
>>> torch.arange(5).unsqueeze(1).size()
torch.Size([5, 1])
```

代码中的位置编码并不是直接按公式计算的，而是做了一些变换，先计算一个中间量 `div_term`，其中 `torch.arange(0, d_model, 2)` 即为 $2i$，可以整理出

$$\begin{align}
    \mathrm{div\_term}_i&=\exp\left[2i\times(-\frac{\ln10000}{d_k})\right]\\
    &=\left[\exp(-\frac{\ln10000}{d_k})\right]^{2i}\\
    &=\left[10000^{-\frac{1}{d_k}}\right]^{2i}\\
    &=10000^{-2i/d_k}
\end{align}
$$

所以 `position * div_term` 就可以得到

$$\mathrm{position}\times \mathrm{div\_term}_i=\mathrm{pos}/10000^{2i/d_k}$$

就是位置编码中的一项。

`pe[:, 0::2]` 与 `pe[:, 1::2]` 是 Pytorch 中的高级索引操作。索引中用 `,` 分隔不同维度，例中以 `,` 为分界，前面是对第 1 维的索引，后面是对第 2 维的索引。索引操作也遵守 Python 的规则，即 `a:b:c` 中 `a` 为起始，`b` 为末尾，`c` 为步长。

所以 `pe[:, 0::2]` 与 `pe[:, 1::2]` 取出全部第 1 维中的元素，即行方向上不操作，再在第 2 维中分别从 `0` 或 `1` 开始以步长 `2` 取出元素，即取出第 $2i$ 或第 $2i+1$ 列。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8811?authkey=ALYpzW-ZQ_VBXTU)

在 `forward()` 部分，输出的位置编码为 `pe[:, :x.size(1)]`，这主要是为了确保矩阵形状在加法过程中不会因非法输入的广播而改变。其实在输入合法的情况下，`x.size(1)` 就是 `d_model`，等价于 `pe[:, :]`，也等价于 `pe`。

<!-- 指定 `requires_grad_(False)` 是因为 PyTorch 会自动保存 Tensor 的来源，用于更快地计算梯度，而这里的加法计算并不是训练过程，取消保存能节省一部分资源。 -->

### SelfAttention

在进入 Transformer 核心部分之前，我们需要再次明确一下输入模型的数据格式。上文中仅以输入模型一条数据（由若干 token 组成的一条句子）为例，在实际操作中，为了提高训练效率，会同时输入若干条数据，在构建模型时也要考虑到这一点。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8810?authkey=ALYpzW-ZQ_VBXTU)

如上图所示，一次输入模型的数据条数就称为 batch size，所以模型所处理的其实是一个 $\mathrm{batch\_size}\times\mathrm{max\_len}\times\mathrm{d\_model}$ 的高维矩阵。也就是说，`x.size()` 的结果是 `[batch_size, max_len, d_model]`，务必注意三者顺序。

```py
class SelfAttention(nn.Module):
    def __init__(self, embed_size, heads):
        super(SelfAttention, self).__init__()
        self.embed_size = embed_size
        self.heads = heads
        self.head_dim = embed_size // heads
        # 确保 embed_size 能被 heads 整除
        assert (
            self.head_dim * heads == embed_size
        ), "Embedding size needs to be divisible by heads"

        self.values = nn.Linear(embed_size, embed_size)
        self.keys = nn.Linear(embed_size, embed_size)
        self.queries = nn.Linear(embed_size, embed_size)
        self.fc_out = nn.Linear(embed_size, embed_size)
```

先看 `SelfAttention` 的初始化部分，明白了注意力机制的计算过程就不难理解上面的各个属性了。`head_dim` 是每一个 head 中注意力的维度，`embeds_size` 必须能被 `heads` 整除，否则将多头注意力拼接在一起的维数不等于模型处理的维数就会出现问题。

`values`、`keys`、`queries` 都是计算多头注意力前的线性变换，`fc_out` 是拼接多头注意力后的线性变换。线性变换可以直接调用 `nn.Linear(in_dim, out_dim)`，只需要指定线性变换前后的维数即可，这里线性变换前后维数没有变化。

可能会有读者疑惑为什么这里所设定的线性变换不改变维数，原文中所描述的步骤不是应该将 $d_\mathrm{model}$ 升至 $d_v$ 再计算注意力吗？这是正确的，原文中的计算流程确实如此。如下图所示，在线性变换后复制 `h` 份（例中为 2） $\boldsymbol{Q}$，用若干份 $\boldsymbol{Q}$ 分别计算注意力再拼合起来，得到注意力的维数自然就是 `h * d_v` （例中为 2 * 6），再用一个线性变换将其转化回模型所处理的维数 `d_model`（例中为 5）。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8812?authkey=ALYpzW-ZQ_VBXTU)

但代码中优化了一部分比较繁琐的操作，也有其他版本的代码使用了更接近原文的实现方式，如  [<i class="fa fa-github"></i> jadore801120 / attention-is-all-you-need-pytorch ](https://github.com/jadore801120/attention-is-all-you-need-pytorch/blob/master/transformer/SubLayers.py)，流程就如下图所示，勉强称之为「单头注意力变多头注意力」的一种代码实现吧。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8814?authkey=ALYpzW-ZQ_VBXTU)

例中 `d_model` 也就是词嵌入的维数还是 5，`heads` 仍为 2，`d_value` 仍为 6，但模型不再是将 $d_\mathrm{model}$ 升至 $d_v$，而是将 $d_\mathrm{model}$ 直接升至 $hd_v$，然后将 $\boldsymbol{Q}$ 分成 `h` 份，每份分别用于计算并拼接为注意力。与上例相比，本质上其实并无区别，区别仅仅是上例先复制多个矩阵再分别做线性变换，而该例只使用了一个更大的矩阵乘法就完成了上述操作，效率上更优。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8815?authkey=ALYpzW-ZQ_VBXTU)

多头注意力还有一种实现方法，也是这里展示代码所使用的方法。如上图所示，这种方法对词嵌入的维数有要求，在词嵌入的步骤中就将 token 表示为 `d_v * h` 维，这也是前文代码在初始化中使用 `assert` 语句缘由。后续的线性变换不改变维数，计算多头注意力时直接将 `d_v * h` 维切分为 `h` 份作为每个 head 计算的对象。拼接各 head 的注意力后，最后的线性变换也不改变维数。

在我看来，这种方法应该是对前两种方法的简化，三个例子中用于计算多头注意力的 `d_value` 都为 6，计算量相同。第 3 种方法需要更大的 `d_model`，而且计算多头注意力时没有使用到全部的 embedding，虽说效果类似，但总觉有些奇怪。这或许是为了计算上的方便，不用做过多的矩阵变换 🤔

```py
# class SelfAttention(nn.Module):
    def forward(self, values, keys, query, mask):
        # 获取 batch_size
        N = query.shape[0]
        # d_v, d_k, d_q
        value_len, key_len, query_len = values.shape[1], keys.shape[1], query.shape[1]

        # 对 query, key, value 做线性变换
        values = self.values(values)    # (N, value_len, embed_size)
        keys = self.keys(keys)          # (N, key_len, embed_size)
        queries = self.queries(query)   # (N, query_len, embed_size)

        # 将 token 的词嵌入划分为 heads 份
        # d_model = embed_size = d_v * heads
        values = values.reshape(N, value_len, self.heads, self.head_dim)
        keys = keys.reshape(N, key_len, self.heads, self.head_dim)
        queries = queries.reshape(N, query_len, self.heads, self.head_dim)

        # queries: (N, query_len, heads, heads_dim),
        # keys: (N, key_len, heads, heads_dim)
        # energy: (N, heads, query_len, key_len)
        energy = torch.einsum("nqhd,nkhd->nhqk", [queries, keys])

        # 将掩码矩阵中为 0 的对应项设为 -inf，不参与计算
        if mask is not None:
            energy = energy.masked_fill(mask == 0, float("-1e20"))

        # 得到的点积除以 sqrt(d_k) 并用 Softmax 归一化
        # attention: (N, heads, query_len, key_len)
        attention = torch.softmax(energy / (self.embed_size ** (1 / 2)), dim=3)

        # attention: (N, heads, query_len, key_len)
        # values: (N, value_len, heads, heads_dim)
        # out after matrix multiply: (N, query_len, heads, head_dim), then
        # we reshape and flatten the last two dimensions.
        out = torch.einsum("nhql,nlhd->nqhd", [attention, values]).reshape(
            N, query_len, self.heads * self.head_dim
        )

        # 拼接多头注意力后的线性变换
        # out: (N, query_len, embed_size)
        out = self.fc_out(out)

        return out
```

`forward()` 部分描述了上述计算多头重意力的过程。线性变换后，使用 `reshape()` 方法将 Tensor 转化化为指定维度，也就是将词嵌入划分为 `heads` 份的操作，Tensor 的形状由 `[N, query_len, embed_size]` 变为 `[N, query_len, self.heads, self.head_dim]`，把 `embed_size` 拆成 `heads * head_dim`。

接着使用 `torch.einsum()` 得到注意力计算的一个中间量 `energy`。`torch.einsum()` 称为爱因斯坦求和约定，可以非常简洁地进行矩阵乘法、转置待操作，但会有些难以理解。

例如矩阵乘法 $\boldsymbol{A}_{i\times j}\boldsymbol{B}_{j\times k}=\boldsymbol{C}_{i\times k}$，可以表示为 `"ij,jk->ik"`：

```python-repl
>>> A = torch.randn(3, 4)
>>> B = torch.randn(4, 5)
>>> C = torch.einsum("ij,jk->ik", [A, B])
>>> C.size()
torch.Size([3, 5])
```

例如矩阵转置 $(\boldsymbol{A}_{i\times j})^\top=\boldsymbol{B}_{j\times i}$，可以表示为 `"ij->ji"`：

```python-repl
>>> A = torch.randn(3, 4)
>>> B = torch.einsum("ij->ji", [A])
>>> B.size()
torch.Size([4, 3])
```

定义了矩阵乘法的表示后，相应的数量积与向量积就也能表示了，不再赘述。求和操作将矩阵转化为数值，行与列都会消失，所以 $\sum a_{ij}\in\boldsymbol{A}_{i\times j}$ 可以记作 `"ij->"`：

```python-repl
>>> A = torch.randn(3, 4)
>>> torch.einsum("ij->", [A])
tensor(0.5634)
```

此外，爱因斯坦求和约定还可以表示在指定维度上求和、做数量积等一系列的复杂操作，读者可以自行试验。

代码中 `queries` 的形状为 `[N, query_len, heads, heads_dim]`，记作 $\boldsymbol{Q}_{N\times q\times h \times d}$，`keys` 的形状为 `[N, key_len, heads, heads_dim]`，记作 $\boldsymbol{K}_{N\times k\times h \times d}$，那么 `torch.einsum("nqhd,nkhd->nhqk", [queries, keys])` 所做的操作就是：

1. 将 $\boldsymbol{Q}_{N\times q\times h \times d}$ 转置为 $\boldsymbol{Q}_{N\times h \times q\times d}$，将 $\boldsymbol{K}_{N\times k\times h \times d}$ 转置为 $\boldsymbol{K}_{N\times h\times k \times d}$；
2. 两个矩阵中的 $N\times h$ 是 `batch_size` 与 `heads` 的乘积，仅仅是表示数量，所以 $\boldsymbol{K}_{N\times h \times k\times d}$ 可以视作由 $N\times h$ 个 $(\boldsymbol{K}_i)_{\ k\times d}$ 子矩阵构成的大矩阵。那么固定前两维不变，转置后两维，相当于**转置**所有子矩阵，得到 $\boldsymbol{K}_{N\times h \times d\times k}$；
3. 固定前两维，令 $\boldsymbol{Q}_{N\times h \times q\times d}$ 与 $\boldsymbol{K}_{N\times h \times d\times k}$ 在后两维上做乘法，得到 $(\boldsymbol{QK})_{N\times h \times q \times k}$。

仔细思考上述的转置和乘法过程，实际上就是在做多头注意力中的 $\boldsymbol{Q}\boldsymbol{K}^\top$。

掩码部分的操作先略过。接着 `torch.softmax(energy / (self.embed_size ** (1 / 2)), dim=3)` 先将前一步中得到 `energy` 除以 $\sqrt{d_k}$ 再用 Softmax 归一化。指定的 `dim=3` 与 `dim=-1` 等价，其目的是在最后一维的方向上归一化。

以一个简单的 $\boldsymbol{Q}\boldsymbol{K}^\top$ 乘法为例，如下图所示，$\boldsymbol{Q}$ 与 $\boldsymbol{K}$ 的每一行都是一个 token 的词嵌入表示。计算得到 $\boldsymbol{Q}\boldsymbol{K}^\top$ 后需要归一化，`softmax(dim=0)` 是在行方向上归一化，在得到的结果中，全部行加起来，各元素为 1；`softmax(dim=1)` 是在列方向上归一化，结果中的全部列加起来，各元素为 1。

计算注意力还是为了得到更准确的 token 表示，所以归一化的方向应该与原始的 $\boldsymbol{Q}$ 方向相同，即 `softmax(dim=1)`。代码中也是一样，$(\boldsymbol{QK})_{N\times h \times q \times k}$ 是 $N\times h$ 个 $(\boldsymbol{Q}\boldsymbol{K}_i)_{q\times k}$ 子矩阵，要在所有子矩阵的列方向上做归一化，那么就是在第 4 个维度上做 Softmax，即 `softmax(dim=3)`。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8820?authkey=ALYpzW-ZQ_VBXTU)

此时，上述过程已经完成了多头注意力中的 $\mathrm{Softmax}(\boldsymbol{Q}\boldsymbol{K}^\top/\sqrt{d_k})$，将结果记作 $\boldsymbol{A}_{N\times h\times q\times k}$。

在下一步中，用 `"nhql,nlhd->nqhd"` 表示了 $\boldsymbol{A}$ 与 $\boldsymbol{V}$ 的乘法，具体操作是：

1. 将 $\boldsymbol{V}_{N\times v\times h\times d}$ 转置为 $\boldsymbol{V}_{N\times h\times v\times d}$；
2. 固定前两维，令 $\boldsymbol{A}_{N\times h\times q\times k}$ 与 $\boldsymbol{V}_{N\times h\times v\times d}$ 在后两维上做乘法，这里有 $q=k=v$，所以结果为 $(AV)_{N\times h \times q\times d}$，到这一步已经计算了 $\mathrm{Softmax}(\boldsymbol{Q}\boldsymbol{K}^\top/\sqrt{d_k})\boldsymbol{V}$；
3. 将结果转置为 $(AV)_{N\times q \times h\times d}$。

最后代码使用 `reshape()` 合并后两维，将结果转化为 $(AV)_{N\times q \times hd}$，很巧妙地拼接了多个 head 的注意力，最后通过线性层再输出结果。

至此，Transformer 中的 `SelfAttention` 部分已经结束，读者或许会觉得头昏脑胀。不必担心，最为艰涩的一部分已经过去，接下来是一路下坡 🚩

### TransformerBlock

```py
class TransformerBlock(nn.Module):
    def __init__(self, embed_size, heads, dropout, forward_expansion):
        super(TransformerBlock, self).__init__()
        # 前一层的多头注意力
        self.attention = SelfAttention(embed_size, heads)
        # Add & Norm 层
        self.norm1 = nn.LayerNorm(embed_size)
        self.norm2 = nn.LayerNorm(embed_size)
        # 前馈层
        self.feed_forward = nn.Sequential(
            nn.Linear(embed_size, forward_expansion * embed_size),
            nn.ReLU(),
            nn.Linear(forward_expansion * embed_size, embed_size),
        )

        self.dropout = nn.Dropout(dropout)

    def forward(self, value, key, query, mask):
        attention = self.attention(value, key, query, mask)

        x = self.dropout(self.norm1(attention + query))
        forward = self.feed_forward(x)
        out = self.dropout(self.norm2(forward + x))
        return out
```

`TransformerBlock` 模块包括多头注意力与后接的 Add & Norm、Feed Forward、Add & Norm 三层。

初始化部分使用 `nn.Sequential()` 将 `nn.Linear()`、`nn.ReLU()`、`nn.Linear` 依次连接起来形成前馈层，正如前文所说的，数据进入前馈层先升维再激活，最后再降回原来维度，`forward_expansion` 决定升维的倍数。`dropout` 用于随机弃用一部分数据防止过拟合，直接调用 `nn.Dropout()` 类，接收的数值决定了弃用数据的比例。

`forward()` 部分也很简单，计算的多头注意力依次做 Add & Norm、Feed Forward、Add & Norm 三层后输出数据。

### Encoder

```py
class Encoder(nn.Module):
    def __init__(
        self,
        src_vocab_size,
        embed_size,
        num_layers,
        heads,
        device,
        forward_expansion,
        dropout,
        max_length,
    ):

        super(Encoder, self).__init__()
        self.embed_size = embed_size
        # CPU or GPU
        self.device = device
        self.word_embedding = nn.Embedding(src_vocab_size, embed_size)
        self.position_embedding = PositionalEncoding(embed_size, max_length)

        self.layers = nn.ModuleList(
            [
                TransformerBlock(
                    embed_size,
                    heads,
                    dropout=dropout,
                    forward_expansion=forward_expansion,
                )
                for _ in range(num_layers)
            ]
        )

        self.dropout = nn.Dropout(dropout)
```

Encoder 是 Transformer 中的左边部分，Transformer 中有 $N$ 个 `TransformerBlock` 顺序叠放在一起组成 encoder。所以在初始化部分，使用列表推导式在 `layers` 中放置了 `num_layers` 层 `TransformerBlock`。

```py
# class Encoder(nn.Module):
    def forward(self, x, mask):
        # 输入数据的 batch_size 与长度
        N, seq_length = x.shape
        # 从输入数据计算位置索引
        positions = torch.arange(0, seq_length).expand(N, seq_length).to(self.device)
        # 由位置索引得到位置编码，并 dropout 一部分数据
        out = self.dropout(
            (self.word_embedding(x) + self.position_embedding(positions))
        )

        # 让数据逐层经过 encoder，计算自注意力
        for layer in self.layers:
            out = layer(out, out, out, mask)

        return out
```

在 `forward()` 部分中，使用 `torch.arange()` 得到位置索引，再用 `expand()` 方法将位置索引矩阵的形状变为与输入数据相同，`expand()` 方法的主要作用是复制，例如：

```python-repl
>>> torch.arange(0, 5)
tensor([0, 1, 2, 3, 4])
>>> torch.arange(0, 5).expand(2, 5)
tensor([[0, 1, 2, 3, 4],
        [0, 1, 2, 3, 4]])
```

`to()` 方法用于指定 Tensor 存储的设备，例如 `"CPU"` 或 `"GPU"`。将词嵌入加上位置编码得到 `out`，再将 `out` 送入 encoder 中计算结果。

`layer(out, out, out)` 看起来或许有些奇怪，请留意，前文已经讨论过，在 encoder 中计算的是**自注意力**，所以此时的 query、key、value 都是相同的，而在 decoder 中就会有所不同了。

### DecoderBlock

```py
class DecoderBlock(nn.Module):
    def __init__(self, embed_size, heads, forward_expansion, dropout, device):
        super(DecoderBlock, self).__init__()
        self.norm = nn.LayerNorm(embed_size)
        self.attention = SelfAttention(embed_size, heads=heads)
        self.transformer_block = TransformerBlock(
            embed_size, heads, dropout, forward_expansion
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, value, key, src_mask, trg_mask):
        attention = self.attention(x, x, x, trg_mask)
        query = self.dropout(self.norm(attention + x))
        out = self.transformer_block(value, key, query, src_mask)
        return out
```

类似地，Decoder 是 Transformer 结构图中的右侧部分，也是由 $N$ 层 `DecoderBlock` 组成。decoder 只比 encoder 多了一个掩码注意力层，其他结构相同，所以 `DecoderBlock` 的初始化中直接调用了先前定义的 `TransformerBlock`。

`forward()` 中，target 进入 decoder 后，先计算**自注意力**（`attention(x, x, x)`），再经过 Add & Norm 层得到 `query`，再与 encoder 中的结果做多头注意力（`attention(value, key, query)`），输出结果。留意两种注意力计算的不同，参考 Transformer 结构图理解一下就会很明确。

### Decoder

```py
class Decoder(nn.Module):
    def __init__(
        self,
        trg_vocab_size,
        embed_size,
        num_layers,
        heads,
        forward_expansion,
        dropout,
        device,
        max_length,
    ):
        super(Decoder, self).__init__()
        self.device = device
        self.word_embedding = nn.Embedding(trg_vocab_size, embed_size)
        self.position_embedding = PositionEmbedding(embed_size,max_length)

        self.layers = nn.ModuleList(
            [
                DecoderBlock(embed_size, heads, forward_expansion, dropout, device)
                for _ in range(num_layers)
            ]
        )
        self.fc_out = nn.Linear(embed_size, trg_vocab_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, enc_out, src_mask, trg_mask):
        N, seq_length = x.shape
        positions = torch.arange(0, seq_length).expand(N, seq_length).to(self.device)
        x = self.dropout((self.word_embedding(x) + self.position_embedding(positions)))

        for layer in self.layers:
            x = layer(x, enc_out, enc_out, src_mask, trg_mask)

        out = self.fc_out(x)

        return out
```

实现了 `DecoderBlock` 后，`Decoder` 就没有什么内容了，与 encoder 类似，就是将多个 `DecoderBlock` 组装起来，按接口传入数据进行计算。

### Transformer

最后的 `Transformer` 将各个模块都组合起来：

```py
class Transformer(nn.Module):
    def __init__(
        self,
        src_vocab_size,
        trg_vocab_size,
        src_pad_idx,
        trg_pad_idx,
        embed_size=512,
        num_layers=6,
        forward_expansion=4,
        heads=8,
        dropout=0,
        device="cpu",
        max_length=100,
    ):

        super(Transformer, self).__init__()

        self.encoder = Encoder(
            src_vocab_size,
            embed_size,
            num_layers,
            heads,
            device,
            forward_expansion,
            dropout,
            max_length,
        )

        self.decoder = Decoder(
            trg_vocab_size,
            embed_size,
            num_layers,
            heads,
            forward_expansion,
            dropout,
            device,
            max_length,
        )

        self.src_pad_idx = src_pad_idx
        self.trg_pad_idx = trg_pad_idx
        self.device = device

    def make_src_mask(self, src):
        src_mask = (src != self.src_pad_idx).unsqueeze(1).unsqueeze(2)
        # (N, 1, 1, src_len)
        return src_mask.to(self.device)

    def make_trg_mask(self, trg):
        N, trg_len = trg.shape
        trg_mask = torch.tril(torch.ones((trg_len, trg_len))).expand(
            N, 1, trg_len, trg_len
        )

        return trg_mask.to(self.device)

    def forward(self, src, trg):
        src_mask = self.make_src_mask(src)
        trg_mask = self.make_trg_mask(trg)
        enc_src = self.encoder(src, src_mask)
        out = self.decoder(trg, enc_src, src_mask, trg_mask)
        return out
```

初如化部分主要是设定了默认的参数，并引入前面定义好的 `Encoder` 与 `Decoder` 模块。`Transformer` 中还多了 `make_src_mask()` 与 `make_trg_mask()` 两个函数，这就不得不谈谈 Transformer 中的掩码机制了。

考虑一个情境，需要使用 Transformer 翻译一批（若干条）句子，各句子的长度自然是不同的，那么输入模型的数据的形状也是不同的，这在后续步骤中就会出现很多问题。在实际中，通常会找到文本中最长的句子（`max_len`），再将所有句子都变为该长度，这种操作称为 padding。

具体做法如下图所示，分别用 `<s>` 与 `<e>` 标记句子的起讫，用 `<p>` 填充 `<e>` 后的空位，各数据的长度就会一致。然后根据设定的词典，将 token 转化为索引，接着再做词嵌入。`make_src_mask()` 就是根据 `<p>` 的索引，将 `<p>` 所在位置都标记为 `False`，其他位置标记为 `True`。

后续 `unsqueeze()` 的操作比较费解，其实它是利用了 PyTorch 的广播机制，用于自动匹配矩阵的形状。图中的例子可以看作是将矩阵翻转再在第 3 个方向上拉长。因为代码中的掩码要用于掩盖形状为 `[N, heads, query_len, key_len]` 具有 4 个方向的 `energy`，所以要额外再做一次 `unsqueeze()`。最后将掩码用于掩盖词嵌入数据，掩码就像一个罩子盖在词嵌入数据上，模型只计算 `True` 位置上的数据。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8821?authkey=ALYpzW-ZQ_VBXTU)

使用掩码可以让模型灵活地处理不同长度的数据，数据的长度由掩码决定，改变掩码就相当于改变处理的数据，而不去改变存储在硬件中的数据，这对于计算更有利。

`make_trg_mask()` 函数产生用于 target 数据的掩码，在 target 上使用掩码的原因与 source 不同。在 decoder 中，模型要根据输入数据的计算结果给出新 token，而生成文本的过程是顺序的，依赖于前一步生成的结果。具体来说就是，

1. 序列以 `<s>` 标记起始；
2. 根据已有的 `<s>` 生成 `A`；
3. 根据生成的 `<s> A` 生成 `B`；
4. 根据生成的 `<s> A B` 生成 `C`；
5. 以此类推，直至模型生成 `<e>`，句子结束。

前文已经讨论过，这种方法有很多局限性，而 Transformer 的巧妙之处就在于能够并行完成这个过程。

我们可以考虑训练过程，实际上与生成过程类似，训练过程就是要根据已经生成的 `<s>` 建立与下一个 token `A` 的关系，而不能是与后续 `B` 或 `C` 的关系，将这种关系以参数的形式存储到模型中，推理阶段就能顺利地根据 `<s>` 生成 `A`。这样的训练过程可以表示为一个下三角矩阵，如下图所示。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8822?authkey=ALYpzW-ZQ_VBXTU)

Transformer 不需要逐个 token 生成再建立关系，可以通过下三角矩阵一次直接取出 `<s>`、`<s> A`、`<s> A B` 等 token 序列，并行地训练模型与对应的下一个 token 建立关系。最后将 `<s>` 与每一步骤中新生成 token `A`、`B`、`C`、`<e>` 拼合起来，即得到生成的文本。

`make_trg_mask()` 就是在构建这个下三角的掩码。`torch.ones()` 用于生成指定大小元素全为 `1` 的矩阵，然后用 `torch.tril()` 取该矩阵的下三角，再用 `expand()` 方法将该矩阵复制到与 `batch_size` 匹配。

### Train

从前面讨论的模型生成过程还可以知道的一点是，模型永远不会生成 `<s>`，所以 target 中没有 `<s>`，而 source 则必须由 `<s>` 起始。在实际中，一种做法是，用预处理的脚本在原始训练数据（例如 `.csv`、`.txt` 文件）中标上标记；另一种方法是，在训练代码中加入预处理的功能，读取数据时分别为数据做上相应标记。为了方便起见，本文就不实现这一部分功能，使用 Transformer 可以直接处理的数据。

生成训练数据的函数为

```py
def generate_random_batch(batch_size, max_length=16):
    src = []
    for i in range(batch_size):
        # 随机指定有效数据的长度
        random_len = random.randint(1, max_length - 2)
        # 在数据起讫处加上标记，"<s>": 0, "<e>": 1
        random_nums = [0] + [random.randint(3, 9) for _ in range(random_len)] + [1]
        # padding 填满数据长度，"<p>": [2]
        random_nums = random_nums + [2] * (max_length - random_len - 2)
        src.append(random_nums)

    src = torch.LongTensor(src)
    # tgt 去除末尾的 token
    tgt = src[:, :-1]
    # tgt_y 去除首个 <s>，即模型需要预测的 token，用于计算损失
    tgt_y = src[:, 1:]
    # 模型需要预测的 token 数量（不计 <p>），用于计算损失函数
    n_tokens = (tgt_y != 2).sum()

    return src, tgt, tgt_y, n_tokens
```

`generate_random_batch()` 能够生成 Transformer 可以直接计算的相同的 source 与 target，该模型的任务目标就是生成与输入相同的序列。模型不会生成 `<s>`，所以`tgt_y` 去除 `<s>` 用于与生成的序列对比计算损失，这很容易理解。但为什么 `tgt` 需要去除最后一个 token 呢？这一点我将在后文生成序列的 Predict 一节讨论。训练与测试模型的代码如下：

```py
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

# <p> 索引
src_pad_idx = 2
trg_pad_idx = 2
# 词表大小，即全部 token 数量，包括 <s> <e> <p> 等标记
src_vocab_size = 10
trg_vocab_size = 10
# 文本最大长度
max_len = 16

model = Transformer(src_vocab_size, trg_vocab_size, src_pad_idx, trg_pad_idx,
                    embed_size=128, num_layers=2, dropout=0.1, max_length=max_len,
                    device=device).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)
criteria = nn.CrossEntropyLoss()
total_loss = 0

for step in range(2000):
    src, tgt, tgt_y, n_tokens = generate_random_batch(batch_size=2, max_length=max_len)
    optimizer.zero_grad()
    out = model(src, tgt)

    # contiguous() 与 view() 将矩阵在各行首尾相连为一行（即向量）
    # 在两向量间计算损失函数
    # tgt_y 中元素的值是索引，除以 n_tokens 将其缩放到 [0, 1]
    loss = criteria(out.contiguous().view(-1, out.size(-1)),
                    tgt_y.contiguous().view(-1)) / n_tokens
    loss.backward()
    optimizer.step()

    total_loss += loss

    if step != 0 and step % 40 == 0:
        print(f"Step {step}, total_loss: {total_loss}")
        total_loss = 0

# Predict
copy_test(model, max_len)
```

PyTorch 使用 `torch.optim` 定义模型的训练过程，其中可以选择非常多种的优化过程，这里选择了 `Adam()`，`lr=3e-4` 指定了训练步骤的学习率。`nn.CrossEntropyLoss()` 用于计算两个向量的交叉熵损失，作为训练过程的损失函数。

在训练循环中，每一个循环处理 1 个 batch 的数据，在同一个 batch 中 PyTorch 自动计算梯度的反向传播并更新参数。但在新的 batch 中，因为已经更新到参数中了，我们不希望保留上一个 batch 的梯度，所以用 `optimizer.zero_grad()` 将梯度清空。

将 `src` 与 `tgt` 传入模型，`out` 就是 Transformer 的计算结果。`loss.backward()` 与 `optimizer.step()` 两行代码就是前面所说的让 PyTorch 自动计算梯度的反向传播并更新参数。

### Predict

训练结束后，我用 `copy_test()` 函数测试模型的效果，这个测试函数定义为

```py
def copy_test(model, max_len):
    model = model.eval()
    src = torch.LongTensor([[0, 6, 3, 4, 5, 6, 7, 4, 3, 1, 2, 2]])
    # 模型从 <s> 开始生成序列，但不会生成 <s>，所以指定起始的 <s>
    tgt = torch.LongTensor([[0]])

    for i in range(max_len):
        # out： (1, i + 1, 10)
        # i + 1 模型输出的 token 数量
        # 10 为 vocab_size，是词表中 token 数量，out 是词表中各 token 在此处出现的概率
        out = model(src, tgt)
        # 取输出的 i + 1 个 token 中的最后一个
        # predict: (1, 10)
        predict = out[:, -1]
        # 取得概率最大的 token 索引
        # y: (1, )
        y = torch.argmax(predict, dim=1)
        # 逐个拼合 token 索引
        # y.unsqueeze(0): (1, 1)
        # tgt: (1, i + 1 )
        tgt = torch.concat([tgt, y.unsqueeze(0)], dim=1)
        # 若生成 token <e>，表示句子结束，退出循环
        if y == 1:
            break
    print(tgt)
```

`eval()` 方法令模型退出训练模式，会关闭 dropout 等训练过程中才需要的功能。在循环中逐个拼合生成的 token，就能得到生成的句子。循环中的操作如下图所示，在第 1 次循环中，`tgt` 为 `<s>`，通过与 `src` 的注意力与下三角矩阵得到计算结果 `out` 为 `A`，然后将 `tgt` 更新为 `<s> A`，在第 2 次循环中，得到的 `out` 为 `A B`，所以在每次循环中都只取新生成的 `out[-1]` 更新 `tgt`，最后将结果拼接起来得到完整的输出结果。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8824?authkey=ALYpzW-ZQ_VBXTU)

或许读者会有疑惑，既然使用下三角矩阵并行计算是 Transformer 的优势，为什么这里却是用循环顺序地生成呢？为什么计算上图中最后一个矩阵的 `out`，而是要用一个个的 `out[-1]` 呢？

要注意的是，训练与生成有重要的一个不同，就是生成中的 `tgt` 是空白的、模型不可知的，而训练中的 `tgt` 是完整的、模型可知的。如上图中，`tgt` 在每个循环中都在变长，只有 `tgt` 变成了 `<s> A B C …` 才会有最后一个矩阵中的 `out`。如果说只要最后一个矩阵中的 `out` 而不要前面的步骤，就变成了「吃两个馒头吃饱，所以只吃后一个能吃得饱的馒头」的笑话。

所以<dot>生成过程并不是并行的，Transformer 的并行指的是训练过程</dot>。如下图所示，在训练过程中 Transformer 只需要做一次下三角矩阵的运算就可以建立多个 token 间的关系。这张图还解释了模型永远不会生成 `<s>` 但 `tgt` 必须以 `<s>` 起始的原因。图中还可以很明白的看出为什么先前的训练代码要去除 `tgt` 末尾的 token，因为 Transformer 的输出 `out` 计算的是 `tgt` 下一个 token（及此前）的计算结果，若不去除末位就超出范围了。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8823?authkey=ALYpzW-ZQ_VBXTU)

最后训练与测试的结果为

```python-repl
cpu
Step 40, total_loss: 4.021485328674316
Step 80, total_loss: 2.8817126750946045
……
Step 1920, total_loss: 0.9760974049568176
Step 1960, total_loss: 0.8644390106201172
tensor([[0, 6, 3, 4, 5, 7, 6, 4, 3, 1]])
```

输出的结果没有输出 source `[[0, 6, 3, 4, 5, 6, 7, 4, 3, 1, 2, 2]]` 中末尾代表 `<p>` 的 `2`，前面的 token 索引也与 source 相差无几，说明模型正确复制了输入序列，训练是成功的。

## 后记

至此，这篇 Transformer 的介绍终于告一段落了。从起草、绘图再到最后的代码梳理，前后花了一周多的时间。虽名为介绍，其实还是为自己在做梳理，边写边想、边想边查，终于把 Transformer 中的一些细节弄明白了，这篇笔记也能为读者勾勒出一个大致的图景。

当然，限于篇幅，限于「从零起步」的初衷，也限于笔力，还有许多更深层次问题都没有探讨，但我相信，在看懂了这篇笔记之后，再去阅读那些文章已经不成问题了，这也符合我的初心。

或许读者还很困惑，疑惑为什么数学推导上并不那么严谨的模型居然能有效，甚至具有极好的表现，那就说明需要钻入研究 Transformer 的底层了，不可不再读些更专业的文章。我也把写这篇文章时所参考以及较好的相关资料罗列于后，以飨读者。

## References

- [Vaswani, A. et al. Attention Is All You Need (2017) - arXiv](https://arxiv.org/abs/1706.03762)
- [《Attention is All You Need》浅读（简介+代码）- 科学空间](https://spaces.ac.cn/archives/4765)
- [从语言模型到 Seq2Seq：Transformer 如戏，全靠 Mask - 科学空间](https://spaces.ac.cn/archives/6933)
- [Language Modeling with nn.Transformer and torchtext - PyTorch](https://pytorch.org/tutorials/beginner/transformer_tutorial.html)
- [The Illustrated Transformer - Jay Alammar](http://jalammar.github.io/illustrated-transformer/)
- [Transformer 源码中 Mask 机制的实现 - 博客园](https://www.cnblogs.com/wevolf/p/12484972.html)
- [torch.einsum 详解 - 知乎](https://zhuanlan.zhihu.com/p/434232512)
- [Pytorch 中 nn.Transformer 的使用详解与 Transformer 的黑盒讲解 - CSDN 博客](https://blog.csdn.net/zhaohongfei_358/article/details/126019181)