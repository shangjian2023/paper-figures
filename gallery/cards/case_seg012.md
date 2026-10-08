---
title: Nature 系统发育树圈图(一)
kind: 数据图
purpose: [空间分布]
data: 约60叶Newick树+每叶(测序类型,门,出现环)
input: newick (reference/data-schemas.json #012)
journal: Nature
recipe: scripts/recipes/case_seg012.py
preview: ../case_seg012.png
---

**一句话**：环形系统发育树+注释环（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：环形树枝按10门着色;外3环:Type(黑/橙/蓝)、Phylum色块、Occurrence绿白格;右侧3组图例含N计数

**复现**：配方 `scripts/recipes/case_seg012.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
