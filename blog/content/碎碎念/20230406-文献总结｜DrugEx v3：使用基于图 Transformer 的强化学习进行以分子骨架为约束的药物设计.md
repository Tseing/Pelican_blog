title: 文献总结｜DrugEx v3：使用基于图 Transformer 的强化学习进行以分子骨架为约束的药物设计
slug: summary-doi.org/10.1186/s13321-023-00694-z
date: 2023-04-06
tags: Literature Summary, CADD, Transformer
summary: 本文介绍 2023 年发布在 *Journal of Cheminformatics* 上的一篇文章，文章原标题为 DrugEx v3: scaffold‑constrained drug design with graph transformer‑based reinforcement learning，文章介绍了使用包括 Transformer 和 LSTM 模型实现以分子骨架为约束的药物设计的方法并对比了使用 SMILES 与图两种方式的分子表示在分子生成中的区别。

<i class="fa fa-external-link"></i> [doi.org/10.1186/s13321-023-00694-z](https://doi.org/10.1186/s13321-023-00694-z)

本文介绍 2023 年发布在 *Journal of Cheminformatics* 上的一篇文章，文章原标题为 DrugEx v3: scaffold‑constrained drug design
with graph transformer‑based reinforcement learning，文章介绍了使用包括 Transformer 和 LSTM 模型实现以分子骨架为约束的药物设计的方法，并且对比了使用 SMILES 与图两种分子表示方式在分子生成中的区别。

在先前的工作中，作者设计了名为 DrugEx 的 RNN 模型，它能够通过基于分布的方式探索化学空间并通过强化学习的策略实现基于目标的分子生成，但它无法接受用户的输入，无法基于先验知识给出结果，只能在已有的化学空间中给出结果，当任务改变后又需要重新训练模型，这些方面的问题使其在具体应用上具有很大的局限性。

因此这篇文章使用多种深度学习模型重构了 DrugEx，DrugEx 可以接受用户指定的分子骨架生成具有目标结构的分子，并且在模型中引入强化学习策略，更加有效地控制生成分子的目标性质，此外文章对比了不同深度学习模型和以 SMILES 或图两种不同编码方式实现以分子骨架为约束的药物设计的效果。

## 方法

### 数据

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8738?authkey=ALYpzW-ZQ_VBXTU)

由来源于 ChEMBL 的约 170 万条分子数据构成 ChEMBL 数据集，用于预训练模型，由对人腺苷受体具有活性的 10828 条分子数据构成 LIGAND 数据集，用于微调生成模型。

所有数据都构建为「输入- 输出」对的形式，使用 BRICS 规则将每个分子分割为最多 4 个的一系列片段，片段的排列组合就作为输入部分，被分割的分子就作为输出部分。分割完成后，用于预训练生成模型的分子对数据有 9335410 万条。

若以 SMILES 作为分子表示，则是使用词表将每条 SMILES 序列分为若干 token，就可以将 SMILES 表示为 token 的索引序列，用于模型计算。

若以图作为分子表示，首先需要计算分子的临接矩阵，接着每个分子都会被表示为具有 5 行的矩阵，前两行分别代表原子类型和化学键类型，第三行表示连接原子的索引，第四行表示目前原子的索引，第五行表示片段索引。按列连接 start、fragment、growing、end 和 linking 五个部分的上述五种信息，start 与 end 两部分分别具有一列，只有标记分隔的作用，fragment 部分中组织了各分子骨架中的原子信息，growing 部分组织了分子中去除分子骨架后剩余原子的信息，linking 部分组织了 fragment 与 growing 部分间相互连接的化学键信息。

### 模型

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8739?authkey=ALYpzW-ZQ_VBXTU)

文章中设计了 4 种模型用于完成分子生成成任务：

1. 图 Transformer
2. LSTM
3. LSTM + 注意力机制
4. 序列 Transformer

其中分子的图表示只用于图 Transformer 模型中，其他三种模型都使用 SMILES 表示分子。

