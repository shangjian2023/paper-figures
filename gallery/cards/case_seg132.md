---
title: Nature 点线图
kind: 数据图
purpose: [趋势变化]
data: 16温度×频率扫描数值
input: long (reference/data-schemas.json #132)
journal: Nature
recipe: scripts/recipes/case_seg132.py
preview: ../case_seg132.png
---

**一句话**：点线图(普通vs顶刊对比)（Nature 风格）

**部件亮点**
- 结构布局：上下两面板对比
- 编码方式：上:线性x多彩曲线;下:log x,16条温度曲线52K-100K彩虹着色,空心/实心点+平滑线,右列图例

**复现**：配方 `scripts/recipes/case_seg132.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
