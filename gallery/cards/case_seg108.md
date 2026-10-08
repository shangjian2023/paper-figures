---
title: iMeta 多分组火山图(一)
kind: 数据图
purpose: [差异展示, 排序]
data: 长表:蛋白,log2FC,score,组织
input: long (reference/data-schemas.json #108)
journal: iMeta
recipe: scripts/recipes/case_seg108.py
preview: ../case_seg108.png
---

**一句话**：多分组火山图（iMeta 风格）

**部件亮点**
- 结构布局：左1大图+右上18组织小图阵+下方放大
- 编码方式：蓝/粉底色标Down/Up区,分面彩色标题条,点色=组织,顶部Down/Up箭头

**复现**：配方 `scripts/recipes/case_seg108.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
