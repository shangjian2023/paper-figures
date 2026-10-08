# -*- coding: utf-8 -*-
"""案例29 - Cell 分面小提琴图: 3 面板, 灰 Reference vs 彩色 Specialized。
参考: frames/seg_029.jpg — 顶部彩色标题条, 面板底色渐变, 中位数/四分位虚线, P 值括号。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.colors import LinearSegmentedColormap

set_style()

panels = [
    dict(title='Very ancient\n(> 473 mya)', tcolor='#17A2B8', vcolor='#1B8FA6',
         grad='#BFE4EC', ptxt='P = 1.18e-30', ylim=(0.76, 0.88), yticks=[0.76, 0.78, 0.80, 0.82, 0.84, 0.86, 0.88],
         ref=(0.782, 0.004), spec=(0.842, 0.005)),
    dict(title='Ancient\n(111-473 mya)', tcolor='#9B7BB8', vcolor='#8E6BAE',
         grad='#E0D4EC', ptxt='P = 6.04e-7', ylim=(0.10, 0.18), yticks=[0.10, 0.12, 0.14, 0.16, 0.18],
         ref=(0.152, 0.005), spec=(0.130, 0.007)),
    dict(title='Recent/very recent\n(0-111 mya)', tcolor='#D9534F', vcolor='#D0453F',
         grad='#F8DCC8', ptxt='P = 3.80e-33', ylim=(0, 0.08), yticks=[0, 0.02, 0.04, 0.06, 0.08],
         ref=(0.064, 0.003), spec=(0.027, 0.003)),
]

fig, axes = plt.subplots(1, 3, figsize=cm2in(17.5, 9.0))

for ax, pp in zip(axes, panels):
    # 面板底色: 底部彩色 -> 顶部白 的渐变
    cmap = LinearSegmentedColormap.from_list('g', ['white', pp['grad']])
    grad = np.linspace(1, 0, 256).reshape(-1, 1)
    ax.imshow(grad, extent=[-0.5, 1.5, *pp['ylim']], aspect='auto',
              cmap=cmap, origin='lower', zorder=0, alpha=0.85)
    r = rng(29)
    for xi, (mu, sd), fc, ec in [
            (0, pp['ref'], '#8C8C8C', '#6E6E6E'),
            (1, pp['spec'], pp['vcolor'], pp['vcolor'])]:
        vals = r.normal(mu, sd, 300)
        k = gaussian_kde(vals)
        grid = np.linspace(vals.min(), vals.max(), 120)
        w = 0.30 * k(grid) / k(grid).max()
        ax.fill(np.concatenate([xi - w, (xi + w)[::-1]]),
                np.concatenate([grid, grid[::-1]]),
                facecolor=fc, edgecolor=ec, lw=0.9, zorder=2, alpha=0.95)
        # 中位数虚线 + 四分位点线
        q1, md, q3 = np.percentile(vals, [25, 50, 75])
        wq1 = 0.30 * k(q1) / k(grid).max()
        wq3 = 0.30 * k(q3) / k(grid).max()
        wmd = 0.30 * k(md) / k(grid).max()
        ax.plot([xi - wmd, xi + wmd], [md, md], ls=(0, (4, 2)), c='black',
                lw=0.9, zorder=3)
        for q, wq in [(q1, wq1), (q3, wq3)]:
            ax.plot([xi - wq, xi + wq], [q, q], ls=':', c='black', lw=0.9,
                    zorder=3)
    # P 值 + 短横线
    ytop, rng_ = pp['ylim'][1], pp['ylim'][1] - pp['ylim'][0]
    ax.plot([0, 1], [ytop - 0.13 * rng_] * 2, c='black', lw=0.8)
    it = r'$\it{P}$'
    pval = pp['ptxt'].split('= ')[1]
    ax.text(0.5, ytop - 0.025 * rng_, f'{it} = {pval}',
            ha='center', va='top', fontsize=8.5)
    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(*pp['ylim'])
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Reference', 'Specialized\nfor diapause'],
                       rotation=45, ha='right', fontsize=8)
    ax.set_yticks(pp['yticks'])
    ax.set_ylabel('Fraction of total paralogs', fontsize=8.5)
    for sp in ax.spines.values():
        sp.set_visible(True)
    ax.tick_params(length=3)
    # 顶部彩色标题条
    ax.text(0.5, 1.16, pp['title'], transform=ax.transAxes, ha='center',
            va='bottom', color='white', fontsize=8.5, linespacing=1.25,
            bbox=dict(boxstyle='square,pad=0.45', fc=pp['tcolor'], ec='none'))

fig.subplots_adjust(wspace=0.55, bottom=0.24, top=0.80)
save(fig, 'case_seg029.png')
