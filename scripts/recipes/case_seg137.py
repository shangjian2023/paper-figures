# -*- coding: utf-8 -*-
"""案例142 - 泳道图(swimmer plot): 患者行×术后天数的事件时间线。
参考: frames/seg_137.jpg — a 主泳道(左3列注释色条+菱形手术起点+治疗色段+
时间点圆点+复发/进展+死亡) + 顶部5组图例; b 堆叠圆点柱+饼图; c 配对箱线。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle, Circle, Polygon

set_style()
r = rng(137)

# ---------------------------------------------------------------- 调色
tx_cols = {'Radiotherapy': '#EDC948', 'Immunotherapy': '#3B7DD8',
           'Chemotherapy': '#D94A4E', 'Targeted therapy': '#59A14F',
           'Nintedanib': '#B07AA1'}
hist_cols = {'LUAD': '#9B1B30', 'LUSC': '#2C5F8A', 'Other': '#8D8D8D'}
stage_cols = {'1a': '#F2F2F2', '1b': '#CFCFCF', '2a': '#AECFE8',
              '2b': '#6FA8DC', '3a': '#3B7DD8', '3b': '#1F4E9C'}
smoke_cols = {'Never': '#3B7DD8', 'Ex': '#ABABAB', 'Current': '#333333'}

ids = ['CRUKP8172', 'CRUKP3207', 'CRUKP0712', 'CRUKP1584', 'CRUKP9145',
       'CRUKP2757', 'CRUKP4715', 'CRUKP6590', 'CRUKP9506', 'CRUKP7216',
       'CRUKP4761', 'CRUKP3371', 'CRUKP8433', 'CRUKP7127', 'CRUKP8780',
       'CRUKP3581', 'CRUKP3358', 'CRUKP0294']
n = len(ids)

hist = r.choice(list(hist_cols), n, p=[0.72, 0.20, 0.08])
stage = r.choice(list(stage_cols), n, p=[0.1, 0.2, 0.2, 0.25, 0.2, 0.05])
smoke = r.choice(list(smoke_cols), n, p=[0.5, 0.3, 0.2])

# ---------------------------------------------------------------- 版面
fig = plt.figure(figsize=cm2in(24, 19))
gs = fig.add_gridspec(3, 3, height_ratios=[0.40, 2.25, 1],
                      width_ratios=[1, 1.0, 0.78], wspace=0.30, hspace=0.42,
                      left=0.05, right=0.99, top=0.975, bottom=0.085)
axl = fig.add_subplot(gs[0, :])          # 顶部图例带
ax = fig.add_subplot(gs[1, :2])          # a: 泳道
axh = fig.add_subplot(gs[1, 2])          # a 右: 人体器官分布内嵌
axb = fig.add_subplot(gs[2, 0])          # b: 堆叠点柱
axc1 = fig.add_subplot(gs[2, 1])         # c 左: Mutation 配对箱线
axc2 = fig.add_subplot(gs[2, 2])         # c 右: SCNA 配对箱线

# ---------------------------------------------------------------- 图例带
axl.set_xlim(0, 100)
axl.set_ylim(0, 10.5)
axl.axis('off')


def leg_group(x0, title, entries):
    axl.text(x0, 9.6, title, fontsize=6, va='center')
    for k, ent in enumerate(entries):
        yk = 8.2 - k * 1.15
        if ent[0] == 'm':                       # ('m', _, marker, mfc, mec)
            axl.plot(x0 + 1.0, yk, ent[2], ms=3.6, mfc=ent[3], mec=ent[4],
                     ls='none', mew=0.5)
        else:                                   # 色块 ('p', color, label)
            axl.add_patch(Rectangle((x0 + 0.25, yk - 0.5), 1.7, 1.0,
                                    fc=ent[1], ec='0.35', lw=0.3))
        axl.text(x0 + 2.3, yk, ent[-1], fontsize=5.2, va='center')


leg_group(25, 'Time point', [
    ('m', 0, 'D', '#4A4A4A', 'black', 'Surgery'),
    ('m', 0, 'D', 'white', 'black', 'Surgery LN'),
    ('m', 0, '^', '#E8A0A0', '#7A3535', 'Relapse sample'),
    ('m', 0, 's', '#C9506E', '#5E1F30', 'Progression sample'),
    ('m', 0, 's', 'white', '#5E1F30', 'Autopsy sample'),
    ('m', 0, 'X', 'white', 'black', 'Relapse'),
    ('m', 0, '|', 'black', 'black', 'Death')])
leg_group(47, 'Treatment',
          [('p', c, k) for k, c in tx_cols.items()] +
          [('m', 0, 'o', '#9A9A9A', '0.3', 'Adjuvant chemotherapy cycle'),
           ('m', 0, 'D', '#7A1F28', 'black',
            'Metastatectomy or ablation')])
leg_group(66, 'Smoking status', [('p', c, k) for k, c in smoke_cols.items()])
leg_group(78, 'Histology', [('p', c, k) for k, c in hist_cols.items()])
leg_group(88, 'Stage', [('p', c, k) for k, c in stage_cols.items()])
panel_label(axl, 'a', dx=0.0, dy=0.88)

# ---------------------------------------------------------------- a: 泳道
xs_ann = [(-140, 40), (-88, 40), (-38, 36)]       # 三列注释色条 (中心,宽)
ann_keys = list(zip(hist, stage, smoke))
for i in range(n):
    y = n - 1 - i
    end = float(r.integers(400, 2950))
    ax.plot([0, end], [y, y], ls=':', color='0.55', lw=0.9, zorder=1)
    for (xc, wc), key, cmap in zip(xs_ann, ann_keys[i],
                                   (hist_cols, stage_cols, smoke_cols)):
        ax.add_patch(Rectangle((xc - wc / 2, y - 0.36), wc, 0.72,
                               fc=cmap[key], ec='0.35', lw=0.3, zorder=2))
    ax.scatter(0, y, marker='D', s=26, fc='#4A4A4A', ec='black',
               lw=0.5, zorder=5)                       # 手术起点
    for j in range(r.integers(3, 6)):                  # 辅助化疗周期
        ax.scatter(55 + 55 * j + r.uniform(-8, 8), y, s=8, fc='#9A9A9A',
                   ec='0.3', lw=0.3, zorder=4)
    nseg = int(r.integers(1, 4))                       # 治疗色段
    pos = np.sort(r.uniform(120, max(end - 300, 400), nseg * 2))
    for s0, s1, tk in zip(pos[0::2], pos[1::2],
                          r.choice(list(tx_cols), nseg)):
        ax.plot([s0, s1], [y, y], lw=6, solid_capstyle='butt',
                color=tx_cols[tk], zorder=3)
    m = int(r.integers(4, 11))                         # 末端时间点圆点
    tpx = np.sort(end - r.uniform(0, 420, m))
    tpc = [tx_cols[t] for t in r.choice(list(tx_cols), m)]
    ax.scatter(tpx, np.full(m, y), s=24, c=tpc, zorder=6)
    if r.random() < 0.6:                               # 复发样本(三角)
        ax.scatter(r.uniform(end * 0.2, end * 0.7), y, marker='^', s=34,
                   fc='#E8A0A0', ec='#7A3535', lw=0.4, zorder=5)
    if r.random() < 0.5:                               # 进展样本(方块)
        ax.scatter(r.uniform(end * 0.3, end * 0.85), y, marker='s', s=26,
                   fc='#C9506E', ec='#5E1F30', lw=0.4, zorder=5)
    if r.random() < 0.45:                              # 影像复发 X
        ax.scatter(r.uniform(200, end * 0.9), y, marker='X', s=26,
                   fc='white', ec='black', lw=0.6, zorder=6)
    if r.random() < 0.3:                               # 死亡 |
        ax.plot([end, end], [y - 0.34, y + 0.34], color='black', lw=1.4,
                zorder=6)

ax.set_xlim(-165, 3020)
ax.set_ylim(-2.6, n - 0.4)
ax.set_yticks(np.arange(n)[::-1])
ax.set_yticklabels(ids, fontsize=5.2)
ax.tick_params(axis='y', length=0)
ax.set_xticks(np.arange(0, 3001, 500))
ax.tick_params(labelsize=6.5)
despine(ax, left=True, bottom=False)
ax.spines['left'].set_bounds(-0.5, n - 0.5)
for (xc, _), lab in zip(xs_ann, ['Histology', 'Stage', 'Smoking']):
    ax.text(xc, -1.6, lab, rotation=50, ha='center', va='top', fontsize=5.5)
ax.set_xlabel('Time after primary surgery (days)', fontsize=7.5)

# ---------------------------------------------------------------- a 右: 人体内嵌
axh.set_xlim(0, 10.8)
axh.set_ylim(0.0, 10.9)
axh.set_aspect('equal')
axh.axis('off')
BF, BE = '#F3F3F3', '#B8B8B8'            # 人体填充/描边
axh.text(5.3, 10.55, 'Metastatic sites', ha='center', va='top', fontsize=5.5)
# 头
axh.add_patch(Circle((5.3, 9.5), 0.72, fc=BF, ec=BE, lw=0.7))
# 颈+躯干
torso = [(4.75, 8.85), (5.85, 8.85), (5.9, 8.35), (7.15, 7.7), (7.35, 4.75),
         (6.45, 4.05), (4.15, 4.05), (3.25, 4.75), (3.45, 7.7), (4.7, 8.35)]
axh.add_patch(Polygon(torso, closed=True, fc=BF, ec=BE, lw=0.7,
                      joinstyle='round'))
# 四肢: 描边管(深灰粗线+浅灰细线)
for (x0, y0, x1, y1) in [(3.5, 7.55, 2.55, 3.9), (7.1, 7.55, 8.05, 3.9),
                         (4.6, 4.1, 4.45, 0.85), (6.0, 4.1, 6.15, 0.85)]:
    axh.plot([x0, x1], [y0, y1], lw=5.4, color='#A8A8A8',
             solid_capstyle='round')
    axh.plot([x0, x1], [y0, y1], lw=3.9, color=BF, solid_capstyle='round')

# 器官气泡: 色=器官, 大小=转移病灶数(1-5)
organs = [('Brain', 5.3, 9.5, 2, '#7B5EA7'),
          ('Lung primary', 3.95, 7.1, 5, '#2C5F8A'),
          ('Lymph node', 5.8, 6.85, 5, '#3B7DD8'),
          ('Bone', 7.85, 6.9, 2, '#C8A165'),
          ('Liver', 4.15, 5.9, 4, '#8C1D28'),
          ('Kidney', 6.35, 5.7, 2, '#B02A30'),
          ('Gastric', 5.25, 5.5, 2, '#C0392B'),
          ('Adrenal', 4.55, 6.4, 1, '#E29BB5'),
          ('Bowel', 5.3, 4.65, 3, '#E8A0A0'),
          ('Bladder', 5.3, 3.7, 1, '#8D8D8D')]
for name, ox, oy, cnt, oc in organs:
    rr = 0.24 + 0.155 * cnt
    axh.add_patch(Circle((ox, oy), rr, fc=oc, ec='white', lw=0.6,
                         alpha=0.92, zorder=3))
    if cnt >= 2:
        axh.text(ox, oy, str(cnt), ha='center', va='center',
                 fontsize=4.2 + 0.5 * cnt, color='white',
                 fontweight='bold', zorder=4)
# 小图例(右侧竖排)
for k, (name, _, _, _, oc) in enumerate(organs):
    yk = 9.4 - k * 0.78
    axh.plot(8.85, yk, 'o', ms=2.6, mfc=oc, mec='0.3', mew=0.3)
    axh.text(9.15, yk, name, fontsize=4.0, va='center')
axh.text(8.65, 2.0, 'Bubble size\n= no. lesions\n(1–5)', fontsize=3.8,
         ha='left', va='top', color='0.35')

# ---------------------------------------------------------------- b: 堆叠点柱
counts = np.sort(r.integers(3, 30, 14))
pid_b = ['CRUKP%04d' % v for v in r.choice(
    [1761, 8759, 9712, 5037, 5650, 6114, 1908, 7271, 4236, 7156,
     6908, 3584, 2175, 5580], 14, replace=False)]
for j, c in enumerate(counts):
    n_dark = int(c * r.uniform(0.35, 0.7))     # imaged and sampled
    n_pink = int((c - n_dark) * 0.6)           # sampled only
    for k in range(c):
        if k < n_dark:
            fc, ec = '#B02A30', '#B02A30'
        elif k < n_dark + n_pink:
            fc, ec = '#EFC1C6', '#EFC1C6'
        else:
            fc, ec = 'white', '#666666'
        axb.scatter(j, k + 0.5, s=17, facecolor=fc, edgecolor=ec, lw=0.5)
axb.set_xlim(-1, len(counts))
axb.set_ylim(0, counts.max() + 3)
axb.set_xticks(range(len(counts)))
axb.set_xticklabels(pid_b, rotation=90, fontsize=4.8)
axb.tick_params(axis='y', labelsize=6.5)
axb.set_ylabel('Metastases', fontsize=7.5)
despine(axb)
pie = axb.inset_axes([0.05, 0.52, 0.28, 0.42])
pie.pie([112, 67, 48], colors=['#B02A30', '#EFC1C6', 'white'],
        wedgeprops={'edgecolor': 'black', 'linewidth': 0.6}, startangle=100)
pie.set_aspect('equal')
axb.legend(handles=[Patch(fc='#B02A30', label='Imaged and sampled'),
                    Patch(fc='white', ec='#666', label='Imaged only'),
                    Patch(fc='#EFC1C6', label='Sampled only')],
           loc='upper left', bbox_to_anchor=(0.36, 1.0), frameon=False,
           fontsize=5.2, handlelength=1.1, handletextpad=0.4)
panel_label(axb, 'b', dx=-0.16, dy=1.04)

# ---------------------------------------------------------------- c: 配对箱线×2
grp = ['Intra-primary', 'Intra-met', 'Inter-met', 'Primary-met']
gcol = ['#2C5F8A', '#1E5B3C', '#3B9C6B', '#37C0C0']


def paired_boxes(axc, means, brackets, ylab):
    data = [np.clip(r.normal(m, 0.11, 14), 0.005, None) for m in means]
    axc.boxplot(data, positions=range(1, 5), widths=0.55, patch_artist=True,
                medianprops={'color': '0.25', 'lw': 1},
                boxprops={'facecolor': 'white', 'edgecolor': '0.35', 'lw': 0.7},
                whiskerprops={'lw': 0.7, 'color': '0.35'},
                capprops={'lw': 0.7, 'color': '0.35'},
                flierprops={'ms': 0})
    for k in range(14):                             # 跨组虚线(配对示意)
        axc.plot([1, 2, 3, 4], [data[g][k] for g in range(4)],
                 ls='--', color='0.75', lw=0.5, zorder=1)
    for g in range(4):
        axc.scatter(np.full(14, g + 1) + r.uniform(-0.13, 0.13, 14), data[g],
                    s=10, fc=gcol[g], ec='white', lw=0.3, zorder=3)
    for x1, x2, ptxt, yy in brackets:
        sig_bracket(axc, x1, x2, yy, ptxt, fontsize=4.8)
    axc.set_xticks(range(1, 5))
    axc.set_xticklabels(grp, rotation=30, ha='right', fontsize=5)
    axc.tick_params(axis='y', labelsize=6)
    axc.set_ylabel(ylab, fontsize=6.5)
    axc.set_ylim(-0.02, 1.05)
    despine(axc)


paired_boxes(axc1, [0.16, 0.08, 0.24, 0.42],
             [(1, 4, r'3.3$\times$10$^{-6}$', 0.93),
              (1, 2, '0.033', 0.76),
              (3, 4, r'6.0$\times$10$^{-6}$', 0.76)],
             'Mean mutation diversity\nper patient')
paired_boxes(axc2, [0.30, 0.12, 0.27, 0.45],
             [(1, 4, r'1.9$\times$10$^{-6}$', 0.93),
              (1, 2, '0.656', 0.76),
              (3, 4, r'6.0$\times$10$^{-6}$', 0.76)],
             'Mean SCNA diversity\nper patient')
panel_label(axc1, 'c', dx=-0.22, dy=1.10)

save(fig, 'case_seg137.png')
