# -*- coding: utf-8 -*-
"""案例39 - Cell 堆积柱形图: 双 100% 堆积条 + 右列 SHM rate 点图。
参考: frames/seg_039.jpg — 20 个 B 细胞簇 c01-c20; 左条 BCR isotype 8 色,
中条 SHM 3 水平, 右面板黑点 SHM rate 带浅灰网格; 图例右侧两组。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

set_style()

clusters = [
    'c01_Bn_TCL1A', 'c02_Bn_NR4A2', 'c03_Bn_IFN-response', 'c04_classical-Bm_TXNIP',
    'c05_classical-Bm_GPR183', 'c06_Bm_stress-response', 'c07_Bm_IFN-response',
    'c08_ABC_FCRL4', 'c09_ABC_FGR', 'c10_Bm_TCL1A', 'c11_pre-GC', 'c12_Bgc_LZ-like',
    'c13_Bgc_DZ-like', 'c14_Bm_activated-cycling', 'c15_cycling_ASC', 'c16_PC_IGHG',
    'c17_PC_IGHA', 'c18_early-PC_MS4A1$^{low}$', 'c19_early-PC_LTB', 'c20_early-PC_RGS13',
]
naive = {0, 1, 2}
iso_names = ['IGHM', 'IGHD', 'IGHA1', 'IGHA2', 'IGHG1', 'IGHG2', 'IGHG3', 'IGHG4']
iso_colors = ['#A6CEE3', '#2C7BB6', '#C7E9B4', '#4DAF4A',
              '#F4A6B8', '#E31A1C', '#FDD0A2', '#F28E2B']
shm_names = ['High', 'Median', 'Low']
shm_colors = ['#7F2704', '#F58220', '#FDEBD2']

r = rng(39)
n = len(clusters)

# 每簇 isotype 比例
iso_prop = np.zeros((n, 8))
for i in range(n):
    if i in naive:
        base = np.array([0.72, 0.14, 0.005, 0.005, 0.05, 0.005, 0.06, 0.015])
    elif i in (9, 10):                       # Bm_TCL1A / pre-GC
        base = np.array([0.42, 0.05, 0.03, 0.03, 0.35, 0.04, 0.05, 0.03])
    elif i >= 15:                            # 浆细胞
        base = np.array([0.05, 0.005, 0.14, 0.10, 0.47, 0.05, 0.045, 0.13])
    else:                                    # 经典记忆 / ABC / GC
        base = np.array([0.28, 0.03, 0.14, 0.09, 0.36, 0.04, 0.03, 0.03])
    p = base * r.normal(1, 0.12, 8)
    p = np.clip(p, 0.002, None)
    iso_prop[i] = p / p.sum()

shm_prop = np.zeros((n, 3))
for i in range(n):
    if i in naive or i == 10:
        base = np.array([0.16, 0.16, 0.68])
    elif i >= 15:
        base = np.array([0.50, 0.40, 0.10])
    else:
        base = np.array([0.56, 0.33, 0.11])
    p = base * r.normal(1, 0.10, 3)
    shm_prop[i] = p / p.sum()

shm_rate = np.array([0.9, 1.1, 0.7, 5.8, 4.9, 5.5, 4.2, 4.6, 3.0, 1.2,
                     2.5, 4.0, 3.7, 4.4, 5.9, 6.2, 6.5, 5.2, 5.6, 2.9])

ys = np.arange(n)
fig, (ax1, ax2, ax3) = plt.subplots(
    1, 3, figsize=cm2in(20, 14), sharey=True,
    gridspec_kw={'width_ratios': [1.05, 1.05, 0.85], 'wspace': 0.10})

left1 = np.zeros(n)
for j in range(8):
    ax1.barh(ys, iso_prop[:, j], left=left1, height=0.86, color=iso_colors[j], lw=0)
    left1 += iso_prop[:, j]
ax1.set_xlim(0, 1.0)
ax1.set_xlabel('Proportion', fontsize=9)
ax1.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax1.set_xticklabels(['0.00', '0.25', '0.50', '0.75', '1.00'], rotation=45, ha='right')

left2 = np.zeros(n)
for j in range(3):
    ax2.barh(ys, shm_prop[:, j], left=left2, height=0.86, color=shm_colors[j], lw=0)
    left2 += shm_prop[:, j]
ax2.set_xlim(0, 1.0)
ax2.set_xlabel('Proportion', fontsize=9)
ax2.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax2.set_xticklabels(['0.00', '0.25', '0.50', '0.75', '1.00'], rotation=45, ha='right')

ax3.scatter(shm_rate, ys, s=16, color='black', zorder=3)
ax3.set_xlim(0, 7.4)
ax3.set_xlabel('SHM rate (%)', fontsize=9)
ax3.set_xticks([0, 2, 4, 6])
ax3.grid(True, color='#DCDCDC', lw=0.8)
ax3.set_axisbelow(True)
for sp in ax3.spines.values():
    sp.set_visible(True)
    sp.set_color('black')

ax1.set_yticks(ys)
ax1.set_yticklabels(clusters, fontsize=7.5)
ax1.invert_yaxis()
ax1.tick_params(left=False)

leg1 = ax3.legend(handles=[Patch(fc=c, label=nm) for nm, c in zip(iso_names, iso_colors)],
                  loc='upper left', bbox_to_anchor=(1.06, 1.02), frameon=False,
                  fontsize=8, title='BCR isotype', title_fontsize=9,
                  handlelength=1.3, handleheight=1.1, labelspacing=0.55)
leg2 = ax3.legend(handles=[Patch(fc=c, label=nm) for nm, c in zip(shm_names, shm_colors)],
                  loc='upper left', bbox_to_anchor=(1.06, 0.42), frameon=False,
                  fontsize=8, title='SHM level', title_fontsize=9,
                  handlelength=1.3, handleheight=1.1, labelspacing=0.55)
ax3.add_artist(leg1)

fig.subplots_adjust(left=0.155, right=0.83, top=0.97, bottom=0.10)
save(fig, 'case_seg039.png')
