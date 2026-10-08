# -*- coding: utf-8 -*-
"""案例109 - Nature 多分组火山图(二): 上排9个脑区分面 + 下排3个放大分面。
灰底点 + 每区彩色高亮基因带引线基因名, y=avg_log2FC, x=表达百分比。
参考: frames/seg_109.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt

set_style()

REGIONS = [
    ('olfactory bulb', '#c0434f',
     [('Ms4a4c', 18, 4.6), ('Cxcl10', 14, 4.1), ('Cd3d', 12, 3.6),
      ('Ccl5', 15, 2.4), ('Serpina3g', 16, 1.9),
      ('Zbp1', 22, -1.2), ('Cybb', 26, -1.5), ('Ms4a6c', 24, -1.9),
      ('Oasl1', 30, -2.2), ('Plac8', 33, -2.8)]),
    ('cortex-1', '#4a90c4',
     [('Gzma', 48, 4.6), ('Xkr41', 22, 1.6), ('Ccl5', 30, 1.2),
      ('Zfp185', 36, 1.1), ('Lgals3', 40, 0.9),
      ('Pirb1', 26, -0.9), ('Ly6c2', 32, -1.3), ('Il2rb', 35, -1.6),
      ('Napsa1', 40, -1.9), ('Tgtp1', 30, -3.0)]),
    ('cortex-2', '#a8c04a',
     [('Camp', 40, 5.2), ('Klrd1', 55, 4.6), ('Gm318342', 35, 2.6),
      ('Retnlg', 42, 1.6),
      ('Ccl19', 30, -0.9), ('Plin4', 38, -1.4), ('Ms4a6c', 34, -2.0),
      ('Wfdc17', 36, -2.4)]),
    ('hippocampus', '#3ba45f',
     [('Ccl5', 30, 3.6), ('Nrg7', 36, 3.1), ('Arm', 33, 2.4),
      ('Fst3', 30, 1.8),
      ('Gbp5', 28, -0.9), ('Plin4', 34, -1.3), ('BC067072', 38, -1.7),
      ('Ascl1', 42, -2.6)]),
    ('midbrain', '#e08aa0',
     [('Ms4a4a', 14, 6.2), ('Chd3', 16, 5.6), ('Ntng7', 18, 5.2),
      ('Cdkn3', 20, 4.8), ('Hp3', 24, 4.2),
      ('Timp2', 26, -0.9), ('Mall', 32, -1.4), ('Oaz1a', 34, -1.8),
      ('Fgf4', 36, -2.3)]),
    ('cerebellum', '#e8a33d',
     [('Gm11573', 18, 4.4), ('Top3', 26, 3.9), ('Cdc42', 22, 3.3),
      ('Gm15492', 20, 2.6), ('Krg2', 24, 2.2), ('Gm9925', 27, 1.9),
      ('Gucb', 25, -1.1), ('Grin1', 30, -1.6), ('Ms4a6c', 33, -2.4)]),
    ('hindbrain', '#3ba8a8',
     [('Gm15492', 20, 3.4), ('Krg2', 26, 2.8), ('Gm9925', 24, 2.3),
      ('Tgf1', 30, 1.8),
      ('Plin4', 28, -1.0), ('Myo1g', 34, -1.5), ('Klra1', 38, -2.1)]),
    ('thalamus', '#c0434f',
     [('Cttna3', 12, 6.4), ('Kdrq2', 16, 6.0), ('Wnt11', 20, 5.6),
      ('Gm8073', 24, 5.2),
      ('Gal2', 18, -1.2), ('Lrmda', 24, -1.7), ('Angpt2', 28, -2.1),
      ('Tdrd6', 32, -2.6), ('Adgrv1', 36, -3.1)]),
    ('hypothalamus', '#9a6bc4',
     [('Trnc1', 58, 2.4), ('Chil3', 62, 1.9), ('Ccdc10', 66, 1.5),
      ('Gabra5', 70, 1.0),
      ('Sall5', 60, -1.3), ('Zbp14', 64, -1.7), ('Lgals25', 68, -2.2),
      ('Caonb36', 72, -2.8)]),
]

r = rng(109)


def facet_points(n=140):
    x = r.uniform(2, 88, n)
    y = r.normal(0, 1.6, n)
    y += (r.random(n) < 0.12) * r.normal(0, 2.6, n)
    y = np.clip(y, -5.6, 7.6)
    return x, y


def draw_facet(ax, name, color, genes, fs_gene, fs_tick, leaders=True,
               max_lab=None, lab_gap=1.3):
    x, y = facet_points()
    ax.scatter(x, y, s=7, color='0.72', alpha=0.8, lw=0, zorder=2)
    ax.axhline(0, color='0.45', ls='--', lw=0.9, zorder=3)
    sel = sorted(genes, key=lambda g: -abs(g[2]))
    if max_lab is not None:
        sel = sel[:max_lab]          # 小面板只标最显著的 2-3 个
    up = [g for g in sel if g[2] > 0]
    dn = [g for g in sel if g[2] <= 0]

    def text_y(items):
        # 同面板全部标签按 y 排序后逐个错开, 保证文字纵向间距 >= lab_gap,
        # 再整体回中并限幅在 ylim 内。上调/下调两组一起参与排序,
        # 防止两组各自错位后在 y=0 附近互相叠印
        items = sorted(items, key=lambda g: g[2])
        ys = [g[2] for g in items]
        for i in range(1, len(ys)):
            if ys[i] - ys[i - 1] < lab_gap:
                ys[i] = ys[i - 1] + lab_gap
        if ys:
            shift = sum(ys) / len(ys) - sum(g[2] for g in items) / len(items)
            ys = [min(7.6, max(-5.6, v - shift)) for v in ys]
        return {g[0]: ty for g, ty in zip(items, ys)}

    ty_map = text_y(sel)
    for gname, gx, gy in up:
        ax.scatter([gx], [gy], s=13, color=color, zorder=4)
        ax.annotate(italic_gene(gname), (gx, gy),
                    xytext=(gx + 12, ty_map[gname]),
                    fontsize=fs_gene, color=color, va='center',
                    arrowprops=dict(arrowstyle='-', lw=0.6, color=color))
    for gname, gx, gy in dn:
        ax.scatter([gx], [gy], s=13, color=color, zorder=4)
        ax.annotate(italic_gene(gname), (gx, gy),
                    xytext=(gx + 12, ty_map[gname]),
                    fontsize=fs_gene, color=color, va='center',
                    arrowprops=dict(arrowstyle='-', lw=0.6, color=color))
    ax.set_xlim(0, 92)
    ax.set_ylim(-6, 8)
    ax.set_xticks([0, 20, 40, 60, 80])
    ax.set_yticks([-6, -4, -2, 0, 2, 4, 6, 8][::2])
    ax.tick_params(labelsize=fs_tick, length=2, pad=1)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_title(name, fontsize=fs_gene + 0.5, pad=3,
                 bbox=dict(facecolor='0.92', edgecolor='0.4', lw=0.7,
                           pad=2.5))
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


fig = plt.figure(figsize=cm2in(18, 16.5))
# ---------------- 上排 9 区
gs1 = fig.add_gridspec(1, 9, left=0.055, right=0.995, top=0.685,
                       bottom=0.475, wspace=0.60)
axes1 = []
for i, (name, color, genes) in enumerate(REGIONS):
    ax = fig.add_subplot(gs1[i])
    axes1.append(ax)
    draw_facet(ax, name, color, genes, fs_gene=4.8, fs_tick=6, max_lab=3,
               lab_gap=1.4)
    if i > 0:
        ax.set_yticklabels([])
axes1[0].set_ylabel('avg_log2FC', fontsize=8)

# ---------------- 下排 3 区放大
gs2 = fig.add_gridspec(1, 3, left=0.24, right=0.76, top=0.40,
                       bottom=0.045, wspace=0.42)
axes2 = []
for j, (name, color, genes) in enumerate(REGIONS[:3]):
    ax = fig.add_subplot(gs2[j])
    axes2.append(ax)
    draw_facet(ax, name, color, genes, fs_gene=8.5, fs_tick=7.5, lab_gap=0.95)
    if j > 0:
        ax.set_yticklabels([])
axes2[0].set_ylabel('avg_log2FC (ECM vs. CON)', fontsize=8.5)
axes2[1].set_xlabel('Percent expressing', fontsize=9, labelpad=2)

save(fig, 'case_seg109.png')
