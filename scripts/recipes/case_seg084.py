# -*- coding: utf-8 -*-
"""案例84 - Nature 蜂群图: 21 行细胞类型, 左红(early)右紫(late)蜂群 + 右侧
半小提琴, 近 0 渐透明, 0 处竖虚线, 左轴类型色条, 底部双向箭头 log(FC)。
参考: frames/seg_084.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.patches import Rectangle

set_style()


def beeswarm(vals, dx, dy, max_k=40):
    """简单蜂群布局: 返回每个点的行内偏移。"""
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


types = ['Neural cell', 'Megakaryocyte', 'Fibroblast', 'Macrophage',
         'Neutrophil', 'Haem progenitor', 'DC', 'Melanocyte', 'ILC',
         'Skeletal muscle', 'Mural cell', 'Vascular endothelium', 'Monocyte',
         'Schwann cell', 'Adipocyte', 'Mast cell', 'Erythroid',
         'Lymphatic endothelium', 'Keratinocyte', 'T cell', 'B cell']
chips = ['#3CB8A8', '#F0A8B8', '#F8E0C0', '#7A1030', '#8090C0', '#283898',
         '#C07880', '#88D8C8', '#7A88C0', '#B8E8A0', '#78B858', '#D82870',
         '#4878C8', '#E88820', '#F0B880', '#A8B8E8', '#E87080', '#28A838',
         '#B8E8D8', '#C8C8D0', '#C0A8B0']

# 每行平均 logFC: 负值行(early 富集) 与幅度
mu_early = np.array([-0.55, -0.75, -0.55, -0.60, -0.80, -0.85, -0.45, -0.85,
                     -0.85, -0.35, -0.80, -0.75, -0.60, -0.70, -0.75, -0.55,
                     -0.62, -0.30, -0.80, -0.20, -0.25])
r = rng(84)
nrow = len(types)

fig, ax = plt.subplots(figsize=cm2in(13.5, 17.0))
DX, DY = 0.030, 0.042
for i, t in enumerate(types):
    yc = nrow - 1 - i
    m = abs(mu_early[i])
    # 左侧实心半小提琴 (红, Early) + 红蜂群 (对数正态避免边界堆积)
    vL = -r.lognormal(np.log(0.40 * m + 0.12), 0.52, 130).clip(0.01, 1.05)
    kL = gaussian_kde(vL)
    gxL = np.linspace(vL.min() * 1.05, -0.001, 90)
    wL = 0.38 * kL(gxL) / kL(gxL).max()
    ax.fill(np.concatenate([gxL, gxL[::-1]]),
            np.concatenate([yc - wL, (yc + wL)[::-1]]),
            facecolor='#B23A3A', edgecolor='none', alpha=0.60, zorder=1)
    offL = beeswarm(vL, DX, DY)
    aL = 0.10 + 0.90 * np.minimum(np.abs(vL) / 0.9, 1.0)
    ax.scatter(vL, yc + offL, s=4.5, c='#B23A3A', alpha=aL, linewidths=0,
               zorder=3)
    # 右侧实心半小提琴 (紫, Late) + 紫蜂群
    vR = r.lognormal(np.log(0.42 * m + 0.14), 0.52, 130).clip(0.01, 1.05)
    kR = gaussian_kde(vR)
    gxR = np.linspace(0.001, vR.max() * 1.05, 90)
    wR = 0.38 * kR(gxR) / kR(gxR).max()
    ax.fill(np.concatenate([[0], gxR, gxR[::-1], [0]]),
            np.concatenate([[yc], yc - wR, yc + wR[::-1], [yc]]),
            facecolor='#8878C8', edgecolor='none', alpha=0.85, zorder=1)
    offR = beeswarm(vR, DX, DY)
    aR = 0.10 + 0.90 * np.minimum(np.abs(vR) / 0.9, 1.0)
    ax.scatter(vR, yc + offR, s=4.5, c='#5A50A0', alpha=aR, linewidths=0,
               zorder=3)
    # 左侧标签 + 色条
    ax.text(-1.30, yc, t, ha='right', va='center', fontsize=8.5,
            clip_on=False)
    ax.add_patch(Rectangle((-1.24, yc - 0.32), 0.045, 0.64, facecolor=chips[i],
                           edgecolor='none', clip_on=False, zorder=5))

ax.axvline(0, ls=(0, (4, 3)), c='#909090', lw=1.0, zorder=2)
ax.set_xlim(-1.12, 1.12)
ax.set_ylim(-0.8, nrow - 0.2)
ax.set_xticks([-1, 0, 1])
ax.set_yticks([])
ax.tick_params(labelsize=9)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.plot([-1.12, 1.12], [-0.8, -0.8], c='black', lw=0.8, clip_on=False)

# 底部双向箭头注记
ax.annotate('', xy=(0.66, -0.125), xytext=(-0.66, -0.125),
            xycoords=('data', 'axes fraction'),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.0))
ax.text(0.0, -0.085, 'log(fold change)', ha='center', va='bottom',
        transform=ax.get_xaxis_transform(), fontsize=8.5)
ax.text(-0.66, -0.125, 'Early gestation', ha='right', va='center',
        transform=ax.get_xaxis_transform(), fontsize=8.5)
ax.text(0.66, -0.125, 'Late gestation', ha='left', va='center',
        transform=ax.get_xaxis_transform(), fontsize=8.5)

fig.subplots_adjust(left=0.24, right=0.97, top=0.985, bottom=0.09)
save(fig, 'case_seg084.png')
