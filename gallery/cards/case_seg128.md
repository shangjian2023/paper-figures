---
title: Nature 三元图(5)
kind: 数据图
purpose: [构成占比, 相关关系]
data: 属级三处理丰度+分类
input: long (reference/data-schemas.json #128)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg128.py
preview: ../case_seg128.png
---

**一句话**：三元气泡图(属水平)（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：三个处理（Control/NPK/NPKM 这类）下各分类单元的相对丰度，想知道哪个属在哪种处理下占主导

**有什么用**：三种施肥处理各占三角形一个角，每个属按占比落点：彩色大气泡是关键优势属，还用箭头文字直接点名，灰色弱化背景，一眼看出哪个属在哪种处理下占主导。

**部件亮点**
- 结构布局：单面板
- 编码方式：顶点Control/NPK/NPKM 0-100;气泡=丰度,色=属(红/蓝/绿),灰=低丰度;黑箭头注释重点属

**复现**：配方 `scripts/recipes/case_seg128.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
