---
title: Cancer Cell 拟合散点图
kind: 数据图
purpose: [相关关系]
data: 亚群×(分数x,指数y,类型色)
input: long (reference/data-schemas.json #061)
journal: Cancer Cell
recipe: scripts/recipes/case_seg061.py
preview: ../case_seg061.png
---

**一句话**：拟合散点图（Cancer Cell 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：彩色散点(Set3系)+黑回归线灰置信带;0处横竖虚线;轴两端彩色箭头注方向;标签带引线;右上r=0.64、P=8.6e-08

**复现**：配方 `scripts/recipes/case_seg061.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
