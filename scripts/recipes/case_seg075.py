# -*- coding: utf-8 -*-
"""案例77 - Plant Bio. J. 相关性矩阵图 + 拟合散点。
(a) 4×4 pairs: 对角直方图+KDE, 上三角色块 R²/P 文本, 下三角灰点+红虚线拟合;
(b) 右列 4 个年份散点带方程。
参考: frames/seg_075.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

set_style()

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

vars_ = ['AAC', 'PC', 'LC', 'TV']
vcolor = ['#d62f2f', '#4daf4a', '#eeb422', '#7b52ab']
yr = rng(75).uniform(1970, 2030, 200)
rr = rng(175)
tv = 55 + 0.3035 * (yr - 2000) + rr.normal(0, 14, 200)
aac = 15.5 - 0.26 * (tv - 58) + rr.normal(0, 4.2, 200)
pc = 8 - 0.0086 * (yr - 2000) + rr.normal(0, 1.2, 200)
lc = 1.4 - 0.0005 * (yr - 2000) + rr.normal(0, 0.25, 200)
D = np.clip(np.column_stack([aac, pc, lc, tv]),
            [0.5, 0.5, 0.1, 5], [26.5, 11.5, 2.0, 88])

pairs = {(0, 1): ('0.0063', '0.3135', 'ns'),
         (0, 2): ('0.0010', '0.6924', 'ns'),
         (0, 3): ('0.6024', '< 0.0001', '****'),
         (1, 2): ('0.0052', '0.3605', 'ns'),
         (1, 3): ('0.1041', '< 0.0001', '****'),
         (2, 3): ('0.0016', '0.6180', 'ns')}
block_fc = {(0, 1): '#e8e697', (0, 2): '#77c17d', (0, 3): '#d66a6a',
            (1, 2): '#c2c24e', (1, 3): '#e2b168', (2, 3): '#77c17d'}
eqs = [('y = \u22120.1783x + 373.5', 'R$^2$ = 0.1897   ****', (0, 27), (0, 9, 18, 27)),
       ('y = \u22120.0086x + 25.316', 'R$^2$ = 0.0097   ns', (0, 12), (0, 4, 8, 12)),
       ('y = \u22120.0005x + 2.4625', 'R$^2$ = 0.0004   ns', (0, 2.1), (0, 0.7, 1.4, 2.1)),
       ('y = 0.3035x \u2212 543.51', 'R$^2$ = 0.1308   ****', (0, 90), (0, 30, 60, 90))]

fig = plt.figure(figsize=cm2in(19.0, 16.5))
gs = fig.add_gridspec(4, 5, width_ratios=[1, 1, 1, 1, 1.18],
                      hspace=0.10, wspace=0.10,
                      left=0.075, right=0.975, top=0.945, bottom=0.075)
axes = [[fig.add_subplot(gs[i, j]) for j in range(4)] for i in range(4)]
axb = [fig.add_subplot(gs[i, 4]) for i in range(4)]

def fit_line(x, y):
    k, b = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 10)
    return xs, k * xs + b

lims = [(0, 27), (0, 12), (0, 2.1), (0, 90)]
for i in range(4):
    for j in range(4):
        ax = axes[i][j]
        if i == j:                                   # 对角: 直方图 + KDE
            cnt, _, _ = ax.hist(D[:, i], bins=15, color=vcolor[i], zorder=2)
            kde = gaussian_kde(D[:, i])
            xs = np.linspace(D[:, i].min(), D[:, i].max(), 120)
            ax.plot(xs, kde(xs) / kde(xs).max() * cnt.max() * 0.98,
                    color='black', lw=0.9, zorder=3)
            ax.set_ylim(0, cnt.max() * 1.30)
        elif j > i:                                  # 上三角: 色块 + 文本
            ax.set_facecolor(block_fc[(j - 3, j)] if False else block_fc[(i, j)])
            r2, pv, st = pairs[(i, j)]
            ax.text(0.5, 0.72, '$R^2$ = ' + r2, transform=ax.transAxes,
                    ha='center', va='center', fontsize=7)
            p_pre = '$P$ ' if pv[0] in '<>' else '$P$ = '
            ax.text(0.5, 0.47, p_pre + pv, transform=ax.transAxes,
                    ha='center', va='center', fontsize=7)
            ax.text(0.5, 0.22, st, transform=ax.transAxes, ha='center',
                    va='center', fontsize=7)
        else:                                        # 下三角: 散点 + 拟合
            ax.scatter(D[:, j], D[:, i], s=5, color='#b0b0b0', alpha=0.65,
                       linewidths=0, zorder=2)
            xs, ys = fit_line(D[:, j], D[:, i])
            ax.plot(xs, ys, color='#d62f2f', ls='--', lw=1.0, zorder=3)
        ax.set_xlim(*lims[j])
        if i != j:
            ax.set_ylim(*lims[i])
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_linewidth(0.7)
        if i == 3:
            ax.set_xticks([(lims[j][0] + lims[j][1]) / 2])
            ax.set_xticklabels([vars_[j]], fontsize=7.5)
        if j == 0:
            ax.set_yticks([(lims[i][0] + lims[i][1]) / 2])
            ax.set_yticklabels([vars_[i]], fontsize=7.5)

# (b) 右列: 年份散点 + 方程
for i in range(4):
    ax = axb[i]
    eq, r2t, ylim_, ytk = eqs[i]
    ax.scatter(yr, D[:, i], s=7, color=vcolor[i], alpha=0.85,
               linewidths=0, zorder=2)
    xs, ys = fit_line(yr, D[:, i])
    ax.plot(xs, ys, color='black', ls='--', lw=1.0, zorder=3)
    ax.set_xlim(1970, 2030)
    ax.set_ylim(*ylim_)
    ax.set_yticks(ytk)
    ax.set_xticks([1970, 2000, 2030])
    ax.tick_params(labelsize=6.5, length=2)
    ax.text(0.03, 0.90, eq, transform=ax.transAxes, ha='left', va='top',
            fontsize=6.5)
    ax.text(0.03, 0.74, r2t, transform=ax.transAxes, ha='left', va='top',
            fontsize=6.5)
    if i == 3:
        ax.set_xlabel('Year', fontsize=7.5)
    else:
        ax.set_xticklabels([])
    despine(ax)

fig.text(0.022, 0.955, '(a)', fontsize=10, fontweight='bold')
fig.text(0.70, 0.955, '(b)', fontsize=10, fontweight='bold')

save(fig, 'case_seg075.png')
