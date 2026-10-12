---
title: Nature 差异雷达图(二)
kind: 数据图
purpose: [差异展示, 排序, 多指标综合]
data: 亚区×2组密度值+p值
input: long (reference/data-schemas.json #099)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg099.py
preview: ../case_seg099.png
---

**一句话**：雷达图(14轴)（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：在约 12-16 个亚区（脑区分层、皮层亚层、组织亚结构）上比较正好两组（如 D1 vs D2 细胞、两种处理）的密度或强度值

**有什么用**：两个细胞群在十四个脑区亚层上的密度各画一条线叠在一起，差异明显处打星号，外圈黑弧把细分层归并成几个大区，哪里多哪里少直接对比。

**部件亮点**
- 结构布局：单面板
- 编码方式：约14亚区轴,2系列(D1橙红/D2绿)线+点,径向400/800刻度,灰虚线环,*显著性,外圈黑弧分段标区名

**复现**：配方 `scripts/recipes/case_seg099.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
