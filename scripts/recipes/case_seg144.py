# -*- coding: utf-8 -*-
"""案例144 - 森林图(背景色带): 方块+CI, 方块色按β分级(红High/浅蓝Moderate/黑Low),
背景蓝(0-0.4)/粉(0.4-0.8)竖带, 水平虚线分疾病组, 左侧 Disease/Count/MIRO 列,
右侧 beta (95% CI)/Padj 列。x -0.8~1.6。参考: frames/seg_144.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt

set_style()

ROWS = [
    ('Sjogren disease', 17, '1.39 (2.05)', 1.26, 0.82, 1.71, '<0.0001', 0),
    ('Systemic sclerosis', 12, '0.88 (0.85)', 0.83, 0.27, 1.38, '0.015', 0),
    ('Dermatomyositis', 6, '0.57 (0.63)', 0.70, -0.07, 1.47, '0.201', 0),
    ('Systemic lupus erythematosus', 79, '0.70 (1.47)', 0.64, 0.43, 0.84,
     '<0.0001', 1),
    ('Primary biliary cirrhosis', 13, '0.55 (0.87)', 0.40, -0.11, 0.92,
     '0.258', 0),
    ('Coeliac disease', 76, '0.40 (0.83)', 0.34, 0.13, 0.55, '0.009', 0),
    ('Vasculitis', 38, '0.48 (0.94)', 0.34, 0.04, 0.64, '0.084', 0),
    ('Vitiligo', 19, '0.10 (1.19)', 0.27, -0.16, 0.69, '0.372', 0),
    ('Rheumatoid arthritis', 209, '0.33 (1.08)', 0.22, 0.09, 0.35, '0.005', 0),
    ('Type 1 diabetes', 107, '0.41 (0.89)', 0.21, 0.02, 0.39, '0.084', 1),
    ('Myasthenia gravis', 9, '0.38 (1.48)', 0.19, -0.44, 0.82, '0.609', 0),
    ('Polymyalgia rheumatica', 62, '0.18 (1.34)', 0.17, -0.07, 0.41,
     '0.313', 0),
    ('Sarcoidosis', 43, '0.42 (1.15)', 0.16, -0.12, 0.45, '0.402', 0),
    ('Inflammatory bowel disease', 152, '0.16 (0.94)', 0.13, -0.02, 0.28,
     '0.224', 0),
    ("Hashimoto's disease", 34, '0.03 (0.84)', 0.13, -0.19, 0.44, '0.534', 0),
    ('Ankylosing spondylitis', 28, '0.16 (0.90)', 0.11, -0.24, 0.46,
     '0.612', 0),
    ('Psoriasis', 308, '0.08 (0.91)', 0.05, -0.06, 0.15, '0.519', 0),
    ('Pernicious anaemia', 82, '0.07 (0.90)', -0.01, -0.21, 0.20, '0.940', 0),
    ("Graves' disease", 195, '-0.06 (0.86)', -0.04, -0.17, 0.10, '0.612', 0),
    ('Multiple sclerosis', 73, '-0.19 (0.73)', -0.11, -0.33, 0.11, '0.473', 0),
    ("Addison's disease", 4, '-0.47 (0.99)', -0.58, -1.52, 0.37, '0.372', 0),
]

fig = plt.figure(figsize=cm2in(18.5, 11))
ax = fig.add_axes([0.395, 0.085, 0.475, 0.825])
n = len(ROWS)
YMIN, YMAX = -1.15, n - 0.05


def fy(y):
    return 0.085 + (y - YMIN) / (YMAX - YMIN) * 0.825


# ---------------- 背景竖色带
ax.axvspan(0, 0.4, facecolor='#cfe0f0', alpha=0.8, lw=0, zorder=0)
ax.axvspan(0.4, 0.8, facecolor='#f6d0d0', alpha=0.8, lw=0, zorder=0)

for i, (name, cnt, miro, b, lo, hi, padj, sep) in enumerate(ROWS):
    y = n - 1 - i
    c = '#d82818' if b >= 0.6 else ('#a8c8e0' if b >= 0.2 else '#111111')
    xlo, xhi, arrow_r, arrow_l = lo, hi, False, False
    if hi > 1.58:
        xhi, arrow_r = 1.42, True      # 箭头止于数值列文本 (fig x 0.832) 之前
    if lo < -0.78:
        xlo, arrow_l = -0.70, True
    ax.plot([xlo, xhi], [y, y], color='0.35', lw=1.0, zorder=3)
    if arrow_r:
        ax.annotate('', xy=(1.43, y), xytext=(1.30, y),
                    arrowprops=dict(arrowstyle='->', color='0.35', lw=1.0))
    if arrow_l:
        ax.annotate('', xy=(-0.82, y), xytext=(-0.66, y),
                    arrowprops=dict(arrowstyle='<-', color='0.35', lw=1.0))
    ax.plot([b], [y], marker='s', ms=5.5, color=c, zorder=4)
    fy_ = fy(y)
    fig.text(0.012, fy_, name, fontsize=7.8, va='center')
    fig.text(0.245, fy_, str(cnt), fontsize=7.8, va='center', ha='right')
    fig.text(0.262, fy_, miro, fontsize=7.8, va='center')
    fig.text(0.832, fy_, '%.2f (%.2f, %.2f)' % (b, lo, hi), fontsize=7.2,
             va='center')
    fig.text(0.962, fy_, padj, fontsize=7.4, va='center')
    if sep:
        ax.plot([-2.3, 2.6], [y - 0.5, y - 0.5], color='0.25',
                ls=(0, (4, 2)), lw=1.0, zorder=2, clip_on=False)

# ---------------- 列标题 (两列各自锚定本列中心, 防连印)
yt = fy(n - 0.25)
fig.text(0.012, yt, 'Disease', fontsize=9, fontweight='bold')
fig.text(0.245, yt, 'Count', fontsize=9, fontweight='bold', ha='right')
fig.text(0.262, yt + 0.011, 'MIRO,', fontsize=9, fontweight='bold')
fig.text(0.262, yt - 0.014, 'mean (SD)', fontsize=9, fontweight='bold')
fig.text(0.878, yt, '$\\beta$ (95% CI)', fontsize=9, fontweight='bold',
         ha='center')
fig.text(0.972, yt, 'P$_{adj}$', fontsize=8, fontweight='bold', ha='center')
# Lower / Moderate / High (位于绘图区上方)
for xd, lab, c in [(-0.12, 'Lower', '0.1'), (0.2, 'Moderate', '#3a7ab8'),
                   (0.75, 'High', '#d82818')]:
    fx = 0.395 + (xd + 0.85) / 2.5 * 0.475
    fig.text(fx, yt, lab, fontsize=8, ha='center', color=c)

# ---------------- 参考线与阈值标注
ax.axvline(0, color='0.2', ls='--', lw=1.0, zorder=1)
ax.axvline(0.4, color='#d82818', ls='--', lw=1.0, zorder=1)
tr = ax.get_yaxis_transform()
ax.text(0.2, -0.75, '$\\beta$=0.2', fontsize=7, color='#3a7ab8',
        ha='center', transform=tr)
ax.text(0.6, -0.75, '$\\beta$=0.6', fontsize=7, color='#d82818',
        ha='center', transform=tr)

ax.set_xlim(-0.85, 1.65)
ax.set_ylim(YMIN, YMAX)
ax.set_xticks([-0.8, -0.4, 0, 0.4, 0.8, 1.2, 1.6])
ax.tick_params(labelsize=8.5)
ax.set_xlabel('$\\beta$', fontsize=10)
ax.set_yticks([])
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)

save(fig, 'case_seg144.png')
