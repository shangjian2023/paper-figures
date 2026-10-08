---
title: Nature 带显著性的小提琴图(二)
kind: 数据图
purpose: [分布形态, 组间比较]
data: 长表:10亚群×2状态×百分比
input: long (reference/data-schemas.json #122)
journal: Nature
recipe: scripts/recipes/case_seg122.py
preview: ../case_seg122.png
---

**一句话**：双面板小提琴+星号（Nature 风格）

**部件亮点**
- 结构布局：上下两面板各10组×2小提琴
- 编码方式：***星号+括号;底部CD4/Treg/CD8分组横线;图例右上;内嵌散点

**复现**：配方 `scripts/recipes/case_seg122.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
