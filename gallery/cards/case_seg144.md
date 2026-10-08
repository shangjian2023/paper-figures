---
title: 森林图
kind: 数据图
purpose: [差异展示, 排序]
data: 疾病级β、95%CI、Padj+阈值
input: long (reference/data-schemas.json #144)
journal: 未标注
recipe: scripts/recipes/case_seg144.py
preview: ../case_seg144.png
---

**一句话**：森林图(背景色带)

**部件亮点**
- 结构布局：单面板
- 编码方式：方块+CI,方块色按β分级(红High/浅蓝Moderate/黑Low);背景蓝(0-0.4)/粉(0.4-0.8)竖带;水平虚线分疾病组;x -0.8~1.6

**复现**：配方 `scripts/recipes/case_seg144.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
