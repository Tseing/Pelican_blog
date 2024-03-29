title: 文献总结｜ChemistGA：用于实际药物发现的可合成分子生成算法
slug:  summary-doi.org/10.1021/acs.jmedchem.2c01179
date: 2022-10-29
tags: Literature Summary, CADD, Algorithm
summary: 本文介绍于 2022 年发表在 Journal of Medicinal Chemistry 上的一篇文章，文章原标题为 ChemistGA: A Chemical Synthesizable Accessible Molecular Generation Algorithm for Real-World Drug Discovery，文章改进了传统的遗传算法，使其在药物分子生成的任务上具有比深度学习更优的表现效果。

<i class="fa-solid fa-arrow-up-right-from-square"></i> [doi.org/10.1021/acs.jmedchem.2c01179](https://doi.org/10.1021/acs.jmedchem.2c01179)

本文介绍于 2022 年发表在 *Journal of Medicinal Chemistry* 上的一篇文章，文章原标题为 ChemistGA: A Chemical Synthesizable Accessible Molecular Generation Algorithm for Real-World Drug Discovery，文章改进了传统的遗传算法，ChemistGA 算法在药物分子生成的任务上具有比深度学习更优的表现效果。

## 引言

基于深度学习的分子生成方法大多都是数据驱动型的方法，这些模型通常需要大量的数量用于训练模型，从而生成特定结构和特征的分子。而传统的机器学习方法，例如遗传算法，不需要大量数据，也不需要经过训练过程，只需要少量的分子数据就能生成大量分子。因此，在深度学习席卷所有行业的今天，遗传算法等机器学习方法仍具有优势。

遗传算法借鉴了生物学中遗传的概念，从初始种群（初始数据）出发，在两两个体间发生数据的交叉、突变，得到子代，再以子代作为父代不断繁衍。在繁衍的过程中，引入适应函数，适应性函数衡量了个体是否适应环境（满足目标要求），并淘汰低于阈值的个体。繁衍与淘汰的过程不断迭代，直至满足结束条件（迭代次数或子代与父代间适应性函数的差异），最终的种群就是问题的最优解。

但将遗传算法用于分子生成任务仍有一定问题，例如，染色体交叉和突变的过程通常是随机的，若将分子的片段随机交换，很容易生成大量无法合成的分子。

因此，文章结合化学合成模版和逆合成预测等模块改进了遗传算法，构造了适用于分子生成任务的模型，取得了良好的效果。

## 方法

### 交叉

ChemistGA 的交叉步骤不是随机的交换，而是使用了反应预测模型 molecular transformer（MT），MT 以两个分子的为输入（`SMILES.SMILES`），输出一系列分子。MT 已经经过专门化学反应数据的预训练，因此它会基于反应事实预测两个分子相互反应可能产生的结果。就算两个分子不能反应，MT 也能给出一系列具有两分子结构特征的分子，从而避免生成不可合成的分子。

### 反交

使用 MT 作为分子交叉的模型无法避免最后的结果陷入局部最优解，因此引入了反应的方法。具体来说，就是在每一子代中插入一部分初始种群中的个体。

### 适应性函数

文章使用了两种适应性函数，一种是连续适应性函数，另一种是离散适应性函数。连续适应性函数可以理解为对分子的打分，涉及 QED、SA 以及生物活性等指标。离散适应性函数也与之类似，唯一的不同在于使用 1 或 0 表示分子是否满足指标的要求。

### 数据集

| 靶点  | negative / positive | 来源 |
|------|---------------------|------|
| DRD2 | 100000 / 7219       | [Olivecrona et al.](https://doi.org/10.1186/s13321-017-0235-x) |
| JNK3 | 50000 / 2665        | [Li et al.](https://doi.org/10.48550/arXiv.1806.02473) |
| GSK3β| 50000 / 740         | [Li et al.](https://doi.org/10.48550/arXiv.1806.02473) |

### 活性预测模型

文章针对 DRD2、JNK3 和 GSK3β 构建了两利活性预测模型，一种模型预测结果较为准确，另一种模型较不准确。

- 准确的活性预测模型：随机森林分类
- 不准确的活性预测模型：3 层决策树分类

### 指标

- **Synthesizability Rate**：随机选择生成的 5000 个分子，使用 Retro* 算法预测其逆合成过程，可完成的分子占比就为 Synthesizability Rate。
- **Mismatch Rate**：随机选择生成的 5000 个分子，使用 RECAP 算法获取分子片段，将生成分子的片段库与商用分子片段库对比得到 Mismatch Rate。
- **Diversity**：$\mathrm{diversity}=1-\frac{2}{n(n-1)}\sum\mathrm{sim}(X,Y)$，其中 $\mathrm{sim}(X,Y)$ 为谷本距离。
- **Novelty**：$\mathrm{novelty}=\frac{1}{n}\sum1[\mathrm{sim}(G,G_\mathrm{SNN}<0.4>)]$
- **Scaffolds**：使用 Murcko 化合物骨架数据计算骨架数量。

## 结果与论论

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!7893?authkey=ALYpzW-ZQ_VBXTU)

ChemistGA 的主要工作流程是如果所示，首先计算初始种群的适应性函数，根据适应性函数选择其中的部分分子交叉，再经过突变过程后，重新计算分子的适应性函数，不断迭代。与 ChemistGA 不同，R-ChemistGA 每个周期前 4 次使用不准确的活性预测模型计算适应性函数，而第 5 次使用准确模型。

这是由于在现实情况下，我们很难得到完全准确且数据量大的化合物活性数据库，引入的噪声的目的就是为了模拟了这种现实状况。

### 实验方案 1

实验方案 1 分别使用 ChemistGA 与 GB-GA（传统遗传算法）针对 JNK3 与 GSK3β 生成分子，比较二者结果。

在生物活性（通过预测模型）、QED 以及 SA 几个方面，ChemistGA 都生成了更好的结果，其中的重要原因就是 GB-GA 等传统遗传算法的交叉过程是随机的，不可避免地生成了大量无效分子。

### 实验方案 2

实验方案 2 的目标是评估 ChemistGA 基于现实活性分子生成药物分子的能力，任务 1 针对于 DRD2 靶点，任务 1 针对于 JNK3 与 GSK3β 靶点。

分别从 REINVENT、GB-GA、RationaleRL 和 ChemistGA 几种模型中随机选择 5000 个分子用于比较结果。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!7894?authkey=ALYpzW-ZQ_VBXTU)

从表格上半部分的结果中，可以看出，ChemistGA 在各方面具有比较均衡结果，也就是 ChemistGA 在生成分子的多样性与可合成性间找到了平衡。而 REINVENT 产生的结果明显多样性不足，GB-GA 的结果可合成性低。任务 2 的结果也类似。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!7896?authkey=ALYpzW-ZQ_VBXTU)

### 适应性函数的影响

以上实验中的遗传算法（GB-GA 与 ChemistGA）使用的都是连续适应性函数，接下来将适应性函数换为离散适应性函数，表格的下半部分即为结果，以（F）表示。

在使用离散适应性函数后，生成结果有了一定程度上的提升，其本质原因是使用离散适应性函数相当于引入了一定的随机性。例如，在使用连续适应性函数的情况下，若有评分为 3.65、3.64 与 3.63 的三个分子，算法就会选择 3.65 与 3.64 两个分子作为父代，尽管 3.63 的分子也具有近似相同的评分，但也会被淘汰，所以该分子的结构片段就很难进入到最终的生成结果中。若使用离散适应性函数，相应的打分就为 4、4、4，那么算法就将随机选择两个分子作为父代，最后的结果也会具有更大的多样性和可合成性。

### R-ChemistGA

R-ChemistGA 与 ChemistGA 唯一不同之处在于 R-ChemistGA 使用不准确的活性预测模型引入了噪声，用于模拟真实世界中的数据。

R-ChemistGA 产生的结果在各方面都与 ChemistGA 相当，同时具有更高的 novelty，说明 ChemistGA 算法不仅足够稳健，可以用不完全准确的真实数据集训练，同时还能通过使用不准确的活性预测模型的方法提升生成分子的 novelty。

可以将 R-ChemistGA 工作流程中的 5 次循环看作 1 个周期，每个周期中，前 4 次循环使用用不准确的活性预测模型淘汰分子，第 5 次循环使用准确的活性预测模型淘汰分子。

R-ChemistGA 的生成结果具有更高 novelty 的原因就在于，预测模型认为没有活性的分子会被淘汰，不会使其产生子代，但很重要的一个事实就是，没有活性的分子通过交叉得到的子代可能具有活性。因此，R-ChemistGA 相当于放宽了淘汰的标准，使其尽可能产生多的分子，在第 5 次循环才用更严格的标准淘汰掉没有活性的分子。

## 结论

文章提出了两种分子生成算法，分别是 ChemistGA 与 R-ChemistGA。这两种算法都基于机器学习中的遗传算法，改进了遗传算法生成的分子难于合成等问题，让遗传算法在分子生成领域也能发挥其独特的优势。

ChemistGA 与 R-ChemistGA 的主要特点就是不需要大量数据用于训练模型，算法足够稳健，可以使用不是完全准确的真实活性数据用于分子生成，生成的分子具有较高的多样性与可合成性。