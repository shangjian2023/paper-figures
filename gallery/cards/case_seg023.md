---
title: Nature 相关性热图
kind: 数据图
purpose: [相关关系]
data: 约90基因相关矩阵+模块归属
input: matrix (reference/data-schemas.json #023)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg023.py
preview: ../case_seg023.png
---

**一句话**：三角相关聚类热图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：约 50-150 个基因的相关矩阵，先聚类再画，讲清 2-4 个共表达模块

**有什么用**：把几十个基因两两比较“是否同步起落”，先自动把爱抱团的归成几族再画成三角彩格：红=同步、蓝=相反；顶部小树状图交代谁和谁一组。

**部件亮点**
- 结构布局：下三角热图+顶部聚类树
- 编码方式：下三角红白蓝相关热图;顶部模块聚类树+灰底模块标签;基因名沿对角线放射;右下ρ色条

**复现**：配方 `scripts/recipes/case_seg023.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
