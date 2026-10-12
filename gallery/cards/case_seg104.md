---
title: Nature 散点图
kind: 数据图
purpose: [组间比较, 差异展示]
data: 长表:细胞型,组别,MFI重复值
input: long (reference/data-schemas.json #104)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg104.py
preview: ../case_seg104.png
---

**一句话**：分组strip散点图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：8 个左右细胞型/类别（DC、cDC1、pDC…）×2-4 个处理组，每组 n≈5-15 的重复测量值（MFI、计数、强度），要展示全部原始点

**有什么用**：每种细胞占一列，每个样本是一个点：空心是对照、实心是处理后，一眼看出处理后哪些细胞被抬高、差异是否明显，黑色短横线是各组的平均水平。

**部件亮点**
- 结构布局：单面板
- 编码方式：8细胞型×4组:空心圆=mock、实心=PCV13,蓝/绿双色,虚线竖线分组隔,均值短横线,*显著性,图例右上

**复现**：配方 `scripts/recipes/case_seg104.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
