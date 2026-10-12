---
title: Plant Bio. J. 相关性矩阵图+拟合散点
kind: 数据图
purpose: [相关关系]
data: 4变量×约200样本成对值+年份
input: matrix (reference/data-schemas.json #075)
journal: Plant Bio. J.
wow: 2
recipe: scripts/recipes/case_seg075.py
preview: ../case_seg075.png
---

**一句话**：pairs图+拟合散点（Plant Bio. J. 风格）

**高级感**：★★ 有设计感

**适用场景**：4-6 个连续变量两两关系的全景：对角分布直方图、上三角 R²/P 色块、下三角散点+拟合线

**有什么用**：把几个指标的分布和两两关系拼成一张矩阵：对角线是每个指标自己的分布，其余格子看两个指标怎么一起变化，一眼看出哪一对关系最强。

**部件亮点**
- 结构布局：(a)4×4矩阵+(b)右列4散点
- 编码方式：对角直方图+密度线(红/绿/黄/紫);上三角色块注R²/P/ns;下三角灰点+红虚线拟合;b列彩色点带方程

**复现**：配方 `scripts/recipes/case_seg075.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
