---
title: iMeta 多分组火山图(一)
kind: 数据图
purpose: [差异展示, 排序]
data: 长表:蛋白,log2FC,score,组织
input: long (reference/data-schemas.json #108)
journal: iMeta
wow: 1
recipe: scripts/recipes/case_seg108.py
preview: ../case_seg108.png
---

**一句话**：多分组火山图（iMeta 风格）

**高级感**：★ 常规扎实

**适用场景**：蛋白/基因的 log2FC × 组织特异评分散点，按 FC 正负分成 Down/Up 两条背景色带（蓝/粉），点色=18 个组织来源

**有什么用**：左边大图把减少的蛋白和增加的蛋白分蓝、粉两半，每个点是一种蛋白、颜色代表来自哪个组织；右边和下方的小图再按组织逐个复看。想知道'变化都来自哪些组织'就用它。

**部件亮点**
- 结构布局：左1大图+右上18组织小图阵+下方放大
- 编码方式：蓝/粉底色标Down/Up区,分面彩色标题条,点色=组织,顶部Down/Up箭头

**复现**：配方 `scripts/recipes/case_seg108.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
