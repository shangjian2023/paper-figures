---
title: Nature 双Y轴图
kind: 数据图
purpose: [组间比较]
data: 20条目×(基因数,P值)
input: long (reference/data-schemas.json #010)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg010.py
preview: ../case_seg010.png
---

**一句话**：双Y轴柱线组合图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：GO/KEGG 富集结果：20 条左右条目，柱子画基因数、折线画 -Log10 P 值

**有什么用**：每个功能条目一根柱子，柱子越高代表牵涉的基因越多；上面再连一条线，点越低说明结果越可靠。看'哪些功能最突出'的测序报告常用这张图。

**部件亮点**
- 结构布局：单面板
- 编码方式：20个GO条目:棕褐柱=基因数(顶标数值,左轴)+绿色点虚线=-Log10P(右轴);X标签45°;顶部图例框;总标题

**复现**：配方 `scripts/recipes/case_seg010.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
