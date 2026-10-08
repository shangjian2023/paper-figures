---
title: Nature 分组柱形图
kind: 数据图
purpose: [组间比较]
data: 7个变体×4处理×3重复,倍数变化
input: long (reference/data-schemas.json #008)
journal: Nature
recipe: scripts/recipes/case_seg008.py
preview: ../case_seg008.png
---

**一句话**：分组柱形图+P值标签（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：7变体×4条件柱(深灰/浅灰/蓝/橙),误差线+空心圆点;每柱竖排P值;FC=1黑虚线;顶部横排图例框

**复现**：配方 `scripts/recipes/case_seg008.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
