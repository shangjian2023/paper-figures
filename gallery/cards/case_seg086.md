---
title: Nature 拟合散点图
kind: 数据图
purpose: [相关关系]
data: 样地×(初始C,变化量,时长,干扰)
input: long (reference/data-schemas.json #086)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg086.py
preview: ../case_seg086.png
---

**一句话**：2×3拟合散点（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：按 3 个生态系统/大类分列成 2×3 面板：上排变化量对初始值的线性关系，下排对持续时间的衰减关系

**有什么用**：三类生态系统各占一列，上排看变化量与初始储量的直线关系，下排看随年限的衰减快慢，一眼看出哪个系统掉得最快、哪条规律更稳。

**部件亮点**
- 结构布局：2×3按三大生态系统分列
- 编码方式：上排变化量vs初始碳库:线性拟合、25%/75%虚线参考、R²/P注记;下排vs时长:指数衰减+CI带;点色=干扰类型

**复现**：配方 `scripts/recipes/case_seg086.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
