---
title: Nature 三元图(2)
kind: 数据图
purpose: [构成占比, 相关关系]
data: 三维状态得分+年龄组
input: long (reference/data-schemas.json #125)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg125.py
preview: ../case_seg125.png
---

**一句话**：三元散点图(两组)（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：三个状态得分（如 TH1/TH2/TH17）构成 + 两组样本（Young vs Older），一张三角图看两组分布重心是否偏移

**有什么用**：两个年龄组各按三种免疫状态的打分画进同一个三角形，青色是年轻组、金色是年长组；看两团点各往哪个角偏，就知道年长后免疫状态往哪边移。

**部件亮点**
- 结构布局：单面板
- 编码方式：灰色三角网格;红/绿/蓝点划参考线;三边彩箭头TH1/TH2/TH17;青色Young、棕橙Older带黑边

**复现**：配方 `scripts/recipes/case_seg125.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
