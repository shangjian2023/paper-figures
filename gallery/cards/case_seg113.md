---
title: Nature 火山图+富集图(三)
kind: 数据图
purpose: [差异展示, 排序]
data: 两组蛋白log2FC/p;富集FDR
input: long (reference/data-schemas.json #113)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg113.py
preview: ../case_seg113.png
---

**一句话**：火山+发散条形（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：两个比较（如 IE vs non-IE、NYHA IV vs II/III）各一张火山图，旁边配同色系的富集结果，组成 2×2 组合图

**有什么用**：左边两张火山图分别找出两组比较中升高和降低的蛋白，右边用朝右、朝左的条形列出对应的功能通路。两组比较并排摆，结论可以互相印证。

**部件亮点**
- 结构布局：2×2:2火山+2发散条形
- 编码方式：火山黄/绿、紫/淡紫标上下调+图例+基因标注;条形上调右bar下调左bar,x=-log10FDR

**复现**：配方 `scripts/recipes/case_seg113.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
