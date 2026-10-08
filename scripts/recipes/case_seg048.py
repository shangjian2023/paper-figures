# -*- coding: utf-8 -*-
"""案例49 - Nature 环形图: 多环参与者环形图。
参考: frames/seg_048.jpg — 约100参与者沿270°弧排布; 内3环=三组指标着色弧段;
外圈红(BMI)/紫(Age)点+放射ID标签; 左上 Age/BMI 点图与 Gender/Ethnicity/Insulin 堆叠条。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Rectangle

set_style()
r = rng(48)
N = 100
ang = 95.0 - 270.0 * np.arange(N) / (N - 1)          # 顺时针从 95° 绕到 -175°, 左侧留缺口
ids = ['Z' + ''.join(r.choice(list('ABCDEFGHJKMNPQRSTUVWXY'), 7)) for _ in range(N)]
age = r.uniform(18, 75, N)
bmi = np.clip(r.normal(28, 5.5, N), 16, 41)
c1, c2, c3 = r.integers(0, 4, N), r.integers(0, 5, N), r.integers(0, 5, N)
R1C = ['#C43C3C', '#E2B56C', '#D97B4F', '#8F2D2D']
R2C = ['#C43C3C', '#E2B56C', '#4E8FCC', '#7FB2D9', '#B7C9D8']
R3C = ['#E2B56C', '#C43C3C', '#4E8FCC', '#E8DCC0', '#6B9AC4']

fig = plt.figure(figsize=cm2in(19.5, 17.5))
ax = fig.add_axes([0.24, 0.02, 0.74, 0.96])
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-6.9, 6.9); ax.set_ylim(-6.5, 6.6)

wid = 270.0 / (N - 1)
for i, a in enumerate(ang):
    for (rr, ci, cmap) in ((1.55, c1[i], R1C), (2.22, c2[i], R2C), (2.89, c3[i], R3C)):
        ax.add_patch(Wedge((0, 0), rr, a - wid * 0.46, a + wid * 0.46,
                           width=0.60, facecolor=cmap[ci], edgecolor='white',
                           lw=0.3, zorder=2))
    ar = np.radians(a)
    ax.plot([0.95 * np.cos(ar), 5.55 * np.cos(ar)],
            [0.95 * np.sin(ar), 5.55 * np.sin(ar)],
            color='#B8B8B8', lw=0.45, zorder=1)
    rb = 3.10 + (bmi[i] - 16) / 25.0 * 0.95          # 红点 = BMI
    ra = 4.30 + (age[i] - 18) / 57.0 * 0.90          # 紫点 = Age
    ax.scatter([rb * np.cos(ar)], [rb * np.sin(ar)], s=11, color='#E03616', zorder=3)
    ax.scatter([ra * np.cos(ar)], [ra * np.sin(ar)], s=13, color='#7A2E8F', zorder=3)
    rot = a % 360
    if 90 < rot <= 270:
        rot -= 180
    ax.text(5.72 * np.cos(ar), 5.72 * np.sin(ar), ids[i], rotation=rot,
            ha='center', va='center', fontsize=3.6, color='#333333')

# 径向刻度数字(弧起点附近): 紫点=Age, 红点=BMI
for v in (75, 51, 21):
    rr = 4.30 + (v - 18) / 57.0 * 0.90
    ar = np.radians(99)
    ax.text(rr * np.cos(ar), rr * np.sin(ar), str(v), fontsize=4.6,
            color='#7A2E8F', ha='right', va='center')
for v in (41, 30, 15):
    rr = 3.10 + (v - 16) / 25.0 * 0.95
    ar = np.radians(103)
    ax.text(rr * np.cos(ar), rr * np.sin(ar), str(v), fontsize=4.6,
            color='#E03616', ha='right', va='center')
# 刻度数字顶部的归属小标题
ar = np.radians(99)
ax.text(5.38 * np.cos(ar), 5.38 * np.sin(ar), 'Age (yrs)', fontsize=4.6,
        color='#7A2E8F', ha='right', va='bottom')
ar = np.radians(103)
ax.text(4.22 * np.cos(ar), 4.22 * np.sin(ar), 'BMI', fontsize=4.6,
        color='#E03616', ha='right', va='bottom')

# ---------------------------------------------------------------- 左侧小面板
def strip_panel(x0, vals, color, title):
    axp = fig.add_axes([x0, 0.615, 0.052, 0.295])
    for s in axp.spines.values():
        s.set_visible(True); s.set_linewidth(0.7)
    axp.set_xticks([]); axp.set_yticks([])
    yy = np.sort(vals)
    xx = r.uniform(0.28, 0.72, len(yy))
    axp.set_xlim(0, 1); axp.set_ylim(min(yy) * 0.92, max(yy) * 1.06)
    q1, q2, q3 = np.percentile(yy, [25, 50, 75])
    for qq, hh in ((q1, 0.14), (q2, 0.20), (q3, 0.14)):
        axp.add_patch(Rectangle((0.28, qq - hh), 0.44, 2 * hh, facecolor='#C8C8C8',
                                edgecolor='#888888', lw=0.4, zorder=2))
    axp.scatter(xx, yy, s=5, color=color, zorder=3)
    axp.set_title(title, fontsize=6.3, pad=2)

strip_panel(0.030, age, '#7A2E8F', 'Age\n(years)')
strip_panel(0.090, bmi, '#E03616', 'BMI')

def stack_panel(x0, segs, colors, title):
    axp = fig.add_axes([x0, 0.615, 0.023, 0.295])
    for s in axp.spines.values():
        s.set_visible(True); s.set_linewidth(0.7)
    bot = 0.0
    for v, c in zip(segs, colors):
        axp.bar(0.5, v, bottom=bot, width=0.94, color=c, edgecolor='white', lw=0.4)
        if v >= 6:
            # 过小(<6%)的分段不放段内数字, 避免被底边裁切
            axp.text(0.5, bot + v / 2, ('%.1f' % v),
                     ha='center', va='center', fontsize=4.2,
                     color='white' if c not in ('#E8DCC0', '#D9B36C', '#E2C68C')
                     else '#555555')
        bot += v
    axp.set_xlim(0, 1); axp.set_ylim(0, 100); axp.set_xticks([]); axp.set_yticks([])
    # 标题 40° 斜排(像 xticklabels 一样彼此平行错开), 单行, 不再互相叠压
    axp.set_title(title, fontsize=5.8, pad=4, rotation=40, ha='left',
                  rotation_mode='anchor')

stack_panel(0.150, [48.1, 51.9], ['#D9B36C', '#C43C4A'], 'Gender (%)')
stack_panel(0.179, [3.5, 68.7, 7.4, 20.4], ['#B0B0B0', '#E2C68C', '#A8CBE4', '#4E8FCC'],
            'Ethnicity (%)')
stack_panel(0.208, [35.2, 31.5, 33.3], ['#B0B0B0', '#C43C4A', '#4E8FCC'],
            'Insulin resp. (%)')

fig.text(0.012, 0.44, 'Participant ID', rotation=90, fontsize=7, va='center')

# ---------------------------------------------------------------- 图例系统(左下空白区)
axl = fig.add_axes([0.030, 0.035, 0.215, 0.42])
axl.set_xlim(0, 1); axl.set_ylim(0, 1)
axl.axis('off')

axl.text(0.02, 0.98, 'Legend', fontsize=7, fontweight='bold', va='center')

def ring_legend_row(y, cmap, label):
    for k, cc in enumerate(cmap):
        axl.add_patch(Rectangle((0.05 + k * 0.052, y - 0.011), 0.040, 0.022,
                                facecolor=cc, edgecolor='#999999', lw=0.3))
    axl.text(0.36, y, label, fontsize=5.4, va='center')

axl.text(0.02, 0.885, 'Arc rings (categorical)', fontsize=5.8,
         color='#333333', va='center')
ring_legend_row(0.795, R1C, 'Inner ring · Variable 1')
ring_legend_row(0.705, R2C, 'Middle ring · Variable 2')
ring_legend_row(0.615, R3C, 'Outer ring · Variable 3')

axl.text(0.02, 0.515, 'Outer dots (radial position)', fontsize=5.8,
         color='#333333', va='center')
axl.scatter([0.065], [0.425], s=13, color='#7A2E8F', zorder=3)
axl.text(0.105, 0.425, 'Age · 18 (inner) → 75 (outer)', fontsize=5.4,
         va='center')
axl.scatter([0.065], [0.345], s=11, color='#E03616', zorder=3)
axl.text(0.105, 0.345, 'BMI · 16 (inner) → 41 (outer)', fontsize=5.4,
         va='center')

axl.text(0.02, 0.25, 'Scale digits at arc origin', fontsize=5.8,
         color='#333333', va='center')
axl.text(0.05, 0.165, '75 · 51 · 21 = Age (yrs)', fontsize=5.2,
         color='#7A2E8F', va='center')
axl.text(0.05, 0.085, '41 · 30 · 15 = BMI', fontsize=5.2,
         color='#E03616', va='center')

save(fig, 'case_seg048.png')
