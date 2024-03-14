title: 文献总结｜MolGPT：使用 Transformer 解码器模型实现分子生成
slug: summary-doi.org/10.1021/acs.jcim.1c00600
date: 2023-03-03
tags: Literature Summary, CADD, Transformer, GPT
summary: 本文介绍于 2022 年发表在 *Journal of Chemical Information and Modeling* 上的一篇文章，文章原标题为 MolGPT: Molecular Generation Using a Transformer-Decoder Model，在 GPT 模型已经在自然语言处理领域得到了成功应用的背景下，这篇文章首次将 GPT 模型应用于完成分子生成的任务，实现了分子性质和结构两个方面的优化。

<i class="fa-solid fa-arrow-up-right-from-square"></i> [doi.org/10.1021/acs.jcim.1c00600](https://doi.org/10.1021/acs.jcim.1c00600)

本文介绍于 2022 年发表在 *Journal of Chemical Information and Modeling* 上的一篇文章，文章原标题为 MolGPT: Molecular Generation Using a Transformer-Decoder Model，在生成预训练（Generative Pre-training, GPT）模型已经在自然语言处理领域得到了成功应用的背景下，这篇文章首次将 GPT 模型应用于完成分子生成的任务，实现了分子性质和结构两个方面的优化。

## 方法

### 数据

分子数据来自于 MOSES 和 GuacaMol 的数据集，其中包括源于 Zinc 的 190 万个类先导化合物与源于 ChEMBL 的 160 万个分子，分子为 SMILES 形式，使用 RDKit 提取分子的骨架用于模型训练。

此外，使用 RDKit 计算出分子的logP、SA、拓扑极性表面积（TPSA）和 QED，用于训练具有性质约束的模型。

### 模型

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8625?authkey=ALYpzW-ZQ_VBXTU)

在得到原始分子的分子骨架与性质信息后，将分子性质与分子骨架序列连接在一起，称为「条件」，那么原始分子就成为需要 MolGPT 根据条件生成的「目标分子」。

在训练过程中，将条件和目标分子序列一同送入 MolGPT，使模型建立条件与目标分子的关系。GPT 模型通过顺序读取每个 token，由当前 token 预测下一个 token，从而获得采样的权重。

具体来说，分子 SMILES 词嵌入为 256 维的向量后，将性质条件和骨架条件也分别词嵌入为 256 维的向量，将其直接拼接在 SMILES 向量的起始端，就构成了实际输入模型的信息。

在推理过程中，模型对训练集中的所有 token 根据权重随机取样得到第一个字符，接着模型就根据输入的条件（即目标性质与需要改造的分子骨架）和第一个字符生成下一个字符，直至生成整个分子。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8626?authkey=ALYpzW-ZQ_VBXTU)

在 Transformer 中，encoder 模块对输入编码得到状态向量 $c$，再由 decoder 模块对状态 $c$ 解码并运算产生输出，由于输入的情况是多种多样的，将其转化为等长的 $c$ 就有很大的局限性。GPT 模型减去了 Transformer 中的 encoder 模块，而保留了 Transformer 中例如 self-attention 在内的其他机制，具有更好的长文本处理能力。

## 结果与讨论

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8632?authkey=ALYpzW-ZQ_VBXTU)

首先使模型在不给定条件的情况下生成分子，即 MolGPT 根据从训练数据集中学习到的化学空间中的分子分布生成生成分子，生成的分子与训练集分子具有相似的特征。

文章分析了 MolGPT 生成一个分子的过程，上图中的黑色横线表示当前步骤生成的字符（token），其他 token 上颜色的深浅表示了与生成该 token 之间的权重关系。

可以看出，MolGPT 首先从已经学习到的分布中随机抽取出 `C`，接着根据它继续生成后续 token，每个 token 都是由先前生成的 token 决定。同时还可以发现 MolGPT 在生成分子的过程中具有一定的「化学知识」，例如第一行中生成 `O` 时，明显由前面的 `=` 与 `N` 决定，所以 MolGPT 不仅能够在双键上连接氧原子，还会构建酰胺结构使分子更稳定。

### 性质条件

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8627?authkey=ALYpzW-ZQ_VBXTU)

文章接着只使用性质条件作为输入分子的条件，测试模型是否能按照要求生成满足约束的分子，结果如上图所示，与训练集中分子的性质分布不同，生成的分子集中在设定的性质条件（黑线）两侧，评估生成分子，各组分子的 validity、unique 和 novelty 都在0.97 以上，具有很好的效果。

此外文章还同时使用多种性质约束作为模型条件，在保持较高的 validity、unique 和 novelty 条件下，生成的分子散落在设置性质条件的周围，所以模型对也能很好地处理多性质约束的分子生成。

### 性质与骨架条件

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8628?authkey=ALYpzW-ZQ_VBXTU)

接下来文章测试了将性质与分子骨架同时作为模型的生成条件，分析了生成分子的性质分布以及生成分子与设定分子骨架的谷本相似度。与仅性质条件的结果相比，额外加入分子骨架条件后生成分子的性质虽然有一些偏移（如上图 g），但仍然能大致满足性质约束。同时生成的分子与设定的分子骨架具有极高的相似性，从这两个可以证明 MolGPT 可以用于对给定的分子骨架进行指定性质的优化。

最后文章展示了使用 MolGPT 实现分子骨架优化的例子：

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8631?authkey=ALYpzW-ZQ_VBXTU)

## 结论

文章使用 GPT 构建了分子生成模型 MolGPT，MolGPT 生成的分子具有很高的 validity 和 uniqueness，在对 MolGPT 生成分子过程中的权重分析发现，MolGPT 能够很好学习到 SMILES 中所包含的化学语义。在实际应用上，MolGPT 可以根据指定的多种分子性质和（或）指定的分子骨架生成目标的分子，生成的分子能够很好满足预先设定的要求，有助于指导化合物优化的方向。