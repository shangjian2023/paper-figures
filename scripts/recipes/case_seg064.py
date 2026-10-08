# -*- coding: utf-8 -*-
"""案例66 - Nature 平滑曲线图(二): 3 条电解液电导率曲线 + 峰下光晕椭圆。
参考: frames/seg_064.jpg — 深蓝/绿/红平滑曲线 + 空心圆标记,
峰区彩色半透明 Ellipse 光晕, 图例右上。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse
from scipy.interpolate import PchipInterpolator

set_style()

series = [
    ('LiFSI/FAN', '#2D2A8C',
     [0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.3, 1.5, 2.5, 4.0],
     [8.5, 15.5, 22.7, 25.2, 31.7, 35.0, 39.0, 40.2, 39.8, 34.7, 25.0]),
    ('LiTFSI/FAN', '#2E9E4F',
     [0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.3, 1.5, 2.5, 4.0],
     [6.2, 9.8, 14.0, 15.2, 17.0, 18.2, 18.8, 18.7, 17.2, 13.8, 8.0]),
    ('LiPF$_6$/EC-EMC', '#D62839',
     [0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.3, 1.5, 2.0, 3.0, 4.0],
     [2.2, 4.2, 6.2, 7.5, 8.7, 9.2, 8.9, 8.3, 7.0, 3.6, 1.2]),
]

fig, ax = plt.subplots(figsize=cm2in(12.5, 13.5))

# ---- 峰下彩色光晕 (双层椭圆叠加) ----
glows = [((1.15, 41.5), 1.6, 17, '#9FB6E8'),
         ((1.0, 19.5), 1.5, 11, '#A5D6A5'),
         ((0.85, 9.0), 1.4, 9, '#F2B49B')]
for (cx, cy), w, h, c in glows:
    ax.add_patch(Ellipse((cx, cy), w * 1.25, h * 1.25, facecolor=c,
                         alpha=0.10, edgecolor='none', zorder=0))
    ax.add_patch(Ellipse((cx, cy), w, h, facecolor=c, alpha=0.16,
                         edgecolor='none', zorder=0))

handles = []
for name, color, xs, ys in series:
    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    xx = np.linspace(xs.min(), xs.max(), 300)
    yy = PchipInterpolator(xs, ys)(xx)
    ax.plot(xx, yy, color=color, lw=1.8, zorder=3)
    ax.plot(xs, ys, 'o', ms=5.5, mfc='white', mec=color, mew=1.5,
            zorder=4)
    handles.append(Line2D([], [], color=color, lw=1.8, marker='o',
                          ms=5.5, mfc='white', label=name))

ax.legend(handles=handles, loc='upper right', frameon=False,
          fontsize=9, labelspacing=0.8)

ax.set_xlim(-0.1, 4.35)
ax.set_ylim(0, 50)
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_yticks([0, 10, 20, 30, 40, 50])
ax.set_xlabel('Concentration (M)')
ax.set_ylabel('Ionic conductivity (mS cm$^{-1}$)')

save(fig, 'case_seg064.png')
