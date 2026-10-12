---
title: UMAP (T 亚群)
kind: 数据图
purpose: [排序降维]
data: UMAP坐标+T亚群标签
input: xy (reference/data-schemas.json #141)
journal: 未标注
wow: 2
recipe: scripts/recipes/case_seg141.py
preview: ../case_seg141.png
---

**一句话**：UMAP标签框注释

**高级感**：★★ 有设计感

**适用场景**：画免疫/肿瘤微环境细胞亚群的 UMAP 单面板：每个亚群一团淡彩半透明云，亚群名用彩底标签框标在簇心，不要图例

**有什么用**：把细胞按相似程度排成点云、相近的抱成一簇，每簇用彩底名牌直接写出细胞名称；看肿瘤免疫构成、想让读者不查图例就认出每个簇时用它。

**部件亮点**
- 结构布局：单面板
- 编码方式：淡彩半透明簇云;每簇中心彩色底标签框,文字与底色对比;无图例无网格;轴umap_1(-10~10)、umap_2

**复现**：配方 `scripts/recipes/case_seg141.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
