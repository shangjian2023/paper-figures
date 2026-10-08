# -*- coding: utf-8 -*-
"""案例44 (seg 43) - Nature 联合密度 + 边际直方图。
参考 frames/seg_043.jpg: 中央两组填充等高密度 (蓝 Species A / 红 Species B),
顶部/右侧边际直方图 (描边同色), 右上组图例 + "深浅=密度"注释,
坐标 30-80, 轴 Body mass (kg) / Heart rate (bpm) / Density。"""
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from scipy.stats import gaussian_kde

set_style()
r = rng(43)

A = r.multivariate_normal([50, 61], [[16, 3], [3, 18]], 420).clip(30, 80)
B = r.multivariate_normal([60, 49], [[18, -2], [-2, 26]], 460).clip(30, 80)
GROUPS = [('Species A', A, 'Blues', '#3b6ea5', '#c6dbef'),
          ('Species B', B, 'Reds', '#c0392b', '#f4c7c3')]

fig = plt.figure(figsize=cm2in(15, 14))
gs = fig.add_gridspec(2, 2, width_ratios=[3.1, 1.0], height_ratios=[1.0, 3.1],
                      wspace=0.06, hspace=0.06, left=0.105, right=0.98,
                      top=0.95, bottom=0.085)

axH = fig.add_subplot(gs[0, 0])
for name, pts, cmap, ec, fc in GROUPS:
    axH.hist(pts[:, 0], bins=32, range=(30, 80), density=True,
             facecolor=fc, edgecolor=ec, lw=0.6)
axH.set_xlim(30, 80)
axH.set_ylim(0, 0.16)
axH.set_yticks([0.0, 0.1])
axH.set_ylabel('Density', fontsize=9)
axH.tick_params(labelbottom=False, labelsize=7)
despine(axH)

axV = fig.add_subplot(gs[1, 1])
for name, pts, cmap, ec, fc in GROUPS:
    axV.hist(pts[:, 1], bins=32, range=(30, 80), density=True,
             orientation='horizontal', facecolor=fc, edgecolor=ec, lw=0.6)
axV.set_ylim(30, 80)
axV.set_xlim(0, 0.16)
axV.set_xticks([0.0, 0.1])
axV.set_xlabel('Density', fontsize=9)
axV.tick_params(labelleft=False, labelsize=7)
despine(axV)

axM = fig.add_subplot(gs[1, 0])
gx = np.linspace(30, 80, 150)
gy = np.linspace(30, 80, 150)
XX, YY = np.meshgrid(gx, gy)
grid = np.vstack([XX.ravel(), YY.ravel()])
for name, pts, cmap, ec, fc in GROUPS:
    Z = gaussian_kde(pts.T)(grid).reshape(XX.shape)
    Z /= Z.max()
    axM.contourf(XX, YY, Z, levels=np.linspace(0.05, 1.0, 12), cmap=cmap)
axM.set_xlim(30, 80)
axM.set_ylim(30, 80)
axM.set_xticks(np.arange(30, 81, 10))
axM.set_yticks(np.arange(30, 81, 10))
axM.set_xlabel('Body mass (kg)', fontsize=10)
axM.set_ylabel('Heart rate (bpm)', fontsize=10)
axM.tick_params(labelsize=8)
for sp in axM.spines.values():
    sp.set_visible(True)

axL = fig.add_subplot(gs[0, 1])
axL.axis('off')
handles = [Patch(facecolor=fc, edgecolor=ec, label=name)
           for name, _, _, ec, fc in GROUPS]
axL.legend(handles=handles, loc='upper left', bbox_to_anchor=(0.02, 1.06),
           fontsize=8, frameon=False, handlelength=1.4, handleheight=1.0)
axL.text(0.05, 0.34, 'Contour shading: darker = higher density\n'
         '(KDE normalized to each species\u2019 peak)',
         fontsize=6.8, color='#555555', va='top', ha='left',
         linespacing=1.5)

save(fig, 'case_seg043.png')
