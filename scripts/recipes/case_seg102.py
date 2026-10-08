# -*- coding: utf-8 -*-
"""案例104 (seg 102) - Nature 渐变型等高线密度图。
参考 frames/seg_102.jpg: 灰度填充等高线 + 浅灰背景散点,
黑/蓝/红三条虚斜线参考线, 绿/红重点基因点带引线斜体标注,
右侧灰度色条 'Contour probability density' 0-3。"""
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from scipy.stats import gaussian_kde

set_style()
r = rng(102)

n_bg = 1600
xv = r.normal(0.48, 0.26, n_bg).clip(-0.38, 1.06)
yv = (xv + r.normal(0.02, 0.17, n_bg)).clip(-0.38, 1.06)

gx = np.linspace(-0.42, 1.10, 170)
XX, YY = np.meshgrid(gx, gx)
Z = gaussian_kde(np.vstack([xv, yv]))(np.vstack([XX.ravel(), YY.ravel()]))
Z = (Z / Z.max() * 2.5).reshape(XX.shape)

GREEN = ['#2ca02c', [(0.885, 0.995, 'TMEM100', 0.60, 1.035),
                     (0.975, 0.985, 'MYL1', 1.00, 1.045),
                     (0.962, 0.948, 'CPN2', 1.05, 0.955),
                     (0.945, 0.912, 'CORO1A', 1.05, 0.878),
                     (0.900, 0.930, 'TIMP3', 0.62, 0.925),
                     (0.858, 0.868, 'C5orf52', 0.58, 0.862),
                     (0.883, 0.842, 'LAMP3', 0.72, 0.795)]]
RED = ['#d05050', [(0.950, 0.550, 'HDC', 0.920, 0.585, 0),
                   (0.850, 0.475, 'CA3', 0.890, 0.505, 1),
                   (0.940, 0.345, 'C10orf53', 0.920, 0.388, 0),
                   (0.965, 0.265, 'CSRP3', 0.945, 0.305, 0),
                   (0.760, 0.260, 'PIGR', 0.775, 0.297, 0),
                   (0.715, 0.420, 'S100A14', 0.645, 0.438, 0),
                   (0.665, 0.270, 'PLCB3', 0.555, 0.345, 1),
                   (0.630, 0.130, 'GFRA1', 0.585, 0.168, 0),
                   (0.780, 0.175, 'NKD1', 0.720, 0.108, 1),
                   (0.630, 0.075, 'PCK2', 0.555, 0.060, 0),
                   (0.480, -0.030, 'USE1', 0.515, -0.028, 0),
                   (0.800, -0.050, 'SFRP5', 0.745, -0.052, 0),
                   (0.630, -0.125, 'HNRNPA1', 0.628, -0.170, 0)]]

fig, ax = plt.subplots(figsize=cm2in(14, 13))
fig.subplots_adjust(left=0.115, right=0.86, top=0.97, bottom=0.10)

ax.contourf(XX, YY, Z, levels=np.linspace(0, 3, 14), cmap='Greys')
ax.contour(XX, YY, Z, levels=np.linspace(0.12, 2.9, 15),
           colors='0.45', linewidths=0.35)
ax.scatter(xv, yv, s=2.5, color='0.55', alpha=0.35, lw=0, zorder=3)

# 黑 / 蓝 / 红三条虚斜参考线
ax.plot([-0.35, 1.06], [-0.35, 1.06], color='black', ls='--', lw=1.1,
        dashes=(5, 2.5), zorder=4)
ax.plot([-0.42, 0.53], [0.10, 1.05], color='#2a3db8', ls='--', lw=1.1,
        dashes=(5, 2.5), zorder=4)
ax.plot([0.12, 1.06], [-0.43, 0.51], color='#c03030', ls='--', lw=1.1,
        dashes=(5, 2.5), zorder=4)

gc, gpts = GREEN
ax.scatter([p[0] for p in gpts], [p[1] for p in gpts], s=30, color='#3cb44b',
           zorder=6, edgecolor='white', lw=0.4)
for px, py, name, tx, ty in gpts:
    ax.annotate(r'$\it{%s}$' % name.replace('_', ''), xy=(px, py), xytext=(tx, ty),
                fontsize=8, ha='center', va='center', zorder=7,
                arrowprops=dict(arrowstyle='-', color=gc, lw=0.8,
                                shrinkA=2, shrinkB=2))
rc, rpts2 = RED
ax.scatter([p[0] for p in rpts2], [p[1] for p in rpts2], s=24, color=rc,
           zorder=6, edgecolor='white', lw=0.4)
for px, py, name, tx, ty, leader in rpts2:
    if leader:
        ax.annotate(r'$\it{%s}$' % name, xy=(px, py), xytext=(tx, ty),
                    fontsize=8, ha='center', va='center', zorder=7,
                    arrowprops=dict(arrowstyle='-', color=rc, lw=0.8,
                                    shrinkA=2, shrinkB=2))
    else:
        ax.text(tx, ty, r'$\it{%s}$' % name, fontsize=8, ha='center',
                va='center', zorder=7)

handles = [Line2D([], [], marker='o', ls='none', color='#3cb44b', ms=5.5,
                  label='Highly conserved'),
           Line2D([], [], marker='o', ls='none', color=rc, ms=5.5,
                  label='HL conserved')]
ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(0.01, 1.0),
          fontsize=8, frameon=False)

sm = ScalarMappable(norm=Normalize(0, 3), cmap='Greys')
cb = fig.colorbar(sm, ax=ax, fraction=0.048, pad=0.03, ticks=[0, 1, 2, 3])
cb.ax.set_title('Contour\nprobability\ndensity', fontsize=7.5, loc='left',
                pad=8)
cb.ax.tick_params(labelsize=7)

ax.set_xlim(-0.42, 1.10)
ax.set_ylim(-0.42, 1.10)
ax.set_xticks(np.arange(-0.2, 1.01, 0.2))
ax.set_yticks(np.arange(-0.2, 1.01, 0.2))
ax.tick_params(labelsize=8)
ax.set_xlabel(r'$r_{\mathrm{gHL}}$', fontsize=10)
ax.set_ylabel(r'$r_{\mathrm{gHM}}$', fontsize=10)

save(fig, 'case_seg102.png')
