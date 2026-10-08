# -*- coding: utf-8 -*-
"""案例50a - J.Hazard Mat. 环状柱形图(一): 8性状扇区×3处理径向柱。
参考: frames/seg_049.jpg — 淡彩底楔+3根深浅蓝径向柱, 柱端a/b/c字母,
径向刻度数字, 外弧彩色弧条+性状名沿弧旋转, 右上KB/BC/BAc图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

set_style()

# (性状, 3处理值[KB,BC,BAc], 径向刻度, 底色, 外弧色) — 单位按根系性状真实量级:
# 根径 µm(细根 100-800), 根体积 cm³, 表面积 cm², 总根长 cm, 其余为计数
traits = [
    ('Crossings',      [320, 210, 95],      [130, 260, 390],           '#FCE7F0', '#444444'),
    ('Length(cm)',     [9200, 5600, 2300],  [2500, 5000, 7500, 10000], '#FBE3EC', '#F06CA8'),
    ('SurfArea(cm$^2$)',[780, 490, 210],    [280, 560, 840],           '#FADCE7', '#D81B60'),
    ('AvgDiam(µm)',    [490, 310, 160],     [180, 360, 540],           '#D9EED9', '#43A047'),
    ('RootVolume(cm$^3$)', [410, 290, 130], [110, 220, 330, 440],      '#E8F3E4', '#66BB6A'),
    ('Tips',           [10800, 7100, 3400], [3800, 7600, 11400],       '#EFF6EA', '#A5D6A7'),
    ('Forks',          [8900, 5600, 2500],  [3000, 6000, 9000],        '#FDF6DC', '#F2E28A'),
    ('Branches',       [5200, 3300, 1500],  [2000, 4000, 6000],        '#FDF6DC', '#E8E38F'),
]
BARC = ['#3D8EC9', '#8FC3E4', '#C9E2F2']

fig, ax = plt.subplots(figsize=cm2in(15.5, 15.0), subplot_kw=dict(projection='polar'))
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

for k, (name, vals, scale, bg, acc) in enumerate(traits):
    tc = k * sect + sect / 2.0
    tw = np.radians(sect - 5)
    ax.bar(np.radians(tc), 2.75, bottom=0.55, width=tw, color=bg,
           edgecolor='white', lw=0.6, zorder=1)
    offs = [sect / 2 - 8.5, sect / 2, sect / 2 + 8.5]
    for j, (off, v) in enumerate(zip(offs, vals)):
        ln = v / max(vals) * LENG * (0.45 + 0.55 * j / 2) if False else v / max(vals) * LENG
        th = k * sect + off
        ax.bar(np.radians(th), ln, bottom=R0, width=np.radians(6.8),
               color=BARC[j], edgecolor='#5A5A5A', lw=0.5, zorder=3)
        ax.text(np.radians(th), R0 + ln + 0.13, 'abc'[j], ha='center', va='center',
                fontsize=8.5, fontstyle='italic', fontweight='bold',
                rotation=tang_rot(th), rotation_mode='anchor', zorder=4)
    smax = scale[-1]
    for sv in scale:
        rr = R0 + sv / smax * LENG
        th = k * sect + 1.5
        lab = '%d' % sv if sv >= 1000 else '%g' % sv
        ax.text(np.radians(th), rr, lab, ha='center', va='center',
                fontsize=4.2, color='#333333', rotation=rad_rot(th + sect / 2 - 1.5),
                rotation_mode='anchor', zorder=4)
    ax.text(np.radians(tc), 3.62, name, ha='center', va='center', fontsize=8.5,
            color='#222222', rotation=tang_rot(tc), rotation_mode='anchor')
    ax.bar(np.radians(tc), 0.13, bottom=3.92, width=np.radians(sect - 9),
           color=acc, edgecolor='none', zorder=2)

handles = [Patch(fc=c, ec='#5A5A5A', lw=0.5) for c in BARC]
fig.legend(handles, ['KB', 'BC', 'BAc'], loc='upper right', bbox_to_anchor=(0.99, 0.99),
           fontsize=8, frameon=False, handlelength=1.2, handleheight=1.0)
save(fig, 'case_seg049.png')
