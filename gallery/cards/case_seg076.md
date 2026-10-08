---
title: New Phytol. 相关性网络&散点矩阵
kind: 数据图
purpose: [网络与流向, 相关关系]
data: 6变量×约90观测+r/P矩阵
input: edges (reference/data-schemas.json #076)
journal: New Phytol.
recipe: scripts/recipes/case_seg076.py
preview: ../case_seg076.png
---

**一句话**：相关网络+散点矩阵（New Phytol. 风格）

**部件亮点**
- 结构布局：左网络+右上三角6×6散点
- 编码方式：对角盒节点,弧线蓝r≥0红r<0、实线P<0.05虚线NS;上三角散点黑拟合线;点色=4样地,形=叶型

**复现**：配方 `scripts/recipes/case_seg076.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
