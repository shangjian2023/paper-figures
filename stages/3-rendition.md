# Rendition 演绎（画图）

目标：用用户的数据把选中的图演绎出来。是演绎不是临摹：学样例的画法和气质，画用户的数据和结论。

## 动手之前

1. **打开选中案例的参考图和卡片**（`gallery/case_segNNN.png` + `gallery/cards/case_segNNN.md`）。
   不要凭记忆画——线宽、留白、标注位置的细节都在图里。
2. **从卡片的 `recipe` 出发改**，不要重写。配方已经过视觉验收，布局/标注骨架保持不动。
3. 用户选的是组合（A 的布局 + C 的配色）时，先写部件清单：

   ```
   结构布局 ← seg045 三层桑基
   配色     ← seg091 的灰底+蓝色高亮流
   显著性   ← seg001 的支架星号
   其余     ← seg045
   ```

## 数据

- **数据接入走 data_io 三步链**：`load()` 读文件 → `validate(df, <seg>)` 对照
  `reference/data-schemas.json` 校验（缺列/类型/缺失率，FAIL 就报给用户）→
  `as_groups / as_matrix / as_xy / as_edges / as_ternary / as_sets` 适配成配方数据形态。
  不要即兴写 pandas 预处理绕过契约——schema 就是用户数据和图库之间的合同。
- 读数、清洗、变形都在脚本里完成；不改用户的原始文件。
- 数据不足以支撑该图（如配对图没有配对 ID）时明确说缺什么，不要编数补上。
- 显著性不要沿用配方里写死的星号：用 `helpers.stats.vs_control(groups, control=0)`
  对真实数据实算（Welch t + Bonferroni，装了 statsmodels 自动升 Dunnett），再喂给标注。
- 用户没有数据时用模拟数据：规模和分布贴近真实研究，图角落标 "example data"，
  脚本开头注释标出替换真实数据的位置。
- **量纲/范围变化时检查魔法数**：配方里相对 ylim 的偏移（如星号高度）已是相对量；
  若遇到硬编码偏移，换算成 `(ylim[1]-ylim[0])*比例` 再改数据。

## 画

- 头部照配方：`from paper_style import *; set_style()`——Arial、8pt、去顶右轴，别手动覆盖。
- 颜色用 `pal()` 系调色板；渐变/发散按 `reference/style_guide.md` 的规则。
- 基因名斜体 `italic_gene()`，显著性支架 `sig_bracket()`。
- 标签防重叠是最高频翻车点：白描边 `path_effects.withStroke` 或排序错位 + 短引线。
- 尺寸沿用样例宽高比；用户点名期刊时按其栏宽（单栏约 89 mm、双栏约 183 mm）用 `cm2in()`。
- 图里出现中文先确认字体（`Microsoft YaHei` 可用），否则出方框。

## 交付

默认输出到用户当前项目的 `figures/`，三件同名：

- `<名字>.png`：300 dpi（`save(fig, name, dirs='figures')`）
- `<名字>.pdf`：矢量，投稿用（`fig.savefig('figures/<名字>.pdf')`）
- `<名字>.py`：脚本开头写清数据路径，可独立重跑

选图阶段的草图不需要三件套，一张 PNG 放临时目录即可。
画完不要直接交付，先进 Appraisal。
