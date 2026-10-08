---
title: Nature 三元图(6)
kind: 数据图
purpose: [构成占比, 相关关系, 分布形态]
data: 三维概率向量
input: long (reference/data-schemas.json #129)
journal: Nature
recipe: scripts/recipes/case_seg129.py
preview: ../case_seg129.png
---

**一句话**：三元核密度图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：紫白渐变KDE等高线叠加灰细散点;三顶点0/1.0;三支彩色箭头;虚线中线;右上Probability色标

**复现**：配方 `scripts/recipes/case_seg129.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
