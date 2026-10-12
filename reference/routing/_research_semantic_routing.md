# 意图理解改造调研：semantic routing / 混合检索 / 零样本分类

> 2026-10-11 调研。目标：改进 `scripts/route.py` 的意图打分（当前 = triggers 子串匹配 +
> purpose 同义词命中 + use_when 词面重合的线性加和），服务对象是 146 条中文场景档案
> （`reference/routing/segNNN.json`，字段 use_when[]/triggers[]/anti_when[]/style/similar[]/audience）。
> 约束：Windows / py3.11 / 依赖要少 / 可离线降级。
> 所有结论均经本次会话取证（源码/官方文档/PyPI 元数据），来源见各节。

---

## 1. aurelio-labs/semantic-router —— 向量路由层的事实标准

- 仓库: https://github.com/aurelio-labs/semantic-router （MIT）
- 论文: https://arxiv.org/abs/2404.15869 （5G 网管意图路由，IEEE GlobeCom 2024）
- 定位: 不经 LLM 生成、纯靠 embedding 相似度做"utterance → route"的决策层，毫秒级。

### 核心机制（读源码取证：`semantic_router/routers/base.py`、`semantic_router/linear.py`、`index/local.py`）

1. **每条 Route 挂若干条 utterance**（例句，每条路由通常 5~10 句）。初始化时全部编码，连同 route 名存进本地索引（1.x 是 `LocalIndex`，纯 numpy 矩阵）。
2. **查询时**：查询编码成 1 个向量 → `index.query(vector, top_k=5)`：与**所有** utterance 向量算余弦（`similarity_matrix` 就是 `dot / (|x|·|q|)`），取全局 top-k 条 utterance（不分路由）。
3. **按路由分组聚合**：`_score_routes` 把 top-k 的 (score, route) 按 route 分组，每组用 `aggregation_method` 聚合——**1.x 默认 `mean`，可选 `max`/`sum`**（base.py L358: `aggregation: str = "mean"`；L420 校验三选一）。0.x 时代默认 max（"查询 vs 路由内多个 utterance 取最大余弦"）。
4. **阈值门控**：每条 route 可设 `score_threshold`（不设则用 router 全局默认），`_pass_routes` 只放行"聚合分 ≥ 阈值"的路由。
5. **拒绝机制**：没有任何路由过阈值 → 返回**空的 RouteChoice()**（README 演示：问 llama 2 时 politics/chitchat 都不命中，返回 None）。这是"宁可不答，不硬凑"的官方姿势。
6. 阈值怎么定：官方提供 **Route Optimization** notebook（docs/06-threshold-optimization.ipynb），用标注对去搜每条路由的阈值；也支持 encoder 自带 score_threshold。
7. 可选 hybrid：`sparse_encoder`（BM25/SPLADE 类）+ dense 并存；`HuggingFaceEncoder`/`FastEmbed` 支持全本地运行。

### 移植到我们的场景（"意图 vs 每条目 use_when+triggers 文本"）

- 档案侧天然就是"路由 + utterances"结构：**seg = Route；use_when 每行 + triggers 每词 + plain 整句 = utterances**。
  规模估算：146 条 × 平均 7 行 ≈ **约 1000 个向量**，bge-small 512 维 → 索引 2MB，全量余弦 = 一次 1000×512 矩阵乘，CPU <10ms，**根本不需要向量库**。
- 查询侧 = 意图整句编码 1 次。
- 聚合：我们每个 seg 的"utterance 数"不均（use_when 4 行 + triggers 14 词），用 `max`（最像的一行说了算）比 `mean`（被 triggers 稀释）合理；进阶做法是 use_when 行用 mean、triggers 行用 max 分开算再合成。
- 阈值：按 seg 校准太贵，先全局一个阈值（bge 系 cosine 经验 0.45~0.55 起步，用 route_log 校准），后续可给 10 个 purpose 组各设一个。

### 伪代码

