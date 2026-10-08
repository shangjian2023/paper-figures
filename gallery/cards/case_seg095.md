---
title: Nature 环状折线图
kind: 数据图
purpose: [多指标综合, 趋势变化]
data: 指标×4组z-score长表
input: long (reference/data-schemas.json #095)
journal: Nature
recipe: scripts/recipes/case_seg095.py
preview: ../case_seg095.png
---

**一句话**：环状折线图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：4组线(蓝/橙/黄/粉)带圆点标记沿60指标环形排布,径向±1.5刻度,中心圆分区注释

**复现**：配方 `scripts/recipes/case_seg095.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
