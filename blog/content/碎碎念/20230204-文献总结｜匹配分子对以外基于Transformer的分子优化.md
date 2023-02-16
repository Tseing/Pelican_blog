title: 文献总结｜匹配分子对以外基于 Transformer 的分子优化
slug: summary-doi.org/10.1186/s13321-022-00599-3
date: 2023-02-04
tags: Literature Summary, CADD, Transformer
summary: 本文介绍于 2022 年发表在 *Journal of Cheminformatics* 上的一篇文章，文章原标题为 Transformer‑based molecular optimization beyond matched molecular pairs，目前已经出现许多使用 MMP 的 Transformer 模型，针对这种现状，文章评估了除 MMP 以外其他分子匹配方式对 Transformer 模型表现的影响。

<i class="fa fa-external-link"></i> [doi.org/10.1186/s13321-022-00599-3](https://doi.org/10.1186/s13321-022-00599-3)

本文介绍于 2022 年发表在 *Journal of Cheminformatics* 上的一篇文章，文章原标题为 Transformer‑based molecular optimization beyond matched molecular pairs，目前已经出现许多使用匹配分子对（matched molecular pairs, MMP）的 Transformer 模型，针对这种现状，文章评估了除 MMP 以外其他分子匹配方式对 Transformer 模型表现的影响。

尽管 MMP 已经广泛应用在多种分子生成模型中，但 MMP 也存在一定的局限性，例如 MMP 在分子单键处匹配的特点决定了每次只能修改分子中单一部分的结构，这与实际中对分子多部分结构进行改造的方法有所差别。除此以外，化学家改造分子的目的是使其满足一定的性质，目前少有研究关注在模型上以此为目标进行直接的分子优化。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8500?authkey=ALYpzW-ZQ_VBXTU)

因此文章从分子的结构与性质两个方面考量模型的表现，如图所示，输入序列由性质约束与分子 SMILES 构成，Transformer 生成优化后的分子，评估生成分子是否满足结构与性质两种约束。

## 方法

### 构造分子对

分子的 SMILES 数据来自于 ChEMBL，经过筛选、去重等数据清洗步骤后，需要将以往文献中改造前后的分子组合为分子对，文章使用了 3 种构造分子对的方法：

1. MMP：对比分子的结构，将仅具有单一部分结构差异的两个分子作为分子对，这种方法获取的分子改造仅改变了分子中单一部分。
2. 谷本相似度：通过摩根指纹计算两个不同分子的谷本相似度，相似度在相应阈值内的两个分子视为分子对，这种方法获取的两个分子可能具有多部分结构差异，文章中使用的阈值包括
   - Similarity (≥0.5)
   - Similarity ([0.5,0.7))
   - Similarity (≥0.7)
3. 分子骨架匹配：同一系列分子中，将具有相同分子骨架的两个分子作为分子对，generic scaffold 则是将骨架中的所有原子转化为碳、所有化学键转化为单键后进行行匹配。

### 分子性质优化

收集到大量分子改造的分子对后，根据源分子与目标分子间性质的变化定义了不同的性质描述符，例如 `LogD_change_(− inf, − 6.9]`、`Solubility_high→low` 和 `Clearance_no_change` 等，这些描述符放置在原始分子 SMILES 前，通过 Transformer 的 self-attention 机制决定对分子的结构改造。

对于缺少相关性质数据的分子，文章使用性质预测模型确定性质的变化并指定性质描述符。

### 评估指标

#### 性质约束

满足以下条件的生成分子视作满足性质约束：

- $|\log D_\mathrm{generated}-\log D_\mathrm{target}|\leq 0.4$
- $\mathrm{solubility_{low}}\leq 2.3\ \mathrm{or}\ \mathrm{solubility_{high}}\geq 1.1$
- $\mathrm{clearance}=1.3\pm0.35$

#### 结构约束

若生成分子通过了相应算法（例如 MMP）的检查，则可以认为分子满足了结构约束。

### 基线

- Transformer-U：不具有特征约束的 Transformer 模型。
- Random：从测试集中随机选取 10 个具有相同结构约束的分子。

## 结果与讨论

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8501?authkey=ALYpzW-ZQ_VBXTU)

结果表明，Transformer 具有最好的效果，由于 Transformer-U 没有学习到分子的性质特征，所生成分子中满足性质约束的占比很低。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8502?authkey=ALYpzW-ZQ_VBXTU)

对比不同分子对算法模型生成分子与训练集的分布，可以发现，在使用谷本相似度的三种模型中，尽管生成分子与训练集的分布吻合程度稍低，但模型生成的满足性质约束的分子并未被结构约束限制住（超出红色范围的淡绿色），这说明使用谷本相似度的模型具有一定探索化学空间的能力。

使用 MMP、分子骨架的模型中，生成分子与训练集的分布十分吻合，模型学习到了数据特征并在结构约束中生成具有目标性质的分子。对比 MMP 与分子骨架的模型，MMP 模型两种分布的吻合程度更高，对分子的结构改变更小，而分子骨架模型偏向于产生谷本相似度更高的分子。

结合表中的数据，相比于基于谷本相似度的模型，MMP 和分子骨架模型更容易生成满足结构约束的分子，这是因为于谷本相似度训练集中的分子差异较大，这使得 Transformer 更难获取其中的特征。另一方面，由于分子差异较大，模型更倾向于探索化学空间，能够得到了更多满足性质约束的分子（Similarity (≥0.7)），但在探索的化学空间太大时，寻找同时满足性质约束与结构约束的分子就会变得困难，因此较恰当的 Similarity (≥0.7) 与 MMP 两组模型表现最好。

根据分子对匹配方法原理不同，可以将文章中的模型分为 3 类：

1. 单一部分改造：MMP
2. 多部分改造但不改变骨架：Scaffold 与 Scaffold generic
3. 多部分改造且改变骨架：Similarity (≥0.5)、Similarity ([0.5,0.7)) 与 Similarity (≥0.7)

从生成分子中也可以看出不同模型的分子改造方式：

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8503?authkey=ALYpzW-ZQ_VBXTU)

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8504?authkey=ALYpzW-ZQ_VBXTU)

## 结论

文章评估了包括 MMP 在内的多种分子对匹配方法，虽然 MMP 是目前广泛应用的一种方法，并且在文章的评估中也表现良好，但必须考虑到 MMP 的原理使其对分子做的是单一部分改造，这就会影响分子多样性等指标。在实际应用中，应当根据模型目的考虑多种分子对匹配方法，或者参考该文章的方法评估不同分子对匹配方法对模型表现的影响。