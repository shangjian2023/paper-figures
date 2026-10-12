---
title: J.Hazard Mat. 环状柱形图(一)
kind: 数据图
purpose: [多指标综合]
data: 8性状×3处理均值+显著性字母
input: long (reference/data-schemas.json #049)
journal: J.Hazard Mater.
wow: 2
recipe: scripts/recipes/case_seg049.py
preview: ../case_seg049.png
---

**一句话**：环状分组柱形图（J.Hazard Mater. 风格）

**高级感**：★★ 有设计感

**适用场景**：6-10 个性状/指标各量纲不同，每个指标独占一个扇区用独立径向标尺，扇区内比较 2-4 个处理

**有什么用**：把八项根系指标绕成一圈，每个扇区里三根柱子是三种处理，柱端标 a/b/c 显著性字母，哪个处理强、差在哪项一目了然。

**部件亮点**
- 结构布局：单面板
- 编码方式：8性状各占扇区(淡彩底),每扇区3根径向柱(深蓝到浅蓝),柱端a/b/c字母;径向刻度;性状名沿外弧+彩弧条

**复现**：配方 `scripts/recipes/case_seg049.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
