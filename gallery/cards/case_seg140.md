---
title: 普通UMAP vs Cell 复现图
kind: 数据图
purpose: [排序降维]
data: UMAP坐标+12类标签
input: xy (reference/data-schemas.json #140)
journal: 未标注
recipe: scripts/recipes/case_seg140.py
preview: ../case_seg140.png
---

**一句话**：UMAP标签框注释(顶刊版)

**部件亮点**
- 结构布局：以复现版为目标
- 编码方式：淡彩半透明簇云;每簇中心彩色底标签框(白/黑字);无图例无网格;轴umap_1/2

**复现**：配方 `scripts/recipes/case_seg140.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
