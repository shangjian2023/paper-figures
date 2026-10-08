---
title: Nature 相关性热图
kind: 数据图
purpose: [相关关系]
data: 约90基因相关矩阵+模块归属
input: matrix (reference/data-schemas.json #023)
journal: Nature
recipe: scripts/recipes/case_seg023.py
preview: ../case_seg023.png
---

**一句话**：三角相关聚类热图（Nature 风格）

**部件亮点**
- 结构布局：下三角热图+顶部聚类树
- 编码方式：下三角红白蓝相关热图;顶部模块聚类树+灰底模块标签;基因名沿对角线放射;右下ρ色条

**复现**：配方 `scripts/recipes/case_seg023.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
