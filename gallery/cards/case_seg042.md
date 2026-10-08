---
title: Nature 柱状图
kind: 数据图
purpose: [组间比较]
data: 5组×3-4重复qPCR+P值
input: long (reference/data-schemas.json #042)
journal: Nature
recipe: scripts/recipes/case_seg042.py
preview: ../case_seg042.png
---

**一句话**：柱状图+误差棒+散点（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：5柱,y=相对表达量0-3;灰/白/棕/白/绿填充(含斜线纹理);mean±SEM+样本圆点;星号显著性;x标签45°

**复现**：配方 `scripts/recipes/case_seg042.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
