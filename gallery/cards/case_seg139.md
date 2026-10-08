---
title: 普通条形图 vs Cell 内向环形图
kind: 数据图
purpose: [多指标综合]
data: 22组织×4亚型丰度矩阵(0~1)
input: long (reference/data-schemas.json #139)
journal: 未标注
recipe: scripts/recipes/case_seg139.py
preview: ../case_seg139.png
---

**一句话**：内向环形堆叠图(顶刊版)

**部件亮点**
- 结构布局：以顶刊版(内向环形图)为目标
- 编码方式：极坐标堆叠面积向圆心填充,扇区间留白,外圈灰色刻度环(0-0.8),放射组织标签+右图例22组织×4亚型

**复现**：配方 `scripts/recipes/case_seg139.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
