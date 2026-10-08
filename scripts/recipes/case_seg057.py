# -*- coding: utf-8 -*-
"""案例59 - Nature 圆形雷达图(3组): 3 个并排 8 轴圆形雷达。
参考: frames/seg_057.jpg — 外圈浅蓝/灰弧带, 半透明填充多边形+描边+顶点点,
底部 Peptide antigen / TCRβ 两个图例框。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle, FancyBboxPatch

set_style()

order = list('ABCDEFGH')
# 轴角度(数学角, 度): B 顶, 顺时针 C D E F G, H 左, A 左上
ang = dict(B=90, C=45, D=0, E=-45, F=-90, G=-135, H=180, A=135)
theta = np.array([np.radians(ang[l]) for l in order])

# 每组 8 值, 顺序 A..H
data = [
    ('PG3', 'High', [0.78, 0.97, 0.14, 0.10, 0.16, 0.30, 0.86, 0.92], '#E8934A'),
    ('PG2', 'Low',  [0.80, 0.58, 0.74, 0.56, 0.52, 0.44, 0.24, 0.38], '#7FA8D0'),
    ('PG1', 'Low',  [0.16, 0.22, 0.66, 0.90, 0.56, 0.52, 0.16, 0.30], '#5FB585'),
]

fig = plt.figure(figsize=cm2in(17.5, 16.5))
fig.text(0.5, 0.955, 'Peptide Group : TCR Group', ha='center',
         fontsize=11, fontweight='bold')

XS = [0.035, 0.36, 0.685]
YW, H = 0.42, 0.42


def draw_radar(x0, y0, vals, color):
    ax = fig.add_axes([x0, y0, 0.285, H])
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal'); ax.axis('off')
    # 外圈弧带: 上半浅蓝, 下半浅灰
    ax.add_patch(Wedge((0, 0), 1.17, -22.5, 157.5, width=0.12,
                       fc='#C7E3EA', ec='none'))
    ax.add_patch(Wedge((0, 0), 1.17, 157.5, 337.5, width=0.12,
                       fc='#D9D9D9', ec='none'))
    ax.add_patch(Circle((0, 0), 1.03, fc='white', ec='none'))
    # 网格
    for r in (0.25, 0.5, 0.75, 1.0):
        ax.add_patch(Circle((0, 0), r, fc='none', ec='#CCCCCC', lw=0.5))
    for t in theta:
        ax.plot([0, np.cos(t)], [0, np.sin(t)], color='#CCCCCC', lw=0.5, zorder=0.5)
    ax.add_patch(Circle((0, 0), 1.0, fc='none', ec='#BBBBBB', lw=0.7))
    # 同心环刻度: 归一化值 0-1, 标在 A/B 轴之间的 112.5° 空档方向
    t_r = np.radians(112.5)
    for rv, lab in zip((0.25, 0.5, 0.75, 1.0), ('0.25', '0.50', '0.75', '1.0')):
        ax.text(rv * 0.98 * np.cos(t_r), rv * 0.98 * np.sin(t_r), lab,
                ha='center', va='center', fontsize=5.8, color='#888888',
                bbox=dict(fc='white', ec='none', alpha=0.75, pad=0.6),
                zorder=4)
    # 多边形
    v = np.asarray(vals)
    xs, ys = v * np.cos(theta), v * np.sin(theta)
    ax.fill(xs, ys, color=color, alpha=0.38, zorder=2)
    ax.plot(np.append(xs, xs[0]), np.append(ys, ys[0]), color=color,
            lw=1.4, zorder=3)
    ax.scatter(xs, ys, s=13, color=color, zorder=4)
    # 轴标签
    for lab, t in zip(order, theta):
        ax.text(1.32 * np.cos(t), 1.32 * np.sin(t), lab, ha='center',
                va='center', fontsize=10.5)
    return ax


for i, (pg, lv, vals, color) in enumerate(data):
    draw_radar(XS[i], YW, vals, color)
    fig.text(XS[i] + 0.14, YW + H + 0.012, pg, ha='center', fontsize=11,
             color=color, fontweight='bold')
    fig.text(XS[i] + 0.14 + (0.024 if pg == 'PG3' else 0.019), YW + H + 0.012,
             ':' + lv, ha='left', fontsize=11,
             color='#CC2222' if lv == 'High' else 'black')

# ---- 径向刻度说明 ----------------------------------------------------
fig.text(0.5, 0.395, 'Concentric ring scale: normalized value, 0 (center) \u2013 1 (outer ring)',
         ha='center', fontsize=7.5, color='#555555')

# ---- 底部两个图例框 --------------------------------------------------
BY0, BH = 0.155, 0.135          # 框底/框高
fig.text(0.250, BY0 + BH + 0.028, 'Peptide antigen', ha='center', fontsize=9.5)
fig.patches.append(FancyBboxPatch((0.115, BY0), 0.335, BH,
                                  boxstyle='round,pad=0.012,rounding_size=0.02',
                                  fc='#DCF2F4', ec='#B9DDE0', lw=1.0,
                                  transform=fig.transFigure, zorder=0))
fig.text(0.150, BY0 + BH - 0.018, 'A: Anchor_HPphobic\nB: Charge\n'
         'C: Bulkiness\nD: HPphobic', fontsize=8.5, va='top',
         linespacing=1.55)
fig.text(0.355, BY0 + BH - 0.062, '}', fontsize=17, va='center')
fig.text(0.378, BY0 + BH - 0.062, 'Exposed', fontsize=8.5, va='center')

fig.text(0.720, BY0 + BH + 0.028, 'TCR\u03b2', ha='center', fontsize=9.5)
fig.patches.append(FancyBboxPatch((0.575, BY0), 0.325, BH,
                                  boxstyle='round,pad=0.012,rounding_size=0.02',
                                  fc='#EBEBEB', ec='#C8C8C8', lw=1.0,
                                  transform=fig.transFigure, zorder=0))
fig.text(0.610, BY0 + BH - 0.018, 'E: TCR\u03b2_length\nF: Charge\n'
         'G: Bulkiness\nH: HPphobic', fontsize=8.5, va='top',
         linespacing=1.55)
fig.text(0.810, BY0 + BH - 0.062, '}', fontsize=17, va='center')
fig.text(0.833, BY0 + BH - 0.062, 'CDR3\u03b2mer', fontsize=8.5, va='center')

save(fig, 'case_seg057.png')
