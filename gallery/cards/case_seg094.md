---
title: Nature 环状柱形图
kind: 数据图
purpose: [多指标综合]
data: 指标名,z值,星号,维度分类
input: long (reference/data-schemas.json #094)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg094.py
preview: ../case_seg094.png
---

**一句话**：环状柱形图(SD)（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：有约 40-80 个有序指标（问卷条目/量表/基因）的 z 分数或标准化偏差（约 ±1.5 SD），想在一圈环上纵览全部指标的轮廓

**有什么用**：几十项量表得分与常模的偏差围成一圈短柱：柱越长偏得越多，红高蓝低，星号表示统计显著，中心圆标出每段指标属于哪个方面，整体画像一圈看完。

**部件亮点**
- 结构布局：单面板
- 编码方式：约60指标径向柱,柱高=SD(-1.5~+1.5),红黄蓝渐变,星号显著性,中心圆分区注释,右上色条

**复现**：配方 `scripts/recipes/case_seg094.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
