---
title: Nature 时间序列图(四)
kind: 数据图
purpose: [趋势变化]
data: 两处理×时间ΔF/F均值+CI
input: long (reference/data-schemas.json #080)
journal: Nature
recipe: scripts/recipes/case_seg080.py
preview: ../case_seg080.png
---

**一句话**：事件对齐时间序列（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：棕褐4weeks与紫Fasted均值线+置信带;0与10s两条灰虚线夹事件窗;图例右上;y=ΔF/F(%)

**复现**：配方 `scripts/recipes/case_seg080.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
