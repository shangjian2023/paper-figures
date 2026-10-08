# -*- coding: utf-8 -*-
"""案例74 - Nature 堆积柱形图(一): 百分比堆积柱 + 段上误差棒 + 显著性支架。
参考: frames/seg_072.jpg — 两组(B6 low / B6 high)×7 基因型,
黑 M+0 / 青 M+1 / 粉 M+2 堆积至 100%, 顶部 ****/ns 支架, 斜体斜排 X 标签。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

set_style()

geno = [r'$\it{WT}$', r'$\it{+ev}$', r'$\it{+A38}$-$\it{WT}$', r'$\it{+A38}$-$\it{R134C}$',
        r'$\it{SFXN1}^{-/-}$', r'$\it{SHMT1}^{-/-}$', r'$\it{SHMT2}^{-/-}$']

r = rng(72)
# 每列 6 个重复 → 均值/SEM (三段)
m0_mean = np.array([22, 23, 25, 23, 26, 30, 32, 23, 31, 32, 31, 28, 31, 45], float)
m1_mean = np.array([77, 40, 73, 23, 43, 68, 66, 60, 58, 60, 60, 22, 67, 5], float)
m2_mean = 100 - m0_mean - m1_mean

ncol = 14
reps = 6
m0 = np.clip(m0_mean[:, None] + r.normal(0, 2.0, (ncol, reps)), 0, 100)
m1 = np.clip(m1_mean[:, None] + r.normal(0, 2.0, (ncol, reps)), 0, 100)
m2 = np.clip(m2_mean[:, None] + r.normal(0, 1.5, (ncol, reps)), 0, 100)
tot = m0 + m1 + m2
m0, m1, m2 = m0 / tot * 100, m1 / tot * 100, m2 / tot * 100

c0, c1, c2 = 'black', '#1F9E89', '#F4A6BE'

xs = np.array([0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14], float)
fig, ax = plt.subplots(figsize=cm2in(19, 13))
w = 0.72

sem0, sem1, sem2 = m0.std(1, ddof=1), m1.std(1, ddof=1), m2.std(1, ddof=1)
mean0, mean1, mean2 = m0.mean(1), m1.mean(1), m2.mean(1)

ax.bar(xs, mean0, width=w, color=c0, edgecolor='black', lw=0.6, zorder=3)
ax.bar(xs, mean1, bottom=mean0, width=w, color=c1, edgecolor='black', lw=0.6, zorder=3)
ax.bar(xs, mean2, bottom=mean0 + mean1, width=w, color=c2, edgecolor='black', lw=0.6,
       zorder=3)
# 每段误差棒
for k in range(ncol):
    ax.errorbar(xs[k], mean0[k], yerr=sem0[k], fmt='none', ecolor='black',
                elinewidth=1.1, capsize=3, capthick=1.1, zorder=4)
    ax.errorbar(xs[k], mean0[k] + mean1[k], yerr=sem1[k], fmt='none', ecolor='black',
                elinewidth=1.1, capsize=3, capthick=1.1, zorder=4)
    ax.errorbar(xs[k], mean0[k] + mean1[k] + mean2[k], yerr=sem2[k], fmt='none',
                ecolor='black', elinewidth=1.1, capsize=3, capthick=1.1, zorder=4)

ax.set_ylim(0, 122)
ax.set_yticks([0, 25, 50, 75, 100])
ax.set_ylabel('Fraction of total (%)', fontsize=9)
ax.set_xticks(xs)
ax.set_xticklabels(geno * 2, rotation=45, ha='right', rotation_mode='anchor', fontsize=8)
ax.set_xlim(-0.8, 14.8)

# 顶部显著性支架
bracket = lambda x1, x2, y, t: sig_bracket(ax, x1, x2, y, t, lw=0.9, fontsize=8)
bracket(-0.18, 1.18, 108, '****')
bracket(0.82, 2.18, 108, 'ns')
bracket(2.82, 4.18, 104, '****')
bracket(3.82, 5.18, 104, 'ns')
bracket(4.82, 6.18, 104, '****')
bracket(7.82, 9.18, 108, 'ns')
bracket(8.82, 10.18, 108, 'ns')
bracket(10.82, 12.18, 104, '****')
bracket(11.82, 13.18, 104, 'ns')
bracket(12.82, 14.18, 104, '****')

# 底部分组括号与标签(axes 外)
def under_bracket(x1, x2, y, label=None, fs=8.5):
    ax.plot([x1, x1, x2, x2], [y, y - 1.6, y - 1.6, y], lw=0.9, color='black',
            clip_on=False)
    if label:
        ax.text((x1 + x2) / 2, y - 2.6, label, ha='center', va='top', fontsize=fs,
                clip_on=False)

for x1, x2 in ((0.6, 3.4), (8.6, 11.4)):
    under_bracket(x1, x2, -28, r'$\it{SLC25A38}^{-/-}$', 8.5)
under_bracket(-0.4, 6.4, -47)
under_bracket(7.6, 14.4, -47)
ax.text(3.0, -53.5, 'B6 low', ha='center', va='top', fontsize=10, clip_on=False)
ax.text(11.0, -53.5, 'B6 high', ha='center', va='top', fontsize=10, clip_on=False)

# 左侧图例
leg = ax.legend(handles=[Patch(fc=c2, ec='black', lw=0.5, label='D2-TTP (M+2)'),
                         Patch(fc=c1, ec='black', lw=0.5, label='D1-TTP (M+1)'),
                         Patch(fc=c0, ec='black', lw=0.5, label='TTP (M+0)')],
                loc='center left', bbox_to_anchor=(-0.30, 0.42), frameon=False,
                fontsize=8.5, handlelength=1.5, handleheight=1.2)

fig.subplots_adjust(left=0.14, right=0.985, top=0.96, bottom=0.40)
save(fig, 'case_seg072.png')
