# -*- coding: utf-8 -*-
"""案例71 - Nature 差异云雨图(三): 水平云雨图 × 2 面板, 配对灰/黑线连接,
KS 与 Wilcoxon P 值注记, 右侧图例 (Result / TNM)。
参考: frames/seg_071.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter

set_style()

panels = [
    dict(top='#8898C8', bot='#D89098', ks='6.66 × 10$^{-16}$', wil='4 × 10$^{-12}$'),
    dict(top='#88B878', bot='#F0B060', ks='6.74 × 10$^{-16}$', wil='4 × 10$^{-12}$'),
]

fig = plt.figure(figsize=cm2in(16.0, 13.5))
gs = fig.add_gridspec(2, 2, width_ratios=[3.1, 1.05], height_ratios=[1, 1],
                      hspace=0.55, wspace=0.06,
                      left=0.09, right=0.99, top=0.86, bottom=0.10)
axes = [fig.add_subplot(gs[i, 0]) for i in range(2)]
axleg = fig.add_subplot(gs[:, 1])
axleg.axis('off')

# 总标题
fig.text(0.40, 0.945, 'Distance between macrophage_\n'
         r'VIM$^+$ cells and T$_{\mathrm{reg}}$ cells',
         ha='center', va='top', fontsize=10.5, linespacing=1.4)

for pi, (pp, ax) in enumerate(zip(panels, axes)):
    r = rng(71 + pi)
    n = 300
    d_top = r.gamma(1.6, 190, n).clip(15, 1720)
    d_bot = r.gamma(1.8, 210, n).clip(15, 1750)
    y_top, y_bot = 1.0, 0.0

    for d, y0, c, up in [(d_top, y_top, pp['top'], True),
                         (d_bot, y_bot, pp['bot'], False)]:
        k = gaussian_kde(d)
        xs = np.linspace(0, 1750, 300)
        h = 0.42 * k(xs) / k(xs).max()
        if up:
            ax.fill(xs, y0 + h, color=c, lw=0, zorder=2)
            ax.plot(xs, y0 + h, color=c, lw=0.6, zorder=3)
        else:
            ax.fill(xs, y0 - h, color=c, lw=0, zorder=2)
            ax.plot(xs, y0 - h, color=c, lw=0.6, zorder=3)
        # 箱线 (小, 白底) + 基线散点阵雨
        ax.boxplot(d, positions=[y0], widths=0.055, orientation='horizontal',
                   whis=(0, 100), patch_artist=True, manage_ticks=False,
                   boxprops=dict(facecolor='white', edgecolor='black', lw=0.9),
                   medianprops=dict(color='black', lw=1.4),
                   whiskerprops=dict(color='black', lw=0.8),
                   capprops=dict(color='black', lw=0.8),
                   showfliers=False, zorder=5)
        jit = r.normal(0, 0.006, len(d))
        ax.scatter(d, y0 + jit, s=1.6, color='#2A2A2A', alpha=0.55,
                   linewidths=0, zorder=4)
    # 配对连接线: 前 12 个个体, 两端补圆点 (显著=黑实心, NS=灰空心)
    for j in range(12):
        sig = abs(d_top[j] - d_bot[j]) < 280
        c = 'black' if sig else '#B8B8B8'
        ax.plot([d_top[j], d_bot[j]], [y_top - 0.015, y_bot + 0.015],
                c=c, lw=0.8, zorder=1)
        if sig:
            ax.scatter([d_top[j], d_bot[j]], [y_top - 0.015, y_bot + 0.015],
                       s=17, c='black', linewidths=0, zorder=6)
        else:
            ax.scatter([d_top[j], d_bot[j]], [y_top - 0.015, y_bot + 0.015],
                       s=15, facecolors='none', edgecolors='#A0A0A0',
                       linewidths=0.9, zorder=6)
    # 检验注记
    ax.text(980, 0.74, 'Kolmogorov–Smirnov\n'
            f'test: P = {pp["ks"]}', ha='left', va='center', fontsize=8,
            linespacing=1.4)
    ax.text(980, 0.26, 'Wilcoxon signed-rank\n'
            f'test: P = {pp["wil"]}', ha='left', va='center', fontsize=8,
            linespacing=1.4)
    ax.set_xlim(-60, 1820)
    ax.set_ylim(-0.62, 1.62)
    ax.set_yticks([])
    ax.set_ylabel('Group', fontsize=10)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{int(v):,}'))
    if pi == 1:
        ax.set_xticks([0, 500, 1000, 1500])
        ax.set_xlabel('Distance (pixels)', fontsize=10)
        ax.tick_params(labelsize=8.5)
    else:
        ax.set_xticks([])

# 右侧图例: 每面板一组 (Result + TNM)
axleg.set_xlim(0, 1)
axleg.set_ylim(0, 1)
for pi, pp in enumerate(panels):
    yb = 0.97 - pi * 0.52
    axleg.text(0.06, yb, 'Result', fontsize=10)
    axleg.scatter([0.10], [yb - 0.07], s=22, color='#B8B8B8', edgecolors='none')
    axleg.text(0.17, yb - 0.07, 'NS', fontsize=9, va='center')
    axleg.scatter([0.10], [yb - 0.13], s=22, color='#1A1A1A', edgecolors='none')
    axleg.text(0.17, yb - 0.13, r'$P$ < 0.05', fontsize=9, va='center')
    axleg.text(0.06, yb - 0.23, 'TNM', fontsize=10)
    axleg.add_patch(plt.Rectangle((0.06, yb - 0.325), 0.09, 0.055,
                                  facecolor=pp['bot'], edgecolor='none'))
    axleg.text(0.17, yb - 0.30, 'Stages III & IV', fontsize=9, va='center')
    axleg.add_patch(plt.Rectangle((0.06, yb - 0.395), 0.09, 0.055,
                                  facecolor=pp['top'], edgecolor='none'))
    axleg.text(0.17, yb - 0.37, 'Stages I & II', fontsize=9, va='center')

save(fig, 'case_seg071.png')
