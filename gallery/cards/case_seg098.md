---
title: iMeta 差异雷达图(一)
kind: 数据图
purpose: [差异展示, 排序, 多指标综合]
data: 组织×3指标比率矩阵
input: long (reference/data-schemas.json #098)
journal: iMeta
recipe: scripts/recipes/case_seg098.py
preview: ../case_seg098.png
---

**一句话**：雷达图(20轴)（iMeta 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：20条组织轴,3系列填充多边形+圆点(暗紫/暗红/橄榄绿),虚线30%参考圆,轴标签按组织着色

**复现**：配方 `scripts/recipes/case_seg098.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
