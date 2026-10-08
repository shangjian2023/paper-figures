# -*- coding: utf-8 -*-
"""案例112 - iMeta 火山图+富集图(二): 上火山(深蓝下调/深红上调/灰NS, 虚线阈值)
+ 下两张水平条形(紫/绯红), 通路条+成员基因文本+mini色标。
参考: frames/seg_112.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle

set_style()
r = rng(112)

fig = plt.figure(figsize=cm2in(15, 18.5))
gs = fig.add_gridspec(2, 2, left=0.105, right=0.965, top=0.925, bottom=0.055,
                      height_ratios=[1.05, 1.0], wspace=0.42, hspace=0.42)
axv = fig.add_subplot(gs[0, :])

# ================= 火山 =================
n = 950
fc = r.normal(0.4, 1.9, n)
pv = r.exponential(0.75, n) + 0.12 * np.abs(fc)
pv = np.clip(pv, 0.02, 4.45)
sig = pv > 1.3
up = sig & (fc > 0.35)
dn = sig & (fc < -0.5)
ns = ~(up | dn)
axv.scatter(fc[ns], pv[ns], s=17, color='#b8b8b8', alpha=0.9, lw=0)
axv.scatter(fc[dn], pv[dn], s=20, color='#3a3a6e', alpha=0.95, lw=0)
axv.scatter(fc[up], pv[up], s=20, color='#8e2440', alpha=0.95, lw=0)
axv.axvline(-0.5, color='0.25', ls='--', lw=1.0)
axv.axvline(0.35, color='0.25', ls='--', lw=1.0)
axv.axhline(1.3, color='0.25', ls='--', lw=1.0)
axv.set_xlim(-6.6, 8.6)
axv.set_ylim(0, 4.55)
axv.set_xticks([-4, 0, 4])
axv.set_yticks([0, 1, 2, 3, 4])
axv.tick_params(labelsize=7.5)
axv.set_xlabel('log$_2$(FC): Young vs. Aged', fontsize=9)
axv.set_ylabel('-log$_{10}$(p-value)', fontsize=9)
axv.set_title('Plasma proteins expression', fontsize=10, pad=6)

# ================= 通路条形面板 =================
PURPLE = mcolors.LinearSegmentedColormap.from_list(
    'pl', ['#cbc0dd', '#8a76a8', '#544270'])
CRIM = mcolors.LinearSegmentedColormap.from_list(
    'cr', ['#eeb6c0', '#c85b70', '#8e1f38'])

LEFT = [('Tuberculosis', 2.72, 'CAMP, LBP, MRC1'),
        ('Motor proteins', 2.55, 'MYL1, MYLPF, TUBB4B'),
        ('Toll-like receptor signaling pathway', 1.98, 'LBP, SPP1'),
        ('Cytoskeleton in muscle cells', 1.38, 'MYL1, MYLPF'),
        ('Salmonella infection', 1.08, 'MYLPF, TUBB4B')]
RIGHT = [('Complement and coagulation cascades', 6.25,
          'CFD, C2, C4b, C9, SERPIND1, TFPI, F12'),
         ('ECM-receptor interaction', 3.15,
          'COMP, LTGA2, LTGB1, THBS4, TNC'),
         ('Focal adhesion', 2.62,
          'COMP, LTGA2, LTGB1, THBS4, TNC, RAP1B'),
         ('PI3K-Akt signaling pathway', 2.45,
          'CDC37, COMP, HSP90AB1, LTGA2, LTGB1'),
         ('Platelet activation', 1.72, 'LTGA2, FERMT3, RAP1B')]


def bar_panel(ax, rows, cmap, vmin, vmax, xmax, xticks, title,
              cpos=(0.60, 0.115, 0.16, 0.085), cax=None):
    ax.set_title(title, fontsize=9, pad=5)
    nrow = len(rows)
    for i, (term, val, genes) in enumerate(rows):
        y = nrow - 1 - i
        c = cmap(0.25 + 0.75 * (val - vmin) / (vmax - vmin))
        ax.barh(y, val, height=0.62, facecolor=c, edgecolor='none')
        ax.text(0.08, y + 0.02, term, fontsize=7.6, va='center', color='black')
        ax.text(0.08, y - 0.62, genes, fontsize=7.2, va='center',
                color=cmap(0.55))
    ax.set_ylim(-0.9, nrow - 0.2)
    ax.set_xlim(0, xmax)
    ax.set_xticks(xticks)
    ax.tick_params(labelsize=7.5, length=2)
    ax.set_xlabel('-log$_{10}$(p-value)', fontsize=8)
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.set_yticks([])
    # mini 渐变色标 (cax 为 None 时内嵌于轴内 cpos; 否则用外部传入的 fig 级 axes)
    if cax is None:
        cax = ax.inset_axes(list(cpos))
    grad = np.linspace(0, 1, 128).reshape(1, -1)
    cax.imshow(grad, aspect='auto', cmap=cmap)
    cax.set_xticks([0, 128])
    cax.set_xticklabels([('%g' % vmin), ('%g' % vmax)], fontsize=6)
    cax.set_yticks([])
    cax.tick_params(length=1.5, pad=1)
    cax.set_title('-log$_{10}$(p-value)', fontsize=6.5, pad=2)


axl = fig.add_subplot(gs[1, 0])
bar_panel(axl, LEFT, PURPLE, 1.0, 3.0, 3.15, [0, 1, 2],
          'Age-reduced plasma proteins')
axrt = fig.add_subplot(gs[1, 1])
# 右面板基因列表文字几乎占满轴宽, 轴内无空白 → 色条移到面板外右上
# (两行之间的空带: 高于本面板标题带 y<0.435, 低于火山图轴/刻度 y>0.55),
# 主轴线不再穿色条, 色条刻度 1.5/6.5 与主轴 '6' 刻度彻底脱开
cax_r = fig.add_axes([0.80, 0.472, 0.13, 0.052])
bar_panel(axrt, RIGHT, CRIM, 1.5, 6.5, 7.0, [0, 2, 4, 6],
          'Age-accumulated plasma proteins', cax=cax_r)

save(fig, 'case_seg112.png')
