---
title: Nature 小提琴图&NMDS图
kind: 数据图
purpose: [分布形态, 组间比较, 排序降维]
data: 4组值;样本NMDS1/2坐标+分组
input: long (reference/data-schemas.json #083)
journal: Nature
recipe: scripts/recipes/case_seg083.py
preview: ../case_seg083.png
---

**一句话**：小提琴+NMDS散点（Nature 风格）

**部件亮点**
- 结构布局：A小提琴+B,C两个NMDS
- 编码方式：A对数轴4小提琴(黄/红/浅黄/暗红)白中位点;B/C散点+彩色半透明凸包;图例含n

**复现**：配方 `scripts/recipes/case_seg083.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
