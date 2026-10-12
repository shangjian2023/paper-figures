---
title: Nature 柱状图
kind: 数据图
purpose: [组间比较]
data: 5组×3-4重复qPCR+P值
input: long (reference/data-schemas.json #042)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg042.py
preview: ../case_seg042.png
---

**一句话**：柱状图+误差棒+散点（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：3-6 组处理的均值比较（如 qPCR 相对表达量、ELISA、蛋白定量），每组只有 3-5 个生物学重复

**有什么用**：最经典的柱子图：每种处理一根柱子，高度是平均值，上面小横杠是误差范围，旁边点缀每个样本的点，显著的加星号。实验每组只有几个重复、想直接比谁高谁低时用它。

**部件亮点**
- 结构布局：单面板
- 编码方式：5柱,y=相对表达量0-3;灰/白/棕/白/绿填充(含斜线纹理);mean±SEM+样本圆点;星号显著性;x标签45°

**复现**：配方 `scripts/recipes/case_seg042.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
