# -*- coding: utf-8 -*-
"""案例84 - Nature FC-FC 对角带散点: 对角线±0.5平行带内分色, 带外灰点, 基因名红箭头标注。
参考: frames/seg_082.jpg — shEif2b5 versus shCon"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D

set_style()

r = rng(82)
LIM = 5.3

def band_pts(n, mu, sig, seed_off):
    """对角带内点: y = x + U(-0.45,0.45)"""
    rr = rng(82 + seed_off)
    x = np.clip(rr.normal(mu, sig, n), -LIM, LIM)
    y = np.clip(x + rr.uniform(-0.45, 0.45, n), -LIM, LIM)
    return x, y

# ---- 类别数据
xg1, yg1 = band_pts(1150, 2.0, 1.35, 1)        # 浅绿 2,317 (上调带)
xg2, yg2 = band_pts(820, -2.0, 1.35, 2)        # 深绿 1,633 (下调带)
xs1 = np.clip(r.normal(1.0, 0.9, 52), -LIM, LIM)          # 鲑红 52 (带上方)
ys1 = np.clip(xs1 + r.normal(1.35, 0.55, 52), -LIM, LIM)
xs2 = np.clip(r.normal(-0.6, 1.0, 151), -LIM, LIM)        # 暗红 151 (带下方)
ys2 = np.clip(xs2 + r.normal(-1.35, 0.55, 151), -LIM, LIM)
xs3 = np.clip(r.normal(-0.7, 0.5, 49), -LIM, LIM)         # 浅蓝 49
ys3 = np.clip(xs3 + r.normal(-1.1, 0.4, 49), -LIM, LIM)
xs4 = np.clip(r.normal(0.1, 0.3, 8), -LIM, LIM)           # 藏青 8
ys4 = np.clip(xs4 - r.normal(1.25, 0.2, 8), -LIM, LIM)

ngray = 950
xg = np.clip(r.normal(0, 2.1, ngray), -LIM, LIM)
yg = np.clip(r.normal(0, 2.1, ngray), -LIM, LIM)

fig, ax = plt.subplots(figsize=cm2in(12.5, 12.5))
ax.set_title('shEif2b5 versus shCon', fontsize=11, pad=8)

# 中央灰区 + 背景灰点
ax.add_patch(Rectangle((-0.5, -0.5), 1, 1, fc='0.88', ec='none', zorder=0.5))
ax.scatter(xg, yg, s=11, c='#B8B8B8', alpha=0.55, linewidths=0, zorder=1)

# 十字与对角带
ax.axhline(0, ls=':', lw=1.0, color='black', zorder=2)
ax.axvline(0, ls=':', lw=1.0, color='black', zorder=2)
ax.axhline(0.5, lw=1.4, color='black', zorder=6)
ax.axhline(-0.5, lw=1.4, color='black', zorder=6)
ax.axvline(0.5, lw=1.4, color='black', zorder=6)
ax.axvline(-0.5, lw=1.4, color='black', zorder=6)
dg = np.array([-LIM, LIM])
ax.plot(dg, dg + 0.5, color='black', lw=1.5, zorder=6)
ax.plot(dg, dg - 0.5, color='black', lw=1.5, zorder=6)
ax.plot(dg, dg, ls=':', lw=1.0, color='black', zorder=2)

# 彩色点
pts = [('#B8B8B8', xg, yg), ('#F2A285', xs1, ys1), ('#9E1B1B', xs2, ys2),
       ('#AFC8E8', xs3, ys3), ('#1F3F94', xs4, ys4),
       ('#B7E4A8', xg1, yg1), ('#1E7A34', xg2, yg2)]
for c, xp, yp in pts:
    ax.scatter(xp, yp, s=13, c=c, alpha=0.85, linewidths=0, zorder=4)

# ---- 基因名红箭头标注
genes = [('Atf5', (0.7, 2.9), (-0.4, 3.7)),
         ('Atf3', (2.1, 3.2), (1.9, 4.2)),
         ('Atf4', (-0.4, 2.4), (-1.9, 3.0)),
         ('Pck2', (3.2, 2.8), (4.7, 2.75)),
         ('Chop', (3.0, 2.3), (4.8, 2.05)),
         ('Sox5', (3.4, 1.8), (4.9, 1.35)),
         ('Gadd34', (1.0, 0.8), (1.6, -1.5))]
for nm, (px, py), (tx, ty) in genes:
    ha = 'right' if tx > 4.0 else 'center'
    ax.annotate(r'$\it{%s}$' % nm, xy=(px, py), xytext=(tx, ty), fontsize=11,
                color='black', ha=ha, va='center', zorder=7,
                arrowprops=dict(arrowstyle='-|>', color='#CC2222', lw=1.3,
                                shrinkA=2, shrinkB=1))

# ---- 图例(左上/右下): 色点 + 类别名 + (n=...)
def dot(color, label, alpha=0.9):
    return Line2D([], [], marker='o', ls='none', mfc=color, mec=color,
                  ms=5.5, alpha=alpha, label=label)

leg1 = ax.legend(handles=[dot('#F2A285', 'Translation up-regulated (n=52)'),
                          dot('#9E1B1B', 'Translation down-regulated (n=151)'),
                          dot('#AFC8E8', 'Both down: mRNA & polysome (n=49)')],
                 loc='upper left', bbox_to_anchor=(0.02, 0.99), frameon=False,
                 fontsize=8, handlelength=1.2, handletextpad=0.5,
                 labelspacing=0.4, borderaxespad=0)
ax.add_artist(leg1)
ax.legend(handles=[dot('#1F3F94', 'Translation down, mRNA unchanged (n=8)'),
                   dot('#B7E4A8', 'On-diagonal up (n=2,317)'),
                   dot('#1E7A34', 'On-diagonal down (n=1,633)')],
          loc='lower right', bbox_to_anchor=(0.98, 0.02), frameon=False,
          fontsize=8, handlelength=1.2, handletextpad=0.5,
          labelspacing=0.4, borderaxespad=0)

ax.set_xlim(-LIM, LIM)
ax.set_ylim(-LIM, LIM)
ax.set_xticks([-4, -2, 0, 2, 4])
ax.set_yticks([-4, -2, 0, 2, 4])
ax.set_xlabel(r'Total RNA (log$_2$[FC])', fontsize=10)
ax.set_ylabel(r'Polysome-associated' + '\n' + r'RNA (log$_2$[FC])', fontsize=10)
for sp in ('top', 'right'):
    ax.spines[sp].set_visible(True)
ax.tick_params(direction='out', length=4, width=1.1)
for sp in ax.spines.values():
    sp.set_linewidth(1.4)

save(fig, 'case_seg082.png')
