---
title: Nature 多边形雷达图
kind: 数据图
purpose: [多指标综合]
data: 两材料×5属性
input: long (reference/data-schemas.json #060)
journal: Nature
recipe: scripts/recipes/case_seg060.py
preview: ../case_seg060.png
---

**一句话**：五边形雷达对比（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：5轴=折射率/热导/硬度/杨氏模量/电阻;粉红大五边形 vs 蓝色小五边形;顶点白字数值;底部双行图例

**复现**：配方 `scripts/recipes/case_seg060.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
