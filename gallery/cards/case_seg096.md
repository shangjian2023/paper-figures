---
title: Nature 相关性矩阵点图(一)
kind: 数据图
purpose: [相关关系]
data: 菌群×ARG:相关,p值,丰度
input: matrix (reference/data-schemas.json #096)
journal: Nature
recipe: scripts/recipes/case_seg096.py
preview: ../case_seg096.png
---

**一句话**：相关矩阵点图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：14行菌群×10列ARG:圆面积=丰度3档,填充红蓝=相关±0.8,*显著,列间竖分隔线,右侧双图例

**复现**：配方 `scripts/recipes/case_seg096.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
