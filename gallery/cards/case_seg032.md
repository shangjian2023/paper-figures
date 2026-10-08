---
title: Nature 山脊图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 每行(genus)一组值+正负计数
input: long (reference/data-schemas.json #032)
journal: Nature
recipe: scripts/recipes/case_seg032.py
preview: ../case_seg032.png
---

**一句话**：山脊图+侧边条形图（Nature 风格）

**部件亮点**
- 结构布局：左山脊KDE+右正负双色条形
- 编码方式：各属一行,KDE填色按β1正负红/紫渐变;右侧条形深红/紫蓝双色对齐;共轴β1(MAG)

**复现**：配方 `scripts/recipes/case_seg032.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
