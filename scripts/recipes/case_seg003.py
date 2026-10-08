# -*- coding: utf-8 -*-
"""案例3 - Nature PCoA图: ~1500样本散点(6研究x2组) + 右列/底行箱线 + 研究图例。
参考: frames/seg_003.jpg — 圆=control 三角=IBD, L形边际箱线。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt

set_style()

studies = ['Puxi_cohort', 'HMP_2019_ibdmdb', 'LifeLD_VilaAV_2018',
           'NielsenHB_2014', 'FranzosaEA_2019A', 'HeQ_2017']
scolors = ['#DE6E5E', '#5D8FC4', '#EE9E52', '#63A86B', '#A98BC4', '#9FB6C9']
gcolors = {'control': '#B23A3A', 'IBD': '#2E75B6'}
centers = [(-0.02, 0.24), (0.10, 0.16), (0.12, -0.16), (-0.06, -0.06),
           (0.02, 0.02), (-0.10, 0.02)]
scales = [0.020, 0.014, 0.017, 0.013, 0.012, 0.010]
per_study = [300, 320, 300, 220, 220, 140]

r = rng(3)
fig = plt.figure(figsize=cm2in(17.0, 16.0))
outer = fig.add_gridspec(2, 2, width_ratios=[2.9, 1.15], height_ratios=[2.9, 1.15],
                         hspace=0.10, wspace=0.10)
gs_right = outer[0, 1].subgridspec(1, 2, wspace=0.25)
gs_bot = outer[1, 0].subgridspec(2, 1, hspace=0.55)
ax_main = fig.add_subplot(outer[0, 0])
ax_rs = fig.add_subplot(gs_right[0, 0])
ax_rg = fig.add_subplot(gs_right[0, 1])
ax_bs = fig.add_subplot(gs_bot[0])
ax_bg = fig.add_subplot(gs_bot[1])
ax_leg = fig.add_subplot(outer[1, 1])
ax_leg.axis('off')

# ---------------- 主散点 ----------------
all_xy = []
for si, (n, c, sd) in enumerate(zip(per_study, centers, scales)):
    for gi, g in enumerate(['control', 'IBD']):
        m = n // 2
        xy = r.multivariate_normal(c, [[sd, 0.004], [0.004, sd]], m)
        xy += r.normal(0, 0.012, xy.shape) + np.array([0, -0.035 * gi])
        all_xy.append((xy, si, g))
for xy, si, g in all_xy:
    mk = 'o' if g == 'control' else '^'
    ax_main.scatter(xy[:, 0], xy[:, 1], s=8, marker=mk, c=scolors[si],
                    alpha=0.75, linewidths=0, zorder=3)
ax_main.text(0.03, 0.97, 'PERMANOVA\np=0.001', transform=ax_main.transAxes,
             ha='left', va='top', fontsize=11)
ax_main.legend(handles=[
    plt.Line2D([], [], marker='o', ls='', color='#444444', label='control'),
    plt.Line2D([], [], marker='^', ls='', color='#444444', label='IBD')],
    loc='lower left', frameon=False, fontsize=8.5, title='Group',
    title_fontsize=9, handletextpad=0.2, borderaxespad=0.1)
ax_main.set_xlim(-0.32, 0.56)
ax_main.set_ylim(-0.42, 0.47)
ax_main.set_xticks([-0.25, 0.0, 0.25, 0.5])
ax_main.set_yticks([-0.2, 0.0, 0.2, 0.4])
ax_main.set_title('PCo1 [15.9%]', fontsize=11, pad=6)
ax_main.set_ylabel('PCo2 [10.2%]', fontsize=11)

# 每研究 PCo1 / PCo2 值(供箱线)
x_by = [np.concatenate([xy[:, 0] for xy, s, g in all_xy if s == i]) for i in range(6)]
y_by = [np.concatenate([xy[:, 1] for xy, s, g in all_xy if s == i]) for i in range(6)]
ctrl_x = np.concatenate([xy[:, 0] for xy, s, g in all_xy if g == 'control'])
ibd_x = np.concatenate([xy[:, 0] for xy, s, g in all_xy if g == 'IBD'])
ctrl_y = np.concatenate([xy[:, 1] for xy, s, g in all_xy if g == 'control'])
ibd_y = np.concatenate([xy[:, 1] for xy, s, g in all_xy if g == 'IBD'])


def style_box(bp, colors):
    for b, c in zip(bp['boxes'], colors):
        b.set_facecolor(c)
        b.set_edgecolor('black')
        b.set_linewidth(0.9)
    for w in bp['whiskers'] + bp['caps']:
        w.set_color('black')
        w.set_linewidth(0.9)
    for m in bp['medians']:
        m.set_color('black')
        m.set_linewidth(1.1)


# ---------------- 右列: Study / Group 纵向箱线 ----------------
bp = ax_rs.boxplot(x_by, positions=range(6), widths=0.6, patch_artist=True,
                   showfliers=True,
                   flierprops=dict(marker='o', ms=2.5, mfc='black', mec='black'),
                   medianprops=dict(color='black'))
style_box(bp, scolors)
ax_rs.set_xticks([])
ax_rs.set_ylim(-0.42, 0.47)
ax_rs.set_yticks([-0.2, 0.0, 0.2, 0.4])
ax_rs.set_yticklabels(['-0.2', '0.0', '0.2', '0.4'], fontsize=7)
despine(ax_rs, bottom=True)

bp = ax_rg.boxplot([ctrl_y, ibd_y], positions=[0, 1], widths=0.6,
                   patch_artist=True, showfliers=True,
                   flierprops=dict(marker='o', ms=2.5, mfc='black', mec='black'),
                   medianprops=dict(color='black'))
style_box(bp, [gcolors['control'], gcolors['IBD']])
ax_rg.set_xticks([])
ax_rg.set_yticks([-0.2, 0.0, 0.2, 0.4])
ax_rg.set_yticklabels(['', '', '', ''], fontsize=7)
ax_rg.text(0.5, 1.05, 'Study Group', transform=ax_rg.transAxes, ha='center',
           fontsize=11)
despine(ax_rg, bottom=True)

# ---------------- 底行: Study / Group 横向箱线 ----------------
bp = ax_bs.boxplot(x_by, orientation='horizontal', positions=range(6), widths=0.6,
                   patch_artist=True, showfliers=True,
                   flierprops=dict(marker='o', ms=2.5, mfc='black', mec='black'),
                   medianprops=dict(color='black'))
style_box(bp, scolors)
ax_bs.set_yticks([])
ax_bs.set_xlim(-0.32, 0.56)
ax_bs.set_xticks([-0.25, 0.0, 0.25, 0.5])
ax_bs.set_ylabel('Study', fontsize=10, rotation=90, labelpad=2)
despine(ax_bs, left=True)

bp = ax_bg.boxplot([ibd_x, ctrl_x], orientation='horizontal', positions=[1, 0], widths=0.6,
                   patch_artist=True, showfliers=True,
                   flierprops=dict(marker='o', ms=2.5, mfc='black', mec='black'),
                   medianprops=dict(color='black'))
style_box(bp, [gcolors['IBD'], gcolors['control']])
ax_bg.set_yticks([])
ax_bg.set_xlim(-0.32, 0.56)
ax_bg.set_xticks([-0.25, 0.0, 0.25, 0.5])
ax_bg.set_xlabel('PCo1', fontsize=10)
ax_bg.set_ylabel('Group', fontsize=10, rotation=90, labelpad=2)
despine(ax_bg, left=True)

# ---------------- 右下: Study 图例 ----------------
ax_leg.text(0.5, 1.10, 'Study', ha='center', fontsize=10,
            transform=ax_leg.transAxes)
for i, (s, c) in enumerate(zip(studies[::-1], scolors[::-1])):
    yy = 0.90 - i * 0.17
    ax_leg.add_patch(plt.Rectangle((0.06, yy - 0.045), 0.10, 0.09,
                                   transform=ax_leg.transAxes,
                                   facecolor=c, edgecolor='black', lw=0.7,
                                   clip_on=False))
    ax_leg.text(0.22, yy, s, va='center', fontsize=7.6,
                transform=ax_leg.transAxes)

save(fig, 'case_seg003.png')
