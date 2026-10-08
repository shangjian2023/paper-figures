---
title: 火山图
kind: 数据图
purpose: [差异展示, 排序]
data: 基因log2FC与-log10P+关键子集
input: long (reference/data-schemas.json #136)
journal: 未标注
recipe: scripts/recipes/case_seg136.py
preview: ../case_seg136.png
---

**一句话**：火山图(框式标签)

**部件亮点**
- 结构布局：单面板
- 编码方式：粉色带黑边=显著点、灰=NS;竖虚线FC阈值、横虚线P阈值;关键基因大号深紫点+白底黑边斜体标签框

**复现**：配方 `scripts/recipes/case_seg136.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
