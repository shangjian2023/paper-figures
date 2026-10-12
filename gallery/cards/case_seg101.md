---
title: Nature 环状条形图
kind: 数据图
purpose: [多指标综合]
data: 靶点名+抑制值+panel两列
input: long (reference/data-schemas.json #101)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg101.py
preview: ../case_seg101.png
---

**一句话**：环状条形图(双系列)（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：两套独立的靶点/指标 panel（如药理靶点 panel + 安全性 panel）各约 30-50 项，想各占半环一图收拢

**有什么用**：两张筛选清单各占半环：青绿色是药理靶点、深红色是安全性靶点，柱子长短代表抑制强弱，最强的几项在环上自然冒尖，全部结果一图收拢。

**部件亮点**
- 结构布局：单面板
- 编码方式：双系列:青绿MTase面板+深红Safety面板各占半环;径向条长=抑制值;内弧彩字面板名;标签旋转

**复现**：配方 `scripts/recipes/case_seg101.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
