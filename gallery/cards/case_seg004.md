---
title: Nature 折线图
kind: 数据图
purpose: [趋势变化]
data: 4组×7时间点(0-35天)×体重变化%,每组10-15
input: long (reference/data-schemas.json #004)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg004.py
preview: ../case_seg004.png
---

**一句话**：分组折线图+内嵌柱形图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：展示 2-5 组在 0-35 天这类时间序列上的均值±SEM 变化趋势

**有什么用**：几条折线跟着时间走，看各组指标怎么升怎么降；实验中途的干预用虚线和灰底分成前后两段，顶部还把两段的'总变化量'缩成小条形图直接比出显著。

**部件亮点**
- 结构布局：主折线+顶部两个iAUC内嵌条形
- 编码方式：4组折线(蓝红青黄)空心圆点±SEM;20天黑虚线+右侧灰底区;内嵌条形带散点***;右侧显著性括号;图例顶部

**复现**：配方 `scripts/recipes/case_seg004.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
