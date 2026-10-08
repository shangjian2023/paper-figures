---
title: Nature FC-FC
kind: 数据图
purpose: [组间比较, 差异展示]
data: 每基因两条件log2FC+分类
input: long (reference/data-schemas.json #081)
journal: Nature
recipe: scripts/recipes/case_seg081.py
preview: ../case_seg081.png
---

**一句话**：FC-FC四象限散点（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：两轴log2FC;0横虚线与±0.5竖虚线;紫(同向)/品红/蓝(反向)/灰(NS);四角↑↓注Discordant/Concordant

**复现**：配方 `scripts/recipes/case_seg081.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
