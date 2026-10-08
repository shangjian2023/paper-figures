# -*- coding: utf-8 -*-
"""案例88 - Nature 2×3 拟合散点: 上排 碳库变化 vs 初始碳库(线性拟合), 下排 vs 时长(指数衰减+CI带)。
参考: frames/seg_086.jpg — Mangrove / Saltmarsh / Seagrass 三大生态系统。"""
import sys, os
import zlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()

fig, axs = plt.subplots(2, 3, figsize=cm2in(21.5, 12.5))
UC = ['#F2A0B8', '#BFCF3A', '#8FCBEE']   # 顶栏下划线色

# ---------- 顶行辅助 ----------
def top_panel(ax, title, groups, xlim, ylim, xticks, yticks, r2p, uc):
    ax.set_title(title, fontweight='bold', fontsize=9, pad=17)
    ax.plot([0.04, 0.96], [1.09, 1.09], color=uc,
            lw=2.2, clip_on=False, transform=ax.transAxes, zorder=5)
    for c, lab, mu, sd, n_, slope, sl_sd in groups:
        rr = rng(zlib.crc32(lab.encode('utf-8')) % 9999)  # 确定性 seed(hash() 每进程随机)
        x = np.clip(rr.normal(mu, sd, n_), xlim[0] + 5, xlim[1])
        y = slope * x + rr.normal(0, sl_sd, n_)
        y = np.clip(y, ylim[0], ylim[1])
        ax.scatter(x, y, s=11, color=c, alpha=0.8, linewidths=0, zorder=3)
        xs = np.linspace(max(x.min(), 5), x.max(), 20)
        ax.plot(xs, slope * xs, color=c, lw=1.4, zorder=4)
    xr = np.linspace(0, xlim[1], 10)
    ax.plot(xr, -0.25 * xr, ls='--', lw=0.8, color='0.55', zorder=2)
    ax.plot(xr, -0.75 * xr, ls='--', lw=0.8, color='0.25', zorder=2)
    ax.set_xlim(xlim); ax.set_ylim(ylim)
    ax.set_xticks(xticks); ax.set_yticks(yticks)
    for i, (c, txt) in enumerate(r2p):
        ax.text(0.03, 0.965 - i * 0.075, txt, transform=ax.transAxes, fontsize=5.2,
                color=c, va='top')
    # 组内图例: 干扰类型色点 + 25%/75% loss 虚线键, 放右上空白角
    handles = [Line2D([], [], ls='', marker='o', ms=3.2, color=c, label=lab)
               for c, lab, *_ in groups]
    handles.append(Line2D([], [], ls='--', lw=0.8, color='0.55',
                          label='25% loss'))
    handles.append(Line2D([], [], ls='--', lw=0.8, color='0.25',
                          label='75% loss'))
    ax.legend(handles=handles, loc='upper right', fontsize=5, frameon=False,
              handlelength=1.5, borderaxespad=0.25, labelspacing=0.32,
              handletextpad=0.45)

def bottom_panel(ax, A, k, base, col, band_col, xlim, ylim, r2p, seed):
    rr = rng(seed)
    x = np.clip(rr.uniform(1, xlim[1], 55), 0, xlim[1])
    y = base + A * np.exp(-x / k) + rr.normal(0, 38, 55)
    y = np.clip(y, ylim[0] + 5, ylim[1])
    ax.scatter(x, y, s=13, color=col, alpha=0.8, linewidths=0, zorder=3)
    xs = np.linspace(0.5, xlim[1], 200)
    yc = base + A * np.exp(-xs / k)
    resid = y - (base + A * np.exp(-x / k))
    band = 1.96 * resid.std(ddof=2)
    ax.fill_between(xs, yc - band, yc + band, color=band_col, alpha=0.5, lw=0, zorder=2)
    ax.plot(xs, yc, color=col, lw=1.4, zorder=4)
    ax.set_xlim(xlim); ax.set_ylim(ylim)
    for i, (c, txt) in enumerate(r2p):
        ax.text(0.04, 0.96 - i * 0.085, txt, transform=ax.transAxes, fontsize=5.6,
                color=c, va='top')

# ================= a Mangrove =================
axa = axs[0, 0]
ga = [('#D95F02', 'Agriculture', 260, 120, 20, -0.55, 90),
      ('#8B1A1A', 'Aquaculture', 200, 100, 18, -0.50, 110),
      ('#C510B0', 'Climate/hydrological change', 380, 150, 14, -0.45, 130),
      ('#8B6E4E', 'Harvesting', 620, 240, 18, -0.10, 70)]
