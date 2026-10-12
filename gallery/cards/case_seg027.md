---
title: Nature 和弦图
kind: 数据图
purpose: [网络与流向]
data: 节点×节点流量方阵
input: edges (reference/data-schemas.json #027)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg027.py
preview: ../case_seg027.png
---

**一句话**：和弦图（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：8-40 个节点之间的流量/关联总量，想用环形弦带做'一眼惊艳'的总览

**有什么用**：一个圆环，各类条目沿边排开，谁和谁有关系就在中间拉一条带子，带子越宽关系越强；适合做总览或开场图，气势足、一眼记住。

**部件亮点**
- 结构布局：单面板
- 编码方式：环形和弦:节点弧+贝塞尔带,带色=源节点;用 helpers.chord.chord_diagram

**复现**：配方 `scripts/recipes/case_seg027.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