```python
# build_embedding_index.py —— 一次性预计算（档案变了增量重建）
texts_by_seg = {seg: use_when_lines + triggers + [plain] for each profile}
M[seg] = encoder.encode(texts_by_seg[seg])        # (n_i, 512)
save "routing_emb.npz" {seg: M[seg]}

# route.py 查询侧
q = encoder.encode(intent)                        # (512,)
for seg, M in index.items():
    sims = M @ q / (norm(M, axis=1) * norm(q))    # cosine, 同 linear.py
    sem_score[seg] = sims.max()                   # max 聚合(0.x 默认)
top = sorted(sem_score, reverse=True)[:5]
if sem_score[top[0]] < THRESHOLD: return "图库没有合适的"   # 空返回=拒绝
```

---

## 2. GPTCache —— 语义缓存的阈值教训

- 仓库: https://github.com/zilliztech/GPTCache
- 论文: Bang 2023, "GPTCache: An Open-Source Semantic Cache for LLM Applications..."（ACL 2023 workshop，cited 270+）
- 定位：LLM 应用的语义缓存——查询先过缓存：**query → embedding → 向量检索 → 相似度评估器 → 超阈值即直接返回缓存答案**，未过阈值才调 LLM。

### 核心机制
1. 四件套：embedding 模型、向量存储、**相似度评估器（可插拔：strsim / np / onnx 分类器）、阈值**。
2. **阈值是最重要的旋钮，且没有万能值**：GPTCache 论文自报 0.7 平衡命中率与正确率；生产实践普遍建议 0.93~0.97（低阈值 → 错误命中 = 返回"看似对其实错"的答案；高阈值 → 命中率低）。评估器还支持把"top1 分数"和"top1−top2 差距"联合判断。
3. 预处理归一化（去大小写/标点/停用词）再查缓存，提高鲁棒命中。

### 移植点
- route.py 已有 `route_log.jsonl`——可以升级成**带向量键的语义缓存**：意图归一化后若与最近 N 次意图的余弦 > 0.95，直接复用上次 top 结果（快速重复路由场景）。
- 更重要的是**方法论教训**：(a) 相似度阈值必须按自己的场景校准，不能抄别人的数；(b) "命中"与"答对"是两个指标，路由场景宁可高阈值（拒绝）也别低阈值（错配）。这与现有"近 3 次展示降权"机制是互补而非替代。

---

## 3. LangChain / LlamaIndex 的 Router —— 分层与选择器模式

- LangChain Router chains: https://reference.langchain.com/python/langchain-classic/chains/router
- LlamaIndex RouterQueryEngine: https://developers.llamaindex.ai/python/framework/module_guides/querying/router
- LlamaIndex RouterRetriever 源码: https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/retrievers/router_retriever.py
- LangChain MultiQueryRetriever: https://reference.langchain.com/python/langchain-classic/retrievers/multi_query/MultiQueryRetriever

### 核心机制
1. **Router 是"选择器"抽象**：LangChain `LLMRouterChain + MultiRouteChain` 用 LLM 读一段"各候选链的用途描述"再选一个；LlamaIndex `RouterQueryEngine/RouterRetriever` 用 Pydantic 结构化选择器在多个 query engine/retriever 里选一个或多个。候选路由**各自带一段自然语言描述**，选择器读描述做决策——这就是我们 use_when 的角色，但它们把"选择"交给 LLM 而非词面匹配。
2. **两级路由**：粗（选 retriever 类型）→ 细（具体查询引擎），与"purpose 粗分类 → seg 细分类"同构。
3. **MultiQueryRetriever 是查询扩展**：LLM 把一个查询改写成多个变体，分别检索后取 **union 去重融合**——绕开"一种措辞搜不到"的单点失败。

### 移植点
- 保留"描述驱动"哲学：我们已有 use_when，缺的是**让更强的匹配器读它**（embedding），而不是更多关键词。
- 两级结构已存在（PURPOSE_SYNONYMS 的 10 类）：可在粗级保留/升级（NLI 或 embedding 对 10 类中心句），细级交给语义通道。
- MultiQuery 的"union 融合"思想可以廉价实现：意图 → 用同义词表展开成 2~3 个变体（规则版 MultiQuery），三变体的语义得分取 max。HyDE 的 LLM 版在"离线降级"约束下不作为主路径（见 §5）。

---

