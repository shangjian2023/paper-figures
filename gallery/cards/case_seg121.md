---
title: cell 带显著性的小提琴图(一)
kind: 数据图
purpose: [分布形态, 组间比较]
data: 长表:7类×2区室×数值
input: long (reference/data-schemas.json #121)
journal: Cell
wow: 1
recipe: scripts/recipes/case_seg121.py
preview: ../case_seg121.png
---

**一句话**：成对小提琴+显著性（Cell 风格）

**高级感**：★ 常规扎实

**适用场景**：5-8 个组别（细胞类型/脑区/组织），每组比较同一二元条件下的连续变量分布（如 Active vs Repressive 区室）

**有什么用**：七类细胞每种并排画粉、蓝两把分布轮廓，白点标出中间水平：一眼看出每组都是蓝色偏高、而且七组的差距全都显著。

**部件亮点**
- 结构布局：单面板
- 编码方式：7组×2小提琴成对,顶部彩色组标签矩形,括号+P值,白点=中位数;粉=Active、深蓝=Repressive

**复现**：配方 `scripts/recipes/case_seg121.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
