---
title: Nature 截断+分组柱形图
kind: 数据图
purpose: [组间比较]
data: 2处理×3基因型×6-8重复
input: long (reference/data-schemas.json #007)
journal: Nature
recipe: scripts/recipes/case_seg007.py
preview: ../case_seg007.png
---

**一句话**：截断Y轴分组柱形图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：Y轴截断(0-2/1000-4000带断裂斜线);2条件×3基因型柱+散点±SEM;*与n.s.括号;图例左上;灰/橙/紫

**复现**：配方 `scripts/recipes/case_seg007.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
