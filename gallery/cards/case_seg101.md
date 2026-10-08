---
title: Nature 环状条形图
kind: 数据图
purpose: [多指标综合]
data: 靶点名+抑制值+panel两列
input: long (reference/data-schemas.json #101)
journal: Nature
recipe: scripts/recipes/case_seg101.py
preview: ../case_seg101.png
---

**一句话**：环状条形图(双系列)（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：双系列:青绿MTase面板+深红Safety面板各占半环;径向条长=抑制值;内弧彩字面板名;标签旋转

**复现**：配方 `scripts/recipes/case_seg101.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
