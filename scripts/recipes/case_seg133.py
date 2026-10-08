# -*- coding: utf-8 -*-
"""案例135 - Cell 环形热图 + UpSet 内嵌。
外圈 6 扇区弧形热图(基因×5 Exp, 蓝白红 -2~2), 基因名放射排列,
扇区间留白 + 内侧弧形通路名; 中心迷你 UpSet(交集柱+点阵+Set size)。
参考: frames/seg_133.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Wedge
from matplotlib.colors import Normalize

set_style()

r = rng(133)
pathways = ['Metabolism', 'Cell_Cycle', 'Signaling', 'Hypoxia', 'Immune',
            'Morphogenic']
arc_colors = ['#bccfec', '#e9b9cd', '#f0cfc2', '#f3efe4', '#bccfec', '#f2ddc4']
n_gene, n_exp = 8, 5
span, gap = 52.0, 8.0
r_out, row_h = 1.48, 0.055
r_heat_in = r_out - n_gene * row_h          # 热图内半径
r_band_out, r_band_in = r_heat_in - 0.015, r_heat_in - 0.115

names_pool = [f'Gene{i}' for i in r.permutation(np.arange(1, 51))] * 2
cmap = plt.get_cmap('RdBu')
norm = Normalize(-2, 2)

fig = plt.figure(figsize=cm2in(19.0, 18.6))
ax = fig.add_axes([0.045, 0.015, 0.84, 0.90])
ax.set_xlim(-1.85, 1.85)
ax.set_ylim(-1.85, 1.85)
ax.set_aspect('equal')
ax.axis('off')

for k, pw in enumerate(pathways):
    c = 90 - k * (span + gap) - span / 2.0        # 扇区中心角, 顺时针
    t1, t2 = c - span / 2, c + span / 2
    # 扇区热图
    vals = r.normal(0, 0.9, (n_gene, n_exp)).clip(-2, 2)
    for g in range(n_gene):
        ro = r_out - g * row_h
        ri = ro - row_h + 0.006
        for e in range(n_exp):
            a1 = t1 + e * span / n_exp
            a2 = a1 + span / n_exp - 0.4
            ax.add_patch(Wedge((0, 0), ro, a1, a2, width=ro - ri,
                               facecolor=cmap(norm(vals[g, e])),
                               edgecolor='white', lw=0.3))
    # 通路弧带 + 名字
    ax.add_patch(Wedge((0, 0), r_band_out, t1, t2,
                       width=r_band_out - r_band_in, facecolor=arc_colors[k],
                       edgecolor='white', lw=1.0))
    amid = np.radians(c)
    trot = (c + 90) % 360                      # 弧面切向, 保证可读
    if 90 < trot <= 270:
        trot -= 180
    ax.text(np.cos(amid) * (r_band_out - 0.05), np.sin(amid) * (r_band_out - 0.05),
            pw, rotation=trot, rotation_mode='anchor', ha='center', va='center',
            fontsize=9, color='#1f3b66', fontweight='bold')
    # 基因名: 统一放环外同一半径 (放射状排开, 切向旋转, 白描边不压色带)
    for g in range(n_gene):
        ang = t1 + (g + 0.5) * span / n_gene
        arad = np.radians(ang)
        rot = (ang + 90) % 360                  # 切向, 保证可读
        if 90 < rot <= 270:
            rot -= 180
        ax.text(np.cos(arad) * (r_out + 0.07), np.sin(arad) * (r_out + 0.07),
                names_pool[k * n_gene + g], rotation=rot,
                rotation_mode='anchor', ha='center', va='center',
                fontsize=5.5, color='0.15',
                path_effects=[pe.withStroke(linewidth=1.6, foreground='white')])

# 顶部扇区的 Exp_1..Exp_5 列标签
t1 = 90 - span / 2
for e in range(n_exp):
    a = np.radians(t1 + (e + 0.5) * span / n_exp)
    ax.text(np.cos(a) * 1.62, np.sin(a) * 1.62, f'Exp_{e + 1}',
            ha='center', va='center', fontsize=6.5)

# ------------------------------------------------ 中心迷你 UpSet
ux = fig.add_axes([0.365, 0.335, 0.235, 0.235])
ux.set_xlim(-3.4, 17.5)
ux.set_ylim(-1.3, 8.6)
ux.axis('off')
n_int = 15
sizes = np.array([2, 1, 2, 2, 3, 2, 2, 3, 3, 3, 4, 3, 5, 6, 7])
subs = [[0], [2], [0, 1], [1], [0, 1, 2], [2, 3], [1, 2], [0, 2],
        [0, 1, 3], [2, 4], [1, 2, 3], [0, 1, 2, 4], [1, 2, 3, 4],
        [0, 1, 2, 3, 4], [0, 2, 3, 4]]
bar_c = '#3b7dd8'
for i in range(n_int):
    h = sizes[i] * 0.42
    ux.add_patch(plt.Rectangle((i - 0.32, 5.6), 0.64, h, facecolor=bar_c,
                               edgecolor='none'))
    ux.plot([i, i], [4.6, 5.6], color='0.75', lw=0.6, zorder=1)
    for s in range(5):
        on = s in subs[i]
        ux.scatter(i, 4 - s, s=7, facecolor=bar_c if on else '#c9d6ec',
                   edgecolor='0.5', linewidth=0.3, zorder=3)
set_names = ['Cell_Cycle', 'Signaling', 'Hypoxia', 'Immune', 'Metabolism']
for s, nm in enumerate(set_names):
    ux.text(15.4, 4 - s, nm, fontsize=5.8, va='center')
    w = r.uniform(0.9, 2.1)
    ux.add_patch(plt.Rectangle((-3.3, 4 - s - 0.28), w, 0.56,
                               facecolor=['#f2b9c6', '#f6cdd6', '#fae4e9',
                                          '#b9cdf0', '#a9c2ec'][s],
                               edgecolor='0.6', linewidth=0.3))
ux.text(-3.3, 8.0, 'Intersection size', fontsize=5.8, ha='left')
ux.text(-3.3, -1.05, 'Set size', fontsize=5.8, ha='left')
ux.text(0.0, -1.05, '', fontsize=1)

# 中心底部标题
ax.text(0.0, -0.86, 'Morphogenic\ngenes', ha='center', va='center',
        fontsize=9.5, fontweight='bold', color='#1a1a1a')

# ------------------------------------------------ Expression 色标
cax = fig.add_axes([0.905, 0.735, 0.022, 0.15])
fig.colorbar(plt.cm.ScalarMappable(norm, cmap), cax=cax,
             ticks=[2, 1.2, 0.4, -0.4, -1.2, -2])
cax.tick_params(labelsize=6.5)
cax.set_title('Expression', fontsize=8, loc='left', pad=5)

save(fig, 'case_seg133.png')
