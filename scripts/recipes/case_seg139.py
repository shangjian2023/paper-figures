# -*- coding: utf-8 -*-
"""案例144(顶刊版) - Cell 内向环形堆叠图: 22 组织扇区 x 4 亚型,
堆叠面积向圆心填充, 扇区间留白, 外圈灰色刻度环(0-0.8), 放射组织标签+右图例。
参考: frames/seg_139.jpg 下方主面板。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

set_style()

tissues = [
    ('brain', '#E8433C'), ('liver', '#7CC24B'), ('spleen', '#3E6DB5'),
    ('muscle', '#F0D24A'), ('artery', '#C46BCB'), ('pancreas', '#7FC4E8'),
    ('heart', '#F0913A'), ('esophagus', '#8E5DA8'), ('skin', '#A8C84A'),
    ('colon', '#E569C4'), ('nerve', '#9AA8E8'), ('ovary', '#E8C84A'),
    ('lung', '#E8D860'), ('stomach', '#E8695A'), ('bonemarrow', '#5AA84A'),
    ('adiposetissue', '#C97B3A'), ('kidney', '#7B5DC9'),
    ('adrenalgland', '#F0A8C0'), ('prostate', '#4AB8B0'),
    ('thyroid', '#F07B6A'), ('bladder', '#B01818'),
    ('smallintestine', '#88B8B0'),
]
NT = len(tissues)
GRAYS = ['#1A1A1A', '#777777', '#ABABAB', '#D4D4D4']   # GLS4..GLS1
gls_names = ['GLS1', 'GLS2', 'GLS3', 'GLS4']

rng = np.random.default_rng(139)
G = rng.dirichlet(np.r_[3.0, 1.6, 1.2, 0.8], NT)        # GLS1..4 比例
G = G / G.sum(1, keepdims=True)

R_OUT, R_HOLE = 0.80, 0.20
GAP_DEG = 3.0
sect_w = 360.0 / NT
gap = np.radians(GAP_DEG)

fig = plt.figure(figsize=cm2in(18.0, 17.5))
ax = fig.add_axes([0.015, 0.02, 0.80, 0.96], projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_ylim(R_HOLE - 0.02, 0.97)
ax.set_xticks([])
ax.set_yticks([])
ax.set_thetamin(0)
ax.set_thetamax(360)
ax.spines['polar'].set_visible(False)
ax.patch.set_visible(False)
ax.grid(False)

tdeg_all = np.linspace(0, 2 * np.pi, 721)


def ring(r_out, r_in, a0, a1, color, zorder=3):
    ta = np.linspace(a0, a1, 90)
    th = np.concatenate([ta, ta[::-1]])
    rr = np.concatenate([np.full_like(ta, r_out), np.full_like(ta, r_in)])
    ax.fill(th, rr, color=color, lw=0, zorder=zorder)


for i, (name, color) in enumerate(tissues):
    c = np.radians((i + 0.5) * sect_w)
    a0, a1 = c - np.radians(sect_w / 2) + gap / 2, c + np.radians(sect_w / 2) - gap / 2
    # 外圈黑边
    ta = np.linspace(a0, a1, 60)
    ax.plot(ta, np.full_like(ta, R_OUT), color='black', lw=1.4, zorder=4)
    # GLS 灰阶弧段(由外向内 GLS4->GLS1, 薄)
    r_top = R_OUT - 0.010
    for k in (3, 2, 1, 0):                    # GLS4,3,2,1
        dk = 0.010 + 0.055 * G[i, k]
        ring(r_top, r_top - dk, a0, a1, GRAYS[k])
        r_top -= dk
    # 组织彩色主体, 内缘白色火焰状深切
    depth = 0.32 + 0.22 * G[i, 0] / G[:, 0].max()
    amp = 0.11 + 0.07 * rng.uniform()
    ph = rng.uniform(0, 2 * np.pi)
    ta = np.linspace(a0, a1, 200)
    u = (ta - a0) / (a1 - a0)
    spikes = (0.5 + 0.5 * np.sin(2 * np.pi * 4 * u + ph)) ** 4
    ripples = 0.25 * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * u + 2 * ph)) ** 2
    jag = amp * (spikes + 0.3 * ripples)
    r_in = np.clip(r_top - depth + jag, R_HOLE + 0.03, 0.72)
    th = np.concatenate([ta, ta[::-1]])
    rr = np.concatenate([np.full_like(ta, r_top), r_in])
    ax.fill(th, rr, color=color, lw=0, zorder=3)
    # 放射组织标签
    tdeg = np.degrees(c)
    rot = -tdeg if tdeg <= 90 or tdeg > 270 else 180 - tdeg
    ha = 'left' if (tdeg < 90 or tdeg > 270) else 'right'
    ax.text(c, 0.86, name, rotation=rot, rotation_mode='anchor', ha=ha,
            va='center', fontsize=6.2, color='#111111', zorder=5)

# 外圈灰色刻度环(0-0.8) + 刻度
ax.plot(tdeg_all, np.full_like(tdeg_all, 0.855), color='#9A9A9A', lw=0.9,
        zorder=2)
for k in range(36):
    a = np.radians(k * 10)
    ax.plot([a, a], [0.855, 0.878], color='#9A9A9A', lw=0.7, zorder=2)
MIN = chr(0x2212)
a_lab = np.radians(315)                      # 左上放射线标数值
for t, lab in [(0.2, '0.2'), (0.4, '0.4'), (0.6, '0.6'), (0.8, '0.8')]:
    ax.text(a_lab, t + 0.058, lab, ha='center', va='center', fontsize=5.5,
            color='#333333', zorder=5, rotation=45)
ax.text(a_lab, 0.222, '0', ha='center', va='center', fontsize=5.5,
        color='#333333', zorder=5, rotation=45)

# 右侧图例(22 组织 + GLS1-4)
handles = [Patch(fc=c, ec='none', label=n) for n, c in tissues]
handles += [Patch(fc=g, ec='none', label=gn)
            for gn, g in zip(gls_names, GRAYS[::-1])]
fig.legend(handles=handles, loc='center right', bbox_to_anchor=(0.995, 0.50),
           frameon=False, fontsize=5.6, handlelength=1.1, handleheight=0.9,
           labelspacing=0.32, borderaxespad=0)

# 环形编码说明: GLS1-4 灰黑环 = 亚型占比, 由外向内
fig.text(0.02, 0.008, 'Note: grey-to-black concentric arcs (GLS1\u2013GLS4, '
         'light to dark) give subtype proportions, stacked from the outer '
         'rim inward.', fontsize=6.5, color='#555555', ha='left', va='bottom')

save(fig, 'case_seg139.png')
