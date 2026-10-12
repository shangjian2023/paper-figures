---
title: Nature 蜂群图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 行×细胞logFC,两套对比
input: long (reference/data-schemas.json #085)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg085.py
preview: ../case_seg085.png
---

**一句话**：配对面板蜂群图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：约 25 行细胞群/类别各有 logFC 蜂群，需要同时呈现两套对比（如解剖轴×发育时期）

**有什么用**：几十类细胞分上下两节排开，每节左右两栏各是一次对比，看同一类细胞的点整体偏向哪边，一眼读出四组对比里谁升谁降。

**部件亮点**
- 结构布局：上下两节,每节左右双面板
- 编码方式：红/蓝/紫三组对比;25行细胞;0处黑粗虚线;左括号分Chondrogenic/Osteogenic

**复现**：配方 `scripts/recipes/case_seg085.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
