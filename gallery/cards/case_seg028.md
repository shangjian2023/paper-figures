---
title: Science 火山图
kind: 数据图
purpose: [差异展示, 排序]
data: 约5000基因(log2FC,adjP)+基因集
input: long (reference/data-schemas.json #028)
journal: Science
wow: 2
recipe: scripts/recipes/case_seg028.py
preview: ../case_seg028.png
---

**一句话**：火山图+基因集条纹带（Science 风格）

**高级感**：★★ 有设计感

**适用场景**：几千个基因的差异表达火山图：log2FC vs -log10 adjP，显著点橙色高亮、其余灰空心

**有什么用**：每个基因一个点：离中心越远变化越大，越靠上越可信；橙点是既明显又可信的，几个被点名的是主角；底部两排小竖线交代一组相关基因整体往哪边偏。

**部件亮点**
- 结构布局：主火山图+底部基因集条纹带
- 编码方式：灰空心点;左右Top200虚线框;橙点=显著;关键基因气泡标签;α=0.05虚线;底部UP/DN条纹+ES/pval

**复现**：配方 `scripts/recipes/case_seg028.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
