---
name: paper-figures
description: >-
  看图选图、照图画图的论文绘图闭环，自带 146 个顶刊案例的图库（Nature/Science/Cell 风格，
  每张配鉴赏卡片和可运行配方）。不让用户用文字描述"要什么图"，而是把候选图摆成样板册让用户挑、
  支持自由组合（A 的布局 + C 的配色），再用用户的数据画出来并与参考并排品评。
  只要用户想画图、配图、做 figure、可视化数据、问"这个数据怎么画好看"、说"帮我出张图"、
  给了一张例图想要同款、想换配色或版式、投稿需要出版级图表、问该用哪种图表类型，
  都应使用本技能，即使用户没有提到图库或技能名。用户要"高级感/惊艳/顶刊范"的图时
  按 wow 分级精确选图。也用于维护图库：加图、删图、去重、重建索引。
---

# Paper Figures — 看图选图、照图画图

规则写不尽"好看"，但样例可以。图库里有什么图，就能画出什么气质的图。所以：

- **把对的图摆到用户面前**让他们用眼睛选，而不是用文字描述要什么；
- **给出你自己的推荐**（面向发表时受众的眼光比个人口味重要），但最终选择权在用户；
- **数据的事全部自己处理**：读文件、整理、变形都由你来做。

## 四个阶段

| 阶段 | 做什么 | 细则 |
|---|---|---|
| **Appreciation** 鉴赏 | 看懂图库每张图（卡片+索引）；加图、删图、去重 | `stages/1-appreciation.md` |
| **Resonance** 共鸣 | 把候选图摆成样板册，和用户一起选出方向 | `stages/2-resonance.md` |
| **Rendition** 演绎 | 用用户的数据把选中的图画出来 | `stages/3-rendition.md` |
| **Appraisal** 品评 | 对照参考检查、并排比较给用户、决定是否入库 | `stages/4-appraisal.md` |

进入某阶段前先读对应细则，不要凭印象做。

## 从哪里进入

- **用户要画图**（有数据或只有用途）→ Resonance → Rendition → Appraisal
- **用户要"高级/惊艳/顶刊范"的图** → Resonance 的 wow 通道：wow=3 样板册起手（`--min-wow 3`），
  再按数据情形收窄——见 `reference/selection.md` 高级感速查
- **用户给了一张例图**想要同款 → Resonance 的 example 入口
- **用户说"你定""直接画"** → Resonance 快速路径：直接画首选，附两个备选
- **用户要加图、删图、整理图库、问案例编号** → Appreciation
- **用户问某种数据该用什么图** → 先答选型（`reference/selection.md`），再摆 2-3 张候选确认

一轮画完不是终点：用户看成品有了新想法，就回 Resonance 或 Rendition 再走一圈。

## 终端（TUI）运行约定

本技能运行在终端 agent（Claude Code / Codex / ZCode / OpenCode / DSH 等）中，呈图与省上下文有固定做法：

1. **给用户看图**：生成样板册/对照图后，用 `python scripts/show.py <png> ...` 打开系统看图器
   （加 `--print-only` 只打印路径不弹窗，适合无人值守）。同时在**对话里给文字菜单**：
   每个候选一行 `A. seg005 云雨图 —— 一句话点评`（取自卡片正文），用户看图选字母，看文字也选得出。
2. **省上下文**：选图先跑 `python scripts/route.py "<意图>" --n 9 --log`（场景路由器，五层打分
   + 多样性硬约束），不要 grep 整份索引；定位到候选后只 Read 命中的 2-3 张卡片。
3. **无图显示能力时**（纯文本会话）：改为按路由器/卡片的场景与反指给出 3 个文字候选 + 参考图路径，
   让用户自己在看图器里打开比较。
4. **环境异常**：先跑 `python scripts/doctor.py`，把缺失项（依赖/字体/数据文件）一次性报给用户。

## 图库

