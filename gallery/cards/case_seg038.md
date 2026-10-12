---
title: Cognition 密度图&箱线/蜂群图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 每参数条件×被试recovered值+真值
input: long (reference/data-schemas.json #038)
journal: Cognition
wow: 2
recipe: scripts/recipes/case_seg038.py
preview: ../case_seg038.png
---

**一句话**：密度+箱线蜂群组合（Cognition 风格）

**高级感**：★★ 有设计感

**适用场景**：认知建模/参数恢复：3-4 个参数×4 个条件的网格，每格上半画该条件的参数分布 KDE 曲线并放红色方块标真值

**有什么用**：验证模型能不能从行为数据'猜回'真实参数：每格上半画数据的分布轮廓并标出红色真值方块，下半画模型猜出的结果（箱线加每个被试一个点），点云围住红方块就说明猜得准。

**部件亮点**
- 结构布局：上3×4参数×条件矩阵+下放大面板
- 编码方式：每格:顶部KDE曲线(灰/蓝/紫/橙)+红方块真值;底部粉红箱线+蜂群;下面板Empirical/Recovered对照

**复现**：配方 `scripts/recipes/case_seg038.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
