# -*- coding: utf-8 -*-
"""案例70 - Nature 差异云雨图(二): 背靠背半小提琴(淡紫/粉红) + 箱线 + 抖动散点,
** 与 **** 支架, 图例左上, Y=P_AD 0-1。
参考: frames/seg_070.jpg — MCI 与 DE 两组。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.patches import Patch

set_style()

r = rng(70)
groups = {
    'MCI': {'noad': r.normal(0.24, 0.09, 400).clip(0.02, 0.80),
            'ad':   r.normal(0.26, 0.13, 400).clip(0.02, 0.92)},
    'DE':  {'noad': r.normal(0.44, 0.09, 400).clip(0.10, 0.72),
            'ad':   r.normal(0.70, 0.09, 400).clip(0.30, 0.94)},
}
CL, CR = '#C8C4E0', '#E08A8A'   # 淡紫 / 粉红

fig, ax = plt.subplots(figsize=cm2in(14.0, 10.0))

for gi, (name, dd) in enumerate(groups.items()):
    xc = gi * 1.5 + 0.5          # MCI -> 0.5, DE -> 2.0
    noad, ad = dd['noad'], dd['ad']
    # 背靠背半小提琴 (共用中心线)
    for vals, color, side in [(noad, CL, -1), (ad, CR, +1)]:
        k = gaussian_kde(vals)
        grid = np.linspace(vals.min(), vals.max(), 150)
        w = 0.34 * k(grid) / k(grid).max()
        ax.fill(np.concatenate([[xc], xc + side * w, [xc]]),
                np.concatenate([[grid[0]], grid, [grid[-1]]]),
                facecolor=color, edgecolor='#555555', lw=0.6,
                alpha=0.9, zorder=2)
    # 双箱线 (左右并排) + 通体须线
    for vals, fc, off in [(noad, CL, -0.075), (ad, CR, +0.075)]:
        ax.boxplot(vals, positions=[xc + off], widths=0.11, patch_artist=True,
                   whis=(0, 100),
                   boxprops=dict(facecolor=fc, edgecolor='black', lw=0.8),
                   medianprops=dict(color='black', lw=1.1),
                   whiskerprops=dict(color='black', lw=0.7),
                   capprops=dict(color='black', lw=0.7),
                   showfliers=False, zorder=4, manage_ticks=False)
    # 抖动散点 (右侧, 两色混合)
    for vals, c in [(noad, '#9C96B8'), (ad, '#D06060')]:
        jit = r.uniform(0.14, 0.42, len(vals))
        ax.scatter(xc + jit, vals, s=3.5, color=c, alpha=0.55,
                   linewidths=0, zorder=3)
    # 显著性
    stars = '**' if name == 'MCI' else '****'
    sig_bracket(ax, xc - 0.16, xc + 0.30, 0.985, stars, h=0.02, fontsize=9)

# 图例左上
handles = [Patch(facecolor=CL, edgecolor='#777777'),
           Patch(facecolor=CR, edgecolor='#777777')]
leg = ax.legend(handles, ['No AD', 'AD as primary\nor contributing\nfactor'],
                loc='upper left', bbox_to_anchor=(0.01, 1.0), frameon=False,
                fontsize=8, handlelength=1.2, handleheight=1.0,
                labelspacing=0.9, borderaxespad=0)

ax.set_xlim(-0.15, 2.85)
ax.set_ylim(-0.06, 1.02)
ax.set_xticks([0.5, 2.0])
ax.set_xticklabels(['MCI', 'DE'], fontsize=10)
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_ylabel(r'$P_{AD}$', fontsize=10)
ax.tick_params(length=3)
despine(ax)

save(fig, 'case_seg070.png')
