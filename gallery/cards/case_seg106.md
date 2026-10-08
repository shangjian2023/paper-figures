---
title: Cell 热图(一)
kind: 数据图
purpose: [相关关系]
data: 状态×因子active/repressed%+显著性
input: matrix (reference/data-schemas.json #106)
journal: Cell
recipe: scripts/recipes/case_seg106.py
preview: ../case_seg106.png
---

**一句话**：多面板热图（Cell 风格）

**部件亮点**
- 结构布局：2行×3列+下方放大面板
- 编码方式：激活橙黑渐变、抑制蓝绿渐变,白点=显著,底部因子分类色条,右侧两色标

**复现**：配方 `scripts/recipes/case_seg106.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
