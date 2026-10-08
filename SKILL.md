---
name: paper-figures
description: >-
  看图选图、照图画图的论文绘图闭环，自带 146 个顶刊案例的图库（Nature/Science/Cell 风格，
  每张配鉴赏卡片和可运行配方）。不让用户用文字描述"要什么图"，而是把候选图摆成样板册让用户挑、
  支持自由组合（A 的布局 + C 的配色），再用用户的数据画出来并与参考并排品评。
  只要用户想画图、配图、做 figure、可视化数据、问"这个数据怎么画好看"、说"帮我出张图"、
  给了一张例图想要同款、想换配色或版式、投稿需要出版级图表、问该用哪种图表类型，
  都应使用本技能，即使用户没有提到图库或技能名。也用于维护图库：加图、删图、去重、重建索引。
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
2. **省上下文**：先读 `reference/gallery-index.md` 头部的用途词统计 → `grep` 用途词定位行 →
   只 Read 命中的 2-3 张卡片，不要整份读索引或整目录扫图。
3. **无图显示能力时**（纯文本会话）：改为按卡片 `purpose` 给出 3 个文字候选 + 参考图路径，
   让用户自己在看图器里打开比较。
4. **环境异常**：先跑 `python scripts/doctor.py`，把缺失项（依赖/字体/数据文件）一次性报给用户。

## 图库

```
gallery/              146 张已验收成品 case_segNNN.png（图库主体，随技能分发）
gallery/cards/        每图一张鉴赏卡片（purpose/data/recipe 词表见 stages/1）
scripts/recipes/      146 个可独立运行的配方（改数据段即得成品）
scripts/              工具链: gen_cards / build_index / make_contact_sheet / new_case / show / doctor / test_helpers
reference/            catalog.json(全部元数据) · selection.md(决策表) · style_guide.md(风格+坑) · gallery-index.md
stages/               四阶段细则
taste.md              用户品味记录（本机，逐次追加）
assets/map_data/      地图类配方依赖的 GeoJSON
integrations/         各 agent 的 slash commands 与 AGENTS.md 指针片段
requirements.txt      Python 依赖清单
```

常用命令（技能目录下运行）：

```bash
python scripts/make_contact_sheet.py sheet --out /tmp/sheet.png "5::我的推荐" "69::贴近你的口味" "121" --open
python scripts/make_contact_sheet.py sheet --out /tmp/sheet.png --family volcano --sample 6
python scripts/make_contact_sheet.py compare --out /tmp/cmp.png <seg> --open
python scripts/show.py /tmp/sheet.png            # 在用户屏幕上打开
python scripts/build_index.py                    # 重建索引(用途词统计在头部)
python scripts/gen_cards.py                      # 从 catalog 重建全部卡片
python scripts/new_case.py --from 005 --name my-fig --title "..."   # 加图脚手架
python scripts/doctor.py                         # 环境与图库自检
python scripts/test_helpers.py                   # 特殊图型助手冒烟
```

## 选型速查（详见 reference/selection.md 与 stages/2-resonance.md）

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

## 数据输入约定（用户给数据时走这条链）

1. **读**：`from data_io import load; df = load('data.csv')` —— 支持 csv/tsv/xlsx/json，编码自动尝试。
2. **校验**：`validate(df, <seg>)` —— 对照 `reference/data-schemas.json` 里该案例的输入契约
   （format: long/wide/matrix/edges/sets/xy/newick + 必需列/类型）。
   校验 FAIL 时把 errors 报给用户（缺什么列、什么类型不对），**不要静默造数据补列**。
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
# 注意: ① 脚本移出技能目录时, 把头部 sys.path 改为技能 scripts 目录的绝对路径;
#      ② 量纲变化后检查相对 ylim 的偏移(星号高度等已是相对量); ③ 模拟数据要标 example data
```
