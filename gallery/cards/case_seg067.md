---
title: Nature 蝴蝶状&堆积条形图
kind: 数据图
purpose: [构成占比]
data: 9细胞态×(PFS,OS)×正负计数
input: long (reference/data-schemas.json #067)
journal: Nature
recipe: scripts/recipes/case_seg067.py
preview: ../case_seg067.png
---

**一句话**：镜像堆积条形图（Nature 风格）

**部件亮点**
- 结构布局：左右镜像,中央共享标签轴
- 编码方式：水平堆积镜像:蓝Protective+红Risk;x=癌种数10-0-10;红虚线框高亮首行;图例左下

**复现**：配方 `scripts/recipes/case_seg067.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
