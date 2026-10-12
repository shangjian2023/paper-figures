---
title: Cell 上下双热图
kind: 数据图
purpose: [相关关系]
data: 60×60相关矩阵+p值+签名注释
input: matrix (reference/data-schemas.json #119)
journal: Cell
wow: 2
recipe: scripts/recipes/case_seg119.py
preview: ../case_seg119.png
---

**一句话**：点阵相关矩阵热图（Cell 风格）

**高级感**：★★ 有设计感

**适用场景**：展示 30-80 个变量（基因签名/通路/指标）两两之间的 Spearman 或 Pearson 相关，矩阵大到方格里标不下数字

**有什么用**：把几十个指标两两之间的相关强弱画成一张大方格点阵：蓝点越深越正相关、红点越深越负相关，点越大越可信，同类指标抱成块，一眼看出哪些指标总是一起变化。

**部件亮点**
- 结构布局：单面板
- 编码方式：60×60点阵:点色=Spearman(红白蓝,-1~1)、点径=显著性;对角深蓝;顶部类别色块;左侧分类色条;底部色标

**复现**：配方 `scripts/recipes/case_seg119.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
