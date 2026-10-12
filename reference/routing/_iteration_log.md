# 意图理解迭代日志

评测集: reference/routing/_eval.jsonl (42 意图, 期望 seg 取自 selection.md 决策表)
评测器: scripts/route_eval.py (use_log=False 可复现)
覆盖: 评测随档案生产进度变化, 以"可覆盖命中率"(至少一个期望 seg 已有档案的案例)为主指标。

## R0 基线 (2026-10-12, 档案覆盖 68/146)

| 指标 | 值 |
|---|---|
| hit@5 | 0.595 |
| MRR@9 | 0.506 |
| 可覆盖命中率 | 0.806 |
| 可覆盖MRR | 0.685 |
| famcov@9 | 6.0 |
| monopoly@9 | 0.0 |
| novelty(总不同seg) | 54 |

病灶归因(引导后续轮次): ①字面形态差("山脊一样"≠"山脊图") ②意图槽位与反指无机器通道 ③词面打分无 IDF/字段权重 ④语义鸿沟 ⑤纯硬约束多样性。

## R1 查询理解层 (routing/query.py: 归一化+同义词组扩展+槽位/反指约束比对)

| 指标 | R0 | R1 | Δ |
|---|---|---|---|
| hit@5 | 0.595 | 0.619 | +2.4pt |
| 可覆盖命中率 | 0.806 | 0.839 | +3.3pt |
| 可覆盖MRR | 0.685 | 0.770 | +8.5pt |
| novelty | 54 | 58 | +4 |

修复: "堆成山脊一样"(同义词组扩面)、"边上带直方图"(边际分布组)。新增: 意图槽位(组数等)与反指界限机器比对, 违反硬罚 -3。

## R2 BM25 词面层 (routing/lexical.py: jieba+BM25Okapi, 字段加权 triggers×3/type_zh×2/use_when×2/type_en×1.5/anti_when×1/style×1, min-max 归一线性融合 w_lex=2.2)

| 指标 | R1 | R2 | Δ |
|---|---|---|---|
| hit@5 | 0.619 | 0.690 | +7.1pt |
| 可覆盖命中率 | 0.839 | 0.935 | +9.6pt |
| 可覆盖MRR | 0.770 | 0.862 | +9.2pt |
| novelty | 58 | 68 | +10 |

BM25 的 IDF 自动压泛词, "疗效差异/哪组效果好"这类不在 triggers 里的口语说法经由 use_when/anti_when 语料命中。

## R3a 语义层·tfidf 后端 (routing/semantic.py: char_wb 1-3 gram 余弦) — 无增益, 已降级为保底

| 指标 | R2 | R3a(sem=0.6) | R3a(sem=1.2) |
|---|---|---|---|
| 可覆盖命中率 | 0.935 | 0.935 | 0.903 ↓ |
| 可覆盖MRR | 0.862 | 0.858 | 0.847 ↓ |

结论: 字符 n-gram 余弦与 BM25 高度同源(都是词面), 在 146 条小语料上只引入噪声 → sem=0.0,
tfidf 后端仅作无 jieba/rank_bm25 环境的降级保底。真语义升级靠 R3b 的中文 embedding 模型
(AI-ModelScope/bge-small-zh-v1.5, ModelScope 源)。

## R4 多样性与反馈 (routing/diversity.py: MMR λ=0.85 + routing/feedback.py: 事件分型反馈)

| 指标 | R2 | R4 | Δ |
|---|---|---|---|
| 可覆盖命中率 | 0.935 | 0.935 | 0 |
| 可覆盖MRR | 0.862 | 0.862 | 0 |
| famcov@9 | 6.02 | 6.12 | +0.1 |
| monopoly@9 | 0 | 0 | 0 |

λ 扫描: 0.72/0.60 开始损失命中(0.903), 0.85 是帕累托点 → 配置定 λ=0.85。
反馈层(依调研 Top1 改造): 展示日志事件分型 shown/picked/vetoed, 指数衰减半衰期 2 天, 单 seg 封顶 2.5,
picked 不罚(展示≠不想要); taste.md 的"选了 segXXX"→+0.5 口味加权, "否决 segXXX"→-1.5;
新增确定性 ε-greedy 探索槽(top9 末位给累计曝光最低的可行候选), 防头部垄断。



## R3b 语义通道定稿 (routing/semantic.py 行级 bge + routing/fusion.py RRF)