## 4. 混合检索的标准设计：BM25+dense 融合、RRF、重排分层

四家引擎/数据库的官方设计（全部本次取证）：
- Elasticsearch RRF: https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion
- Qdrant Hybrid Queries: https://qdrant.tech/documentation/concepts/hybrid-queries/
- Weaviate hybrid search: https://docs.weaviate.io/weaviate/search/hybrid
- OpenSearch 归一化/组合: https://docs.opensearch.org （min-max / L2 / z-score + arithmetic_mean，2025-02 也加了 RRF）

### 4.1 RRF 公式与实现

Elasticsearch 官方公式（rank 从 1 起）：

```
score(d) = Σ_q  1 / (k + rank_q(d))          # d 不在结果集 q 中则该项不计
```

- ES 默认 `k=60`（`rank_constant`），`rank_window_size` 控制每路取多深；**权重固定每路相等，"无需调参"是它的卖点**。
- Qdrant 用 **0 起的 rank，默认 k=2**（1.16 起可配 `"rrf": {"k": 60}`，1.17 起支持每路 `weights`）；k 越大排名差异越平缓。
- Qdrant 官方选型表（直接回答"RRF 还是加权线性"）：
  | 情形 | 建议 |
  |---|---|
  | 有评测集 | 加权 RRF，在 train/val 上调 weights |
  | 相信各路原始分、无评测集 | DBSF（3σ 归一化后相加） |
  | 既无评测集也无分数先验 | **plain RRF（安全默认）** |
- 线性加权的坑：BM25 分无上界、cosine 有界 [0,1]，直接 `w1*bm25 + w2*cos` 尺度失配；OpenSearch 因此要先 min-max/L2/z-score 归一再算术平均，而 min-max 又会被单个离群分拉爆——RRF 只用排名，绕开整类问题。
- Weaviate 的折中：`alpha` 线性混合（0=纯 BM25F，1=纯向量，默认 0.5）+ `relativeScoreFusion`（先归一化再混，1.24 起默认）或 `rankedFusion`（即 RRF 思想）。alpha 需按"信关键词还是信语义"来调。

**几行实现（k=60，rank 从 1 起，与 ES 一致）：**

```python
def rrf(rankings: dict[str, list], k: int = 60) -> dict[str, float]:
    """rankings: {'bm25': [seg,...], 'semantic': [seg,...], 'rules': [seg,...]}"""
    out: dict[str, float] = {}
    for _ch, segs in rankings.items():
        for r, seg in enumerate(segs, start=1):
            out[seg] = out.get(seg, 0.0) + 1.0 / (k + r)
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))
```

### 4.2 阶段划分（对我们 route.py 的映射）

业界三段式：**召回（每通道宽取 top24）→ 融合（RRF）→ 重排（交叉编码器/业务规则）**。

route.py 现状恰好已有"重排层"：数据契约 validate、防重复降权、每 family≤2/用途≤3 的多样性硬约束——这些**留在 RRF 之后做**（它们是排序 business rules，不是相关性信号）；把现在揉在一起的**相关性打分**（触发词分 + purpose 加成 + use_when 重合 + 气质分）拆成独立通道，各出排名，RRF 融合。

---

## 5. 查询预处理 / 扩展：同义词归一、HyDE、小语料扩展

- HyDE 论文: https://arxiv.org/abs/2212.10496 （Gao et al., ACL 2023）
- LangChain MultiQueryRetriever（上文）
- jieba 0.42.1（PyPI 验证，纯 Python）/ rank_bm25 0.2.2（PyPI 验证）

