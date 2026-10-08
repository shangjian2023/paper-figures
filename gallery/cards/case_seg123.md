---
title: Nature 带显著性的小提琴图(三)
kind: 数据图
purpose: [分布形态, 组间比较]
data: 长表:区域×事件×时期×百分比
input: long (reference/data-schemas.json #123)
journal: Nature
recipe: scripts/recipes/case_seg123.py
preview: ../case_seg123.png
---

**一句话**：叠加小提琴(实色+虚线轮廓)（Nature 风格）

**部件亮点**
- 结构布局：上下两面板各7事件×2时期
- 编码方式：实色小提琴+虚线轮廓小提琴叠加;实线=中位、虚线=四分位;红点划零线;灰/橙/绿/红/蓝/粉

**复现**：配方 `scripts/recipes/case_seg123.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
