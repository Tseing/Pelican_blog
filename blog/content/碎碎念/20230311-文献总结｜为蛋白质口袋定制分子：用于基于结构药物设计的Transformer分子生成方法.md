title: 文献总结｜为蛋白质口袋定制分子：用于基于结构药物设计的 Transformer 分子生成方法
slug: summary-doi.org/10.48550/arXiv.2209.06158
date: 2023-03-11
tags: Literature Summary, CADD, Transformer, VAE
summary: 本文介绍由微软研究团队于 2022 年发布在 arXiv 上的一篇文章，文章原标题为 Tailoring Molecules for Protein Pockets: a Transformer-based Generative Solution for Structured-based Drug Design，文章使用 Transformer 构建了一种能够获取受体 3 维信息的分子生成模型 TamGent，其中分子生成部分使用了预训练模型，避免了训练数据有限的问题。

<i class="fa fa-external-link"></i> [doi.org/10.48550/arXiv.2209.06158](https://doi.org/10.48550/arXiv.2209.06158)

本文介绍由微软研究团队于 2022 年发布在 arXiv 上的一篇文章，文章原标题为 Tailoring Molecules for Protein Pockets: a Transformer-based Generative Solution for Structured-based Drug Design，文章使用 Transformer 构建了一种能够获取受体 3 维信息的分子生成模型 TamGent，其中分子生成部分使用了预训练模型，避免了训练数据有限的问题。

随着人工智能技术的发展，深度学习也进入到基于结构的药物设计（Structure Based Drug Design, SBDD）领域。SBDD 基于受体蛋白的结构设计与之适配的分子，是药物化学中的重要方法，而在深度学习辅助下的 SBDD 也将大大提升药物设计的效率，但目前这一方向还存在两个问题：

1. 用于训练模型的「靶点-药物分子对」有限；
2. SBDD AI 模型还不能很好利用靶点活性口袋的 3 维信息。

针对以上两个问题，文章首先使用分子数据预训练 Transformer 生成模型，使其学习到分子数据中更通用的特征，避免标签不足；其次，文章设计了一种变种的 Transformer encoder，通过 encoder 获得氨基酸序列中的 3 维结构信息，文章将最后得到的模型称为 TamGent（Target-aware molecule generator with Transformer）。

## 方法

### 数据

文章使用来自于 PubChem 数据库中的 1000 万个分子的 SMILES 序列预训练用于分子生成的 Transformer decoder 模型，使用来源于文献（[Luo et al.](https://arxiv.org/abs/2205.07249)）的 12.3 万个靶点-配体对训练配体生成模型。

### 模型

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8650?authkey=ALYpzW-ZQ_VBXTU)

使用 $\boldsymbol{a}=(a_1,a_2,\cdots,a_N)$ 表示氨基酸序列，其中 $a_i$ 为长度为 20 的 ont-hot 向量，可以用于表示 20 种氨基酸，使用 $\boldsymbol{r}=(r_1,r_2,\cdots,r_N)$ 表示相应的 3 维坐标，其中 $r_i\in\mathbb{R}^3$。将配体分子的 SMILES 编码转化为向量 $\boldsymbol{y}=(y_1,y_2,\cdots,y_M)$，那么模型训练的目标就是学习从 $\boldsymbol{x}=(\boldsymbol{a},\boldsymbol{r})$ 到 $\boldsymbol{y}$ 的映射。

TamGent 的架构参考了变分自编码器的工作模式，也就是主要由活性口袋 encoder 和配体分子 decoder 构成，encoder 与 decoder 都使用了 Transformer 中的结构。

配体分子 decoder 部分与 Transformer 完全一样，具有 self-attention 机制，能够根据生成的 toekn 生成下一个 token，完成分子生成，因此使用 1000 万个分子数据预训练该模型，使其能够根据数据集中分子的普遍特征生成分子。

活性口袋 encoder 部分修改了其中的 attention 机制，文章中称为 distance-aware attention。具体来说，就是认为距离较远的氨基酸与配体的相互作用更小，所以将输入的氨基酸序列和坐标转化为特征矩阵后，再与 $\exp(-\mathrm{distance}^2/\tau)$ 相乘，距离越远的氨基酸的权重就会越小。

在推断过程中，将氨基酸序列及其坐标输入模型，embedding 为特征矩阵后进入活性口袋 encoder 部分计算 distance-aware attention，得到活性口袋的表示，最后将其作为配体分子 decoder 部分中的 pocket-SMILES attention，生成分子得到预测的活性配体结果。

## 结果与讨论

### 生成分子结果

文章使用 DrugBank 数据库中 1641 个靶点-配体对的数据用于测试模型效果，随机抽取其中的 100 个靶点-配体对，使用 TamGent、3DGen 和 SECSE 三种模型针对每个靶点生成 20 个分子，对比生成效果。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8651?authkey=ALYpzW-ZQ_VBXTU)

