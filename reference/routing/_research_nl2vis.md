# NL→Vis 路由机制外部调研（自然语言意图 → 图型）

调研日期：2026-10-11。取证方式：WebSearch + 直接抓取 GitHub 源码/文档（Draco 的 ASP 知识库、NL4DV 的 constants.py、nvBench 的 README、data-to-viz 官网均为一手证据）。

**我们的现状锚点**（对照对象，见 `scripts/route.py` + `scripts/routing/query.py`）：
- 五层路由：触发词子串匹配 + PURPOSE 十类同义词 + use_when 词面重合 + BM25/语义分 + 数据契约惩罚 + 反馈/多样性。
- `PURPOSE_SYNONYMS` 十类：组间比较 / 分布形态 / 相关关系 / 构成占比 / 趋势变化 / 网络与流向 / 空间分布 / 多指标综合 / 差异展示 / 排序降维。
- 槽位抽取：组数/变量数/类别数/时间点/样本数（中文数字→阿拉伯）；anti_when 里的可判定界限用 `BOUND_RE` 从自由文本里"猜"出来再机器比对。
- 146 档案的 anti_when 是自然语言句子，机器只利用了其中一小部分。

---

## 1. Draco / Draco2 —— 把设计知识写成"硬约束 + 加权软约束"

**是什么**：CMU/UW 的可视化设计约束求解器，知识库用 Answer Set Programming（ASP，Clingo 求解）写成。推荐 = 枚举所有合法设计 → 按违反软约束的加权和（cost）排序取 top-k。

**一手证据**（uwdata/draco 仓库 asp/ 目录）：
- `define.lp`：事实域定义——marktype(point;bar;line;area;text;tick;rect)、字段类型(quantitative/ordinal/nominal/temporal)、通道(x;y;color;size;shape;text;row;column;detail)、聚合操作、stacking(zero;normalize)、**tasks(value;summary)**。数据侧每字段只喂 4 个属性：**type / cardinality / entropy / extent(min,max)**。
- 图型族由数据形状推导：`is_c_c`（连续×连续）、`is_c_d`、`is_d_d` —— 正是"数据形状→图型"的机器可读写法。
- `hard.lp`：表达力硬约束，全部是我们可以直接抄的 anti_when 母题：
  - 数值字段配字符串类型 → 非法（`enc_type_valid`）；
  - log 轴要求正值连续字段（`log_non_positive`）；负值数据不用 size/面积通道（`size_negative`）；nominal 不上 size 通道（`size_nominal`）；shape 通道要求 nominal（`shape_discrete_non_ordered`）。
- `soft.lp`：加权偏好，例子（每条 = 一个条件谓词 + 权重）：
  - "shape 通道基数 >5 要罚"（`shape_cardinality`）；"数值列别当 nominal"（`number_nominal`）；"binned 后基数 <15 罚"（`bin_cardinality`）；"x、y 都是离散且不聚合 → 遮挡，罚"（`x_y_raw`）；"extent 跨 0 时别强行含 0 基线"（`includes_zero`）。
- `weights_learned.lp`：**按"数据形状×图型"存学习到的权重**——c_c_line=+309、c_c_point=−397（连续×连续数据里，线图被偏好、点图被惩罚，来自 Kim2018/Saket2018 感知实验回归）。这是"实验先验 → 权重表"的范例。
- Draco2（arXiv:2308.14247）改进在工程化：entity 层级（root/view/mark/encoding/scale）+ `@definition` 注解的域声明 + 多视图/分面 + 测试套件；task 域仍是 value/summary——**任务语义并不靠求解器，靠的是上游 NL 层**。

**对我们的移植点**：
1. anti_when 不该是"一段话"，该是**谓词+权重**。Draco 每条软约束 = `{条件: 维度谓词, 动作: 罚分}`。我们的 146 条 anti_when 可以升级成结构字段（保留原文做展示）：`{"dim":"组数","op":">","val":8,"w":-2.8,"text":"分组因素超过1个..."}`，`query.parse_bounds` 就不用正则猜句子了。
2. **每字段 4 属性画像**（type/cardinality/entropy/extent）是最小够用集——--data 时算这些就够了，不用 VizML 的 745 维。
3. "数据形状×图型"的先验权重表可以手工起步（抄 is_c_c/is_c_d/is_d_d 分类 + 常识初值），以后有 route_log 累积的选择数据再学。
4. stacking(zero;normalize) 正好对应我们"构成占比"里"原始计数堆积 vs 百分比堆积"两分支——构成判据应问"是否和为100%"。

---

## 2. DeepEye / Compass(SeeDB) / VizML —— 数据特征 → 图型推荐

