---
title: Nature 环状柱形图
kind: 数据图
purpose: [多指标综合]
data: 指标名,z值,星号,维度分类
input: long (reference/data-schemas.json #094)
journal: Nature
recipe: scripts/recipes/case_seg094.py
preview: ../case_seg094.png
---

**一句话**：环状柱形图(SD)（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：约60指标径向柱,柱高=SD(-1.5~+1.5),红黄蓝渐变,星号显著性,中心圆分区注释,右上色条

**复现**：配方 `scripts/recipes/case_seg094.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
