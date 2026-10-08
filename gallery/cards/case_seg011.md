---
title: Nature 气泡热图
kind: 数据图
purpose: [相关关系]
data: 26基因×14细胞×(平均表达,表达比例)
input: matrix (reference/data-schemas.json #011)
journal: Nature
recipe: scripts/recipes/case_seg011.py
preview: ../case_seg011.png
---

**一句话**：气泡热图(点阵热图)（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：26基因×14细胞类型:点径=表达核比例,绿色深浅=平均表达;左侧分组灰条;右侧色条+尺寸图例

**复现**：配方 `scripts/recipes/case_seg011.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
