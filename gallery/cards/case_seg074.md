---
title: Nature 空转&组合图
kind: 数据图
purpose: [相关关系, 组间比较, 差异展示]
data: 行×(两条件值,表达占比矩阵,KS值)
input: long (reference/data-schemas.json #074)
journal: Nature
recipe: scripts/recipes/case_seg074.py
preview: ../case_seg074.png
---

**一句话**：哑铃+点阵+条形组合（Nature 风格）

**部件亮点**
- 结构布局：三联面板共享30余行
- 编码方式：左哑铃(WT黑/KO青圆连线);中点阵(色=表达量黄-红,大小=占比);右横条KS差异蓝/橙/灰;底部四组图例

**复现**：配方 `scripts/recipes/case_seg074.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
