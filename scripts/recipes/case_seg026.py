# -*- coding: utf-8 -*-
"""案例26 - Nature 分组散点图: 5粒径组半透明散点 + 黑菱形均值±SD + theory虚线。
参考: frames/seg_026.jpg — 蓝/浅蓝/绿/黄/橙, Energy(eV) vs Lifetime(ps)。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

# 组: (名称, 颜色, n, 中心E, 中心L, sdE, sdL)
specs = [
    ('7 nm',  '#4A89C8', 42, 2.418, 545, 0.014, 85),
    ('9 nm',  '#A9D2EE', 45, 2.380, 360, 0.013, 75),
    ('13 nm', '#4FBA85', 55, 2.362, 325, 0.011, 75),
    ('16 nm', '#E9C74E', 30, 2.352, 265, 0.008, 50),
    ('23 nm', '#D8793C', 35, 2.338, 170, 0.007, 45),
]

r = rng(26)
fig, ax = plt.subplots(figsize=cm2in(12.0, 12.0))

means = []
for name, c, n, mu_e, mu_l, sd_e, sd_l in specs:
    # 截断采样避免组间过度重叠
    e, l = [], []
    while len(e) < n:
        cand = r.multivariate_normal([mu_e, mu_l], [[sd_e ** 2, 0], [0, sd_l ** 2]], n * 2)
        ok = cand[(abs(cand[:, 0] - mu_e) < 2.2 * sd_e) & (abs(cand[:, 1] - mu_l) < 2.4 * sd_l)]
        need = n - len(e)
        e += list(ok[:need, 0]); l += list(ok[:need, 1])
    e, l = np.array(e), np.array(l)
    ax.scatter(e, l, s=110, color=c, alpha=0.55, edgecolors='none', zorder=3)
    means.append((e.mean(), l.mean(), e.std(ddof=1), l.std(ddof=1)))

# 均值菱形 + XY误差棒(SD)
for me, ml, se, sl in means:
    ax.errorbar(me, ml, xerr=se, yerr=sl, fmt='D', color='black', ms=9,
                elinewidth=1.4, capsize=0, mec='black', mfc='black', zorder=5)

# theory 虚线
xt = np.array([2.331, 2.447])
ax.plot(xt, 90 + 5250 * (xt - 2.331), ls='--', lw=2.2, color='black',
        dashes=(6, 3), zorder=2)

ax.set_xlim(2.308, 2.462)
ax.set_ylim(55, 715)
ax.set_xticks(np.arange(2.32, 2.451, 0.02))
ax.set_yticks(np.arange(100, 701, 100))
ax.set_xlabel('Energy (eV)', fontsize=10)
ax.set_ylabel('Lifetime (ps)', fontsize=10)

# 图例(左上, 带边框)
handles = [plt.Line2D([], [], ls='--', lw=2.2, color='black', label='theory')]
handles += [plt.Line2D([], [], marker='o', ls='', ms=8, color=c, alpha=0.8,
                       label=name) for name, c, *_ in specs]
handles.append(plt.Line2D([], [], marker='D', ls='', ms=8, color='black',
                          label='mean'))
ax.legend(handles=handles, loc='upper left', frameon=True, edgecolor='black',
          framealpha=1.0, fontsize=9, borderaxespad=0.4, labelspacing=0.45,
          handletextpad=0.5)

save(fig, 'case_seg026.png')
