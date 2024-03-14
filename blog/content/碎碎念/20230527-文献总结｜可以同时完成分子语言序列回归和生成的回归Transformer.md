title: 文献总结｜可以同时完成分子语言序列回归和生成的 Regression Transformer
slug: summary-doi.org/10.1038/s42256-023-00639-z
date: 2023-05-27
tags: Literature Summary, CADD, Transformer
summary: 本文介绍于 2023 年 IBM 研究团队发表在 *Nature Machine Intelligence* 上的一篇文章，文章原标题为 Regression Transformer enables concurrent sequence regression and generation for molecular language modelling，文章提出了一种可以同时处理序列中的数值与文本并完成回归与生成的多任务的 Transformer 模型。

<i class="fa-solid fa-arrow-up-right-from-square"></i> [doi.org/10.1038/s42256-023-00639-z](https://doi.org/10.1038/s42256-023-00639-z)

本文介绍于 2023 年 IBM 研究团队发表在 *Nature Machine Intelligence* 上的一篇文章，文章原标题为 Regression Transformer enables concurrent sequence regression and generation for molecular language modelling，文章提出了一种可以同时处理序列中的数值与文本并完成回归与生成的多任务的 Transformer 模型。

基于 Transformer 的模型是化学任务中常用的模型，但由于 Transformer 最早是用于自然语言处理的模型，难以处理回归任务，这些模型只能完成性质预测或条件分子生成，无法同时完成指定结构的生成和性质预测。若要实现有约束的分子生成，即根据指定的性质生成分子，则不得不通过在多个模型间传递参数再得到反馈的方法不断调节并得到目标的分子，如下图中 **a** 所示。

文章尝试将回归任务融入到文本序列建模的过程中，提出了一种可以同时处理序列中的数值与文本并完成回归与生成的多任务模型，称为 回归 Transformer（Regression Transformer, RT）。在实验部分，文章使用化学领域中常见的分子生成、性质预测、化学反应预测、生物领域中蛋白质性质预测以及自然语言处理中的文本生成等多种任务测试了模型效果，证明 RT 是一种可以通用于多种任务且可以同时完成序列回归和生成的模型。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!9166?authkey=ALYpzW-ZQ_VBXTU)

## 方法

### 模型

Transformer 原为由左至右逐次由前一个 token 预测下一个 token 的自回归模型，而在分子语言，如 SMILES 中，序列中各原子的顺序是没有特定意义的，序列中的原子也并非由前一个原子决定，因此文章选择使用非自回归模型。BERT、XLNet 都是 Transformer 的变种，BERT 使用掩码的方式随机掩盖序列中的 token，并根据周围的 token 预测被掩盖的 token，因为这个过程使用周围信息编码掩盖的 token，这类模型称为自编码模型。

XLNet 结合了自回归模型与自编码模型的优势，尽管 XLNet 还是由左至右预测 token，但它使用排列置换的方法将随机选择的待预测 token 放至序列末端，与 BERT 的掩码机制实际上相同，称为排列语言模型（Permutation language modeling, PLM）。文章使用 XLNet 作为主要的模型。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!9167?authkey=ALYpzW-ZQ_VBXTU)

#### 数值编码器

如上图所示，输入的数据格式为 `<ESOL>-2.92|SMILES`，`<ESOL>` 标识了预测的性质，`-2.92` 为该性质的数值。由于 Transformer 无法识别数值，会将其识别为数字字符，文章设计了数值编码器（numeric encoder, NE）获取数值信息。

先将 `-2.92` 分为 `_-_` `_2_0_` `_._` `_9_-1_` `_2_-2_` 几个 token，其中的 `_-_` 与 `_._` 分别表示负号与小数点，数字 `9` 就以 `_9_-1_` 表示，其中 `9` 表示数值为 9，`-1` 表示该值位于十分位（10<sup>-1</sup>）。

对于数值 token $t_{v,p}$，$v$ 表示该 token 的数值，$p$ 表示该 token 数值的位置，词嵌入的第 $j$ 维按下式计算：

$$
\mathrm{NE_{Float}}(v,p,j)=(-1)^j\cdot\frac{v\cdot 10^p}{j+1}
$$

然后与 SMILES 的常规词嵌入一起加上位置编码进入 XLNet 中进行计算。

#### XLNet