模型: AI-ModelScope/bge-small-zh-v1.5 (ModelScope 源, 24M/512维); 行级编码(use_when/triggers/anti_when/plain/style/type_zh 各自成行)取 max 余弦, 指纹缓存 _sem_cache.npz。
诊断记录: ①tfidf 字符 n-gram 与 BM25 同源无增益(R3a); ②bge 整段/行级分数易饱和(多行 1.0 平手), 检索指令前缀必须带(疗效差异 rank2→1); ③语义只能做弱通道。

| 指标 | R2 线性 | R3b RRF(sem=0.5) |
|---|---|---|
| 可覆盖命中率 | 0.935 | 0.935 |
| 可覆盖MRR | 0.862 | 0.856 |
| famcov@9 | 6.12 | 6.24 |
| novelty | 68 | 65 |

评测打平但采用 RRF: 各通道按排名融合免归一免调参(Elasticsearch 同款), 对评测集之外的新说法更稳,
famcov 更优。权重定稿 rule=1.0 / lex=1.0 / sem=0.5 / rrf_k=60。

## R3b 补充: RRF 三通道评测 (bge 行级语义通道)

| 指标 | R2 线性 | RRF(rule+lex) | RRF(+sem=0.5) |
|---|---|---|---|
| 可覆盖命中率 | 0.935 | 0.935 | 0.935 |
| 可覆盖MRR | 0.862 | 0.833 | 0.856 |
| famcov@9 | 6.17 | 6.33 | 6.24 |

诊断: ①字符 n-gram tfidf 与 BM25 同源无增益; ②bge 行级分数易饱和(多行 1.0 平手, max 聚合受行数偏置),
检索指令前缀必须带(疗效差异 rank2→1); ③语义通道在 146 条小语料 + 短意图场景**评测无增益**。

## R5 轻量化定稿 (用户约束: skill 必须可移植, 不嵌入模型)

语义通道降为**默认关闭的可选增强**: `_weights.json sem=0.0` → 融合走线性(rule + 2.2×BM25, R2 最优);
本地装了 bge 模型且 sem>0 时才启用 RRF 三通道, 未装自动降级。运行依赖只有 jieba + rank_bm25(纯 Python)。
架构收编: routing/{query,rule,lexical,semantic,fusion,diversity,feedback}.py, route.py 瘦身为编排+CLI。
新增: 拒绝机制(三通道全弱 → 如实说"没有合适的"并给改述建议, 评测零误拒);
route.py --pick/--veto 事件记录(picked 不罚 / vetoed 重罚)。

## 最终指标 (默认轻量配置, 档案覆盖 68/146)

| 指标 | R0 基线 | R5 定稿 | Δ |
|---|---|---|---|
| hit@5 | 0.595 | 0.690 | +9.5pt |
| MRR@9 | 0.506 | 0.636 | +13.0pt |
| 可覆盖命中率 | 0.806 | 0.935 | **+12.9pt** |
| 可覆盖MRR | 0.685 | 0.862 | **+17.7pt** |
| famcov@9 | 6.0 | 6.17 | +0.17 |
| monopoly@9 | 0 | 0 | 0 |
| novelty | 54 | 68 | +14 |

未覆盖档案的案例仍随流水线生产推进自动改善(可覆盖率从 62% 升至 88%)。

## R5+ 调研吸收 (NL2VIS 报告 Top 项落地)

- 否定窗口守卫: 触发词前 3 字窗含"不/别/无/非/无需"不算命中(rule.py _negated, 学 NL4DV)
- 数据画像软约束: routing/datashape.py — 行和≈100→构成加分 / 时间列→趋势加分 / 组列2-8组且组内≥3→组间加分
  (DeepEye/SeeDB 轻量版, 仅 --data 时生效, 评测零回归)
- Resonance 澄清问题库 5 问(stages/2, data-to-viz 式, 仅 top 候选跨家族分裂时问)
- anti_when 结构化({dim,op,val,w} 机器字段): 并入终审波任务(生产+审计全齐后由终审智能体逐档案补)

## R5++ 中文检索调研吸收 (报告: _research_chinese_lexical.md)

- BM25 参数 k1=1.2/b=0.3(短文档): 评测持平, 采纳(依据更强)
- HMM=False: **回退**——评测 0.935→0.903, 实测有害
- 字符 bigram 容错通道(lex2_linear): 评测 0.860 vs 0.862, 无增益 → 默认关闭保留开关
  (对错别字/中英混写稳健, 用户口语输入质量差时可手动打开)
- 词林同义词表构建期扩容 / pypinyin 拼音容错: 记入调研报告, 有真实需求再做
