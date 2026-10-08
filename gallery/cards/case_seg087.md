---
title: Nature 一维变量的相关性热图
kind: 数据图
purpose: [相关关系]
data: 39×39相关矩阵+变量分组
input: matrix (reference/data-schemas.json #087)
journal: Nature
recipe: scripts/recipes/case_seg087.py
preview: ../case_seg087.png
---

**一句话**：下三角相关热图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：39变量全下三角;灰阶=正相关、红阶=负相关;变量名按4组着色(微生物紫/样地青/土地橙/流域蓝)

**复现**：配方 `scripts/recipes/case_seg087.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
