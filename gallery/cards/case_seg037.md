---
title: Science FC-FC
kind: 数据图
purpose: [组间比较, 差异展示]
data: 两列log2FC+基因名+显著性
input: long (reference/data-schemas.json #037)
journal: Science
recipe: scripts/recipes/case_seg037.py
preview: ../case_seg037.png
---

**一句话**：FC-FC散点图（Science 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：双log2FC轴带灰参考线;数万黑点背景+红(up)/蓝(down)高亮,点径映射显著性;米白空心=中等显著;约40基因名引线斜体标注

**复现**：配方 `scripts/recipes/case_seg037.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