### 结论
1. **同义词归一最划算**：中英混写（"柱状图/bar chart"）、全半角、别称（小提琴=violin）先归一再匹配。route.py 的 PURPOSE_SYNONYMS 已是雏形，问题是没有覆盖 triggers 层。做法：一张**全局 synonym 表**（目标词 → 变体组，条目新增 triggers 时顺手登记），查询侧 expand 后同时打原句和扩展句。
2. **HyDE 不适合我们当主路径**：论文自己指出，**语料小/同质时假设文档缺乏对比信号**（对 BEIR 生物医学小语料效果差）；且每查询要一次 LLM 生成，离线降级链上等于没有。146 条档案恰恰是"小而同质"。
3. **廉价替代 = "档案体扩展"**（规则版 MultiQuery + HyDE 反向）：不是把查询扩成"假答案"，而是用同义词表+句式把"比较 3 组酶活性有显著性"扩成"组间比较；显著性；柱状图"这类**档案用语**——向档案的 use_when/triggers 词分布靠拢，等价于缩小 query-document 的语言鸿沟，零 LLM。
4. **BM25 通道**：jieba 分词 + rank_bm25（BM25Okapi）对 triggers/use_when 建"文档"，作为词面通道替换现在的子串计数（解决"用户说散点图但 triggers 里是抖动散点"漏配）。两个依赖都是纯 Python、无二进制。

---

## 6. 零样本意图分类：NLI 管线 / SetFit 在 146 类上现实吗

- HF zero-shot-classification pipeline: https://huggingface.co/docs/transformers/main_classes/pipelines
- 多语言 NLI: MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7（100+ 语言含中文）；轻量替代 multilingual-MiniLMv2-L6-mnli-xnli
- Laurer et al. 2024 "Building Efficient Universal Classifiers with NLI": https://arxiv.org （+9.4% 零样本提升）
- SetFit: https://github.com/huggingface/setfit （官方口径 8~16 标注样本/类）

### 结论（直接回答"是否现实"）
1. **NLI 管线 = 每 (查询, 标签) 一次前向，成本随标签数线性涨**。146 类 × 每查询 = 146 次 (premise, hypothesis) 前向，mDeBERTa-base 在 CPU 上单条 ~50-100ms → 单查询 7~15s，**不现实**；MiniLMv2-L6 能压到 ~1-2s 但仍贵、且小语料上 146 类的分辨率存疑。
2. **折中：NLI 只用于 10 个粗用途**（现有 purpose 组间比较/分布形态/...），10 次前向 CPU 可接受，作为 purpose 通道的升级选项（词表打不准的"我想看看这两组有没有关系"→ 相关关系，NLI 能接住）。
3. **SetFit 需要 8~16 条标注/类 × 146 = 1200~2400 条**——没有现成标注，不现实。**但**：route_log.jsonl 在积累 (意图 → 用户实际选用 seg) 的弱标注，攒够后可以做一次性的 SetFit 蒸馏或至少做阈值校准集。当下不做。
4. **赢家仍是 embedding 相似度**：标签文本（use_when）**一次性**离线编码，查询时只编码 1 次 + O(146) 矩阵乘——标签数不进推理成本，这正是 HF 生态对"标签太多"的标准建议（用 embedding 相似度替代 NLI 管线）。

---

## 7. 小语料 embedding 检索的工程要点（146 条、中文、Windows、可离线）

### 模型选型（本次取证）
| 模型 | 参数 | 维度 | 中文 | 备注 |
|---|---|---|---|---|
| **BAAI/bge-small-zh-v1.5** | ~24M | 512 | 强 | **fastembed 官方支持列表内**（ONNX/CPU）；v1.5 缓解相似度分布问题；短查询检索建议加指令前缀"为这个句子生成表示以用于检索相关文章：" |
| moka-ai/m3e-small | ~24M | 768 | 强 | 不在 fastembed 列表，需 sentence-transformers（引 torch） |
| netease-youdao/bce-embedding-base_v1 | ~278M | 768 | 最强档 | C-MTEB 领先，但 CPU 明显更重，违背"依赖少" |

- **fastembed 0.9.0**（PyPI 验证，requires_python ≥3.10 → py3.11 OK）：基于 onnxruntime，**不引 torch**；模型首跑下载到 `local_cache`/`cache_dir`，之后可整体拷贝离线用（`HF_HUB_OFFLINE=1`）。Windows 无特殊问题。
- 选型结论：**fastembed + bge-small-zh-v1.5** 是本场景唯一同时满足"中文/小/CPU/离线/单一轻依赖"的选项。降级链：fastembed 可用 → 用；不可用 → 纯规则通道（现在的打分保留为降级路径，而不是删掉）。

