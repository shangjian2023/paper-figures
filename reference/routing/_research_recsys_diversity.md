# 调研笔记: 推荐系统多样性重排 + 反馈信号 → route.py 移植

日期: 2026-10-11 ｜ 调研者: ZCode ｜ 场景: route.py 候选池 146, 单请求 top-9, 中文, 依赖要少
现状: 打分(线性加权和) → 防重复(最近 3 行 log 每条 −0.9) → 硬约束 diversify(每 family≤2, 每用途≤3)
已有依赖: numpy≥1.26, scipy≥1.11, matplotlib, pillow, networkx (requirements.txt) — **零新增依赖是硬约束**

---

## 1. MMR (Maximal Marginal Relevance)

### 机制
Carbonell & Goldstein (SIGIR 1998). 每步从剩余候选里贪心选一个, 同时兼顾"与查询相关"和"与已选集合不重复":

```
MMR(d_i) = λ · Sim1(d_i, q) − (1−λ) · max_{d_j∈S} Sim2(d_i, d_j)
```

- `S` = 已选集合, `q` = 查询, `Sim1` = 候选对查询的相关度, `Sim2` = 候选对已选项的冗余度
- λ=1 纯相关性(退化为原排序), λ=0 纯多样性(最远点采样), 实践常用 **0.5–0.8**
- 第一个元素直接取相关性最高者, 之后逐步贪心; 复杂度 O(k·n) (k=选出数, n=池大小), 146×9 约等于瞬间

### 代表实现
- **langchain**: `langchain_core/vectorstores/utils.py` 的 `maximal_marginal_relevance(query_embedding, embedding_list, lambda_mult=0.5, k=4)` (已取证 master 分支 L112–152): numpy 余弦相似度, 先 argmax 选第一个, 之后循环里对每个候选算 `λ·sim_to_query − (1−λ)·max_sim_to_selected`, 贪心加入。被所有 VectorStore 的 `max_marginal_relevance_search` 和 `MaxMarginalRelevanceExampleSelector` 复用。
  URL: https://github.com/langchain-ai/langchain/blob/master/libs/core/langchain_core/vectorstores/utils.py
- **sentence-transformers**: `util.community_detection(embeddings, threshold=0.75, min_community_size=10)` (v3.0.1 util.py L416, 已取证) 是另一路数——在余弦相似度图上做快速社区检测(Louvain), 返回按大小排序的社区。**注意**: 它为"大语料聚类"设计, `min_community_size=10` 的默认值对 146 条目基本聚不出社区; 适合离线做家族再聚合, 不适合逐请求重排。
  URL: https://github.com/UKPLab/sentence-transformers/blob/v3.0.1/sentence_transformers/util.py
- 原文: https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf

### 我们的移植点
`Sim2` 不需要 embedding——候选是结构化档案文本(family/type_zh/use_when/triggers/anti_when), 三档相似度方案(依赖从低到高):

| 档位 | 相似度 | 依赖 | 备注 |
|---|---|---|---|
| T0 | 字符 n-gram (2–4) Jaccard, 文本=family+type_zh+use_when+triggers | **纯 stdlib** (route.py 已有 `[\u4e00-\u9fff]{2,4}` 抽取) | 中文无分词友好; 语义弱但抓字面重叠 |
| T1 | TF-IDF 余弦(字符 n-gram 向量), **离线预计算 146×146 相似度矩阵存 JSON** | numpy (已有) | `sklearn` 不引入; 自己写 15 行 TF-IDF 或直接 numpy |
| T2 | 中文 embedding 余弦(如 BGE/small 模型), 同样离线预计算矩阵 | 离线装模型, 运行时仍 0 依赖 | 语义最好; 矩阵文件约 146²·4B ≈ 85KB (int8 量化后 21KB) |

**关键设计: 相似度矩阵离线算好, 运行时只做查表**, 所以任何档位都不增加 route.py 运行时依赖。

### 伪代码 (route.py 版, T0 档)
```python
def ngrams(text, n=(2,3,4)):
    toks = set()
    for i in range(len(text)):
        for L in n:
            if i+L <= len(text): toks.add(text[i:i+L])
    return toks

def mmr_rerank(scored, sim, n=9, lam=0.7):
    # scored: 相关性降序; sim[(a,b)]: 0..1 候选间相似度(查表)
    S, rest = [scored[0]], scored[1:]
    while rest and len(S) < n:
        best = max(rest, key=lambda c:
            lam*c['_score'] - (1-lam)*max((sim[(c['seg'], s['seg'])] for s in S), default=0))
        S.append(best); rest.remove(best)
    return S
```
注意: 先把 `_score` 归一化到 [0,1] (min-max on current pool) 再进 MMR, 否则 λ 两项量纲不可比。

