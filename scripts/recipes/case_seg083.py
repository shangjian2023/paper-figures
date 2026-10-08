# -*- coding: utf-8 -*-
"""案例83 - Nature 小提琴 & NMDS 图: A 对数轴 4 小提琴(白中位点) + B/C
NMDS 散点 + 半透明凸包。
参考: frames/seg_083.jpg — Mimulus 属花香排放实验。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy.spatial import ConvexHull

set_style()

C_MVY, C_MVR = '#E8C830', '#E03030'
C_MCY, C_MCR = '#F0E868', '#9C1818'

fig = plt.figure(figsize=cm2in(15.5, 14.5))
gs = fig.add_gridspec(2, 6, hspace=0.45, wspace=0.55,
                      left=0.14, right=0.96, top=0.93, bottom=0.09)
axA = fig.add_subplot(gs[0, 1:5])
axB = fig.add_subplot(gs[1, 0:3])
axC = fig.add_subplot(gs[1, 3:6])

# ---------------- 面板 A: 对数轴小提琴 ----------------
r = rng(83)
groups = [('MvY', C_MVY, 17, 620, 120), ('MvR', C_MVR, 18, 270, 90),
          ('McY', C_MCY, 15, 4.6, 1.5), ('McR', C_MCR, 32, 2.6, 1.2)]
for i, (g, c, n, mu, sd) in enumerate(groups):
    vals = r.normal(mu, sd, n).clip(0.6, None)
    k = gaussian_kde(np.log10(vals))
    grid = np.linspace(vals.min() * 0.75, vals.max() * 1.25, 120)
    ld = np.log10(grid)
    w = 0.30 * k(ld) / k(ld).max()
    axA.fill(np.concatenate([i - w, (i + w)[::-1]]),
             np.concatenate([grid, grid[::-1]]),
             facecolor=c, edgecolor='black', lw=0.9, zorder=2)
    q1, md, q3 = np.percentile(vals, [25, 50, 75])
    axA.plot([i, i], [q1, q3], c='white', lw=1.4, zorder=3)
    axA.scatter([i], [md], s=22, c='white', edgecolors='black',
                linewidths=0.5, zorder=4)
# 物种内比较括号
axA.plot([0, 1], [60, 60], c='black', lw=0.8)
axA.text(0.5, 38, r'$\it{Mimulus}$ $\it{verbenaceus}$' + '\n'
         r'$\rho$ = 4.8e-8', ha='center', va='top', fontsize=8,
         linespacing=1.4)
axA.plot([2, 3], [7.5, 7.5], c='black', lw=0.8)
axA.text(2.5, 8.3, r'$\it{Mimulus}$ $\it{cardinalis}$' + '\n'
         r'$\rho$ = 0.002', ha='center', va='bottom', fontsize=8,
         linespacing=1.4)
axA.set_yscale('log')
axA.set_ylim(0.8, 1400)
axA.set_yticks([1, 5, 10, 50, 100, 500, 1000])
axA.set_yticklabels(['1', '5', '10', '50', '100', '500', '1000'], fontsize=8)
axA.set_xlim(-0.6, 3.6)
axA.set_xticks(range(4))
axA.set_xticklabels(['MvY', 'MvR', 'McY', 'McR'], fontsize=9)
axA.set_ylabel('Total volatile emissions (ng/(flower·hr)), log scale',
               fontsize=7.5)
axA.set_title('Total volatile emissions, log scale', fontsize=9.5,
              fontweight='bold', pad=6)
handles = [plt.Rectangle((0, 0), 1, 1, facecolor=c, edgecolor='black', lw=0.5)
           for _, c, n, _, _ in groups]
axA.legend(handles, ['MvY (n = 17)', 'MvR (n = 18)', 'McY (n = 15)',
                     'McR (n = 32)'], loc='upper right', fontsize=7.5,
           frameon=True, edgecolor='#BBBBBB', framealpha=0.9,
           handlelength=1.0, handleheight=1.0)

# ---------------- 面板 B/C: NMDS + 凸包 ----------------


def nmds_panel(ax, pts1, pts2, c1, c2, lab1, lab2, title, leg_loc):
    for pts, c in [(pts1, c1), (pts2, c2)]:
        hull = ConvexHull(pts)
        poly = pts[hull.vertices]
        ax.fill(poly[:, 0], poly[:, 1], facecolor=c, alpha=0.25,
                edgecolor=c, lw=1.0, zorder=1)
    ax.scatter(pts1[:, 0], pts1[:, 1], s=34, c=c1, edgecolors='black',
               linewidths=0.5, zorder=3)
    ax.scatter(pts2[:, 0], pts2[:, 1], s=34, c=c2, edgecolors='black',
               linewidths=0.5, zorder=3)
    ax.set_title(title, fontsize=9, fontweight='bold', style='italic', pad=5)
    ax.set_xlabel('NMDS1', fontsize=8.5)
    ax.set_ylabel('NMDS2', fontsize=8.5)
    ax.tick_params(labelsize=7.5)
    h = [plt.Line2D([], [], marker='o', ls='', color=c, markersize=6,
                    markeredgecolor='black', markeredgewidth=0.5)
         for c in (c1, c2)]
    ax.legend(h, [lab1, lab2], loc=leg_loc, fontsize=7.5, frameon=True,
              edgecolor='#BBBBBB', framealpha=0.9)


r2 = rng(830)
pts_mvr = np.column_stack([r2.normal(0.32, 0.19, 18), r2.normal(0.10, 0.16, 18)])
pts_mvy = np.column_stack([r2.normal(-0.33, 0.09, 17), r2.normal(-0.06, 0.09, 17)])
nmds_panel(axB, pts_mvr, pts_mvy, C_MVR, C_MVY,
           'MvR (n = 18)', 'MvY (n = 17)',
           'Mimulus verbenaceus: NMDS', 'upper left')
axB.set_xlim(-0.75, 0.90)
axB.set_ylim(-0.55, 0.72)

pts_mcr = np.column_stack([r2.normal(-0.30, 0.30, 32), r2.normal(0.10, 0.42, 32)])
pts_mcy = np.column_stack([r2.normal(0.78, 0.10, 15), r2.normal(-0.42, 0.14, 15)])
nmds_panel(axC, pts_mcr, pts_mcy, C_MCR, C_MCY,
           'McR (n = 32)', 'McY (n = 15)',
           'Mimulus cardinalis: NMDS', 'upper right')
axC.set_xlim(-1.15, 2.05)
axC.set_ylim(-1.25, 1.75)

for ax, letter in [(axA, 'A'), (axB, 'B'), (axC, 'C')]:
    panel_label(ax, letter, dx=-0.28 if ax is axA else -0.18, dy=1.02)

save(fig, 'case_seg083.png')
