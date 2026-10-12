---
title: Nature 分组柱形图
kind: 数据图
purpose: [组间比较]
data: 7个变体×4处理×3重复,倍数变化
input: long (reference/data-schemas.json #008)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg008.py
preview: ../case_seg008.png
---

**一句话**：分组柱形图+P值标签（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：展示 5-8 个变体/构建体在 3-4 种处理剂量下的倍数变化（fold change）

**有什么用**：一排排变体并排比，各自画出在几种药物剂量下相对基准的变化倍数；虚线是'没变化'的基准，柱子高出它就是被诱导起来，柱上还写着精确 P 值。

**部件亮点**
- 结构布局：单面板
- 编码方式：7变体×4条件柱(深灰/浅灰/蓝/橙),误差线+空心圆点;每柱竖排P值;FC=1黑虚线;顶部横排图例框

**复现**：配方 `scripts/recipes/case_seg008.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