```
gallery/              146 张已验收成品 case_segNNN.png（图库主体，随技能分发）
gallery/cards/        每图一张鉴赏卡片（purpose/data/wow/recipe 词表见 stages/1）
gallery/index.md      全库索引（用途词统计 + 高级感 TOP 在头部；build_index.py 重建）
catalog.json          146 案例全部元数据（seg/期刊/family/features/data/wow…）
scripts/recipes/      146 个可独立运行的配方（改数据段即得成品）
scripts/              工具链: gen_cards / build_index / make_contact_sheet / new_case / show /
                      polish(完美度门禁) / wow_score(高级感分级) / doctor / test_helpers
reference/            selection.md(决策表) · style_guide.md(风格+坑) · data-schemas.json(数据契约)
stages/               四阶段细则
taste.md              用户品味记录（本机，逐次追加）
assets/map_data/      地图类配方依赖的 GeoJSON
integrations/         各 agent 的 slash commands 与 AGENTS.md 指针片段
requirements.txt      Python 依赖清单
```

常用命令（技能目录下运行）：

```bash
python scripts/route.py "三组比较, 要显著性" --n 9 --log      # 场景路由器: 一句话 → 跨家族候选+样板册命令
python scripts/route.py "..." --data data.csv                # 带数据做契约适配+数据画像, 缺列候选降权
python scripts/route.py --pick 5                             # 记录用户选择(picked/vetoed 事件, 反馈层用)
python scripts/route_eval.py                                 # 路由评测(hit@5/MRR/家族覆盖), 调参后必跑
python scripts/make_contact_sheet.py sheet --out /tmp/sheet.png "5::我的推荐" "69::贴近你的口味" "121" --open
python scripts/make_contact_sheet.py sheet --out /tmp/sheet.png --family volcano --sample 6
python scripts/make_contact_sheet.py sheet --out /tmp/wow.png --min-wow 3 --sample 9 --open   # 高级感样板册
python scripts/make_contact_sheet.py compare --out /tmp/cmp.png <seg> --open
python scripts/show.py /tmp/sheet.png            # 在用户屏幕上打开
python scripts/build_index.py                    # 重建索引(用途词统计+高级感 TOP 在头部)
python scripts/gen_cards.py                      # 从 catalog+路由档案重建全部卡片
python scripts/new_case.py --from 005 --name my-fig --title "..."   # 加图脚手架
python scripts/wow_score.py                      # 新图入库后重算 wow 分级
python scripts/polish.py figures/my_fig.py       # 成品完美度门禁(交付前必过)
python scripts/captions.py --segs 5 69 --with-plain --out figures/captions.md  # 文档插图图题(附图下方, 不嵌图内)
python scripts/check_routing.py                  # 路由档案质量校验(146 份齐全性+字段)
python scripts/doctor.py                         # 环境与图库自检
python scripts/test_helpers.py                   # 特殊图型助手冒烟
```

## 选型速查（详见 reference/selection.md 与 stages/2-resonance.md）

- **首选路径是路由器**：`python scripts/route.py "<意图>" --n 9 --log`——146 张图各有场景档案
  （reference/routing/），五层架构：查询理解(同义词/槽位/反指比对) → 三通道打分(规则/BM25/可选语义)
  → 反馈(展示衰减/口味/探索槽) → MMR 多样性重排 → 拒绝机制。调参见 reference/routing/_weights.json
  与 _iteration_log.md；下面的速查表是人工兜底。
- 用户说"要高级/惊艳/顶刊范" → 高级感速查（selection.md 第 0 节）：wow=3 共 32 张按惊艳点分组；
  先摆 `--min-wow 3` 样板册，再按数据情形收窄。wow 是惊艳度不是合适度，数据撑不起就退一档。
