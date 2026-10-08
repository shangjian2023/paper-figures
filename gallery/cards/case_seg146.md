---
title: 火山+条形图
kind: 数据图
purpose: [差异展示, 排序]
data: 基因log2FC与p;GO条目与基因
input: long (reference/data-schemas.json #146)
journal: 未标注
recipe: scripts/recipes/case_seg146.py
preview: ../case_seg146.png
---

**一句话**：火山+GO条形复合图

**部件亮点**
- 结构布局：上左粉/上右蓝横条形+下火山,背景呼应
- 编码方式：上条形:条长=-log10(p),GO名+代表基因,左粉右蓝;下火山:红显著/蓝未达FC/灰NS,虚线阈值,基因名引线

**复现**：配方 `scripts/recipes/case_seg146.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
