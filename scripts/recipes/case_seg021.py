# -*- coding: utf-8 -*-
"""案例21 - Nature 散点图(Python版): log-log散点 + 边际KDE填充 + 残差箱线inset。
参考: frames/seg_021.jpg — 蓝/紫/黑 半透明散点, 红虚线拟合, 灰虚参考线。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

set_style()

r = rng(21)
SLOPE, ICEPT = 1.08, -3.48

specs = [('MHQ SAG (N=226)', 226, '#4B9CD3', 6.22, 0.13),
         ('MHQ MAG (N=2288)', 2288, '#B9A6D0', 6.42, 0.24),
         ('MHQ WGS (N=3164)', 3164, '#1A1A1A', 6.62, 0.27)]
data = []
for name, n, c, mu, sd in specs:
    lx = r.normal(mu, sd, n)
    lx = np.clip(lx, 5.62, 7.32)
    ly = SLOPE * lx + ICEPT + r.normal(0, 0.055, n) + r.normal(0, 0.10, n) * (r.random(n) < 0.04)
    data.append((name, n, c, lx, ly))

allx = np.concatenate([d[3] for d in data])
ally = np.concatenate([d[4] for d in data])
k, b = np.polyfit(allx, ally, 1)
res = ally - (k * allx + b)

fig = plt.figure(figsize=cm2in(15.5, 15.0))
gs = fig.add_gridspec(2, 2, width_ratios=[3.3, 1.0], height_ratios=[1.0, 3.3],
                      hspace=0.06, wspace=0.06)
ax_top = fig.add_subplot(gs[0, 0])
ax_main = fig.add_subplot(gs[1, 0])
ax_rgt = fig.add_subplot(gs[1, 1])

# ---------------- 主散点(半透明) ----------------
for name, n, c, lx, ly in [data[0], data[2], data[1]]:
    ax_main.scatter(10 ** lx, 10 ** ly, s=16, color=c, alpha=0.40,
                    linewidths=0, label=name, zorder=3)
xf = np.linspace(5.65, 7.3, 50)
ax_main.plot(10 ** xf, 10 ** (k * xf + b), color='#D62728', ls='--', lw=1.8,
             zorder=4)

ax_main.set_xscale('log'); ax_main.set_yscale('log')
ax_main.set_xlim(5.6e5, 1.6e7); ax_main.set_ylim(5.8e2, 2.2e4)
ax_main.set_xlabel('Genome total size [bp] (corrected)', fontsize=9.5)
ax_main.set_ylabel('Number of predicted CDS (corrected)', fontsize=9.5)
ax_main.grid(True, which='major', ls='--', lw=0.8, color='#BFBFBF')
h, l = ax_main.get_legend_handles_labels()
order = [0, 2, 1]                                   # 图例顺序 SAG/MAG/WGS
ax_main.legend([h[i] for i in order], [l[i] for i in order],
               loc='upper left', frameon=True, framealpha=0.9,
               edgecolor='#999999', fontsize=8.5, handletextpad=0.3)
ax_main.tick_params(which='minor', length=2)

# ---------------- 边际 KDE 填充(log 域) ----------------
gx = np.linspace(5.5, 7.4, 300)
ax_top.set_xscale('log')
for name, n, c, lx, ly in data:
    d = gaussian_kde(lx)(gx); d = d / d.max() * 0.92
    ax_top.fill_between(10 ** gx, 0, d, color=c, alpha=0.35, lw=1.0)
    ax_top.plot(10 ** gx, d, color=c, lw=1.0)
ax_top.set_xlim(5.6e5, 1.65e7); ax_top.set_ylim(0, 1)
ax_top.set_yticks([]); ax_top.set_xticks([])
ax_top.tick_params(labelbottom=False)
despine(ax_top, left=True)

gy = np.linspace(2.75, 4.4, 300)
ax_rgt.set_yscale('log')
for name, n, c, lx, ly in data:
    d = gaussian_kde(ly)(gy); d = d / d.max() * 0.92
    ax_rgt.fill_betweenx(10 ** gy, 0, d, color=c, alpha=0.35, lw=1.0)
    ax_rgt.plot(d, 10 ** gy, color=c, lw=1.0)
ax_rgt.set_ylim(5.8e2, 2.2e4); ax_rgt.set_xlim(0, 1)
ax_rgt.set_xticks([]); ax_rgt.set_yticks([])
ax_rgt.tick_params(labelleft=False)
despine(ax_rgt, bottom=True)

# ---------------- 残差箱线 inset ----------------
axi = ax_main.inset_axes([0.47, 0.10, 0.50, 0.32])
axi.set_xscale('linear'); axi.set_yscale('linear')
res_by = [res[:226], res[226:2514], res[2514:]]
order2 = [2, 1, 0]
cols = ['#4B9CD3', '#B9A6D0', '#7F8890']
for pos, oi in zip([3, 2, 1], order2):
    rr = res_by[oi]
    bp = axi.boxplot(rr, orientation='horizontal', positions=[pos], widths=0.5,
                     patch_artist=True, showfliers=False,
                     medianprops=dict(color='black', lw=1.0),
                     whiskerprops=dict(color='black', lw=0.8),
                     capprops=dict(color='black', lw=0.8))
    bp['boxes'][0].set_facecolor(cols[pos - 1])
    bp['boxes'][0].set_edgecolor('#555555')
    bp['boxes'][0].set_linewidth(0.8)
    jit = rng(60 + pos).uniform(-0.13, 0.13, len(rr))
    axi.scatter(rr, pos + jit, s=3, color='#333333', zorder=3)

def bracket(y1, y2, x, txt):
    axi.plot([x, x + 0.045, x + 0.045, x], [y1, y1, y2, y2], lw=0.8, c='black')
    axi.text(x + 0.075, (y1 + y2) / 2, txt, va='center', fontsize=6.5)

bracket(2.06, 2.94, 0.72, '**')
bracket(1.06, 1.94, 0.60, '****')
bracket(1.06, 2.94, 0.90, '****')
axi.set_xlim(-0.62, 1.08)
axi.set_ylim(0.5, 3.5)
axi.set_yticks([])
axi.set_xticks([-0.5, 0.0, 0.5, 1.0])
axi.set_xticklabels(['-0.5', '0.0', '0.5', '1.0'])
axi.tick_params(labelsize=6.5)
axi.set_title('Residuals (log)', fontsize=7.5, pad=2)
axi.set_facecolor('white')
for s in axi.spines.values():
    s.set_visible(True)
    s.set_linewidth(0.7)

save(fig, 'case_seg021.png')
