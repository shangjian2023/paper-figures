---
title: Nature 表格热图
kind: 数据图
purpose: [相关关系]
data: 20方法×数据集排名1-3+注释列
input: matrix (reference/data-schemas.json #031)
journal: Nature
recipe: scripts/recipes/case_seg031.py
preview: ../case_seg031.png
---

**一句话**：表格排名热图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：行=方法按Rank排序,列=数据集与指标;蓝/绿/橙按列着色;格子填排名数字;彩色表头胶囊;箭头渐变色条

**复现**：配方 `scripts/recipes/case_seg031.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
