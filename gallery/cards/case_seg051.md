---
title: Nature 样本地理分布图(一)
kind: 数据图
purpose: [空间分布]
data: 国家级数量+构成
input: long (reference/data-schemas.json #051)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg051.py
preview: ../case_seg051.png
---

**一句话**：世界地图+饼图（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：展示种质/样本/记录按原产国的数量分布：国家底色按数量深浅填色（choropleth），叠加饼图显示每国 2-4 类构成（如生态型冬性/半冬性/春性）

**有什么用**：世界地图按国家填深浅表示样本多少，主要国家再叠个小饼看类型构成，一眼看出资源集中在哪几国、各以什么类型为主。

**部件亮点**
- 结构布局：单面板
- 编码方式：国家choropleth按数量蓝白渐变,灰=无数据;叠饼图表示构成(蓝/绿/黄);左下饼径同心圆图例;用 helpers.geo.world_map

**复现**：配方 `scripts/recipes/case_seg051.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
