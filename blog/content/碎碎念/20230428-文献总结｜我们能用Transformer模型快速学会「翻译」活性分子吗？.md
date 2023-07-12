title: 文献总结｜我们能用 Transformer 模型快速学会「翻译」活性分子吗？
slug: summary-doi.org/10.1021/acs.jcim.2c01618
date: 2023-04-28
tags: Literature Summary, CADD, Transformer
summary: 本文介绍于 2023 年发表在 *Journal of Chemical Information and Modeling* 上的一篇文章，文章原标题为 Can We Quickly Learn to “Translate” Bioactive Molecules with Transformer Models? 文章使用 MMP 数据训练 Transformer，使其生成具有活性的分子，文章结果表明 Transformer 对于未知靶点也能生成活性分子。

<i class="fa fa-external-link"></i> [doi.org/10.1021/acs.jcim.2c01618](https://doi.org/10.1021/acs.jcim.2c01618)

本文介绍于 2023 年发表在 *Journal of Chemical Information and Modeling* 上的一篇文章，文章原标题为 Can We Quickly Learn to “Translate” Bioactive Molecules with Transformer Models? 文章使用 MMP 数据训练 Transformer，使其生成具有活性的分子，文章结果表明 Transformer 对于未知靶点也能生成活性分子。

## 方法

### 数据

文章所使用的分子数据来源于 ChEMBL 29，包含有 950640 个分子。数据集中的分子都由 SMILES 表示，将其输入 MMP 软件匹配其中的相似分子。输出的数据中，每对数据都由两个 SMILES 构成，形成一个 MMP 对，用 SMIRK 表示两个 SMILES 间的化学转化，最后得到了约 5700 万条 MMP 对。

接着文章对得到的 MMP 对数据进一步清洗，主要包括两个步骤：

1. 排除 SMIRK 出现次数少于 $N_1$ 的 MMP 对；
2. 在剩余的 MMP 对中，随机保留 $N_2$ 条数据。

第 1 步的清洗是为了除去数据中出现频率过少的化学转化，因为它们过于特殊，并不能普适地用于所有分子；第 2 步是为了避免数据中的极端偏向影响模型，因为在数据集中，简单的转化（如 -H → -CH<sub>3</sub>）出现频率极高，这会导致模型无法学习到那些复杂的转化。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8914?authkey=ALYpzW-ZQ_VBXTU)

### 模型

文章使用 OpenNMT 构建 Transformer 模型，在 SMILES 数据输入模型前，都将其转化为 SELFIES 形式。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8917?authkey=ALYpzW-ZQ_VBXTU)

在训练过程中，使用 OpenNMT 中默认的损失函数，使用困惑度（perplexity）评估模型训练效果。困惑度是自然语言处理中所使用的评估指标，它定义为 $ppl=\exp(L/N)$，其中 $L$ 为损失函数，$N$ 为全部备选的 token 数量。在自然语言处理中，模型根据前一个 token 预测下一个 token，并将其连成句子，困惑度的意义就是模型在获取前一个 token 的情况下，概率较高的下一个 token 的数量，所以困惑度越小时，表明模型能在目前分布下生成更合理的句子。同样，将其应用于分子生成模型，困惑度就可以表示分枝原子上可以备选的连接原子。

此外，文章测试了模型对未知靶点生成分子的效果。在上一步得到的数据中，分别除去对 COX2、DRD2 或 HERG 有活性的分子，分别用三种数据训练 Transformer，最后得到的各模型对指定靶点「不可知」。文章又将去除掉的活性分子根据活性大小分为前 5% 与后 95% 的子数据集，用后 95% 作为模型输入，测试模型是否能输出前 5% 的分子。

## 实验

#### Transformer 可以为未知靶点生成活性分子

分别从训练数据中除去 COX2、DRD2 或 HERG 的活性分子，训练了 3 个 Transformer 模型，模型无法得到关于特点靶点的信息。将对相应靶点具有活性的后 95% 分子作为输入，模型生成的分子不仅满足相应的化学规则，而且相当数量的活性分子，说明模型具有相当好的泛化能力。生成分子的结果如下图所示，横轴表示分子与前 5% 高活性分子的相似性，竖轴表示分子活性，其中蓝色圆点表示生成的分子，红色菱形表示输入模型的分子。图中只展示了一部分输入-输出的变换，用箭头表示，可以看出许多生成的分子都是往右上方向移动，也就是生成活性更高、与高活性分子更相似的结构。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8916?authkey=ALYpzW-ZQ_VBXTU)

#### Transformer 可以为苗头化合物发现生成新颖分子

文章统计了训练集与输入-输出分子中的 SMIRKS 化学转化，在模型生成的结果中有 1086 种化转化并未出现在训练集中，所以文章认为模型可以生成新颖的化学结构。一部分化学转化如下图所示，训练集中的化学转化都是 MMP 转化，而图中的化学换化显然并不符合规则，而是模型根据训练集中的信息所新造的化学转化。

文章认为使用深度学习实现分子生成并不是将所有可能的 SMIRKS 规则放到输入分子上，这种排列组合的模式势必会大大增加生成的数据量，将有价值的信息淹没。Transformer 能够上下文相关地获取分子信息，并根据信息通过合适的 SMIRKS 规则构建新分子，这种分子生成的手段更有帮助，同时文章发现 Transformer 所使用的 SMIRKS 并不是完全照搬训练集中的数据，而是根据已有信息新构造出的转化规则，这一点可能也是提升 Transformer 分子生成效果的方向。

![!n](https://storage.live.com/items/4D18B16B8E0B1EDB!8915?authkey=ALYpzW-ZQ_VBXTU)

文章还认为，相比于更常用的 SMILES，SELFIES 更有利于 Transformer 学习其中的化学信息，因为 SMILES 无法保证分子合法，必须先训练模型使其学习生成合乎规则的分子。相反，使用 SELFIES 的分子生成模型不需要先让模型学会表示分子的语法，极少出现分子不合法的情况，可能使用 SELFIES 表示分子也是能实现文章实验中效果的重要原因。

文章也指出这只是一个尝试性的工作，还有很多的问题没有解决。首要的一点就是文章使用与活性分子的相似性来评价生成分子的效果，尽管两个分子十分相似，它们也可能具有十分悬殊的活性，这是使用深度学习手段进行药物发现尤需解决的问题。所以文章中的分子生成也只能起到「启发」的作用，并不能真接指导药物化学家找到活性更高的分子。另一点就是文章中并没有对模型做全面的评估与超参数的选择，只是验证的方法的可行性，并没有对比与其他模型的优势。文章中还推测 SELFIES 相比 SMILES 更具有优势，但也未对比两种模型的效果。

## 结论

文章将 Transformer 用于苗头化合物的发现，并且发现 Transformer 对于训练集中不存在的未知靶点也能生成相当数量的活性分子，其中一部分分子与高活性的配体具有很高的相似性。文章还发现，Transformer 生成的结果中，其化学变化并不局限于用于训练的 MMP 数据，这表明 Transformer 具有上下文相关的信息识别能力，利用好这一特性有利于实现活性分子的生成。