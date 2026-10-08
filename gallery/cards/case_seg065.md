---
title: Nature 平滑曲线图(三)
kind: 数据图
purpose: [趋势变化]
data: 两组浓度-响应各8-9点
input: long (reference/data-schemas.json #065)
journal: Nature
recipe: scripts/recipes/case_seg065.py
preview: ../case_seg065.png
---

**一句话**：剂量-响应曲线（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：x对数10^-9~10^-4;橙圆与蓝方两组Sigmoid拟合;图例左上含KD标注

**复现**：配方 `scripts/recipes/case_seg065.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
