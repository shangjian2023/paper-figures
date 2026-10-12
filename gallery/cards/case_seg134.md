---
title: Cell umap图
kind: 数据图
purpose: [排序降维]
data: UMAP二维坐标+三列注释
input: xy (reference/data-schemas.json #134)
journal: Cell
wow: 3
recipe: scripts/recipes/case_seg134.py
preview: ../case_seg134.png
---

**一句话**：UMAP+环形注释（Cell 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：单细胞 UMAP/tSNE 散点按 10-15 种细胞类型着色，还要在外圈标注每簇的 timepoint/condition 构成

**有什么用**：单细胞降维散点图：每个点是一个细胞、颜色标细胞类型，外圈三层弧形环再交代每群细胞主要来自哪个时间点和处理组；想一图看清“有哪些细胞、各来自哪里”时用它。

**部件亮点**
- 结构布局：单面板
- 编码方式：散点按13细胞类型着色;外圈三层弧形注释环(Celltype/Timepoint/Condition)分段着色+类名;右侧三块图例

**复现**：配方 `scripts/recipes/case_seg134.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
