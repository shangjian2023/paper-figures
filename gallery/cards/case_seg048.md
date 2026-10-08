---
title: Nature 环形图
kind: 数据图
purpose: [多指标综合]
data: 每参与者ID+三组指标+分类
input: long (reference/data-schemas.json #048)
journal: Nature
recipe: scripts/recipes/case_seg048.py
preview: ../case_seg048.png
---

**一句话**：多环参与者环形图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：约100参与者沿270°弧排布;内3环=三组指标着色弧段(红/黄/蓝系);外圈每参与者扇区+红/紫点;左嵌小面板

**复现**：配方 `scripts/recipes/case_seg048.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
