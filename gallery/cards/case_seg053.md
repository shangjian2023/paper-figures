---
title: Nature 样本地理分布图(三)
kind: 数据图
purpose: [空间分布]
data: 国家坐标+11亚型构成
input: long (reference/data-schemas.json #053)
journal: Nature
recipe: scripts/recipes/case_seg053.py
preview: ../case_seg053.png
---

**一句话**：世界地图+大饼图（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：米色陆地白海洋;各国叠大饼图,11类配色(玫红为主);饼径∝样本量同心圆图例1/10/100/1000;底部图例

**复现**：配方 `scripts/recipes/case_seg053.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
