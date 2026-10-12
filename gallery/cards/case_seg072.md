---
title: Nature 堆积柱形图(一)
kind: 数据图
purpose: [构成占比]
data: 14列×3分数均值±SEM+显著性
input: long (reference/data-schemas.json #072)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg072.py
preview: ../case_seg072.png
---

**一句话**：百分比堆积柱形图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：展示各基因型/处理下 3-4 个组分的占比（合计100%），如同位素标记的 M+0/M+1/M+2 分数

**有什么用**：每根柱子都堆满百分之百，黑绿粉三段代表三种同位素标记形态，段上带误差棒、顶部星号比较组间差异，两种剂量并排各摆七种基因型。

**部件亮点**
- 结构布局：两机组×7基因型
- 编码方式：黑M+0/青M+1/粉M+2三段堆积至100%,段上黑误差棒;顶部****与ns支架;图例左侧;斜体斜排x标签

**复现**：配方 `scripts/recipes/case_seg072.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
