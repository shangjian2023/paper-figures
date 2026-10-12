---
title: Nature 相关性矩阵(Python版)
kind: 数据图
purpose: [相关关系]
data: 同案例132
input: matrix (reference/data-schemas.json #131)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg131.py
preview: ../case_seg131.png
---

**一句话**：配对相关矩阵图(Python风格)（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：同 seg130 的 5-8 变量两两相关，但想要 Python/matplotlib 原生风格、每个密度子图自带坐标刻度

**有什么用**：同类相关全景图的另一版本：每个小格自带坐标刻度，变量量纲差别大也能逐格读出数据范围，配色更浓、对比更强。

**部件亮点**
- 结构布局：单面板
- 编码方式：同R版布局但子图带刻度;jet色标右侧0.1-0.8;色块边框;下三角彩色密度散点

**复现**：配方 `scripts/recipes/case_seg131.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
