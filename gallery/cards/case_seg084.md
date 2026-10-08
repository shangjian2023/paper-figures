---
title: Nature 蜂群图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 行×单细胞logFC值
input: long (reference/data-schemas.json #084)
journal: Nature
recipe: scripts/recipes/case_seg084.py
preview: ../case_seg084.png
---

**一句话**：水平渐隐蜂群图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：每行左红右紫蜂群+半小提琴,近0渐透明;0处竖虚线;左轴类型色条;底部双向箭头log(FC)

**复现**：配方 `scripts/recipes/case_seg084.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
