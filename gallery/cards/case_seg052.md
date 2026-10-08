---
title: Science 样本地理分布图(二)
kind: 数据图
purpose: [空间分布]
data: 采样点经纬度+类别构成计数
input: long (reference/data-schemas.json #052)
journal: Science
recipe: scripts/recipes/case_seg052.py
preview: ../case_seg052.png
---

**一句话**：世界地图+采样饼图（Science 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：白陆地+浅蓝海洋;采样点叠饼图,饼分色=类别(玫红/黄绿/深棕),饼径∝样本数;左下同心圆图例

**复现**：配方 `scripts/recipes/case_seg052.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
