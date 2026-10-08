# -*- coding: utf-8 -*-
"""案例121 - Cell 点阵相关矩阵热图: 60×60 点阵, 点色=Spearman(-1红~+1蓝),
点径=显著性, 对角深蓝, 顶部类别色块行 + 左侧分类色条列,
右侧/底部 PSA、KI-67 注释条, 左上 M0/M1 三角示意, 底部组合图例块。
参考: frames/seg_119.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Rectangle

set_style()

base = ['AR', 'ARV7', 'BROMO10', 'CCP', 'CD4_Act', 'CD8_Act', 'CHD1_loss',
        'Cholesterol', 'CTLA4', 'Decipher', 'EMT', 'ER_E', 'ER_L', 'EST_Purity',
        'EST_Sroma', 'FAM', 'Glycolysis', 'GR', 'HRdef', 'HRR', 'Hypoxia',
        'IFN', 'Imm190', 'Inflammation', 'KRAS', 'MDSC', 'Mtorc1', 'NE_Ala',
        'NE_Bat', 'NE_Bel', 'NE_Kun', 'NE_Tsai', 'PDL2', 'Persist', 'PerjM',
        'PI3K', 'PORTOS', 'PROSGen', 'PTEN_Liu', 'PTEN_Snr', 'RT_sens',
        'SPOP_mut', 'TLS', 'TP53_loss', 'TP53_Donh', 'Treg']
suffix = ['_HM', '_IPS', '_Liu', '_Carter', '_Ricketts', '_Weiner', '_Kuner',
          '_SnaR', '_Esch', '_Calib']
r0 = rng(119)
names = []
for k, b in enumerate(base):
    names.append(b + suffix[k % 10])
while len(names) < 60:
    g = ['BAX', 'BCL2', 'CDK4', 'EGFR', 'FOS', 'JUN', 'KRAS', 'MYC', 'PTEN',
         'STAT3', 'VEGFA', 'TP53', 'SRC', 'AKT1'][len(names) % 14]
    names.append(g + '_pathway')
names = names[:60]

# 10 个类别, 按类别分块
cat_sizes = [5, 6, 5, 7, 6, 7, 5, 6, 7, 6]
cat_names = ['AR-ISR signaling', 'Cellular plasticity', 'Chromatin remodeling',
             'DNA repair', 'Genome instability', 'Immune activity',
             'Microenvironment', 'Metabolic', 'Oncogenic pathways',
             'Radiosensitivity']
cat_colors = pal('set3', 10)
cat_of = np.concatenate([[k] * s for k, s in enumerate(cat_sizes)])
n = len(cat_of)
starts = np.where(np.diff(np.concatenate([[-1], cat_of])) != 0)[0]

# 分块相关矩阵: 同类强相关, 异类近零
R = r0.normal(0, 0.18, (n, n))
block_sign = r0.choice([-1, 1], 10, p=[0.3, 0.7])
for k in range(10):
    idx = cat_of == k
    blk = r0.normal(0.42 * block_sign[k], 0.22, (idx.sum(), idx.sum()))
    R[np.ix_(idx, idx)] = blk
R = (R + R.T) / 2.0
R = R.clip(-0.95, 0.95)
np.fill_diagonal(R, 1.0)

# p 值随 |r| 减小
P = np.exp(-np.abs(R) * 6.2 + r0.normal(0, 0.9, (n, n)))
P = P.clip(1e-9, 1.0)
np.fill_diagonal(P, 1e-12)

cmap = plt.get_cmap('RdBu')          # -1=红, +1=蓝 (同参考)
cmap_cat = ListedColormap(cat_colors)
norm_cat = BoundaryNorm(np.arange(-0.5, 10.5, 1), 10)

# PSA / KI-67 注释值(与主矩阵相互独立的弱相关)
psa_v = r0.normal(0, 0.32, n).clip(-0.85, 0.85)
k67_v = r0.normal(0, 0.32, n).clip(-0.85, 0.85)
psa_sig = np.clip(-np.log10(r0.uniform(1e-4, 1, n)) / 3.0, 0.05, 1)
k67_sig = np.clip(-np.log10(r0.uniform(1e-4, 1, n)) / 3.0, 0.05, 1)

fig = plt.figure(figsize=cm2in(20.0, 18.0))
# 轴与色条间留出完整标签通道: 上方 0.08 / 左侧 0.095 图幅, 容纳最长签名名
ax = fig.add_axes([0.345, 0.24, 0.50, 0.575])
ax.set_xlim(-0.5, n - 0.5)
ax.set_ylim(n - 0.5, -0.5)
ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(names, rotation=90, fontsize=3.6)
ax.set_yticklabels(names, fontsize=4.0)
ax.tick_params(length=1.2, pad=1.2)
ax.xaxis.tick_top()
for s in ax.spines.values():
    s.set_color('0.4')
# 类别分界浅线
for st in starts[1:]:
    ax.axhline(st - 0.5, color='0.75', lw=0.5, zorder=1)
    ax.axvline(st - 0.5, color='0.75', lw=0.5, zorder=1)

# ~3600 点一次 scatter: 色=r, 径=显著性
ii, jj = np.meshgrid(np.arange(n), np.arange(n), indexing='ij')
sig = np.clip(-np.log10(P) / 3.0, 0, 1)
ss = 1.5 + sig * 30
ax.scatter(jj.ravel(), ii.ravel(), c=R.ravel(), s=ss.ravel(), cmap=cmap,
           vmin=-1, vmax=1, edgecolors='none', zorder=3)

# 顶部类别色块行 / 左侧分类色条列 (与热图对齐, 远离标签通道)
tax = fig.add_axes([0.345, 0.895, 0.50, 0.012])
tax.imshow(cat_of[None, :], aspect='auto', cmap=cmap_cat, norm=norm_cat,
           interpolation='nearest')
tax.set_xticks([]); tax.set_yticks([])
for s in tax.spines.values():
    s.set_linewidth(0.6)
lax = fig.add_axes([0.25, 0.24, 0.014, 0.575])
lax.imshow(cat_of[:, None], aspect='auto', cmap=cmap_cat, norm=norm_cat,
           interpolation='nearest')
lax.set_xticks([]); lax.set_yticks([])
for s in lax.spines.values():
    s.set_linewidth(0.6)

# ------------------------------------------------ 右侧 PSA / KI-67 窄列小热图
def anno_col(rect, vals, sg, label):
    ac = fig.add_axes(rect)
    ac.set_xlim(0, 1); ac.set_ylim(0, n)
    for i in range(n):
        ac.add_patch(Rectangle((0, i), 1, 1, fill=False, ec='0.78', lw=0.3))
    ac.scatter([0.5] * n, [i + 0.5 for i in range(n)],
               c=vals, s=1.5 + sg * 9, cmap=cmap, vmin=-1, vmax=1,
               edgecolors='none', zorder=3)
    ac.axis('off')
    fig.text(rect[0] + rect[2] + 0.006, rect[1] + rect[3] + 0.012, label,
             rotation=90, ha='left', va='bottom', fontsize=4.5, color='0.15')

def anno_row(rect, vals, sg, label):
    ar = fig.add_axes(rect)
    ar.set_xlim(0, n); ar.set_ylim(0, 1)
    for i in range(n):
        ar.add_patch(Rectangle((i, 0), 1, 1, fill=False, ec='0.78', lw=0.3))
    ar.scatter([i + 0.5 for i in range(n)], [0.5] * n,
               c=vals, s=1.5 + sg * 9, cmap=cmap, vmin=-1, vmax=1,
               edgecolors='none', zorder=3)
    ar.axis('off')
    fig.text(rect[0] - 0.008, rect[1] + rect[3] / 2, label,
             ha='right', va='center', fontsize=4.5, color='0.15')

anno_col([0.858, 0.24, 0.012, 0.575], psa_v, psa_sig, 'PSA')
anno_col([0.886, 0.24, 0.012, 0.575], k67_v, k67_sig, 'KI-67')
anno_row([0.345, 0.200, 0.50, 0.011], psa_v, psa_sig, 'PSA')
anno_row([0.345, 0.179, 0.50, 0.011], k67_v, k67_sig, 'KI-67')

# 注释列 mini 色条
for cx in (0.912, 0.942):
    mc = fig.add_axes([cx, 0.42, 0.007, 0.26])
    mc.imshow(np.linspace(1, -1, 128).reshape(-1, 1), aspect='auto',
              cmap=cmap, vmin=-1, vmax=1)
    mc.set_xticks([]); mc.set_yticks([])
    for s in mc.spines.values():
        s.set_linewidth(0.4); s.set_color('0.5')

# ------------------------------------------------ 左上 M0/M1 三角示意图例
tri = fig.add_axes([0.055, 0.852, 0.165, 0.118])
tri.set_xlim(0, 1.46); tri.set_ylim(0, 1.0)
tri.axis('off')
x0, y0, w_sq, h_sq = 0.44, 0.05, 0.59, 0.86      # 纸面正方
tri.add_patch(Rectangle((x0, y0), w_sq, h_sq, fill=False, ec='0.2', lw=0.7))
tri.plot([x0, x0 + w_sq], [y0 + h_sq, y0], color='0.2', lw=0.7)
tri.text(x0 + w_sq * 0.72, y0 + h_sq * 0.62,
         'M1 inter\nsignature\ncorrelation', ha='center', va='center',
         fontsize=4.2, color='0.15', linespacing=1.25)
tri.text(x0 + w_sq * 0.27, y0 + h_sq * 0.30,
         'M0 inter\nsignature\ncorrelation', ha='center', va='center',
         fontsize=4.2, color='0.15', linespacing=1.25)
tri.text(x0 + w_sq / 2, y0 + h_sq + 0.05, 'M1', ha='center', va='bottom',
         fontsize=5)
tri.text(x0 + w_sq / 2, y0 - 0.05, 'M0', ha='center', va='top', fontsize=5)
tri.text(x0 - 0.05, y0 + h_sq / 2, 'M0', ha='right', va='center', fontsize=5)
tri.text(x0 + w_sq + 0.05, y0 + h_sq / 2, 'M1', ha='left', va='center',
         fontsize=5)

# ------------------------------------------------ 底部组合图例块 (虚线外框 + 4 分格)
fig.add_artist(Rectangle((0.045, 0.028), 0.93, 0.132, fill=False,
                         ls=(0, (4, 2)), ec='0.55', lw=0.7,
                         transform=fig.transFigure))

# 分格 I: Biological category (10 类, 与顶/左色条一致, 4 列排布)
bx1 = fig.add_axes([0.055, 0.033, 0.46, 0.122]); bx1.axis('off')
for s in bx1.spines.values():
    s.set_linewidth(0.6); s.set_color('0.35')
fig.text(0.285, 0.1435, 'Biological category', ha='center', va='center',
         fontsize=5.2, color='0.1')
fig.add_artist(plt.Line2D([0.245, 0.325], [0.1375, 0.1375],
                          transform=fig.transFigure, color='0.1', lw=0.5))
SQ_W, SQ_H = 0.008, 0.0089                 # 图例色块(纸面近正方)
col_x = [0.062, 0.182, 0.302, 0.415]
rows_y = [0.106, 0.074, 0.043]
for k, (cname, ccol) in enumerate(zip(cat_names, cat_colors)):
    cx_ = col_x[k // 3] if k < 9 else col_x[3]
    cy_ = rows_y[k % 3]
    fig.add_artist(Rectangle((cx_, cy_ - SQ_H / 2), SQ_W, SQ_H,
                             facecolor=ccol, edgecolor='0.3', lw=0.3,
                             transform=fig.transFigure))
    fig.text(cx_ + 0.013, cy_, cname, ha='left', va='center', fontsize=4.6,
             color='0.15')

# 分格 II: Origin of signature
bx2 = fig.add_axes([0.535, 0.033, 0.24, 0.122]); bx2.axis('off')
for s in bx2.spines.values():
    s.set_linewidth(0.6); s.set_color('0.35')
fig.text(0.655, 0.1435, 'Origin of signature', ha='center', va='center',
         fontsize=5.2, color='0.1')
fig.add_artist(plt.Line2D([0.612, 0.698], [0.1375, 0.1375],
                          transform=fig.transFigure, color='0.1', lw=0.5))
origin = [('Prostate cancer', '#8c8c8c'), ('Pan cancer', '#c49c6b'),
          ('Melanoma', '#5c5c40'), ('CRPC', '#8c5a3c'),
          ('Bladder', '#6b6b40'), ('Breast', '#8c3c3c'),
          ('cell line (LNCaP)', '#1a1a1a'), ('Gastric', '#9c8c3c'),
          ('Renal', '#9c5a4c')]
ocol_x = [0.545, 0.632, 0.719]
for k, (oname, ocol) in enumerate(origin):
    ox_ = ocol_x[k % 3]; oy_ = rows_y[k // 3]
    fig.add_artist(Rectangle((ox_, oy_ - SQ_H / 2), SQ_W, SQ_H,
                             facecolor=ocol, edgecolor='0.3', lw=0.3,
                             transform=fig.transFigure))
    fig.text(ox_ + 0.012, oy_, oname, ha='left', va='center', fontsize=4.4,
             color='0.15')

# 分格 III: Cell cycle explicated
bx3 = fig.add_axes([0.79, 0.033, 0.085, 0.122]); bx3.axis('off')
for s in bx3.spines.values():
    s.set_linewidth(0.6); s.set_color('0.35')
fig.text(0.8325, 0.1435, 'Cell cycle', ha='center', va='center',
         fontsize=5.2, color='0.1')
fig.text(0.8325, 0.131, 'explicated', ha='center', va='center',
         fontsize=5.2, color='0.1')
fig.add_artist(plt.Line2D([0.806, 0.859], [0.1245, 0.1245],
                          transform=fig.transFigure, color='0.1', lw=0.5))
for yy_, lab, cc in [(0.095, 'No', '#2e8b57'), (0.06, 'Yes', '#e83e8c')]:
    fig.add_artist(Rectangle((0.803, yy_ - SQ_H / 2), SQ_W, SQ_H,
                             facecolor=cc, edgecolor='0.3', lw=0.3,
                             transform=fig.transFigure))
    fig.text(0.816, yy_, lab, ha='left', va='center', fontsize=4.6,
             color='0.15')

# 分格 IV: Spearman Correlation 渐变条
bx4 = fig.add_axes([0.888, 0.033, 0.082, 0.122]); bx4.axis('off')
for s in bx4.spines.values():
    s.set_linewidth(0.6); s.set_color('0.35')
fig.text(0.929, 0.1435, 'Spearman Correlation', ha='center', va='center',
         fontsize=5.2, color='0.1')
fig.add_artist(plt.Line2D([0.885, 0.973], [0.1375, 0.1375],
                          transform=fig.transFigure, color='0.1', lw=0.5))
gx = fig.add_axes([0.898, 0.075, 0.062, 0.045])
gx.imshow(np.linspace(-1, 1, 256).reshape(1, -1), aspect='auto', cmap=cmap,
          vmin=-1, vmax=1)
gx.set_xticks([]); gx.set_yticks([])
for s in gx.spines.values():
    s.set_linewidth(0.4); s.set_color('0.4')
for tv, tl in [(-1, '-1'), (-0.6, '-0.6'), (-0.2, '-0.2'),
               (0.2, '0.2'), (0.6, '0.6'), (1, '1')]:
    fig.text(0.898 + (tv + 1) / 2 * 0.062, 0.068, tl, ha='center',
             va='top', fontsize=4.2, color='0.2')

save(fig, 'case_seg119.png')
