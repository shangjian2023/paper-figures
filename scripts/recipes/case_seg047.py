# -*- coding: utf-8 -*-
"""案例48(seg47) - Nature 散点饼图: 3个bla基因面板, 医院(45°斜排) x Inc类型网格,
每观测一个饼图(分色=物种, 饼径∝菌株数), 白底灰网格。参考: frames/seg_047.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Patch

set_style()

SPECIES = [('Klebsiella spp.', '#3ACC3A'),
           ('Enterobacter spp.', '#E040E0'),
           ('Escherichia coli', '#F5A623'),
           ('Citrobacter freundii', '#2244CC'),
           ('others', '#9A9A9A')]

hospitals = ['Okinawa-A', 'Kumamoto-A', 'Saga-A', 'Fukuoka-G', 'Fukuoka-E',
             'Fukuoka-D', 'Fukuoka-C', 'Fukuoka-B', 'Fukuoka-A', 'Kochi-A',
             'Ehime-A', 'Tokushima-A', 'Okayama-C', 'Okayama-B', 'Nara-A',
             'Hyogo-E', 'Hyogo-D', 'Hyogo-C', 'Hyogo-B', 'Hyogo-A', 'Osaka-E',
             'Osaka-B', 'Osaka-A', 'Mie-A']
NH = len(hospitals)

PANELS = [
    (r'$bla_{\rm KPC}$-like',
     ['C', 'FIA', 'FIA-N', 'FIA-R', 'FIB-FII', 'FII', 'I(pECLA)', 'HI2',
      'M1', 'M2', 'N', 'ND', 'others'], 34),
    (r'$bla_{\rm NDM}$-like',
     ['FIA-FIB-N', 'FIA-FII-N', 'FIB-N', 'HI2', 'N'], 11),
    (r'$bla_{\rm OXA}$-like',
     ['FIA-FIB-FIC', 'FIA-FIB-FII', 'FIB-FII', 'FII', 'X3'], 9),
]

r = rng(47)


def make_cells(n_cells, n_rows):
    cells = {}
    while len(cells) < n_cells:
        h = int(r.integers(0, NH))
        row = int(r.integers(0, n_rows))
        if (h, row) in cells:
            continue
        cnt = int(np.clip(r.exponential(3.2) + 1, 1, 13))
        comp = r.dirichlet([2.2, 1.8, 2.0, 1.2, 0.9])
        cells[(h, row)] = (cnt, comp)
    return cells


fig = plt.figure(figsize=cm2in(18.0, 15.0))
gs = fig.add_gridspec(3, 1, height_ratios=[13, 5, 5], hspace=0.14,
                      left=0.085, right=0.795, top=0.965, bottom=0.115)
axes = []
for pi, (blalab, rows, ncell) in enumerate(PANELS):
    ax = fig.add_subplot(gs[pi])
    axes.append(ax)
    ax.set_xlim(-0.7, NH - 0.3)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_xticks(range(NH))
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(rows, fontsize=7)
    ax.set_aspect('equal')
    ax.set_facecolor('white')
    ax.grid(True, color='#DCDCDC', lw=0.6, zorder=0)
    ax.tick_params(axis='both', length=2, width=0.7)
    if pi < 2:
        ax.tick_params(labelbottom=False)
    else:
        ax.set_xticklabels(hospitals, rotation=45, ha='right', fontsize=6.2)
    # 左侧 bla 基因竖排标签
    ax.text(-0.115, 0.5, blalab, transform=ax.transAxes, rotation=90,
            ha='right', va='center', fontsize=8.5)
    # 画饼
    for (h, row), (cnt, comp) in make_cells(ncell, len(rows)).items():
        rad = 0.17 + 0.30 * np.sqrt(cnt / 13.0)
        th1 = 90.0
        for si, frac in enumerate(comp):
            th2 = th1 + frac * 360.0
            ax.add_patch(Wedge((h, row), rad, th1, th2,
                               facecolor=SPECIES[si][1], edgecolor='black',
                               lw=0.45, zorder=3))
            th1 = th2
    for sp in ax.spines.values():
        sp.set_linewidth(0.9)

axes[0].text(-0.075, 1.045, 'Plasmid\nInc type', transform=axes[0].transAxes,
             ha='right', va='bottom', fontsize=8)
axes[2].text(-0.115, -0.90, 'Hospital', transform=axes[2].transAxes,
             ha='right', va='center', fontsize=8)

# ---------------- 图例(右侧) ----------------
leg_ax = fig.add_axes([0.815, 0.585, 0.18, 0.38])
leg_ax.axis('off')
for i, (name, c) in enumerate(SPECIES):
    yy = 0.96 - i * 0.135
    leg_ax.add_patch(plt.Rectangle((0.00, yy - 0.035), 0.10, 0.075,
                                   transform=leg_ax.transAxes, facecolor=c,
                                   edgecolor='black', lw=0.5, clip_on=False))
    leg_ax.text(0.15, yy, name, transform=leg_ax.transAxes, va='center',
                fontsize=7.5)
leg_ax.text(0.0, 0.28, 'Number of isolates', transform=leg_ax.transAxes,
            fontsize=7.5)
size_order = [('>=10', 13), ('7 - 9', 8), ('4 - 6', 5), ('1 - 3', 2.5)]
for i, (lab, cnt) in enumerate(size_order):
    xx = 0.10 + i * 0.27
    rad = 0.17 + 0.30 * np.sqrt(cnt / 13.0)
    leg_ax.scatter([xx], [0.10], s=(rad * 17) ** 2, facecolors='none',
                   edgecolors='black', linewidths=0.8,
                   transform=leg_ax.transAxes, clip_on=False)
    leg_ax.text(xx, -0.045, lab, transform=leg_ax.transAxes, ha='center',
                fontsize=6.8)

save(fig, 'case_seg047.png')
