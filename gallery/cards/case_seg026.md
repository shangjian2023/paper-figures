---
title: Nature 分组散点图
kind: 数据图
purpose: [相关关系]
data: 5组×约50点(能量,寿命)+均值±SD
input: long (reference/data-schemas.json #026)
journal: Nature
recipe: scripts/recipes/case_seg026.py
preview: ../case_seg026.png
---

**一句话**：分组散点+均值误差菱形（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：5粒径组散点(深蓝/浅蓝/绿/黄/橙半透明)+黑菱形均值带XY误差棒;黑粗虚线theory;图例左上

**复现**：配方 `scripts/recipes/case_seg026.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
