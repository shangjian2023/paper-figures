---
title: Nature 双Y轴图
kind: 数据图
purpose: [组间比较]
data: 20条目×(基因数,P值)
input: long (reference/data-schemas.json #010)
journal: Nature
recipe: scripts/recipes/case_seg010.py
preview: ../case_seg010.png
---

**一句话**：双Y轴柱线组合图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：20个GO条目:棕褐柱=基因数(顶标数值,左轴)+绿色点虚线=-Log10P(右轴);X标签45°;顶部图例框;总标题

**复现**：配方 `scripts/recipes/case_seg010.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
