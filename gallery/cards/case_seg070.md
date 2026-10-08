---
title: Nature 差异云雨图(二)
kind: 数据图
purpose: [差异展示, 排序, 分布形态]
data: 两组×两状态概率值
input: long (reference/data-schemas.json #070)
journal: Nature
recipe: scripts/recipes/case_seg070.py
preview: ../case_seg070.png
---

**一句话**：分半小提琴云雨图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：背靠背半小提琴(淡紫/粉红)+箱线+抖动散点;**与****支架;图例左上;y=P_AD 0-1

**复现**：配方 `scripts/recipes/case_seg070.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
