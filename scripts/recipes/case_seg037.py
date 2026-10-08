# -*- coding: utf-8 -*-
"""案例37 - Science FC-FC散点: 数万黑点背景 + 红/蓝高亮(点径∝显著性) + 米色空心
中等显著 + ~40基因引线斜体标注。参考: frames/seg_037.jpg — ERKi vs KRAS siRNA。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D

set_style()

r = rng(37)
fig, ax = plt.subplots(figsize=cm2in(14.5, 13.0))
stroke = [pe.withStroke(linewidth=2.2, foreground='white')]

# ---------------- 背景黑点 (~20000) ----------------
core = r.multivariate_normal([0.0, -0.35], [[0.55, 0.22], [0.22, 0.95]], 15000)
spread = r.multivariate_normal([0.0, -0.20], [[2.4, 1.1], [1.1, 2.8]], 7000)
bg = np.vstack([core, spread])
ax.scatter(bg[:, 0], bg[:, 1], s=2.5, color='#1A1A1A', alpha=0.22,
           linewidths=0, zorder=1)

# ---------------- 高亮点(大小∝显著性) ----------------
def sig_scatter(n, mu, cov, color, s0=8, s1=130, ec='none', fc_alpha=0.9):
    pts = r.multivariate_normal(mu, cov, n)
    p = r.uniform(0, 1, n) ** 2.2                       # 多数点较小
    sizes = s0 + (s1 - s0) * p
    ax.scatter(pts[:, 0], pts[:, 1], s=sizes, color=color, alpha=fc_alpha,
               edgecolors=ec if ec != 'none' else color, linewidths=0.6,
               zorder=4)
    return pts

red = sig_scatter(150, [0.75, 2.35], [[0.28, 0.06], [0.06, 0.75]], '#C41E3A')
blue = sig_scatter(130, [-1.45, -2.10], [[0.42, 0.12], [0.12, 0.85]], '#2E3FD0')
tan = sig_scatter(90, [0.60, 1.10], [[1.30, 0.45], [0.45, 1.60]], '#D9C6A0',
                  s0=10, s1=90, fc_alpha=0.55)
tan2 = sig_scatter(30, [-1.60, 0.90], [[0.8, 0.3], [0.3, 1.0]], '#D9C6A0',
                   s0=10, s1=70, fc_alpha=0.55)

# ---------------- 基因引线标注 ----------------
# (基因, 点坐标, 文本坐标, 文字颜色)
genes = [
    ('KRAS',      (-2.90, 0.30),  (-3.05, 0.75), 'k'),
    ('HEPACAM2',  (-2.45, 3.60),  (-2.85, 4.05), 'k'),
    ('TRIM22',    (-0.40, 3.70),  (-1.30, 4.00), 'k'),
    ('VTCN1',     (0.20, 4.55),   (0.05, 5.05), 'k'),
    ('ACE2',      (0.55, 4.30),   (0.70, 4.65), 'k'),
    ('LDLRAD1',   (1.10, 4.40),   (1.30, 4.95), 'k'),
    ('EDN2',      (2.30, 4.35),   (2.35, 4.75), 'k'),
    ('SH2D3C',    (2.20, 3.55),   (2.55, 3.95), 'k'),
    ('SLC52A1',   (1.55, 3.60),   (1.55, 3.95), 'k'),
    ('ATP6V1B1',  (1.90, 3.15),   (2.45, 3.35), 'k'),
    ('BMF',       (-0.35, 3.30),  (-0.95, 3.30), 'k'),
    ('UBD',       (0.10, 3.45),   (-0.42, 3.80), 'k'),
    ('CYP26A1',   (0.55, 3.05),   (0.02, 3.22), 'k'),
    ('GPR37L1',   (0.35, 2.55),   (-0.28, 2.30), 'k'),
    ('FRR15L',    (1.20, 2.35),   (1.62, 2.55), 'k'),
    ('ALDH3B2',   (0.90, 1.85),   (0.55, 1.55), 'k'),
    ('EXOC3L',    (1.95, 1.55),   (2.40, 1.75), 'k'),
    ('TP53INP1',  (1.65, 1.10),   (2.20, 0.95), 'k'),
    ('CLIC3',     (2.55, 2.90),   (2.80, 3.15), 'k'),
    ('CHPF',      (2.45, -0.05),  (2.55, 0.25), 'k'),
    ('EMP2',      (1.85, -0.65),  (2.10, -0.70), 'k'),
    ('LSMEM2',    (-2.55, -1.55), (-3.10, -1.35), 'k'),
    ('HMGA2',     (-2.05, -1.95), (-2.45, -2.10), 'k'),
    ('ETV1',      (-2.85, -2.85), (-3.15, -2.95), 'k'),
    ('NAV2',      (-1.45, -2.30), (-1.60, -2.10), 'k'),
    ('CORO2B',    (-0.45, -2.20), (-0.10, -1.95), 'k'),
    ('NT5E',      (-2.60, -3.40), (-3.00, -3.55), 'k'),
    ('FOSL1',     (-1.35, -3.35), (-1.80, -3.60), 'k'),
    ('SPRY4',     (-0.45, -3.30), (-0.10, -3.40), 'k'),
    ('PTX3',      (-1.95, -3.90), (-2.62, -3.82), 'k'),
    ('TNS4',      (-1.55, -4.05), (-2.30, -4.20), 'k'),
    ('MMP1',      (-0.55, -4.05), (-0.28, -4.38), 'k'),
    ('IL1RL1',    (-0.15, -4.15), (0.30, -4.15), 'k'),
    ('ETV4',      (-1.75, -4.45), (-2.20, -4.75), 'k'),
    ('ETV5',      (-1.30, -4.55), (-1.05, -4.85), 'k'),
    ('GPR3',      (-0.85, -4.85), (-0.55, -5.10), 'k'),
    ('EGR2',      (-0.35, -4.60), (-0.10, -4.75), 'k'),
    ('DUSP6',     (-1.85, -5.40), (-2.30, -5.65), 'k'),
    ('EGR1',      (-0.75, -5.90), (-0.30, -5.95), 'k'),
]
for g, (px, py), (tx, ty), col in genes:
    hi = '#C41E3A' if py > 0.8 and px > -0.6 else ('#2E3FD0' if py < -1.0 else '#D9C6A0')
    if px < -1.8 and py < 0:
        hi = '#2E3FD0'
    ax.scatter([px], [py], s=60, color=hi, alpha=0.95, edgecolors='white',
               linewidths=0.4, zorder=5)
    ax.annotate(r'$\it{%s}$' % g, xy=(px, py), xytext=(tx, ty), fontsize=8.2,
                color=col, ha='center', va='center', zorder=6,
                path_effects=stroke,
                arrowprops=dict(arrowstyle='-', lw=0.7, color='#333333',
                                shrinkA=2, shrinkB=1))

# ---------------- 轴 ----------------
ax.axhline(0, color='#8C8C8C', lw=1.1, zorder=1.5)
ax.axvline(0, color='#8C8C8C', lw=1.1, zorder=1.5)
ax.set_xlim(-3.45, 3.45)
ax.set_ylim(-6.6, 5.3)
ax.set_xticks([-2, 0, 2])
ax.set_yticks([-6, -3, 0, 3])
ax.set_xlabel(r'$\it{KRAS}$ vs NS siRNA (log$_2$FC)', fontsize=10)
ax.set_ylabel('ERKi 24 h vs Control (log$_2$FC)', fontsize=10)

# ---------------- 图例: 高亮三类(红/蓝/米), 放右下空白区 ----------------
leg_handles = [
    Line2D([], [], marker='o', ls='none', mfc='#C41E3A', mec='#C41E3A',
           ms=5.5, alpha=0.9, label='Both up'),
    Line2D([], [], marker='o', ls='none', mfc='#2E3FD0', mec='#2E3FD0',
           ms=5.5, alpha=0.9, label='Both down'),
    Line2D([], [], marker='o', ls='none', mfc='#D9C6A0', mec='#D9C6A0',
           ms=5.5, alpha=0.75, label='Discordant'),
]
ax.legend(handles=leg_handles, loc='lower right', bbox_to_anchor=(0.99, 0.02),
          frameon=False, fontsize=8.5, handletextpad=0.4, borderaxespad=0,
          labelspacing=0.45, title='Dot diameter $\\propto$ significance',
          title_fontsize=7.5, alignment='left')

save(fig, 'case_seg037.png')
