# 中文词面通道改进调研（2026-10-11）

背景：`scripts/routing/lexical.py` 已落地 jieba 分词 + rank_bm25(BM25Okapi) 词面通道，
`query.py` 有 33 组手写 SYNONYM_GROUPS，`fusion.py` 用 RRF 融合可插拔通道（权重在
`_weights.json`，w=0 即关闭）。硬约束：**skill 轻量可移植，运行依赖只能是纯 Python 小包，不引入模型**。
本调研全部基于本次会话取证（原文抓取，非转述），来源 URL 附在各节。

现状要点（取证自代码）：
- BM25Okapi 用库默认 `k1=1.5, b=0.75, epsilon=0.25`（rank_bm25 源码证实）；
- 字段加权靠"字段文本 ×3/×2 重复拼接"实现 → 抬高词频 tf 的同时也拉长文档，与 b 的长度归一互相纠缠；
- jieba `add_word(freq=1000/500)` 注册 triggers/type_zh 为整词；`jieba.lcut` 默认 `HMM=True`；
- RRF 融合层天然支持加第二词面通道：产出 `{seg: score}` 字典 + `_weights.json` 加一个键即可。

---

## 1. BM25 调参：k1/b 与 BM25+/BM25L 变体

**结论**：值得调，幅度小。短文档、长度相对均匀的语料应**调低 b**（0.2–0.3），k1 取 1.2 左右；
BM25+/BM25L 变体**不值得换**（它们治的病是长文档，本语料没有），但库免费自带，可用 `_eval.jsonl` 做 5 分钟 A/B。

**依据**（均本次取证）：
- rank_bm25 源码（raw 抓取证实）：
  https://raw.githubusercontent.com/dorianbrown/rank_bm25/master/rank_bm25.py
  - BM25Okapi 默认 `k1=1.5, b=0.75, epsilon=0.25`；
  - **负 IDF 处理**：df > N/2 的词（146 条语料里即 >73 条含该词）Okapi IDF 为负，库将其替换为 `epsilon × average_idf`（0.25×均值，小正值）——泛词不会得 0 分而是得小分，靠 `_STOP` 停用词兜底是对的；
  - **OOV 查询词**：`self.idf.get(q) or 0`、`doc.get(q) or 0`，静默贡献 0 分，不报错；
  - **硬依赖 numpy**（模块级 import，分数用 np.zeros/argsort）；
  - BM25L 默认 `k1=1.5, b=0.75, delta=0.5`；BM25Plus 默认 `k1=1.5, b=0.75, delta=1`。
- Elastic 官方调参指南（Practical BM25 Part 3）：
  https://www.elastic.co/blog/practical-bm25-part-3-considerations-for-picking-b-and-k1-in-elasticsearch
  - 实验中最优 k1 多落在 **0.5–2.0**，短文档集合建议 k1 取低侧（词出现几次就基本代表主题，tf 饱和应更早）；
  - 最优 b 多落在 **0.3–0.9**；文档长度均匀且短时，长度惩罚意义不大 → b 调低；
  - "b/k1 放最后调，先做同义词、模糊匹配"——与本调研其余各节顺序一致。
- BM25+/BM25L（Lv & Zhai 2011）解决的问题：**长文档中缺失词惩罚过大、TF 归一没有下界**；
  BM25+ 在饱和 tf 项外加 δ 常数（Trotman et al. 2014 实验最佳 δ≈0.5）。
  大规模复现研究（Kamphuis et al. 2020, *Which BM25 Do You Mean?*）结论：变体间实际差异**很小**。
  https://pmc.ncbi.nlm.nih.gov/articles/?term=Which+BM25+Do+You+Mean （综述转引自检索结果，
  原文：https://dl.acm.org/doi/10.1002/asi.24417）

**移植点**：
1. `lexical.py` 的 `BM25Okapi(docs)` 改为 `BM25Okapi(docs, k1=1.2, b=0.3)`（一行）；
2. 根因优化（可选，~20 行，零依赖）：放弃"×3 重复拼接"，改为**每个字段独立 BM25 得分、按字段权加权和**
   （whoosh BM25F 的思路，见第 5 节）——tf/文档长度不再被重复拼接扭曲；
