# -*- coding: utf-8 -*-
"""案例81 - Nature 时间序列图(三): 4 脑区比值轨迹 small-multiple。
参考: frames/seg_079.jpg — 上排 4 小面板(S1BF 紫/CA1 蓝/LD 绿/Cpu 红)
比值轨迹 + 淡色 SEM 带, t=0 阶跃; 下方 1 大面板紫色放大重绘, 线段式图例。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()

regions = [
    ('S1BF', '#9B30D9', 3.90, 3.85, 1.6),
    ('CA1', '#2E6FBF', 3.70, 3.55, 0.6),
    ('LD', '#3FA83F', 3.75, 3.52, 1.0),
    ('Cpu', '#DE6B6B', 3.65, 3.23, 0.6),
]
t = np.linspace(-10, 20, 301)


def trace(base, post, t0, r, noise=0.016):
    step = base + (post - base) / (1 + np.exp(-(t - t0) / 0.35))
    y = step + r.normal(0, noise, t.size)
    sem = 0.020 + 0.010 * np.abs(np.sin(np.linspace(0, 9, t.size)))
    return y, sem


fig = plt.figure(figsize=cm2in(17.0, 15.0))
gs = fig.add_gridspec(2, 4, height_ratios=[1.0, 1.35], hspace=0.52,
                      wspace=0.42)

for k, (name, c, base, post, t0) in enumerate(regions):
    ax = fig.add_subplot(gs[0, k])
    r = rng(790 + k)
    y, sem = trace(base, post, t0, r, noise=0.014)
    ax.fill_between(t, y - sem, y + sem, color=c, alpha=0.30, lw=0)
    ax.plot(t, y, color=c, lw=1.0)
    ax.legend([Line2D([], [], color=c, lw=1.4)], [name], loc='upper right',
              frameon=False, fontsize=7.5, handlelength=1.1,
              handletextpad=0.5, borderaxespad=0.1)
    ax.set_xlim(-11, 21)
    lo, hi = min(base, post), max(base, post)
    ax.set_ylim(lo - 0.16, hi + 0.12)
    ax.set_xticks([-10, -5, 0, 5, 10, 15, 20])
    ax.tick_params(labelsize=6.5)
    ax.set_xlabel('Time (s)', fontsize=8)
    if k == 0:
        ax.set_ylabel('F$_{570}$/F$_{595}$ Ratio', fontsize=8)

# ---- 下方大面板: S1BF 放大重绘(与上排同源数据, 注明语义避免误读) ----
ax = fig.add_subplot(gs[1, :])
r = rng(790)
y, sem = trace(3.90, 3.85, 1.6, r, noise=0.018)
ax.fill_between(t, y - sem, y + sem, color='#9B30D9', alpha=0.32, lw=0)
ax.plot(t, y, color='#7A1EC2', lw=1.3)
ax.legend([Line2D([], [], color='#7A1EC2', lw=1.8)], ['S1BF'],
          loc='upper left', bbox_to_anchor=(0.34, 1.02), frameon=False,
          fontsize=10, handlelength=1.6)
ax.set_title('mean \u00b1 SEM (magnified)', fontsize=8.5, pad=3)
ax.set_xlim(-11, 21)
ax.set_ylim(3.74, 4.0)
ax.set_xticks([-10, -5, 0, 5, 10, 15, 20])
ax.set_yticks([3.8, 3.9, 4.0])
ax.set_xlabel('Time (s)')
ax.set_ylabel('F$_{570}$/F$_{595}$ Ratio')

save(fig, 'case_seg079.png')
