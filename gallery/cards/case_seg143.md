---
title: 3D地图
kind: 数据图
purpose: [空间分布]
data: 子流域多边形+归一化降雨径流(4组)
input: matrix (reference/data-schemas.json #143)
journal: 未标注
recipe: scripts/recipes/case_seg143.py
preview: ../case_seg143.png
---

**一句话**：3D双层填充地图

**部件亮点**
- 结构布局：2×2四面板,右侧两条竖色标
- 编码方式：3D盒轴:底层径流多边形黄橙红,上层降雨多边形蓝色悬空;底面经纬度115-120E/29-35N;竖轴Rainfall/Runoff

**复现**：配方 `scripts/recipes/case_seg143.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
