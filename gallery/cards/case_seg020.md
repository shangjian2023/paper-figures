---
title: Nature 散点图(R 版本)
kind: 数据图
purpose: [相关关系]
data: 约5600点(总大小bp,CDS数,3组别)
input: long (reference/data-schemas.json #020)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg020.py
preview: ../case_seg020.png
---

**一句话**：散点图+边际直方图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：几千个点的两变量关系且跨多个数量级，需要 log-log 散点（如基因组大小 vs 预测 CDS 数）

**有什么用**：几千个点铺成一片云、配一条趋势线，一眼看出两个量同步变大；上方和右侧还各挂一张分布柱图，右下角小图交代偏差大小。

**部件亮点**
- 结构布局：主散点+上/右边际直方+右下内嵌箱线
- 编码方式：log-log散点3组(蓝/橙/灰)+红色虚线拟合;边际直方图带轮廓;右下残差箱线内嵌***;顶部图例

**复现**：配方 `scripts/recipes/case_seg020.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
