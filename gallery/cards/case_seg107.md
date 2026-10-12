---
title: Cell 热图(二)
kind: 数据图
purpose: [相关关系]
data: TF×TF:active%,repressed%,p
input: matrix (reference/data-schemas.json #107)
journal: Cell
wow: 2
recipe: scripts/recipes/case_seg107.py
preview: ../case_seg107.png
---

**一句话**：三角分割热图（Cell 风格）

**高级感**：★★ 有设计感

**适用场景**：同一对称方阵（TF×TF 因子配对，约 35×35）上下三角各装一个量：上三角 %active 暖色（黑-红-橙-黄）、下三角 %repressed 冷色（黑-蓝-绿），一图装两个矩阵

**有什么用**：一张方格表同时看两件事：右上半个表颜色越亮代表两个因子搭配时激活越强，左下半个表越亮代表抑制越强。哪对因子是'开关'、哪对平平，扫一眼就有数。

**部件亮点**
- 结构布局：单面板
- 编码方式：上三角%active黑红橙黄,下三角%repressed黑蓝绿,白色对角线,轴旋转基因名,右侧双色标,白点=显著

**复现**：配方 `scripts/recipes/case_seg107.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
