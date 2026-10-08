---
title: Nature 系统发育树圈图(二)
kind: 数据图
purpose: [空间分布]
data: Newick树+叶(门,丰度0-0.6,4环境有无)
input: newick (reference/data-schemas.json #013)
journal: Nature
recipe: scripts/recipes/case_seg013.py
preview: ../case_seg013.png
---

**一句话**：环形发育树+柱状/热图环（Nature 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：黑色环形树;扇形底色区分4环境;外侧红蓝柱状环;内层Presence灰白热图环;放射刻度0-0.6

**复现**：配方 `scripts/recipes/case_seg013.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
