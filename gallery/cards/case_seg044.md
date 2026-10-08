---
title: Nature 散点图
kind: 数据图
purpose: [相关关系]
data: 每点:年龄,速度及误差,光谱类型
input: long (reference/data-schemas.json #044)
journal: Nature
recipe: scripts/recipes/case_seg044.py
preview: ../case_seg044.png
---

**一句话**：散点+直方图双面板（Nature 风格）

**部件亮点**
- 结构布局：上a直方图+核密度(双y轴),下b散点
- 编码方式：散点圆/方点、实/空区分,色按光谱型蓝-黄-红渐变灰=未知;x/y双向误差棒;黑虚线阈值;右侧光谱色条

**复现**：配方 `scripts/recipes/case_seg044.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
