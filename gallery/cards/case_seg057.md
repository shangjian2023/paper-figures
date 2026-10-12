---
title: Nature 圆形雷达图
kind: 数据图
purpose: [多指标综合]
data: 3组×8属性归一化得分
input: long (reference/data-schemas.json #057)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg057.py
preview: ../case_seg057.png
---

**一句话**：圆形雷达图(3组)（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：2-3 组/条件各用 5-8 个相同属性（归一化 0-1 得分）画画像，一排三个圆环雷达并排，每组一色（橙/蓝/绿）

**有什么用**：三组各画一个圆形画像，八个属性各占一条轴：哪边鼓出来哪项就强，三个画像并排一摆，组间差异的形状立现。

**部件亮点**
- 结构布局：三面板并排
- 编码方式：8轴圆环雷达,外圈浅蓝/灰弧带;多边形填充半透明(橙/蓝/绿)+描边+顶点点;轴标签外置

**复现**：配方 `scripts/recipes/case_seg057.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
