# -*- coding: utf-8 -*-
"""案例8 - Nature 分组柱形图: 7变体x4条件柱 + 竖排P值 + FC=1虚线。
参考: frames/seg_008.jpg — 深灰/浅灰/蓝/橙, 空心圆点, 顶部横排图例框。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, rng, cm2in

import numpy as np
import matplotlib.pyplot as plt

set_style()

variants = ['WT', 'L713F', 'L698A', 'L701A', 'L765A', 'L768A', 'L698A/\nL701A']
conds = ['-DOX', 'DMSO', '10 nM veliparib', r'1 $\mu$M veliparib']
cols = ['#6E6E6E', '#CCCCCC', '#4C5FBF', '#E87722']

# 每变体 x 每条件的均值
means = np.array([
    [1.0, 1.0, 1.35, 1.35],
    [1.0, 1.0, 1.75, 5.15],
    [1.0, 1.0, 1.45, 1.85],
    [1.0, 1.0, 1.45, 1.55],
    [1.0, 1.0, 2.55, 4.25],
    [1.0, 1.0, 3.15, 6.85],
    [1.0, 1.0, 2.45, 4.25],
])
# 蓝/橙两列的竖排 P 值 (灰柱无标注)
plabels = [['0.7718', '0.6848'],
           ['0.4231', '<0.0001'],
           ['0.6782', '0.3609'],
           ['0.6916', '0.6481'],
           ['0.0423', '<0.0001'],
           ['0.0048', '<0.0001'],
           ['0.0716', '<0.0001']]

r = rng(8)
fig, ax = plt.subplots(figsize=cm2in(17, 11))
w = 0.20
for v in range(7):
    for k in range(4):
        base = means[v, k]
        sd = 0.06 if k < 2 else (0.35 if k == 2 else 0.28 * base / 4 + 0.12)
        n = 2 if k < 2 else 3
        d = r.normal(base, sd, n).clip(0.02 if k < 2 else 0.3, None)
        x = v + (k - 1.5) * (w + 0.015)
        ax.bar(x, d.mean(), width=w, facecolor=cols[k], edgecolor='black',
               linewidth=0.8, zorder=2)
        sem = d.std(ddof=1) / np.sqrt(len(d))
        ax.errorbar(x, d.mean(), yerr=sem, fmt='none', ecolor='black',
                    elinewidth=1.0, capsize=3, capthick=1.0, zorder=3)
        ax.scatter(np.full(len(d), x), d, s=20, facecolor='white',
                   edgecolor='black', linewidth=0.9, zorder=4)
        if k >= 2:
            ptxt = ('P=' + plabels[v][k - 2]) if plabels[v][k - 2][0] != '<' \
                else ('P<' + plabels[v][k - 2][1:])
            ax.text(x, d.mean() + sem + 0.18, ptxt, rotation=90, ha='center',
                    va='bottom', fontsize=6.8)

ax.axhline(1.0, color='black', linestyle='--', linewidth=1.0, zorder=1)
ax.set_xticks(np.arange(7))
ax.set_xticklabels(variants, fontsize=10)
ax.set_xlabel('PARP1 variant', fontsize=12)
ax.set_ylabel('PARP1-GFP FC', fontsize=12)
ax.set_ylim(0, 10.4)
ax.set_xlim(-0.55, 6.55)
ax.tick_params(axis='y', labelsize=9)

handles = [plt.Rectangle((0, 0), 1, 1, facecolor=c, edgecolor='black',
                         linewidth=0.8) for c in cols]
leg = ax.legend(handles, conds, loc='lower left', bbox_to_anchor=(0.0, 1.01),
                ncol=4, frameon=True, edgecolor='black', fontsize=9,
                handlelength=1.4, handleheight=1.1, borderaxespad=0.35)
leg.get_frame().set_linewidth(0.8)
leg.get_frame().set_boxstyle('round', pad=0.4, rounding_size=0.5)

save(fig, 'case_seg008.png')
