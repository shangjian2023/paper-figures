# -*- coding: utf-8 -*-
"""案例52 - Science 样本地理分布图(二): 白陆地+浅蓝海洋+采样点饼图。
参考: frames/seg_052.jpg — 海洋采样点, 饼色=3 类群, 饼径∝样本数, 左下同心圆图例 80/20/1。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'helpers'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle, Rectangle, Patch
from geo import world_map, mercator

SEED = 52
r52 = rng(SEED)

CLADE = [('Clade I', '#C46A7E'), ('Clade II', '#C9D96F'), ('Clade III', '#5F463C')]

# 采样点: (名, lon, lat, 样本数) — 海洋/近海站位
ST = [('Hawaii', -155.5, 20.0, 85), ('Caribbean', -68.0, 16.0, 62),
      ('Gulf Stream', -75.0, 30.0, 40), ('Bermuda', -63.0, 31.5, 28),
      ('Sargasso', -52.0, 27.0, 18), ('S. Pacific', -120.0, -28.0, 9),
      ('S. Atlantic', -18.0, -28.0, 14), ('S. Africa', 22.0, -36.0, 46),
      ('Indian Ocean', 67.0, -8.0, 20), ('Maldives', 72.5, 4.0, 30),
      ('Bay of Bengal', 88.0, 14.0, 12), ('S. China Sea', 114.0, 11.0, 24),
      ('W. Pacific', 142.0, 14.0, 38), ('Coral Sea', 154.0, -17.0, 26),
      ('Tasman Sea', 166.0, -40.0, 16), ('Mediterranean', 17.0, 35.5, 44)]

fig = plt.figure(figsize=cm2in(18, 8.8))
ax = fig.add_subplot(111)
world_map(ax, facecolor_fn=lambda p: 'white', edgecolor='#9FB6C2', lw=0.35,
          extent=(-175, 185, -62, 80))
ox0, oy0 = mercator(-175, -62)
ox1, oy1 = mercator(185, 80)
ax.add_patch(Rectangle((ox0, oy0), ox1 - ox0, oy1 - oy0, facecolor='#A6DCEF',
                       edgecolor='none', zorder=0))

for nm, lon, lat, n in ST:
    fr = r52.dirichlet([2.4, 2.0, 1.2])
    x, y = mercator(lon, lat)
    r = np.radians(0.55 + 1.05 * np.sqrt(n))
    start = 90.0
    for (_lab, col), f in zip(CLADE, fr):
        sweep = 360.0 * f
        ax.add_patch(Wedge((x, y), r, start, start + sweep, width=r,
                           facecolor=col, edgecolor='#3A3A3A', lw=0.45, zorder=6))
        start += sweep

# ---------------------------------------------------------------- 左下同心圆图例
tx, ty = 0.02, 0.06
cx0 = tx + 0.075
for k_i, v in enumerate([80, 20, 1]):
    r = 0.075 * np.sqrt(v / 80.0)
    ax.add_patch(Circle((cx0, ty + r), r, transform=ax.transAxes,
                        facecolor='white', edgecolor='#333333', lw=0.7, zorder=11))
    ly = ty + 0.155 - k_i * 0.045
    ax.plot([cx0 + r * 0.6, tx + 0.145], [ty + r * 0.85, ly],
            transform=ax.transAxes, color='#333333', lw=0.5, zorder=11)
    ax.text(tx + 0.152, ly, str(v), transform=ax.transAxes, fontsize=6.5,
            va='center', zorder=11)
ax.plot([cx0 - 0.05, cx0 + 0.045], [ty + 0.008, ty + 0.008],
        transform=ax.transAxes, color='#333333', lw=0.5, zorder=11)

# ---------------------------------------------------------------- 右下三色图例
handles = [Patch(facecolor=col, edgecolor='#3A3A3A', lw=0.5, label=lab)
           for lab, col in CLADE]
leg = ax.legend(handles=handles, loc='lower right', bbox_to_anchor=(0.885, 0.025),
                frameon=True, facecolor='white', edgecolor='#9FB6C2',
                framealpha=0.95, fontsize=6.8, handlelength=1.15,
                handleheight=1.15, borderpad=0.55, labelspacing=0.38)
leg.set_zorder(12)

save(fig, 'case_seg052.png')
