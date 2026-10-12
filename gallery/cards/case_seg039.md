---
title: Cell 堆积柱形图
kind: 数据图
purpose: [构成占比]
data: 20簇×9类比例、×3水平比例、rate值
input: matrix (reference/data-schemas.json #039)
journal: Cell
wow: 2
recipe: scripts/recipes/case_seg039.py
preview: ../case_seg039.png
---

**一句话**：堆积柱+点图组合（Cell 风格）

**高级感**：★★ 有设计感

**适用场景**：十几个簇/类别（如 20 个 B 细胞簇）各占一行，想同时展示两套分类构成加一个连续指标

**有什么用**：每行一个细胞簇：左边两根百分比条分别展示两套分类的构成，右边一个黑点给出对应的连续数值，三栏逐行对齐。想回答'哪类以什么成分为主、数值是高还是低'这类构成加数值的问题时用它。

**部件亮点**
- 结构布局：两条100%堆积条+右列SHM散点,共享20行标签
- 编码方式：左条isotype 9色,右条SHM 3色;右面板黑点SHM rate带浅灰网格;图例右侧两组

**复现**：配方 `scripts/recipes/case_seg039.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
