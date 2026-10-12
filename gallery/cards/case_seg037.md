---
title: Science FC-FC
kind: 数据图
purpose: [组间比较, 差异展示]
data: 两列log2FC+基因名+显著性
input: long (reference/data-schemas.json #037)
journal: Science
wow: 1
recipe: scripts/recipes/case_seg037.py
preview: ../case_seg037.png
---

**一句话**：FC-FC散点图（Science 风格）

**高级感**：★ 常规扎实

**适用场景**：全转录组数万个基因做灰色小点背景，突出几百个显著基因的双 log2FC 对比（如 KRAS 敲低 vs ERKi 处理）

**有什么用**：几万个点铺成灰色的背景云，把真正重要的几百个基因用大红、大蓝的气泡顶出来：红的一起升高、蓝的一起降低、米色的两处方向不一致，点越大越显著。数据很大又想既保全貌又突出主角时用它。

**部件亮点**
- 结构布局：单面板
- 编码方式：双log2FC轴带灰参考线;数万黑点背景+红(up)/蓝(down)高亮,点径映射显著性;米白空心=中等显著;约40基因名引线斜体标注

**复现**：配方 `scripts/recipes/case_seg037.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