### 预计算与增量更新
- 索引产物：`reference/routing/_emb_index.npz`（seg → 向量矩阵 + 行类型标记）。146 条 × ~7 行 × 512 维 float32 ≈ **2~3MB**，进 git 无压力。
- 增量：build 时记录每个 segNNN.json 的 mtime/内容哈希，重跑只重编码变化的条目；全量重建也就 1000 行 × 24M 模型 ≈ CPU 几秒，不做花哨的也没关系。
- 查询侧每查询只编码 1~3 条文本（原句 + 扩展变体），**毫秒级**。
- 版本锁定：把 fastembed 模型名和哈希写进索引文件，模型换了就强制全量重建（不同模型的余弦不可比，阈值也要重校准）。

### 阈值 / 拒绝机制（什么时候说"没有合适的"）
- 触发条件建议**双通道联合**（避免单通道阈值误杀）：`semantic_top1 < τ_sem`（如 0.5，待 route_log 校准）**且** 规则通道 top1 分数低于历史分布的 P30 → 输出"图库可能没有贴切的案例"，给出最接近的 2~3 个 family 让用户改述（或扩档案）。
- 绝不硬凑的理由来自两边：semantic-router 的空 RouteChoice 设计（没有匹配就返回 None）；GPTCache 的教训（低阈值"命中"= 错误答案）。对样板册场景，硬凑 9 张不像的图会毁掉"样板册"的可信度。
- 阈值校准数据从哪来：初期人工 20~30 条典型意图标注 top3 对错，够拟合全局 τ；后期 route_log 自动积累。
- 附带：bge 系 cosine 在中文短句上的典型区间——同义改写 0.75+，相关但不同 0.55~0.7，无关 <0.5（经验值，非保证；以自己校准为准）。

### 查询理解应抽的结构化信号（业界怎么抽）
| 信号 | 抽法 | 业界对应 |
|---|---|---|
| 统计意图（purpose 10 类） | 词表（现有）→ 可升级 NLI 10 假设 | LangChain/LlamaIndex 两级路由的粗级 |
| 组数/组结构 | 正则：`([二三两四五六七八九十\d]+)\s*组`、"对照组/处理组"、--data 列基数 | 意图槽位填充（slot filling），规则优先 |
| 数据形态（有 --data 时） | 列名/dtype 推断：时间列→趋势、类别列→比较、矩阵→热图、两两关系→网络 | 特征工程式结构抽取，无需模型 |
| 受众（组会/投稿/海报） | 词表（现有 AUDIENCE_HINTS 够用） | 元数据过滤（Weaviate 的 filter 与检索分独立） |
| 气质（高级/朴素） | 词表（现有 WOW_UP/PLAIN 够用） | 同上，属于 rerank 层业务规则 |
| 语义模糊部分（以上都接不住的） | embedding 通道兜底 | dense retrieval |

原则（与四家引擎一致）：**硬信号做 filter/重排，软语义做召回融合**——不要用语义分去干正则能干的事，也不要用词表去猜没见过的说法。

---

## 8. Top5 可落地改造清单（按性价比排序）

> 评分口径：意图理解提升 ÷ (代码量 + 依赖成本 + 校准成本)。现有五层机制（气质/数据适配/防重复/多样性）全部保留为重排层，以下只动"相关性打分"。

### 1. 把线性加和改成 RRF 通道融合 —— 零新依赖，~20 行
现状 score = 触发词分 + purpose 加成 + use_when 重合 + 气质分线性相加，量纲不可比（触发词一分 1.08+，重合一分 0.6）。改成四通道各自排名 → §4.1 的 10 行 rrf()：
- 通道A 词面（现有触发词匹配保留）、通道B 用途（purpose 命中排名）、通道C 场景重合（use_when）、通道D 语义（改造 2 落地后加入）。
- 依赖：无。风险：参数 k=60 直接用，无需调参（ES 卖点）。

