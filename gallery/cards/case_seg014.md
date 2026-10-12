---
title: Nature 系统发育树圈图(三)
kind: 数据图
purpose: [空间分布]
data: 约90个ASV的树+ASV名,门,大小,ΔNiche
input: newick (reference/data-schemas.json #014)
journal: Nature
wow: 3
recipe: scripts/recipes/case_seg014.py
preview: ../case_seg014.png
---

**一句话**：环形发育树+ASV热图环（Nature 风格）

**高级感**：★★★ 镇场级（用户要"高级/惊艳"时优先摆）

**适用场景**：约 80-120 个 ASV/OTU 的进化树，枝按门填色、支系区域浅色填充，叶端用黑点大小编码丰度

**有什么用**：一圈'家谱'树：枝条按大类铺了浅色底，叶端黑点越大代表这个物种数量越多，最外圈红白格子再标出每个物种某项指标是升是降，编号沿圆周排开方便查表。

**部件亮点**
- 结构布局：单面板
- 编码方式：枝按门填色+叶端黑点=ASV大小;外环ΔNiche红白热图;ASV编号放射标注;右侧门图例+色条

**复现**：配方 `scripts/recipes/case_seg014.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
