---
title: Nature 散点图(R 版本)
kind: 数据图
purpose: [相关关系]
data: 约5600点(总大小bp,CDS数,3组别)
input: long (reference/data-schemas.json #020)
journal: Nature
recipe: scripts/recipes/case_seg020.py
preview: ../case_seg020.png
---

**一句话**：散点图+边际直方图（Nature 风格）

**部件亮点**
- 结构布局：主散点+上/右边际直方+右下内嵌箱线
- 编码方式：log-log散点3组(蓝/橙/灰)+红色虚线拟合;边际直方图带轮廓;右下残差箱线内嵌***;顶部图例

**复现**：配方 `scripts/recipes/case_seg020.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
