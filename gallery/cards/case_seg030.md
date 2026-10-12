---
title: Cell 箱线图
kind: 数据图
purpose: [分布形态, 组间比较]
data: 4年龄类×2组×dN/dS值
input: long (reference/data-schemas.json #030)
journal: Cell
wow: 1
recipe: scripts/recipes/case_seg030.py
preview: ../case_seg030.png
---

**一句话**：分面箱线图（Cell 风格）

**高级感**：★ 常规扎实

**适用场景**：按年龄段/分期/等级等 3-8 个条件分面，每个分面内比较两组（如 Reference vs 特化组）的同一连续指标

**有什么用**：把数据按年龄段分成几个面板，每个面板里用一对箱线图比较两组数据的高低和波动，面板上方直接标出检验的 P 值。想说明'每个条件下都是同一组更低'这类一致结论时最省事。

**部件亮点**
- 结构布局：4个独立分面箱线
- 编码方式：灰 vs 彩色箱线;面板底色对应年龄渐变;含须线;顶部P值横线;彩色标题条;X标签斜排

**复现**：配方 `scripts/recipes/case_seg030.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
