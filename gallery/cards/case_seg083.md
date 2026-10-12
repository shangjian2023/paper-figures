---
title: Nature 小提琴图&NMDS图
kind: 数据图
purpose: [分布形态, 组间比较, 排序降维]
data: 4组值;样本NMDS1/2坐标+分组
input: long (reference/data-schemas.json #083)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg083.py
preview: ../case_seg083.png
---

**一句话**：小提琴+NMDS散点（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：一张图同时给出 4 组某指标的分布（对数轴小提琴+白中位点）和组间显著性（ρ/P 支架）

**有什么用**：上面用轮廓比较四组数值的高低与波动，下面两张点图看样本是否按组各自聚堆，一眼同时证明总量不同、结构也不同。

**部件亮点**
- 结构布局：A小提琴+B,C两个NMDS
- 编码方式：A对数轴4小提琴(黄/红/浅黄/暗红)白中位点;B/C散点+彩色半透明凸包;图例含n

**复现**：配方 `scripts/recipes/case_seg083.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
