# C方法来源与报告引文核对

本记录核对C使用的方法文献及事实来源入口，供C报告和研究页引用；不代替整组报告最终格式校对。方法原论文、来源网页和本项目实测结果分别使用，避免把相关工作中的改善幅度写成本项目结果。

| 引文 | 原始来源与核对位置 | 本项目对应及差异 |
| --- | --- | --- |
| M1 | Stephen Robertson; Hugo Zaragoza，2009，[The Probabilistic Relevance Framework: BM25 and Beyond](https://doi.org/10.1561/1500000019)。原论文封面及第3.4—3.5节，式3.15和变体说明 | 词频饱和、长度归一化和IDF加权的BM25排序思想。 本项目使用中文二元片段/英文数字词元、非负平滑IDF、k1=1.5、b=0.75及独立主题锚点过滤；锚点消歧/年份回退是本项目规则，不声称来自该论文。 |
| M2 | Patrick Lewis; Ethan Perez; Aleksandra Piktus; et al.，2020，[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)。摘要及模型的参数记忆/外部检索记忆定义 | 以外部检索证据辅助生成的研究方向与来源追溯动机。 本项目为固定BM25和提示词证据注入，未联合训练稠密检索器与生成器，也未复现论文RAG-Sequence/RAG-Token；论文的提升幅度不迁移为本项目成效。 |
| M3 | Qwen Team，网页日期未单列，[Qwen2.5-0.5B-Instruct model card](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)。官方模型卡、License和Transformers调用示例 | 基础模型身份与使用入口；官方页面标注apache-2.0。 实验按本地保存的模型文件哈希、生成配置和实际软件版本复现，不把官方卡上的通用能力表当成本项目实测结果。 |

## 报告可以使用的表述

本文实现基于词面检索与证据提示的抗幻组件。BM25参考Robertson与Zaragoza的概率相关性研究[M1]；外部资料辅助生成的研究背景参考Lewis等[M2]。本实现不训练稠密检索器或生成器，也不复现RAG-Sequence/RAG-Token。主题锚点、特定词项消歧和年份别名回退为本项目的工程规则，效果只按对应开发对照解释。基础模型为本地Qwen2.5-0.5B-Instruct[M3]，身份以官方模型卡和本地权重哈希共同记录。

实际排序使用k1=1.5、b=0.75和非负平滑IDF；top_k=2、min_score=1.5属于当前显式配置。上述阈值与中文二元片段处理不是论文推荐的通用最佳参数。

事实来源映射覆盖v4检索资料、125题来源台账、17题补查及五题后续补查。完整标题、URL、定位、历史访问方式和日期见[reference_map.json](reference_map.json)。审计来源没有因为被列入参考文献就自动进入RAG。

M1的原论文正文在[大学保存的原论文副本](https://www.ccs.neu.edu/home/vip/teach/IRcourse/IR_surveys/robertson_foundations.pdf)核对；DOI当前落地页元数据版式可能不同，引用采用原PDF封面的2009年3卷4期333—389页。
