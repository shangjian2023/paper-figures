---
title: 双曲线火山图
kind: 数据图
purpose: [差异展示, 排序, 趋势变化]
data: 基因:效应值+p值+重点名单
input: long (reference/data-schemas.json #135)
journal: 未标注
recipe: scripts/recipes/case_seg135.py
preview: ../case_seg135.png
---

**一句话**：双曲线边界火山图

**部件亮点**
- 结构布局：单面板
- 编码方式：黑色虚线双曲线为显著性边界;非显著黑点居中;左侧浅蓝、右侧浅紫基因集;重点基因深蓝/橙/绿/紫大点+斜体标签

**复现**：配方 `scripts/recipes/case_seg135.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
