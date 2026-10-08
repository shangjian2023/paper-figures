# -*- coding: utf-8 -*-
"""案例51 - Nature 样本地理分布图(一): 世界 choropleth + 国别饼图。
参考: frames/seg_051.jpg — 蓝白渐变填色(中国最深), 叠冬/半冬/春 3 色饼图, 左下图例+同心圆+色条。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'helpers'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle, Rectangle
from matplotlib import cm, colors as mcolors
from geo import world_map, mercator

SEED = 51
r51 = rng(SEED)

# ---------------------------------------------------------------- 国家 accession 数(合成)
COUNT = {'China': 1000, 'Russia': 420, 'Canada': 380, 'Australia': 320,
         'Germany': 220, 'France': 170, 'Poland': 120, 'India': 90,
         'Japan': 70, 'Kazakhstan': 45, 'Mongolia': 35, 'United States of America': 20,
         'Iran': 18, 'Pakistan': 12, 'Italy': 10, 'Spain': 8}
cmap = plt.get_cmap('Blues')
norm = mcolors.LogNorm(vmin=1, vmax=1000)

def fill(props):
    nm = props.get('name')
    if nm in COUNT:
        return cmap(norm(COUNT[nm]))
    return '#FBFBFB'

fig = plt.figure(figsize=cm2in(18, 8.8))
ax = fig.add_subplot(111)
world_map(ax, facecolor_fn=fill, edgecolor='#8C8C8C', lw=0.35,
          extent=(-172, 185, -58, 82))
ax.set_facecolor('white')

# 地图外框
ax.add_patch(Rectangle((0.002, 0.004), 0.996, 0.992, transform=ax.transAxes,
                       facecolor='none', edgecolor='black', lw=0.8, zorder=10))

# ---------------------------------------------------------------- 国别饼图(8 国)
ECO = [('Winter', '#3A6BA5'), ('Semi-winter', '#57C78A'), ('Spring', '#F2C14E')]
PIES = [('Canada', -108, 58), ('Germany', 10.5, 51.5), ('France', 2.2, 47.0),
        ('Russia', 62, 62), ('India', 79, 22.5), ('China', 103.5, 34.5),
        ('Japan', 138.5, 37.5), ('Australia', 134.5, -25.5)]
comp = {}
for nm, lon, lat in PIES:
    total = COUNT[nm]
    fr = r51.dirichlet(np.array([2.0, 3.2, 1.6]) *
                       (3.0 if nm == 'China' else 1.0))
    comp[nm] = (lon, lat, total, fr)

for nm, (lon, lat, total, fr) in comp.items():
    x, y = mercator(lon, lat)
    r = np.radians(1.0 + 6.6 * np.sqrt(total / 1000.0))
    start = 90.0
    for (lab, col), f in zip(ECO, fr):
        sweep = 360.0 * f
        ax.add_patch(Wedge((x, y), r, start, start + sweep, width=r,
                           facecolor=col, edgecolor='white', lw=0.5, zorder=6))
        start += sweep

# ---------------------------------------------------------------- 左下图例(axes 坐标)
tx, ty = 0.015, 0.30
ax.text(tx, ty + 0.175, 'Ecotype', transform=ax.transAxes, fontsize=7.5, va='top')
for k_i, (lab, col) in enumerate(ECO):
    yy = ty + 0.105 - k_i * 0.048
    ax.add_patch(Rectangle((tx, yy - 0.012), 0.018, 0.026, transform=ax.transAxes,
                           facecolor=col, edgecolor='#666666', lw=0.4, zorder=11))
    ax.text(tx + 0.026, yy, lab, transform=ax.transAxes, fontsize=6.8, va='center',
            zorder=11)

ax.text(tx + 0.145, ty + 0.175, 'Accessions', transform=ax.transAxes,
        fontsize=7.5, va='top')
cx0, cy0 = tx + 0.185, ty - 0.006
for k_i, (v, lab) in enumerate([(1000, '1,000'), (100, '100'), (10, '10')]):
    r = 0.062 * np.sqrt(v / 1000.0)
    ax.add_patch(Circle((cx0, cy0 + r), r, transform=ax.transAxes,
                        facecolor='none', edgecolor='#555555', lw=0.6, zorder=11))
    ly = ty + 0.095 - k_i * 0.035
    ax.plot([cx0 + r * 0.55, tx + 0.245], [cy0 + r * 0.9, ly],
            transform=ax.transAxes, color='#555555', lw=0.5, zorder=11)
    ax.text(tx + 0.25, ly, lab, transform=ax.transAxes,
            fontsize=6.2, va='center', zorder=11)

cax = fig.add_axes([0.465, 0.09, 0.010, 0.26])   # 南大西洋空白海域, 避开南美洲
cb = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax)
cb.set_ticks([1, 10, 100])
cb.ax.set_yticklabels(['1', '10', '100'], fontsize=6.5)
cb.outline.set_edgecolor('#888888')
cb.outline.set_linewidth(0.5)
cb.set_label('Accessions', fontsize=7, labelpad=2)

save(fig, 'case_seg051.png')
