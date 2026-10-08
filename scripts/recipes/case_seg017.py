# -*- coding: utf-8 -*-
"""案例17 - Nature 分面山脊图。
参考 frames/seg_017.jpg: 上排 6 个 marker 分面, 每面 9 行亚群山脊
(c1-c8 + All cells, 蓝红绿紫灰橙黄浅蓝), 黑竖线 = 中位数,
左侧 Vγ9Vδ2 / Vδ1 括号; 底部 CD161 / NKG2A 两个加宽放大分面。"""
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import blended_transform_factory
from scipy.stats import gaussian_kde

set_style()
r = rng(17)

MARKERS = ['CD161', 'NKG2A', 'CD31', 'CD8', 'CD57', 'CD28']
ROWS = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'All cells']
COLS = ['#4a72b8', '#d6605f', '#57a55e', '#8073b8', '#6f6f6f',
        '#e29a4a', '#e7d36b', '#a9cbe3', '#cbcbcb']
# 每亚群 (主峰, 宽度, 次峰或 None); 各 marker 峰位再作扰动, 模拟真实表达分布
BASE = [(4.4, 0.75, None), (2.0, 0.90, (4.1, 0.50)), (2.9, 1.10, (0.7, 0.45)),
        (1.5, 0.85, (4.5, 0.60)), (2.5, 1.25, None), (2.6, 1.20, None),
        (2.3, 1.10, None), (2.1, 1.00, (3.5, 0.80)), (2.4, 1.35, None)]


def make_data(mi, ri, n=2500):
    pk, sd, sec = BASE[ri]
    pk = pk + 0.5 * np.sin(mi * 1.9 + ri * 1.1)
    v = r.normal(pk, sd, n).clip(-0.5, 7.5)
    if sec is not None:
        v = np.concatenate([v, r.normal(sec[0] + 0.3 * np.sin(mi + ri), sec[1], n // 6)])
    return v


def draw_facet(ax, data, show_y=False, min_h=0.72, br=None):
    x = np.linspace(-0.5, 7.5, 400)
    n = len(data)
    offs = -np.arange(n).astype(float)
    for i, (v, off, c) in enumerate(zip(data, offs, COLS)):
        k = gaussian_kde(v)(x)
        k /= k.max()
        ax.fill_between(x, off, off + min_h * k, color=c, lw=0, zorder=n - i)
        ax.plot(x, np.full_like(x, off), color='0.15', lw=0.6, zorder=n - i)
        med = np.median(v)
        ax.plot([med, med], [off, off + 0.92 * min_h], color='black', lw=1.0,
                zorder=n - i + 0.4)
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-n + 0.45, 1.0)
    ax.set_xticks([0, 2, 4, 6])
    ax.tick_params(labelsize=6)
    despine(ax)
    if show_y:
        line_x, text_x = br
        ax.set_yticks(offs)
        ax.set_yticklabels(ROWS, fontsize=7)
        ax.tick_params(axis='y', pad=12)
        tr = blended_transform_factory(ax.transAxes, ax.transData)
        for y1, y2, lab in [(offs[0], offs[3], 'Vγ9Vδ2'), (offs[5], offs[7], 'Vδ1')]:
            ax.plot([line_x, line_x], [y1, y2], transform=tr, clip_on=False,
                    color='black', lw=0.8)
            for yy in (y1, y2):
                ax.plot([line_x, line_x + 0.02], [yy, yy], transform=tr,
                        clip_on=False, color='black', lw=0.8)
            ax.text(text_x, (y1 + y2) / 2, lab, transform=tr, rotation=90,
                    ha='center', va='center', fontsize=7)
    else:
        ax.set_yticks([])


fig = plt.figure(figsize=cm2in(18, 17))
gs = fig.add_gridspec(2, 6, height_ratios=[1.0, 1.25], hspace=0.45, wspace=0.32,
                      left=0.10, right=0.98, top=0.925, bottom=0.065)
TOP_BR = (-0.05, -0.55)   # 组标签再左移, 与 c1-c8 行标签拉开间距, 避免文字相交
BOT_BR = (-0.02, -0.27)
ax_top = []
for mi, m in enumerate(MARKERS):
    ax = fig.add_subplot(gs[0, mi])
    ax_top.append(ax)
    draw_facet(ax, [make_data(mi, ri) for ri in range(9)],
               show_y=(mi == 0), br=TOP_BR)
    ax.set_title(m, fontsize=8, pad=4,
                 bbox=dict(boxstyle='square', ec='black', fc='white', lw=0.8))

for mi in range(2):  # 底部两个加宽放大分面, 仅左侧带行标签/括号
    ax = fig.add_subplot(gs[1, mi * 3:(mi + 1) * 3])
    draw_facet(ax, [make_data(mi, ri, n=4000) for ri in range(9)],
               show_y=(mi == 0), min_h=0.78, br=BOT_BR)
    ax.set_title(MARKERS[mi], fontsize=9, pad=4,
                 bbox=dict(boxstyle='square', ec='black', fc='white', lw=0.8))
    ax.tick_params(labelsize=7)

ax_top[2].annotate('Expression', xy=(0.5, -0.30), xycoords='axes fraction',
                   ha='center', va='center', fontsize=8)
save(fig, 'case_seg017.png')
