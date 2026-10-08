# -*- coding: utf-8 -*-
"""案例12 - Nature 环形系统发育树圈图(一)。
参考: frames/seg_012.jpg — 环形树(枝按10门着色) + Type/Phylum/Occurrence 三注释环 + 右侧三组图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'helpers'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from newick import random_newick, parse_newick

SEED, N = 12, 60

# ---------------------------------------------------------------- 数据
PHYLUM = [('Proteobacteria',  '#C94F1E', 14, 2474),
          ('Bacteroidota',    '#E8823A', 10,  822),
          ('Actinobacteriota','#F0A868',  7,  383),
          ('Cyanobacteria',   '#F7CBA8',  6,  281),
          ('Firmicutes',      '#5CAD55',  5,  187),
          ('Planctomycetota', '#8BC98B',  4,  123),
          ('Chloroflexi',     '#B2DDB2',  4,  117),
          ('Verrucomicrobiota','#D5ECD5', 4,  107),
          ('Desulfobacterota','#8A8AB0',  3,   78),
          ('Marinisomatota',  '#B3A8D5',  3,   76)]
TYPE_COL = {'WGS': '#111111', 'MAG': '#E87D2B', 'SAG': '#3B7DD8'}
OCC_COL = ['#1E7A3C', '#A8D8A0', '#FFFFFF']          # >=10 / >=1 / absent

tree = parse_newick(random_newick(N, seed=SEED))

def leaves_of(nd):
    if not nd['children']:
        return [nd['name']]
    out = []
    for c in nd['children']:
        out += leaves_of(c)
    return out

order = leaves_of(tree)                                # DFS 叶序
leaf2ph = {}
i = 0
for nm, col, k, _n in PHYLUM:                          # 门沿叶序成块(进化枝连贯)
    for t in order[i:i + k]:
        leaf2ph[t] = (nm, col)
    i += k
r12 = rng(SEED)
leaf2type = {t: r12.choice(['WGS', 'MAG', 'SAG'], p=[0.30, 0.55, 0.15]) for t in order}
leaf2occ = {t: int(r12.choice(3, p=[0.18, 0.34, 0.48])) for t in order}

# ---------------------------------------------------------------- 环形树(枝=枝各大门优势色)
R0, R1 = 0.06, 0.55
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

def ncol(nd):
    if not nd['children']:
        return leaf2ph[nd['name']][1]
    u, c = np.unique([ncol(x) for x in nd['children']], return_counts=True)
    return u[np.argmax(c)]

fig = plt.figure(figsize=cm2in(17.5, 10.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1.18, 1], wspace=-0.05)
ax = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

def walk(nd):
    a0, a1, d = SPAN[id(nd)]
    if nd['children']:
        k = nleaf[id(nd)]; pos = a0
        for ch in nd['children']:
            w = nleaf[id(ch)] / k * (a1 - a0)
            SPAN[id(ch)] = (pos, pos + w, d + 1); pos += w
    if not nd['children']:
        a = ang[nd['name']]
        (x0, y0), (x1, y1) = P(a, rd(d)), P(a, R1)
        ax.plot([x0, x1], [y0, y1], color=leaf2ph[nd['name']][1], lw=0.7, zorder=2)
        ax.plot([x1], [y1], 'o', ms=1.6, color=leaf2ph[nd['name']][1], zorder=3)
    else:
        col = ncol(nd)
        mid = 0.5 * (a0 + a1)
        (x0, y0), (x1, y1) = P(mid, rd(d)), P(mid, rd(d + 1))
        ax.plot([x0, x1], [y0, y1], color=col, lw=0.7, zorder=2)
        ax.add_patch(Wedge((0, 0), rd(d + 1), np.degrees(a0), np.degrees(a1),
                           width=max(rd(d + 1) - rd(d), 1e-4), facecolor='none',
                           edgecolor=col, lw=0.7, zorder=2))
        for ch in nd['children']:
            walk(ch)

SPAN = {id(tree): (0.0, 2 * np.pi, 0)}
walk(tree)

# ---------------------------------------------------------------- 三个注释环
def ring(r_in, r_out, colors, lw=0.3, ec='white'):
    hw = np.pi / N * 0.96
    for j, nm in enumerate(order):
        a = np.degrees(ang[nm])
        ax.add_patch(Wedge((0, 0), r_out, a - np.degrees(hw), a + np.degrees(hw),
                           width=r_out - r_in, facecolor=colors[j],
                           edgecolor=ec, lw=lw, zorder=2))

ring(0.605, 0.665, [TYPE_COL[leaf2type[t]] for t in order])
ring(0.690, 0.752, [leaf2ph[t][1] for t in order])
ring(0.777, 0.860, [OCC_COL[leaf2occ[t]] for t in order], ec='#BBBBBB')

for txt, r in [('Type', 0.635), ('Phylum', 0.721), ('Presence', 0.818)]:
    a = -0.30
    ax.text(r * np.cos(a), r * np.sin(a), txt, rotation=-90, ha='center',
            va='center', fontsize=6.5, style='italic')

ax.set_xlim(-1.0, 1.0); ax.set_ylim(-1.0, 1.0)
ax.set_aspect('equal'); ax.axis('off')

# ---------------------------------------------------------------- 右侧三组图例
ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.axis('off')

def block(y0, title, entries, colors=None, marker='sq', fs=6.5, dy=0.028):
    ax2.text(0.02, y0, title, fontsize=8, va='top', fontweight='normal')
    y = y0 - 0.045
    for k_i, label in enumerate(entries):
        if colors is None:
            col, lab = label[1], label[0]
        else:
            col, lab = colors[k_i], label
        if marker == 'sq':
            ax2.add_patch(plt.Rectangle((0.03, y - 0.018), 0.030, 0.024,
                                        facecolor=col, edgecolor='#999999', lw=0.4))
        else:
            ax2.plot([0.045], [y - 0.006], 'o', ms=4.5, color=col)
        ax2.text(0.075, y - 0.006, lab, fontsize=fs, va='center')
        y -= dy
    return y

y = block(0.99, 'Genome Type', [('WGS', TYPE_COL['WGS']), ('MAG', TYPE_COL['MAG']),
                                ('SAG', TYPE_COL['SAG'])])
y = block(y - 0.035, 'Occurrence in samples',
          [('Present in >=10 photic samples', OCC_COL[0]),
           ('Present in at least 1 photic', OCC_COL[1]),
           ('Absent from photic samples', OCC_COL[2])])
y = block(y - 0.035, 'Phylum (Top 10)',
          ['%s (N=%d)' % (nm, ncnt) for nm, _c, _k, ncnt in PHYLUM],
          colors=[c for _n, c, _k, _nc in PHYLUM])

save(fig, 'case_seg012.png')
