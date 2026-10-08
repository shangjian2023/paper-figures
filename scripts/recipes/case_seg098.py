# -*- coding: utf-8 -*-
"""案例100 - iMeta 差异雷达图(一): 20 条组织轴, 3 系列填充多边形+圆点,
虚线 30% 参考圆, 轴标签按组织着色。
参考: frames/seg_098.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()

tissues = ['Pancreas', 'Thymus', 'Bladder', 'Beige fat', 'WAT',
           'Spinal cord', 'Colon', 'Eye', 'Bone', 'Skin', 'Spleen',
           'Small intestine', 'Liver', 'Cerebellum', 'BAT', 'Testis',
           'Kidney', 'Muscle', 'Lung', 'Brain']
M = len(tissues)
tcolor = ['#C0504D', '#C0504D', '#4C9A4A', '#E07B39',
          '#B5A425', '#8A8A2E', '#E07B39', '#9CC98A', '#4C9A4A',
          '#8E5DA8', '#E07B39', '#4A7EBB', '#4C9A4A', '#E07B39',
          '#4A7EBB', '#C0504D', '#C0504D', '#C0504D', '#4C9A4A',
          '#8C8C8C']

step = 360.0 / M
ang = np.radians(np.arange(M) * step)

r = np.random.default_rng(98)
detected = r.uniform(0.38, 0.82, M)
detected[1] = 0.88                       # Thymus 高
detected[15] = 0.42
different = r.uniform(0.10, 0.30, M)
different[1] = 0.62                      # Thymus / 免疫组织高
different[13] = 0.30
different[10] = 0.24
ratio = different / detected * r.uniform(0.85, 1.15, M) * 0.75
ratio = np.clip(ratio, 0.06, 0.24)

series = [
    ('detected features in ratio', detected, '#3B3B5E', '#DDDDF0', 0.55),
    ('different features in ratio', different, '#A5283C', '#EFC9D2', 0.55),
    ('different/detected features in ratio', ratio, '#B8B420', '#EDEDBE',
     0.60),
]

fig = plt.figure(figsize=cm2in(15.0, 17.0))
ax = fig.add_subplot(projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_ylim(0, 1.0)
ax.set_yticks([0, 0.3, 0.6])
ax.set_yticklabels(['', '30%', '60%'], fontsize=8, color='#333333')
for t in ax.get_yticklabels():
    t.set_bbox(dict(facecolor='white', edgecolor='none', pad=0.8))
ax.yaxis.grid(True, color='#CCCCCC', lw=0.6)
ax.set_rlabel_position(189)
ax.set_xticks(ang)

# '0' 刻度标签手动置于中心 (默认 ytick 标签会被系列填充盖住)
ax.text(np.radians(189), 0.045, '0', fontsize=8, color='#333333',
        ha='center', va='center', zorder=6,
        bbox=dict(facecolor='white', edgecolor='none', pad=0.8))
ax.set_thetamin(0)
ax.set_thetamax(360)
ax.spines['polar'].set_visible(True)
ax.spines['polar'].set_linewidth(0.8)
ax.xaxis.grid(True, color='#CCCCCC', lw=0.5)
ax.yaxis.grid(False)
ax.set_xticklabels([])
ax.tick_params(axis='x', pad=14)
ax.tick_params(axis='y', pad=1)

th = np.concatenate([ang, ang[0:1]])
for name, v, ec, fc, alpha in series:
    vv = np.append(v, v[0])
    ax.fill(th, vv, color=ec, alpha=0.35 if fc == '#DDDDF0' else 0.45,
            zorder=2, lw=0)
    ax.plot(th, vv, color=ec, lw=1.1, zorder=3)
    ax.plot(ang, v, 'o', color=ec, ms=3.4, zorder=4)

# 30% 虚线参考圆 (0/30%/60% 刻度环已由 ytick 网格承担, 30% 环加深强调)
tref = np.linspace(0, 2 * np.pi, 361)
ax.plot(tref, np.full_like(tref, 0.30), color='#555555', lw=0.9,
        ls=(0, (5, 3)), zorder=3.5)

# 径向轴标题: 放在 Spleen/Small intestine 之间低值扇区的空白带 (r≈0.73),
# 切向排版 + 白底, 不压任何系列多边形
ax.text(np.radians(189), 0.73, 'Feature ratio (%)', rotation=-9,
        rotation_mode='anchor', ha='center', va='center', fontsize=8.5,
        color='#222222', zorder=6,
        bbox=dict(facecolor='white', edgecolor='none', pad=1.2))

# 组织标签(按组织着色, 径向旋转)
for i, (t, c) in enumerate(zip(tissues, tcolor)):
    tdeg = np.degrees(ang[i])
    rot = -tdeg if tdeg <= 90 or tdeg > 270 else 180 - tdeg
    ha = 'left' if (tdeg < 90 or tdeg > 270) else 'right'
    ax.text(ang[i], 1.06, t, rotation=rot, rotation_mode='anchor', ha=ha,
            va='center', fontsize=7.5, color=c, zorder=5)

handles = [Line2D([], [], color=ec, marker='o', ms=4, lw=1.1)
           for _, _, ec, _, _ in series]
fig.legend(handles, [s[0] for s in series], loc='lower center',
           bbox_to_anchor=(0.52, 0.005), frameon=False, fontsize=8.5,
           labelspacing=0.9, handlelength=1.6)

save(fig, 'case_seg098.png')
