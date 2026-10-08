---
title: Nature 火山图+富集图(一)
kind: 数据图
purpose: [差异展示, 排序, 网络与流向]
data: 基因log2FC/FDR;通路-基因富集
input: long (reference/data-schemas.json #111)
journal: Nature
recipe: scripts/recipes/case_seg111.py
preview: ../case_seg111.png
---

**一句话**：火山+富集网络（Nature 风格）

**部件亮点**
- 结构布局：2×2:左列2火山,右列2网络
- 编码方式：火山红上/蓝下+基因名,x=-log10FDR含断轴;网络蓝红节点、灰边、椭圆功能群、大小=基因数色=FDR

**复现**：配方 `scripts/recipes/case_seg111.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
