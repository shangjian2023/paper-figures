---
title: Nature 折线图与柱形图
kind: 数据图
purpose: [趋势变化]
data: 2组×11周体重曲线+2体成分指标
input: long (reference/data-schemas.json #024)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg024.py
preview: ../case_seg024.png
---

**一句话**：折线+柱形双面板（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：两组（对照 vs 敲除/处理）8-12 周体重或指标曲线 ±SEM，逐时间点在点上方标 P 值

**有什么用**：左图画两条随时间上升的线（黑白对比），在时间点上标出两组差异是否显著；右图换成柱子比终点的脂肪与瘦肉量，散点是个体数据。

**部件亮点**
- 结构布局：左右两面板
- 编码方式：左:双组折线(黑圆/红方)±SEM,点上方竖排P值;右:Fat/Lean柱+散点,显著性线;图例左上

**复现**：配方 `scripts/recipes/case_seg024.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
