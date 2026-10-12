---
title: Nature 差异云雨图(一)
kind: 数据图
purpose: [差异展示, 排序, 分布形态]
data: 两组各数百值
input: long (reference/data-schemas.json #069)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg069.py
preview: ../case_seg069.png
---

**一句话**：云雨图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：比较两组（如病例 vs 对照）的连续变量分布，每组有上百个原始观测，要同时展示分布形状、中位数和原始数据点

**有什么用**：两组各几百个数据点同台比：分布轮廓、箱线中位数和每个原始点三层都摆出来，顶部再架一条显著性支架，谁高谁散、差多少一目了然。

**部件亮点**
- 结构布局：单面板
- 编码方式：两组:外侧半小提琴(紫/黄)+中间箱线+内侧点阵雨;顶部p<2.22e-16支架线

**复现**：配方 `scripts/recipes/case_seg069.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
