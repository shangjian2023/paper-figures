# -*- coding: utf-8 -*-
"""案例146 - 火山+GO条形复合图: 上左粉底横条形(上调GO)+上右蓝底横条形(下调GO),
条形上写GO名+下附代表基因; 下火山图(红显著/蓝未达FC/灰NS), 虚线阈值,
粉/蓝背景呼应, 基因名引线。参考: frames/seg_146.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle

set_style()
r = rng(146)

fig = plt.figure(figsize=cm2in(15, 17))
gs = fig.add_gridspec(2, 2, left=0.115, right=0.965, top=0.955, bottom=0.062,
                      height_ratios=[0.92, 1.55], wspace=0.52, hspace=0.30)

# ================= 上排条形 =================
GO_L = [('Tuberculosis', 2.55, 'Camp, Lbp, Mrc1'),
        ('Motor proteins', 2.48, 'Myl1, Mylpf, Tubb4b'),
        ('Toll-like receptor signaling pathway', 2.10, 'Lbp, Spp1'),
        ('Cytoskeleton in muscle cells', 1.52, 'Myl1, Mylpf'),
        ('Salmonella infection', 1.30, 'Mylpf, Tubb4b')]
GO_R = [('Complement and coagulation cascades', 6.0,
         'Cfd, C2, C4b, C9, Serpind1, Tfpi, F12'),
        ('ECM-receptor interaction', 3.0, 'Comp, Itga2, Itgb1, Thbs4, Tnc'),
        ('Focal adhesion', 2.7, 'Comp, Itga2, Itgb1, Thbs4, Tnc, Rap1b'),
        ('PI3K-Akt signaling pathway', 2.4,
         'Cdc37, Comp, Hsp90ab1, Itga2, Itgb1'),
        ('Platelet activation', 1.9, 'Itga2, Fermt3, Rap1b')]


def go_bar(ax, rows, base, hi, xmax, xticks, xlab):
    nr = len(rows)
    bc = np.array(mcolors.to_rgb(base))
    hc = np.array(mcolors.to_rgb(hi))
    for i, (term, val, genes) in enumerate(rows):
        y = nr - 1 - i
        frac = np.clip((val - 0.9) / (6.0 - 0.9), 0, 1)
        c = tuple(bc + (hc - bc) * frac)
        ax.barh(y, val, height=0.50, facecolor=c, edgecolor='none')
        ax.text(0.06, y, term, fontsize=7.6, va='center', color='#222222')
        ax.text(0.06, y - 0.50, genes, fontsize=7.0, va='center', color=base)
    ax.set_ylim(-1.45, nr - 0.15)
    ax.set_xlim(0, xmax)
    ax.set_xticks(xticks)
    ax.tick_params(labelsize=7.5, length=2)
    ax.set_xlabel(xlab, fontsize=9)
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.set_yticks([])


axl = fig.add_subplot(gs[0, 0])
go_bar(axl, GO_L, '#e89ab8', '#e05a8a', 3.2, [0, 1, 2, 3],
       '$-$ log$_{10}$(p)')
axl.set_title('', pad=0)
axr = fig.add_subplot(gs[0, 1])
go_bar(axr, GO_R, '#aebfd4', '#7e97b8', 6.8, [0, 2, 4, 6],
       '$-$ log$_{10}$(p)')

# ================= 下火山 =================
axv = fig.add_subplot(gs[1, :])
axv.add_patch(Rectangle((-4.35, 1.3), 3.8, 5.2, facecolor='#fdeef4',
                        edgecolor='none', zorder=0))
axv.add_patch(Rectangle((0.55, 1.3), 3.8, 5.2, facecolor='#e9eef6',
                        edgecolor='none', zorder=0))

n = 2800
fc = r.normal(0, 1.15, n)
# y = -log10(p): p∈(0,1) → y 天然非负; 下限 0.08 让点云浮在 y=0 轴线上方
pv = r.exponential(0.8, n) + 0.25 * np.abs(fc)
pv = np.clip(pv, 0.08, 6.3)
sig = pv > 1.3
ns = ~sig
# 蓝色: p 达标但 |FC| 未达阈 (贴着两条虚线内侧的竖带)
blue = sig & (np.abs(fc) <= 0.62)
red = sig & (np.abs(fc) > 0.62)
# 蓝点横向收拢成贴线的窄竖带
mb = blue.sum()
fc[blue] = np.sign(fc[blue]) * (0.62 - 0.34 * r.random(mb))
axv.scatter(fc[ns], pv[ns], s=13, color='#8a8a8a', alpha=0.8, lw=0, zorder=2)
axv.scatter(fc[blue], pv[blue], s=13, color='#7fa8d0', alpha=0.9, lw=0,
            zorder=3)
axv.scatter(fc[red], pv[red], s=13, color='#c0392b', alpha=0.9, lw=0,
            zorder=3)

axv.axvline(-0.62, color='black', ls='--', lw=1.1, zorder=1)
axv.axvline(0.62, color='black', ls='--', lw=1.1, zorder=1)
axv.axhline(1.3, color='black', ls='--', lw=1.1, zorder=1)

# ---------------- 基因引线标注
LEFT_LAB = [('KRAS', -2.15, 4.92), ('STARD3NL', -1.35, 4.78),
            ('NT5E', -1.72, 4.22), ('HMGA2', -2.02, 3.32),
            ('ETV1', -1.90, 2.92), ('PTX3', -1.30, 2.56),
            ('TMEM156', -2.22, 2.14), ('NAV3', -1.06, 2.10),
            ('GALNT3', -2.30, 1.68)]
RIGHT_LAB = [('HIPK3', 1.15, 5.62), ('EMP2', 1.92, 5.12),
             ('CHPF', 1.52, 4.02), ('EXOC3L1', 2.22, 2.78),
             ('SCRN1', 0.95, 2.62), ('KCNK3', 1.70, 2.22),
             ('RUNDC3A', 0.92, 1.86), ('SMTNL2', 2.30, 1.62),
             ('PCDHGA12', 1.90, 1.38)]
for g, x, y in LEFT_LAB:
    axv.text(x, y, italic_gene(g), fontsize=7.4, ha='center', va='center',
             color='#1a1a1a', zorder=6)
for g, x, y in RIGHT_LAB:
    axv.text(x, y, italic_gene(g), fontsize=7.4, ha='center', va='center',
             color='#1a1a1a', zorder=6)
# NPPC 引线
axv.scatter([2.42], [2.05], s=20, color='#c0392b', zorder=5)
axv.annotate(italic_gene('NPPC'), (2.42, 2.05), xytext=(3.15, 2.18),
             fontsize=7.4, va='center', zorder=6,
             arrowprops=dict(arrowstyle='-', lw=0.7, color='black'))

axv.set_xlim(-4.35, 4.35)
axv.set_ylim(0, 6.5)
axv.set_xticks([-3, -2, -1, 0, 1, 2, 3])
axv.set_yticks([0, 2, 4, 6])
axv.tick_params(labelsize=7.5)
axv.set_xlabel('log$_2$(FC)', fontsize=9.5)
axv.set_ylabel('$-$ log$_{10}$(p)', fontsize=9.5)

save(fig, 'case_seg146.png')
