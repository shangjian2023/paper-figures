---
title: Nature PCoA图
kind: 数据图
purpose: [分布形态, 组间比较, 排序降维]
data: 约1500样本×PCo1/PCo2,研究来源(6)×组别(2)
input: xy (reference/data-schemas.json #003)
journal: Nature
recipe: scripts/recipes/case_seg003.py
preview: ../case_seg003.png
---

**一句话**：PCoA散点+边缘箱线组合（Nature 风格）

**部件亮点**
- 结构布局：L形:主散点+右列2箱线+底部2横箱线
- 编码方式：圆=control三角=IBD,色按6个研究;右侧Study/Group箱线;底部横箱线;左上PERMANOVA p=0.001;轴PCo1[15.9%]/PCo2[10.2%]

**复现**：配方 `scripts/recipes/case_seg003.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
