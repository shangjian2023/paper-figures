# -*- coding: utf-8 -*-
"""案例137 - Cell UMAP + 环形注释: 12 细胞类型高斯簇 + 外圈三层弧形注释环
(Celltype/Timepoint/Condition) + 右侧三块图例。
参考: frames/seg_134.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.lines import Line2D

set_style()

# ---- 12 簇: 名称/颜色/中心/协方差/点数
spec = [
    ('RGC',                 '#D9534F', (-1.0, 2.8), (2.1, 1.5, 0.3), 3800),
    ('Astrocyte',           '#2E5F8A', (-1.0, -0.6), (1.7, 1.1, 0.2), 3000),
    ('RPE',                 '#DAA23B', (3.1, -0.7), (0.5, 0.5, -0.75), 2000),
    ('MG',                  '#2E9E4F', (0.1, -2.6), (2.4, 0.8, 0.0), 2600),
    ('Monocyte_macrophage', '#B5D433', (-2.3, -3.1), (0.9, 0.6, 0.3), 800),
    ('Endothelial',         '#C2183C', (1.05, -2.3), (0.35, 0.28, 0.2), 420),
    ('Microglia',           '#36A852', (-3.4, -2.0), (0.55, 0.45, 0.4), 620),
    ('B_cell',              '#45C1B0', (-3.9, -0.85), (0.4, 0.35, 0.2), 480),
    ('Bipolar_cell',        '#8FD8C8', (-4.1, -1.7), (0.32, 0.3, 0.1), 380),
    ('Neutrophil',          '#6A3D9A', (-3.1, -3.7), (0.42, 0.36, 0.3), 520),
    ('T_cell',              '#F080B0', (-2.6, -3.2), (0.5, 0.4, -0.2), 480),
    ('Amacrine_cell',       '#4C7FA8', (0.85, -1.85), (0.4, 0.32, 0.1), 420)]
tp_colors = ['#E15759', '#F1CE63', '#4DC5D6', '#A0D995', '#27408B', '#2E8B57', '#F28E2B']
tp_names = ['Control', '12h', '1d', '2d', '4d', '1w', '2w']
cond_colors = ['#4C7FA8', '#F28E2B']
cond_names = ['Control', 'Injury']

r = rng(134)
pts, centers = [], []
for nm, c, mu, cv, n in spec:
    sx, sy, rho = cv
    cov = [[sx * sx, rho * sx * sy], [rho * sx * sy, sy * sy]]
    pts.append((nm, c, r.multivariate_normal(mu, cov, n).T))
    centers.append((nm, c, mu))

allp = np.hstack([p[2] for p in pts])
cx, cy = allp[0].mean(), allp[1].mean()
R = np.sqrt(((allp - np.array([[cx], [cy]]))**2).sum(0)).max()

# ---- 按质心角度排序, 分配弧段(以各自质心角为中心)
ang = np.arctan2([m[2][1] - cy for m in centers],
                 [m[2][0] - cx for m in centers])
deg = np.degrees(ang) % 360
order = np.argsort(deg)
ds = deg[order]
dd = np.diff(np.concatenate([ds, [ds[0] + 360]]))     # 到下一簇的角距
dprev = np.roll(dd, 1)
GAP = 3.0
segs = {}
for r_, i in enumerate(order):
    lo = ds[r_] - dprev[r_] / 2 + GAP
    hi = ds[r_] + dd[r_] / 2 - GAP
    lo = min(lo, ds[r_] - 2.0)          # 钳制: 保证包含自身角度且最小 4°
    hi = max(hi, ds[r_] + 2.0)
    segs[i] = (lo, hi)

fig, ax = plt.subplots(figsize=cm2in(19.5, 14.5))
for nm, c, xy in pts:
    ax.scatter(xy[0], xy[1], s=1.6, c=c, alpha=0.45, linewidths=0, zorder=2)

GAP = 3.0
r1, r2, r3, r4 = R * 1.06, R * 1.15, R * 1.24, R * 1.33
for i, (nm, c, mu) in enumerate(centers):
    lo, hi = segs[i]
    mid = (lo + hi) / 2
    ax.add_patch(Wedge((cx, cy), r2, lo, hi, width=r2 - r1, fc=c,
                       ec='white', lw=1.0, zorder=3))
    ax.add_patch(Wedge((cx, cy), r3, lo, hi, width=r3 - r2,
                       fc=tp_colors[i % 7], ec='white', lw=1.0, zorder=3))
    ax.add_patch(Wedge((cx, cy), r4, lo, hi, width=r4 - r3,
                       fc=cond_colors[i % 2], ec='white', lw=1.0, zorder=3))
    rot = 90 - mid
    if rot < -90 or rot > 90:
        rot += 180
    th = np.radians(mid)
    rl = r4 + (0.5 if i % 2 == 0 else 1.05)      # 交错半径避免标签互压
    ax.text(cx + rl * np.cos(th), cy + rl * np.sin(th),
            nm.replace('_', ' '), rotation=rot, rotation_mode='anchor',
            ha='center', va='center', fontsize=8.5, zorder=4)

for rr, lab in [((r1 + r2) / 2, 'Celltype'), ((r2 + r3) / 2, 'Timepoint'),
                ((r3 + r4) / 2, 'Condition')]:
    th = np.radians(6)
    ax.text(cx + rr * np.cos(th), cy + rr * np.sin(th), lab, rotation=90 - 6,
            rotation_mode='anchor', ha='center', va='center', fontsize=6.5,
            color='0.25', zorder=4)

ax.set_xlim(cx - r4 - 2.6, cx + r4 + 2.6)
ax.set_ylim(cy - r4 - 2.6, cy + r4 + 2.6)
ax.set_aspect('equal')
ax.set_xlabel('umap_1', fontsize=9)
ax.set_ylabel('umap_2', fontsize=9)
ax.tick_params(labelsize=6.5, length=2.5, width=0.7)
ax.set_xticks([]); ax.set_yticks([])
for sp in ('top', 'right'):
    ax.spines[sp].set_visible(False)

# ---- 右侧三块图例
h1 = [Line2D([], [], marker='s', ls='', ms=7, mfc=c, mec='none', label=nm)
      for nm, c, _ in centers]
h2 = [Line2D([], [], marker='s', ls='', ms=7, mfc=c, mec='none', label=nm)
      for nm, c in zip(tp_names, tp_colors)]
h3 = [Line2D([], [], marker='s', ls='', ms=7, mfc=c, mec='none', label=nm)
      for nm, c in zip(cond_names, cond_colors)]
leg1 = ax.legend(handles=h1, title='Celltype', loc='upper left',
                 bbox_to_anchor=(1.02, 0.99), frameon=False, fontsize=7.5,
                 title_fontsize=9, handletextpad=0.4, labelspacing=0.5,
                 borderaxespad=0)
ax.add_artist(leg1)
leg2 = ax.legend(handles=h2, title='Timepoint', loc='upper left',
                 bbox_to_anchor=(1.02, 0.50), frameon=False, fontsize=7.5,
                 title_fontsize=9, handletextpad=0.4, labelspacing=0.5,
                 borderaxespad=0)
ax.add_artist(leg2)
ax.legend(handles=h3, title='Condition', loc='upper left',
          bbox_to_anchor=(1.02, 0.19), frameon=False, fontsize=7.5,
          title_fontsize=9, handletextpad=0.4, labelspacing=0.5,
          borderaxespad=0)

save(fig, 'case_seg134.png')
