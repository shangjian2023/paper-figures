---
title: Plant Bio. J. 相关性矩阵图+拟合散点
kind: 数据图
purpose: [相关关系]
data: 4变量×约200样本成对值+年份
input: matrix (reference/data-schemas.json #075)
journal: Plant Bio. J.
recipe: scripts/recipes/case_seg075.py
preview: ../case_seg075.png
---

**一句话**：pairs图+拟合散点（Plant Bio. J. 风格）

**部件亮点**
- 结构布局：(a)4×4矩阵+(b)右列4散点
- 编码方式：对角直方图+密度线(红/绿/黄/紫);上三角色块注R²/P/ns;下三角灰点+红虚线拟合;b列彩色点带方程

**复现**：配方 `scripts/recipes/case_seg075.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
