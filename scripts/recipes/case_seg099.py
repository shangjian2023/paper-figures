# -*- coding: utf-8 -*-
"""案例101 - Nature 差异雷达图(二): 14 亚区轴, D1(橙红)/D2(绿) 两系列,
径向 400/800 虚线刻度环, * 显著性, 外圈黑弧分段标 CA1/CA3/DG。
参考: frames/seg_099.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt

set_style()

# 14 亚区轴: dSub + CA1(5) + vSub + DG(4) + CA3(3)
regions = ['dSub', 'so', 'py', 'sr', 'slm', 'rad', 'vSub', 'mo', 'gc',
           'hil', 'iml', 'so', 'py', 'sr']
groups = [('CA1', 1, 5), ('vSub', 6, 6), ('DG', 7, 10), ('CA3', 11, 13)]
M = len(regions)
step = 360.0 / M
ang = np.radians(np.arange(M) * step)

D1 = np.array([300, 430, 320, 270, 230, 210, 490, 350, 300, 520, 260,
               410, 300, 400], float)
D2 = np.array([320, 390, 290, 250, 215, 200, 570, 290, 330, 880, 240,
               330, 260, 300], float)

stars = {3: ('*', 360), 4: ('**', 330), 7: ('***', 430), 9: ('***', 1000),
         6: ('***', 700), 12: ('**', 400), 13: ('***', 490), 10: ('*', 330)}

fig = plt.figure(figsize=cm2in(14.5, 15.5))
ax = fig.add_subplot(projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_ylim(0, 1080)
ax.set_rorigin(-320)
ax.set_yticks([400, 800])
ax.set_yticklabels(['400', '800'], fontsize=11)
ax.set_rlabel_position(9)
ax.set_xticks(ang)
ax.set_xticklabels([])
ax.set_thetamin(0)
ax.set_thetamax(360)
ax.spines['polar'].set_visible(False)
ax.grid(True, axis='y', color='#B8B8B8', lw=1.0, ls=(0, (5, 3)))
ax.grid(True, axis='x', color='#B0B0B0', lw=1.2)
ax.tick_params(pad=10)

th = np.concatenate([ang, ang[0:1]])
ax.plot(th, np.append(D1, D1[0]), '-', color='#C1440E', lw=1.7, zorder=3)
ax.plot(ang, D1, 'o', color='#C1440E', ms=4.2, zorder=4)
ax.plot(th, np.append(D2, D2[0]), '-', color='#199A6E', lw=1.7, zorder=3)
ax.plot(ang, D2, 'o', color='#199A6E', ms=4.2, zorder=4)

# 显著性星号(径向旋转)
for i, (txt, rr) in stars.items():
    tdeg = np.degrees(ang[i])
    rot = -tdeg if tdeg <= 90 or tdeg > 270 else 180 - tdeg
    ax.text(ang[i], rr, txt, rotation=rot, rotation_mode='anchor',
            ha='center', va='center', fontsize=7.5, color='#111111',
            zorder=5)

# 亚区标签(内侧, 黑色, 径向旋转)
for i, name in enumerate(regions):
    tdeg = np.degrees(ang[i])
    rot = -tdeg if tdeg <= 90 or tdeg > 270 else 180 - tdeg
    ha = 'left' if (tdeg < 90 or tdeg > 270) else 'right'
    ax.text(ang[i], 1150, name, rotation=rot, rotation_mode='anchor',
            ha=ha, va='center', fontsize=10, color='#111111', zorder=5)

# 外圈黑色分组弧 + 组名
tarc = np.linspace(0, 2 * np.pi, 721)
ax.plot(tarc, np.full_like(tarc, 1330), color='#222222', lw=1.0,
        zorder=2, clip_on=False)
for name, i1, i2 in groups:
    a1 = ang[i1] - np.radians(step * 0.42)
    a2 = ang[i2] + np.radians(step * 0.42)
    ta = np.linspace(a1, a2, 60)
    ax.plot(ta, np.full_like(ta, 1420), color='#111111', lw=1.7,
            solid_capstyle='butt', zorder=4, clip_on=False)
    if name != 'vSub':
        amid = (a1 + a2) / 2
        tdeg = np.degrees(amid)
        rot = -tdeg if tdeg <= 90 or tdeg > 270 else 180 - tdeg
        ax.text(amid, 1620, name, rotation=rot, rotation_mode='anchor',
                ha='center', va='center', fontsize=11.5, color='#111111',
                zorder=5)
    else:
        vd = np.degrees(ang[i1])
        vrot = -vd if vd <= 90 or vd > 270 else 180 - vd
        vha = 'left' if vd <= 90 or vd > 270 else 'right'
        ax.text(ang[i1], 1620, 'vSub', rotation=vrot,
                rotation_mode='anchor', ha=vha, va='center',
                fontsize=11.5, color='#111111', zorder=5)
# dSub(单轴)标签
ax.text(0, 1620, 'dSub', rotation=0, ha='center', va='center',
        fontsize=11.5, color='#111111', zorder=5)

# 轴名称 + 图例
fig.text(0.50, 0.965, 'Density (cells mm$^{-2}$)', ha='center',
         fontsize=11)
handles = [plt.Line2D([], [], color=c, marker='o', ms=4.5, lw=1.7)
           for c in ('#C1440E', '#199A6E')]
fig.legend(handles, ['D1', 'D2'], loc='upper right',
           bbox_to_anchor=(0.97, 0.985), frameon=False, fontsize=10,
           labelspacing=0.4, handlelength=1.6)

save(fig, 'case_seg099.png')
