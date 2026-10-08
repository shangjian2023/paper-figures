---
title: Nature 二维变量的相关性热图
kind: 数据图
purpose: [相关关系]
data: 相关矩阵+聚类树+行分组
input: matrix (reference/data-schemas.json #088)
journal: Nature
recipe: scripts/recipes/case_seg088.py
preview: ../case_seg088.png
---

**一句话**：聚类相关热图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：34×30行列树状图聚类;紫正绿负色标-0.5~0.5;行左侧组色条(上皮橙/间质黄/髓绿/内皮紫红/淋巴蓝)

**复现**：配方 `scripts/recipes/case_seg088.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
