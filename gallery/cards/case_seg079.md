---
title: Nature 时间序列图(三)
kind: 数据图
purpose: [趋势变化]
data: 4脑区×时间比值均值±SEM
input: long (reference/data-schemas.json #079)
journal: Nature
recipe: scripts/recipes/case_seg079.py
preview: ../case_seg079.png
---

**一句话**：small-multiple时间序列（Nature 风格）

**部件亮点**
- 结构布局：上排4小面板+下方1大面板
- 编码方式：四脑区比值轨迹(紫/蓝/绿/红)+淡色SEM带;t=0阶跃;大图紫色放大重绘;线段式图例

**复现**：配方 `scripts/recipes/case_seg079.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
