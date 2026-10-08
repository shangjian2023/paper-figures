---
title: Cell 相关性聚类热图
kind: 数据图
purpose: [相关关系]
data: 两套相关矩阵R+显著性+FC注释
input: matrix (reference/data-schemas.json #040)
journal: Cell
recipe: scripts/recipes/case_seg040.py
preview: ../case_seg040.png
---

**一句话**：双三角聚类相关热图（Cell 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：下三角(In-house)绿-白-紫,上三角(GSE)蓝-白-红;四周聚类树;关键簇红框;右侧4个图例

**复现**：配方 `scripts/recipes/case_seg040.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
