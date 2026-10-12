---
title: Nature 三元图(6)
kind: 数据图
purpose: [构成占比, 相关关系, 分布形态]
data: 三维概率向量
input: long (reference/data-schemas.json #129)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg129.py
preview: ../case_seg129.png
---

**一句话**：三元核密度图（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：每个细胞/样本有三维归一化概率向量（和为1），想看概率质量聚在哪里、有无亚群

**有什么用**：样本太多看不清单个点时，在三角形里画“密度云”：颜色越深代表点越扎堆，主团在中央、角落还有一小撮；适合看几百上千个样本整体聚在哪、有没有小亚群。

**部件亮点**
- 结构布局：单面板
- 编码方式：紫白渐变KDE等高线叠加灰细散点;三顶点0/1.0;三支彩色箭头;虚线中线;右上Probability色标

**复现**：配方 `scripts/recipes/case_seg129.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
