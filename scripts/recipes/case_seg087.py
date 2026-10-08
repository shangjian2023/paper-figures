# -*- coding: utf-8 -*-
"""案例89(seg087) - Nature 一维变量相关性热图: 39×39 下三角。
灰阶=正相关、红阶=负相关; 变量名按 4 组着色(微生物紫/样地青/土地橙/流域蓝)。
参考: frames/seg_087.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import Rectangle
from matplotlib.cm import ScalarMappable

groups = [
    ('Microbial', '#7b52ab', [
        'MAG richness', 'MAG Shannon diversity', 'Gene richness',
        'Gene Shannon diversity', 'Aerobic Microaerophillic', 'Light driven',
        'N reducer', 'DNRA', 'Methanotroph']),
    ('Site', '#17b3c9', [
        'Stream order', 'Latitude', 'Longitude', 'Water column height',
        'NPOC', 'Specific conductivity', 'SO4--', 'NO2--', 'Total nitrogen']),
    ('Land use', '#e8891d', [
        'Dam density', 'Percentage fire', 'Percentage open water',
        'Percentage developed open space', 'Percentage low-intensity developed',
        'Percentage medium-intensity developed',
        'Percentage high-intensity developed', 'Percentage barren land',
        'Percentage deciduous forest', 'Percentage coniferous forest',
        'Percentage grassland', 'Percentage crop',
        'Percentage wooded wetland', 'Percentage herbaceous wetland']),
    ('Watershed', '#2b5fad', [
        'Precipitation', 'WWTP density', 'Aridity', 'NPP',
        'Mean temperature', 'Runoff', 'Drainage area'])]
names = [s for _, _, ss in groups for s in ss]
gidx = np.array([gi for gi, (_, _, ss) in enumerate(groups) for _ in ss])
n = len(names)                        # 39

r = rng(87)
M = r.uniform(-0.30, 0.35, (n, n))
def blk(a, b, lo, hi):
    ia, ib = np.where(gidx == a)[0], np.where(gidx == b)[0]
    M[np.ix_(ia, ib)] = r.uniform(lo, hi, (len(ia), len(ib)))
for g in range(4):                    # 组内正相关
    blk(g, g, 0.35, 0.92)
blk(0, 2, -0.85, -0.30)               # 微生物 × 土地利用: 负
blk(0, 3, 0.15, 0.55)                 # 微生物 × 流域: 正
blk(1, 2, 0.10, 0.45)
blk(2, 3, 0.25, 0.65)
M = (M + M.T) / 2
np.fill_diagonal(M, 1.0)

cmap_all = LinearSegmentedColormap.from_list(
    'rg', ['#67000d', '#a50f15', '#ef6548', '#fcae91', '#f7f7f7',
           '#bdbdbd', '#969696', '#636363', '#252525'], N=256)

fig = plt.figure(figsize=cm2in(19.0, 19.5))
gs = fig.add_gridspec(1, 1, left=0.015, right=0.985, top=0.985, bottom=0.075)
ax = fig.add_subplot(gs[0])

cmap_pos = plt.get_cmap('Greys')
cmap_neg = plt.get_cmap('Reds_r')
for i in range(n):
    for j in range(i + 1):                # 下三角含对角
        v = M[i, j]
        if v >= 0:
            fc = cmap_pos(v)              # 正相关: 灰阶
        else:
            fc = cmap_neg(v)              # 负相关: 红阶
        ax.add_patch(Rectangle((j, i), 1, 1, facecolor=fc,
                               edgecolor='white', linewidth=0.25, zorder=2))
ax.set_xlim(-14.0, n + 12.5)
ax.set_ylim(n + 2.2, -9.8)
ax.set_xticks([]); ax.set_yticks([])
ax.axis('off')

# 行名(左, 着色) / 列名(上, 45°着色) / 右侧组色条 + 名单
for j in range(n):
    ax.text(j + 0.5, -0.7, names[j], rotation=45, ha='left', va='bottom',
            fontsize=4.6, color=groups[gidx[j]][1])
for i in range(n):
    ax.text(-0.7, i + 0.5, names[i], ha='right', va='center',
            fontsize=4.6, color=groups[gidx[i]][1])
    ax.add_patch(Rectangle((n + 1.0, i + 0.06), 1.5, 0.88,
                           facecolor=groups[gidx[i]][1], edgecolor='none'))
    ax.text(n + 3.0, i + 0.5, names[i], ha='left', va='center', fontsize=4.6)
for gi, (gname, gc, _) in enumerate(groups):
    rows = np.where(gidx == gi)[0]
    ax.text(-12.6, (rows[0] + rows[-1]) / 2.0 + 0.5, gname, rotation=90,
            ha='center', va='center', fontsize=6.5, color=gc)

# 底部色条
pos = ax.get_position()
cax = fig.add_axes([pos.x0 + pos.width * 14.0 / 65.5, pos.y0 - 0.038,
                    pos.width * 39 / 65.5, 0.016])
cb = fig.colorbar(ScalarMappable(norm=Normalize(-1, 1), cmap=cmap_all),
                  cax=cax, orientation='horizontal',
                  ticks=[-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
cb.ax.tick_params(labelsize=6.5, length=2.5)
cb.outline.set_linewidth(0.7)

save(fig, 'case_seg087.png')
