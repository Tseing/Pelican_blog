title: 文献总结｜SyntaLinker：使用 Conditional Transformer 神经网络自动连接分子片段
slug:  summary-doi.org/10.1039/d0sc03126g
date: 2022-11-14
tags: Literature Summary, CADD, Transformer
summary: 本文介绍于 2020 年发表在 Chemical Science 上的一篇文章，文章原标题为 SyntaLinker: automatic fragment linking with deep conditional transformer neural networks，文章将基于语义模型 Transformer 识别并连接分子片段，最终设计了一种分子片段连接工具 SyntaLinker，它能够有效完成有约束的分子片段连接任务。

<i class="fa-solid fa-arrow-up-right-from-square"></i> [doi.org/10.1039/d0sc03126g](https://doi.org/10.1039/d0sc03126g)

本文介绍于 2020 年发表在 *Chemical Science* 上的一篇文章，文章原标题为 SyntaLinker: automatic fragment linking with deep conditional transformer neural networks，文章将基于语义模型 Transformer 识别并连接分子片段，最终设计了一种分子片段连接工具 SyntaLinker，它能够有效完成有约束的分子片段连接任务。

## 引言

基于片段的药物设计（Fragment-Based Drug Design , FBDD）是计算机辅助药物设计的一种基本手段，在药物设计中 FBDD 需要完成的任务包括

1. 寻找合适的分子片段；
2. 基于分子片段生长并优化片段，最终得到类药分子。

其中，使分子片段不断生长并连接组成分子的任务仍具有很大困难，因为很大的一个挑战就在于如何保持各片段连接后各片段与受体的结合方式不发生改变。从这一点看来，连接片段的任务是 FBDD 中的关键难题。

文章借用深度学习的方法来解决这一问题，文章以 SMILES 表示分子片段，将片段连接视作自然语言处理中的句子填空任务，并设计了一种新的 conditional transformer 模型用于完成该任务。

## 方法

### 分子表示

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!7969?authkey=ALYpzW-ZQ_VBXTU)

如图所示，文章使用 SMILES 表示分子片段，用 `[*]` 表示分子片段的连接位置，用 `.` 分隔两个分子片段。文章还设计了两种有约束任务，在最短连接键长（shortest linker bond distance, SLBD）约束模式下，在 SMILES 最前面以 `[L_n]` 表示两个分子片段连接部分应当具有 $n$ 个化学键。在多约束模式下，考虑的约束条件除了 SLBD 以外，还包括氢键给体、氢键受体、可旋转键和环状结构，若需要约束连接部分是否存在相应结构，则按四个约束的次序分别以 $1$ 表示存在，以 $0$ 表示不存在，如图中的 `[L_4 1 1 1 0]`。

### 模型

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!7975?authkey=ALYpzW-ZQ_VBXTU)

