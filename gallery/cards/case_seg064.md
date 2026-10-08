---
title: Nature 平滑曲线图(二)
kind: 数据图
purpose: [趋势变化]
data: 3组浓度-电导率各十余点
input: long (reference/data-schemas.json #064)
journal: Nature
recipe: scripts/recipes/case_seg064.py
preview: ../case_seg064.png
---

**一句话**：平滑曲线图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：3条平滑曲线+空心圆标记(深蓝/绿/红);峰下彩色光晕椭圆;图例右上

**复现**：配方 `scripts/recipes/case_seg064.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
