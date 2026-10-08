---
title: Nature 堆积柱形图(一)
kind: 数据图
purpose: [构成占比]
data: 14列×3分数均值±SEM+显著性
input: long (reference/data-schemas.json #072)
journal: Nature
recipe: scripts/recipes/case_seg072.py
preview: ../case_seg072.png
---

**一句话**：百分比堆积柱形图（Nature 风格）

**部件亮点**
- 结构布局：两机组×7基因型
- 编码方式：黑M+0/青M+1/粉M+2三段堆积至100%,段上黑误差棒;顶部****与ns支架;图例左侧;斜体斜排x标签

**复现**：配方 `scripts/recipes/case_seg072.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
