# -*- coding: utf-8 -*-
"""案例6 - Nature 分组柱形图: 4基因 x 3基因型 柱 + 空心圆散点 + 竖排P值。
参考: frames/seg_006.jpg — 黑/橙/青三基因型, 柱顶±SEM, 右侧 Day15 图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, rng, cm2in, italic_gene

import numpy as np
import matplotlib.pyplot as plt

set_style()

genes = ['ubq-1', 'ubq-2', 'ubl-1', 'usp-14']
genos = ['Wild-type', 'eat-2(ad1116)', 'daf-2(e1370)']
cols = ['#3A3A3A', '#E8891C', '#2BA6A2']

means = np.array([[1.00, 0.65, 0.38],
                  [0.95, 0.71, 0.69],
                  [1.11, 0.68, 1.13],
                  [1.09, 0.94, 0.90]])
sds = np.array([[0.22, 0.20, 0.12],
                [0.18, 0.16, 0.18],
                [0.14, 0.20, 0.22],
                [0.12, 0.20, 0.16]])
r = rng(6)
data = [[r.normal(means[g, k], sds[g, k], 9).clip(0.02, 2.4)
         for k in range(3)] for g in range(4)]

# 每个基因上方的竖排 P 值 (genotype 索引 -> 文本), 与参考图一致
plabels = [{0: 'P = 0.035', 2: 'P = 1e-04'},
           {0: 'P = 0.292 (NS)', 1: 'P = 0.059 (NS)'},
           {1: 'P = 0.009', 2: 'P = 0.877 (NS)'},
           {1: 'P = 0.341 (NS)', 2: 'P = 0.171 (NS)'}]

fig, ax = plt.subplots(figsize=cm2in(12.5, 9.5))
offs = [-0.30, 0.0, 0.30]
w = 0.28
for g in range(4):
    for k in range(3):
        d = data[g][k]
        x = g + offs[k]
        ax.bar(x, d.mean(), width=w, facecolor=cols[k], edgecolor='black',
               linewidth=0.8, zorder=2)
        sem = d.std(ddof=1) / np.sqrt(len(d))
        ax.errorbar(x, d.mean(), yerr=sem, fmt='none', ecolor='black',
                    elinewidth=1.0, capsize=3.5, capthick=1.0, zorder=3)
        jit = rng(60 + 10 * g + k).uniform(-0.09, 0.09, len(d))
        ax.scatter(x + jit, d, s=22, facecolor='white', edgecolor='black',
                   linewidth=0.9, zorder=4)
        if k in plabels[g]:
            y0 = max(d.mean() + sem, d.max()) + 0.10
            ax.text(x, y0, plabels[g][k], rotation=90, ha='center',
                    va='bottom', fontsize=7.5)

ax.set_xticks(np.arange(4))
ax.set_xticklabels([italic_gene(g) for g in genes], fontsize=11)
ax.set_ylabel('Relative_mRNA levels', fontsize=11)
ax.set_ylim(0, 2.55)
ax.set_yticks(np.arange(0, 2.6, 0.5))
ax.set_xlim(-0.62, 3.62)
ax.tick_params(axis='both', labelsize=9)

handles = [plt.Rectangle((0, 0), 1, 1, facecolor=c, edgecolor='black',
                         linewidth=0.8) for c in cols]
leg = ax.legend(handles, genos, loc='upper left', bbox_to_anchor=(1.02, 1.0),
                frameon=False, fontsize=9, title='Day15', handlelength=1.2,
                handleheight=1.1, borderaxespad=0.0)
leg.get_title().set_fontsize(10)

save(fig, 'case_seg006.png')
