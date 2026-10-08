---
title: Nature 三元图(2)
kind: 数据图
purpose: [构成占比, 相关关系]
data: 三维状态得分+年龄组
input: long (reference/data-schemas.json #125)
journal: Nature
recipe: scripts/recipes/case_seg125.py
preview: ../case_seg125.png
---

**一句话**：三元散点图(两组)（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：灰色三角网格;红/绿/蓝点划参考线;三边彩箭头TH1/TH2/TH17;青色Young、棕橙Older带黑边

**复现**：配方 `scripts/recipes/case_seg125.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
