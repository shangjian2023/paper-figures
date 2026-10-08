---
title: UMAP (T 亚群)
kind: 数据图
purpose: [排序降维]
data: UMAP坐标+T亚群标签
input: xy (reference/data-schemas.json #141)
journal: 未标注
recipe: scripts/recipes/case_seg141.py
preview: ../case_seg141.png
---

**一句话**：UMAP标签框注释

**部件亮点**
- 结构布局：单面板
- 编码方式：淡彩半透明簇云;每簇中心彩色底标签框,文字与底色对比;无图例无网格;轴umap_1(-10~10)、umap_2

**复现**：配方 `scripts/recipes/case_seg141.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
