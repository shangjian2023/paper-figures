---
title: Nature 样本地理分布图(一)
kind: 数据图
purpose: [空间分布]
data: 国家级数量+构成
input: long (reference/data-schemas.json #051)
journal: Nature
recipe: scripts/recipes/case_seg051.py
preview: ../case_seg051.png
---

**一句话**：世界地图+饼图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：国家choropleth按数量蓝白渐变,灰=无数据;叠饼图表示构成(蓝/绿/黄);左下饼径同心圆图例;用 helpers.geo.world_map

**复现**：配方 `scripts/recipes/case_seg051.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
