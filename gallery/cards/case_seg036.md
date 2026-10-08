---
title: Nature FC-FC
kind: 数据图
purpose: [组间比较, 差异展示]
data: 两列log2FC+显著性+基因名
input: long (reference/data-schemas.json #036)
journal: Nature
recipe: scripts/recipes/case_seg036.py
preview: ../case_seg036.png
---

**一句话**：FC-FC散点图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：双log2FC轴,过原点十字线+灰色对角虚线;红=up(both)粉=up(one)蓝=down(both)浅蓝=down(one)空心=NS;关键基因斜体引线标注;角落标签框

**复现**：配方 `scripts/recipes/case_seg036.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
