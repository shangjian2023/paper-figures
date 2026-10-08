---
title: Cell 环形热图
kind: 数据图
purpose: [网络与流向]
data: 基因×5样本矩阵+通路分组;交集矩阵
input: matrix (reference/data-schemas.json #133)
journal: Cell
recipe: scripts/recipes/case_seg133.py
preview: ../case_seg133.png
---

**一句话**：环形热图+UpSet内嵌（Cell 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：外圈6扇区弧形热图,蓝白红(-2~2)色标;基因名放射;扇区间留白+弧形通路名;中心UpSet交集柱+点阵

**复现**：配方 `scripts/recipes/case_seg133.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
