---
title: Nature 系统发育树圈图(四)
kind: 数据图
purpose: [空间分布]
data: Newick树+叶(门,属,bsh有无,BBAA 0-0.6)
input: newick (reference/data-schemas.json #015)
journal: Nature
recipe: scripts/recipes/case_seg015.py
preview: ../case_seg015.png
---

**一句话**：环形发育树+双注释环（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：枝色=门,属名沿弧标注;外环1红渐变=BBAA比例,外环2蓝/白=bsh有无;属区填色

**复现**：配方 `scripts/recipes/case_seg015.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
