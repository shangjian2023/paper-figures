---
title: 上下双热图
kind: 数据图
purpose: [相关关系]
data: 两套57×57相关矩阵+签名名
input: matrix (reference/data-schemas.json #120)
journal: 未标注
recipe: scripts/recipes/case_seg120.py
preview: ../case_seg120.png
---

**一句话**：双色点阵相关矩阵

**部件亮点**
- 结构布局：单面板
- 编码方式：57×57点阵:上M1绿-白-红、下M0黄-白-紫双色标,点径=|r|,对角灰色,底部双色标

**复现**：配方 `scripts/recipes/case_seg120.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
