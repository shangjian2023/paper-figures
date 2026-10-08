# -*- coding: utf-8 -*-
"""案例22 - Nature 相关性点阵热图: 47×47 下三角。
点径=|r|, 蓝白红渐变; 行列名按 5 类着色; 右侧丰度条形; 左侧迷你图例。
参考: frames/seg_022.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.patches import Rectangle

cat_colors = {1: '#1a1a1a', 2: '#a8a41e', 3: '#8b1a1a', 4: '#2e8b57',
              5: '#7b52ab'}
names = [
    (1, 'Arg-dihydroxylated BA 1'), (1, 'Arg-dihydroxylated BA 2'),
    (1, 'Asn-dihydroxylated BA 1'), (1, 'Asn-dihydroxylated BA 2'),
    (1, 'Ser-dihydroxylated BA'), (1, 'Cys-dihydroxylated BA'),
    (1, 'Ala-dihydroxylated BA'), (1, 'Gln-dihydroxylated BA'),
    (2, 'Glycohyodeoxycholic acid'), (2, 'Glycocholic acid'),
    (2, 'Glycochenodeoxycholic acid'), (2, 'Glycoursodeoxycholic acid'),
    (2, 'Glycohyocholic acid'), (2, 'Tauro-alpha-muricholic acid'),
    (2, 'Tauro-beta-muricholic acid'), (2, 'Tauro-omega-muricholic acid'),
    (2, 'Taurohyodeoxycholic acid'), (2, 'Taurocholic acid'),
    (3, 'Cholic acid'), (3, 'Chenodeoxycholic acid'),
    (3, 'Deoxycholic acid'), (3, 'Lithocholic acid'),
    (3, 'Ursodeoxycholic acid'), (3, 'Alpha-muricholic acid'),
    (3, 'Beta-muricholic acid'), (3, 'Omega-muricholic acid'),
    (3, 'Hyocholic acid'), (3, 'Hyodeoxycholic acid'),
    (4, 'Tauroursodeoxycholic acid'), (4, 'Taurolithocholic acid'),
    (4, 'Glycolithocholic acid'), (4, 'Glycodeoxycholic acid'),
    (4, 'Taurochenodeoxycholic acid'), (4, 'Glyco-omega-muricholic acid'),
    (4, 'Taurodeoxycholic acid'), (4, 'Glycoursodeoxycholic acid 2'),
    (4, 'Tauro-alpha-hyocholic acid'),
    (5, '6-Ketolithocholic acid'), (5, '7-Ketolithocholic acid'),
    (5, '12-Ketolithocholic acid'), (5, '3-Oxocholic acid'),
    (5, 'Dehydrocholic acid'), (5, 'Nor-cholic acid'),
    (5, 'Apo-cholic acid'), (5, 'Iso-lithocholic acid'),
    (5, 'Allolithocholic acid'), (5, '3-Epicholic acid')]
n = len(names)                        # 47
cats = np.array([c for c, _ in names])
labels = [s for _, s in names]

r = rng(22)
R = r.uniform(-0.35, 0.55, (n, n))
def boost(a, b, lo, hi):
    R[np.ix_(a, b)] = r.uniform(lo, hi, (len(a), len(b)))
i1 = np.where(cats == 1)[0]; i2 = np.where(cats == 2)[0]
i3 = np.where(cats == 3)[0]; i4 = np.where(cats == 4)[0]
i5 = np.where(cats == 5)[0]
boost(i1, i1, 0.75, 0.98); boost(i2, i2, 0.55, 0.9)
boost(i3, i3, 0.6, 0.92); boost(i4, i4, 0.5, 0.85)
boost(i5, i5, 0.55, 0.9)
boost(i1, i2, 0.6, 0.95); boost(i3, i4, 0.35, 0.7)
boost(i4, i5, 0.3, 0.6)
boost(i1, i5, -0.5, -0.1)
R = (R + R.T) / 2
np.fill_diagonal(R, 1.0)
abun = r.uniform(0.4, 6.2, n)

fig = plt.figure(figsize=cm2in(19.5, 19.0))
gs = fig.add_gridspec(1, 3, width_ratios=[0.72, 3.15, 0.72], wspace=0.06,
                      left=0.015, right=0.985, top=0.90, bottom=0.065)
ax_l = fig.add_subplot(gs[0]); ax_l.axis('off')
ax = fig.add_subplot(gs[1])
ax_r = fig.add_subplot(gs[2], sharey=ax)

norm = Normalize(-1, 1)
cmap = plt.get_cmap('RdBu')

# 浅灰网格
for k in range(n + 1):
    ax.axhline(k, color='#d9d9d9', lw=0.3, zorder=1)
    ax.axvline(k, color='#d9d9d9', lw=0.3, zorder=1)

# 下三角点阵 (含对角)
xs, ss, cs = [], [], []
for i in range(n):
    for j in range(i + 1):
        rr = R[i, j]
        xs.append((j, i))
        ss.append(2.5 + 68 * rr ** 2)
        cs.append('#08306b' if i == j else cmap(norm(rr)))
xs = np.array(xs, float)
ax.scatter(xs[:, 0], xs[:, 1], s=ss, c=cs, edgecolors='none', zorder=3)

ax.set_xlim(-7.0, n)
ax.set_ylim(n, -1.6)
ax.axis('off')

# 行列名 (按类着色)
for j in range(n):
    ax.text(j, -0.55, labels[j], rotation=45, ha='left', va='bottom',
            fontsize=4.0, color=cat_colors[cats[j]])
for i in range(n):
    ax.text(-0.55, i, labels[i], ha='right', va='center',
            fontsize=3.8, color=cat_colors[cats[i]])

# 右侧丰度条形
bar_colors = {1: '#5b3a8e', 2: '#3f9b4f', 3: '#5b3a8e', 4: '#3f9b4f',
              5: '#5b3a8e'}
ax_r.barh(np.arange(n), abun, height=0.78,
          color=[bar_colors[c] for c in cats])
ax_r.set_ylim(n - 0.5, -0.5)
ax_r.set_xlim(0, 6.4)
ax_r.set_xticks([0, 2, 4, 6])
ax_r.set_yticks([])
ax_r.tick_params(axis='x', labelsize=6, length=2, pad=1)
ax_r.set_xlabel('Mean abundance (log10)', fontsize=6.5, labelpad=1.5)
ax_r.spines[['top', 'right', 'left']].set_visible(False)
ax_r.spines['bottom'].set_linewidth(0.7)

# ---- 左侧图例面板: 迷你点阵 + 色条 + 类别图例
ax_l.set_xlim(0, 1); ax_l.set_ylim(-0.12, 1)
cols_hdr = [(2, cat_colors[2]), (3, cat_colors[3]), (4, cat_colors[4]),
            (5, cat_colors[5])]
for k, (num, cc) in enumerate(cols_hdr):
    ax_l.text(0.32 + k * 0.17, 0.80, str(num), ha='center', va='bottom',
              fontsize=7, color=cc)
for k in range(4):
    ax_l.text(0.10, 0.715 - k * 0.105, str(k + 1), ha='center', va='center',
              fontsize=7, color=cat_colors[2])
mini_s = [[70, 210, 70, 210], [30, 260, 25, 15], [40, 200, 45, 170],
          [15, 25, 130, 40]]
mini_c = [['#92c5de', '#2166ac', '#92c5de', '#2166ac'],
          ['#d1e5f0', '#05306b', '#f7f7f7', '#f7f7f7'],
          ['#d1e5f0', '#4393c3', '#d1e5f0', '#4393c3'],
          ['#f7f7f7', '#f7f7f7', '#2166ac', '#d1e5f0']]
for ri in range(4):
    for ci in range(4):
        ax_l.scatter(0.32 + ci * 0.17, 0.715 - ri * 0.105, s=mini_s[ri][ci],
                     c=mini_c[ri][ci], edgecolors='none')
sm = ScalarMappable(norm=norm, cmap=cmap)
cb = fig.colorbar(sm, cax=ax_l.inset_axes([0.04, 0.34, 0.90, 0.035],
                                        transform=ax_l.transAxes),
                  orientation='horizontal',
                  ticks=[1, 0.5, 0, -0.5, -1])
cb.ax.tick_params(labelsize=5.5, length=2, pad=1)
cb.outline.set_linewidth(0.6)

legend_txt = [(1, '1. Microbially conjugated\n   bile acids'),
              (2, '2. 1\u00b0 conjugated\n   bile acids'),
              (3, '3. 1\u00b0 bile acids'),
              (4, '4. 2\u00b0 conjugated\n   bile acids'),
              (5, '5. 2\u00b0 bile acids')]
y0 = 0.155
for k, (num, txt) in enumerate(legend_txt):
    y = y0 - k * 0.055
    ax_l.scatter(0.07, y, marker='s', s=42, c=cat_colors[num],
                 edgecolors='none')
    ax_l.text(0.14, y, txt, ha='left', va='center', fontsize=5.8,
              color=cat_colors[num], linespacing=1.25)

save(fig, 'case_seg022.png')
