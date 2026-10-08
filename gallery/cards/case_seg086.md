---
title: Nature 拟合散点图
kind: 数据图
purpose: [相关关系]
data: 样地×(初始C,变化量,时长,干扰)
input: long (reference/data-schemas.json #086)
journal: Nature
recipe: scripts/recipes/case_seg086.py
preview: ../case_seg086.png
---

**一句话**：2×3拟合散点（Nature 风格）

**部件亮点**
- 结构布局：2×3按三大生态系统分列
- 编码方式：上排变化量vs初始碳库:线性拟合、25%/75%虚线参考、R²/P注记;下排vs时长:指数衰减+CI带;点色=干扰类型

**复现**：配方 `scripts/recipes/case_seg086.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