---

## 2. DPP (Determinantal Point Process)

### 机制
把每个候选的"质量×相似度"编码进核矩阵 L = diag(q)·S·diag(q) (q 为质量分, S 为相似度矩阵), 一个子集被 DPP 采出的概率 ∝ det(L_S)——**子集行列式大 ⟺ 元素质量高且彼此不相似**。行列式天然捕捉高阶负相关(MMR 只看两两), 且核可以从数据里学。

### 为什么比 MMR 贵
- 贪心 MAP 推理(近似选概率最大的子集)朴素实现每步要重算行列式/求逆, O(n³)/步;
- **Fast Greedy MAP** (L. Chen, G. Zhang, E. Zhou, NeurIPS 2018, "Fast Greedy MAP Inference for DPP to Improve Recommendation Diversity"): 维护增量 Cholesky 分解, 每选一个只做 O(k²) 的行列增补, 使 DPP 重排在工业界可用 (LII ≈ 每步 log|det| 贪心)。
  URL: https://proceedings.neurips.cc/paper_files/paper/2018/hash/504acec3574cc7892aa538f69637b346-Abstract.html
- **YouTube 生产级应用**: Wilhelm et al., "Practical Diversified Recommendations on YouTube with DPP" (RecSys 2018) — 核矩阵由一个用户偏好模型生成 (CIFGEN), 贪心 MAP 出最终 slate。
  URL: https://jgillenw.com/cikm2018.pdf
