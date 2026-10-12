---
title: Nature 表格热图
kind: 数据图
purpose: [相关关系]
data: 20方法×数据集排名1-3+注释列
input: matrix (reference/data-schemas.json #031)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg031.py
preview: ../case_seg031.png
---

**一句话**：表格排名热图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：十到二十几个方法/模型在多个数据集和指标上的成绩，想做成一张按综合排名排序的'排行榜'大表

**有什么用**：把十到二十几个方法做成一张排行榜大表：一行一个方法、一列一项测试，格子颜色深浅表示成绩好坏，前三名直接写数字加框。挑方法或汇报评测结果时，扫一眼就知道谁最稳。

**部件亮点**
- 结构布局：单面板
- 编码方式：行=方法按Rank排序,列=数据集与指标;蓝/绿/橙按列着色;格子填排名数字;彩色表头胶囊;箭头渐变色条

**复现**：配方 `scripts/recipes/case_seg031.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
