title: 文献总结｜Molecular Sets (MOSES)：分子生成模型的评估平台
slug: summary-doi.org/10.48550/arXiv.1811.12823
date: 2023-01-08
tags: Literature Summary, CADD
summary: 本文介绍于 2020 年发布在 arXiv 上的一篇文章，文章原标题为 Molecular Sets (MOSES): A Benchmarking Platform for Molecular Generation Models，文章介绍了目前在评估分子生成模型方面存在的问题，并且设计了用于衡量模型表现的一套标准指标，目前 MOSES 已经广泛应用于各类分子生成任务。

<i class="fa fa-external-link"></i> [doi.org/10.48550/arXiv.1811.12823](https://doi.org/10.48550/arXiv.1811.12823)

本文介绍于 2020 年发布在 arXiv 上的一篇文章，文章原标题为 Molecular Sets (MOSES): A Benchmarking Platform for Molecular Generation Models，文章介绍了目前在评估分子生成模型方面存在的问题，并且设计了用于衡量模型表现的一套标准指标，目前 MOSES 已经广泛应用于各类分子生成任务。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8452?authkey=ALYpzW-ZQ_VBXTU)

随着深度学习技术的发展，也产生了大量分子生成模型，但由于缺乏统一的评估指标，难以对比不同分子生成模型间的表现差异。此外，由于在分子生成模型中需要考虑化合物的的物理性质、生物活性、可合成性等不同方面的约束，不同的评估指标带来了混乱的同时也让模型更难泛化推广。

文章提供了用于分子生成模型的工具套件 Molecular Sets (MOSES)，其中包括标准数据集、数据预处理工具、评估指标和分子生成模型。

## 分布学习

MOSES 主要用于评估基于分布学习的模型，例如，训练集数据 $X_\mathrm{tr}=\{x^\mathrm{tr}_1,\cdots,x^\mathrm{tr}_N\}$ 满足未知的概率分布 $p(x)$，分布学习模型最终用概率分布 $q(x)$ 逼近 $p(x)$，从而产生与训练集具有相同特征的数据。

评估分布学习模型的方法就是计算概率分布 $p(x)$ 与 $q(x)$ 间的差值。对于显式模型而言，可以计算得到 $q(x)$，通常直接评估概率质量函数。而包括神经网络在内的隐式模型只能从 $q(x)$ 中取样，但无法计算出 $q(x)$。对于这一类模型，MOSES 主要对其生成数据进行评估。

## 评估指标

- **Valid** 和 **Unique@k** 用于评估生成 SMILES 序列的合法性与独特性。使用 RDKit 检查生成分子是否满足 SMILES 规则，合法分子比例即为 Valid，用于确定模型是否学习到化学约束。Unique@k 表示在 k 个合法分子中不同分了比例，用于确定模型是否陷入局部最优点。
- **Novelty** 表示生成分子中未出现在训练集中分子的比例，Novelty 较低就意味着模型过拟合。
- **Filters** 表示生成分子中通过过滤器的分子比例。在构建训练集时，过滤器用于排除非目标的结构，Filters 用于评估模型是否学习到过滤器约束。
- **Fragment similarity (Frag)** 用于比较生成分子与测试集分子的片段相似性。首先将分子切割为 BRICS 片段，接着对比片段的余弦相似度：
    $$
    \mathrm{Frag}(G,R)=\frac{\sum_{f\in F}\left[c_f(G)\cdot c_f(R)\right]}{\sqrt{\sum_{f\in F}c^2_f(G)}\sqrt{\sum_{f\in F}c^2_f(R)}}
    $$
    其中 $c_f(A)$ 表示片段 $f$ 在数据集 $A$ 中出现的次数，$G$ 表示生成分子，$R$ 表示测试集分子。
- **Scaffold similarity (Scaff)** 与片段相似性类似，但是是使用 RDKit 的 Bemis–Murcko 分子架算法将分子分割为分子骨架，计算分子骨架的相似性：
    $$
    \mathrm{Scaff}(G,R)=\frac{\sum_{s\in S}\left[c_s(G)\cdot c_s(R)\right]}{\sqrt{\sum_{s\in S}c^2_s(G)}\sqrt{\sum_{s\in S}c^2_s(R)}}
    $$
    Scaff 用于表示出现在生成分子与测试数据中的分子骨架相似程度。
- **Similarity to a nearest neighbor (SNN)** 计算了生成分子 $m_G$ 分子指纹与其在测试数据中最近邻分子 $m_R$ 的来均谷本相似性 $T(m_G,m_R)$：
    $$
    \mathrm{SNN}(G,R)=\frac{1}{|G|}\sum_{m_g\in G}\max_{m_R\in R}T(m_G,m_R)
    $$
    SNN 使用分子的摩根指纹计算生成分子与测试数据中分子的相似程度。
- **Internal diversity (IntDiv<sub>p</sub>)** 在生成分子数据中评估化学多样性：
    $$
    \mathrm{IntDiv}_p(G)=1-\sqrt[p]{\frac{1}{|G|^2}\sum_{m_1,m_2\in G}T(m_1,m_2)^p}
    $$
    若 IntDiv<sub>p</sub> 较小，内部多样性低，表明可能模型发生了模式崩塌。
- **Fréchet ChemNet Distance (FCD)** 定义为
    $$
    \mathrm{FCD}(G,R)=||\mu_G-\mu_R||^2+\mathrm{Tr}\left[\Sigma_G+\Sigma_R-2(\Sigma_G\Sigma_R)^{1/2}\right]
    $$
    其中 $\mu$ 是相应数据集的平均向量，$\Sigma$ 是相应的协方差矩阵。FCD 同时考虑了生成分子的化学和生物性质，FCD 也与其他指标相关，主要用于调试模型的超参数，FCD 越小时模型表现越好。
- **Properties distribution** 使用 RDKit 计算了分子的分子量、LogP、SA 分数和 QED，生成相应的特征分布（如下图），通过计算生成分子各特征分布与目标特征分布间的 Wasserstein 距离，就够评估模型是否有效学习到了训练集中的特征。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8453?authkey=ALYpzW-ZQ_VBXTU)

## 结论

文章提出了一套评估分布学习模型的标准指标 MOSES，使用相同训练数据训练了目前已经提出多种分子生成模型，利用 MOSES 评估不同分子生成模型，测试结果表明 MOSES 能够全面评估不同分子生成模型表现，发现分子生成任务中存在的问题。MOSES 提供了大量指标满足了分子生成任务的需求，目前是分子生成研究中的标准工具。