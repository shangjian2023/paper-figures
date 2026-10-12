---
title: Nature 限制性立方样条(RCS)
kind: 数据图
purpose: [趋势变化]
data: 自变量,HR,95%CI,两个P值
input: long (reference/data-schemas.json #066)
journal: Nature
wow: 2
recipe: scripts/recipes/case_seg066.py
preview: ../case_seg066.png
---

**一句话**：RCS剂量风险曲线（Nature 风格）

**高级感**：★★ 有设计感

**适用场景**：流行病学/临床队列：连续暴露变量（血细胞计数、CRP 等）与发病/死亡风险 HR 的非线性剂量-反应关系

**有什么用**：血液指标和患病风险不是直线关系：四张小图各画一条风险曲线，横轴是指标水平、纵轴是风险倍数，风险从哪个水平开始抬升、有没有拐点一眼看清。

**部件亮点**
- 结构布局：2×2四面板,各含左上内嵌小图
- 编码方式：HR实线+同色CI带(绿/黄/粉/橙),HR=1黑虚线;内嵌Mortality曲线灰带;注Pnon-linear与Poverall

**复现**：配方 `scripts/recipes/case_seg066.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
