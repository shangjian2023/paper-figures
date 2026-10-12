---
title: Nature 相关性热图
kind: 数据图
purpose: [相关关系]
data: 47×47相关矩阵+丰度+类别标签
input: matrix (reference/data-schemas.json #022)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg022.py
preview: ../case_seg022.png
---

**一句话**：相关性点阵热图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：20-50 个代谢物/物种的两两相关矩阵，只画下三角避免信息重复

**有什么用**：一张三角形点阵：点越大代表两个指标关联越强，蓝色是一同升降、红色是一升一降；右侧再配条形图交代每种物质的含量高低。

**部件亮点**
- 结构布局：下三角点阵+右丰度条图+左说明
- 编码方式：下三角点阵:点径=|r|,蓝白红渐变;行名按5类着色;右侧紫/绿丰度条形图;45°列名

**复现**：配方 `scripts/recipes/case_seg022.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
