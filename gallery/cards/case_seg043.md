---
title: Nature 密度图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 两组各数百(x,y)样本
input: long (reference/data-schemas.json #043)
journal: Nature
recipe: scripts/recipes/case_seg043.py
preview: ../case_seg043.png
---

**一句话**：联合密度+边际直方图（Nature 风格）

**部件亮点**
- 结构布局：中央二维密度+顶部/右侧边际直方
- 编码方式：GroupA蓝/GroupB红;中心多层半透明填充等高线;边际直方图描边同色;右上渐变色条;坐标30-80

**复现**：配方 `scripts/recipes/case_seg043.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
