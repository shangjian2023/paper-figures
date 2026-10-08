---
title: Microbiome Upset图(一)
kind: 数据图
purpose: [网络与流向]
data: 8集合元素交集计数
input: sets (reference/data-schemas.json #114)
journal: Microbiome
recipe: scripts/recipes/case_seg114.py
preview: ../case_seg114.png
---

**一句话**：UpSet图（Microbiome 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：顶部交集条形+数值,左侧setSize条形,8集合点阵连线;彩色版紫/橙条;用 helpers.upset.upset_plot_pro

**复现**：配方 `scripts/recipes/case_seg114.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