top_panel(axa, 'Mangrove', ga, (0, 1200), (-800, 800), np.arange(0, 1201, 200),
          np.arange(-800, 801, 400),
          [('#B03030', '$R^2$ = 0.89  $P$ < 0.001'), ('#8B1A1A', '$R^2$ = 0.45  $P$ < 0.001'),
           ('#C510B0', '$R^2$ = 0.06  $P$ = 0.855'), ('#8B6E4E', '$R^2$ = 0.04  $P$ = 0.298')],
          uc=UC[0])
_refbb = dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.85)
axa.text(1185, -262, '25% loss', ha='right', va='bottom', fontsize=5.2,
         color='0.45', bbox=_refbb, zorder=6)
axa.text(1052, -756, '75% loss', ha='right', va='center', fontsize=5.2,
         color='0.25', bbox=_refbb, zorder=6)
panel_label(axa, 'a', dx=-0.09)
axa.set_xlabel(r'Initial soil C$_{\mathrm{org}}$ stock (Mg C ha$^{-1}$)', fontsize=7)
axa.set_ylabel(r'Soil C$_{\mathrm{org}}$ stock change (Mg C ha$^{-1}$)', fontsize=7)

# ================= b Saltmarsh =================
axb = axs[0, 1]
gb = [('#35B57A', 'Agriculture', 90, 45, 26, 0.55, 55),
      ('#8F8B1A', 'Climate/hydrological change', 210, 80, 20, -0.85, 70)]
top_panel(axb, 'Saltmarsh', gb, (0, 400), (-400, 400), np.arange(0, 401, 100),
          np.arange(-400, 401, 200),
          [('#35B57A', '$R^2$ = 0.74  $P$ < 0.001'), ('#8F8B1A', '$R^2$ = 0.16  $P$ = 0.044')],
          uc=UC[1])
panel_label(axb, 'b', dx=-0.13)
axb.set_xlabel(r'Initial soil C$_{\mathrm{org}}$ stock (Mg C ha$^{-1}$)', fontsize=7)

# ================= c Seagrass =================
axc = axs[0, 2]
gc = [('#2B4FA8', 'Dredging', 120, 70, 18, -0.55, 45),
      ('#66B2E8', 'Vegetation cover damage', 170, 90, 14, -0.25, 40)]
top_panel(axc, 'Seagrass', gc, (0, 500), (-400, 200), np.arange(0, 501, 100),
          np.arange(-400, 201, 200),
          [('#2B4FA8', '$R^2$ = 0.20  $P$ = 0.143'), ('#66B2E8', '$R^2$ = 0.10  $P$ = 0.109')],
          uc=UC[2])
panel_label(axc, 'c', dx=-0.13)
axc.set_xlabel(r'Initial soil C$_{\mathrm{org}}$ stock (Mg C ha$^{-1}$)', fontsize=7)

# ================= d/e/f 底行 =================
axd = axs[1, 0]
bottom_panel(axd, 140, 8, -85, '#D97030', '#F6C9BC', (0, 50), (-100, 500),
             [('#C0392B', '$R^2$ = 0.34  $P$ = 0.039'), ('#D97030', '$R^2$ = 0.17  $P$ = 0.013'),
              ('#E8A030', '$R^2$ = 0.07  $P$ = 0.237')], 861)
panel_label(axd, 'd', dx=-0.09)
axd.set_xlabel('Duration (Years)', fontsize=7)
axd.set_ylabel(r'Soil C$_{\mathrm{org}}$ stock change (%)', fontsize=7)

axe = axs[1, 1]
bottom_panel(axe, 220, 80, -105, '#35B57A', '#BDE8D2', (0, 500), (-100, 400),
             [('#35B57A', '$R^2$ = 0.23  $P$ = 0.002'), ('#8F8B1A', '$R^2$ = 0.06  $P$ = 0.215'),
              ('#2B6FB8', '$R^2$ = 0.54  $P$ = 0.098')], 862)
panel_label(axe, 'e', dx=-0.13)
axe.set_xlabel('Duration (Years)', fontsize=7)

axf = axs[1, 2]
bottom_panel(axf, 145, 4, -52, '#2B4FA8', '#D5D5D5', (0, 100), (-100, 100),
             [('#2B4FA8', '$R^2$ = 0.41  $P$ = 0.035'), ('#66B2E8', '$R^2$ = 0.04  $P$ = 0.417')],
             863)
panel_label(axf, 'f', dx=-0.13)
axf.set_xlabel('Duration (Years)', fontsize=7)

fig.subplots_adjust(left=0.075, right=0.99, top=0.94, bottom=0.10,
                    wspace=0.30, hspace=0.38)
save(fig, 'case_seg086.png')
