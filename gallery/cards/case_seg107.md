---
title: Cell 热图(二)
kind: 数据图
purpose: [相关关系]
data: TF×TF:active%,repressed%,p
input: matrix (reference/data-schemas.json #107)
journal: Cell
recipe: scripts/recipes/case_seg107.py
preview: ../case_seg107.png
---

**一句话**：三角分割热图（Cell 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：上三角%active黑红橙黄,下三角%repressed黑蓝绿,白色对角线,轴旋转基因名,右侧双色标,白点=显著

**复现**：配方 `scripts/recipes/case_seg107.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
