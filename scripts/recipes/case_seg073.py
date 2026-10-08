# -*- coding: utf-8 -*-
"""案例75 - Nature 堆积柱形图(二): 6 时间块 × 3 处理纵向堆积柱。
参考: frames/seg_073.jpg — % of hCD45+ 堆积(红/橙/蓝/黄 + 后期品红),
每段误差棒, 块间点状竖虚线, 块标题在上, X 标签斜排。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

blocks = ['4wks', '8wks', '12wks', '16wks', '20wks', '24wks']
treats = ['unedited', 'GFP gRNA', 'TB48+ TB50']
r = rng(73)

# 每块基线: [红, 橙, 蓝, 黄, 品红]
base = {
    0: [30, 12, 56, 1.5, 0],
    1: [12, 2.5, 84, 1.0, 0],
    2: [11, 2.0, 85.5, 1.0, 0],
    3: [10, 2.0, 84, 2.0, 1.5],
    4: [16, 2.0, 71, 1.0, 10],
    5: [18, 2.5, 62, 1.5, 14],
}
colors = ['#B94A48', '#E67E22', '#85C1E9', '#F1C40F', '#DF3FE3']

ncol = 18
reps = 6
props = np.zeros((ncol, reps, 5))
for b in range(6):
    for t in range(3):
        k = b * 3 + t
        for rep in range(reps):
            vals = np.array(base[b]) * r.normal(1, 0.16, 5)
            vals = np.clip(vals, 0, None)
            props[k, rep] = vals / vals.sum() * 100

means = props.mean(1)
sems = props.std(1, ddof=1) / np.sqrt(reps)

xs = np.arange(ncol, dtype=float)
fig, ax = plt.subplots(figsize=cm2in(20, 13))
w = 0.78

bottom = np.zeros(ncol)
for j in range(5):
    ax.bar(xs, means[:, j], bottom=bottom, width=w, color=colors[j],
           edgecolor='black', lw=0.5, zorder=3)
    ax.errorbar(xs, bottom + means[:, j], yerr=sems[:, j], fmt='none',
                ecolor='black', elinewidth=0.9, capsize=2.5, capthick=0.9, zorder=4)
    bottom += means[:, j]

ax.set_ylim(0, 118)
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_ylabel('% of hCD45$^+$', fontsize=9)
ax.set_xlim(-0.8, ncol - 0.2)

# 块间点状竖虚线
for b in range(1, 6):
    ax.axvline(b * 3 - 0.5, ls=':', color='black', lw=1.3, zorder=2)

# 块标题
for b, name in enumerate(blocks):
    ax.text(b * 3 + 1, 110, name, ha='center', va='bottom', fontsize=10)

labels = treats * 6
ax.set_xticks(xs)
ax.set_xticklabels(labels, rotation=40, ha='right', rotation_mode='anchor',
                   fontsize=7.5)

# 图例: 5 个亚群, 图外顶部横排
from matplotlib.patches import Patch
subsets = ['CD3$^+$ T cells', 'CD19$^+$ B cells', 'CD33$^+$ myeloid',
           'CD56$^+$ NK cells', 'CD34$^+$ progenitors']
handles = [Patch(facecolor=colors[j], edgecolor='black', lw=0.5,
                 label=subsets[j]) for j in range(5)]
fig.legend(handles=handles, loc='upper center', ncol=5, frameon=False,
           fontsize=7.5, bbox_to_anchor=(0.53, 1.0), handlelength=1.3,
           columnspacing=1.1, handletextpad=0.4)

fig.subplots_adjust(left=0.075, right=0.985, top=0.895, bottom=0.17)
save(fig, 'case_seg073.png')
