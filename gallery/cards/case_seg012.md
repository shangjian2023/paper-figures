---
title: Nature 系统发育树圈图(一)
kind: 数据图
purpose: [空间分布]
data: 约60叶Newick树+每叶(测序类型,门,出现环)
input: newick (reference/data-schemas.json #012)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg012.py
preview: ../case_seg012.png
---

**一句话**：环形系统发育树+注释环（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：有 50-150 个基因组/物种的 Newick 进化树，想按门/纲给树枝上色，再在外圈叠 2-3 层离散注释环

**有什么用**：把上百个物种的'家谱'画成一圈树枝，谁跟谁亲缘近一眼看出；外面再套几圈色环标出每个物种的类别和来源，一张图讲清整批基因组的关系。

**部件亮点**
- 结构布局：单面板
- 编码方式：环形树枝按10门着色;外3环:Type(黑/橙/蓝)、Phylum色块、Occurrence绿白格;右侧3组图例含N计数

**复现**：配方 `scripts/recipes/case_seg012.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
