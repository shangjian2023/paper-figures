---
title: Cell umap图
kind: 数据图
purpose: [排序降维]
data: UMAP二维坐标+三列注释
input: xy (reference/data-schemas.json #134)
journal: Cell
recipe: scripts/recipes/case_seg134.py
preview: ../case_seg134.png
---

**一句话**：UMAP+环形注释（Cell 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：散点按13细胞类型着色;外圈三层弧形注释环(Celltype/Timepoint/Condition)分段着色+类名;右侧三块图例

**复现**：配方 `scripts/recipes/case_seg134.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
