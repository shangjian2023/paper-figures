---
title: Nature 蜂群图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 行×单细胞logFC值
input: long (reference/data-schemas.json #084)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg084.py
preview: ../case_seg084.png
---

**一句话**：水平渐隐蜂群图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：约 20 个类别（细胞类型/组织）各有一批 logFC 值，想逐行横排展示正负两个方向的分布

**有什么用**：二十多种细胞各占一行，点偏左是早期更高、偏右是晚期更高，越靠近中线越淡，一眼看出哪类细胞在发育中此消彼长。

**部件亮点**
- 结构布局：单面板
- 编码方式：每行左红右紫蜂群+半小提琴,近0渐透明;0处竖虚线;左轴类型色条;底部双向箭头log(FC)

**复现**：配方 `scripts/recipes/case_seg084.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
