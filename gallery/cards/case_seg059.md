---
title: Nature 多边形雷达图
kind: 数据图
purpose: [空间分布, 多指标综合]
data: 10山脉×6属性+坐标
input: long (reference/data-schemas.json #059)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg059.py
preview: ../case_seg059.png
---

**一句话**：地图+雷达内嵌（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：有 4-12 个地点（山脉/站点/样地）各有经纬度坐标，想在地图对应位置原地展示每个地点的多指标画像

**有什么用**：把世界地图当底图，在十一座山脉的位置各嵌一个小雷达，六个角代表六项气候指标，哪里冷哪里干、各山差异一眼看清。

**部件亮点**
- 结构布局：单面板
- 编码方式：浅灰世界地图为底,10个山脉位置各嵌小雷达+引线标签;每雷达6轴按山脉配色;顶点标数值

**复现**：配方 `scripts/recipes/case_seg059.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
