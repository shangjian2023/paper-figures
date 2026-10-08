---
title: Clin.Transl.Med Upset图(二)
kind: 数据图
purpose: [网络与流向]
data: 8组DEG交集矩阵
input: sets (reference/data-schemas.json #115)
journal: Clin.Transl.Med
recipe: scripts/recipes/case_seg115.py
preview: ../case_seg115.png
---

**一句话**：UpSet图（Clin.Transl.Med 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：交集条形计数330~4,点阵圆点连线8组,左侧setSize条;蓝/红条+行背景渐变+空心点阵

**复现**：配方 `scripts/recipes/case_seg115.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