输入 RT 的 $\boldsymbol{x}$ 是由 $k$ 个性质 token $[\boldsymbol{x}^p]_k$ 和 $l$ 个文本 token $[\boldsymbol{x}^t]_l$ 拼接而成，即

$$
\boldsymbol{x}=[\boldsymbol{x}^p,\boldsymbol{x}^t]_T=[x^p_1,\cdots,x^p_k,x^t_1,\cdots,x^t_l]
$$

其中 $T=k+l$，为整个序列的 token 数量。

**PLM objective**（$\mathcal{J}_\mathrm{PLM}$）：在原始的 XLNet 中，输入的序列就要做 $T!$ 次的排列，将掩盖的 token 放置到序列末端，训练目标是使模型能够预测出掩盖的 token。如上图中 PLM objective 所示，由于这种训练方法是随机选取，打断了整体的 $\boldsymbol{x}^p$ 或 $\boldsymbol{x}^t$，因而不适合该任务，仅用于预训练。

**Property prediction objective**（$\mathcal{J}_\mathrm{P}$）：对于分子性质预测的回归任务，将表示分子性质的 $\boldsymbol{x}^p$ 全部掩盖并排列置换位置，使用分子的文本 $\boldsymbol{x}^t$ 预测被掩盖的分子性质。

**Conditional text generation objective**（$\mathcal{J}_\mathrm{G}$）：对于分子生成任务，正与上述过程相反，将表示分子的 $\boldsymbol{x}^t$ 全部掩盖。

**Self-consistency (SC) objective**（$\mathcal{J}_\mathrm{SC}$）：为了使 RT 能够同时完成回归和生成任务，文章设计了该训练目标：

$$\mathcal{J}_\mathrm{SC}=\mathcal{J}_\mathrm{G}(\boldsymbol{x})+\alpha\cdot\mathcal{J}_\mathrm{P}(\hat{\boldsymbol{x}})$$

其中 $\alpha$ 为权重，$\hat{\boldsymbol{x}}=[\boldsymbol{x}^p,\hat{\boldsymbol{x}}^t]$ 为生成的样本。该训练任务就是先使用分子性质生成分子，再用生成的分子预测其性质。

### 数据

使用 SELFIES 作为分子表示，许多研究表明，相比 SMILES，SELFIES 在分子生成任务上更具有优势。

Synthetic QED dataset：由 ChEMBL 得到的约 160 万个分子，约 140 万用于训练，1000 条数据用于验证，10000 条数据用于测试。

## 实验

文章中使用 RT 在化学反应、蛋白质性质预测等任务上测试了模型性能，这里仅以分子生成与分子性质预测的任务为例。

在 QED 数据集上，先使用 $\mathcal{J}_\mathrm{PLM}$ 训练模型，至验证集数据的指标收敛后，再每 50 轮用 $\mathcal{J}_\mathrm{P}$、$\mathcal{J}_\mathrm{G}$ 或 $\mathcal{J}_\mathrm{SC}$ 轮流微调（Alternate），不同模型设定的结果如下图所示。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!9168?authkey=ALYpzW-ZQ_VBXTU)

从实验结果中可以看出，（1）SELFIES 在生成任务上更有优势，但在回归任务上稍逊于 SMILES；（2）不论是回归还是生成任务，预训练使模型的表现提升；（3）设计的数值编码器有利于模型识别数值信息，提升模型表现；（4）在微调阶段轮流使用不同的训练任务，使模型在回归和生成两种任务上的泛化能力更好，在回归和生成单个任务上都具有与单任务模型接近甚至更优的表现。

能够处理回归与生成两种任务的模型也可以用于实现分子的性质优化，具体过程是设定一个 seed 分子以及目标的性质（primer），模型随机掩盖分子中 token 再通过 primer 将 token 预测出来，得到优化后的新分子，再通过新分子计算其性质的预测值，下图展示了在两种不同的数据集上微调得到的模型实现分子性质优化的样例。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!9169?authkey=ALYpzW-ZQ_VBXTU)

## 结论

文章提出了回归 Transformer（RT）模型，该模型以 XLNet 为主要的结构，文章增加了数值编码器用于获取数值信息，并设计了不同的训练模式使模型在预训练-微调后能够完成数值回归与序列生成两种不同的任务。RT 设计用于数值回归与序列生成，因此也可以用于蛋白性质预测、反应预测等。