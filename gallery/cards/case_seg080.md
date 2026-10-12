---
title: Nature 时间序列图(四)
kind: 数据图
purpose: [趋势变化]
data: 两处理×时间ΔF/F均值+CI
input: long (reference/data-schemas.json #080)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg080.py
preview: ../case_seg080.png
---

**一句话**：事件对齐时间序列（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：比较两种处理/生理状态在事件前后的均值响应曲线，一条深下探、一条平缓，幅度差异大

**有什么用**：以事件发生为零点，把两种状态的平均响应画成两条带影子的曲线，灰色竖带标出事件时段，一眼看出一条深下探、一条平缓的幅度差别。

**部件亮点**
- 结构布局：单面板
- 编码方式：棕褐4weeks与紫Fasted均值线+置信带;0与10s两条灰虚线夹事件窗;图例右上;y=ΔF/F(%)

**复现**：配方 `scripts/recipes/case_seg080.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
