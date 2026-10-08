---
title: Nature 散点图
kind: 数据图
purpose: [组间比较, 差异展示]
data: 长表:细胞型,组别,MFI重复值
input: long (reference/data-schemas.json #104)
journal: Nature
recipe: scripts/recipes/case_seg104.py
preview: ../case_seg104.png
---

**一句话**：分组strip散点图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：8细胞型×4组:空心圆=mock、实心=PCV13,蓝/绿双色,虚线竖线分组隔,均值短横线,*显著性,图例右上

**复现**：配方 `scripts/recipes/case_seg104.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