### 2. 语义通道：fastembed + bge-small-zh-v1.5，"意图 vs 每条目逐行文本取 max 余弦" —— 1 个轻依赖
- `scripts/build_emb_index.py` 预计算 `_emb_index.npz`（~2MB 进 git），route.py 查询侧只编码 1 次。
- 文本组织：每条目 = use_when 各行 + plain + triggers 拼一行（triggers 词与句子分开编码，行级 max 聚合，semantic-router 移植）。
- 依赖：fastembed（onnxruntime，py3.11 OK，模型下载后完全离线）；降级：import 失败 → 跳过通道D，退回纯规则。
- 这是唯一**新增信息量**的改造（其余都是重组现有信息），直接治"意图理解不到位"。

### 3. 阈值 + 拒绝："图库没有合适的"是合法输出 —— 零新依赖
- 双通道联合拒绝条件（§7），fallback 给 family 级建议和改述提示；route.py 新增 `--strict` 或在 top1 低分时显著提示。
- 依赖：无；需要 20~30 条人工标注做首轮校准（半天工作量）。

### 4. 查询预处理：归一化 + 全局同义词表 + jieba BM25 通道 —— 2 个纯 Python 小依赖
- 归一化（全半角/中英）零成本先做；同义词表覆盖 triggers 别称；jieba+rank_bm25 把词面通道从子串计数升级为 BM25 排名（接进改造 1 的通道A）。
- HyDE/LLM 扩展不做主路径（离线约束 + 小语料无对比信号）；skill 跑在 ZCode agent 里，**上层 LLM 可以免费当查询改写器**——建议 route.py 加一个 `--rewrite "改写后的意图"` 入参，让调用方 agent 先改写再路由，代码零负担。

### 5. 结构化信号抽取器 + NLI 粗用途升级位 —— 后置
- 抽取器按 §7 表格落成 `parse_intent()`（组数正则、--data 形态推断、受众/气质沿用），输出 dict 进通道/重排。
- NLI（mDeBERTa-xnli 或 MiniLMv2-L6）只升级 10 个 purpose 假设，可选、非必需；SetFit 等 route_log 攒够 1200+ 弱标注再蒸馏。当下都不动。

### 依赖成本总览
| 改造 | 新增依赖 | 大小/风险 |
|---|---|---|
| 1 RRF | 无 | 0 |
| 2 语义通道 | fastembed(含 onnxruntime) | ~40MB wheel + 模型 ~90MB，一次性，可降级 |
| 3 拒绝 | 无 | 需少量人工标注 |
| 4 预处理 | jieba + rank_bm25 | 纯 Python，~2MB |
| 5 抽取器/NLI | （可选）transformers | 重，仅粗分类可选装 |

---

## 附：本次取证来源清单
- semantic-router README/源码（ghproxy 拉取 base.py/linear.py/index/local.py）: https://github.com/aurelio-labs/semantic-router
- Semantic Routing for 5G intent (arXiv 2404.15869): https://arxiv.org/abs/2404.15869
- GPTCache 仓库: https://github.com/zilliztech/GPTCache
- Elasticsearch RRF 官方文档: https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion
- Qdrant Hybrid Queries（RRF/DBSF/weights/选型表）: https://qdrant.tech/documentation/concepts/hybrid-queries/
- Weaviate hybrid search（alpha/fusion 类型）: https://docs.weaviate.io/weaviate/search/hybrid
- OpenSearch hybrid 归一化（min-max/L2/z-score/RRF 博客）: https://opensearch.org
- HyDE (arXiv 2212.10496，标题经 arXiv 页面验证): https://arxiv.org/abs/2212.10496
- HF zero-shot pipeline / mDeBERTa-xnli / multilingual-MiniLMv2-L6-mnli-xnli（模型卡与社区评测）
- SetFit (8~16 样本/类官方口径): https://github.com/huggingface/setfit
- fastembed PyPI 元数据（0.9.0，py≥3.10）与支持模型列表: https://qdrant.github.io/fastembed/examples/Supported_Models/
- bge-small-zh-v1.5 模型卡（24M/512 维/检索指令）: https://huggingface.co/BAAI/bge-small-zh-v1.5
- jieba 0.42.1 / rank_bm25 0.2.2 PyPI 元数据（本次直接查询）
- LangChain router / MultiQueryRetriever、LlamaIndex RouterQueryEngine、RouterRetriever 源码（链接见 §3）
