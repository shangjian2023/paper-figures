---
title: Nature 截断+分组柱形图
kind: 数据图
purpose: [组间比较]
data: 2处理×3基因型×6-8重复
input: long (reference/data-schemas.json #007)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg007.py
preview: ../case_seg007.png
---

**一句话**：截断Y轴分组柱形图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：2 种条件（对照 vs 诱导处理）×3 种基因型的表达量，对照接近 0 而处理组上千，量级悬殊

**有什么用**：对照组数值小得贴地、处理组却冲到上千，同一根轴画不下，就在中间'剪一刀'断开：小值和大值都看得清，柱子照样叠数据点、标显著性。

**部件亮点**
- 结构布局：单面板
- 编码方式：Y轴截断(0-2/1000-4000带断裂斜线);2条件×3基因型柱+散点±SEM;*与n.s.括号;图例左上;灰/橙/紫

**复现**：配方 `scripts/recipes/case_seg007.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
