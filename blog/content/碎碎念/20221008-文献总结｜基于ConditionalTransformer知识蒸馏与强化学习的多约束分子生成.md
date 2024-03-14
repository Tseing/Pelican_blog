title: 文献总结｜基于 Conditional Transformer、知识蒸馏与强化学习的多约束分子生成
slug:  summary-doi.org/10.1038/s42256-021-00403-1
date: 2022-10-08
tags: Literature Summary, CADD, Transformer
summary: 本文介绍了来自浙江大学侯廷军老师的工作，文章原标题为 Multi-constraint molecular generation based on conditional transformer, knowledge distillation and reinforcement learning，于 2021 年发表在 Nature Machine Intelligence 上。文章基于 transformer 建立了分子生成模型，并借助知识蒸馏与强化学习算法，提出了一种新的分子生成模型。

本文介绍了来自浙江大学侯廷军老师的工作，文章原标题为 Multi-constraint molecular generation based on conditional transformer, knowledge distillation and reinforcement learning，于 2021 年发表在 *Nature Machine Intelligence* 上。文章基于 transformer 建立了分子生成模型，并借助知识蒸馏与强化学习算法，提出了一种新的分子生成模型，该模型能够顺利完成药物分子生成这样的多约束优化问题。

<i class="fa-solid fa-arrow-up-right-from-square"></i> [doi.org/10.1038/s42256-021-00403-1](https://doi.org/10.1038/s42256-021-00403-1)

## 引言

在药物分子生成的任务中，目标分子既需要有高类药性、低毒性，其结构又需要尽可多样和新颖，药物分子生成就是这样一个多约束优化问题。

文章针对该问题提出了一种新的分子生成方法——MCMG（Multi-Constraint Molecular Generation），鉴于 conditional transformer 在自然语言处理中的优势，MCMG 将其作为分子生成模型，接着使用知识蒸馏降低模型复杂程度，简化后的模型更便于使用强化学习 fine-tune，最后得到由 RNN 构成的代理模型。

## 方法

### 编码

MCMG 使用 SMILES 作为分子的表示方式。

### 数据来源

- 训练数据来自于 [Olivecrona et al.](https://doi.org/10.1186/s13321-017-0235-x) 从 ChEMBL 中挑选的数据。

- 生物活性数据：

    | 靶点  | negative / positive | 来源 |
    |------|---------------------|------|
    | DRD2 | 100000 / 7219       | [Olivecrona et al.](https://doi.org/10.1186/s13321-017-0235-x) |
    | JNK3 | 50000 / 2665        | [Li et al.](https://doi.org/10.48550/arXiv.1806.02473) |
    | GSK3β| 50000 / 740         | [Li et al.](https://doi.org/10.48550/arXiv.1806.02473) |

### 活性预测模型

| 靶点 | 算法       | 来源 |
|-----|------------|-----|
| DRD2 | 支持向量机 | [Olivecrona et al.](https://doi.org/10.1186/s13321-017-0235-x) |
| JNK3 | 随机森林   | [Jin et al.](https://doi.org/10.48550/arXiv.2002.03244) |
| GSK3β| 随机森林   | [Jin et al.](https://doi.org/10.48550/arXiv.2002.03244) |

### 分子生成模型

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7714?authkey=ALYpzW-ZQ_VBXTU)

**1. 先验模型**：生成具有目标特征的分子。

在先验模型中添加了约束码 $c$，约束码 $c$ 是一个 n 位字符串，用于表示分子是否满足了 n 个约束。先验模型的训练目标就是以 `\s` + SMILES 为输入，以 SMILES + `\EOS` 为输出，通过 $c$ 表示分子状态，输出最优分子。先验模型通过这个过程中学习到的条件概率分布生成预期分子：

$$p(x|c)=\prod^n_{i=1}p(x_i|x_{<i},c)$$

**2. 蒸馏模型**：简化 transformer 结果，便于 RL 优化。

蒸馏模型的结构是具有三层循环单元的 RNN，蒸馏模型分为两种模式，分别是 DL（Distilled Likelihood） 与 DM（Distilled Molecules）。

- DL: 使用先验模型中生成的字符作为训练集，与先验模型的训练过程类似，首先输入 `\s` 与 $c$，再逐个输入先验模型生成的下一个字符，直至到达 `\EOS`。在这个过程中，模型能够学习到准确的概率。最后经过 fine-tune 的模型就称作 MCMGL。
- DM： 直接使用先验模型中生成的分子集作为训练集，无法学习到准确的概率。最后经过 fine-tune 的模型就称作 MCMGM。

此外，文章还提出了 semi-DM 与 semi-MCMGM 模型，这部分模型的训练集由满足一部分约束条件的分子构成，例如 QED 与 SA，用于增加计算效率。

**3. 代理模型**：使用 RL 算法 fine-tune 预先训练好的神经网络。

在该步骤中，使用 REINVENT 中的 RL 算法 fine-tune 蒸馏模型。具体来说，RL 将模型产生 SMILES 视作行为，接着根据每个行为给予一定的奖惩，代理模型最终学习到状态 $S$ 下行为 $A$ 的条件概率 $p(A|S)$。

在代理模型生成的分子中取样，记录其概率 $\log p(A)_{\mathrm{agent}}$，将生成的分子输入蒸馏模型得到概率 $\log p(A)_{\mathrm{middle}}$，通过下式计算增广概率：

$$\log p(A)_{\mathrm{aug}}=\log p(A)_{\mathrm{middle}}+\sigma S(A)$$

式中 $S(A)$ 是对分子的打分，可以通过活性预测模型得到。代理模型的损失函数就是

$$\mathrm{Loss}=[\log p(A)_{\mathrm{aug}}-\log p(A)_{\mathrm{agent}}]^2$$

### 模型评估

对于模型的评估从两方面展开：

- **实验 1**：评估优化后各个最佳模型的能力，即评估模型最后生成的分子的各方面指标；
- **实验 2**：评估各模型在相同条件下生成分子的性能与质量，即保存了全过程中生成的分子用于评估。

文章中将针对 DRD2 生成活性分子的工作称为任务 1，针对 JNK3 与 GSK3β 的称为任务 2。

### 评价指标

文章中对生成分子的评价使用了 [Jin et al.](https://doi.org/10.48550/arXiv.2002.03244) 提出的标准指标与 MOSES 指标。

标准指标：

- Success：若 QED、SA、对受体活性的预测值都在指定范围内，则认为该分子属于 success，successful 分子占比即为 success rate。
- Real success：生成分子中满足 success 条件的独特（unique）分子占比。
- Diversity：在 successful 分子中基于摩根指纹两两评估谷本距离 $\mathrm{sim}(X,Y)$，
    $$\mathrm{Diversity}=1-\frac{2}{n(n-1)}\sum_{X,Y}\mathrm{sim}(X,Y)$$
- Novelty：对于每个 successful 分子 $G$，在训练集中取其最近邻 $G_{\mathrm{SNN}}$，
    $$\mathrm{Novelty}=\frac{1}{n}\sum_G\mathrm{sim}(G,G_{\mathrm{SNN}})$$

生成分子集为 $G$，测试集为 $T$，MOSES 指标：

- $\mathrm{Novelty}=1-\frac{|\mathrm{set}(G\cap T)|}{G}$
- $\mathrm{IntDiv}(G)=1-\frac{1}{|\mathrm{set}(G)|^2}\sum_{(X,Y)\in\mathrm{set}(G)}\mathrm{sim}(X,Y)$
- Frag：衡量训练集与测试集中不同的分子片段出现频率，用 RDKit 的 BRICS 函数计算。
- SNN：生成分子中分子与训练集中其最近邻分子的平均谷本系数。

## 结果

### Transformer 相比 RNN 的优势

为了对比 RNN、conditional RNN 和 conditional transformer 性能差别，经过训练后，在各模型中抽取相同数量的生成分子进行评估。

RNN 的 success 占比为 0%，这说明 RNN 模型生成的分子无法同时满足四种约束，c-RNN 虽然生成了一定数量的 successful 分子，但仍是低于 c-transformer 模型。这是因为 c-transformer 模型并不是像 RNN 模型那样依赖于输入的上一个词再输出下一个词，c-transformer 模型将句子看作整体进行计算，不仅提高了计算性能，还有效避免了长期依赖问题。

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7715?authkey=ALYpzW-ZQ_VBXTU)

### 两种蒸馏模式的对比

文章对比了两种蒸馏模式生成分子的结果，其中 DM 生成的 successful 分子显著少于 DL，但 DM 模式具有更高的 Frag 与 IntDiv，DM 模式可能构建了一个更大的化学空间，生成了更多新颖的分子。

文章提出了以下假设，将灰色的椭圆区域视作无条件的化学空间，其中的红点代表需要寻找的分子。DL 模式得到的模型可以看作为蓝色区域，在这个区域中红点的密度更高（success 比例更大），但区域面积较小，在后续 RL 过程中容易陷入局部最优点，而 DM 模式得到的模型可以看作为绿色区域，虽然红点密度比蓝色区域更低，但是相比于灰色区域还是更高的，因此也可以使用后续 RL 过程优化。

![chemical space](https://storage.live.com/items/4D18B16B8E0B1EDB!7716?authkey=ALYpzW-ZQ_VBXTU)

文章计算了 RNN、DM、DL 和 semi-DM 模型生成分子的平均负对数似然（Negative Log-Likelihood, NLL），平均 NLL 越小，生成 SMILES 序列的随机性也越小，分子多样性越低，相应化学空间也更小。

结果表明 DL 模型的平均 NLL 最低，DM 次之，semi-DM 再次之，验证了上文的假设。

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7717?authkey=ALYpzW-ZQ_VBXTU)

### 模型评估

实验 1 的目的是评估模型经过若干过程的优化后，最终生成的分子的各方面指标。模型不断优化得到最优模型的过程可以看作模型相应的化学空间不断缩小，化学空间中预期分子密度达到设定值的过程，左图中橙色区域就代表最优模型。

实验 2 的目的是评估各模型在优化过程中生成分子的质量，也就是评估化学空间缩小的过程中涉及的分子，如右图中的路径所示。

![模型评估](https://storage.live.com/items/4D18B16B8E0B1EDB!7718?authkey=ALYpzW-ZQ_VBXTU)

实验 1 的结果列举在表格中，其中 MCMGL（DL）具有接近 100% 的 success 比例，但该模型生成分子的 Novelty 与 Div 都很低，REINVENT2.0 模型也有同样的问题。这不仅是因为训练数据集中活性分子占比少，更是因为 MCMGL 经过 RL 优化后的化学空间很小，在这一点上，化学空间更大的 MCMGM 与 semi-MCMGM 具有更大优势。

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7719?authkey=ALYpzW-ZQ_VBXTU)

实验 2 评估了在 RL 优化过程中每个步骤生成的一部分分子。在初始阶段，MCMGM、MCMGL 和 REINVENT2.0 模型就生成了大量 successful 分子，在 1000 步后，REINVENT 和 semi-MCMGM 模型生成的分子迅速增长。其原因就是 REINVENT 和 semi-MCMGM 模型具有更大的化学空间，不会受制随着 RL 过程推进而越一越小的化学空间。在后期，MCMGL 无法生成新颖的 successful 分子，REINVENT2.0 显然也有相同的趋势，这是因为 RL 优化进入了局部最优点。

除此之外，文章还对模型生成的分子骨架做了相似性评估，其中 MCMGM 和 semi-MCMGM 模型在生成新颖骨架上同样具有优势。

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7720?authkey=ALYpzW-ZQ_VBXTU)

## 结论

文章提出了一种运用了 conditional transformer、知识蒸馏与强化学习的分子生成方法，经过一系列评估，MCMG 方法能够生成更多独特且满足目标条件的分子，在一系列评估中，MCMG 模型与已知的活性分子具有最低的相似度，能够完成针对文中 3 个靶点的活性分子生成任务。在一系列模型评估中，MCMG 模型具有显著优势。

## 另：Transformer 的介绍

transformer 是一种应用在自然语言处理中的模型，transformer 解决了 RNN 存在的一系列缺点。对于 RNN（或 LSTM）来说，计算的过程是顺序的，那么，

1. 第 $t$ 步的计算依赖于第 $t-1$ 步的计算结果，不能并行计算；
2. 顺序计算导致长时间前的信息丢失，尽管 LSTM 可以缓解这一问题，但对于特别长期的记忆仍然会失效，也就是长期依赖问题。

而对于 transformer 来说，

1. 使用了注意力机制，序列中任意两个位置之间的距离为常量；
2. 并非顺序计算，具有并行能力。

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7721?authkey=ALYpzW-ZQ_VBXTU)

transformer 的结构可以大致分为 Encoder 与 Decoder 两个部分。

### Encoder

#### Self-Attention 机制

`输入的单词` → `映射为向量并添加位置编码` → `得到 Input Embedding (x)` → `通过矩阵乘法得到 q,k,v`

矩阵乘法的的运算过程为

$$q=xW^Q,\,k=xW^K,\,v=xW^V$$

$q$ 代表 query，$k$ 代表 key，$v$ 代表 value，也就是需要用 query 去寻找更匹配的 key，因为数量积可以表示两向量的相似程度，匹配程度就为

$$\mathrm{score}=q\cdot k_i=qk^\mathrm{T}_i$$

假设输入的句子中包含两个单词，需要得到的中间量 $z$ 通过下式计算：

$$\begin{align}
    z_1=\theta_{11}v_1+\theta_{12}v_2\\
    z_2=\theta_{21}v_1+\theta_{22}v_2
\end{align}$$

权值 $\theta$ 可以通过下式计算：

$$(\theta_{11},\theta_{12})=\mathrm{softmax}\left(\frac{q_1k^\mathrm{T}_1}{\sqrt{d_k}},\frac{q_1k^\mathrm{T}_2}{\sqrt{d_k}}\right)$$

其中 $d_k$ 是向量的维度，将上述运算转为矩阵形式，也就是

$$\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^\mathrm{T}}{\sqrt{d_k}}\right)V$$

self-attention 机制的目的就是在句子中寻找对自己影响力大的词。

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7722?authkey=ALYpzW-ZQ_VBXTU)

#### Multi-headed Attention

使用不同的矩阵 $W^Q$，$W^K$，$W^V$ 就能得到不同的 $Q$，$K$，$V$，multi-headed attention 就是使用了不同的 $Q$，$K$，$V$，产生若干不同的 $z_{i1},z_{i2},\cdots,z_{in}$，然后在全连通网络中，将其拼接为一个长向量再乘以矩阵 $W^O$，得到形状符合预期的向量 $z_i$。

使用不同的矩阵 $W^Q$，$W^K$，$W^V$ 的目的就是从不同角度（特征）计算 attention，例如在某一角度 panda 与 bamboo 具有高关联性，而另一个角度，panda 与 China 也有很高关联，那么 multi-attention 的作用就是将这些不同角度的 attention 综合起来。

![!NoCaption](https://storage.live.com/items/4D18B16B8E0B1EDB!7723?authkey=ALYpzW-ZQ_VBXTU)

### Decoder

Decoder 部分具有与 Encoder 相类似的注意力层，但 Decoder 部分除了接收前一步骤的输出 $x$ 以外，还要接收 Encoder 部分的结果 $m$。可以这么理解，Decoder 部分将 $m$ 视作 key 和 value，以前一步的输出 $x$ 作为 query，具体过程如下：

1. Decoder 输入 Encoder 对整个句子的运算结果和开始符号 `\s`，Decoder 产生预测 `I`:
2. Decoder 输入 Encoder 对整个句子的运算结果和 `\s I`，产生预测 `am`；
3. Decoder 不断产生预测直至生成 `\EOS`，句子结束。

![Decoder](https://storage.live.com/items/4D18B16B8E0B1EDB!7724?authkey=ALYpzW-ZQ_VBXTU)

---

## References

- [Self-Attention和Transformer - GitBook](https://luweikxy.gitbook.io/machine-learning-notes/self-attention-and-transformer)
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)