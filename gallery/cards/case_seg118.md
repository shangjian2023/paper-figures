---
title: PNAS 中国地图(二)
kind: 数据图
purpose: [空间分布]
data: 省界;城市:经纬度,亏缺量分档
input: long (reference/data-schemas.json #118)
journal: PNAS
recipe: scripts/recipes/case_seg118.py
preview: ../case_seg118.png
---

**一句话**：中国地图+气泡图（PNAS 风格）

**部件亮点**
- 结构布局：单面板
- 编码方式：省界白底灰线,粉红城市气泡4档=亏缺量,绿色南北分界线,省名标注,指北针+比例尺+图例

**复现**：配方 `scripts/recipes/case_seg118.py` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
