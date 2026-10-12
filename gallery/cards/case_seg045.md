---
title: Nature 动态交互桑基图(一)
kind: 数据图
purpose: [网络与流向]
data: 链表:源→中间→目标流量
input: edges (reference/data-schemas.json #045)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg045.py
preview: ../case_seg045.png
---

**一句话**：三层桑基图（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：展示'时间点/条件 → 中间枢纽 → 具体条目'的三层流量拆分，如 4 个锻炼时间点经 4 个核心基因分流到 21 个下游基因

**有什么用**：把'锻炼时间点→核心基因→下游基因'的流向画成彩色丝带，带子越宽量越大，一眼看出哪个时间点、哪条通路贡献最大。

**部件亮点**
- 结构布局：单面板
- 编码方式：左列4时间点节点(橙/浅蓝/红/绿),中层4基因节点,右列20基因末端小块;流带宽∝值,同色半透明;用 helpers.sankey.sankey

**复现**：配方 `scripts/recipes/case_seg045.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
