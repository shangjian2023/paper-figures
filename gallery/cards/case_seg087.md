---
title: Nature 一维变量的相关性热图
kind: 数据图
purpose: [相关关系]
data: 39×39相关矩阵+变量分组
input: matrix (reference/data-schemas.json #087)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg087.py
preview: ../case_seg087.png
---

**一句话**：下三角相关热图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：20-45 个变量的两两相关系数矩阵，只画下三角去重，一张图装下全部变量对

**有什么用**：几十个指标两两算相关铺成一张格子表：颜色越深关系越强、红是负灰是正，一眼锁定哪片指标抱团变化、哪片互不相干。

**部件亮点**
- 结构布局：单面板
- 编码方式：39变量全下三角;灰阶=正相关、红阶=负相关;变量名按4组着色(微生物紫/样地青/土地橙/流域蓝)

**复现**：配方 `scripts/recipes/case_seg087.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
