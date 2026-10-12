---
title: Nature FC-FC
kind: 数据图
purpose: [组间比较, 差异展示]
data: 每基因两log2FC;六类分类
input: long (reference/data-schemas.json #082)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg082.py
preview: ../case_seg082.png
---

**一句话**：对角带FC散点（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：比较两个 log2FC（如 total RNA vs polysome RNA），检验转录水平与翻译水平调控是否一致

**有什么用**：每个基因按两套测量各自的变化幅度定位置：落在中间斜带里的是两步同步变化，带外少数例外被箭头点名，一眼看出大多数同步、少数失控。

**部件亮点**
- 结构布局：单面板
- 编码方式：对角线±0.5平行带内着色(绿2317/深绿1633/红52/暗红151/蓝8);±0.5十字灰区;基因名红箭头标注

**复现**：配方 `scripts/recipes/case_seg082.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
