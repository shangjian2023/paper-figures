# -*- coding: utf-8 -*-
"""案例42 - Nature 柱状图: 5 柱 + 斜线纹理 + 误差棒 + 样本点 + 星号。
参考: frames/seg_042.jpg — Cyp3a11 相对表达, 灰/白/棕黄/白/绿柱,
柱上散点同色, ** 与 * 显著性, X 标签 45°。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

labels = ['Vehicle', '50 μM', '100 μM', '50 μM', '100 μM']
r = rng(42)
# 每组 6 个重复 (参考图每组 3-4 点, 此处按规范取 6)
group_means = [0.72, 1.87, 1.02, 1.71, 1.20]
group_sds = [0.13, 0.55, 0.18, 0.25, 0.15]
data = [r.normal(m, s, 6).clip(0.2, 3.0) for m, s in zip(group_means, group_sds)]

fills = ['#8C8C8C', 'white', '#B8860B', 'white', '#5CB85C']
hatches = ['///', None, '///', None, '///']
dot_cols = ['#8C8C8C', '#B8860B', '#B8860B', '#5CB85C', '#5CB85C']
stars = {1: '**', 3: '*'}

fig, ax = plt.subplots(figsize=cm2in(9.5, 11.5))
xs = np.arange(5)
for i, d in enumerate(data):
    ax.bar(xs[i], d.mean(), width=0.68, facecolor=fills[i], edgecolor='black',
           linewidth=1.5, hatch=hatches[i], zorder=2)
    sem = d.std(ddof=1) / np.sqrt(len(d))
    ax.errorbar(xs[i], d.mean(), yerr=sem, fmt='none', ecolor='black',
                elinewidth=1.4, capsize=5, capthick=1.4, zorder=4)
    jit = r.uniform(-0.13, 0.13, len(d))
    ax.scatter(xs[i] + jit, d, s=42, color=dot_cols[i], zorder=5,
               edgecolor='none', alpha=0.95)

# 星号偏移为 ylim 相对量(换数据/换量纲无需重算); 需要 ylim 已设好, 故先 set_ylim 再标注
ax.set_ylim(0, 3)
ax.set_yticks([0, 1, 2, 3])
_y0, _y1 = ax.get_ylim()
_star_h = (_y1 - _y0) * 0.075
_star_fs = 8 * (_y1 - _y0) / 3.0 * (13 / 8) * 3.0 / (_y1 - _y0)  # = 13pt @ 满量程 3
for xi, st in stars.items():
    ytop = data[xi].mean() + data[xi].std(ddof=1) / np.sqrt(len(data[xi]))
    ax.text(xs[xi], ytop + _star_h * 0.35, st, ha='center', va='bottom',
            fontsize=13, fontweight='bold')

ax.set_ylabel(r'$\it{Cyp3a11}$ expression (norm. to $\it{Gapdh}$)', fontsize=9)
ax.set_xticks(xs)
ax.set_xticklabels(labels)
plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor',
         fontsize=9)
ax.set_xlim(-0.65, 4.65)

save(fig, 'case_seg042.png')
