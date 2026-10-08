---
title: Nature 三元图(3)
kind: 数据图
purpose: [构成占比, 相关关系]
data: 三维得分+年龄数值
input: long (reference/data-schemas.json #126)
journal: Nature
recipe: scripts/recipes/case_seg126.py
preview: ../case_seg126.png
---

**一句话**：三元散点(连续着色)（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：散点颜色=年龄蓝(40)→黄→红(90)渐变;右侧Age色标;灰三角网格+三色点划线+边箭头

**复现**：配方 `scripts/recipes/case_seg126.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
