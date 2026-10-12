---
title: Science 样本地理分布图(二)
kind: 数据图
purpose: [空间分布]
data: 采样点经纬度+类别构成计数
input: long (reference/data-schemas.json #052)
journal: Science
wow: 3
recipe: scripts/recipes/case_seg052.py
preview: ../case_seg052.png
---

**一句话**：世界地图+采样饼图（Science 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：有多个具体采样点的经纬度（海域、群岛、全球站位），要在地图上每个站位叠一个饼图显示谱系/类群构成（2-4 类）

**有什么用**：在地图上每个采样点叠一个小饼：饼越大采的样本越多，颜色区分里面有几类，哪个海域采样密、构成像不像一眼可比。

**部件亮点**
- 结构布局：单面板
- 编码方式：白陆地+浅蓝海洋;采样点叠饼图,饼分色=类别(玫红/黄绿/深棕),饼径∝样本数;左下同心圆图例

**复现**：配方 `scripts/recipes/case_seg052.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