三种模型生成分子的对接打分中，TamGent 生成的分子明显更低，说明分子与靶点具有更好的亲和力，同时其平均值也与标签数据最为接近。对比三种模型生成的分子与标签分子的相似性，同样是 TamGent 具有更大的相似性，生成的分子最接近标签分子。同时，在 QED、MD 和 SA 几项的分子指标上，TamGent 也都高于其他两种模型，以上几点可以表明 TamGent 在 DrugBank 数据上根据靶点生成分子具有明显的优势。

### 案例研究

接下来文章使用 TamGent 针对于具体的靶点生成配体，分析模型表现。文章选择 SARS-CoV-2 主糖蛋白酶（*M* <sup>pro</sup>）作为靶点生成分子，收集了 415 个高分辨率结构后，使用模型生成了 4563 个分子，其中找到了先前报道过的一种 *M* <sup>pro</sup> 候选抑制剂（GC-376）和 6 个可能的先导化合物片段。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8652?authkey=ALYpzW-ZQ_VBXTU)

上图展示了相应分子的二维分布，其中灰色表示在 PubChem 中随机选取的 3 万个分子，蓝色表示 TamGent 生成的分子，黄色表示在先前报道中提到了可能的 *M* <sup>pro</sup> 抑制剂。

明显可以看出 TamGent 生成的分子与随机选取的分子具有不同的分布并且成簇聚集，主要分为 ① 和 ② 两簇。在第 ① 簇中，生成分子与 GC-376 的谷本相似度达到 0.82，并且此前报道的 6 种候选抑制剂都位于该簇中。但在第 ② 簇中没有找到对接分数较好的分子，只在分子中找到了一些可能的活性片段。

最后文章选出了第 ① 簇中两个结构不同的分子与 *M* <sup>pro</sup> 对接，两种分子都能很好地填充活性口袋，对接分数分别为 -10.2 和 -9.5，而先前的 GC-376 是 -9.4，说明 TamGent 能够根据口性口袋生成具有良好活性的分子。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8653?authkey=ALYpzW-ZQ_VBXTU)

## 结论

文章参考变分自编码器的结构使用 Transformer 构建了一种能够获取受体 3 维信息的分子生成模型 TamGent，其中分子生成部分使用了预训练模型，避免模型依赖于有限的「靶点-药物分子对」。在分子生成任务中，TamGent 生成分子的效果优于以往的两种模型，使用 TamGent 针对 SARS-CoV-2 主糖蛋白酶生成活性分子，甚至找到了比先前报道的候选抑制剂具有更好对接打分的分子，表现出 TamGent 的优异性能。

对于 TamGent，文章提出了 3 点改进措施，第一是使用更多实验测试得到的「靶点-药物分子对」进一步优化模型，第二是在模型中整合考虑 ADMET 待药理性质，第三是在具体靶点上微调模型，使其帮助提升针对相应靶点的药物研发效率。