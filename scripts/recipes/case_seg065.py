# -*- coding: utf-8 -*-
"""案例67 - Nature 平滑曲线图(三): 剂量-响应曲线。
参考: frames/seg_065.jpg — x 对数 1e-9~1e-4, 橙圆 Venetoclax(KD=96 nM) 与
蓝方 No venetoclax 两组 Sigmoid 拟合线 + 散点, 图例左上含 KD 文本, 全框。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()


def drc(x, bottom, top, logic50, hill):
    """x 为 log10 浓度。"""
    return bottom + (top - bottom) / (1 + 10 ** ((logic50 - x) * hill))


# Venetoclax: KD = 96 nM -> logIC50 = -7.018
conc_o = np.array([3.9e-9, 7.8e-9, 1.56e-8, 3.1e-8, 6.2e-8, 1.25e-7,
                   2.5e-7, 5.0e-7, 1.0e-6])
shift_o = np.array([0.031, 0.037, 0.061, 0.104, 0.146, 0.212, 0.281,
                    0.283, 0.309])
fit_o = dict(bottom=0.028, top=0.315, logic50=np.log10(9.6e-8), hill=1.0)

# No venetoclax: 右移约 1 个十位
conc_b = np.array([4.0e-8, 1.6e-7, 3.2e-7, 6.4e-7, 1.3e-6, 2.6e-6,
                   5.2e-6, 1.05e-5, 1.6e-5])
shift_b = np.array([-0.017, -0.014, -0.006, 0.012, 0.042, 0.099, 0.138,
                    0.191, 0.276])
fit_b = dict(bottom=-0.022, top=0.300, logic50=-5.95, hill=1.15)

fig, ax = plt.subplots(figsize=cm2in(13.0, 13.0))
for s in ax.spines.values():
    s.set_visible(True)

xs = np.linspace(-9, -4, 400)
ax.semilogx(10 ** xs, drc(xs, **fit_o), color='#E8801A', lw=1.5, zorder=2)
ax.semilogx(10 ** xs, drc(xs, **fit_b), color='#5B9BD5', lw=1.5, zorder=2)
ax.plot(conc_o, shift_o, 'o', ms=7, mfc='#E8801A', mec='#9A5410',
        mew=1.0, zorder=3)
ax.plot(conc_b, shift_b, 's', ms=7, mfc='#5B9BD5', mec='#2E5B8A',
        mew=1.0, zorder=3)

ax.text(0.035, 0.975, 'DBVen1619_2', transform=ax.transAxes,
        fontsize=9, va='top')
handles = [
    Line2D([], [], color='#5B9BD5', lw=1.5, marker='s', ms=6,
           mfc='#5B9BD5', mec='#2E5B8A', label='No venetoclax'),
    Line2D([], [], color='#E8801A', lw=1.5, marker='o', ms=6,
           mfc='#E8801A', mec='#9A5410',
           label='Venetoclax:\n$K_\\mathrm{D}$ = 96 nM'),
]
ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(0.035, 0.88),
          frameon=False, fontsize=9, labelspacing=1.4)

ax.set_xlim(1e-9, 1e-4)
ax.set_ylim(-0.06, 0.34)
ax.set_yticks([0, 0.1, 0.2, 0.3])
ax.set_xticks([1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4])
ax.set_xlabel('Concentration (M)')
ax.set_ylabel('Shift (nm)')

save(fig, 'case_seg065.png')
