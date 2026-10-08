---
title: Nature 相关性矩阵(R版)
kind: 数据图
purpose: [相关关系]
data: 7变量相关矩阵+变量对原始数据
input: matrix (reference/data-schemas.json #130)
journal: Nature
recipe: scripts/recipes/case_seg130.py
preview: ../case_seg130.png
---

**一句话**：配对相关矩阵图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：7×7:对角变量名+上三角色块按r值彩虹+标数值+下三角2D核密度散点;右侧竖色标

**复现**：配方 `scripts/recipes/case_seg130.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
