# -*- coding: utf-8 -*-
"""案例33 - Nature 哑铃图: 左三段堆叠比例条 + 右水平哑铃。
参考: frames/seg_033.jpg — 每科灰色期望区间横杠 + 空心 Expected 圆 +
实心 Observed 圆连线; 绿=高于期望/深灰=区间内/黄=低于期望。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

set_style()

# (科名, 期望下限, 期望上限, 期望点, 观察值, 分类 a/b/w, 是否红名)
rows = [
    ('Serranidae',       5, 40, 18, 55, 'w', 0),
    ('Zoarcidae',        5, 30,  8, 26, 'a', 1),
    ('Myctophidae',      8, 28, 12, 32, 'a', 0),
    ('Sebastidae',       3, 20,  7, 16, 'a', 1),
    ('Liparidae',        4, 22,  9, 17, 'a', 1),
    ('Carangidae',       2, 26, 15, 20, 'w', 0),
    ('Scombridae',       2, 18,  6, 12, 'a', 0),
    ('Psychrolutidae',   1, 15,  8, 10, 'w', 0),
    ('Notothenioid',     1, 14,  5, 11, 'a', 1),
    ('Macrouridae',      1, 16, 10, 13, 'w', 0),
    ('Soleidae',         1, 12,  6,  9, 'w', 0),
    ('Pleuronectidae',   1, 10,  4,  8, 'a', 1),
    ('Paralichthyidae',  1, 10,  4,  8, 'a', 0),
    ('Sternoptychidae',  1, 10,  5,  7, 'w', 0),
    ('Ophidiidae',       1, 10,  5,  7, 'w', 0),
    ('Lutjanidae',       1,  9,  4,  6, 'w', 0),
    ('Sparidae',         1,  9,  4,  6, 'w', 0),
    ('Moridae',          1,  9,  4,  6, 'w', 0),
    ('Monacanthidae',    1,  9,  3,  5, 'w', 0),
    ('Agonidae',         1,  9,  3,  4, 'w', 0),
    ('Triglidae',        1,  9,  3,  4, 'w', 0),
    ('Platycephalidae',  1, 10,  3,  4, 'w', 0),
    ('Ophichthidae',     1, 10,  3,  4, 'w', 0),
    ('Antennariidae',    1, 10,  3,  3, 'w', 0),
    ('Holocentridae',    1, 10,  3,  3, 'w', 0),
    ('Bothidae',         1, 11,  3,  3, 'w', 0),
    ('Chaetodontidae',   1, 11,  2,  3, 'w', 0),
    ('Clupeidae',        2, 30,  9,  8, 'w', 0),
    ('Tetraodontidae',   1, 12,  2,  3, 'w', 0),
    ('Nemipteridae',     1, 11,  2,  2, 'w', 0),
    ('Muraenidae',       2, 22,  6,  8, 'w', 0),
    ('Mullidae',         1, 12,  2,  3, 'w', 0),
    ('Lethrinidae',      1, 11,  2,  2, 'w', 0),
    ('Balistidae',       1, 11,  2,  2, 'w', 0),
    ('Stomiidae',        1, 19,  4,  5, 'w', 0),
    ('Exocoetidae',      2, 10,  3,  1, 'b', 0),
    ('Acanthuridae',     2, 14,  3,  1, 'b', 0),
    ('Sciaenidae',       1, 14,  3,  3, 'w', 0),
    ('Syngnathidae',     1, 13,  3,  2, 'w', 0),
    ('Pomacanthidae',    2, 12,  3,  1, 'b', 0),
    ('Haemulidae',       1, 13,  2,  2, 'w', 0),
    ('Blenniidae',       1, 16,  3,  3, 'w', 0),
    ('Apogonidae',       3, 26,  6,  1, 'b', 0),
    ('Pomacentridae',    4, 37, 10,  1, 'b', 0),
    ('Gobiidae',         9, 60, 20,  8, 'b', 0),
    ('Labridae',        10, 70, 24,  9, 'b', 0),
]

r = rng(33)
n = len(rows)
ys = np.arange(n)[::-1]

c_shallow, c_inter, c_deep = '#BEE7E4', '#3D7EAA', '#123B5C'
c_above, c_within, c_below = '#00A878', '#4A4A4A', '#F0A500'
c_gray = '#D9D9D9'

fig, (axp, axd) = plt.subplots(
    1, 2, figsize=cm2in(17.5, 21), sharey=True,
    gridspec_kw={'width_ratios': [0.55, 1.6], 'wspace': 0.04})

for y, (name, lo, hi, ex, ob, cls, red) in zip(ys, rows):
    p1 = r.uniform(0.40, 0.75)
    p2 = r.uniform(0.12, 0.45)
    p3 = 1 - p1 - p2
    axp.barh(y, p1, left=0, height=0.72, color=c_shallow, edgecolor='white', lw=0.4)
    axp.barh(y, p2, left=p1, height=0.72, color=c_inter, edgecolor='white', lw=0.4)
    axp.barh(y, p3, left=p1 + p2, height=0.72, color=c_deep, edgecolor='white', lw=0.4)

    axd.barh(y, hi - lo, left=lo, height=0.42, color=c_gray, zorder=1)
    axd.plot([ex, ob], [y, y], color='#3A3A3A', lw=0.9, zorder=2)
    col = {'a': c_above, 'w': c_within, 'b': c_below}[cls]
    axd.scatter(ex, y, s=34, facecolor='white', edgecolor='black', lw=1.0, zorder=3)
    axd.scatter(ob, y, s=42, facecolor=col, edgecolor='none', zorder=4)

axp.set_yticks(ys)
axp.set_yticklabels([rr[0] for rr in rows], fontsize=7)
for lab, rr in zip(axp.get_yticklabels(), rows):
    if rr[5]:
        lab.set_color('#E8556D')
axp.set_xlim(0, 1.02)
axp.set_xticks([])
despine(axp, left=True, bottom=True)

axd.set_xlim(-2, 78)
axd.set_ylim(-0.9, n - 0.1 + 1.6)
axd.set_xlabel('Number of Transitions', fontsize=9)
axd.set_xticks([0, 20, 40, 60])
axd.tick_params(left=False)
despine(axd, left=True, bottom=False)

# 顶部注释: Expected / Observed transitions
y0 = n - 0.1 + 0.55
axd.annotate('Observed transitions', xy=(55, ys[0] + 0.12), xytext=(57, ys[0] + 1.05),
             fontsize=7.5, ha='center',
             arrowprops=dict(arrowstyle='->', lw=0.8, color='black',
                             connectionstyle='arc3,rad=-0.35'))
axd.plot([5, 40], [y0 + 0.28, y0 + 0.28], ls=':', color='black', lw=0.9)
axd.plot([5, 5], [y0 + 0.05, y0 + 0.28], ls=':', color='black', lw=0.9)
axd.plot([40, 40], [y0 + 0.05, y0 + 0.28], ls=':', color='black', lw=0.9)
axd.text(22, y0 + 0.42, 'Expected\ntransitions', fontsize=7.5, ha='center', va='bottom')

# 图例
leg1 = axp.legend(handles=[Patch(fc=c_shallow, label='Shallow'),
                           Patch(fc=c_inter, label='Intermediate'),
                           Patch(fc=c_deep, label='Deep')],
                  loc='lower left', bbox_to_anchor=(-0.02, -0.115), frameon=False,
                  fontsize=7.5, handlelength=1.4, handleheight=1.1, ncol=2,
                  columnspacing=1.0, borderpad=0.4)
leg2 = axd.legend(handles=[
    Line2D([], [], marker='o', ls='', mfc=c_above, mec='none', ms=6, label='Above expectation'),
    Line2D([], [], marker='o', ls='', mfc=c_within, mec='none', ms=6, label='Within expectation'),
    Line2D([], [], marker='o', ls='', mfc=c_below, mec='none', ms=6, label='Below expectation')],
    loc='lower right', bbox_to_anchor=(0.98, 0.10), frameon=False, fontsize=7.5)

fig.subplots_adjust(left=0.16, right=0.985, top=0.985, bottom=0.055)
save(fig, 'case_seg033.png')
