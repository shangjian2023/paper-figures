---
title: Nature 相关性矩阵(Python版)
kind: 数据图
purpose: [相关关系]
data: 同案例132
input: matrix (reference/data-schemas.json #131)
journal: Nature
recipe: scripts/recipes/case_seg131.py
preview: ../case_seg131.png
---

**一句话**：配对相关矩阵图(Python风格)（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：同R版布局但子图带刻度;jet色标右侧0.1-0.8;色块边框;下三角彩色密度散点

**复现**：配方 `scripts/recipes/case_seg131.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
