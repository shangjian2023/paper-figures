---
title: Nat. Microbiol 中国地图(一)
kind: 数据图
purpose: [空间分布]
data: 省界+区划;样点:经纬度,数量,构成
input: long (reference/data-schemas.json #117)
journal: Nat. Microbiol
recipe: scripts/recipes/case_seg117.py
preview: ../case_seg117.png
---

**一句话**：中国地图+饼图（Nat. Microbiol 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：省填色=生态区划淡彩,采样点饼图大小=样本数、饼色=属,经纬网+指北针+双图例;用 helpers.geo.china_map

**复现**：配方 `scripts/recipes/case_seg117.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
