# -*- coding: utf-8 -*-
"""案例15 - Nature 环形系统发育树圈图(四)。
参考: frames/seg_015.jpg — 枝色=门+属区淡彩底+属名弧标 + BBAA红渐变环 + bsh蓝白有无环 + 右侧3组图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'helpers'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib import cm, colors as mcolors
from newick import random_newick, parse_newick

SEED, N = 15, 100

# ---------------------------------------------------------------- 门分块 + 属进化枝
PHY = [('Actinobacteria', '#C0392B', 6), ('Bacteroidetes', '#45B5C4', 30),
       ('Firmicutes', '#3CA85C', 40), ('Fusobacteria', '#2E4D7B', 6),
       ('Lentisphaerae', '#E8896C', 4), ('Proteobacteria', '#8C8C9E', 4),
       ('Spirochaetes', '#9FD8B4', 5), ('Verrucomicrobia', '#8B1A1A', 5)]
GENERA = [('Bifidobacterium', 0, 4, '#F7DBDD'), ('Collinsella', 4, 2, '#E9E4E6'),
          ('Bacteroides', 6, 22, '#D7ECF7'), ('Enterococcus', 36, 12, '#DBF0DB'),
          ('Clostridium', 48, 20, '#D4EEDA'), ('Fusobacterium', 76, 6, '#DDE0F2')]

tree = parse_newick(random_newick(N, seed=SEED))

def leaves_of(nd):
    if not nd['children']:
        return [nd['name']]
    out = []
    for c in nd['children']:
        out += leaves_of(c)
    return out

order = leaves_of(tree)
leaf2ph = {}
i = 0
for nm, col, k in PHY:
    for t in order[i:i + k]:
        leaf2ph[t] = col
    i += k
r15 = rng(SEED)
bbaa = np.clip(r15.normal(0.20, 0.16, N), 0.005, 0.6)
bsh = r15.random(N) < 0.45
cmap = plt.get_cmap('Reds')
norm = mcolors.Normalize(0, 0.6)

# ---------------------------------------------------------------- 环形树
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

fig = plt.figure(figsize=cm2in(17.5, 11.5))
gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1], wspace=0.02)
ax = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
hw = np.pi / N

# 属区淡彩底 + 属名
for nm, i0, k, col in GENERA:
    a0 = np.degrees(ang[order[i0]] - hw)
    a1 = np.degrees(ang[order[i0 + k - 1]] + hw)
    ax.add_patch(Wedge((0, 0), R1 + 0.015, a0, a1, width=R1 + 0.015 - 0.09,
                       facecolor=col, edgecolor='none', alpha=0.9, zorder=1))
    amid = np.radians(0.5 * (a0 + a1))
    deg = 0.5 * (a0 + a1) % 360
    rot = deg - 90 if 0 < deg <= 180 else deg + 90
    ax.text(0.60 * np.cos(amid), 0.60 * np.sin(amid), nm, rotation=rot,
            fontsize=6, ha='center', va='center', color='#333333')

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
        ax.plot([x0, x1], [y0, y1], color='#555555', lw=0.5, zorder=2)
        ax.add_patch(Wedge((0, 0), rd(d + 1), np.degrees(a0), np.degrees(a1),
                           width=max(rd(d + 1) - rd(d), 1e-4), facecolor='none',
                           edgecolor='#555555', lw=0.5, zorder=2))
        for ch in nd['children']:
            walk(ch)
    else:
        a = ang[nd['name']]
        (x0, y0), (x1, y1) = P(a, rd(d)), P(a, R1)
        ax.plot([x0, x1], [y0, y1], color=leaf2ph[nd['name']], lw=0.75, zorder=2)

walk(tree)

# ---------------------------------------------------------------- 双注释环
for j, nm in enumerate(order):
    a = np.degrees(ang[nm])
    ax.add_patch(Wedge((0, 0), 0.685, a - np.degrees(hw) * 0.92,
                       a + np.degrees(hw) * 0.92, width=0.065,
                       facecolor=cmap(norm(bbaa[j])), edgecolor='#AAAAAA',
                       lw=0.25, zorder=2))
    ax.add_patch(Wedge((0, 0), 0.78, a - np.degrees(hw) * 0.92,
                       a + np.degrees(hw) * 0.92, width=0.062,
                       facecolor='#4FB3C5' if bsh[j] else '#DCE9F4',
                       edgecolor='#AAAAAA', lw=0.25, zorder=2))

ax.set_xlim(-1.0, 1.0); ax.set_ylim(-1.0, 1.0)
ax.set_aspect('equal'); ax.axis('off')

# ---------------------------------------------------------------- 右侧图例
ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.axis('off')
ax2.text(0.02, 0.99, 'Fraction of total\nBBAAs detected', fontsize=7.5, va='top')
CB_TOP, CB_H = 0.86, 0.24
for t_i in range(14):
    ax2.add_patch(plt.Rectangle((0.05, CB_TOP - t_i * CB_H / 14 - CB_H / 14),
                                0.045, CB_H / 14 + 0.001,
                                facecolor=cmap(1 - t_i / 13.0), edgecolor='none'))
for v in [0.6, 0.4, 0.2, 0.0]:
    yy = CB_TOP - (1 - v / 0.6) * CB_H
    ax2.plot([0.095, 0.103], [yy, yy], lw=0.6, color='black')
    ax2.text(0.108, yy, ('%.1f' % v), fontsize=6, va='center')

y = CB_TOP - CB_H - 0.07
ax2.text(0.02, y, u'Presence of bsh gene', fontsize=7.5, va='top')
for lab, col in [('Absent', '#DCE9F4'), ('Present', '#4FB3C5')]:
    y -= 0.035
    ax2.add_patch(plt.Rectangle((0.03, y - 0.016), 0.030, 0.024,
                                facecolor=col, edgecolor='#999999', lw=0.4))
    ax2.text(0.075, y - 0.004, lab, fontsize=6.5, va='center')

y -= 0.05
ax2.text(0.02, y, 'Phylum', fontsize=7.5, va='top')
for nm, col, _k in PHY:
    y -= 0.030
    ax2.plot([0.045], [y - 0.004], 'o', ms=4, color=col)
    ax2.text(0.075, y - 0.004, nm, fontsize=6.5, va='center')

save(fig, 'case_seg015.png')
