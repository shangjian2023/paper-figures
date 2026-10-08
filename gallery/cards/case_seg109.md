---
title: Nature 多分组火山图(二)
kind: 数据图
purpose: [差异展示, 排序]
data: 长表:基因,脑区,log2FC,pct
input: long (reference/data-schemas.json #109)
journal: Nature
recipe: scripts/recipes/case_seg109.py
preview: ../case_seg109.png
---

**一句话**：分面火山图（Nature 风格）

**部件亮点**
- 结构布局：上排9区分面+下排3区放大
- 编码方式：灰底点+每区彩色高亮DE基因带引线基因名,y=avg_log2FC带0虚线,x=表达百分比0-80

**复现**：配方 `scripts/recipes/case_seg109.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
