---
title: iMeta 火山图+富集图(二)
kind: 数据图
purpose: [差异展示, 排序]
data: 蛋白log2FC/p;富集通路p+基因
input: long (reference/data-schemas.json #112)
journal: iMeta
wow: 2
recipe: scripts/recipes/case_seg112.py
preview: ../case_seg112.png
---

**一句话**：火山+富集条形（iMeta 风格）

**高级感**：★★ 有设计感

**适用场景**：单一比较（如 Young vs Aged）的蛋白/基因差异结果配富集分析：上画虚线阈值的火山图（深蓝下调/深红上调/灰不显著），下画上调、下调各前 5 条富集通路水平条形

**有什么用**：上面的火山图一眼看出哪些蛋白减少（蓝）、哪些增多（红）；下面两排条形分别列出减少和增多各自对应的功能通路，条形越长越可信，还注明了代表蛋白的名字。

**部件亮点**
- 结构布局：上1火山+下2水平条形
- 编码方式：火山虚线阈值,深蓝下调/深红上调/灰NS;条形紫/绯红两色,通路条+成员基因文本+色标

**复现**：配方 `scripts/recipes/case_seg112.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
