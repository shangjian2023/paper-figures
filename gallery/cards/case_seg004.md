---
title: Nature 折线图
kind: 数据图
purpose: [趋势变化]
data: 4组×7时间点(0-35天)×体重变化%,每组10-15
input: long (reference/data-schemas.json #004)
journal: Nature
recipe: scripts/recipes/case_seg004.py
preview: ../case_seg004.png
---

**一句话**：分组折线图+内嵌柱形图（Nature 风格）

**部件亮点**
- 结构布局：主折线+顶部两个iAUC内嵌条形
- 编码方式：4组折线(蓝红青黄)空心圆点±SEM;20天黑虚线+右侧灰底区;内嵌条形带散点***;右侧显著性括号;图例顶部

**复现**：配方 `scripts/recipes/case_seg004.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
