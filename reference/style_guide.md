# 期刊风格规则 + 助手 API + 实战坑清单

## 一、风格规则（set_style 已内置）

- 字体 Arial/Helvetica，正文 8pt，刻度 7pt，标题 9pt；`axes.unicode_minus=False` 防负号豆腐块。
- 尺寸：单栏 9cm≈3.5in，双栏 18cm≈7.1in；用 `cm2in(w, h)` 定 figsize；字号相对图幅缩放（小图配 6-7pt）。
- 只保留左/下轴线（`axes.spines.top/right=False`）；刻度朝外 0.8 宽。
- 线宽：数据线 1.2，误差棒/支架 0.9-1.2，参考虚线 0.6-0.8，网格线 0.4 且极淡。
- 调色板 `pal(name, n)`：nature(黑绿) / nature2 / science / cell(Tableau10) / macaron / rdbu / set3 / tab20 / muted。分类 ≤8 色；发散数据 RdBu/RdYlBu；大规模类别用 tab20 循环。
- 原始数据优先：柱/箱上叠散点（`jitter()` 抖动）；误差棒注明 SEM 或 SD；显著性标注分工——**vs 对照的柱顶星号**沿用所改配方的既有骨架（多为 `ax.text` 柱顶式），**任意两柱/两组之间的支架线**用 `sig_bracket(ax, x1, x2, y, '***')`；星号由实算 p 值生成：`helpers.stats.vs_control(groups, control=0)`（Welch t + Bonferroni，装了 statsmodels 自动升 Dunnett）+ `p_to_stars(p)`，换真实数据后不要沿用写死的星号。
- 基因名斜体 `italic_gene('KRAS')` → `$\it{KRAS}$`。
- 面板编号 `panel_label(ax, 'a')`；导出 `save(fig, 'name.png')`（300dpi 自动落 gallery），矢量用 `fig.savefig('name.pdf')`。

## 二、助手 API

### ternary 三元图
```python
from helpers.ternary import Ternary
t = Ternary(ax, vertex_labels=('A(上)', 'B(左下)', 'C(右下)'))
t.setup(grid_values=(20,40,60,80), grid_colors=('r','g','b'))   # 网格+刻度+顶点
t.edge_arrows(['fa名','fb名','fc名'])                            # 三边箭头
t.scatter(fa, fb, fc, c=..., s=...)                              # 数组或标量, 自动归一
t.density(fa, fb, fc, cmap='Purples')                            # KDE 等高线(掩膜到三角内)
# 坐标: x=0.5*fa+fc, y=fa*H; 注意先 density 后 scatter(后画者在上)
```

### chord 和弦图
```python
from helpers.chord import chord_diagram
chord_diagram(labels, matrix, colors, ax, gap_deg=4, ribbon_alpha=0.45)
# matrix 方阵, 行=源; 带色=源节点色
```

### sankey 桑基/冲击图
```python
from helpers.sankey import sankey
sankey(layers, links, ax)
# layers=[{节点名: 高度值}, ...] 每层一个 dict
# links=[(层i, 源名, 层j, 目标名, 值, 颜色), ...] j=i+1
```

### upset UpSet 图
```python
from helpers.upset import upset_plot_pro
fig, ax_top, ax_mid = upset_plot_pro(sets, color='#3B6E8F', max_inter=15)
# 交集条形/点阵/setSize 三区; 返回轴可后处理(改色/空心点/行底纹)
```

### newick 系统发育树
```python
from helpers.newick import random_newick, parse_newick, draw_circular_tree, draw_rect_tree
tree = parse_newick(newick_str)          # 或 random_newick(n_leaves, seed) 造树
draw_circular_tree(ax, tree, color_fn=lambda nm,leaf,d: col, tip_labels=False)
draw_rect_tree(ax, tree, ...)            # 矩形肘版
# 环形注释环: 在同一笛卡尔 ax 上叠 patches.Wedge((0,0), r_out, deg1, deg2, width=...)
# 树占半径 0~0.55, 注释环从 0.62 起
```

### geo 地图
```python
from helpers.geo import world_map, china_map, china_names
world_map(ax, facecolor_fn=lambda props: '#8FB8D8' if props.get('name')=='China' else '#E8E8E8',
          extent=(-180,180,-60,85))      # 返回 None 可跳过某国
china_map(ax, ...)                       # props.get('name')=省名; extent 默认全境
# 饼图叠加: mercator(lon,lat) 把经纬度转画布坐标
```

## 三、实战坑清单（146 案例修复中真实踩过）

### matplotlib 3.11
1. `ax.boxplot(..., orientation='horizontal')` 替代旧 `vert=False`；上色需 `patch_artist=True` 后遍历 `box['boxes']`。
2. 共享轴（sharex/sharey）后再 `set_xlim` 会被边际轴覆盖——边际分布图各轴要独立创建。
3. `inset_axes` 继承父轴的 log formatter，需显式 `set_xticklabels`/ScalarFormatter。
4. 极坐标 `set_xticks` 可能触发 theta 轴 autoscale 冒出黑色起止 spine——用 `set_thetamin/set_thetamax` 复位；`set_rorigin` 小于 rmin 时中心会被裁剪，中心大圆盘用 `transAxes Circle + clip_on=False` 画；axes 白底 patch 会遮内部 Wedge，注意 zorder。
5. seaborn 绘制会覆盖 rcParams：先 sns 后重跑 `set_style()` 或手动补字体。

### numpy 2.x
6. `np.ptp` 只剩函数形式（`arr.ptp()` 方法被移除）。

### 标签防重叠（出现率最高的失败原因）
7. 万能模式：同侧标签按 y（或角度）排序 → 逐个钳制最小间距 → 整体回中 → 短引线连回数据点。
8. 点云上的文字必须：`zorder≥6` + 白描边 `matplotlib.patheffects.withStroke(linewidth=2, foreground='white')` 或半透明白底 bbox。
9. 引线端点要落在文字盒侧缘外，不能竖穿文字——先放文字再算线。
10. 色标刻度：稀疏化（3-5 档）、用 FormatStrFormatter 固定格式，防 '-0.0'/'--0.5' 与粘连；色标标题与刻度留 pad。
11. 环形图外圈标签：统一半径+切向旋转+隔根错位；标签太多就稀疏化显示，宁缺勿叠。
12. 图例颜色必须与图中元素一一对应（修复中出现过色条 cmap 与气泡色系不一致）。

### 构图
13. 上下排布的复合图用 gridspec 明确行高与 hspace，别让单面板偏右留大空白。
14. 底部竖排/旋转标签要 `clip_on=False` 且 figure 底部预留标签带，防压绘图区与画布截断。
15. 断轴：两段子图+在断口画两条斜断裂线（`plot` 标记 `//`），显著性支架悬浮于空白区是惯例。
16. 双 Y 轴 twinx 记得让两轴网格二选一（另一轴 `grid(False)`），图例合并放顶部。
17. 山脊图：从上往下画、zorder 递减，后行遮前行形成 ridge；每行配细基线。
18. 密度等高线先画、散点后画（否则散点被盖）；KDE 网格要掩膜到坐标区内部（如三元三角）。
19. Arial 无 ∝/≈ 等 Unicode 符号字形（渲染成豆腐块）——用 mathtext `$\propto$`/`$pprox$` 表达。
