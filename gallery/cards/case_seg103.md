---
title: Nature 填充型等高线图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 各组(P值,长度)点集+样本数
input: long (reference/data-schemas.json #103)
journal: Nature
recipe: scripts/recipes/case_seg103.py
preview: ../case_seg103.png
---

**一句话**：填充等高线small multiples（Nature 风格）

**部件亮点**
- 结构布局：上排4小面板+下方1大面板
- 编码方式：各面板单色系填充等高线(蓝/紫/红/绿),右上括号样本计数,x=-log10P y=Length,共享轴

**复现**：配方 `scripts/recipes/case_seg103.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
