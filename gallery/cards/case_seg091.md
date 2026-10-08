---
title: Cell 冲击图
kind: 数据图
purpose: [网络与流向]
data: 流向表source-target-count
input: edges (reference/data-schemas.json #091)
journal: Cell
recipe: scripts/recipes/case_seg091.py
preview: ../case_seg091.png
---

**一句话**：冲击图/桑基图（Cell 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：三列节点(Species→Specificity→Brightness),灰主流量+蓝高亮流,各流标n;用 helpers.sankey.sankey

**复现**：配方 `scripts/recipes/case_seg091.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
