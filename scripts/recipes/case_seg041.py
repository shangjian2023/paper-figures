# -*- coding: utf-8 -*-
"""案例41 - Nature 小提琴图: 3 面板 × 3 组, 半透明小提琴 + 空心抖动点
+ 均值横线 + SD 竖线 + y=0 虚线 + 顶部括号 P 值。
参考: frames/seg_041.jpg — 标题 5/10/20。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

set_style()

groups = ['Proband', 'Parent Het', 'Parent Ref']
fills = ['#F5C1C1', '#F8D5A0', '#C8E0F5']
edges = ['#E89494', '#E89140', '#7FB2D8']
darks = ['#D05050', '#D06010', '#2878B8']
# 每面板: 3 组 (mean, sd)
scenarios = [
    dict(title='5',  ps=[(0.20, 0.90), (-0.58, 0.70), (0.15, 0.95)],
         ptop='P = 0.95', pright='P = 0.007', pleft='P = 0.002'),
    dict(title='10', ps=[(0.20, 0.90), (-0.65, 0.70), (0.10, 0.95)],
         ptop='P = 0.81', pright='P = 7x10$^{-4}$', pleft='P = 1x10$^{-4}$'),
    dict(title='20', ps=[(0.25, 0.95), (-0.50, 0.75), (0.05, 1.00)],
         ptop='P = 0.2',  pright='P = 0.04',  pleft='P = 5x10$^{-4}$'),
]

fig, axes = plt.subplots(1, 3, figsize=cm2in(17.0, 8.5), sharey=True)
ylo, yhi = -2.4, 4.0

for ax, sc in zip(axes, scenarios):
    ax.set_facecolor('white')
    r = rng(41)
    for i, (mu, sd) in enumerate(sc['ps']):
        vals = r.normal(mu, sd, 60)
        k = gaussian_kde(vals)
        grid = np.linspace(vals.min(), vals.max(), 100)
        w = 0.34 * k(grid) / k(grid).max()
        ax.fill(np.concatenate([i - w, (i + w)[::-1]]),
                np.concatenate([grid, grid[::-1]]),
                facecolor=fills[i], edgecolor=edges[i], lw=1.0,
                alpha=0.55, zorder=2)
        jit = rng(90 + i).uniform(-0.16, 0.16, len(vals))
        ax.scatter(i + jit, vals, s=16, facecolors='none',
                   edgecolors=darks[i], alpha=0.45, linewidths=0.7, zorder=3)
        m, s = vals.mean(), vals.std(ddof=1)
        ax.plot([i - 0.24, i + 0.24], [m, m], c=darks[i], lw=3.2,
                solid_capstyle='butt', zorder=4)
        ax.plot([i, i], [m - s, m + s], c=darks[i], lw=2.2, zorder=4)
    ax.axhline(0, ls=(0, (5, 3)), c='#AAAAAA', lw=0.9, zorder=1)
    # 顶部括号 P 值
    sig_bracket(ax, -0.30, 2.30, 3.35, sc['ptop'], h=0.08, fontsize=8.5)
    sig_bracket(ax, 0.70, 2.30, 2.70, sc['pright'], h=0.08, fontsize=8.5)
    sig_bracket(ax, -0.30, 1.30, 2.05, sc['pleft'], h=0.08, fontsize=8.5)
    ax.set_xlim(-0.55, 2.55)
    ax.set_ylim(ylo, yhi)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(groups, rotation=45, ha='right', fontsize=8)
    ax.set_title('N risk variants: ' + sc['title'], fontsize=10, pad=4)
    for sp in ax.spines.values():
        sp.set_visible(True)
    ax.tick_params(length=3)

axes[0].set_yticks([-2, -1, 0, 1, 2, 3])
axes[0].set_ylabel('PGS Z-score', fontsize=9)

fig.subplots_adjust(wspace=0.18, bottom=0.24, top=0.90)
save(fig, 'case_seg041.png')
