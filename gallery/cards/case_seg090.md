---
title: Cell 蝴蝶状&堆积柱形图
kind: 数据图
purpose: [构成占比]
data: 24行×7类占比+左右计数
input: long (reference/data-schemas.json #090)
journal: Cell
recipe: scripts/recipes/case_seg090.py
preview: ../case_seg090.png
---

**一句话**：镜像100%堆积条形图（Cell 风格）

**部件亮点**
- 结构布局：左右镜像×24行
- 编码方式：水平100%堆积镜像:灰No Signal/紫Off-target/橙Mixed/绿On-target;中央彩色类型名;两端计数;右侧图例

**复现**：配方 `scripts/recipes/case_seg090.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
