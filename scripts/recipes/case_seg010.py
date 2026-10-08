# -*- coding: utf-8 -*-
"""案例10 - Nature 双Y轴图: GO 富集双轴柱线组合图。
参考: frames/seg_010.jpg — 20 个 GO 条目, 棕褐柱=基因数(左轴, 顶标数值),
绿色点虚线=-Log10(P)(右轴), X 标签 45°, 顶部图例框, 总标题。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

go_terms = [
    'defense response', 'response to biotic stimulus', 'response to other organism',
    'response to bacterium', 'external biotic stimulus', 'response to stress',
    'multi-organism process', 'cell wall organization', 'defense response to bacterium',
    'response to external stimulus', 'response to stimulus', 'RNA modification',
    'signal transduction', 'response to oxygen-containing compound', 'response to chemical',
    'carbohydrate metabolic process', 'response to hormone', 'response to abiotic stimulus',
    'response to endogenous stimulus', 'single-organism catabolic process',
]
counts = np.array([2138, 1472, 1124, 914, 1390, 1359, 3614, 776, 1498, 723,
                   1611, 4520, 792, 1700, 1143, 911, 1104, 1678, 816, 1611])
neglog10p = np.array([120, 65, 57, 56, 56, 55, 50, 47, 46, 43,
                      40, 35, 22, 20, 17, 15, 12, 9, 5, 3], dtype=float)

r = rng(10)
neglog10p = neglog10p + r.normal(0, 0.8, len(neglog10p)).clip(-2, 2)

tan = '#C99B6A'
edge = '#8A6238'
green = '#3E9B4F'

fig, ax = plt.subplots(figsize=cm2in(17.5, 12.5))
xs = np.arange(len(go_terms))
bars = ax.bar(xs, counts, width=0.62, color=tan, edgecolor=edge, linewidth=1.0,
              label='Gene count', zorder=2)

for x, c in zip(xs, counts):
    ax.text(x, c + 90, str(c), ha='center', va='bottom', fontsize=6.2, color='black')

ax.set_ylabel('Gene count', fontsize=9)
ax.set_ylim(0, 6000)
ax.set_yticks(np.arange(0, 6001, 1000))
ax.set_xlim(-0.7, len(go_terms) - 0.3)

# 右轴: -Log10(P)
ax2 = ax.twinx()
ax2.plot(xs, neglog10p, ls=':', color=green, lw=1.4, marker='o', markersize=5,
         markerfacecolor=green, markeredgecolor=green, zorder=3,
         label=r'$-$Log10 ($P$ value)')
ax2.set_ylabel(r'$-$Log10($P$ value)', fontsize=9)
ax2.set_ylim(0, 140)
ax2.set_yticks(np.arange(0, 141, 20))
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(True)
ax2.tick_params(right=True)

# 顶部图例框(双列, 带边框)
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
leg = ax.legend(h1 + h2, l1 + l2, loc='upper center', bbox_to_anchor=(0.5, 1.10),
                ncol=2, frameon=True, edgecolor='black', framealpha=1,
                fontsize=8, handlelength=2.2, borderpad=0.5, columnspacing=2.2)
leg.get_frame().set_linewidth(0.8)

ax.set_title('Enriched GO Terms in Biological Process (expanded gene families)',
             fontsize=9.5, pad=32)

ax.set_xticks(xs)
ax.set_xticklabels(go_terms)
plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor',
         fontsize=7)

fig.subplots_adjust(bottom=0.32, top=0.82)
save(fig, 'case_seg010.png')
