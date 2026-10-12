---
title: New Phytol. 相关性网络&散点矩阵
kind: 数据图
purpose: [网络与流向, 相关关系]
data: 6变量×约90观测+r/P矩阵
input: matrix (reference/data-schemas.json #076)
journal: New Phytol.
wow: 2
recipe: scripts/recipes/case_seg076.py
preview: ../case_seg076.png
---

**一句话**：相关网络+散点矩阵（New Phytol. 风格）

**高级感**：★★ 有设计感

**适用场景**：6-8 个变量间的 Pearson 相关网络：弧线颜色=正负相关、实虚线=是否显著，节点为变量名

**有什么用**：把几个性状两两连线成一张网络，线的颜色分正负、实虚分显著，旁边配上每对性状的散点，一眼看清哪些性状互相牵连、哪些各走各的。

**部件亮点**
- 结构布局：左网络+右上三角6×6散点
- 编码方式：对角盒节点,弧线蓝r≥0红r<0、实线P<0.05虚线NS;上三角散点黑拟合线;点色=4样地,形=叶型

**复现**：配方 `scripts/recipes/case_seg076.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
