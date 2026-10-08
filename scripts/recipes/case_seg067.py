# -*- coding: utf-8 -*-
"""案例69 - Nature 蝴蝶状&堆积条形图: 镜像水平堆积条。
参考: frames/seg_067.jpg — 左 PFS 右 OS, 蓝 Protective + 红 Risk 堆积,
中央 9 个细胞态标签, x=10-0-10, 红虚线框高亮首行。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch

set_style()

states = [r'$APLN^{+}$Tip$^{SI}$', r'Stalk$^{SI}$', r'Tip$^{SIII}$', 'Transition',
          r'Tip$^{SII}$', r'Stalk$^{SIII}$', r'Stalk$^{SII}$', 'ArtEC', 'VenEC']
# (risk, protective) 左=PFS, 右=OS
pfs = [(11.0, 0.0), (0.0, 3.6), (2.2, 2.4), (0.8, 3.2), (0.0, 1.8),
       (0.9, 4.2), (0.0, 1.2), (1.1, 0.5), (1.4, 0.0)]
os_ = [(11.0, 0.0), (2.2, 4.2), (2.4, 2.2), (1.0, 1.2), (0.0, 3.8),
       (0.4, 0.6), (1.2, 2.2), (1.0, 1.0), (0.0, 1.6)]

c_pro, c_risk = '#4E8ABE', '#A62A34'
n = len(states)
ys = np.arange(n)[::-1]

fig, (axL, axM, axR) = plt.subplots(
    1, 3, figsize=cm2in(19, 12.5), sharey=True,
    gridspec_kw={'width_ratios': [1.05, 0.62, 1.05], 'wspace': 0.0})

for ax, dat, sign in ((axL, pfs, -1), (axR, os_, 1)):
    for y, (risk, pro) in zip(ys, dat):
        # Risk(红)紧贴 0, Protective(蓝)向外
        ax.barh(y, sign * risk, height=0.72, color=c_risk, edgecolor='black',
                lw=0.5, zorder=3)
        ax.barh(y, sign * pro, left=sign * risk, height=0.72, color=c_pro,
                edgecolor='black', lw=0.5, zorder=3)
    ax.set_xlim(-12.4 if sign < 0 else -0.05, -0.05 if sign < 0 else 12.4)
    ax.set_ylim(-0.7, n - 0.3 + 1.15)
    despine(ax, left=True, bottom=False)
    ax.tick_params(left=False, length=3)

axL.set_xticks([-10, -5, 0])
axL.set_xticklabels(['10', '5', '0'])
axR.set_xticks([0, 5, 10])
axR.set_yticks(ys)
axL.tick_params(labelleft=False)

axM.set_xlim(0, 1)
axM.set_ylim(-0.7, n - 0.3 + 1.15)
axM.axis('off')
for y, s in zip(ys, states):
    axM.text(0.5, y, s, ha='center', va='center', fontsize=10.5)

axL.set_title('PFS in TCGA', loc='left', fontsize=11.5, pad=6)
axR.set_title('OS in TCGA', loc='left', fontsize=11.5, pad=6)

# 红虚线框高亮首行
ytop = ys[0]
axL.add_patch(Rectangle((-12.15, ytop - 0.52), 12.10, 1.04, fill=False,
                        ec='#C0392B', ls='--', lw=1.3, zorder=5))
axR.add_patch(Rectangle((0.05, ytop - 0.52), 12.10, 1.04, fill=False,
                        ec='#C0392B', ls='--', lw=1.3, zorder=5))

fig.text(0.5, 0.035, 'Number of cancer types', ha='center', va='center', fontsize=10)

leg = axL.legend(handles=[Patch(fc=c_pro, ec='black', lw=0.5, label='Protective'),
                          Patch(fc=c_risk, ec='black', lw=0.5, label='Risk')],
                 loc='lower left', bbox_to_anchor=(0.0, 0.06), frameon=False,
                 fontsize=9, handlelength=1.3, handleheight=1.1)

fig.subplots_adjust(left=0.045, right=0.985, top=0.92, bottom=0.115)
save(fig, 'case_seg067.png')
