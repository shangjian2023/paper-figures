---
title: Nature 相关性矩阵点图(二)
kind: 数据图
purpose: [相关关系]
data: 签名×CNV事件:rho,p值,两组
input: matrix (reference/data-schemas.json #097)
journal: Nature
recipe: scripts/recipes/case_seg097.py
preview: ../case_seg097.png
---

**一句话**：相关矩阵点图(双面板)（Nature 风格）

**部件亮点**
- 结构布局：WGD-low/WGD-high双面板
- 编码方式：圆大小=-log10P,色=Spearman ρ红蓝,圆内*号,6列CNV事件,行按模块分框,右侧双图例

**复现**：配方 `scripts/recipes/case_seg097.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
