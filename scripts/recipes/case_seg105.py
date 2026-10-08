# -*- coding: utf-8 -*-
"""案例107 - Nature 气泡网格图: x=18 皮层柱, y=18 抑制基序组, 气泡4档=Frac Syn,
颜色随皮层彩虹渐变, 灰竖线分层, 右侧尺寸图例。
参考: frames/seg_105.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()

layers = ['L2a', 'L2b', 'L2c', 'L3a', 'L3b', 'L4a', 'L4b', 'L4c', 'L5a',
          'L5b', 'L5E', 'L5N', 'L6s', 'L6c', r'L6t$\epsilon$', r'L6r$\epsilon$',
          r'L6t$\epsilon$', 'L6v']
lcolors = ['#5B8C3E', '#57A64B', '#8FD460', '#A98F2C', '#E8C93E', '#3F7FB5',
           '#4A90D9', '#A8C4E8', '#7C89C9', '#8E7CC3', '#6A4FA3', '#B9A8E0',
           '#C435A8', '#8E1A5B', '#C0392B', '#E8735A', '#E8862B', '#7B4EA3']
SEP = [2.5, 4.5, 7.5, 11.5, 13.5, 15.5]       # 分层灰竖线位置
r = rng(105)

# ---- 气泡: (层idx, 基序组, 尺寸档0-3), 集中在对角带
bubbles = [
    (0, 1, 3), (1, 1, 2), (2, 1, 1), (1, 2, 1), (0, 3, 1), (2, 2, 2),
    (3, 3, 2), (4, 3, 2), (3, 4, 1), (4, 4, 2), (2, 5, 1), (3, 6, 1),
    (4, 6, 1), (5, 4, 1), (6, 4, 2), (7, 4, 2), (6, 5, 1), (7, 5, 1),
    (5, 7, 3), (6, 7, 2), (7, 7, 1), (7, 8, 2), (8, 8, 2), (9, 8, 1),
    (8, 9, 1), (9, 9, 2), (10, 9, 3), (10, 10, 1), (11, 10, 2), (9, 11, 1),
    (11, 6, 1), (11, 12, 1), (12, 9, 1), (12, 13, 2), (13, 13, 1),
    (12, 14, 2), (13, 15, 2), (14, 13, 1), (14, 14, 1), (14, 15, 1),
    (15, 13, 1), (15, 14, 2), (15, 16, 2), (15, 15, 1), (16, 12, 1),
    (16, 13, 2), (16, 14, 1), (16, 16, 3), (16, 17, 1), (17, 15, 1),
    (17, 17, 3), (10, 2, 1), (6, 9, 2), (13, 14, 1), (5, 12, 1), (2, 8, 1),
    (0, 8, 1), (1, 8, 1), (8, 6, 1), (9, 10, 2)]

SIZE = [30, 90, 200, 380]      # <5% / 5-15% / 15-30% / >=30%
fig, ax = plt.subplots(figsize=cm2in(14.0, 13.5))

for li, mi, si in bubbles:
    ax.scatter(li + 1, mi, s=SIZE[si], color=lcolors[li], alpha=0.88,
               linewidths=0, zorder=3)

for xv in SEP:
    ax.axvline(xv, color='0.72', lw=0.9, zorder=1)

ax.set_xlim(0.3, 18.7)
ax.set_ylim(18.6, 0.4)                      # y 反转: 1 在顶
ax.set_xticks(range(1, 19))
ax.set_xticklabels(layers, rotation=90, fontsize=8)
ax.xaxis.tick_top()
ax.set_yticks(range(1, 19))
ax.tick_params(length=3)
ax.set_xlabel('Output fraction', fontsize=10, labelpad=8)
ax.set_ylabel('Inhibitory motif group', fontsize=10)
for sp in ('right', 'bottom'):
    ax.spines[sp].set_visible(False)
ax.spines['top'].set_position(('outward', 2))

h = [Line2D([], [], marker='o', ls='', markerfacecolor='black',
            markersize=np.sqrt(SIZE[k]) / 2, label=t)
     for k, t in enumerate(['<5%', '5-15%', '15-30%', '$\\geq$30%'])]
leg = ax.legend(handles=h, title='Frac Syn', loc='center left',
                bbox_to_anchor=(1.02, 0.45), frameon=False, fontsize=9,
                title_fontsize=10, labelspacing=1.15, handletextpad=1.0,
                borderaxespad=0)
leg._legend_box.align = 'left'

save(fig, 'case_seg105.png')
