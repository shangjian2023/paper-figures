---
title: Nature 动态交互桑基图(二)
kind: 数据图
purpose: [网络与流向]
data: 链表:年份段→谱系→国家→省
input: edges (reference/data-schemas.json #046)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg046.py
preview: ../case_seg046.png
---

**一句话**：四层桑基图（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：追溯样本/病例的层级归属链：时间段 → 谱系 → 国家 → 省份这类 3-4 层传递

**有什么用**：样本从年份段到谱系再到国家、省份层层分流，每段标着百分比，顺着彩带就能看清哪条谱系占大头、最后集中在哪个省。

**部件亮点**
- 结构布局：单面板
- 编码方式：层1年份段(彩块+百分比),层2谱系,层3国家,层4省;标签'名(百分比)';小流量浅灰;用 helpers.sankey.sankey

**复现**：配方 `scripts/recipes/case_seg046.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
