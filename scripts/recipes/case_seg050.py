# -*- coding: utf-8 -*-
"""案例50b - J.Hazard Mat. 环状柱形图(二): 11指标扇区×4处理径向柱。
参考: frames/seg_050.jpg — 浅彩底+外弧彩条(黄/粉/绿/紫系), 每扇区4根深浅蓝柱,
柱端a-d字母, 虚线刻度圈, 指标名沿弧旋转, 右上CK/Cd/GSH/GSH+Cd图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

set_style()
r = rng(50)                                    # 误差棒长度用, 固定种子可复现

traits = [
    ('H$_2$O$_2$(mmol g$^{-1}$)', [55, 50, 74, 66],   [25, 50, 75],        '#FDFBE8', '#E3DE8A'),
    ('O$_2^{-}$(U T$^{-1}$)',     [22, 30, 26, 38],   [15, 30, 45],        '#FDF8DC', '#EFE38A'),
    ('MDA(mmol g$^{-1}$)',        [7, 12, 10, 19],    [7.5, 15, 22.5],     '#FDF3C4', '#F2D33C'),
    ('SOD(U g$^{-1}$)',           [90, 150, 240, 200],[240, 480, 720],     '#FBE9EF', '#F2A7C3'),
    ('CAT(U g$^{-1}$)',           [240, 360, 300, 420],[140, 280, 420],    '#FBDDE8', '#E87BA8'),
    ('POD(U g$^{-1}$)',           [22, 16, 38, 30],   [15, 30, 45],        '#F7CCDC', '#C2185B'),
    ('APX(U mg$^{-1}$)',          [0.8, 1.2, 1.6, 1.1],[0.5, 1, 1.5],      '#F2F2EC', '#C8C8B8'),
    ('GSH(mg g$^{-1}$)',          [8, 12, 15, 10],    [5, 10, 15],         '#E8F2E0', '#A8D08D'),
    ('GST(U mg$^{-1}$)',          [300, 180, 420, 240],[150, 300, 450],    '#D9EDD0', '#66BB6A'),
    ('GR(U g$^{-1}$)',            [4, 6, 9, 7],       [4, 8, 12],          '#EFE4F5', '#B89AD4'),
    ('GPX(U mg$^{-1}$)',          [800, 950, 1200, 1050],[400, 800, 1200], '#E4D9F2', '#8E6FBF'),
]
BARC = ['#4FA3D8', '#8FC3E4', '#B8D9EE', '#DCEBF7']

fig, ax = plt.subplots(figsize=cm2in(16.5, 16.0), subplot_kw=dict(projection='polar'))
ax.set_theta_zero_location('N'); ax.set_theta_direction(-1)
ax.spines['polar'].set_visible(False)
ax.set_xticks([]); ax.set_yticks([])
ax.set_ylim(0, 4.25)

R0, LENG = 0.72, 2.35
sect = 360.0 / len(traits)

def tang_rot(t):
    rot = 180.0 - t
    while rot > 90:
        rot -= 180
    while rot < -90:
        rot += 180
    return rot

def rad_rot(t):
    rot = 90.0 - t
    while rot > 90:
        rot -= 180
    while rot < -90:
        rot += 180
    return rot

# 虚线刻度圈
for frac in (1 / 3, 2 / 3, 1.0):
    th = np.linspace(0, 2 * np.pi, 361)
    ax.plot(th, np.full_like(th, R0 + frac * LENG), ls=(0, (3, 3)),
            color='#C4C4C4', lw=0.45, zorder=1)

for k, (name, vals, scale, bg, acc) in enumerate(traits):
    tc = k * sect + sect / 2.0
    ax.bar(np.radians(tc), 2.75, bottom=0.55, width=np.radians(sect - 3.5), color=bg,
           edgecolor='white', lw=0.6, zorder=1)
    # 字母按秩分配(并列同名)
    order = np.argsort(vals)[::-1]
    letters = [''] * 4
    prev_v, prev_l = None, ''
    for rank, idx in enumerate(order):
        l = 'abcd'[rank] if vals[idx] != prev_v else prev_l
        letters[idx] = l
        prev_v, prev_l = vals[idx], l
    offs = [-13.5, -4.5, 4.5, 13.5]
    for j, (off, v) in enumerate(zip(offs, vals)):
        ln = v / max(vals) * LENG
        th = tc + off
        ax.bar(np.radians(th), ln, bottom=R0, width=np.radians(5.6),
               color=BARC[j], edgecolor='#5A5A5A', lw=0.5, zorder=3)
        # 误差棒: 沿半径方向跨柱顶, 长为值的 6-10%, 两端切向端帽
        err = ln * r.uniform(0.06, 0.10)
        r1, r2 = R0 + ln - err / 2, R0 + ln + err / 2
        thr, cap = np.radians(th), 0.05
        ax.plot([thr, thr], [r1, r2], color='black', lw=0.7, zorder=5)
        for re_ in (r1, r2):
            ax.plot([thr - cap, thr + cap], [re_, re_], color='black', lw=0.7, zorder=5)
        ax.text(np.radians(th), R0 + ln + err / 2 + 0.13, letters[j], ha='center', va='center',
                fontsize=7.5, fontstyle='italic', fontweight='bold',
                rotation=tang_rot(th), rotation_mode='anchor', zorder=4)
    smax = scale[-1]
    for sv in scale:
        rr = R0 + sv / smax * LENG
        th = tc - sect / 2 + 1.6
        ax.text(np.radians(th), rr, ('%g' % sv), ha='center', va='center',
                fontsize=4.2, color='#333333', rotation=rad_rot(tc), zorder=4)
    ax.text(np.radians(tc), 3.60, name, ha='center', va='center', fontsize=7.8,
            color='#222222', rotation=tang_rot(tc), rotation_mode='anchor')
    ax.bar(np.radians(tc), 0.13, bottom=3.92, width=np.radians(sect - 6),
           color=acc, edgecolor='none', zorder=2)

handles = [Patch(fc=c, ec='#5A5A5A', lw=0.5) for c in BARC]
fig.legend(handles, ['CK', 'Cd', 'GSH', 'GSH+Cd'], loc='upper right',
           bbox_to_anchor=(0.99, 0.99), fontsize=8, frameon=False,
           handlelength=1.2, handleheight=1.0)
save(fig, 'case_seg050.png')
