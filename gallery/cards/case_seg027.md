---
title: Nature 和弦图
kind: 数据图
purpose: [网络与流向]
data: 节点×节点流量方阵
input: edges (reference/data-schemas.json #027)
journal: Nature
recipe: scripts/recipes/case_seg027.py
preview: ../case_seg027.png
---

**一句话**：和弦图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：环形和弦:节点弧+贝塞尔带,带色=源节点;用 helpers.chord.chord_diagram

**复现**：配方 `scripts/recipes/case_seg027.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