3. 备选对照：`from rank_bm25 import BM25Plus`（δ=1）跑一遍 `_eval.jsonl`，预期差异不大，输了不留。

---

## 2. jieba 的坑与最佳实践；纯 Python 替代

**结论**：jieba 仍是约束内最优解，无必要换。三个具体坑要修：HMM 默认开着会干扰自定义整词、
add_word 的 freq 语义要理解、启动无预热。替代品全部越线（模型/C++/PyTorch）。

**依据**（jieba README 原文抓取：https://raw.githubusercontent.com/fxsjy/jieba/master/README.md ；PyPI：https://pypi.org/project/jieba/ ）：
- jieba 0.42.1（2020-01 后未再发版，稳定但停滞）：纯 Python、零依赖、MIT；sdist 19.2MB（主要是词典数据）。
- `add_word(word, freq=None)`：freq 决定该词在 DAG 最大概率路径中被整体切出的优先级；**freq 省略时自动取
  "能保证切出该词"的值**。当前代码给 triggers freq=1000、type_zh freq=500 是合理做法，但更省事的是
  `jieba.suggest_freq(word, tune=True)` 自动算（用于"想强制切出/切开某片段"的场景）。
- **HMM 坑**：`lcut` 默认 `HMM=True`，Viterbi 新词发现可能把已注册的自定义词重新切碎或合并；官方 FAQ 明确
  "当分词结果出现词典中没有的词、效果不佳时，可尝试关闭 HMM"。本路由是**封闭词表场景**（146 条档案、
  触发词全部已知），新词发现毫无价值，`HMM=False` 更稳更快。
- `load_userdict` 文件格式：`词 [词频] [词性]`，UTF-8，可传文件路径或 file-like 对象——可以把触发词落成
  `routing/userdict.txt` 一次性加载（替代循环 add_word，启动更快、词表可 diff 审查）。
- 全半角：jieba **不做**全半角归一，全角字母/数字会被当独立 token——query.py 的 normalize() 已在查询侧处理，
  注意**语料侧**拼接文本也要过同一 normalize（当前 corpus 直接用档案原文，好在档案是人工维护的干净文本，风险低）。
- 中文数字、"十几"这类量词槽位不归 jieba 管，query.py 的 CN_NUM 路线正确。

**替代品核查**（全不满足纯 Python 无模型约束）：
- pkuseg：CRF + 每领域数十 MB 预训练模型，依赖 numpy/scipy → 出局（https://github.com/lancopku/pkuseg-python ）；
- THULAC：C++ 加速层需编译 → 出局；
- HanLP 2.x：PyTorch → 出局；HanLP 1.x 需 JVM/大数据包 → 出局；
- SnowNLP：纯 Python 但分词质量一般、面向情感/分类场景 → 无增量；
- snowball：词干化器（英/欧语系），与中文分词无关 → 不适用。
- 对比评测参考：知乎《五款中文分词工具在线PK: Jieba, SnowNLP, PkuSeg, THULAC, HanLP》
  https://zhuanlan.zhihu.com/p/51292786 ；pkuseg 官方对比 https://github.com/lancopku/pkuseg-python

**移植点**：
1. `_tokenizer()` 里 `jieba.lcut(s.lower())` → `jieba.lcut(s.lower(), HMM=False)`（一行）；
2. 触发词注册改 `jieba.initialize()` 预热 + 可选落成 `userdict.txt`（消除首次调用 0.5–1s 延迟）；
3. 可做 A/B：语料侧用 `jieba.cut_for_search`（细粒度，召回高）查询侧仍用精确模式——仅当 `_eval.jsonl`
   显示召回不足时再试。

---

## 3. 可离线白嫖的中文同义词表

**结论**：哈工大《同义词词林扩展版》是唯一值得接的：单文件 0.66MB、纯文本、20 行代码可解析。
关键是**只在构建期使用**：与 146 条档案词表求交集 → 人工审核 → 把精选组并进 SYNONYM_GROUPS 随 skill 分发，
运行时零新依赖、零体积增量。HowNet 与 pip 的 synonyms 包出局。

