---
title: Nature 气泡热图
kind: 数据图
purpose: [相关关系]
data: 26基因×14细胞×(平均表达,表达比例)
input: matrix (reference/data-schemas.json #011)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg011.py
preview: ../case_seg011.png
---

**一句话**：气泡热图(点阵热图)（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：单细胞/单核测序展示 20-40 个 marker 基因在 8-20 种细胞类型中的平均表达量（颜色深浅）和表达比例（点大小）

**有什么用**：一张格子矩阵：行是基因、列是细胞类型，点越大代表越多细胞用这个基因、颜色越深代表用量越高，哪类细胞偏爱哪些基因一眼扫出来。

**部件亮点**
- 结构布局：单面板
- 编码方式：26基因×14细胞类型:点径=表达核比例,绿色深浅=平均表达;左侧分组灰条;右侧色条+尺寸图例

**复现**：配方 `scripts/recipes/case_seg011.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