**DeepEye**（清华，ICDE 2018，https://dbgroup.cs.tsinghua.edu.cn/icde18-deepeye）：
- 关键词驱动：从数据里抽 4 类特征（column 类型/分布/基数 + 列间关系），枚举候选可视化，**规则判断图型对不对（时间列+数值→line；低基数类别+数值→bar/pie；两数值列→scatter）**，再训练二叉决策树把候选分 good/bad 排序。只支持 bar/pie/line/scatter 四类。
- 对我们的意义：**规则层和分类层分开**——确定性形状规则先过滤，剩下靠打分。我们已经有 data_io.validate 做硬过滤，缺的是"形状加分"软层。

**Compass / SeeDB**（MIT，Vartak 硕士论文 "Towards Visualization Recommendation Systems"；SeeDB PVLDB 2013，http://www.vldb.org/vol7/p325-parameswaran）：
- 查询驱动推荐：对用户查询枚举聚合视图，按"与参照分布的偏差(deviation)"定义 interestingness 排序，overview+detail 两段式。
- 对我们的意义有限（我们是意图驱动不是查询驱动），但其"**先摆全景、再收窄**"的两段式与 Resonance 的样板册→收窄流程同构。

**VizML**（MIT Media Lab，CHI 2019，arXiv:1808.09599，https://github.com/mitmedialab/vizml）：
- 119,815 对 Plotly 数据集-图表对，**~745 维特征**训练 RF/NN 预测图型选择与列编码：
  - 单列特征：类型、唯一值数（基数）、偏度、峰度、熵、缺失率、分位数等；
  - 列对特征：Pearson/Spearman 相关、互信息(MI)及其显著性检验。
- 对我们的意义：**别学它端到端 ML（离线+146 样本撑不起），学它的特征字典**。我们画像只需要其单列特征的骨架：类型、基数、是否有时间列、数值列占比、min/max（跨0?）、偏度近似；列对特征取一个：数值对相关/时间列存在性。

**成熟规则清单（可立即机器化为过滤/加减分条件）**——综合 Draco+DeepEye+data-to-viz：
| 数据形状特征 | 约束/倾向 | 出处 |
|---|---|---|
| 时间/有序列 + 数值列 | 趋势类（curve/area）优先 | DeepEye, Draco c_c/trend 权重 |
| 两数值列 | scatter/curve 拟合优先 | DeepEye, Draco is_c_c |
| 类别基数 ≤5 且单数值 | bar/pie 系 | Draco shape_cardinality, DeepEye |
| 类别基数很大（>15-20） | bar 失效 → 热图/山脊/排序条形 | Draco bin_cardinality, data-to-viz |
| 每组只有 1 个聚合值 vs 多个原始观测 | 前者禁分布图（无分布可画）；后者柱形图信息损失 | data-to-viz "1 vs several obs/group" |
| 构成列各行和=100% | 堆叠/ternary/pie 族合法；否则禁百分比堆叠/三元 | Draco stacking(zero;normalize) |
| 数据含负值 | 禁 pie/area/size 通道；柱状基线不强制 0 | Draco size_negative/includes_zero |
| 数值跨度 >2 个数量级 | 禁线性轴柱形 → log/断轴 | seg001 anti_when 已有，业界同款 |
| 变量数 ≥3 数值 | 热图/相关矩阵/降维 | data-to-viz "many numerics" |
| 点数 >~2000 | 散点遮挡 → 2D 密度/六边形 | data-to-viz 阈值分支 |

---

## 3. NL4DV / DataTone / Eviza —— NL 查询 → 分析规格的槽位抽取

**NL4DV**（Georgia Tech→独立组织，TVCG 2020，https://github.com/nl4dv/nl4dv，文档 https://nl4dv.github.io/nl4dv）：
- 输入=数据表+NL 查询，输出=**同一份分析规格 JSON**（属性列表 + 分析任务列表 + Vega-Lite 候选）。三个组件：attribute genie / task genie / vis genie。
- v1（2020）纯语义解析：属性检测=词典精确匹配→别名→词形还原→**模糊/语义相似度**四级，打分 exact=1.0 / similarity=0.9 / alias_exact=0.8 / alias_similarity=0.75（utils/constants.py 的 match_scores）；属性类型用列数据自动判定 dimension/measure。
- `task_keyword_map`（一手源码）把 **Amar et al. 2005 低层分析任务**做成了关键词表：find_extremum（max/highest/best→MAX；min/lowest/worst→MIN）、sort、filter（higher/lower/between/after/before→GT/LT/RANGE）、derived_value（average/sum/total/cumulative）、distribution（distribute/range/extent）、outlier（outlier/exception）、correlation（correlation/relationship）、trend、negation（not）。
- `vis_recos.py` 是一张硬编码决策表：按（属性个数×类型组合×任务）索引 → 每任务给候选 mark。distribution→bar/tick/boxplot；trend→line/area；correlation→point；derived_value+distribution→bar/arc。
- 演化：v2（2022）多轮对话+歧义消解；v3（2024）NL4DV-LLM——**可选 LLM 路径，输出与 v1 完全同一份规格 JSON**（LiteLLM 多后端）；v4（2025）加样式指令。
- **结论（词典够不够）**：NL4DV 自己给出的答案是"双层都接同一规格"——词典解析负责召回和零成本离线，LLM 负责消歧、槽位补全和没见过的表达。我们的 query.py（同义词组+槽位正则）≈ NL4DV v1 的子集，**升级方向不是换 LLM，而是先补上：四级置信度打分、negation 处理、任务槽位表**；LLM 只在 Resonance 阶段作为可选的意图改写器。

