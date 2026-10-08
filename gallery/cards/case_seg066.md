---
title: Nature 限制性立方样条(RCS)
kind: 数据图
purpose: [趋势变化]
data: 自变量,HR,95%CI,两个P值
input: long (reference/data-schemas.json #066)
journal: Nature
recipe: scripts/recipes/case_seg066.py
preview: ../case_seg066.png
---

**一句话**：RCS剂量风险曲线（Nature 风格）

**部件亮点**
- 结构布局：2×2四面板,各含左上内嵌小图
- 编码方式：HR实线+同色CI带(绿/黄/粉/橙),HR=1黑虚线;内嵌Mortality曲线灰带;注Pnon-linear与Poverall

**复现**：配方 `scripts/recipes/case_seg066.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
