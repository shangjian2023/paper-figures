---
title: Nature 差异云雨图(二)
kind: 数据图
purpose: [差异展示, 排序, 分布形态]
data: 两组×两状态概率值
input: long (reference/data-schemas.json #070)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg070.py
preview: ../case_seg070.png
---

**一句话**：分半小提琴云雨图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：两组（如 No AD vs AD）在两个条件下（如 MCI vs DE）的同一指标分布对比，一张图看全'条件×组'的交叉

**有什么用**：两种状态下各把两组的分布劈成左右两半贴在一起比，配箱线和撒开的原始点，顶部星号直接标出哪组差异显著。

**部件亮点**
- 结构布局：单面板
- 编码方式：背靠背半小提琴(淡紫/粉红)+箱线+抖动散点;**与****支架;图例左上;y=P_AD 0-1

**复现**：配方 `scripts/recipes/case_seg070.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
