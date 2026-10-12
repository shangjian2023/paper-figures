---
title: Nature 山脊图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 每行(genus)一组值+正负计数
input: long (reference/data-schemas.json #032)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg032.py
preview: ../case_seg032.png
---

**一句话**：山脊图+侧边条形图（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：10-25 个类别（如菌属/基因/蛋白簇）各有一条数值分布，想叠成山脊图一行一个，看峰的位置和形状差异

**有什么用**：给十几个类别各画一条数据的分布轮廓，一行一层叠成山脊，红色代表偏正、紫色代表偏负，右侧再配一条对齐的样本量小条。类别多、又想同时看分布形状和正负方向时，用它最有气势。

**部件亮点**
- 结构布局：左山脊KDE+右正负双色条形
- 编码方式：各属一行,KDE填色按β1正负红/紫渐变;右侧条形深红/紫蓝双色对齐;共轴β1(MAG)

**复现**：配方 `scripts/recipes/case_seg032.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
