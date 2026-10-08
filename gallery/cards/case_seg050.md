---
title: J.Hazard Mat. 环状柱形图(二)
kind: 数据图
purpose: [多指标综合]
data: 11指标×4处理均值+显著性字母
input: long (reference/data-schemas.json #050)
journal: J.Hazard Mater.
recipe: scripts/recipes/case_seg050.py
preview: ../case_seg050.png
---

**一句话**：环状分组柱形图（J.Hazard Mater. 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：11指标各占扇区,浅彩底+外弧彩条(黄/粉/绿/紫系);每扇区4根径向柱(深到浅蓝);柱端a-d字母;虚线刻度圈

**复现**：配方 `scripts/recipes/case_seg050.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
