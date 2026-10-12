---
title: Nature FC-FC
kind: 数据图
purpose: [组间比较, 差异展示]
data: 每基因两条件log2FC+分类
input: long (reference/data-schemas.json #081)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg081.py
preview: ../case_seg081.png
---

**一句话**：FC-FC四象限散点（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：每个基因/蛋白在两种干预或基因型下各有一个 log2FC，想按同向（concordant）、反向（discordant）、不显著分类上色

**有什么用**：每个基因按两种条件下的变化幅度定位置：落在对角线一带的是两个条件同向变化，跑偏的是少数例外，一眼看出绝大多数基因步调一致。

**部件亮点**
- 结构布局：单面板
- 编码方式：两轴log2FC;0横虚线与±0.5竖虚线;紫(同向)/品红/蓝(反向)/灰(NS);四角↑↓注Discordant/Concordant

**复现**：配方 `scripts/recipes/case_seg081.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
