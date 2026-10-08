# -*- coding: utf-8 -*-
"""案例65 - Nature 平滑曲线图(一): 双峰光谱散点 + 样条平滑线。
参考: frames/seg_063.jpg — 品红 400 nN / 青绿 0 nN 两组各约 300 散点,
空心圆 marker, 样条平滑线, 图例左上线-圆符号, 仅左下 spines。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.interpolate import make_interp_spline

set_style()

r = rng(63)
XL0, XL1 = 672.0, 858.0


def spectrum(x, big_h, r):
    """双峰光谱: 695 nm 小峰 + 748 nm 微包 + 800 nm 主峰 + 噪声。"""
    y = (0.07
         + 0.95 * np.exp(-((x - 695) / 8.0) ** 2)
         + 0.20 * np.exp(-((x - 748) / 16.0) ** 2)
         + big_h * np.exp(-((x - 800) / 10.5) ** 2))
    return y + r.normal(0, 0.11, x.size)


def smooth(x, y, nb=40):
    """分箱均值 + 三次样条插值。"""
    edges = np.linspace(XL0, XL1, nb + 1)
    idx = np.digitize(x, edges) - 1
    cx, cy = [], []
    for k in range(nb):
        m = idx == k
        if m.sum() >= 3:
            cx.append(x[m].mean())
            cy.append(y[m].mean())
    cx, cy = np.array(cx), np.array(cy)
    xx = np.linspace(cx.min(), cx.max(), 400)
    return xx, make_interp_spline(cx, cy, k=3)(xx)


x1 = r.uniform(XL0, XL1, 300)
y1 = spectrum(x1, 7.6, rng(631))
x2 = r.uniform(XL0, XL1, 300)
y2 = spectrum(x2, 4.4, rng(632))

fig, ax = plt.subplots(figsize=cm2in(11.5, 14.5))
ax.scatter(x1, y1, s=13, facecolors='none', edgecolors='#C24BC9',
           linewidths=0.7, alpha=0.85, zorder=2)
ax.scatter(x2, y2, s=13, facecolors='none', edgecolors='#43C1B0',
           linewidths=0.7, alpha=0.85, zorder=2)
xx1, yy1 = smooth(x1, y1)
xx2, yy2 = smooth(x2, y2)
ax.plot(xx1, yy1, color='#7A1FA0', lw=1.8, zorder=3)
ax.plot(xx2, yy2, color='#0E7C74', lw=1.8, zorder=3)

handles = [
    Line2D([], [], color='#7A1FA0', lw=1.8, marker='o', ms=6,
           mfc='none', mec='#C24BC9', label='400 nN'),
    Line2D([], [], color='#0E7C74', lw=1.8, marker='o', ms=6,
           mfc='none', mec='#43C1B0', label='0 nN'),
]
ax.legend(handles=handles, loc='upper left', frameon=False,
          bbox_to_anchor=(0.06, 0.90), fontsize=8.5, labelspacing=0.9)

ax.set_xlim(668, 862)
ax.set_ylim(-0.2, 8.7)
ax.set_yticks([0, 2, 4, 6, 8])
ax.set_xticks([700, 750, 800, 850])
ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Normalized emission intensity')
# set_style 默认只留左/下 spines
save(fig, 'case_seg063.png')
