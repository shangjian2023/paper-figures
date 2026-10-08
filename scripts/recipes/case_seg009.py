# -*- coding: utf-8 -*-
"""案例9 - Nature 双Y轴图: 17样本并列双柱, 左轴蓝OD600 / 右轴米色浓度 (twinx)。
参考: frames/seg_009.jpg — 红/蓝横向阈值线, 顶部图例, p<0.05。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, rng, cm2in

import numpy as np
import matplotlib.pyplot as plt

set_style()

samples = ['Srdi-'] + ['Srdi-idt%i' % i for i in range(1, 17)]
od = np.array([0.68, 1.45, 1.00, 1.60, 1.75, 1.20, 1.20, 1.30, 1.20, 1.50,
               1.35, 0.95, 0.90, 1.15, 1.30, 1.70, 1.60])
conc = np.array([118., 145., 142., 152., 163., 138., 145., 148., 140., 150.,
                 145., 140., 136., 140., 142., 158., 150.])

r = rng(9)
n = 17
x = np.arange(n)
od_rep = np.array([r.normal(m, 0.09, 3).clip(0.05, None) for m in od])
co_rep = np.array([r.normal(m, 6.0, 3).clip(20, None) for m in conc])

BLUE = '#AEC6E8'
BEIGE = '#E3E0B0'
fig, ax = plt.subplots(figsize=cm2in(18, 10.5))
ax2 = ax.twinx()

b1 = ax.bar(x - 0.19, od_rep.mean(axis=1), width=0.36, facecolor=BLUE,
            edgecolor='black', linewidth=0.7, zorder=2,
            yerr=od_rep.std(axis=1, ddof=1) / np.sqrt(3),
            error_kw=dict(ecolor='black', elinewidth=1.0, capsize=3,
                          capthick=1.0))
b2 = ax2.bar(x + 0.19, co_rep.mean(axis=1), width=0.36, facecolor=BEIGE,
             edgecolor='black', linewidth=0.7, zorder=2,
             yerr=co_rep.std(axis=1, ddof=1) / np.sqrt(3),
             error_kw=dict(ecolor='black', elinewidth=1.0, capsize=3,
                           capthick=1.0))
# 散点
for i in range(n):
    ax.scatter(np.full(3, x[i] - 0.19), od_rep[i], s=12, color='black',
               zorder=4)
    ax2.scatter(np.full(3, x[i] + 0.19), co_rep[i], s=12, color='black',
                zorder=4)

# 阈值线
ax.axhline(1.9, color='#D9603B', lw=1.2, zorder=3)
ax.axhline(0.7, color='#4C72B0', lw=1.2, zorder=3)

ax.set_ylim(0, 3)
ax2.set_ylim(0, 170)
ax.set_yticks(np.arange(0, 3.1, 1))
ax2.set_yticks(np.arange(0, 171, 50))
ax.set_ylabel('Indigoidine (OD$_{600}$)', fontsize=11)
ax2.set_ylabel('Daptomycin (\u03bcg/ml)', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(samples, rotation=45, ha='right', fontsize=9,
                   fontstyle='italic')
ax.tick_params(axis='y', labelsize=9)
ax2.tick_params(axis='y', labelsize=9)
ax.set_xlim(-0.7, n - 0.3)

# 边框 (参考图为全框)
for sp in ('top', 'right'):
    ax.spines[sp].set_visible(True)
    ax2.spines[sp].set_visible(True)

ax.text(0.015, 0.97, r'$\mathit{p}$<0.05', transform=ax.transAxes,
        fontsize=10, ha='left', va='top')
handles = [plt.Rectangle((0, 0), 1, 1, facecolor=BLUE, edgecolor='black',
                         linewidth=0.7),
           plt.Rectangle((0, 0), 1, 1, facecolor=BEIGE, edgecolor='black',
                         linewidth=0.7)]
leg = ax.legend(handles, ['Indigoidine', 'Daptomycin'], loc='upper center',
                bbox_to_anchor=(0.5, 1.02), ncol=2, frameon=False, fontsize=10,
                handlelength=1.6, handleheight=1.1)

save(fig, 'case_seg009.png')
