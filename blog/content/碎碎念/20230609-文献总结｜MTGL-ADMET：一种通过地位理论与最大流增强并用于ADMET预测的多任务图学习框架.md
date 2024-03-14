title: 文献总结｜MTGL-ADMET：一种通过地位理论与最大流增强并用于 ADMET 预测的多任务图学习框架
slug: summary-doi.org/10.1007/978-3-031-29119-7_6
date: 2023-06-09
tags: Literature Summary, CADD, GNN
summary: 本文介绍于 2023 年 西北工业大学发表在 RECOMB 2023 上的一篇文章，文章原标题为 MTGL-ADMET: A Novel Multi-task Graph Learning Framework for ADMET Prediction Enhanced by Status-Theory and Maximum Flow，文章通过地位理论与最大流构造了由主要任务与辅助任务构成的多任务模型，相比单任务模型在预测准确性上有很大提高。

<i class="fa-solid fa-arrow-up-right-from-square"></i> [doi.org/10.1007/978-3-031-29119-7_6](https://doi.org/10.1007/978-3-031-29119-7_6)

本文介绍于 2023 年 西北工业大学发表在 RECOMB 2023 上的一篇文章，文章原标题为 MTGL-ADMET: A Novel Multi-task Graph Learning Framework for ADMET Prediction Enhanced by Status-Theory and Maximum Flow，文章通过地位理论与最大流构造了由主要任务与辅助任务构成的多任务模型，相比单任务模型在预测准确性上有很大提高。

对于 ADMET 多种性质的预测，一般的方法是单任务学习，也就是一个模型只完成一种任务（预测一种性质），这种方法不仅繁琐，而且在缺少真实数据的情况下效果不佳。近年来出现的一种新范式是先通过预训练得到分子的通用表示，再将其用于多任务学习，使用一个模型完成所有预测任务，预训练的步骤弥补了缺少真实数据的问题。

文章认为，现有基于多任务的 ADMET 模型都是通过一个模型完成所有预测任务，这样的共同学习很难保证模型能够共同学习到多种性质的信息，导致效果甚至不如单任务学习。文章设想以一个任务为主要任务，多个其他任务作为辅助任务，并通过地位理论找到最佳的任务搭配，改善模型效果。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!9255?authkey=ALYpzW-ZQ_VBXTU)

## 方法

### 模型

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!9256?authkey=ALYpzW-ZQ_VBXTU)

在文章设计的「一个主要任务，多个辅助任务」模式下，需要通过 3 个步骤找到这最佳的任务搭配，如上图中 **a** 所示。

首先先以各任务为单任务建立模型，例如对任务 $t_w$ 与 $t_k$ 分别建立单任务模型 $\mathcal{S}_w$ 与 $\mathcal{S}_k$，再为其建立多任务模型 $\mathcal{D}_{w,k}$，那么 $t_w$ 对 $t_k$ 的影响就可以表示为

$$
\hat{Z}_{w\rightarrow k}=Z^{(d)}_{k|w}-Z^{(s)}_k
$$

其中 $Z^{(s)}_k$ 就是 $\mathcal{S}_k$ 模型的表现，$Z^{(d)}_{k|w}$ 就是 $\mathcal{D}_{w,k}$ 模型的表现，从而可以得到类似下图中的结果：

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!9257?authkey=ALYpzW-ZQ_VBXTU)

接着根据以上结果将相互增强的任务作为同一组的多任务，再通过地位理论决定各组任务中的主要任务，其他任务作为辅助任务。简单来说，地位理论就是将对模型表现提升最多的任务视为主要任务。

最后通过最大流优化所选择的辅助任务。经过以上步骤，就可以将许多 ADMET 性质的预测任务分组，分别建立多任务模型。

多任务模型的预测过程如上图 **b** 所示，输入的分子通过两层 GCN 提取分子的信息，得到分子 embedding 表示，再在 Task-specific molecular embedding module 中得到适用于特定任务的分子表示。对于辅助任务，分子表示直接通过全连接层得到相应任务的预测结果。对于主要任务，除了针对于本任务的分子表示，还通过 Gating Network 通过可学习的权重融合来自于辅助任务的分子表示（图 **c**），最后得到预测结果。

### 数据

模型所使用的 ADMET 数据来源于各文献中收集到的 24 种性质（18 个分类任务，6 个回归任务），共包含 43291 个类药的化合物。

输入模型的分子以图的形式表示，分子图除了原子信息外，还添加了手性、电荷、芳香性、杂化等信息。

## 结果

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!9258?authkey=ALYpzW-ZQ_VBXTU)

MTGL-ADMET 在 24 种性质上的预测结果如上图所示，括号中的数字代表辅助任务的数量。与其他图模型相比，MTGL-ADMET 在 20 个任务上表现最优，另外 4 个任务上表现仅次于最优。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!9259?authkey=ALYpzW-ZQ_VBXTU)

在消融实验中，文章验证了「主要任务+辅助任务」策略的效果，测试结果如上图所示。与单任务（Single）、随机挑选 5 个辅助任务（Ran-5）和不使用地位理论与最大流而仅挑选对模型提升最大的 5 个辅助任务（Top-5）相比，MTGL-ADMET 在所有性质的预测上表现都是最佳的，说明了文章所设计多任务策略的优势。

最后，文章展示了模型的可解释性，下图的案例展示了化合物结构片段与相应性质的相关性。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!9260?authkey=ALYpzW-ZQ_VBXTU)

## 结论

文章提出了一种用于构建 ADMET 多任务的策略，该策略主要使用地位理论与最大流分析了对主要任务具有增强作用的辅助任务，将主要任务与辅助任务一起构建多任务模型，使模型最后的预测效果好过很多完成类似任务的图模型。

**局限**：文章只评估了多任务模型中主要任务的预测结果，而没有全面评估模型包括辅助任务在内的多个预测结果，文章中的策略可以找到辅助提升主要任务结果的辅助任务，但这样的多任务模型不一定在多个任务上都表现得很好。文章中所测试的 ADMET 数据较少，在 ADMET 性质种类很多时，在两两任务间寻找是否具有性能提升的步骤就会变得繁琐。