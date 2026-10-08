# -*- coding: utf-8 -*-
"""案例62 - Nature 多边形雷达图: 五边形雷达对比(粉红大五边形 vs 蓝色小五边形)。
参考: frames/seg_060.jpg — 5 轴材料属性, 顶点白字数值, 黑虚线边界, 底部图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch

set_style()

angs = np.radians([90, 18, -54, -126, -198])       # 顶/右上/右下/左下/左上
R = 1.0

vmax_lbl = ['2.43', '2,100', '90', '1,050', r'1 $\times$ 10$^{16}$']
ours_lbl = ['2.36', '1,300', '49.5', '293', r'1 $\times$ 10$^{10}$']
# 顺序: 折射率, 热导, 硬度, 杨氏模量, 电阻(对数比)
ours_rat = np.array([2.36 / 2.43, 1300 / 2100, 49.5 / 90, 293 / 1050,
                     np.log10(1e10) / np.log10(1e16)])

titles = ['Optical refractive index (at 450 nm)',
          'Thermal conductivity\nW m$^{-1}$ K$^{-1}$',
          'Mechanical hardness\n(GPa)',
          "Young's modulus\n(GPa)",
          'Electrical resistance\n(\u03a9)']

fig = plt.figure(figsize=cm2in(14.0, 15.5))
ax = fig.add_axes([0.02, 0.16, 0.96, 0.80])
ax.set_xlim(-2.10, 2.10)
ax.set_ylim(-1.62, 1.66)
ax.set_aspect('equal')
ax.axis('off')

# 虚线辐条
for t in angs:
    ax.plot([0, R * np.cos(t)], [0, R * np.sin(t)], color='#999999',
            lw=0.7, ls=(0, (4, 3)), zorder=1)

# 粉红五边形 = 标准最大值
sq = np.column_stack([R * np.cos(angs), R * np.sin(angs)])
ax.add_patch(Polygon(sq, closed=True, fc='#F5A9BC', ec='#E8889F', lw=1.2,
                     alpha=0.95, zorder=2))
# 黑虚线外边界
ax.plot(np.append(sq[:, 0], sq[0, 0]), np.append(sq[:, 1], sq[0, 1]),
        color='#1A1A1A', lw=1.1, ls=(0, (4, 2.4)), zorder=4)

# 蓝色五边形 = 我们的金刚石膜
ob = np.column_stack([ours_rat * R * np.cos(angs), ours_rat * R * np.sin(angs)])
ax.add_patch(Polygon(ob, closed=True, fc='#B2ABDC', ec='#847CC2', lw=1.3,
                     alpha=0.85, zorder=3))
ax.plot(ob[:, 0], ob[:, 1], 'o', color='#6C63A8', ms=3.2, zorder=5)

# 顶点白字数值(蓝多边形顶点稍内侧)
for t, rat, lab in zip(angs, ours_rat, ours_lbl):
    ax.text(0.80 * rat * R * np.cos(t), 0.80 * rat * R * np.sin(t), lab,
            ha='center', va='center', color='white', fontsize=10.5, zorder=6)

# 外圈最大值 + 轴标题
for i, (t, vlab, tit) in enumerate(zip(angs, vmax_lbl, titles)):
    c, s = np.cos(t), np.sin(t)
    vx, vy = 1.13 * R * c, 1.13 * R * s
    if i == 0:
        ax.text(vx, vy, vlab, ha='center', va='bottom', fontsize=10.5)
        ax.text(0, 1.36 * R, tit, ha='center', va='bottom', fontsize=9.5)
    elif i == 1:
        ax.text(vx + 0.07, vy, vlab, ha='left', va='center', fontsize=10.5)
        ax.text(1.52 * R, vy - 0.20, tit, ha='left', va='top', fontsize=9.5)
    elif i == 2:
        ax.text(vx + 0.07, vy, vlab, ha='left', va='center', fontsize=10.5)
        ax.text(1.52 * R, vy - 0.28, tit, ha='left', va='top', fontsize=9.5)
    elif i == 3:
        ax.text(vx - 0.07, vy, vlab, ha='right', va='center', fontsize=10.5)
        ax.text(-1.52 * R, vy - 0.28, tit, ha='right', va='top',
                fontsize=9.5)
    else:
        ax.text(vx - 0.07, vy, vlab, ha='right', va='center', fontsize=10.5)
        ax.text(-1.52 * R, vy + 0.20, tit, ha='right', va='bottom',
                fontsize=9.5)

# 底部图例
handles = [Patch(fc='#B2ABDC', ec='#847CC2', label='Our diamond membrane'),
           Patch(fc='#F5A9BC', ec='#E8889F', label='Standard SCD')]
leg = ax.legend(handles=handles, loc='upper center',
                bbox_to_anchor=(0.5, -0.06), ncol=1, frameon=False,
                fontsize=10, handlelength=1.2, handleheight=1.0,
                borderaxespad=0)

save(fig, 'case_seg060.png')
