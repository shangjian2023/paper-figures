---
title: Cell 小提琴图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 3年龄类×2组×约1000值
input: long (reference/data-schemas.json #029)
journal: Cell
wow: 1
recipe: scripts/recipes/case_seg029.py
preview: ../case_seg029.png
---

**一句话**：分面小提琴图（Cell 风格）

**高级感**：★ 常规扎实

**适用场景**：按 2-4 个条件分面（如基因年龄档），每个面板比较参考组 vs 特化组的分布

**有什么用**：每个面板里两只“纺锤”各代表一组的分布轮廓，鼓包宽的地方样本扎堆，纺锤里的虚线标典型值；几块面板各对应一档条件，一眼看出哪组整体偏高。

**部件亮点**
- 结构布局：3个独立分面小提琴
- 编码方式：灰Reference vs 彩色Specialized(青/紫/红);内含中位数与四分位虚线;顶部彩色标签条;P值括号;面板底色渐变

**复现**：配方 `scripts/recipes/case_seg029.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