**依据**（取证）：
- **同义词词林扩展版**（HIT-IRLab，在梅家驹《同义词林》基础上扩展，约 7.7 万词条）：
  - 可直取镜像仓库（GitHub API contents 已核实文件与体积）：
    https://github.com/One-sixth/HIT-IR-Lab-Tongyici-Cilin-Extended
    核心文件 `哈工大社会计算与信息检索研究中心同义词词林扩展版.txt`，**678,557 bytes**，附说明 PDF；
  - 其他可用仓库：BiLiangLtd/WordSimilarity（Apache-2.0，371★，https://github.com/BiLiangLtd/WordSimilarity ）、
    TernenceWind/replaceSynbycilin（MIT，https://github.com/TernenceWind/replaceSynbycilin ）；
  - 格式：每行 `五级编码 标记词 词1 词2 ...`，如 `Aa01A01= 人士 人物 人氏 人选`；标记含义：
    `=` 同义（可互换）、`#` 相关/近义、`@` 独立词、`?` 未收录。解析即按 `=` 切一次、空格切词条。
  - **许可现状：无正式开源许可**。哈工大科研成果，惯例仅供研究/非商业；本 skill 非商业研究用途可用，
    但**不要把原始文件随 skill 分发**，只分发人工精选后的派生同义词组（词条事实性列表，风险低）。
  - 预期产量要务实：词林是通用语义词表，图表术语（云雨图/桑基图/蜂群）大概率不在里面；它能补的是
    通用近义（如 显著/明显、时序/时间序列、排序/排名、构成/占比、趋势/走势、离散/分散 这类 use_when 层的词）。
    期望是"把 33 组扩到 60–100 组"而非翻倍，对触发词子串匹配是净增面。
- **HowNet/OpenHowNet**（清华 THUNLP）：https://github.com/thunlp/OpenHowNet —— pip 装包后**数据要另行手动下载**，
  义原标注 10 万+词条、数据非商业许可；对"同义词扩容"而言路径长、体积大、许可紧 → 出局。
  相关 ehownet 包亦为 GPL-3.0 非商业（https://pypi.org/project/ehownet/ ）。
- **pip synonyms 包**：首次 import 需下载 word2vec 词向量（43 万词表），且 2023-10 起改为春松许可证、
  **模型下载收费**（README 原文抓取证实：https://ghproxy.net/https://raw.githubusercontent.com/huyingxi/Synonyms/master/README.md ）
  → 与硬约束正面冲突，出局。
- 哈工大 LTP 系列词表：官网改版后资源下架，均经 GitHub 二手镜像，不如词林直接。

**移植点**（构建期脚本 `scripts/routing/build_synonyms.py`，~25 行，离线一次性）：
1. 解析词林 txt：`code, _, words = line.partition('=')`；只取标记 `=`（严格同义）和 `#`（近义）；
2. 从 `seg*.json` 收集词表 V（triggers + type_zh 切词 + use_when 切词）；
3. 保留满足以下条件的组：≥2 个成员 ∈ V，组员 2–8 个，去掉含单字泛词（"人""口"级）的组；
4. 输出候选组清单 → 人工过目 → 并入 `query.py` 的 SYNONYM_GROUPS（或独立 `synonym_groups_ext.json`）。
   运行时路径零改动、零新依赖。

---

## 4. 查询容错：拼音/同音字/错别字

**结论**：最小代价方案 = **pypinyin（840KB、零依赖、MIT、纯 Python、离线）+ 触发词拼音索引 + 拼音串
编辑距离 ≤1**，并叠一层 ASR 近音归并（zh/z、ch/c、sh/s、an/ang、in/ing、n/l、f/h、l/r）。
编辑距离匹配只对 ≥2 字 token 开、只做"扩面加分"不做硬改写，把误伤交给 RRF 上层的 rule/sem 通道压制。
中文错别字（非同音类）用同一套机制的字符级编辑距离顺手覆盖，不单开通道。

