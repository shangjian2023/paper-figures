# -*- coding: utf-8 -*-
"""案例31 - Nature 表格排名热图: 行=方法(按 Rank 排序), 列=数据集与指标。
蓝/绿/橙/灰按列组着色, 格内排名数字, 彩色表头胶囊, 底部渐变箭头色条。
参考: frames/seg_031.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

methods = [
    ('scANVI*', 'emb', 'HVG', '-'), ('Scanorama', 'emb', 'HVG', '+'),
    ('scVI', 'emb', 'HVG', '-'), ('fastMNN', 'emb', 'HVG', '-'),
    ('scGen*', 'emb', 'HVG', '-'), ('Harmony', 'emb', 'HVG', '-'),
    ('fastMNN', 'emb', 'HVG', '-'), ('Seurat v3 RPCA', 'emb', 'HVG', '+'),
    ('BBKNN', 'graph', 'HVG', '-'), ('Scanorama', 'genes', 'HVG', '+'),
    ('ComBat', 'genes', 'HVG', '-'), ('MNN', 'genes', 'HVG', '+'),
    ('Seurat v3 CCA', 'genes', 'HVG', '-'), ('trVAE', 'emb', 'HVG', '-'),
    ('Conos', 'graph', 'HVG', '-'), ('DESC', 'emb', 'FULL', '-'),
    ('LIGER', 'emb', 'HVG', '-'), ('SAUCIE', 'emb', 'HVG', '+'),
    ('Unintegrated', 'genes', 'FULL', '-'), ('SAUCIE', 'genes', 'HVG', '+')]
nm = len(methods)

r = rng(31)
score = np.arange(nm)[:, None] + r.normal(0, 4.5, (nm, 10))
ranks = np.argsort(np.argsort(score, axis=0), axis=0) + 1      # 每列 1..20
ranks = ranks.astype(float)
mask = r.random((nm, 10)) < 0.10                               # 少量缺失格
mask[0] = False

col_w = [1.1, 3.6, 1.15, 1.3, 1.15] + [1.35] * 5 + [1.35] * 2 + [1.5] * 2 + [1.35] * 2
col_x = np.concatenate([[0], np.cumsum(col_w)])
W = col_x[-1]
def cx(k):
    return (col_x[k] + col_x[k + 1]) / 2.0

cmaps = {'rna': plt.get_cmap('Blues'), 'sim': plt.get_cmap('Greens'),
         'usa': plt.get_cmap('Oranges'), 'sca': plt.get_cmap('Greys')}

def draw_icon(ax, x, y, kind, s=0.30):
    """Output 列小图标: genes=方格, emb=散点, graph=连线图。"""
    if kind == 'genes':
        for a in range(3):
            for b in range(3):
                ax.add_patch(Rectangle((x - 1.45 * s + a * s,
                                        y - 1.45 * s + b * s),
                                       s * 0.82, s * 0.82, facecolor='#333333',
                                       edgecolor='none', zorder=4))
    elif kind == 'emb':
        rr = np.random.default_rng(7)
        p = rr.uniform(-1.3, 1.3, (7, 2)) * s
        ax.scatter(x + p[:, 0], y + p[:, 1], s=2.2, c='#333333', zorder=4)
    else:
        pts = np.array([[-1.2, -0.9], [-0.4, 0.9], [0.5, -0.5], [1.2, 0.8],
                        [0.1, 0.2]]) * s
        for a in range(len(pts)):
            for b in range(a + 1, len(pts)):
                ax.plot([pts[a, 0] + x, pts[b, 0] + x],
                        [pts[a, 1] + y, pts[b, 1] + y],
                        color='#333333', lw=0.45, zorder=4)
        ax.scatter(pts[:, 0] + x, pts[:, 1] + y, s=2.6, c='#333333', zorder=5)
col_group = ['rna'] * 5 + ['sim'] * 2 + ['usa'] * 2 + ['sca'] * 2
col_lab = ['Pancreas', 'Lung', 'Immune\n(human)', 'Immune\n(human/mouse)',
           'Mouse brain', 'Sim 1', 'Sim 2', 'Package', 'Paper', 'Time',
           'Memory']

fig = plt.figure(figsize=cm2in(20.0, 13.6))
gs = fig.add_gridspec(2, 1, height_ratios=[1.45, 0.15], hspace=0.50,
                      left=0.035, right=0.985, top=0.995, bottom=0.015)
ax = fig.add_subplot(gs[0])
ax.set_xlim(-0.4, W + 0.4)
ax.set_ylim(nm + 0.6, -2.1)
ax.axis('off')

# 隔行底纹 + 行内容
for i in range(nm):
    if i % 2 == 0:
        ax.add_patch(Rectangle((0, i), W, 1, facecolor='#ececec',
                               edgecolor='none', zorder=1))
    name, out, feat, scal = methods[i]
    ax.text(cx(0), i + 0.5, str(i + 1), ha='center', va='center',
            fontsize=7.5, zorder=4)
    ax.text(col_x[1] + 0.15, i + 0.5, name, ha='left', va='center',
            fontsize=7.2, zorder=4)
    draw_icon(ax, cx(2), i + 0.5, out)
    ax.text(cx(3), i + 0.5, feat, ha='center', va='center', fontsize=6.8,
            color='#2e8b57' if feat == 'HVG' else '#9a9a9a', zorder=4)
    ax.text(cx(4), i + 0.5, scal, ha='center', va='center', fontsize=7.5,
            zorder=4)

# 数据格
for j in range(10):
    x0 = col_x[5 + j]
    g = col_group[j]
    for i in range(nm):
        if mask[i, j]:
            continue
        rk = ranks[i, j]
        f = 0.10 + 0.82 * (rk - 1) / 19.0
        ax.add_patch(Rectangle((x0 + 0.08, i + 0.16), col_w[5 + j] - 0.16, 0.68,
                               facecolor=cmaps[g](f), edgecolor='#777777',
                               linewidth=0.45, zorder=3))
        if rk <= 3:
            ax.add_patch(Rectangle((x0 + col_w[5 + j] / 2 - 0.30, i + 0.26),
                                   0.60, 0.48, facecolor='white',
                                   edgecolor='#555555', linewidth=0.45,
                                   zorder=4))
            ax.text(x0 + col_w[5 + j] / 2, i + 0.51, str(int(rk)),
                    ha='center', va='center', fontsize=6.5, zorder=5)

# 表头胶囊
caps = [('Method', 0, 5, '#1a1a1a'), ('RNA', 5, 10, '#5da5cb'),
        ('Simulations', 10, 12, '#67bf5c'), ('Usability', 12, 14, '#f28e2b'),
        ('Scalability', 14, 16, '#9a9a9a')]
for lab, a, b, cc in caps:
    x0, x1 = col_x[a], col_x[b]
    ax.add_patch(FancyBboxPatch((x0 + 0.06, -1.65), (x1 - x0) - 0.12, 0.95,
                                boxstyle='round,pad=0.02,rounding_size=0.35',
                                facecolor=cc, edgecolor='none', zorder=3))
    ax.text((x0 + x1) / 2.0, -1.18, lab, ha='center', va='center',
            fontsize=7.5, color='white', zorder=4)

# 底部列名
for j, lab in enumerate(col_lab):
    ax.text(cx(5 + j), nm + 0.15, lab, rotation=45, ha='right', va='top',
            fontsize=6.8)
for k, lab in enumerate(['Rank', 'Name', 'Output', 'Features', 'Scaling']):
    ax.text(cx(k), nm + 0.15, lab, rotation=45, ha='right', va='top',
            fontsize=6.8)

# ---- 图例: 紧凑单行, 上移至紧贴列名下方, 消除底部大空白
axl = fig.add_subplot(gs[1])
axl.set_xlim(0, 1); axl.set_ylim(0, 1)
axl.axis('off')
yc = 0.52

def legend_icon(kind, x, y):
    if kind == 'genes':
        for a in range(3):
            for b in range(3):
                axl.add_patch(Rectangle((x - 0.0165 + a * 0.011, y - 0.0165 + b * 0.011),
                                        0.0085, 0.0085, facecolor='#333333',
                                        edgecolor='none'))
    elif kind == 'emb':
        rr = np.random.default_rng(11)
        p = rr.uniform(-0.016, 0.016, (7, 2))
        axl.scatter(x + p[:, 0], y + p[:, 1], s=2.0, c='#333333')
    else:
        pts = np.array([[-0.015, -0.012], [-0.005, 0.013], [0.007, -0.008],
                        [0.016, 0.011], [0.002, 0.003]])
        for a in range(len(pts)):
            for b in range(a + 1, len(pts)):
                axl.plot([pts[a, 0] + x, pts[b, 0] + x],
                         [pts[a, 1] + y, pts[b, 1] + y],
                         color='#333333', lw=0.45)
        axl.scatter(pts[:, 0] + x, pts[:, 1] + y, s=2.4, c='#333333')

axl.text(0.035, yc, 'Output', ha='left', va='center', fontsize=7.5)
legend_icon('genes', 0.115, yc)
axl.text(0.145, yc, 'Genes', ha='left', va='center', fontsize=7)
legend_icon('emb', 0.225, yc)
axl.text(0.255, yc, 'Embedding', ha='left', va='center', fontsize=7)
legend_icon('graph', 0.345, yc)
axl.text(0.375, yc, 'Graph', ha='left', va='center', fontsize=7)

axl.text(0.455, yc, 'Scaling', ha='left', va='center', fontsize=7.5)
axl.text(0.525, yc, '+', ha='center', va='center', fontsize=8)
axl.text(0.54, yc, 'Scaled', ha='left', va='center', fontsize=7)
axl.text(0.615, yc, '\u2212', ha='center', va='center', fontsize=8)
axl.text(0.63, yc, 'Unscaled', ha='left', va='center', fontsize=7)

axl.text(0.735, yc, 'Ranking', ha='left', va='center', fontsize=7.5)
for k, g in enumerate(['rna', 'sim', 'usa', 'sca']):
    x = 0.805 + k * 0.028
    grad = np.linspace(1, 0, 100)[None, :]
    axl.imshow(grad, extent=[x, x + 0.018, yc - 0.28, yc + 0.28], aspect='auto',
               cmap=cmaps[g])
    axl.add_patch(Rectangle((x, yc - 0.28), 0.018, 0.56, facecolor='none',
                            edgecolor='#555555', linewidth=0.5))
axl.annotate('', xy=(0.945, yc + 0.30), xytext=(0.945, yc - 0.30),
             arrowprops=dict(arrowstyle='->', lw=0.8, color='black'))
axl.text(0.955, yc + 0.22, '1', ha='left', va='center', fontsize=7)
axl.text(0.955, yc - 0.22, '20', ha='left', va='center', fontsize=7)

save(fig, 'case_seg031.png')
