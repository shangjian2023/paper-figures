# -*- coding: utf-8 -*-
"""案例106 - Nature 分组 strip 散点: 8 细胞型 × 4 组, 空心=mock 实心=PCV13,
虚线分组隔线 + 均值短横线 + 显著性星号。
参考: frames/seg_104.jpg — dLN CD86 MFI。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()

cells = ['DC', 'cDC', 'cDC1', 'cDC2', 'pDC', 'mDC', 'CD11b$^+$', 'rDC']
BLUE, GREEN = '#3350B4', '#2CA02C'

# 每细胞型 4 组均值: GF mock, GF PCV13, SPF mock, SPF PCV13
mu = {'DC':        [950, 1500, 950, 2350],
      'cDC':       [1150, 1750, 1050, 2100],
      'cDC1':      [1100, 1150, 1050, 1300],
      'cDC2':      [1750, 1900, 1600, 2250],
      'pDC':       [150, 120, 130, 300],
      'mDC':       [3600, 3800, 3800, 4500],
      'CD11b$^+$': [3900, 3850, 3900, 4300],
      'rDC':       [600, 550, 550, 800]}
sd = {'DC': [230, 210, 180, 250], 'cDC': [200, 230, 220, 260],
      'cDC1': [180, 150, 130, 200], 'cDC2': [200, 260, 230, 310],
      'pDC': [55, 45, 50, 80], 'mDC': [330, 350, 320, 430],
      'CD11b$^+$': [420, 460, 380, 500], 'rDC': [90, 80, 85, 110]}
r = rng(104)

fig, ax = plt.subplots(figsize=cm2in(19.0, 10.5))
off = [-0.27, -0.09, 0.09, 0.27]         # 4 组亚位置
colors = [BLUE, BLUE, GREEN, GREEN]
filled = [False, True, False, True]

for i, c in enumerate(cells):
    base = i * 2.0
    for j in range(4):
        n = r.integers(7, 11)
        v = np.clip(r.normal(mu[c][j], sd[c][j], n), 20, 5800)
        xj = base + off[j]
        ax.scatter(np.full(n, xj) + r.uniform(-0.055, 0.055, n), v,
                   s=34, facecolor=colors[j] if filled[j] else 'none',
                   edgecolor=colors[j], linewidth=1.1, zorder=3)
        ax.plot([xj - 0.085, xj + 0.085], [v.mean()] * 2, color='black',
                lw=1.3, zorder=4)
    if i:
        ax.axvline(base - 1.0, ls=(0, (2, 2)), lw=1.0, color='black', zorder=2)

# ---- 显著性: 每组 GF mock vs GF PCV13
sig = [('DC', '**', 2750), ('cDC', '*', 2950), ('pDC', '**', 750),
       ('mDC', '*', 4850), ('rDC', '**', 1450)]
for c, st, y in sig:
    i = cells.index(c)
    sig_bracket(ax, i * 2.0 + off[0] - 0.08, i * 2.0 + off[1] + 0.08, y, st,
                h=55, fontsize=9)

h = [Line2D([], [], marker='o', ls='', mfc='none', mec=BLUE, ms=7, label='GF mock'),
     Line2D([], [], marker='o', ls='', mfc='none', mec=GREEN, ms=7, label='SPF mock'),
     Line2D([], [], marker='o', ls='', mfc=BLUE, mec=BLUE, ms=7, label='GF PCV13'),
     Line2D([], [], marker='o', ls='', mfc=GREEN, mec=GREEN, ms=7, label='SPF PCV13')]
ax.legend(handles=h, loc='upper left', bbox_to_anchor=(1.015, 1.0), fontsize=8.5,
          frameon=False, handletextpad=0.35, labelspacing=0.55, borderaxespad=0)

ax.set_xlim(-1.0, 15.0)
ax.set_ylim(0, 6000)
ax.set_xticks([i * 2.0 for i in range(8)])
ax.set_xticklabels(cells, fontsize=9, rotation=45, ha='right')
ax.set_yticks([0, 2000, 4000, 6000])
ax.set_yticklabels(['0', '2,000', '4,000', '6,000'])
ax.set_ylabel('dLN CD86 MFI', fontsize=9)
ax.tick_params(bottom=False)
ax.spines['bottom'].set_visible(False)

save(fig, 'case_seg104.png')
