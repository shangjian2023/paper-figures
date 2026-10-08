---
title: Nature 圆形雷达图
kind: 数据图
purpose: [多指标综合]
data: 3组×8属性归一化得分
input: long (reference/data-schemas.json #057)
journal: Nature
recipe: scripts/recipes/case_seg057.py
preview: ../case_seg057.png
---

**一句话**：圆形雷达图(3组)（Nature 风格）

**部件亮点**
- 结构布局：三面板并排
- 编码方式：8轴圆环雷达,外圈浅蓝/灰弧带;多边形填充半透明(橙/蓝/绿)+描边+顶点点;轴标签外置

**复现**：配方 `scripts/recipes/case_seg057.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
