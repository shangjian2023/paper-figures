# -*- coding: utf-8 -*-
"""案例63 - Cancer Cell 拟合散点图: 彩色散点 + 黑回归线灰置信带 + 轴端箭头注释 + 引线标签 + r/P。
参考: frames/seg_061.jpg — 亚群响应 vs 肿瘤富集, 负相关 r=0.64。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

r = rng(61)

# ---- 合成数据: 负相关, x=肿瘤富集分数, y=响应指数 Ti
n = 46
x = np.concatenate([r.normal(-45, 22, 16), r.normal(5, 18, 14), r.normal(42, 20, 16)])
x = np.clip(x, -72, 78)
y = 0.055 - 0.0038 * x + r.normal(0, 0.065, n)
y = np.clip(y, -0.31, 0.46)

names = ['c05_CD4$^+$ Tcm', 'c18_CD8$^+$ Tcm', 'c21_CD8$^+$ Trm', 'c73_ADAMEC1$^+$ Fibro',
         'c46_IgA$^+$ Plasma', 'c77_ACTA2$^+$ Fibro', 'c74_C7$^+$ Fibro', 'c65_APOE$^+$ Mph',
         'c64_SPP1$^+$ Mph', 'c70_Endo', 'c53_Neutrophil', 'c23_Tex', 'c13_4-1BB$^+$ Treg']
colors = pal('set3') + ['#6A3D9A', '#E31A1C', '#33A02C', '#FF7F00']

fig, ax = plt.subplots(figsize=cm2in(11.5, 11.0))

# 置信带 + 回归线
b1, b0 = np.polyfit(x, y, 1)
res = y - (b0 + b1 * x)
s = res.std(ddof=2)
xg = np.linspace(-72, 78, 100)
xbar = x.mean()
Sxx = ((x - xbar)**2).sum()
ci = 2.02 * s * np.sqrt(1.0 / n + (xg - xbar)**2 / Sxx)
ax.fill_between(xg, b0 + b1 * xg - ci, b0 + b1 * xg + ci, color='0.85', zorder=1)
ax.plot(xg, b0 + b1 * xg, color='black', lw=1.3, zorder=3)

ax.scatter(x, y, s=62, c=[colors[i % len(colors)] for i in range(n)],
           edgecolor='white', linewidth=0.5, zorder=4)

ax.axvline(0, ls='--', lw=1.0, color='black')
ax.axhline(0, ls='--', lw=1.0, color='black')

# ---- 引线标签(挑代表点): 标签放引线终点外侧, 引线只到文字盒侧缘旁, 不穿字
targets = {'c05': -18, 'c18': -57, 'c21': 8, 'c73': -30.5, 'c46': -42,
           'c77': 18, 'c74': -8, 'c65': 30, 'c64': 34, 'c70': 52,
           'c53': 20, 'c23': 74}
idx = {nm: int(np.argmin(np.abs(x - kk))) for nm, kk in targets.items()}
# c13: 右侧(x>35)最低的未标注点, 标签放其左侧空白区
used = set(idx.values())
cand = [i for i in range(n) if x[i] > 40 and i not in used]
i13 = min(cand, key=lambda i: y[i])
idx['c13'] = i13
lbl = [('c05_CD4$^+$ Tcm', (-52, 0.475)),
       ('c18_CD8$^+$ Tcm', (-55, 0.395)),
       ('c21_CD8$^+$ Trm', (12, 0.435)),
       ('c73_ADAMEC1$^+$ Fibro', (-74, 0.29)),
       ('c46_IgA$^+$ Plasma', (-70, 0.145)),
       ('c77_ACTA2$^+$ Fibro', (20, 0.30)),
       ('c74_C7$^+$ Fibro', (-30, 0.185)),
       ('c65_APOE$^+$ Mph', (33, 0.235)),
       ('c64_SPP1$^+$ Mph', (33, -0.115)),
       ('c70_Endo', (42, -0.225)),
       ('c53_Neutrophil', (2, -0.205)),
       ('c23_Tex', (60, -0.30))]
lbl.append(('c13_4-1BB$^+$ Treg', (-12, -0.305)))   # 底部空白带, 引线斜向右上
GAP = 2.2
ltexts = []
for txt, (tx, ty) in lbl:
    t = ax.text(tx, ty, txt, fontsize=8, zorder=6, va='center')
    ltexts.append((t, txt.split('_')[0]))
fig.canvas.draw()                                  # 实测文字包围盒再布引线
ren = fig.canvas.get_renderer()
inv = ax.transData.inverted()
for t, key in ltexts:
    bb = t.get_window_extent(renderer=ren)
    (bx0, by0), (bx1, by1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    i = idx[key]
    X, Y = x[i], y[i]
    ty = t.get_position()[1]
    ex = bx1 + GAP if X >= (bx0 + bx1) / 2 else bx0 - GAP
    if Y < by0:                                    # 端点高度贴盒缘, 线段不进文字盒
        ey = by0
    elif Y > by1:
        ey = by1
    else:
        ey = by0 if Y < (by0 + by1) / 2 else by1
    ax.plot([X, ex], [Y, ey], lw=0.7, color='0.25', zorder=2,
            solid_capstyle='round')

# ---- 右上 r/P
ax.text(0.985, 0.985, 'r = 0.64\n$P$ = 8.6e-08', transform=ax.transAxes,
        ha='right', va='top', fontsize=9)

# ---- 先定轴范围, 再画四支轴端方向箭头
# (annotate 默认 annotation_clip: xy 落在最终轴外时整条不画, 必须 annotation_clip=False)
PUR, CYA = '#7B2D8E', '#3B9DE8'
ax.set_xlim(-76, 80)
ax.set_ylim(-0.34, 0.52)
ax.annotate('', xy=(-76, 0.515), xytext=(-76, 0.10), annotation_clip=False,
            arrowprops=dict(arrowstyle='-|>', color=PUR, lw=1.6,
                            shrinkA=0, shrinkB=0))
ax.annotate('', xy=(-76, -0.335), xytext=(-76, -0.10), annotation_clip=False,
            arrowprops=dict(arrowstyle='-|>', color=CYA, lw=1.6,
                            shrinkA=0, shrinkB=0))
ax.text(-0.145, 0.78, 'Greater increase', transform=ax.transAxes, rotation=90,
        ha='center', va='center', fontsize=8.5)
ax.text(-0.145, 0.16, 'Greater decrease', transform=ax.transAxes, rotation=90,
        ha='center', va='center', fontsize=8.5)
ax.text(-0.225, 0.47, 'indicates better response (Ti)', transform=ax.transAxes,
        rotation=90, ha='center', va='center', fontsize=9.5)

ax.set_xticks([-50, 0, 50])
ax.set_yticks([-0.25, 0, 0.25, 0.50])
ax.set_yticklabels(['$-0.25$', '0.00', '0.25', '0.50'])
ax.tick_params(bottom=False)
for s_ in ('top', 'right'):
    ax.spines[s_].set_visible(False)

# x 轴下方的方向箭头与文字(蓝=normal/decrease 方向, 紫=tumor/increase 方向);
# 箭头放在刻度数字之下, 避免压住 -50/50 刻度
ax.annotate('', xy=(-76, -0.42), xytext=(-4, -0.42), annotation_clip=False,
            arrowprops=dict(arrowstyle='-|>', color=CYA, lw=1.6,
                            shrinkA=0, shrinkB=0))
ax.annotate('', xy=(80, -0.42), xytext=(6, -0.42), annotation_clip=False,
            arrowprops=dict(arrowstyle='-|>', color=PUR, lw=1.6,
                            shrinkA=0, shrinkB=0))
ax.text(-38, -0.47, 'Enriched in normal', ha='center', fontsize=10, clip_on=False)
ax.text(38, -0.47, 'Enriched in tumor', ha='center', fontsize=10, clip_on=False)
ax.set_xlabel('Tumor enrichment', fontsize=10, labelpad=44)

save(fig, 'case_seg061.png')
