# -*- coding: utf-8 -*-
"""案例45(seg44) - Nature 散点+直方图双面板: 上a直方图(左计数/右概率密度),
下b散点(光谱型着色+双向误差棒+log y轴+右侧离散色条)。参考: frames/seg_044.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.colorbar import ColorbarBase

set_style()

SPECTRA = [('WN(h)', '#0B2F7A'), ('O2', '#1D5FA8'), ('O3', '#4E9BC9'),
           ('O4', '#93C6E0'), ('O5', '#CDE9F3'), ('O6', '#F9DC8A'),
           ('O7', '#F5B657'), ('O8', '#EE8437'), ('O9', '#D6402C'),
           ('B or later', '#9E1220'), ('Unknown', '#8C8C8C')]
scolors = [c for _, c in SPECTRA]

r = rng(44)
n = 46
# 光谱型抽样权重: 早型+未知多
w = np.array([2, 3, 5, 5, 4, 4, 4, 4, 4, 3, 8], float)
cls = r.choice(len(SPECTRA), n, p=w / w.sum())
age = r.uniform(0.06, 2.90, n)
vel = (10 ** r.normal(np.log10(55), 0.28, n)).clip(24, 200)
xe = r.uniform(0.03, 0.22, n)
ye = r.uniform(4, 38, n)

fig = plt.figure(figsize=cm2in(13.5, 14.0))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 2.4], hspace=0.08,
                      left=0.13, right=0.86, top=0.97, bottom=0.08)
ax_a = fig.add_subplot(gs[0])
ax_b = fig.add_subplot(gs[1], sharex=ax_a)
plt.setp(ax_a.get_xticklabels(), visible=False)

# ---------------- 面板 a: 直方图 + KDE ----------------
bins = np.arange(0, 3.01, 0.167)
cnt, edges = np.histogram(age, bins=bins)
ax_a.bar(edges[:-1], cnt, width=np.diff(edges), align='edge',
         color='#9E97E8', edgecolor='#5B54B8', lw=0.8, zorder=2)
ax_a.set_ylabel('Number of\nrunaways', fontsize=8.5)
ax_a.set_ylim(0, 8)
ax_a.set_yticks([0, 2, 4, 6, 8])

xk = np.linspace(0, 3, 300)
kde = (0.40 * np.exp(-((xk - 0.25) / 0.42) ** 2)
       + 0.50 * np.exp(-((xk - 1.75) / 0.40) ** 2)
       + 0.34 * np.exp(-((xk - 2.50) / 0.35) ** 2)
       + 0.06)
ax_a2 = ax_a.twinx()
ax_a2.plot(xk, kde, color='black', lw=1.4, zorder=3)
ax_a2.set_ylim(0, 0.6)
ax_a2.set_yticks([0.0, 0.2, 0.4, 0.6])
ax_a2.set_ylabel('Probability\nDensity', fontsize=8.5)
panel_label(ax_a, 'a', dx=0.015, dy=0.97)

# ---------------- 面板 b: 散点 + 误差棒 ----------------
for i in range(n):
    c = scolors[cls[i]]
    filled = r.random() < 0.55
    square = r.random() < 0.25
    mk = 's' if square else 'o'
    if filled:
        ax_b.scatter(age[i], vel[i], s=46, marker=mk, color=c,
                     edgecolors='black', linewidths=0.7, zorder=4)
    else:
        ax_b.scatter(age[i], vel[i], s=46, marker=mk, facecolors=c,
                     edgecolors='black', linewidths=0.9, zorder=4, alpha=0.95)
    ax_b.errorbar(age[i], vel[i], xerr=xe[i], yerr=ye[i], fmt='none',
                  ecolor='#555555', elinewidth=0.8, capsize=0, zorder=2)

ax_b.axhline(28, color='black', ls='--', lw=1.0, zorder=3)
ax_b.set_yscale('log')
ax_b.set_ylim(20, 250)
ax_b.set_yticks([20, 30, 50, 100, 150, 200, 250])
ax_b.yaxis.set_major_formatter(plt.ScalarFormatter())
ax_b.yaxis.set_minor_formatter(plt.NullFormatter())
ax_b.set_xlim(0, 3.0)
ax_b.set_xlabel('Kinematic age (Myr)', fontsize=9.5)
ax_b.set_ylabel(r'Transverse velocity (km s$^{-1}$)', fontsize=9.5)
ax_b.tick_params(which='minor', length=2)
panel_label(ax_b, 'b', dx=0.012, dy=0.98)

# ---------------- 右侧离散色条 ----------------
cmap = ListedColormap(scolors)
norm = BoundaryNorm(np.arange(len(scolors) + 1), cmap.N)
cax = fig.add_axes([0.89, 0.08, 0.035, 0.60])
cb = ColorbarBase(cax, cmap=cmap, norm=norm, ticks=np.arange(len(scolors)) + 0.5)
cax.set_yticklabels([n for n, _ in SPECTRA], fontsize=7.5)
cax.tick_params(length=0)
cax.set_ylabel('Spectral type runaways', fontsize=8.5, labelpad=6)
for sp in cax.spines.values():
    sp.set_linewidth(0.8)

save(fig, 'case_seg044.png')
