---
title: Nature 填充型等高线图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 各组(P值,长度)点集+样本数
input: long (reference/data-schemas.json #103)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg103.py
preview: ../case_seg103.png
---

**一句话**：填充等高线small multiples（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：4 个左右分组（如不同蛋白亚类/处理条件）各有数千个 (x,y) 点，想比较各组的二维分布中心位置和形状差异

**有什么用**：把每一组的数据画成一幅'等高线地形图'：颜色越深的地方数据点越密，一眼看出各组的数值集中在哪里、范围有多宽。几组并排就能比较谁的分布更靠边、更分散。

**部件亮点**
- 结构布局：上排4小面板+下方1大面板
- 编码方式：各面板单色系填充等高线(蓝/紫/红/绿),右上括号样本计数,x=-log10P y=Length,共享轴

**复现**：配方 `scripts/recipes/case_seg103.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
