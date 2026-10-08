# -*- coding: utf-8 -*-
"""案例53 - Nature 样本地理分布图(三): 米色陆地世界地图 + 各国大饼图(11 亚型)。
参考: frames/seg_053.jpg — 饼径∝样本量, 玫红 hpEurope 为主, 底部两行图例 + 同心圆图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'helpers'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle, Patch
from geo import world_map, mercator

SEED = 53
r53 = rng(SEED)

# 11 亚型
HP = [('hpAfrica1', '#2E9E3C'), ('hpEurope', '#D62A8C'), ('hpSahul', '#C99BD9'),
      ('hpNEAfrica', '#3BD52E'), ('hpAsia2', '#F5DE4E'), ('hpNorthAsia', '#40D9C4'),
      ('hpIndigenousAmerica', '#4FA8E8'), ('hpEastAsia', '#F0873C'),
      ('hpSiberia', '#8B5EC8'), ('hpIndigenousNAmerica', '#2B3A9E'),
      ('hpUral', '#9E2B2B')]

# 区域 -> 亚型权重提升
REGION_W = {'Europe': [1, 14, 0.2, 0.3, 1.5, 1, 0.2, 0.5, 1, 0.3, 0.6],
            'EAsia': [0.4, 1.5, 0.2, 0.2, 6, 1.5, 0.2, 14, 1, 0.3, 0.3],
            'Africa': [8, 1, 0.2, 3, 0.3, 0.2, 0.3, 0.2, 0.2, 0.2, 0.4],
            'America': [1.5, 5, 0.3, 0.3, 0.3, 0.3, 5, 0.3, 0.8, 1.5, 0.3],
            'Oceania': [1, 1.5, 8, 0.3, 1, 0.5, 1, 0.5, 0.3, 0.3, 0.3],
            'CSAsia': [1, 2, 0.2, 0.3, 4, 2, 0.2, 2, 0.5, 0.3, 0.5]}
COUNTRY = [('USA', -100, 40, 180, 'America'), ('Canada', -112, 58, 30, 'America'),
           ('Mexico', -102, 23, 220, 'America'), ('Colombia', -74, 4, 90, 'America'),
           ('Brazil', -52, -10, 150, 'America'), ('Peru', -77, -10, 60, 'America'),
           ('Argentina', -65, -34, 45, 'America'),
           ('UK', -1.5, 53, 260, 'Europe'), ('France', 2.5, 47, 320, 'Europe'),
           ('Spain', -3.8, 40, 140, 'Europe'), ('Germany', 10.4, 51.3, 200, 'Europe'),
           ('Italy', 12.8, 42.5, 120, 'Europe'), ('Egypt', 30, 27, 45, 'Africa'),
           ('S.Africa', 25, -29, 80, 'Africa'), ('India', 79, 22, 150, 'CSAsia'),
           ('China', 104, 35, 220, 'EAsia'), ('Japan', 139, 37, 90, 'EAsia'),
           ('Thailand', 101, 15, 60, 'EAsia'), ('Indonesia', 113, -2, 50, 'Oceania'),
           ('Australia', 134, -25, 110, 'Oceania')]

fig = plt.figure(figsize=cm2in(18, 10.5))
ax = fig.add_subplot(111)
world_map(ax, facecolor_fn=lambda p: '#E4D3B0', edgecolor='white', lw=0.4,
          extent=(-170, 185, -58, 80))

for nm, lon, lat, n, reg in COUNTRY:
    fr = r53.dirichlet(np.array(REGION_W[reg]))
    x, y = mercator(lon, lat)
    r = np.radians(max(0.7, 5.2 * np.sqrt(n / 320.0)))
    start = 90.0
    for (_lab, col), f in zip(HP, fr):
        sweep = 360.0 * f
        ax.add_patch(Wedge((x, y), r, start, start + sweep, width=r,
                           facecolor=col, edgecolor='black', lw=0.5, zorder=6))
        start += sweep

# ---------------------------------------------------------------- 左下同心圆图例 1000/100/10/1
tx, ty = 0.02, 0.05
cx0 = tx + 0.07
for k_i, v in enumerate([1000, 100, 10, 1]):
    r = 0.068 * np.sqrt(v / 1000.0)
    ax.add_patch(Circle((cx0, ty + r), r, transform=ax.transAxes,
                        facecolor='white', edgecolor='#333333', lw=0.7, zorder=11))
    ly = ty + 0.185 - k_i * 0.045
    ax.plot([cx0 + r * 0.6, tx + 0.135], [ty + r * 0.85, ly],
            transform=ax.transAxes, color='#333333', lw=0.5, zorder=11)
    ax.text(tx + 0.142, ly, str(v), transform=ax.transAxes, fontsize=6.5,
            va='center', zorder=11)

# ---------------------------------------------------------------- 底部两行图例
handles = [Patch(facecolor=c, edgecolor='black', lw=0.4, label=nm)
           for nm, c in HP]
ax.legend(handles=handles, ncol=6, loc='upper center', bbox_to_anchor=(0.52, -0.015),
          frameon=False, fontsize=6.5, handlelength=1.1, handleheight=0.9,
          columnspacing=1.2)

save(fig, 'case_seg053.png')
