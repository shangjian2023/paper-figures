---
title: Nature 通路富集circos&网络图
kind: 数据图
purpose: [网络与流向]
data: 基因列表;基因-GO归属;通路相似度矩阵
input: edges (reference/data-schemas.json #035)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg035.py
preview: ../case_seg035.png
---

**一句话**：circos弦图+富集网络（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：有几份基因/分子列表（如 alpha cells、beta cells、Islets），想用 circos 弦图展示列表间的共享基因

**有什么用**：左图把几份基因名单排成一圈，紫色丝带连接出现在多份名单里的基因，一眼看出谁和谁高度重合；右图按功能把富集通路归堆，每块饼显示基因来自哪份名单。想交代几组基因的共享与特异之处时用它。

**部件亮点**
- 结构布局：双面板:i circos弦图,j 富集网络
- 编码方式：circos外圈弧按细胞类型分色,基因沿弧排列,紫=共享基因弧连线;网络节点饼图+点径=P值+灰边

**复现**：配方 `scripts/recipes/case_seg035.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
