---
title: Nature 多边形雷达图
kind: 数据图
purpose: [空间分布, 多指标综合]
data: 10山脉×6属性+坐标
input: long (reference/data-schemas.json #059)
journal: Nature
recipe: scripts/recipes/case_seg059.py
preview: ../case_seg059.png
---

**一句话**：地图+雷达内嵌（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：浅灰世界地图为底,10个山脉位置各嵌小雷达+引线标签;每雷达6轴按山脉配色;顶点标数值

**复现**：配方 `scripts/recipes/case_seg059.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
