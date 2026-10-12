---
title: Clin.Transl.Med 多分组火山图(三)
kind: 数据图
purpose: [差异展示, 排序]
data: 长表:比较组,基因,log2FC,方向
input: long (reference/data-schemas.json #110)
journal: Clin.Transl.Med
wow: 2
recipe: scripts/recipes/case_seg110.py
preview: ../case_seg110.png
---

**一句话**：水平分带差异图（Clin.Transl.Med 风格）

**高级感**：★★ 有设计感

**适用场景**：有 5-8 个两两比较（如各 Stage vs Stage I、N+ vs N0、突变 vs 野生）的显著差异基因 log2FC，想一张图内上下并排对比各组谁升谁降

**有什么用**：每个横条代表一次两两比较：左边蓝点是降低的基因、右边红点是升高的基因，重点基因直接写名字。多条对比排在一起，谁升谁降、跨组是否一致一眼扫完。

**部件亮点**
- 结构布局：单面板
- 编码方式：8个比较组水平条带,中央log2FC轴-5~7.5,左青点Down右深红点Up,灰带分组背景,基因名标注

**复现**：配方 `scripts/recipes/case_seg110.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
