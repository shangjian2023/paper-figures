# -*- coding: utf-8 -*-
"""案例123 - Nature 带显著性的小提琴图(三): 实色小提琴 + 虚线轮廓小提琴
叠加 (未来情景), 实线中位/虚线四分位, 红点划零线, North/South 两面板。
参考: frames/seg_123.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy.stats import gaussian_kde

set_style()

events = ['Cold Surge', 'Sandstorm', 'Typhoon', 'Gale', 'Heatwave',
          'Rainstorm', 'Blizzard']
solid_c = ['#B08888', '#F0C080', '#A8A8A8', '#3BA888', '#E86868',
           '#A8C8E8', '#E8B8C8']
dash_c = ['#C8A8A8', '#F8E0B8', '#C8C8C8', '#88C8B0', '#F0A8A8',
          '#C0D8F0', '#F0D0DC']
# 每事件 (实色: mu, sd) / (虚线: mu, sd); South 的 Sandstorm 实色小而居中
north = [((22, 28), (28, 42)), ((28, 38), (40, 55)), ((5, 22), (30, 38)),
         ((18, 24), (22, 34)), ((8, 30), (16, 44)), ((14, 22), (18, 32)),
         ((30, 30), (38, 46))]
south = [((-5, 22), (2, 30)), ((-2, 12), (18, 34)), ((-8, 22), (8, 32)),
         ((-8, 20), (0, 34)), ((-10, 26), (0, 40)), ((-5, 20), (0, 30)),
         ((-2, 16), (4, 24))]

fig, axes = plt.subplots(2, 1, figsize=cm2in(16.5, 14.0),
                         gridspec_kw=dict(hspace=0.42, left=0.10,
                                          right=0.985, top=0.94, bottom=0.075))
r = rng(123)


def violin_pair(ax, xc, sp, dp, c_s, c_d, width=0.30):
    """虚线轮廓小提琴(未来) + 实色小提琴(现在), 错开叠加。"""
    pairs = [(dp, 0.07, 'dash')] if sp is None else \
            [(dp, 0.07, 'dash'), (sp, -0.05, 'solid')]
    for (mu, sd), dx, style in pairs:
        vals = r.normal(mu, sd, 240)
        vals = vals[(vals > mu - 3.2 * sd) & (vals < mu + 3.2 * sd)]
        k = gaussian_kde(vals)
        grid = np.linspace(vals.min(), vals.max(), 130)
        w = width * k(grid) / k(grid).max()
        xL, xR = xc + dx - w, xc + dx + w
        ys = np.concatenate([grid, grid[::-1]])
        xs = np.concatenate([xL, xR[::-1]])
        if style == 'solid':
            ax.fill(xs, ys, facecolor=c_s, edgecolor='black', lw=0.9,
                    zorder=3)
            md, q1, q3 = np.percentile(vals, [50, 25, 75])
            kmd = width * k(md) / k(grid).max()
            kq1 = width * k(q1) / k(grid).max()
            kq3 = width * k(q3) / k(grid).max()
            ax.plot([xc + dx - kmd, xc + dx + kmd], [md, md], c='black',
                    lw=1.1, zorder=4)
            for q, kq in [(q1, kq1), (q3, kq3)]:
                ax.plot([xc + dx - kq, xc + dx + kq], [q, q], c='black',
                        lw=0.9, ls=(0, (3, 2)), zorder=4)
        else:
            ax.plot(xs, ys, c='black', lw=0.9, ls=(0, (2.5, 2)), zorder=2)


for pi, (ax, data, ylab_top) in enumerate(zip(
        axes, [north, south], [160, 120])):
    for ei, ev in enumerate(events):
        sp, dp = data[ei]
        violin_pair(ax, ei, sp, dp, solid_c[ei], dash_c[ei])
    ax.axhline(0, c='#C02020', ls=(0, (6, 2, 1, 2)), lw=1.2, zorder=1)
    ax.set_xlim(-0.6, 6.6)
    ax.set_xticks(np.arange(7))
    ax.set_xticklabels(events, fontsize=9)
    if pi == 0:
        ax.set_ylim(-58, 236)
        ax.set_yticks([-40, 0, 40, 80, 120, 160])
        ax.set_yticklabels(['-40%', '0%', '40%', '80%', '120%', '160%'],
                           fontsize=8.5)
        ax.set_title('North', fontsize=10.5)
    else:
        ax.set_ylim(-95, 128)
        ax.set_yticks([-80, -40, 0, 40, 80, 120])
        ax.set_yticklabels(['-80%', '-40%', '0%', '40%', '80%', '120%'],
                           fontsize=8.5)
        ax.set_title('South', fontsize=10.5)
        # 2050 / 2020 注记 (Typhoon)
        ax.annotate('2050', xy=(2.28, 62), xytext=(1.45, 46),
                    fontsize=8.5, va='center',
                    arrowprops=dict(arrowstyle='-', lw=0.7, color='black'))
        ax.annotate('2020', xy=(1.88, -22), xytext=(1.45, -38),
                    fontsize=8.5, va='center',
                    arrowprops=dict(arrowstyle='-', lw=0.7, color='black'))
    ax.set_ylabel('Projected change (%)', fontsize=8.5)
    ax.tick_params(length=3)
    despine(ax)

# 图例: 实色=2020 现状, 虚线轮廓=2050 预估
leg_h = [Patch(facecolor='#B8B8B8', edgecolor='black', lw=0.9,
               label='2020 observed (filled)'),
         Patch(facecolor='none', edgecolor='black', lw=0.9,
               ls=(0, (2.5, 2)), label='2050 projected (outline)')]
axes[0].legend(handles=leg_h, loc='upper left', ncol=2, frameon=False,
               fontsize=8, handlelength=1.5, columnspacing=1.0,
               borderaxespad=0.1)

save(fig, 'case_seg123.png')
