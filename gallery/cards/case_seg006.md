---
title: Nature 分组柱形图
kind: 数据图
purpose: [组间比较]
data: 4基因×3基因型×6-10次qPCR,以WT=1
input: long (reference/data-schemas.json #006)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg006.py
preview: ../case_seg006.png
---

**一句话**：分组柱形图+散点（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：展示 3-6 个基因在 2-4 种基因型/处理下的相对表达量（qPCR，以野生型=1 归一化）

**有什么用**：每个基因下并排几根柱子代表不同基因型，柱上叠出每次实验的测量点，还直接写出具体 P 值——哪个基因在突变体里升了降了，一眼看清。

**部件亮点**
- 结构布局：单面板
- 编码方式：4基因×3基因型(黑/橙/青)柱,叠空心圆散点,柱顶±SEM,竖排P值;右侧图例Day15;Y轴0-2.5

**复现**：配方 `scripts/recipes/case_seg006.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
