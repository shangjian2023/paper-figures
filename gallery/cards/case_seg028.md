---
title: Science 火山图
kind: 数据图
purpose: [差异展示, 排序]
data: 约5000基因(log2FC,adjP)+基因集
input: long (reference/data-schemas.json #028)
journal: Science
recipe: scripts/recipes/case_seg028.py
preview: ../case_seg028.png
---

**一句话**：火山图+基因集条纹带（Science 风格）

**部件亮点**
- 结构布局：主火山图+底部基因集条纹带
- 编码方式：灰空心点;左右Top200虚线框;橙点=显著;关键基因气泡标签;α=0.05虚线;底部UP/DN条纹+ES/pval

**复现**：配方 `scripts/recipes/case_seg028.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