由于图 Transformer 无法同时处理原子与化学键的信息，因此按下式组合原子和化学键索引：

$$W=T_\mathrm{atom}\times 4+T_\mathrm{bond}$$

通过将原子类型与化学键类型的总数相乘再加上化学键类型得到结果 $W$，用于计算词向量。

由于图 Transformer 处理的不是序列信息，原有的位置编码计算方式同样无法使用，文章设计了以下位置编码：

$$P=I_\mathrm{atom}\times L_\mathrm{max}+I_\mathrm{connected}$$

式中将当前原子索引 $I_\mathrm{atom}$ 与最大长度 $L_\mathrm{max}$ 相乘，然后再加上连接原子的索引 $I_\mathrm{connected}$ 得到位置编码。

### 评估指标

为了更好评估生成分子的多样性，除了常见的分子指标外，文章中还使用了 Solow Polasky measurement，由下式给出：

$$I(A)=\frac{1}{|A|}\boldsymbol{e}^\mathrm{T}F(\boldsymbol{s})^{-1}\boldsymbol{e}$$

其中 $A$ 表示分子数据集，$|A|$ 为数据集大小，$\boldsymbol{e}$ 为 $|A|$ 维元素全为 $1$ 的向量，$F(s)=[f(d_{ij})]$，$f(d_{ij})$ 是表示每对分子间距离的函数：

$$f(d)=\mathrm{e}^{-\theta d_{ij}}$$

其中 $\theta$ 为常数，取 $\theta=0.5$，$d_{ij}$ 为分子 $s_i$ 与 $s_j$ 的分子指纹间的谷本距离。

## 结果与讨论

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8751?authkey=ALYpzW-ZQ_VBXTU)

首先分别使用 ChEMBL 数据集预训练四种模型，再用 LIGAND 数据集微调预训练的生成模型，使用测试集生成分子的结果如上表所示。

同样使用 SMILES 表示分子，相比于 LSTM 模型，训练 Transformer 模型需要的计算资源更多，但训练时间更短而且效果更好。使用 SMILES 的模型在微调后表现有所上升，但还是差于使用图的模型，这主要是由于用图表示分子更容易获得原子的几何关系信息。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8752?authkey=ALYpzW-ZQ_VBXTU)

文章绘制了图 Transformer 生成分子的降维结果，可以看出图 Transformer 生成的分子很好地覆盖了 ChEMBL 和 LIGAND 两个数据集的化学空间。在对生成分子进一步评估中发现，图 Transformer 生成分子的可合成性低于使用 SMILES 的模型，作者认为这是因为基于图的模型能够生成更复杂的结构，导致可合成性降低。

文章总结了图 Transformer 的 4 点优势：

1. 局部尺度上的不变性：图 Transformer 能够很好地识别输入的分子骨架，并使输出的生成分子中具有相同的结构；
2. 全局尺度上的可扩展性：图 Transformer 在生成分子的过程中，可以将生成部分直接插入到表示图的矩阵中，具有很大灵活性；
3. 无语法约束：图 Transformer 不需要关注 SMILES 语法要求，模型不需要额外学习分子中的语法特征；
4. 可引入化学规则：可以在图 Transformer 中引入化学规则，例如价键匹配规则，提高生成分子的准确性。

最后文章还在图 Transformer 中引入了强化学习的策略，模型能够生成对 A<sub>2A</sub>AR 的亲合力和 QED 分数更高的分子。文章中输入模型的分子骨架与生成分子如下图所示：

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8753?authkey=ALYpzW-ZQ_VBXTU)

## 结论

文章重构了以前的 DrugEx 的模型，在对多种深度模型的试验中，图 Transformer 具有最好的分子生成效果。相比于 SMILES，分子的图表示在分子生成任务中可以更好地识别输入的分子结构，并且可以很容易地改造分子结构生成分子，这一点在发现先导化合物以及先导化合物的优化上都能发挥很大的作用。