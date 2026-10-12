---
title: ES&T 环状条形图
kind: 数据图
purpose: [多指标综合]
data: 城市名+CPUG值两列
input: long (reference/data-schemas.json #100)
journal: ES&T
wow: 3
recipe: scripts/recipes/case_seg100.py
preview: ../case_seg100.png
---

**一句话**：环状条形图(渐变)（ES&T 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：约 40-80 个条目（城市/物种/位点/化合物）各有一个带正负的数值（增温幅度、z-score、log2FC），想一圈全览并正负分色

**有什么用**：几十个城市各占一小段圆弧，柱子伸得越长数值越大，正增长画蓝、负增长画红黄、颜色越深幅度越大，绕一圈就把排名和极端城市尽收眼底。

**部件亮点**
- 结构布局：单面板
- 编码方式：约70城市环形柱,正值蓝/负值红黄按值渐变,中心竖直色条,右侧径向刻度线,标签旋转外侧

**复现**：配方 `scripts/recipes/case_seg100.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
