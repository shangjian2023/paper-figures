# -*- coding: utf-8 -*-
"""案例108 - iMeta 多分组火山图(一): 左1大火山 + 右18小分面(3x6, 彩色标题条)
+ 底部18个放大分面。蓝/粉底色标 Down/Up 区, 点色=组织。
参考: frames/seg_108.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

set_style()
r = rng(108)

TISSUES = [
    ('BAT', '#5b8fc4'), ('Beige fat', '#4477aa'), ('Bladder', '#a8a2b8'),
    ('Bone', '#5aa85f'), ('Brain', '#b39db4'), ('Cerebellum', '#d9705c'),
    ('Eye', '#e8a25e'), ('Heart', '#4a7fb5'), ('Kidney', '#b08d57'),
    ('Liver', '#8a9a3b'), ('Lung', '#9cc488'), ('Muscle', '#d05a6a'),
    ('Skin', '#7a5fa8'), ('Small intestine', '#3b5998'),
    ('Spinal cord', '#d9c04f'), ('Spleen', '#a3922e'),
    ('Testis', '#a83232'), ('Thymus', '#c0392b')]
XL, XR = 1.8, 4.7


def panel(ax, name, color, npoints, iseed=0, fs=1.0, title_h=0.30,
          title_fs=7):
    """一个火山分面: 蓝粉底带 + 组织色散点 + 彩色标题条。"""
    ax.axvspan(-XL, -0.26, facecolor='#cfe0ea', alpha=0.75, lw=0)
    ax.axvspan(0.26, XL, facecolor='#f6d3d8', alpha=0.75, lw=0)
    rr = rng(iseed)
    x = np.clip(rr.normal(-0.85, 0.42, npoints // 2), -1.7, -0.27)
    x2 = np.clip(rr.normal(0.85, 0.45, npoints - npoints // 2), 0.27, 1.75)
    x = np.concatenate([x, x2])
    y = np.clip(rr.normal(3.3, 0.55, npoints), 2.25, 4.55)
    ax.scatter(x, y, s=7 * fs, color=color, alpha=0.85, lw=0)
    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(2.2, 4.7)
    ax.set_yticks([2.2, 3.2, 4.2])
    ax.set_xticks([-1.8, 1.8])
    ax.tick_params(labelsize=6.5 * fs, length=2, pad=1)
    ax.add_patch(Rectangle((0, 1.0), 1, title_h, transform=ax.transAxes,
                           clip_on=False, facecolor=color, edgecolor='none'))
    ax.text(0.5, 1.0 + title_h / 2, name, transform=ax.transAxes,
            ha='center', va='center', fontsize=title_fs, color='white')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


fig = plt.figure(figsize=cm2in(19, 17.5))

# ================= 左上大火山 =================
axM = fig.add_axes([0.075, 0.635, 0.335, 0.265])
axM.axvspan(-XL, -0.26, facecolor='#cfe0ea', alpha=0.8, lw=0)
axM.axvspan(0.26, XL, facecolor='#f6d3d8', alpha=0.8, lw=0)
for ti, (name, color) in enumerate(TISSUES):
    rr = rng(10800 + ti)
    npt = 55 if color == '#d05a6a' else 14
    x = np.concatenate([np.clip(rr.normal(-0.75, 0.35, npt // 2), -1.7, -0.27),
                        np.clip(rr.normal(0.8, 0.42, npt - npt // 2), 0.27, 1.75)])
    y = np.clip(rr.normal(3.4, 0.6, npt), 2.25, 4.6)
    axM.scatter(x, y, s=9, color=color, alpha=0.9, lw=0)
axM.set_xlim(-1.9, 1.9)
axM.set_ylim(2.2, 4.7)
axM.set_yticks([2.2, 2.7, 3.2, 3.7, 4.2, 4.7])
axM.set_xticks([-1.80, -1.20, -0.60, 0.60, 1.20, 1.80])
axM.set_xlabel('log$_2$FC (Proteome)', fontsize=8.5)
axM.set_ylabel('Tissue-specific score across tissues', fontsize=8.5)
axM.tick_params(labelsize=7)
for s in ('top', 'right'):
    axM.spines[s].set_visible(False)
# 顶部 Down/Up 箭头
axM.annotate('', xy=(-1.80, 4.92), xytext=(-0.72, 4.92),
             arrowprops=dict(arrowstyle='->', color='#4477aa', lw=1.1))
axM.text(-1.26, 4.97, 'Downregulated', fontsize=8, color='#4477aa',
         ha='center')
axM.annotate('', xy=(1.80, 4.92), xytext=(0.60, 4.92),
             arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.1))
axM.text(1.20, 4.97, 'Upregulated', fontsize=8, color='#c0392b', ha='center')

# ================= 右上 18 小分面 (3行x6列) =================
x0, wgap = 0.475, 0.0875
ytops = [0.875, 0.760, 0.645]
for i, (name, color) in enumerate(TISSUES):
    row, col = divmod(i, 6)
    ax = fig.add_axes([x0 + col * wgap, ytops[row], 0.078, 0.080])
    panel(ax, name, color, 16, iseed=10800 + i, title_h=0.33, title_fs=6.2)
    ax.tick_params(labelsize=5.2)
    if col > 0:
        ax.set_yticklabels([])
    if row < 2:
        ax.set_xticklabels([])

# ================= 底部 18 放大分面 (3行x6列, 全宽) =================
x0b, wgapb = 0.075, 0.1565
ybot = [0.420, 0.255, 0.090]
for i, (name, color) in enumerate(TISSUES):
    row, col = divmod(i, 6)
    ax = fig.add_axes([x0b + col * wgapb, ybot[row], 0.138, 0.106])
    panel(ax, name, color, 26, iseed=10800 + i, fs=1.15, title_h=0.30,
          title_fs=8.5)
    ax.tick_params(labelsize=6.5)
    if col > 0:
        ax.set_yticklabels([])
    if row < 2:
        ax.set_xticklabels([])

save(fig, 'case_seg108.png')
