---
title: Nature 半圆形&小提琴图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 长表group,value;各组中位数
input: long (reference/data-schemas.json #092)
journal: Nature
recipe: scripts/recipes/case_seg092.py
preview: ../case_seg092.png
---

**一句话**：半圆极坐标小提琴图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：约12组小提琴沿180°弧排列,各色内嵌白色小箱线;径向轴0-4;外侧彩色类目标签+中位数标注

**复现**：配方 `scripts/recipes/case_seg092.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
