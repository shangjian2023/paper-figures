---
title: Nature 多维变量的相关性热图
kind: 数据图
purpose: [相关关系]
data: 10变量Pearson r/p;4群落Mantel r/p
input: matrix (reference/data-schemas.json #089)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg089.py
preview: ../case_seg089.png
---

**一句话**：Mantel相关组合热图（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：微生物组/生态数据：3-5 个群落（如原核、微生物、病毒类群）与 8-15 个环境因子做了 Mantel 检验，想把 Mantel r/p 和因子间 Pearson 相关画进同一张组合图

**有什么用**：左边几个群落的组成差异用连线牵到右侧环境因子表：线越粗关系越强，颜色标出是否显著；右侧格子深浅则显示各环境因子彼此间是否同涨同落。

**部件亮点**
- 结构布局：右上三角Pearson矩阵+左侧群落节点连边
- 编码方式：矩阵格青=正红=负带*/**/***;曲线连边=Mantel,线色=p三档、线宽=r三档;右侧3组图例

**复现**：配方 `scripts/recipes/case_seg089.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