- 比较均值/组间差异 → 柱形+散点 (001/006/042)、云雨图 (005/069)、小提琴 (041/121)
- 分布形态 → 箱线 (030)、山脊图 (016/032)、密度 (043)
- 两变量关系 → 散点+拟合 (061/063)、FC-FC (036/037)、气泡 (105)
- 组学大规模 → 热图/点阵 (019/119)、火山 (135/136/146)、曼哈顿 (116)、森林图 (142/144)
- 流向/组成 → 桑基 (045/091)、堆积柱 (072/090)、和弦 (027)、UpSet (114)
- 多指标评价 → 雷达 (057/098)、环形柱 (049/094)、三元图 (125-129)
- 时序 → 折线±SEM带 (077-080)、剂量响应/RCS (065/066)
- 空间 → 世界/中国地图 (051-053/117/118)、发育树圈图 (012-015)

## 风格铁律（详见 reference/style_guide.md）

1. 一律 `from paper_style import *; set_style()`——Arial、8pt、去顶右轴线。
2. 数据说话：散点叠柱/箱展示原始数据；误差棒注明 SEM/SD；显著性用 `sig_bracket()`。
3. 颜色 ≤8 组用 `pal()`；发散数据 RdBu/RdYlBu；标签防重叠（白描边/错位引线）是最高频翻车点。
4. 导出三件套：PNG 300dpi + PDF 矢量 + 脚本，同名放 `figures/`。
5. 交付前过 `python scripts/polish.py figures/<名字>.py` 完美度门禁：文字重叠/导出截断/
   字号事故/**文字压数据与图例盖数据的遮挡**/300dpi 元数据机器先查一遍，POLISH FAIL 先修再进品评
   （细则见 stages/3）；全库层面 `scripts/audit_gallery.py` 对照基线防回退。
6. **逐图讲解**：交付时每张图都要直白讲清"为什么用这张图 / 有什么用 / 注意什么"（stages/3 交付讲解节）。
7. **图名不进图**：用户插图进文档时，图名以文本附在图片下方——用
   `python scripts/captions.py --segs ... --files ... --out figures/captions.md` 生成图题文件一并交付。

## 数据输入约定（用户给数据时走这条链）

1. **读**：`from data_io import load; df = load('data.csv')` —— 支持 csv/tsv/xlsx/json，编码自动尝试。
2. **校验**：`validate(df, <seg>)` —— 对照 `reference/data-schemas.json` 里该案例的输入契约
   （format + 必需列/类型），并按数据形态做结构检查：边表值必须为正、矩阵重复格、
   三元负值/零和、坐标缺失、组样本量不足。校验 FAIL 时把 errors 报给用户
   （缺什么列、什么类型不对），**不要静默造数据补列**；warnings 也要转述——它们标注的正是"能画但画不好看/不可信"的数据坑。
3. **适配**：按配方需要的形态用适配器，返回值直接赋给配方数据变量：
   `as_groups`（组比较→[数组...]）/ `as_matrix`（热图）/ `as_xy`（散点）/ `as_edges`（桑基和弦）/
   `as_ternary`（三元）/ `as_sets`（UpSet）。
4. **示例**：见 SKILL 快速上手；显著性用 `helpers.stats.vs_control(data, control=0)` 实算。
   每个案例的输入 schema 可查 `reference/data-schemas.json`（卡片 frontmatter 的 `input:` 字段有快捷指引）。

## 快速上手：把配方适配到真实数据

**推荐路径**：`python scripts/new_case.py --from 005 --name my-fig --title "..."` 生成脚手架
（自动注入技能路径，复制到任何位置都能跑），再改数据段。

**手改路径**：复制 `scripts/recipes/case_seg001.py` 后只改数据段：

```python
groups = ['Vehicle', 'Low', 'High']
data   = [df[df.dose==g].value.values for g in groups]
stars, padj = vs_control(data, control=0)   # helpers.stats 实算显著性, 别沿用写死的星号
#   注意: stars 按组下标对齐, 对照组那一位是 '-' 占位符——喂 sig_bracket 前先剔除
# 注意: ① 脚本移出技能目录时, 把头部 sys.path 改为技能 scripts 目录的绝对路径;
#      ② 量纲变化后检查相对 ylim 的偏移(星号高度等已是相对量); ③ 模拟数据要标 example data
```
