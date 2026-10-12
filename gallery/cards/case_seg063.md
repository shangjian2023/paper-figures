---
title: Nature 平滑曲线图(一)
kind: 数据图
purpose: [趋势变化]
data: 两组波长-强度各约300点
input: long (reference/data-schemas.json #063)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg063.py
preview: ../case_seg063.png
---

**一句话**：平滑曲线+散点（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：光谱/色谱/传感信号等密集连续数据（每组约上百点），想散点全展示+样条平滑线勾出峰形

**有什么用**：两组各上百个测量点全画成空心点、各配一条平滑曲线勾出峰形，两种条件的峰高差和峰位差一眼看清，适合光谱这类密集信号。

**部件亮点**
- 结构布局：单面板
- 编码方式：空心圆散点+样条平滑线:品红400 nN、青绿0 nN;双峰;图例左上线-圆符号;仅左下spine

**复现**：配方 `scripts/recipes/case_seg063.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
