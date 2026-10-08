# -*- coding: utf-8 -*-
"""案例30 - Cell 分面箱线图: 4 面板, 灰 Reference vs 彩色 Specialized。
参考: frames/seg_030.jpg — 顶部彩色标题条, 面板底色渐变, P 值横线, X 标签斜排。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

set_style()

panels = [
    dict(title='Genome-Wide\n(all ages)', tcolor='#8C8C8C', vcolor='#3B7DD8',
         grad='#DEDEDE', ptxt='P = 2.2e-16', ref=(0.17, 0.09), spec=(0.15, 0.07)),
    dict(title='Very ancient\n(> 473 mya)', tcolor='#17A2B8', vcolor='#17B8A6',
         grad='#C8E8F0', ptxt='P = 2.12e-04', ref=(0.18, 0.07), spec=(0.17, 0.06)),
    dict(title='Ancient\n(111-473 mya)', tcolor='#9B7BB8', vcolor='#9B72C8',
         grad='#E4D8F0', ptxt='P = 9.779e-9', ref=(0.18, 0.08), spec=(0.15, 0.07)),
    dict(title='Recent/very recent\n(0-111 mya)', tcolor='#D9534F', vcolor='#E05252',
         grad='#F8DCC8', ptxt='P = 0.0619', ref=(0.52, 0.20), spec=(0.46, 0.18)),
]

# 先生成全部数据, 统一 y 量程 = 全体数据 max x 1.1 (同一指标跨面板可比)
r = rng(30)
data = [[r.normal(*pp['ref'], 260), r.normal(*pp['spec'], 260)] for pp in panels]
GMAX = max(v.max() for row in data for v in row)
YTOP = GMAX * 1.1
yticks = np.arange(0, YTOP + 1e-9, 0.2)

fig, axes = plt.subplots(1, 4, figsize=cm2in(17.5, 7.5))

for ax, pp, row in zip(axes, panels, data):
    cmap = LinearSegmentedColormap.from_list('g', ['white', pp['grad']])
    grad = np.linspace(1, 0, 256).reshape(-1, 1)
    ax.imshow(grad, extent=[-0.5, 1.5, 0, YTOP], aspect='auto',
              cmap=cmap, origin='lower', zorder=0, alpha=0.85)
    ytop = YTOP
    rng_ = YTOP
    for xi, vals, fc in [(0, row[0], '#B8B8B8'),
                         (1, row[1], pp['vcolor'])]:
        vals = vals.clip(0, ytop - 0.17 * rng_)
        ax.boxplot(vals, positions=[xi], widths=0.42, patch_artist=True,
                   boxprops=dict(facecolor=fc, edgecolor='black', lw=0.9),
                   medianprops=dict(color='black', lw=1.2),
                   whiskerprops=dict(color='black', lw=0.9),
                   capprops=dict(color='black', lw=0.9),
                   showfliers=False, zorder=2, manage_ticks=False)
    ax.plot([0, 1], [ytop - 0.13 * rng_] * 2, c='black', lw=0.8)
    it = r'$\it{P}$'
    txt = pp['ptxt']
    ax.text(0.5, ytop - 0.025 * rng_, txt.replace('P =', it + ' =', 1),
            ha='center', va='top', fontsize=8.5)
    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(0, YTOP)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Reference', 'Specialized\nfor diapause'],
                       rotation=45, ha='right', fontsize=8)
    ax.set_yticks(yticks)
    ax.set_ylabel('dN/dS between paralogs', fontsize=8.5)
    for sp in ax.spines.values():
        sp.set_visible(True)
    ax.tick_params(length=3)
    ax.text(0.5, 1.16, pp['title'], transform=ax.transAxes, ha='center',
            va='bottom', color='white', fontsize=8, linespacing=1.25,
            bbox=dict(boxstyle='square,pad=0.45', fc=pp['tcolor'], ec='none'))

fig.subplots_adjust(wspace=0.50, bottom=0.26, top=0.78)
save(fig, 'case_seg030.png')
