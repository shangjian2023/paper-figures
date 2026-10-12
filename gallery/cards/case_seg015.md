---
title: Nature 系统发育树圈图(四)
kind: 数据图
purpose: [空间分布]
data: Newick树+叶(门,属,bsh有无,BBAA 0-0.6)
input: newick (reference/data-schemas.json #015)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg015.py
preview: ../case_seg015.png
---

**一句话**：环形发育树+双注释环（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：进化树要按属/支系分块填浅色底，并把属名沿弧线排布标注

**有什么用**：一圈按'家族'分块上色的家谱树，属名直接沿弧线写在树上；外面绕两圈：一圈红格深浅表示某项比例的高低，一圈蓝白格子表示有没有目标基因。

**部件亮点**
- 结构布局：单面板
- 编码方式：枝色=门,属名沿弧标注;外环1红渐变=BBAA比例,外环2蓝/白=bsh有无;属区填色

**复现**：配方 `scripts/recipes/case_seg015.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
