---
title: Nature 哑铃图
kind: 数据图
purpose: [组间比较, 差异展示]
data: 每行:期望区间、观察值、分类
input: long (reference/data-schemas.json #033)
journal: Nature
recipe: scripts/recipes/case_seg033.py
preview: ../case_seg033.png
---

**一句话**：哑铃图（Nature 风格）

**部件亮点**
- 结构布局：左堆叠比例条+右水平哑铃
- 编码方式：每科:灰色期望区间横杠+空心圆(Expected)与实心圆(Observed)连线;绿=高/灰=内/黄=低;左条三段青蓝渐变

**复现**：配方 `scripts/recipes/case_seg033.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
