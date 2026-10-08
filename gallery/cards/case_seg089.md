---
title: Nature 多维变量的相关性热图
kind: 数据图
purpose: [相关关系]
data: 10变量Pearson r/p;4群落Mantel r/p
input: matrix (reference/data-schemas.json #089)
journal: Nature
recipe: scripts/recipes/case_seg089.py
preview: ../case_seg089.png
---

**一句话**：Mantel相关组合热图（Nature 风格）

**部件亮点**
- 结构布局：右上三角Pearson矩阵+左侧群落节点连边
- 编码方式：矩阵格青=正红=负带*/**/***;曲线连边=Mantel,线色=p三档、线宽=r三档;右侧3组图例

**复现**：配方 `scripts/recipes/case_seg089.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