**依据**（取证）：
- **pypinyin** 0.55.0（2025-07）：wheel 840KB、`py2.py3-none-any`（纯 Python 无编译）、**PyPI 零依赖**、MIT、
  全离线（拼音表内置自 pinyin-data/phrase-pinyin-data）：
  https://pypi.org/project/pypinyin/ ；https://github.com/mozillazg/python-pinyin
  - `lazy_pinyin(s, style=Style.NORMAL)` 无声调拼音串是索引/比对的标准入口；`Style.FIRST_LETTER` 可加首字母通道；
  - 词组级多音字已内置（"重庆"不会错切 chong/qing），不装 jieba 也能跑（但我们已有 jieba，词组匹配更准）；
  - 高精度可选伴生 pypinyin-g2pW 是**模型** → 不碰。
- 拼音容错工程路线（规则型、无模型，业界一致做法）：
  - 知乎《策略算法工程师之路-Query 纠错算法》：召回阶段"编辑距离召回 + 同音召回 + 易混淆音译字"全是词典/混淆集驱动：
    https://zhuanlan.zhihu.com/p/35889354 （检索结果确认存在该文，策略框架一致）
  - pycorrector（shibing624）音似纠错本质 = 拼音混淆集 + 语言模型打分；其 kenlm/numpy+torch 部分越线，
    但**混淆集构建思想可抄**：https://github.com/shibing624/pycorrector
  - ASR 纠错论文同样以"拼音正则化"为前置（声音-文字脱节是中文 ASR 纠错的核心困难）：
    https://www.alphaxiv.org/abs （Pinyin Regularization for LLM-based ASR error correction，2025）——
    结论引用其思想：先把转写文本转拼音串再匹配，胜过在字面上硬比。
- 编辑距离：纯 Python DP 实现 15 行（`difflib` 是相似度不是 Levenshtein 距离，别用错）。

**移植点**（~40 行 + 840KB 依赖，开关放 `_weights.json`，w=0 即停用）：
1. 索引侧：对每个 trigger 词存 `py_folded(trigger)`（无声调 + 近音归并后的拼音串）；
2. 查询侧：对 jieba 切出的每个 ≥2 字 token 求同款拼音串；
3. 命中规则：拼音串相等，或 Levenshtein ≤1（token 长度 ≥2 才启用）→ 把对应规范触发词追加进查询文本
   （复用 `query.expand()` 的现有管道，等于免费吃到字段加权与 RRF）；
4. 防误伤三闸门：只对 ≥2 字 token；拼音距离阈值 ≤1；命中词追加权重低于直击词（或只进 expand 不进硬覆盖）——
   例如"折线 zhexian"与"这些 zhexie"拼音距离 1，这类碰撞靠 rule/sem 通道投票消化；
5. 字符级错别字：同一函数对**原字串**再跑一遍编辑距离 ≤1（对"山脊"vs"山舂"这类手滑），零额外依赖。

---

## 5. 其他纯 Python 检索器对比（146 条语料谁有增量）

**结论**：whoosh 没有必要引入，但它有两个值得**抄思想**的设计：BM25F 按字段打分（治第 1 节的重复拼接 hack）
和内建 Levenshtein 模糊项扩展。真正有增量的"替代通道"是**自研字符 bigram BM25**——10 行代码、零依赖，
专治分词错误/中英混杂/错别字，与现有词级 BM25 并联进 RRF。snowball 与中文无关。

**依据**（取证）：
- **whoosh**：纯 Python 全文索引+检索+拼写校正引擎（原版停更；维护分支 whoosh-reloaded 2024-02、
  whoosh3 支持 py3.10–3.14）：https://pypi.org/project/whoosh-reloaded/ 、https://pypi.org/project/whoosh3/
  - 自带 BM25F（字段权重原生）、`fuzzy` 查询项（编辑距离扩展）、拼写校正（n-gram 字段实现）；
  - 中文分析器走 `jieba.analyse.ChineseAnalyzer`——底层还是 jieba，分词质量无增量；
  - 引入成本：新依赖 + 磁盘索引文件（损害"轻量可移植"）+ 为 146 条档案维护索引重建逻辑。
    146 条语料内存态 BM25 每次重建也是毫秒级，索引持久化毫无必要 → **不引入，抄两处设计**。
