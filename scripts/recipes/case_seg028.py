# -*- coding: utf-8 -*-
"""案例28 - Science 火山图: 灰空心点火山 + 左右Top200虚线框 + 橙显著点
+ 气泡标签 + α=0.05虚线 + 底部基因集 UP/DN 条纹带。
参考: frames/seg_028.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

set_style()
r = rng(28)

# ---------------- 合成 5200 基因: log2FC 近正态, 显著性与 |FC| 相关
n = 5200
fc = r.normal(0, 0.75, n).clip(-3.05, 3.05)
sig = 0.25 + 1.45 * np.abs(fc) + r.normal(0, 0.55, n)
sig = np.clip(sig, 0, 6.15)

fig = plt.figure(figsize=cm2in(15.5, 17))
gs = fig.add_gridspec(2, 1, height_ratios=[4.2, 1.0], hspace=0.06,
                      left=0.13, right=0.97, top=0.965, bottom=0.055)
ax = fig.add_subplot(gs[0])
axs = fig.add_subplot(gs[1], sharex=ax)

# ---------------- 左右浅色底带 (基因集区域)
ax.add_patch(Rectangle((-2.8, 1.3), 2.55, 4.75, facecolor='#c9c4e2',
                       alpha=0.35, edgecolor='none', zorder=0))
ax.add_patch(Rectangle((0.25, 1.3), 2.75, 4.75, facecolor='#f2c9d4',
                       alpha=0.40, edgecolor='none', zorder=0))

# ---------------- 灰空心点火山
ax.scatter(fc, sig, s=13, facecolors='none', edgecolors='0.35',
           linewidths=0.55, alpha=0.7, zorder=2)
# 深一点的内层, 增加密度感
core = (np.abs(fc) < 0.8) & (sig < 2.8)
ax.scatter(fc[core], sig[core], s=9, facecolors='none', edgecolors='0.2',
           linewidths=0.45, alpha=0.55, zorder=3)

# ---------------- 橙色显著点 (通路成员, 遍布两侧)
nof = r.uniform(-2.45, 2.45, 130)
nsg = np.clip(r.uniform(0, 3.7, 130) ** 1.1, 0, 3.75)
ax.scatter(nof, nsg, s=30, color='#E8A33D', edgecolor='none', zorder=4)

# ---------------- Top 200 虚线框
for x0 in (-2.5, 0.8):
    ax.add_patch(Rectangle((x0, 1.95), 1.65, 4.05, fill=False,
                           edgecolor='black', lw=1.1, ls=':', zorder=5))
ax.text(-2.42, 5.72, 'Top 200', fontsize=10, va='top', zorder=6)
ax.text(2.37, 5.72, 'Top 200', fontsize=10, va='top', ha='right', zorder=6)

# ---------------- 气泡基因标签 (青色点 + 白底黑框)
key = [('KRAS', -2.85, 4.42), ('FOSL1', -1.45, 3.62), ('MYC', -0.60, 2.20)]
for g, gx, gy in key:
    ax.scatter([gx], [gy], s=46, facecolor='#39C0C8', edgecolor='#0d7a80',
               linewidth=0.9, zorder=7)
    ax.text(gx + 0.13, gy, italic_gene(g), fontsize=9.5, va='center',
            bbox=dict(boxstyle='round,pad=0.28', fc='white', ec='0.2',
                      lw=0.9), zorder=7)

# ---------------- 阈值线 / 轴面
ax.axhline(1.3, color='#d98a9c', ls=':', lw=1.3, zorder=1)
ax.axhline(0, color='0.45', lw=1.0, zorder=1)
ax.text(3.05, 1.42, '$\\alpha$ = 0.05', fontsize=9, ha='right',
        color='#c26a80', zorder=6)
ax.text(-1.95, 6.62, 'PDAC KRAS UP\n(KRAS-dependent)', fontsize=10,
        ha='center', color='#8f7bb8', linespacing=1.25)
ax.text(1.95, 6.62, 'PDAC KRAS DOWN\n(KRAS-inhibited)', fontsize=10,
        ha='center', color='#d98a9c', linespacing=1.25)

ax.set_xlim(-3.15, 3.15)
ax.set_ylim(-0.45, 7.25)
ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
ax.set_yticks([0, 2, 4, 6])
ax.set_ylabel('Significance (-log10 adj. p-val.)', fontsize=9)
plt.setp(ax.get_xticklabels(), visible=False)

# ---------------- 底部基因集条纹带 (UP 金色 / DN 灰色)
axs.set_ylim(0, 2)
axs.set_yticks([])
for s in ('top', 'right', 'left'):
    axs.spines[s].set_visible(False)
xu = np.concatenate([r.normal(0, 0.8, 230), r.uniform(-1.85, 1.85, 110)]).clip(-2.45, 2.35)
xd = np.concatenate([r.normal(0, 1.0, 180), r.uniform(-1.85, 1.85, 70)]).clip(-2.45, 2.35)
axs.vlines(xu, 1.28, 1.80, color='#E3B23C', lw=1.0, alpha=0.85)
axs.vlines(xd, 0.20, 0.72, color='#9a9a9a', lw=1.0, alpha=0.85)
# 端部白底标牌(全轨道高): 标签/ES 文字压在牌上, 竖线不穿字 (参考图同款留白)
axs.add_patch(Rectangle((-3.15, 0.0), 1.73, 2.0, facecolor='white',
                        edgecolor='none', zorder=4))
axs.add_patch(Rectangle((2.25, 0.0), 0.90, 2.0, facecolor='white',
                        edgecolor='none', zorder=4))
axs.text(-3.05, 1.54, 'KRAS_SIGNALING_UP', fontsize=9, va='center',
         color='#C99327', zorder=5)
axs.text(3.05, 1.54, 'ES: -0.51\npval: 4.9e-12', fontsize=7.5, va='center',
         ha='right', color='#C99327', linespacing=1.2, zorder=6,
         bbox=dict(boxstyle='round,pad=0.6', facecolor='white', alpha=0.9,
                   edgecolor='none'))
axs.text(-3.05, 0.46, 'KRAS_SIGNALING_DN', fontsize=9, va='center',
         color='#8a8a8a', zorder=5)
axs.text(3.05, 0.46, 'ES: 0.54\npval: 1.6e-08', fontsize=7.5, va='center',
         ha='right', color='#8a8a8a', linespacing=1.2, zorder=6,
         bbox=dict(boxstyle='round,pad=0.6', facecolor='white', alpha=0.9,
                   edgecolor='none'))
axs.set_xlabel('KRAS vs NS siRNA (log2FC)', fontsize=10)
axs.tick_params(labelsize=8)

save(fig, 'case_seg028.png')
