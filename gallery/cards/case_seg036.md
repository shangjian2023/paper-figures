---
title: Nature FC-FC
kind: 数据图
purpose: [组间比较, 差异展示]
data: 两列log2FC+显著性+基因名
input: long (reference/data-schemas.json #036)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg036.py
preview: ../case_seg036.png
---

**一句话**：FC-FC散点图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：同一批基因在两个条件（如两种药物剂量、两种表型）下各有一列 log2FC，想画双 FC 散点看响应是否一致

**有什么用**：把同一批基因在两种条件下的变化量画成一张散点图：右上角共同升高、左下角共同降低、对角线附近步调一致，红蓝着色并标出关键基因的名字。想比较两份差异清单是否同向变化时用它。

**部件亮点**
- 结构布局：单面板
- 编码方式：双log2FC轴,过原点十字线+灰色对角虚线;红=up(both)粉=up(one)蓝=down(both)浅蓝=down(one)空心=NS;关键基因斜体引线标注;角落标签框

**复现**：配方 `scripts/recipes/case_seg036.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