SyntaLinker 模型的结构基于 transformer 模型，能够根据用户指定的条件生成分子，transformer 模型的原理可以参考[先前的文章](https://tseing.github.io/sui-sui-nian/2022-10-08-summary-doi.org/10.1038/s42256-021-00403-1.html)。

输入的 SMILES 字符串以 one-hot 矩阵形式表示，再通过 word embedding 算法转化为 embedding 向量构成的矩阵。输入的 embedding 被编码器层处理为潜在表达，潜在表达被解码器用 softmax 函数转化为各词的概率序列，直至遇到结束符 `</s>`，就完成了分子的生成。最后，使用生成分子与目标分子间的交叉熵损失训练模型：

$$\mathcal{L}(Y,M)=-\sum_{i=1}^ky_i\log m_i$$

### 数据处理

分子数据来自于 ChEMBL，并使用 Lipinski 五规则、泛筛选干扰化合物（pan assay interference compounds, PAINS）结构和 SA score（synthetic accessibility score）初步筛去不合理的分子。

文章使用匹配分子对（matched molecular pairs, MMPs）划分算法将原始分子数据转化为用于训练的分子片段数据。MMPs 划分算法在每个分子的两个非官能团的无环单键处切割，最后得到片段甲、连接部分、片段乙和完整分子四个部分数据，将其称为片段分子四部分数据（fragment molecule quadruples, FMQs）。
接着所有 FMQs 都要经过 RO3（Rule of three）规则、SLBE 和 SA score 的筛选，最终分子片段满足 SLBD 小于 15 的条件从而避免连接部分过于复杂，并满足以下 SA score 要求避免分子难以合成：

$$\begin{equation}
    \mathrm{SAscore\_filter}(x)=
    \begin{cases}
        &\mathrm{SA_{fragment\ 1}<5}\\
        &\mathrm{SA_{fragment\ 2}<5}\\
        &\mathrm{SA_{linker}}<(\mathrm{SA_{fragment\ 1}}+\mathrm{SA_{fragment\ 2}})
    \end{cases}
\end{equation}$$

### 指标

使用通过片段数据生成分子的合法性、独特性、回复性和新颖性评价模型：

**合法性（validity）** 指通过一对分子片段生成合法化学结构分子的比例，定义为

$$\mathrm{Validity}=\frac{\mathrm{\#\ of\ chemically\ valid\ SMILES\ with\ fragments}}{\mathrm{\#\ of\ generated\ SMILES}}$$

**独特性（uniqueness）** 指生成分子中具有特有化合结构分子的数量，定义为

$$\mathrm{Uniqueness}=\frac{\mathrm{\#\ of\ non\mbox{-}duplicate;\ valid\ structures}}{\mathrm{\#\ of\ valid\ structures}}$$

**回复性（recovery）** 指生成分子中生成的训练集中真实分子所占比例;

**新颖性（novelty）** 指生成分子中生成的化学结构合法且未出现在训练集中的连接部分所占比例，定义为

$$\mathrm{Uniqueness}=\frac{\mathrm{\#\ of\ novel\ linkers\ not\ in\ training set}}{\mathrm{\#\ of\ unique\ structures}}$$


## 结果与讨论

### 生成分子

文章设置了无约束的 SyntaLinker_n、SLBD 约束的 SyntaLinker 和 多约束的 SyntaLinker_multi 三种模式，从每对分子片段生成 10 个最优分子，根据生成分子评估三种模式。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!7970?authkey=ALYpzW-ZQ_VBXTU)

使用 ChEMBL 数据集验证生成分子，可以判断三种模式都初步完成了连接分子片段的任务，生成了大比例符合要求的分子，其中多约束的 SyntaLinker_multi 在多方面具有较好的效果。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!7971?authkey=ALYpzW-ZQ_VBXTU)

为了与 DeLinker 模型对比，再从每对分子片段生成 250 个最优分子，生成的分子数据用  CASF 验证集验证。与 DeLinker 模型生成的数据相比，SyntaLinker 的三种模式都具有更优的性能，特别是在新颖性方面的优势，说明 SyntaLinker 能生成结构更新颖的连接部分。在SyntaLinker 的三种模式中，仍然是多约束的 SyntaLinker_multi 具有更好效果。

### 约束能力

与上文设置类似，分别使用 SyntaLinker 的三种模式基于每对分子生成 10 个和 250 个分子，使用 ChEMBL 和 CASF-2016 验证集验证各模型生成的分子是否满足约束条件。SyntaLinker 中的约束条件可以分为两部分，一部分是化学键约束，需要考察生成分子的连接部分满足 SLBD 条件，另一部分是药效团约束，需要考察生成分子是否根据预设的条件生成了类药性高的分子。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!7972?authkey=ALYpzW-ZQ_VBXTU)

<note>(a) The percentage of compounds among top 10 solutions in the ChEMBL test set; (b) the percentage of compounds among top 250 solutions in the ChEMBL test set; (c) the percentage of compounds among top 10 solutions in the CASF set; (d) the percentage of compounds among top 250 solutions in the CASF set.</note>

首先考察各模型的化学键约束，可以看出，具有化学键约束的 SyntaLinker 与 SyntaLinker_multi 在所有评估结果中，生成满足约束分子的比例都要更高，表明两种模型确实能够完成有约束的分子片断连接任务。随着每对片段生成分子数量的增加，满足约束分子的比例也有所减少，但相比无约束的 SyntaLinker_n，有约束的 SyntaLinker 与 SyntaLinker_multi 仍具有优势。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!7973?authkey=ALYpzW-ZQ_VBXTU)

接着考察各模型的药效团约束，药效团约束的结果也表现出相似的趋势，具有约束的 SyntaLinker_multi 生成满足约束的分子占比更多，而无约束的 SyntaLinker 与 SyntaLinker_n 则占比更少。随着每对片段生成分子数从 10 增加到 250，满足多约束的困难增加，满足条件的分子相应减少。

### 权重分析

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!7974?authkey=ALYpzW-ZQ_VBXTU)

文章根据模型权重绘制了热图，从中可以看出模型处理分子对 SMILES 的流程。上方是输入模型的 SMILES ，左方是生成分子的 SMILES，权值大体呈左上至右下的对角线排列，这与输入和输出 SMILES 相似度较高的特性吻合。值得住意的是，表明分子连接位置的 `*` 几乎没有权值，说明模型从语义上学习到 `*` 是不会出现在输出中的输入标记。此外，还可以注意到表示两分子片段的 `.` 在输出的连接（蓝色）部分具有很大权重，表明模型能够认识这个分隔符并将其转化为连接部分。输入 SMILES 开头部分的 `L_3` 在连接（蓝色）部分也具有较大权值，可以佐证模型根据约束条件生成连接部分。

### 分子对接案例

除了对生成分子进行评估，文章还结合分子对接等技术验证了 SyntaLinker 应用在药物发现中的可行性。例如，文章使用已有 FBDD 案例相同的分子片段，借助 SyntaLinker 模型生成最终分子，使用 MOE 对生成分子打分，其分数甚至高于原有案例中设计出的分子。

SyntaLinker 模型还可以用于先导化合物的优化，文章选择 dequalinium 作为先导化合物，使用 MMPs 将其划分为分子对，使用 SyntaLinker 模型根据分子对数据生成分子，经过分子对接的验证，生成分子性能确实得到了优化。

## 结论

文章基于 conditional transformer 模型设计子 SyntaLinker 模型，SyntaLinker 模型能够根据给定的分子对数据生成相应的连接部分，最终生成一个新分子，完成了 FBDD 中分子连接的任务。同时，transformer 能够基于语义处理序列，这使得 SyntaLinker 模型生成的分子能够很好地满足指定的约束。最后文章还尝试了将 SyntaLinker 模型与分子对接相应合，拓展了将其应用于从分子片段构建虚拟库、优化优导化合物的可能性。