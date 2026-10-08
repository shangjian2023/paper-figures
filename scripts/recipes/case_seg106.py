# -*- coding: utf-8 -*-
"""案例108 - Cell 多面板热图: 2行×3列, 上排%active(橙黑), 下排%repressed(蓝绿),
白点=显著, 底部因子分类色条, 右侧两色标+Factor-level summary。
参考: frames/seg_106.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm

set_style()

states = ['Immature', 'Neutrophil', 'Monocyte P.', 'Monocyte',
          'Eosinophil', 'Basophil', 'MegEry']
single8 = ['Cebpa', 'Sp1', 'Gata1', 'Gata2', 'Lyl1', 'Runx1', 'Fli1', 'Klf1']
pool = ['Cebpa', 'Sp1', 'Elk1', 'Trp53', 'Fli1', 'Klf14', 'Nfyc', 'Ddit3', 'Klf1',
        'Stat5a', 'Fos', 'Nfkb1', 'Spdef', 'Mecom', 'Yy1', 'Cic', 'Myb', 'Lyl1',
        'Irf7', 'Gata1', 'Creb1', 'Myc', 'Gata2', 'Nr2c2', 'Tcf3', 'Ikzf1',
        'Tfap2a', 'Gfi1', 'Gli1b', 'Runx1', 'Meis1', 'Pbx1']
pairs = [f'{a}\u2013{b}' for a, b in zip(single8, single8[1:])] + \
        [f'{a}\u2013{b}' for a, b in zip(pool[:14], pool[15:29])]
groups = [('Set 1 (single f.)', single8), ('Set 1 (pairs)', pairs),
          ('Set 2 (single factors)', pool[:24])]
r = rng(106)

# 数据: 上排 active 0-100 (少数亮列), 下排 repressed 0-30
def make_mat(ncols, vmax, boost_cols, boost_rows):
    m = r.uniform(0, 1, (len(states), ncols)) ** 4 * vmax
    for c in boost_cols:
        m[:, c] = r.uniform(0.45, 1.0, len(states)) * vmax
    for c, ri in boost_rows:
        m[ri, c] = vmax * r.uniform(0.7, 1.0)
    return m

act_mats = [make_mat(len(g[1]), 100, [1, 4, 7], [(2, 3), (5, 6)]) for g in groups]
rep_mats = [make_mat(len(g[1]), 30, [0, 3, 6], [(6, 2), (1, 5)]) for g in groups]
sig_a = [r.uniform(0, 1, m.shape) < 0.20 for m in act_mats]
sig_r = [r.uniform(0, 1, m.shape) < 0.15 for m in rep_mats]

cmap_act = LinearSegmentedColormap.from_list(
    'act', ['#000000', '#2b0502', '#660e04', '#a31905', '#d63a10',
            '#ef7d20', '#f9a63a', '#fcca5f'])
cmap_rep = LinearSegmentedColormap.from_list(
    'rep', ['#000000', '#0b2d6b', '#1e5cb8', '#5c9bd8', '#9ccbe8', '#54c568', '#1fe000'])
cat_cmap = ListedColormap(['#66c2a5', '#fc8d62', '#8da0cb', '#b8b8d0'])
cat_names = ['Activator', 'Dual', 'Repressor', 'Other']
cats = [r.choice([0, 1, 2, 3], len(g[1]), p=[0.4, 0.25, 0.2, 0.15]) for g in groups]

fig = plt.figure(figsize=cm2in(19.5, 18.0))
# 三列面板的水平范围 (宽度按列数粗略比例; 窄面板加宽保证竖排因子名互不叠压)
xspan = [(0.115, 0.19), (0.21, 0.585), (0.605, 0.825)]
rows_y = [(0.795, 0.970), (0.586, 0.761)]   # active / repressed (上 2/3)

for ci, (name, facs) in enumerate(groups):
    x0, x1 = xspan[ci]
    for ri, (y0, y1) in enumerate(rows_y):
        mat = act_mats[ci] if ri == 0 else rep_mats[ci]
        sig = sig_a[ci] if ri == 0 else sig_r[ci]
        cmap = cmap_act if ri == 0 else cmap_rep
        vmax = 100 if ri == 0 else 30
        ax = fig.add_axes([x0, y0, x1 - x0, y1 - y0])
        ax.imshow(mat, aspect='auto', cmap=cmap, vmin=0, vmax=vmax,
                  interpolation='nearest')
        nr, nc = mat.shape
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(True)
            s.set_linewidth(1.2)
        yy, xx = np.where(sig)
        ax.scatter(xx, yy, s=3, c='white', zorder=3)
        if ri == 1:
            # 底部因子分类色条
            cbar_ax = fig.add_axes([x0, 0.544, x1 - x0, 0.0195])
            cbar_ax.imshow(cats[ci][None, :], aspect='auto', cmap=cat_cmap,
                           norm=BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], 4),
                           interpolation='nearest')
            cbar_ax.set_xticks([]); cbar_ax.set_yticks([])
            for s in cbar_ax.spines.values():
                s.set_linewidth(0.8)
            # 因子名(竖排)
            tax = fig.add_axes([x0, 0.38, x1 - x0, 0.154])
            tax.set_xlim(-0.5, nc - 0.5); tax.set_ylim(0, 1)
            tax.set_xticks([]); tax.set_yticks([])
            for s in tax.spines.values():
                s.set_visible(False)
            for j, f in enumerate(facs):
                tax.text(j, 0.96, f, rotation=90, ha='center', va='top',
                         fontsize=4.5)
        # 灰底标题
        ax.set_title(name, fontsize=8, pad=2.5,
                     bbox=dict(facecolor='0.88', edgecolor='0.2', lw=0.8, pad=1.8))

# 左侧行标签
for y0, y1 in rows_y:
    lax = fig.add_axes([0.0, y0, 0.115, y1 - y0])
    lax.set_xlim(0, 1); lax.set_ylim(len(states) - 0.5, -0.5)
    lax.set_xticks([]); lax.set_yticks(range(len(states)))
    lax.set_yticklabels(states, fontsize=7)
    lax.tick_params(length=0)
    for s in lax.spines.values():
        s.set_visible(False)
    lax.text(0.99, len(states) - 0.9, '% of sequences\nactive' if y0 > 0.7
             else '% of sequences\nrepressed', fontsize=6.5, ha='right', va='top')

# ------------------------------------------------ 右侧两个色标
cax1 = fig.add_axes([0.86, 0.795, 0.016, 0.174])
fig.colorbar(plt.cm.ScalarMappable(
    plt.Normalize(0, 100), cmap_act), cax=cax1, ticks=[0, 25, 50, 75, 100])
cax1.set_title('% of sequences\nactive', fontsize=7, loc='left', pad=4)
cax1.tick_params(labelsize=6.5)

cax2 = fig.add_axes([0.86, 0.586, 0.016, 0.174])
fig.colorbar(plt.cm.ScalarMappable(
    plt.Normalize(0, 30), cmap_rep), cax=cax2, ticks=[0, 10, 20, 30])
cax2.set_title('% of sequences\nrepressed', fontsize=7, loc='left', pad=4)
cax2.tick_params(labelsize=6.5)

# ------------------------------------------------ Factor-level summary
lax = fig.add_axes([0.90, 0.408, 0.09, 0.126])
lax.set_xlim(0, 1); lax.set_ylim(0, 1)
lax.set_xticks([]); lax.set_yticks([])
for s in lax.spines.values():
    s.set_visible(False)
lax.text(0.0, 1.04, 'Factor\u2013level\nsummary', fontsize=7, va='bottom')
for k, nm in enumerate(cat_names):
    y = 0.72 - k * 0.22
    lax.add_patch(plt.Rectangle((0.05, y - 0.055), 0.14, 0.11,
                                facecolor=cat_cmap(k), edgecolor='none'))
    lax.text(0.24, y, nm, fontsize=7, va='center')

# ------------------------------------------------ 底部放大详情面板: Set 1 (single f.)
bx0, bx1, by0, by1 = 0.44, 0.85, 0.055, 0.315
bax = fig.add_axes([bx0, by0, bx1 - bx0, by1 - by0])
bax.imshow(act_mats[0], aspect='auto', cmap=cmap_act, vmin=0, vmax=100,
           interpolation='nearest')
bax.set_xticks([]); bax.set_yticks([])
for s in bax.spines.values():
    s.set_visible(True)
    s.set_linewidth(1.6)
yy, xx = np.where(sig_a[0])
bax.scatter(xx, yy, s=10, c='white', zorder=3)
bax.set_title('Set 1 (single f.)', fontsize=15, pad=8,
              bbox=dict(facecolor='0.88', edgecolor='0.2', lw=1.2, pad=4))
# 大号行标签 + 短刻度线
blax = fig.add_axes([0.15, by0, bx0 - 0.15, by1 - by0])
blax.set_xlim(0, 1); blax.set_ylim(len(states) - 0.5, -0.5)
blax.set_xticks([]); blax.set_yticks(range(len(states)))
blax.set_yticklabels(states, fontsize=13)
blax.tick_params(length=0, pad=6)
for s in blax.spines.values():
    s.set_visible(False)
for k in range(len(states)):
    blax.plot([0.97, 1.0], [k, k], color='black', lw=1.2,
              clip_on=False)

save(fig, 'case_seg106.png')
