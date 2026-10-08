---
title: Cell 上下双热图
kind: 数据图
purpose: [相关关系]
data: 60×60相关矩阵+p值+签名注释
input: matrix (reference/data-schemas.json #119)
journal: Cell
recipe: scripts/recipes/case_seg119.py
preview: ../case_seg119.png
---

**一句话**：点阵相关矩阵热图（Cell 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：60×60点阵:点色=Spearman(红白蓝,-1~1)、点径=显著性;对角深蓝;顶部类别色块;左侧分类色条;底部色标

**复现**：配方 `scripts/recipes/case_seg119.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
