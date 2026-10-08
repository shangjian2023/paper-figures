# -*- coding: utf-8 -*-
"""案例135 - 双曲线边界火山图: 黑虚线双曲线显著性边界, 中央黑色非显著云,
左侧浅蓝/右侧浅紫显著基因集, 重点基因彩色大点+斜体标签。
x=Knockdown Phenotype (AU), y=-log10P。参考: frames/seg_135.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()
r = rng(135)


def boundary(x):
    """双曲线边界: |x| = 0.35 + 0.85 / y  ->  y = 0.85/(|x|-0.35)"""
    return 0.85 / (np.abs(x) - 0.35)


fig, ax = plt.subplots(figsize=cm2in(13.5, 11.5))
fig.subplots_adjust(left=0.115, right=0.975, top=0.97, bottom=0.10)

# ---------------- 边界虚线 (先画, 点压在上面)
yy = np.linspace(0.24, 4.45, 300)
for sgn in (-1, 1):
    ax.plot(sgn * (0.35 + 0.85 / yy), yy, ls=(0, (3, 2)), color='black',
            lw=1.1, zorder=4)

# ---------------- 中央黑色非显著云
nb = 4800
xb = np.clip(r.normal(0, 0.30, nb), -0.72, 0.72)
yb = r.exponential(0.85, nb)
keep = yb < 4.26
ax.scatter(xb[keep], yb[keep], s=8, color='0.05', alpha=0.38, lw=0, zorder=2)
ng = 900
xg = np.clip(r.normal(0, 0.55, ng), -1.05, 1.05)
yg = r.exponential(0.55, ng)
kg = yg < 1.8
ax.scatter(xg[kg], yg[kg], s=9, color='0.55', alpha=0.30, lw=0, zorder=2)

# ---------------- 左浅蓝 / 右浅紫显著云
def side_cloud(x0, x1, n, color):
    pts = []
    while len(pts) < n:
        xx = r.uniform(x0, x1)
        ym = boundary(np.clip(abs(xx), 0.45, 3.2)) + 0.06
        if ym >= 4.2:
            # 靠近顶帽会堆叠成平头一行 → 向下抖散, 保持完整圆点
            yv = 4.2 - r.uniform(0, 0.5)
        else:
            yv = r.uniform(ym, 4.2)
        pts.append((xx, yv))
    pts = np.array(pts)
    ax.scatter(pts[:, 0], pts[:, 1], s=26, color=color, alpha=0.45, lw=0,
               zorder=3)

side_cloud(-3.15, -0.40, 430, '#a8cede')
side_cloud(0.42, 2.65, 300, '#c9a8cd')

# ---------------- 重点基因大点 + 斜体标签
KEY = [
    # (gene, x, y, color)
    ('MAPT', -2.62, 3.83, '#e8c832'),
    ('PIGK', -1.75, 3.93, '#2233aa'),
    ('PIGT', -1.02, 3.93, '#2233aa'),
    ('PIGL', -0.60, 3.93, '#2233aa'),
    ('PIGS_P', -1.42, 3.70, '#2233aa'),
    ('MTOR', -1.68, 3.42, '#3ba83b'),
    ('PIGC', -0.52, 3.66, '#2233aa'),
    ('USP16', -0.40, 3.62, '#2233aa'),
    ('PIGF', -0.60, 3.42, '#2233aa'),
    ('PIGA', -0.34, 3.22, '#2233aa'),
    ('PIGB', -1.80, 3.00, '#3ba83b'),
    ('PIGQ', -1.18, 3.08, '#2233aa'),
    ('USP22', -0.44, 2.85, '#2233aa'),
    ('UBA5', -1.88, 2.50, '#d97a1a'),
    ('USP10', -1.50, 2.58, '#2233aa'),
    ('UFC1', -1.18, 2.35, '#d97a1a'),
    ('PIGH', -0.80, 2.32, '#d97a1a'),
    ('UFM1', -0.90, 2.10, '#d97a1a'),
    ('PIGV', -1.08, 1.75, '#2233aa'),
    ('PIGW', -1.18, 1.30, '#2233aa'),
    ('ARIH2', 0.78, 3.85, '#7b3fa0'),
    ('SOCS4', 1.55, 3.90, '#7b3fa0'),
    ('WIP12', 2.05, 3.90, '#7b3fa0'),
    ('CUL5', 2.42, 3.78, '#7b3fa0'),
    ('ATG14', 1.78, 3.68, '#3ba83b'),
    ('LAMTOR5', 1.18, 3.55, '#7b3fa0'),
    ('KEAP1', 1.92, 3.45, '#7b3fa0'),
    ('SOCS3', 0.38, 1.90, '#7b3fa0'),
    ('RNF7', 1.62, 1.80, '#7b3fa0'),
]
for g, x, y, c in KEY:
    ax.scatter([x], [y], s=64, color=c, edgecolor='white', linewidth=0.6,
               zorder=6)
    dx = 0.10 if x < 0 else -0.10
    dy = 0.0
    ha = 'left' if x < 0 else 'right'
    # PIGC 上移 / USP16 下移, 消除两者标签重叠
    if g == 'PIGC':
        dy = 0.09
    elif g == 'USP16':
        dx, dy = 0.11, -0.09
    if g in ('PIGT', 'PIGL', 'PIGS_P', 'MTOR', 'SOCS4', 'WIP12', 'CUL5',
             'ATG14', 'LAMTOR5', 'KEAP1'):
        ha, dx = ('left', 0.10) if x < 0 else ('right', -0.10)
    if g == 'SOCS4':
        ha, dx = 'center', 0.0
        ax.annotate(italic_gene(g), (x, y), xytext=(x - 0.28, y + 0.13),
                    fontsize=7.2, ha='center', zorder=7)
        continue
    ax.text(x + dx, y + dy, italic_gene(g), fontsize=7.2, va='center', ha=ha,
            zorder=7)

ax.set_xlim(-3.35, 3.0)
ax.set_ylim(0, 4.45)
ax.set_xticks([-2, 0, 2])
ax.set_yticks([0, 1, 2, 3, 4])
ax.tick_params(labelsize=8)
ax.set_xlabel('Knockdown Phenotype (AU)', fontsize=10)
ax.set_ylabel('$-$log$_{10}$P', fontsize=10)
despine(ax)

# 通路家族图例 (蓝/橙/绿/紫/黄)
fam = [('#2233aa', 'GPI-anchor pathway'), ('#d97a1a', 'UFMylation'),
       ('#3ba83b', 'Autophagy / mTOR'), ('#7b3fa0', 'Cullin-RING / SOCS'),
       ('#e8c832', 'Control')]
fam_h = [Line2D([], [], marker='o', ls='', color=c, ms=5, label=l)
         for c, l in fam]
ax.legend(handles=fam_h, loc='lower right', bbox_to_anchor=(0.97, 0.02),
          frameon=True, framealpha=1.0, edgecolor='#BBBBBB', fontsize=6.2,
          handlelength=1.0, handletextpad=0.5, borderpad=0.6,
          labelspacing=0.35)

save(fig, 'case_seg135.png')
