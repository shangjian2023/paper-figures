---
title: Nature 蜂群图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 行×细胞logFC,两套对比
input: long (reference/data-schemas.json #085)
journal: Nature
recipe: scripts/recipes/case_seg085.py
preview: ../case_seg085.png
---

**一句话**：配对面板蜂群图（Nature 风格）

**部件亮点**
- 结构布局：上下两节,每节左右双面板
- 编码方式：红/蓝/紫三组对比;25行细胞;0处黑粗虚线;左括号分Chondrogenic/Osteogenic

**复现**：配方 `scripts/recipes/case_seg085.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
