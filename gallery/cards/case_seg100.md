---
title: ES&T 环状条形图
kind: 数据图
purpose: [多指标综合]
data: 城市名+CPUG值两列
input: long (reference/data-schemas.json #100)
journal: ES&T
recipe: scripts/recipes/case_seg100.py
preview: ../case_seg100.png
---

**一句话**：环状条形图(渐变)（ES&T 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：约70城市环形柱,正值蓝/负值红黄按值渐变,中心竖直色条,右侧径向刻度线,标签旋转外侧

**复现**：配方 `scripts/recipes/case_seg100.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
