# -*- coding: utf-8 -*-
"""案例110 - Clin.Transl.Med 多分组火山图(三): 8个比较组水平条带。
每带一个窄水平散点区, 左青点Down右深红点Up, 灰带背景, 中央组色条+白底标签,
基因名散布两侧。参考: frames/seg_110.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

set_style()

GROUPS = [
    ('Malignant vs Benign', '#5b9ec9',
     [('S100A9', 1), ('LYZ', 1), ('HLA-DRA', 1), ('S100A8', 2), ('CST3', 2)],
     [('CST7', 1), ('GZMH', 1), ('CCL5', 1), ('NKG7', 2), ('GZMK', 2)]),
    ('StageII vs StageI', '#7fb2d4',
     [('LYZ', 1), ('S100A9', 2), ('HLA-DRA', 1), ('S100A8', 2), ('TYROBP', 2)],
     [('IL32', 1), ('CD2', 1), ('LTB', 1), ('AQP3', 2)]),
    ('StageIII vs StageI', '#a9c9e0',
     [('S100A8', 1), ('NKG7', 1), ('S100A9', 2), ('LYZ', 2)],
     [('HLA-DQA1', 1), ('CD7A', 1), ('CD79B', 1), ('HLA-DQB1', 2),
      ('TCL1A', 2)]),
    ('StageIII vs StageII', '#d9e3ee',
     [('CD3D', 1), ('LTB', 1), ('CD7', 1), ('IL32', 2), ('CD3E', 2)],
     [('HLA-DPA1', 1), ('HLA-DPB1', 1), ('HLA-DRB1', 2), ('HLA-DQA1', 2),
      ('FCER1A', 2)]),
    ('StageIV vs StageI', '#f2c4ad',
     [('IL32', 1), ('RTPRCAP', 1), ('CCL5', 2), ('CD3D', 2), ('LTB', 2)],
     [('FCER1G', 1), ('FCGR3A', 1), ('AIF1', 2), ('LST1', 2),
      ('MS4A7', 2)]),
    ('StageIV vs StageII', '#eba17f',
     [('S100A8', 1), ('HLA-DRA', 1), ('S100A9', 2), ('LYZ', 2), ('CST3', 2)],
     [('PRF1', 1), ('FGFBP2', 1), ('GNLY', 1), ('NKG7', 2), ('GZMB', 2)]),
    ('StageIV vs StageIII', '#e07b52',
     [('NKG7', 1), ('CCL5', 1), ('LTB', 2), ('IL32', 2), ('PTPRCAP', 2)],
     [('MS4A6A', 1), ('TYROBP', 1), ('CD14', 2), ('CST3', 2), ('LYZ', 2)]),
    ('N+ vs N0', '#c0503a',
     [('RPS24', 1), ('RPL9', 1), ('RPS4Y1', 2), ('RPL14', 2), ('MALAT1', 2)],
     [('SDPR', 1), ('PF4', 1), ('CLU', 2), ('GNG11', 2), ('PPBP', 2)]),
]

r = rng(110)
fig, ax = plt.subplots(figsize=cm2in(17, 14.5))
fig.subplots_adjust(left=0.105, right=0.985, top=0.93, bottom=0.09)
ax.set_xlim(-5.1, 8.3)
ax.set_ylim(-0.35, 8 * 1.08 + 0.05)
ax.set_xticks([-5, -2.5, 0, 2.5, 5, 7.5])
ax.set_yticks([])
ax.tick_params(labelsize=8)
despine(ax, left=True)
fig.canvas.draw()                      # 预绘一次, 供基因名实测字宽用
REND = fig.canvas.get_renderer()
INV = ax.transData.inverted()

BH, PITCH = 0.80, 1.08
for i, (gname, gcol, lgenes, rgenes) in enumerate(GROUPS):
    y0 = i * PITCH
    ax.add_patch(Rectangle((-5.1, y0), 13.4, BH, facecolor='0.93',
                           edgecolor='none', zorder=1))
    # 中央组色条
    ax.add_patch(Rectangle((-0.28, y0), 0.56, BH, facecolor=gcol,
                           edgecolor='0.45', lw=0.6, zorder=3))
    # 白底组名标签
    ax.text(0, y0 + BH / 2, gname, fontsize=7.5, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='0.3',
                      lw=0.8), zorder=6)
    # Down 簇 (青) / Up 簇 (深红)
    nd = 70
    xd = np.clip(r.normal(-2.3, 0.95, nd), -4.55, -0.5)
    yd = y0 + r.uniform(0.06, BH - 0.06, nd)
    ax.scatter(xd, yd, s=10, color='#29a3c9', alpha=0.85, lw=0, zorder=4)
    nu = 95
    xu = np.clip(r.normal(3.0, 1.5, nu), 0.4, 8.3)
    yu = y0 + r.uniform(0.06, BH - 0.06, nu)
    ax.scatter(xu, yu, s=10, color='#b02a30', alpha=0.85, lw=0, zorder=4)
    # 基因名: 上行/下行 两侧散布, 自右向左按"实测字宽"排布, 全部收在绘图区内
    # (不再溢出左轴外、也不再互相叠压; 越界即截断)
    tops = [g for g, row in lgenes if row == 1]
    bots = [g for g, row in lgenes if row != 1]
    for items, gy, right_x in ((tops, 0.72, -1.55), (bots, 0.38, -2.35)):
        cur = right_x
        for k, g in enumerate(items[:3]):
            t = ax.text(cur, y0 + gy, italic_gene(g), fontsize=7, ha='right',
                        va='center', color='#137a9a', zorder=6)
            bb = t.get_window_extent(renderer=REND)
            (wx0, _), (wx1, _) = INV.transform([(bb.x0, bb.y0),
                                                (bb.x1, bb.y1)])
            w = wx1 - wx0
            if cur - w < -5.02:
                t.remove()
                break
            if k < 2:                      # 近簇标签带短引线
                ax.plot([cur + 0.08, cur + 0.6], [y0 + gy, y0 + gy], lw=0.5,
                        color='#137a9a', zorder=5)
            cur -= w + 0.18
    for k, (g, row) in enumerate(rgenes):
        gx = 2.2 + 1.85 * ((k % 3) + 0.4 * row)
        gy = y0 + (0.70 if row == 1 else 0.36)
        ax.text(gx, gy, italic_gene(g), fontsize=7, ha='left', va='center',
                color='#8e1f24', zorder=6)
        if k < 2:
            ax.plot([gx - 0.7, gx - 0.08], [gy, gy], lw=0.5, color='#8e1f24',
                    zorder=5)

ax.set_xlabel('Log2 Fold Change', fontsize=10)
ax.set_ylabel('Comparison', fontsize=10, labelpad=8)

handles = [Line2D([], [], marker='o', ls='none', color='#29a3c9',
                  markersize=6, label='Significant Down'),
           Line2D([], [], marker='o', ls='none', color='#b02a30',
                  markersize=6, label='Significant Up')]
ax.legend(handles=handles, loc='upper right', bbox_to_anchor=(1.0, 1.02),
          fontsize=8, frameon=False, handletextpad=0.2)

# 中央彩条说明: 渐变色带 = 行序(自下而上), 与各行中央色条同色系
cmap_bar = mcolors.LinearSegmentedColormap.from_list(
    'rowbar', [g[1] for g in GROUPS])
cax = fig.add_axes([0.105, 0.950, 0.055, 0.015])
cax.imshow(np.linspace(0, 1, 128).reshape(1, -1), aspect='auto',
           cmap=cmap_bar)
cax.set_xticks([])
cax.set_yticks([])
for sp in cax.spines.values():
    sp.set_visible(True)
    sp.set_linewidth(0.6)
    sp.set_color('0.4')
fig.text(0.168, 0.9575, 'Central bar hue = row order: Malignant vs Benign '
         '(blue, bottom) \u2192 N+ vs N0 (red, top)', fontsize=7,
         color='0.25', ha='left', va='center')

save(fig, 'case_seg110.png')
