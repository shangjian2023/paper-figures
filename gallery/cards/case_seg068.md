---
title: Cancer Cell 蝴蝶状&小提琴图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 11基因签名×M1/M2得分分布
input: long (reference/data-schemas.json #068)
journal: Cancer Cell
wow: 2
recipe: scripts/recipes/case_seg068.py
preview: ../case_seg068.png
---

**一句话**：镜像小提琴图（Cancer Cell 风格）

**高级感**：★★ 有设计感

**适用场景**：8-15 个基因签名/特征在两个对立打分方向（如 M1 vs M2、左右两种 module score）上的分布对比

**有什么用**：十来个基因签名各画一对背靠背的小提琴，左边朝 M1、右边朝 M2 展开，胖瘦是得分的分布轮廓，中间嵌小箱线看中位数，红虚线标出阈值。

**部件亮点**
- 结构布局：左右镜像,中间基因标签列
- 编码方式：镜像小提琴内嵌白箱线,0-1.5镜像轴;马卡龙多色;基因名按类着色;红虚线阈值

**复现**：配方 `scripts/recipes/case_seg068.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