**DataTone**（UIST 2015）：把系统的解释（把"糖尿病"理解成列名还是值？）做成**歧义小部件**摆在用户面前一键改。→ 对应我们把路由的 `why/注意` 展示出来让用户纠偏，已有雏形（菜单+route_log）。

**Eviza**（UIST 2016，用户提的"evize"即此）：对查询做**概率解释**（保留多个候选解释而非取一个），支持隐式值/显式值切换与后续追问。→ 我们 top-N 多样性候选本身就是"概率解释"的产品化，不必学它的内部。

---

## 4. nvBench / Text2Vis —— 基准的数据组织与任务分类体系

**nvBench**（清华，https://github.com/TsinghuaDatabaseGroup/nvBench）：首个大规模 NL2VIS 基准，25,750 对（NL,VIS），750 张表 105 个域。关键设计：
- 中间语言 **VQL**：`Visualize <CHART> SELECT ... GROUP BY ... [BIN BY ...]`——把"图型选择"和"数据变换"解耦。
- 7 种图型：Bar、Pie、Line、Scatter、Stacked Bar、Grouping Line、Grouping Scatter；`classify` 字段编码 Z 轴（分系列）。
- 难度分级 Easy/Medium/Hard；任务五分类（继承 Weaver/nvBench 论文）：**TREND / CORRELATION / DISTRIBUTION / COMPARISON / COMPOSITION**。
- **nvBench 2.0**（NeurIPS）：专攻**歧义**——一个 NL 查询对应多个合理可视化（7,878 查询 24,076 个 vis），评测"能否列出全部合理解释"而不是押一个。

**Text2Vis**（2025，arXiv，多模态 text2vis 基准）：20+ 图型，查询类型含 trend/correlation/anomaly/predictive 等，配自动评测。

**与我们 PURPOSE 十类的对齐表**：
| 我们十类 | nvBench/学界对应 | 状态 |
|---|---|---|
| 组间比较 | COMPARISON | ✅ |
| 分布形态 | DISTRIBUTION（Amar: characterize distribution） | ✅ |
| 相关关系 | CORRELATION | ✅ |
| 构成占比 | COMPOSITION | ✅ 但缺"原始计数堆积 vs 100% 堆积"二分 |
| 趋势变化 | TREND | ⚠️ 混入了剂量-响应（本质是 relationship/dose-response，非时间） |
| 网络与流向 | data-to-viz network 分支 / Sankey 系 | ✅（学界基准基本不覆盖，我们反而全） |
| 空间分布 | map 分支 | ✅（同上） |
| 多指标综合 | profile（雷达/平行坐标/多指标热图） | ⚠️ 名字偏"评价"，profile 语义可再显式化 |
| 差异展示 | DEVIATION（火山/森林/Michaelis-Menten 系） | ⚠️ 同义词"差异"同时挂在组间比较类，两类有词面冲突 |
| 排序降维 | cluster/ordination（Amar: cluster） | ✅ 但把 ranking 混进来了 |
| **缺：极值排名** | Amar: find_extremum/sort；"哪个最高/TopN/排名" | ❌ 目前靠"组间比较"兜底 |
| **缺：离群异常** | Amar: outlier/anomaly；Text2Vis: anomaly | ❌ 分布形态部分兜底 |
| 缺：不确定性 | 误差棒/置信带是特征不是用途，现状合理 | —（保持 trigger 层即可） |

---

## 5. data-to-viz / Abela cheat sheet —— 决策树的问题节点设计