- **字符 bigram 通道**（自研，无依赖）：
  - 证据 1：Elasticsearch 官方 CJK 分析器就是 char bigram（二元切分）；
  - 证据 2：跨语言分析器实测（2026-09）：中文场景 char bigram 效果最佳，代价是索引膨胀与查询延迟 4–12×——
    在 146 条语料上该代价≈0：https://www.kshivendu.dev/one-analyzer-every-language
  - 证据 3：纯 BM25 引擎对 CJK 的 OOV/分词问题普遍以 n-gram 兜底（Al analyticDB/Manticore 同款设计）。
  - 机制价值：bigram 对**切分边界不敏感**——查询"云雨图"切成 云雨/雨图，档案 triggers"云雨"切出 云雨，
    bigram 云雨 仍命中；对错字、中英混写（"BM25图"）也比词级稳健。
- **snowball**：多语言词干化器（英文/欧语），中文无词干化问题 → 不适用（https://snowballstem.org/ ）。

**移植点**（~15 行，零依赖）：
1. `lexical.py` 加 `bigram_tokens(s)`：中文连续段内滑窗 bigram，英文/数字段整段小写保留；
2. 同一份加权语料再建一个 `BM25Okapi(bigram_docs, k1=1.2, b=0.3)`；
3. `fusion` 通道表加 `lex2`，`_weights.json` 给 `lex2: 0.5~0.8`（低于主词面通道），`_eval.jsonl` 验证增量；
4. 可选替代第 1 节的重复拼接 hack：6 字段各自 bigram/词级打分加权求和（BM25F 思想）。

---

## Top5 可落地改造（按性价比排序，全部满足"纯 Python 小包、无模型"硬约束）

| # | 改造 | 依赖与体积 | 改动量 | 预期收益 |
|---|------|-----------|--------|----------|
| 1 | **字符 bigram 第二词面通道**（`lex2` 进 RRF，权重 0.5–0.8） | 零新依赖 | ~15 行 + weights 一键 | 分词错误/错别字/中英混写的兜底鲁棒性，与词级通道互补 |
| 2 | **pypinyin 拼音容错**（触发词拼音索引 + 近音归并 + 编辑距离 ≤1 扩面） | +pypinyin 840KB 纯 Python，零传递依赖 | ~40 行 | 语音转写/同音字输入场景从"必然查无"到"基本接住" |
| 3 | **词林扩展版构建期扩容 SYNONYM_GROUPS**（交集→人工审核→并组，运行时零依赖） | 构建期一次性 0.66MB 数据，skill 只分发精选派生组 | ~25 行脚本 + 审核 | 33 组 → 60–100 组，通用近义词覆盖面净增 |
| 4 | **BM25 参数落地**：`k1=1.2, b=0.3`（短文档、长度均匀），顺手 `_eval.jsonl` A/B 一把 BM25Plus | 零新依赖 | 1 行 | 消除 b=0.75 对档案词富集度的隐性惩罚；预期小幅正收益 |
| 5 | **分词细节修正**：`HMM=False` + `jieba.initialize()` 预热（可选：触发词落 userdict.txt） | 零新依赖 | 1–3 行 | 消除 HMM 重切自定义词的隐患与首次调用延迟 |

落选备忘：BM25+/BM25L 变体（差异小、治长文档，本语料无病灶）；whoosh（依赖+磁盘索引，违背轻量，抄 BM25F
与 fuzzy 思想即可）；pkuseg/THULAC/HanLP（模型/编译/PyTorch）；pip synonyms（word2vec 模型 + 2023 起收费）；
OpenHowNet（数据手动下载 + 非商业许可 + 体积）；snowball（与中文无关）。

**最值得先做的一件**：#1 字符 bigram 通道。理由：零依赖零风险、`fusion.py` 的 RRF + `_weights.json`
天然就是为并联通道设计的（加一个键即可启用/停用），且它是唯一不依赖"jieba 这次切对了"的词面保障——
做完它，#2 拼音容错的误伤也会被它和 rule/sem 通道进一步对冲。
