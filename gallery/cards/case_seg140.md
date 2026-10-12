---
title: 普通UMAP vs Cell 复现图
kind: 数据图
purpose: [排序降维]
data: UMAP坐标+12类标签
input: xy (reference/data-schemas.json #140)
journal: 未标注
wow: 2
recipe: scripts/recipes/case_seg140.py
preview: ../case_seg140.png
---

**一句话**：UMAP标签框注释(顶刊版)

**高级感**：★★ 有设计感

**适用场景**：已有 UMAP/t-SNE 坐标和约 12 个簇的细胞类型注释，想把类名直接用彩色圆角标签框标在簇中心，不要右侧图例

**有什么用**：把几千个细胞按相似程度排成点云，抱团处就是一类；每簇直接盖一个彩底名牌写明是什么细胞，不用来回查图例就能认出哪团是肿瘤细胞、哪团是免疫细胞。

**部件亮点**
- 结构布局：以复现版为目标
- 编码方式：淡彩半透明簇云;每簇中心彩色底标签框(白/黑字);无图例无网格;轴umap_1/2

**复现**：配方 `scripts/recipes/case_seg140.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
