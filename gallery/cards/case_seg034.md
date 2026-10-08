---
title: Nature 火山图&富集网络图
kind: 数据图
purpose: [差异展示, 排序, 网络与流向]
data: 蛋白log2FC/P;通路ES+相似度边表
input: long (reference/data-schemas.json #034)
journal: Nature
recipe: scripts/recipes/case_seg034.py
preview: ../case_seg034.png
---

**一句话**：火山图+富集网络（Nature 风格）

**部件亮点**
- 结构布局：2×2:左列2火山图,右列2网络图
- 编码方式：火山图上调紫/下调红着色,灰不显著,竖虚线阈值,基因名标注;网络图灰线连聚类圆圈,节点按ES渐变

**复现**：配方 `scripts/recipes/case_seg034.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
