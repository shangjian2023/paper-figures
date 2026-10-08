---
title: Nature 火山图+富集图(三)
kind: 数据图
purpose: [差异展示, 排序]
data: 两组蛋白log2FC/p;富集FDR
input: long (reference/data-schemas.json #113)
journal: Nature
recipe: scripts/recipes/case_seg113.py
preview: ../case_seg113.png
---

**一句话**：火山+发散条形（Nature 风格）

**部件亮点**
- 结构布局：2×2:2火山+2发散条形
- 编码方式：火山黄/绿、紫/淡紫标上下调+图例+基因标注;条形上调右bar下调左bar,x=-log10FDR

**复现**：配方 `scripts/recipes/case_seg113.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
