---
title: Nature 系统发育树圈图(二)
kind: 数据图
purpose: [空间分布]
data: Newick树+叶(门,丰度0-0.6,4环境有无)
input: newick (reference/data-schemas.json #013)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg013.py
preview: ../case_seg013.png
---

**一句话**：环形发育树+柱状/热图环（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：进化树上每个叶有一个 0-1 的连续量（如相对丰度 0-0.6），要画成外圈放射柱状环并用红/蓝分高低档

**有什么用**：还是一圈'家谱'树，树外再绕两圈：一圈柱子表示每个物种的多少（红高蓝低），一圈格子表示它在哪些环境里出现；背景扇形色块还分出不同栖息地的区段。

**部件亮点**
- 结构布局：单面板
- 编码方式：黑色环形树;扇形底色区分4环境;外侧红蓝柱状环;内层Presence灰白热图环;放射刻度0-0.6

**复现**：配方 `scripts/recipes/case_seg013.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
