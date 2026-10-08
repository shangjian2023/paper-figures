# -*- coding: utf-8 -*-
"""案例7 - Nature 截断+分组柱形图: 断裂Y轴(0-2 / 1000-4000) 两段子图 + 斜断裂线。
参考: frames/seg_007.jpg — 2条件x3基因型, 灰/橙/蓝紫, 散点±SEM, *与n.s.括号。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, rng, cm2in, sig_bracket

import numpy as np
import matplotlib.pyplot as plt

set_style()

cols = ['#9C9C9C', '#E88C3A', '#8B85D1']
genos = ['Wild type', r'TbCSB $\mathit{\beta C1}$-line1',
         r'TbCSB $\mathit{\beta C1}$-line3']
r = rng(7)
# Control 组 (底部段, 0-2)
ctl = [[r.normal(1.00, 0.35, 6).clip(0.45, 1.55),
        r.normal(0.57, 0.15, 7).clip(0.25, 0.90),
        r.normal(0.70, 0.22, 7).clip(0.30, 1.25)]]
# 1.0 mM SA 组 (顶部段, >950)
# 同一组原始数: 柱=均值, 误差棒=SEM, 散点=原始值 -> 三者严格同源、目视一致
sa = [[r.normal(1620., 200., 8).clip(1280., 2020.),
       r.normal(1020., 55., 8).clip(930., 1150.),
       r.normal(1045., 65., 8).clip(940., 1190.)]]

fig, (ax1, ax2) = plt.subplots(
    2, 1, sharex=True, figsize=cm2in(10.5, 13),
    gridspec_kw={'height_ratios': [2.1, 1.5], 'hspace': 0.07})

offs = [-0.22, 0.0, 0.22]
w = 0.20


def draw_group(ax, xc, vals, colors, z0=2):
    for k, v in enumerate(vals):
        x = xc + offs[k]
        ax.bar(x, np.mean(v), width=w, facecolor=colors[k],
               edgecolor='black', linewidth=0.8, zorder=z0)
        sem = np.std(v, ddof=1) / np.sqrt(len(v))
        ax.errorbar(x, np.mean(v), yerr=sem, fmt='none', ecolor='black',
                    elinewidth=1.0, capsize=3.5, capthick=1.0, zorder=3)
        jit = rng(700 + int(xc * 10) + k).uniform(-0.06, 0.06, len(v))
        ax.scatter(x + jit, v, s=20, color=colors[k], edgecolor='white',
                   linewidth=0.5, zorder=4)


# Control -> 底部轴;  SA -> 两轴都画 (柱在底部被截, 顶部段显示)
draw_group(ax2, 0, ctl[0], cols)
for ax in (ax1, ax2):
    draw_group(ax, 1, sa[0], cols)

ax1.set_ylim(950, 3400)
ax1.set_yticks([1000, 2000, 3000])
ax2.set_ylim(0, 2.35)
ax2.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
ax1.set_xlim(-0.55, 1.55)

# 显著性
sig_bracket(ax2, -0.26, 0.26, 1.40, 'n. s.', fontsize=10)
sig_bracket(ax2, -0.02, 0.26, 0.98, '*', fontsize=10)
# SA 组托架: 跨所比较的两柱 (WT vs line1, WT vs line3), 落在顶部段数据上方
sig_bracket(ax1, 0.78, 1.02, 2250, '*', fontsize=10)
sig_bracket(ax1, 0.78, 1.26, 2850, '*', fontsize=10)

# 断裂斜线 (左侧脊柱处)
d = 0.012
kw = dict(marker=[(-1, -0.5), (1, 0.5)], markersize=11, linestyle='none',
          color='k', mec='k', mew=1.0, clip_on=False)
ax1.plot([0], [0], transform=ax1.transAxes, **kw)
ax2.plot([0], [1], transform=ax2.transAxes, **kw)
ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.tick_params(bottom=False)

ax1.legend(handles=[plt.Rectangle((0, 0), 1, 1, facecolor=c, edgecolor='black',
                                  linewidth=0.8) for c in cols],
           labels=genos, loc='lower left', bbox_to_anchor=(-0.04, 1.02),
           frameon=False, fontsize=10, handlelength=1.3, handleheight=1.1)

ax1.set_ylabel('Relative expression of\n' + r'$\mathit{PR1a}$', fontsize=12)
ax2.set_xticks([0, 1])
ax2.set_xticklabels(['Control', '1.0 mM SA'], fontsize=12)
ax1.tick_params(axis='y', labelsize=10)
ax2.tick_params(axis='both', labelsize=10)

save(fig, 'case_seg007.png')
