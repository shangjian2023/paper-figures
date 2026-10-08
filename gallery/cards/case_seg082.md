---
title: Nature FC-FC
kind: 数据图
purpose: [组间比较, 差异展示]
data: 每基因两log2FC;六类分类
input: long (reference/data-schemas.json #082)
journal: Nature
recipe: scripts/recipes/case_seg082.py
preview: ../case_seg082.png
---

**一句话**：对角带FC散点（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：对角线±0.5平行带内着色(绿2317/深绿1633/红52/暗红151/蓝8);±0.5十字灰区;基因名红箭头标注

**复现**：配方 `scripts/recipes/case_seg082.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
