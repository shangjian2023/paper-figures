---
title: Nature 差异云雨图(三)
kind: 数据图
purpose: [差异展示, 排序, 分布形态]
data: 两分期组×距离值,配对关系
input: long (reference/data-schemas.json #071)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg071.py
preview: ../case_seg071.png
---

**一句话**：水平云雨图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：两组配对观测（如同一批样本在两个分期/两种标记下的距离值），想画出每一对的变化方向和幅度

**有什么用**：同一批样本在两个分期各测一次，每个样本用一根连线跨在上下两行之间：黑线是显著变化、灰线是没变化，水平铺开的长尾分布一眼可见。

**部件亮点**
- 结构布局：上下两个水平面板
- 编码方式：水平半小提琴+箱线+抖动点;配对灰线连接(黑=P<0.05,灰=NS);注KS与Wilcoxon P;右侧图例

**复现**：配方 `scripts/recipes/case_seg071.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
