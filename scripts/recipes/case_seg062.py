# -*- coding: utf-8 -*-
"""案例64 - Nature 拟合气泡图 2×2: a/b 虚线1:1, c/d 拟合线+置信带, 气泡=深度3档, 色=8站点。
参考: frames/seg_062.jpg — EHTA/ELTA WOD vs mooring 对比。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()

stations = ['KEO', 'WHOTS', 'MOVE-3', 'RAMA-N', 'RAMA-S', 'IMOS', 'Stratus', 'PIRATA']
scolors = ['#00BFC4', '#3B6E8F', '#8F7FD8', '#1F2FA8',
           '#D62728', '#E8630A', '#B8860B', '#F2D02E']
depth_s = [8, 26, 105]           # 10 m / 100 m / 1000 m
depth_p = [0.25, 0.42, 0.33]     # 各档抽样概率

r = rng(62)
def draw_depth(n):
    d = r.choice(3, n, p=depth_p)
    return d

def bubble_noise(n, lo, hi):
    return np.clip(r.normal(0, 0.10 * (hi - lo), n), lo, hi)

fig, axs = plt.subplots(2, 2, figsize=cm2in(16.5, 17.0))
axa, axb, axc, axd = axs.ravel()

def panel_bubbles(ax, xs, ys, ds):
    for i in range(len(xs)):
        ax.scatter(xs[i], ys[i], s=depth_s[ds[i]], color=scolors[i % 8],
                   alpha=0.85, linewidths=0, zorder=3)

# ---- a: EHTA_WOD vs EHTA_mooring (0-3)
n = 130
xm = np.clip(r.gamma(2.0, 0.55, n), 0.03, 2.9)
yw = np.clip(xm + r.normal(0.05, 0.14, n), 0.02, 2.95)
ds = draw_depth(n)
panel_bubbles(axa, xm, yw, ds)
axa.plot([0, 3], [0, 3], ls='--', color='black', lw=1.0, zorder=2)
axa.set_xlim(0, 3); axa.set_ylim(0, 3)
axa.set_xticks([0, 1, 2, 3]); axa.set_yticks([0, 1, 2, 3])
axa.set_xlabel(r'EHTA_mooring ($^\circ$C)'); axa.set_ylabel(r'EHTA_WOD ($^\circ$C)')
panel_label(axa, 'a', dx=-0.18, dy=1.02)

# ---- b: ELTA_WOD vs ELTA_mooring (-3..0)
xm = -np.clip(r.gamma(2.0, 0.55, n), 0.03, 2.9)
yw = np.clip(xm + r.normal(-0.05, 0.18, n), -2.95, -0.02)
ds = draw_depth(n)
panel_bubbles(axb, xm, yw, ds)
axb.plot([-3, 0], [-3, 0], ls='--', color='black', lw=1.0, zorder=2)
axb.set_xlim(-3, 0); axb.set_ylim(-3, 0)
axb.set_xticks([-3, -2, -1, 0]); axb.set_yticks([-3, -2, -1, 0])
axb.set_xlabel(r'ELTA_mooring ($^\circ$C)'); axb.set_ylabel(r'ELTA_WOD ($^\circ$C)')
panel_label(axb, 'b', dx=-0.18, dy=1.02)

# ---- c/d: 百分比 + 拟合线与置信带
def panel_fit(ax, slope, se, xlo, xhi, xl, yl, letter):
    m = 120
    x0 = np.clip(r.gamma(1.7, 14, m) + 2, 1, 78)
    y0 = np.clip(slope * x0 + r.normal(0, 7.5, m), 0.5, 66)
    ds = draw_depth(m)
    panel_bubbles(ax, x0, y0, ds)
    xf = np.linspace(0, 80, 50)
    ax.plot(xf, slope * xf, color='black', lw=1.3, zorder=4)
    half = 1.96 * se * xf
    ax.fill_between(xf, slope * xf - half, slope * xf + half, color='0.82', zorder=1)
    ax.plot([0, 80], [0, 80], ls='--', color='black', lw=1.0, zorder=2)
    ax.set_xlim(0, 80); ax.set_ylim(0, 80)
    ax.set_xticks([0, 20, 40, 60, 80]); ax.set_yticks([0, 20, 40, 60, 80])
    ax.set_xlabel(xl); ax.set_ylabel(yl)
    ax.text(0.06, 0.94, r'$y$ = (%.2f $\pm$ %.2f)$x$' % (slope, se),
            transform=ax.transAxes, va='top', fontsize=8)
    panel_label(ax, letter, dx=-0.18, dy=1.02)

panel_fit(axc, 0.80, 0.08, 0, 80,
          r'$p_{\mathrm{EHTA\_AE\_mooring}}$ (%)', r'$p_{\mathrm{EHTA\_AE\_WOD}}$ (%)', 'c')
panel_fit(axd, 0.74, 0.05, 0, 80,
          r'$p_{\mathrm{ELTA\_CE\_mooring}}$ (%)', r'$p_{\mathrm{ELTA\_CE\_WOD}}$ (%)', 'd')

# ---- 底部共享图例: 站点两行 + 尺寸一行
h_sta = [Line2D([], [], marker='o', ls='', markersize=7,
                markerfacecolor=c, markeredgecolor=c) for c in scolors]
leg1 = fig.legend(h_sta, stations, loc='lower center', bbox_to_anchor=(0.5, 0.088),
                  ncol=4, frameon=False, fontsize=8, columnspacing=1.6,
                  handletextpad=0.4)
h_sz = [Line2D([], [], marker='o', ls='', markersize=ms, markerfacecolor='0.45',
               markeredgecolor='0.45') for ms in (2.2, 5.5, 10)]
leg2 = fig.legend(h_sz, ['10 m', '100 m', '1,000 m'], loc='lower center',
                  bbox_to_anchor=(0.5, 0.008), ncol=3, frameon=False, fontsize=8,
                  columnspacing=2.2, handletextpad=0.5)
fig.subplots_adjust(left=0.09, right=0.98, top=0.97, bottom=0.22,
                    hspace=0.34, wspace=0.34)

save(fig, 'case_seg062.png')
