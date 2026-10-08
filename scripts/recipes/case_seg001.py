# -*- coding: utf-8 -*-
"""案例1 - Nature 柱形图: 柱 + 抖动散点 + 显著性横线 (Nature 风格)。
参考: frames/seg_001.jpg — 3 组柱(黑描边/绿描边), 柱内散点, *** 与 ns 括号。"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paper_style import (set_style, save, rng, sig_bracket, p_to_stars,
                         italic_gene, cm2in)

import numpy as np
import matplotlib.pyplot as plt

set_style()

groups = ['Cont', 'pcna', 'foxj1a']
n = [13, 8, 15]
means = [205, 75, 55]
r = rng(42)
data = [r.normal(m, s, k).clip(5, 400) for m, s, k in
        zip(means, [65, 45, 25], n)]

colors = ['black', '#1B7837', '#1B7837']
fig, ax = plt.subplots(figsize=cm2in(7.6, 7.0))
xs = np.arange(len(groups))
for i, d in enumerate(data):
    face = 'white' if i == 0 else 'none'
    ax.bar(xs[i], d.mean(), width=0.62, facecolor=face, edgecolor=colors[i],
           linewidth=1.6, zorder=2)
    sem = d.std(ddof=1) / np.sqrt(len(d))
    ax.errorbar(xs[i], d.mean(), yerr=sem, fmt='none', ecolor=colors[i],
                elinewidth=1.2, capsize=4, capthick=1.2, zorder=3)
    jit = rng(100 + i).uniform(-0.18, 0.18, len(d))
    ax.scatter(xs[i] + jit, d, s=16, color=colors[i], zorder=4, alpha=0.85)

ax.set_xticks(xs)
ax.set_xticklabels([italic_gene(g) if g != 'Cont' else g for g in groups], fontsize=9)
ax.set_ylabel('# INL PCNA+ cells / 300 um')
ax.set_ylim(0, 400)
ax.set_yticks([0, 100, 200, 300, 400])
ax.set_xlim(-0.6, 2.6)

sig_bracket(ax, 0.62, 1.38, 335, '***')
sig_bracket(ax, -0.38, 2.38, 380, '***')
sig_bracket(ax, 1.62, 2.38, 255, 'ns')

save(fig, 'case_seg001.png')