- 更快的变体: Hemmi & Tanaka (AISTATS 2022) lazy+fast greedy, C++ 实现; DPPy (https://github.com/guilgautier/DPPy) 是通用 Python 库。

### 146 池下是否可用
**计算上完全可用**: 核矩阵 146×146, 即使朴素贪心也毫秒级; fast greedy 更不必说。**但工程上不值得现在做**, 因为真正的成本在"核的标定":
- 质量项 q(i) 要有校准的概率含义, 相似度矩阵 S 要可靠;
- 我们的相关分是手调启发式(不是校准概率), 直接塞进 L 会让 det 值无意义;
- MMR + 类别约束在 9 个位置上与 DPP 的多样性收益几乎重合 (YouTube 论文自己也强调收益在"模型学的核"而非推理本身)。
结论: 列为后续选项(若未来 taste.md 积累了足够选择日志, 可学一个简单核), 现在 MMR 性价比远高于 DPP。

### 伪代码 (numpy 贪心 MAP, 备用)
```python
def dpp_greedy(q, S, k):            # q: (146,), S: (146,146) ∈[0,1]
    L = np.outer(q, q) * S          # 核: 质量×相似度
    cis, di2s = [], []              # Cholesky 增量
    idx = int(np.argmax(diag := np.diag(L)))
    selected = [idx]
    while len(selected) < k:
        eis = (L[selected, :] @ np.linalg.solve(L[np.ix_(selected, selected)],
                                               L[selected, selected if False else :, None])).ravel() \
              if False else np.array([L[i, selected] @ np.linalg.pinv(L[np.ix_(selected, selected)]) @ L[selected, i]
                                      for i in range(len(q)) if i not in selected])
        # 实现按 NeurIPS 2018 Algorithm: 维护 ci/di, 每步 O(k²) 增补, 见论文伪代码
        cand = [i for i in range(len(q)) if i not in selected]
        nxt = max(cand, key=lambda i: L[i, i] - eis[cand.index(i)])
        selected.append(nxt)
    return selected
```
(此处给骨架示意; 实作照抄论文 Algorithm 1, ~40 行 numpy。)

---

## 3. 覆盖率 / 新颖性 / 意外性指标

### 定义与计算 (Kaminskas & Bridge 2017 综述; Ge et al. RecSys 2010)
- **Catalog coverage** = 所有历史推荐里出现过的去重条目数 / 全目录条目数 (146)。变体: Gini 系数、Shannon 熵——衡量"头部垄断程度"。
- **Novelty (mean self-information)** = −log₂ p(i), p(i) 为条目在历史推荐(或交互)中的占比; 对 slate 求平均。冷门条目 novelty 高。
- **Serendipity** = 相关 且 意外(与用户画像/基线推荐距离远)。Ge et al. 的算式: unexpectedness = 推荐 slate 与"primitive 集合"(用户画像能平凡推出的推荐)的平均距离; serendipity = unexpectedness × usefulness。
  URL: https://web-ainf.aau.at/pub/jannach/files/Conference_RecSys2010.pdf ; 综述 https://www.researchgate.net/publication/311784289

### 我们的移植点 (评测脚本, 不进打分)
- **family coverage (单次)**: top-9 里去重 family 数 / min(9, 总 family 数)
- **catalog coverage (滚动)**: 最近 W 次 route_log 展示过的 seg 去重 / 146 → 监控"总在某几类图里反复挑"是否缓解
- **novelty**: 用 route_log 里每个 seg 的展示频次算 −log₂(count/total), 对 slate 平均; 越低说明越推头部
- **ILS (intra-list similarity)**: 见 §7 评测节, 与相关性均值画帕累托曲线选 λ
- 全部指标可从 route_log.jsonl 离线算, ~60 行脚本, 0 依赖。

---

## 4. 反馈信号设计 (隐式反馈: 展示/选择日志)

### 三类基本件
1. **滑窗 + 时间衰减**: 不用"最近 K 行"这种按条数窗口, 用指数衰减: `w(e) = 0.5^(Δt_days / half_life)`。展示类信号 half-life 短(1–2 天), 选择类信号 half-life 长(2–4 周)。
2. **贝叶斯平滑**: 事件是二项(展示了 n 次被选 c 次), Beta 先验后验均值 `rate = (c+α)/(n+α+β)`, α/(α+β) = 全局平均选择率; 小样本自动向先验收缩, 避免零样本条目被一票否决。出处: Beta-Binomial 共轭, 见 Cornell 讲义 https://sidbanerjee.orie.cornell.edu (posterior mean = (α+N₁)/(α+β+N)) 与 Brown 讲义 https://www.dam.brown.edu
3. **ε-greedy 探索**: 以概率 ε 在 top-9 里保留 1 个"探索槽"(从未/低频展示的合格候选), ε 可随日志量增长衰减(如 ε = max(0.05, 1/√(1+总请求数))); 保证尾部条目持续获得曝光, 头部不会永久垄断。参考: https://imaddabbura.github.io/posts/bandit-algorithms/epsilon-Greedy-Algorithm.html

### 隐式反馈的信噪问题 (展示 ≠ 选择)
Joachims et al. 2007 (https://www.cs.cornell.edu/people/tj/publications/joachims_etal_07a.pdf) 的经典结论: 点击是**有偏的相对偏好信号**——"点击了 A 而没点同屏的 B"比"A 被点击"本身可信; 展示位置决定曝光。映射到我们这里:
- **shown (route_log top)** 只证明"路由器觉得它可能合适", 不是负信号, 降权必须弱、可恢复;
- **picked (taste.md "选了什么")** 是强正信号;
- **vetoed (taste.md "否决了什么")** 是强负信号, 但同样要时间衰减(口味会变);
- taste.md 现在是空模板(格式: 日期|场景|选了什么|否决了什么|一句偏好), 所以反馈管道要**同时定义 taste.md 的机器可解析格式**(或另存机器版 taste_events.jsonl, taste.md 只留人读版)。

### 设计要点: 别把用户想要的图永久压没
- 降权有**下限**: penalty = min(penalty, 2.5) (route.py 里 trigger+purpose 主信号轻松到 4–6 分, 2.5 的惩罚压不死真正相关的候选);
- 展示信号 half-life 1–2 天, 几天后自动回满血;
- 只用 Beta 平滑后的**选择率**做长期降权(选了又选的 family 降, 展示多但没被选的 family 缓降), 且是乘性小系数(0.8–0.95), 不是加性大惩罚;
- ε 探索槽保证每个合格条目仍会周期性出现。

### 伪代码 (route.py 版)
```python
def feedback_weight(now):                    # 读 route_log.jsonl + taste_events.jsonl
    shown, picked, vetoed = Counter(), Counter(), Counter()
    for e in events:                          # {ts, type: shown|picked|vetoed, seg}
        w = 0.5 ** ((now - e.ts).days / e.half_life)   # shown:1.0d, picked:21d, vetoed:14d
        {'shown': shown, 'picked': picked, 'vetoed': vetoed}[e.type][e.seg] += w
    pen = {}                                   # 每候选惩罚, 有下限
    for seg in all_segs:
        sel = (picked[seg] + A) / (picked[seg] + shown[seg] + A + B)   # Beta 平滑选择率
        pen[seg] = min(2.5, 1.2*shown[seg] - 2.0*picked[seg] + 1.5*vetoed[seg]) \
                   - 0.8*(sel - A/(A+B))              # 选择率高于全局 → 减惩罚
    return pen

def explore_slot(ranked, shown_hist, eps=0.1, k=1):
    if random.random() < eps:                # ε-greedy: 概率换 1 个探索位
        tail = [c for c in ranked if shown_hist[c['seg']] == 0][:5]
        if tail: return swap_one(ranked, random.choice(tail), pos=6)   # 放第 7 位, 不占前排
    return ranked
```

---

## 5. Rank fusion (RRF 与分数归一化)

### RRF
Cormack et al. 2009: `score(d) = Σ_lists 1/(k + rank_list(d))`, k 常取 60。Elastic 默认实现: https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html 。优点是**只用名次, 天然免归一化**; 变体: 加权 RRF `Σ w_i/(k+rank_i)`, 每路一个权重 (https://apxml.com/courses/hybrid-search/4-fusion/reciprocal-rank-fusion)。

### 分数归一化 (当必须融合原始分时)
- **min-max**: 对当次候选池归一到 [0,1]; 简单, 但对离群值/分布漂移脆弱 (https://blog.serghei.pl 等实践结论)。
- **z-score**: OpenSearch 2.19 在混合检索里加了 z-score 归一化作为 RRF 之外的选项 (https://opensearch.org/blog/reciprocal-rank-fusion-hybrid-search)。
- **softmax/温度**: 把分数变成伪概率再融合; 温度超参需要调。
- 实证结论: OpenSearch 六个数据集上 RRF(含加权)整体优于调过的分数归一化融合 (https://www.bigdataboutique.com/blog/reciprocal-rank-fusion-rrf-how-it-works-and-when-to-use-it)。

### 我们的移植点
route.py 的 `_score` 是异质项线性相加(触发词 1.0+0.08L、用途 2.2×hits、场景描述 0.6×n、气质 ±、受众 0.8、降权 −0.9×n、数据 ±2.8), 项间量纲本来就是拍脑袋的——两种改造:
1. **最小改动**: 在 diversify/MMR 入口对 `_score` 做当池 min-max (2 行), λ 融合才有意义;
2. **更稳**: 把"触发词命中 / 用途命中 / 场景描述命中 / 气质 / 受众"当 5 路独立排序, 加权 RRF 融合 (`Σ w_i/(60+rank_i)`, w 可调), 数据适配与反馈惩罚仍走分数通道最后相加。这消除了"词长加权 0.08"这类脆参数, 但改动大, 列为非紧急。

---

## 6. lightfm / implicit / surprise 在"无协同数据、纯内容"场景的适用性

| 库 | 机制 | 纯内容可用? | 结论 |
|---|---|---|---|
| **lightfm** | 混合: 协同 MF + item/user 特征嵌入 | 特征齐全时可 content-only, 但要喂 interaction 矩阵训练, 无交互则嵌入学不出来 | **不适用**: 我们的选择日志(<百条)远不够训练; 且库 2020 年后停止维护, numpy 2.x 兼容性差 (https://github.com/lyst/lightfm) |
| **implicit** | 纯协同 (ALS/BPR), 只吃 user×item 交互矩阵 | 无内容特征支持 | **不适用** (146 条目×个位数用户没有共现可学) |
| **surprise** | 显式评分 SVD/KNN | 不支持 item 元数据 | **不适用** (我们没有评分) |

结论要点: **三个库都不值得引入**。我们的"交互"是 route_log(展示)+taste.md(选择), 稀疏到任何矩阵分解都是噪声放大器。正确的做法是把反馈当**信号加权**(§4)而不是模型训练; 内容匹配用已有的 triggers/use_when/purpose 词表 + 手写相似度。唯一例外: 若将来 taste.md 攒下几百条选择, 可以离线学一个"用途→family 偏好"的先验表(就是个平滑计数表), 仍然不需要这些库。

---

## 7. 四个重点设计问题的回答 (146 池 / top-9 / 中文 / 低依赖)

### Q1. MMR 相似度用什么算?
见 §1 三档表。推荐 **T0 起步(字符 2–4 gram Jaccard, 纯 stdlib), 结构允许无痛升级到 T2(离线预计算 embedding 余弦矩阵, 运行时查表)**。不建议 TF-IDF 引 sklearn——numpy 手写 15 行即可, 且 146 条目直接预计算全矩阵存 `reference/routing/_sim_matrix.json`, route.py 零运行时成本。

### Q2. 展示降权怎么设计才不压死真想要的图?
四件套(见 §4): ① 事件分型(shown/picked/vetoed, picked 来自 taste.md, 优先级最高); ② 时间衰减 half-life(shown 1–2 天 / vetoed 14 天 / picked 21 天), 替换"最近 3 行"的条数窗口; ③ 惩罚封顶 2.5 分, 保证强相关信号(触发词+用途 ≈ 4–6 分)能穿透; ④ ε-greedy 探索槽(每轮 top-9 保 1 个低曝光位)。长期维度用 Beta 平滑选择率做 family 级缓降而非 seg 级硬压。

### Q3. λ/k 怎么暴露与评测?
- 配置: `--mmr {off,ng,tfidf,emb}`、`--lambda 0.7`、`--family-cap 2`、`--purpose-cap 3`、`--explore 0.1`, 全部落到 `reference/routing/route_config.json` 可覆盖;
- 评测(离线脚本 `eval_route.py`): 对一组固定意图集(可从 route_log 历史 intent 抽样)跑不同 λ, 输出 **相关性均值(top-9 `_score` 归一化) × ILS × family coverage** 三元组, 画帕累托选点;
- ILS 公式: `ILS = 2/(k(k−1)) Σ_{i<j} sim(d_i,d_j)` (k=9, sim 用同一张相似度表), 越低越多样;
- 每次 route --log 顺手追加一行 aggregate(cov/novelty), 滚动监控。

### Q4. 类别硬约束和 MMR 怎么共存?
**不做"先约束后 MMR"两段式**——先过滤会在池边缘过早丢掉最相关的候选。改为**单遍贪心: MMR 打分 + cap 只跳过不剔除(skip-not-drop)**, 并给"命中未覆盖用途"一个覆盖增益(xQuAD 思想, Santos et al. WWW 2010: https://www.ambuehler.ethz.ch/CDstore/www2010/www/p881.pdf —— 用 aspect 覆盖概率显式奖励尚未覆盖的用途):

```python
def greedy_mmr_constrained(scored, sim, n=9, lam=0.7, beta=0.8,
                           fam_cap=2, pur_cap=3):
    fam, pur, S = Counter(), Counter(), []
    pool = list(scored)                       # 相关性降序
    while len(S) < n and pool:
        for c in pool:                        # 跳过但不删除, 找下一个达标的
            if fam[c['family']] >= fam_cap: continue
            if pur[c['_purposes'][0]] >= pur_cap: continue
            cov = beta * (1 - min(pur[c['_purposes'][0]], 1))   # 未覆盖用途增益
            red = max((sim[(c['seg'], s['seg'])] for s in S), default=0)
            c['_mmr'] = lam*c['_nscore'] - (1-lam)*red + cov
        cand = [c for c in pool if c.get('_mmr') is not None]
        if not cand: break                    # 全被 cap 挡住 → 放宽 caps 重来
        best = max(cand, key=lambda c: c['_mmr'])
        S.append(best); pool.remove(best); fam[best['family']] += 1
        pur[best['_purposes'][0]] += 1
        for c in pool: c.pop('_mmr', None)
    return S
```
要点: cap 违规者**留在池里下轮继续算**(只是当轮跳过), 池不够时逐级放宽 cap——与现有 diversify 的"放宽补齐"语义兼容; 覆盖增益 β 使"每用途≤3"从纯约束变成软引导, xQuAD 证据表明显式 aspect 覆盖在 slate 前段效果最好。

---

## 8. Top5 可落地改造 (按性价比排序)

| # | 改造 | 解决什么 | 依赖成本 | 规模 |
|---|---|---|---|---|
| 1 | **展示降权重做**: 事件分型(shown/picked/vetoed) + 指数时间衰减(half-life 1–2 天) + 惩罚封顶 2.5 + taste.md 同步机器事件格式 | 现在按"最近 3 行"计数, 3 分钟内连查 3 次等于 3 天; 真想要的图会被压; 展示被当负信号 | **0 依赖**, 纯 stdlib 重写 `recent_shows()` | ~35 行 |
| 2 | **MMR 替换硬约束段**: 单遍贪心 `greedy_mmr_constrained` (cap skip-not-drop + 用途覆盖增益), 相似度用字符 2–4 gram Jaccard T0 档 | 硬约束是"可行解"不是"最优解"; MMR 让多样性按相似度连续调节, family/用途结构保留 | **0 依赖** (numpy 已有, T0 只用 stdlib) | ~45 行 + min-max 归一 2 行 |
| 3 | **ε-greedy 探索槽**: top-9 第 7 位保留 1 个低曝光合格候选, ε 默认 0.1 | 头部 family 永久垄断、尾部 146 分之 100+ 永不见天日; 与 #1 一起构成"不会压死"的双保险 | **0 依赖** | ~12 行 |
| 4 | **配置化 + 评测脚本**: `route_config.json` (lambda/caps/eps/half_life) + `eval_route.py` 输出 ILS × family coverage × catalog coverage × novelty, 对 λ∈{1.0,0.85,0.7,0.5} 扫帕累托 | 现在所有阈值硬编码在函数体里, 改动无依据; 每次调参靠感觉 | **0 依赖** | ~60 行脚本 + config 解析 ~15 行 |
| 5 | **Beta 平滑 family 先验**: 用 taste.md 选择 + route_log 展示算 family 级平滑选择率 (c+α)/(n+α+β), 作为乘性先验(0.85–1.1)参与打分 | 长期品味学习: 被反复选中/反复否决的家族类型获得统计意义的升降, 而不是单次事件的噪声 | **0 依赖** | ~25 行 (先攒数据, 后启用) |

**暂不做** (记录原因): DPP 重排(核标定成本高, 146 池下 MMR+约束收益几乎重合, 见 §2); lightfm/implicit/surprise(见 §6); sklearn TF-IDF(需新增依赖, T0+预计算矩阵更划算); 加权 RRF 五路融合(改动面大, 等评分通道稳定后再评估)。

**依赖成本注**: 全部改造运行时 0 新依赖; 唯一可选升级是离线跑一次 embedding 生成 `_sim_matrix.json` (T2 档), route.py 运行时仍是查表。

## 9. 主要来源
- MMR 原文 (Carbonell & Goldstein 1998): https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf
- langchain MMR 实现: https://github.com/langchain-ai/langchain/blob/master/libs/core/langchain_core/vectorstores/utils.py
- sentence-transformers community_detection (v3.0.1): https://github.com/UKPLab/sentence-transformers/blob/v3.0.1/sentence_transformers/util.py
- Fast Greedy MAP DPP (NeurIPS 2018): https://proceedings.neurips.cc/paper_files/paper/2018/hash/504acec3574cc7892aa538f69637b346-Abstract.html
- YouTube DPP (RecSys 2018): https://jgillenw.com/cikm2018.pdf ; DPPy: https://github.com/guilgautier/DPPy
- Beyond-accuracy 指标综述 (Kaminskas & Bridge 2017): https://www.researchgate.net/publication/311784289 ; Ge et al. RecSys 2010: https://web-ainf.aau.at/pub/jannach/files/Conference_RecSys2010.pdf
- Beta-Binomial 平滑: https://sidbanerjee.orie.cornell.edu (Cornell 讲义), https://www.dam.brown.edu (Brown 讲义)
- 隐式反馈评估 (Joachims et al. 2007): https://www.cs.cornell.edu/people/tj/publications/joachims_etal_07a.pdf
- ε-greedy: https://imaddabbura.github.io/posts/bandit-algorithms/epsilon-Greedy-Algorithm.html
- RRF: https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html ; https://apxml.com/courses/hybrid-search/4-fusion/reciprocal-rank-fusion ; OpenSearch z-score: https://opensearch.org/blog/reciprocal-rank-fusion-hybrid-search
- xQuAD (Santos et al. WWW 2010): https://www.ambuehler.ethz.ch/CDstore/www2010/www/p881.pdf
- lightfm: https://github.com/lyst/lightfm ; cold-start 适配讨论: https://mirumee.com/blog
