---
title: Nature 热图
kind: 数据图
purpose: [相关关系]
data: 43代谢物×8受体×(fold change,显著性)
input: matrix (reference/data-schemas.json #019)
journal: Nature
wow: 1
recipe: scripts/recipes/case_seg019.py
preview: ../case_seg019.png
---

**一句话**：注释热图（Nature 风格）

**高级感**：★ 常规扎实

**适用场景**：几十个化合物/代谢物 × 5-10 个靶点/受体的活性或倍数变化矩阵，色块填方向+星号标显著性

**有什么用**：一张彩色表格：每行一种代谢物、每列一个靶点，红=增强、青=抑制、带星号=统计显著；扫一眼就知道哪些组合有效、哪一列靶点最活跃。

**部件亮点**
- 结构布局：单面板
- 编码方式：43胆汁酸×8受体:红=上调、蓝绿=下调、白=无,显著格*号;顶部Fold Change对数色条;行按类别分组留白

**复现**：配方 `scripts/recipes/case_seg019.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
