---
title: Clin.Transl.Med 多分组火山图(三)
kind: 数据图
purpose: [差异展示, 排序]
data: 长表:比较组,基因,log2FC,方向
input: long (reference/data-schemas.json #110)
journal: Clin.Transl.Med
recipe: scripts/recipes/case_seg110.py
preview: ../case_seg110.png
---

**一句话**：水平分带差异图（Clin.Transl.Med 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：8个比较组水平条带,中央log2FC轴-5~7.5,左青点Down右深红点Up,灰带分组背景,基因名标注

**复现**：配方 `scripts/recipes/case_seg110.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
