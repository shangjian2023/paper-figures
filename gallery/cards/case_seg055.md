---
title: Nature 网络条形图
kind: 数据图
purpose: [网络与流向]
data: 类别→条目两层,各权重
input: long (reference/data-schemas.json #055)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg055.py
preview: ../case_seg055.png
---

**一句话**：放射状网络条形图（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：两级结构数据：几个大类（如 10 个代谢通路）各自下辖几十个条目（基因/调控因子/项目），想一圈展示'大类→条目'的归属和每个条目的权重

**有什么用**：中心彩色圆点是大类，细线放射连到外圈一根根短条，条越长该条目权重越大，哪类条目多、哪根最突出，绕一圈看明白。

**部件亮点**
- 结构布局：单面板
- 编码方式：中心9彩色圆点=类别,细曲线放射连到外圈径向条形,条长∝权重、色同类别,外缘斜置标签

**复现**：配方 `scripts/recipes/case_seg055.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
