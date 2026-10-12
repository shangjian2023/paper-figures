---
title: Nature 散点图(Python 版本)
kind: 数据图
purpose: [相关关系]
data: 约5600点(总大小bp,CDS数,3组别)
input: long (reference/data-schemas.json #021)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg021.py
preview: ../case_seg021.png
---

**一句话**：散点图+边际KDE（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：展示两个连续变量的相关，点数成百上千，用半透明叠色出密度感（如基因组大小 vs 基因数）

**有什么用**：几千个点叠成一片半透明点云，旁边用平滑轮廓勾出三组各自的分布；点云沿趋势线整体上升，右下角小图再比较各组的偏差。

**部件亮点**
- 结构布局：主散点+上/右边际KDE+右下内嵌箱线
- 编码方式：log-log散点(蓝/紫/黑半透明)+红虚线拟合;边际平滑KDE填充;灰虚参考线;右下残差箱线内嵌;图例左上

**复现**：配方 `scripts/recipes/case_seg021.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
