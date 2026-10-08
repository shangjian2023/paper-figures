# -*- coding: utf-8 -*-
"""案例85 - Nature 蜂群图: 上下两节各左右双面板, 红/紫 vs 蓝 蜂群,
0 处黑粗虚线, 左侧括号分组 (Chondrogenic/Osteogenic/Cranial Osteogenic)。
参考: frames/seg_085.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory

set_style()


def beeswarm(vals, dx, dy, max_k=40):
    order = np.argsort(vals)
    offs = np.zeros(len(vals))
    slots = {}
    for idx in order:
        v = vals[idx]
        placed = False
        for kk in range(max_k):
            for off in ([0.0] if kk == 0 else (kk * dy, -kk * dy)):
                slot = int(round(off / dy))
                ok = True
                for s in (slot - 1, slot, slot + 1):
                    for pv in slots.get(s, ()):
                        if abs(pv - v) < dx:
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    offs[idx] = off
                    slots.setdefault(slot, []).append(v)
                    placed = True
                    break
            if placed:
                break
    return offs


rows_top = ['InterzoneChon', 'ChondroPro1', 'ChondroPro2', 'CyclingChon',
            'DLK1$^+$Chon', 'PAX7$^+$Chon', 'ArticularChon1',
            'ArticularChon2', 'FacialChon', 'HypertrophicChon',
            'MandibularChon', 'RestingChon', 'LimbMes', 'LEPR$^+$Mes',
            'CranialMes', 'PArchMes', 'FacialMes', 'SutureMes1',
            'SutureMes2', 'Preosteoblast', 'HHIP$^+$PreOB', 'Osteoblast',
            'Osteocyte', 'MatureOsteocyte', 'Mixed']
rows_bot = rows_top[14:]
# 每行平均 logFC (左面板)
mu_top = np.array([-2.6, -2.9, 3.2, -2.4, -2.2, -2.8, -3.0, 4.2, 5.2, -1.0,
                   4.0, 4.6, 0.2, -0.4, 1.8, 3.8, 3.4, 5.0, 5.0, -3.4, -1.2,
                   0.6, 2.4, 2.2, 0.8])
mu_bot = mu_top[14:]
n_top, n_bot = len(rows_top), len(rows_bot)

fig = plt.figure(figsize=cm2in(15.5, 19.0))
gs = fig.add_gridspec(2, 2, width_ratios=[1.25, 1.0], hspace=0.30,
                      wspace=0.10, left=0.385, right=0.975,
                      top=0.945, bottom=0.065)
axs = [[fig.add_subplot(gs[r, c]) for c in range(2)] for r in range(2)]

DX, DY = 0.16, 0.045   # 上节 (x 范围宽)
DX2, DY2 = 0.035, 0.045

# ---- 上节 ----
for c, ax in enumerate(axs[0]):
    r = rng(85 + c)
    for i in range(n_top):
        yc = n_top - 1 - i
        if c == 0:
            vals = r.normal(mu_top[i], 1.3, 70).clip(-6.2, 8.2)
            dx, dy, col = DX, DY, '#E82040'
        else:
            vals = r.normal(mu_top[i] * 0.10 - 0.06, 0.30, 70).clip(-1.25, 1.25)
            dx, dy, col = DX2, DY2, '#3858B8'
        off = beeswarm(vals, dx, dy)
        ax.scatter(vals, yc + off, s=2.2, c=col, alpha=0.8, linewidths=0,
                   zorder=3)
    ax.axvline(0, c='black', ls=(0, (4, 2.5)), lw=2.4, zorder=4)
    for xv in (-5, 0, 5) if c == 0 else (-1, -0.5, 0.5, 1):
        ax.axvline(xv, c='#E4E4E4', lw=0.8, zorder=0)
    ax.set_xlim(-6.5, 8.5) if c == 0 else ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(n_top - 0.4, -0.6)
    ax.set_yticks([])
    if c == 0:
        ax.set_xticks([-5, 0, 5])
    else:
        ax.set_xticks([-1, -0.5, 0, 0.5, 1],
                      labels=['-1', '-0.5', '0', '0.5', '1'])
    ax.tick_params(labelsize=7.5)
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_linewidth(0.8)
    ax.set_title('Appendicular  $\\leftarrow\\ \\rightarrow$  Cranium'
                 if c == 0 else '5 PCW  $\\leftarrow\\ \\rightarrow$  11 PCW',
                 fontsize=9, pad=4)

# ---- 下节 ----
for c, ax in enumerate(axs[1]):
    r = rng(95 + c)
    for i in range(n_bot):
        yc = n_bot - 1 - i
        if c == 0:
            vals = r.normal(mu_bot[i], 2.3, 60).clip(-8.5, 8.5)
            dx, dy, col = DX2, DY2, '#9020A8'
        else:
            vals = r.normal(mu_bot[i] * 0.16 + 0.05, 0.85, 60).clip(-4.5, 3.0)
            dx, dy, col = 0.055, DY2, '#3858B8'
        off = beeswarm(vals, dx, dy)
        ax.scatter(vals, yc + off, s=2.2, c=col, alpha=0.8, linewidths=0,
                   zorder=3)
    ax.axvline(0, c='black', ls=(0, (4, 2.5)), lw=2.4, zorder=4)
    for xv in (-5, 0, 5) if c == 0 else (-4, -2, 2):
        ax.axvline(xv, c='#E4E4E4', lw=0.8, zorder=0)
    ax.set_xlim(-9, 9) if c == 0 else ax.set_xlim(-4.8, 3.3)
    ax.set_ylim(n_bot - 0.4, -0.6)
    ax.set_yticks([])
    ax.set_xticks([-5, 0, 5] if c == 0 else [-4, -2, 0, 2])
    ax.tick_params(labelsize=7.5)
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_linewidth(0.8)
    ax.set_title('Anterior  $\\leftarrow\\ \\rightarrow$  Posterior'
                 if c == 0 else '5 PCW  $\\leftarrow\\ \\rightarrow$  11 PCW',
                 fontsize=9, pad=4)

# 行标签 + 左侧括号 (仅左面板)
for ri, (ax, rows) in enumerate([(axs[0][0], rows_top), (axs[1][0], rows_bot)]):
    n = len(rows)
    for i, t in enumerate(rows):
        ax.text(-0.04, n - 1 - i, t, transform=ax.get_yaxis_transform(),
                ha='right', va='center', fontsize=7, clip_on=False)
    tr = blended_transform_factory(ax.transAxes, ax.transData)
    groups = [(0, 11, 'Chondrogenic'), (12, 24, 'Osteogenic')] if ri == 0 \
        else [(0, 11, 'Cranial Osteogenic')]
    for g0, g1, lab in groups:
        y0, y1 = n - 1 - g1 - 0.4, n - 1 - g0 + 0.4
        ax.plot([-0.42, -0.42], [y0, y1], c='black', lw=0.9,
                transform=tr, clip_on=False)
        ax.plot([-0.42, -0.375], [y0, y0], c='black', lw=0.9,
                transform=tr, clip_on=False)
        ax.plot([-0.42, -0.375], [y1, y1], c='black', lw=0.9,
                transform=tr, clip_on=False)
        ax.text(-0.465, (y0 + y1) / 2, lab, transform=tr, rotation=90,
                ha='center', va='center', fontsize=7.5, clip_on=False)
    ax.text(-0.04, -0.075, 'logFC', transform=ax.transAxes, ha='left',
            va='top', fontsize=9)

save(fig, 'case_seg085.png')
