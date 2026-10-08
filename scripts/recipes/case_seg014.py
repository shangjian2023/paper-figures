# -*- coding: utf-8 -*-
"""案例14 - Nature 环形系统发育树圈图(三)。
参考: frames/seg_014.jpg — 黑枝+进化枝淡彩底+叶端黑点(ASV大小) + ΔNiche红白热图环 + ASV放射标注 + 右侧图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'helpers'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
from matplotlib import cm, colors as mcolors
from newick import random_newick, parse_newick

SEED, N = 14, 88

# ---------------------------------------------------------------- 门分块(块大小不等, 模拟进化枝)
PHY = [('Actinobacteria', '#7FBFB0', 5), ('Armatimonadetes', '#F0A860', 3),
       ('Bacteroidetes', '#E85D5D', 24), ('Cand_division_WPS-1', '#4A6FB5', 4),
       ('Cand_division_WPS-2', '#2E7D5B', 3), ('Cand_Saccharibacteria', '#9FBFE8', 4),
       ('Chloroflexi', '#C8C8E8', 4), ('Cyanobacteria/Chloroplast', '#F0B8B8', 5),
       ('Euryarchaeota', '#E8D0C8', 3), ('Firmicutes', '#F0E0A8', 6),
       ('Gemmatimonadetes', '#D8C8E8', 4), ('Ignavibacteriae', '#E8C8D8', 3),
       ('Planctomycetes', '#8898D0', 4), ('Proteobacteria', '#F0C0C8', 5),
       ('Thaumarchaeota', '#F5EBC8', 4), ('Verrucomicrobia', '#98C8D8', 4),
       ('Unassigned', '#FFFFFF', 3)]
assert sum(k for _, _, k in PHY) == N
SHADE = {'Bacteroidetes': '#FBE9A8', 'Chloroflexi': '#CDEBE2',
         'Cyanobacteria/Chloroplast': '#F9DDDD', 'Firmicutes': '#D9EFD3',
         'Gemmatimonadetes': '#E3D9F2', 'Actinobacteria': '#D5EBE5'}

tree = parse_newick(random_newick(N, seed=SEED))

def leaves_of(nd):
    if not nd['children']:
        return [nd['name']]
    out = []
    for c in nd['children']:
        out += leaves_of(c)
    return out

order = leaves_of(tree)
r14 = rng(SEED)
leaf2ph = {}
i = 0
for nm, col, k in PHY:
    for t in order[i:i + k]:
        leaf2ph[t] = (nm, col)
    i += k
asv_size = np.clip(r14.lognormal(6.3, 0.9, N), 300, 3200)     # ASV reads
dniche = np.clip(r14.normal(0.18, 0.30, N), -0.5, 0.5)
cmap = plt.get_cmap('Reds')
norm = mcolors.Normalize(-0.5, 0.5)

# ---------------------------------------------------------------- 黑色环形树
R0, R1 = 0.07, 0.55
ang = {nm: 2 * np.pi * (j + 0.5) / N for j, nm in enumerate(order)}
nleaf = {}

def cnt(nd):
    nleaf[id(nd)] = 1 if not nd['children'] else sum(cnt(c) for c in nd['children'])
    return nleaf[id(nd)]
cnt(tree)

def maxd(nd):
    return 0 if not nd['children'] else 1 + max(maxd(c) for c in nd['children'])
TOT = max(maxd(tree), 1)

def rd(d):
    return R0 + (R1 - R0) * d / TOT

def P(th, r):
    return (r * np.cos(th), r * np.sin(th))

fig = plt.figure(figsize=cm2in(17.5, 12.5))
gs = fig.add_gridspec(1, 2, width_ratios=[1.22, 1], wspace=0.04)
ax = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# 进化枝淡彩底
hw = np.pi / N
i = 0
for nm, col, k in PHY:
    if nm in SHADE:
        a0 = np.degrees(ang[order[i]] - hw)
        a1 = np.degrees(ang[order[i + k - 1]] + hw)
        ax.add_patch(Wedge((0, 0), R1 + 0.02, a0, a1, width=R1 + 0.02 - 0.10,
                           facecolor=SHADE[nm], edgecolor='none', alpha=0.85, zorder=1))
    i += k

SPAN = {id(tree): (0.0, 2 * np.pi, 0)}

def walk(nd):
    a0, a1, d = SPAN[id(nd)]
    if nd['children']:
        k = nleaf[id(nd)]; pos = a0
        for ch in nd['children']:
            w = nleaf[id(ch)] / k * (a1 - a0)
            SPAN[id(ch)] = (pos, pos + w, d + 1); pos += w
        mid = 0.5 * (a0 + a1)
        (x0, y0), (x1, y1) = P(mid, rd(d)), P(mid, rd(d + 1))
        ax.plot([x0, x1], [y0, y1], color='black', lw=0.55, zorder=2)
        ax.add_patch(Wedge((0, 0), rd(d + 1), np.degrees(a0), np.degrees(a1),
                           width=max(rd(d + 1) - rd(d), 1e-4), facecolor='none',
                           edgecolor='black', lw=0.55, zorder=2))
        for ch in nd['children']:
            walk(ch)
    else:
        a = ang[nd['name']]
        (x0, y0), (x1, y1) = P(a, rd(d)), P(a, R1)
        ax.plot([x0, x1], [y0, y1], color='black', lw=0.55, zorder=2)
        ms = 1.6 + 4.6 * (asv_size[order.index(nd['name'])] - 300) / 2900
        ax.plot([x1], [y1], 'o', ms=ms, color='black', zorder=3)

walk(tree)

# ---------------------------------------------------------------- ΔNiche 热图环
RI, RO = 0.62, 0.70
for j, nm in enumerate(order):
    a = np.degrees(ang[nm])
    ax.add_patch(Wedge((0, 0), RO, a - np.degrees(hw) * 0.96, a + np.degrees(hw) * 0.96,
                       width=RO - RI, facecolor=cmap(norm(dniche[j])),
                       edgecolor='#999999', lw=0.25, zorder=2))

# ASV 放射标注(每隔一叶)
for j, nm in enumerate(order):
    if j % 2:
        continue
    deg = np.degrees(ang[nm])
    a = ang[nm]
    rot = deg - 90 if not (90 < deg % 360 <= 270) else deg + 90
    ax.text((RO + 0.025) * np.cos(a), (RO + 0.025) * np.sin(a), nm,
            rotation=rot, rotation_mode='anchor', fontsize=4.6,
            ha='center', va='center', color='#333333')

ax.set_xlim(-1.02, 1.02); ax.set_ylim(-1.02, 1.02)
ax.set_aspect('equal'); ax.axis('off')

# ---------------------------------------------------------------- 右侧图例
ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.axis('off')
ax2.text(0.02, 0.985, 'Phylum', fontsize=8, va='top')
y = 0.945
for nm, col, _k in PHY:
    ax2.add_patch(plt.Rectangle((0.03, y - 0.014), 0.026, 0.021,
                                facecolor=col, edgecolor='#999999', lw=0.4))
    ax2.text(0.064, y - 0.004, nm, fontsize=5.8, va='center')
    y -= 0.0235

# Δ Niche colorbar
y1 = y - 0.055
ax2.text(0.02, y1, u'\u0394 Niche breadths', fontsize=8, va='top')
CB_TOP, CB_H = y1 - 0.035, 0.24
for t_i in range(14):
    v = 1 - t_i / 13.0
    ax2.add_patch(plt.Rectangle((0.05, CB_TOP - t_i * CB_H / 14 - CB_H / 14), 0.045,
                                CB_H / 14 + 0.001, facecolor=cmap(v),
                                edgecolor='none'))
# 刻度标签紧贴色棒即可; 不再画短刻度线——刻度线与文字粘连会被读成 '--0.5'/'-0.0'
for v, lab in [(1.0, '0.5'), (0.5, '0.0'), (0.0, '-0.5')]:
    yy = CB_TOP - (1 - v) * CB_H
    ax2.text(0.104, yy, lab, fontsize=6, va='center', ha='left')

# ASV size legend
y2 = CB_TOP - CB_H - 0.05
ax2.text(0.02, y2, 'ASV size', fontsize=8, va='top')
yy = y2 - 0.045
for lab in [500, 1000, 2000, 3000]:
    ms = 1.6 + 4.6 * (lab - 300) / 2900
    ax2.add_patch(Circle((0.055, yy), ms * 0.0026, facecolor='black',
                         edgecolor='black'))
    ax2.text(0.10, yy, str(lab), fontsize=6, va='center')
    yy -= 0.032

save(fig, 'case_seg014.png')
