---
title: iMeta 火山图+富集图(二)
kind: 数据图
purpose: [差异展示, 排序]
data: 蛋白log2FC/p;富集通路p+基因
input: long (reference/data-schemas.json #112)
journal: iMeta
recipe: scripts/recipes/case_seg112.py
preview: ../case_seg112.png
---

**一句话**：火山+富集条形（iMeta 风格）

**部件亮点**
- 结构布局：上1火山+下2水平条形
- 编码方式：火山虚线阈值,深蓝下调/深红上调/灰NS;条形紫/绯红两色,通路条+成员基因文本+色标

**复现**：配方 `scripts/recipes/case_seg112.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
