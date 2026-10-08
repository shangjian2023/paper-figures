---
title: Nature 相关性热图
kind: 数据图
purpose: [相关关系]
data: 47×47相关矩阵+丰度+类别标签
input: matrix (reference/data-schemas.json #022)
journal: Nature
recipe: scripts/recipes/case_seg022.py
preview: ../case_seg022.png
---

**一句话**：相关性点阵热图（Nature 风格）

**部件亮点**
- 结构布局：下三角点阵+右丰度条图+左说明
- 编码方式：下三角点阵:点径=|r|,蓝白红渐变;行名按5类着色;右侧紫/绿丰度条形图;45°列名

**复现**：配方 `scripts/recipes/case_seg022.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
