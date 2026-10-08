---
title: Nature 差异云雨图(一)
kind: 数据图
purpose: [差异展示, 排序, 分布形态]
data: 两组各数百值
input: long (reference/data-schemas.json #069)
journal: Nature
recipe: scripts/recipes/case_seg069.py
preview: ../case_seg069.png
---

**一句话**：云雨图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：两组:外侧半小提琴(紫/黄)+中间箱线+内侧点阵雨;顶部p<2.22e-16支架线

**复现**：配方 `scripts/recipes/case_seg069.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