**data-to-viz**（https://www.data-to-viz.com，Yan Holtz，有配套 R/Python/D3/React 图库）：
- 决策树**不问目标、只问数据形状**。5+1 个入口：numeric / categoric / num&cat / maps / network（时序走"有序"分支）。节点问题全是我们槽位该有的：
  - 几个变量？（1 数值→直方/密度；2 数值→散点；3 数值→气泡/3D；多数值→相关矩阵/PCA）
  - **数据有序吗？**（有序→line/area/streamgraph；无序→scatter/density）
  - **多少个点？**（两数值场景 ~2000 点阈值：少→散点/箱线；多→2D 密度/小提琴）
  - **每组 1 个观测还是多个观测？**（1→bar/lollipop/treemap；多→box/violin/ridge）
  - **有层级吗？**（嵌套→treemap/sunburst/dendrogram；并列→venn）
  - 网络分支：边表还是邻接矩阵？边带权吗？（→Sankey/chord/arc）
- 每张图页配 **Common Mistakes**（如"箱线图隐藏了每组样本量"）+ 全站 12 条 caveats 画廊——**这就是英文版的 anti_when**，且每条都能翻译成谓词。
- **Abela "Chart Suggestions"**（2009，extremepresentation.typepad.com）：四象限 cheat sheet（comparison/distribution/composition/relationship × 时间/类别、多少数据点），Tableau 有互动改编。**调研确认：没有公开的机器可读 JSON 实现**——要结构化只能自己编码，规模很小（4 意图×几个分支）。

**对 Resonance 阶段的"反问补全"借鉴**：
- 我们的原则是"能摆图就不提问"（stages/2-resonance.md），与 data-to-viz 把问题全部前置到"数据形状"一致：**形状问题答案大多能从 --data 直接算出来，真正要问用户的只剩两类**——(a) 数据文件没给；(b) 同一数据多种合理解释（nvBench 2.0 的歧义场景）。
- 可借鉴的"澄清问题库"（只在 top-N 候选的 family 分裂时才问）：
  1. 每组是单个聚合值还是原始多次观测？（决定 bar 系 vs 分布系）
  2. 构成数据各行是否加和为 100%？（决定堆叠/三元是否合法）
  3. x 是时间/剂量还是无序类别？（决定趋势类 vs 比较类）
  4. 要看总量还是看占比？（stacking zero vs normalize）
  5. 类别有层级/交集关系吗？（决定 treemap/桑基/venn 分支）
- 每个问题都应有"问了就能把候选砍半"的判据，否则按我们的原则改摆图。

---

## Top5 可落地改造（按性价比排序）

1. **anti_when 结构化升级（谓词+权重+原文三段式）**——给 146 档案的 anti_when 加机器字段 `{"dim","op","val","w","text"}`，`query.parse_bounds` 改读字段、原文仅做展示兜底。学 Draco 的 hard/soft 分层。依赖成本：一次性半自动改 146 个 segNNN.json（BOUND_RE 可做初稿再人工校）+ query.py 小改；纯离线；**收益可被 route_eval 直接度量，是其他一切机器比对的地基**。
2. **数据画像 → 形状软约束层**——--data 时算最小画像（列类型/组数/类别基数/是否时间列/数值列占比/min-max 跨0/行和是否100%/每组观测数），按第 2 节规则表对候选加减分（如：时间列→curve+，构成和100%→堆叠族+，负值→pie/area−，基数>20→bar−）。学 DeepEye"规则先滤、打分随后"。依赖成本：data_io.py 加一个 profile() + route.py 一个打分层；pandas 已有；中低成本。
3. **PURPOSE 补两类 + 修一处冲突**——加"极值排名"（哪个最高/TopN/排名/前三）与"离群异常"（离群/异常/outlier/偏差点）；把"差异"一词从组间比较同义词表挪走或限定为"差异基因/差异代谢物"复合词，消除与"差异展示"的词面冲突。依赖成本：route.py 常量表改动+route_eval 回归；零依赖，半小时级。
4. **NL4DV 式触发词分级打分 + 否定窗口**——触发词命中按 精确/别名/模糊 分级加权（1.0/0.8/0.6）；"不/无需/别/非"前 3 字窗内的触发词转为 anti 信号。依赖成本：lexical.py/semantic.py 小改；需 route_eval 全量回归防退化；中成本中收益。
5. **Resonance 澄清问题库**——把第 5 节 5 问写进 stages/2-resonance.md 作为"仅当槽位缺失且 top 候选跨家族分裂时才问"的标准问题清单，问完直接喂 route.py 槽位。依赖成本：纯文档约定；零依赖；即时可用。

**最值得先做：#1**。理由：anti_when 的结构化是 #2 的输入、#3 回归的基准、也是唯一同时提升"正确性"与"可解释性"且能被现有 route_eval 客观验收的改造。
