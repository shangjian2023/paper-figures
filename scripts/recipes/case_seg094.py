# -*- coding: utf-8 -*-
"""案例96 - Nature 环状柱形图(SD): 29 个代表性指标径向柱, 柱高=SD(-1.5~+1.5),
红黄蓝渐变, 星号显著性, 中心圆盘分区注释, 右上色条。
参考: frames/seg_094.jpg。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import set_style, save, cm2in

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

set_style()

cats = [
    ('Mental\nquality\nof life',
     ['SF8_mentalcomp*', 'SF8_mentalhlt*', 'SF8_roleemot*'], (0.9, 1.5)),
    ('Tinnitus\ncharacteristics',
     ['TINSKAL_freq', 'TINSKAL_loudness', 'TLQ_botheread', 'TLQ_hissing'],
     (-0.4, 0.45)),
    ('Physical\nquality\nof life',
     ['SF8_overallhlt*', 'SF8_physcomp*', 'SF8_rolephys*'], (0.8, 1.4)),
    ('Experiences\nof pain',
     ['SES_affectivepain', 'SSKAL_painfreq*', 'SSKAL_painsev*'], (0.5, 1.2)),
    ('Somatic\nexpressions',
     ['BI_abdsymptoms', 'BI_fatigue', 'BI_overallcompl'], (0.7, 1.3)),
    ('Affective\nsymptoms',
     ['ADSL_depression', 'BSF_anxidepr*', 'BSF_fatigue'], (0.6, 1.4)),
    ('Tinnitus-\nrelated\ndistress',
     ['ISR_depression*', 'ISR_anxiety*', 'ISR_totalpsych*',
      'PHOK_panicsyn*'], (0.8, 1.5)),
    ('Internal\nresources',
     ['TQ_distress*', 'TQ_intrusiveness', 'TQ_cogdistress'], (-0.5, 0.9)),
    ('Perceived\nstress',
     ['ACSA_qol*', 'PSQ_stress', 'SWOP_optimism*'], (0.4, 1.1)),
]
metrics, bounds, cat_mid = [], [], []
for cname, names, (lo, hi) in cats:
    metrics += names
    bounds += [lo, hi]
    cat_mid.append((cname, len(metrics) - len(names) / 2 - 0.5, len(names)))
N = len(metrics)

rng = np.random.default_rng(94)
z = np.empty(N)
k = 0
for _, names, (lo, hi) in cats:
    z[k:k + len(names)] = rng.uniform(lo, hi, len(names))
    k += len(names)

# 径向刻度所在方位(约205度, 左下)必须无柱: 清空夹住该间隙的两根柱
step_deg = 360.0 / N
k_gap = int(round(205.0 / step_deg - 0.5)) % N   # 205度落在 k_gap 与 k_gap+1 的间隙
z[k_gap] = 0.12
z[(k_gap + 1) % N] = 0.18

fig = plt.figure(figsize=cm2in(16.5, 17.0))
ax = fig.add_subplot(projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_ylim(-2.75, 2.10)
ax.set_rorigin(-3.40)
ax.set_yticks([-1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5])
ax.set_yticklabels(['\u22121.5', '\u22121.0', '\u22120.5', '0', '+0.5',
                    '+1.0', '+1.5'], fontsize=6)
# 径向刻度放到左下 205 度的柱间空隙, 避开顶部柱体
ax.set_rlabel_position((k_gap + 0.5) * step_deg)
ax.set_xticks([])
ax.set_thetamin(0)
ax.set_thetamax(360)
ax.spines['polar'].set_visible(False)
ax.patch.set_visible(False)
ax.grid(False)
ax.tick_params(pad=6)

norm = Normalize(-1.5, 1.5)
cmap = plt.get_cmap('RdYlBu_r')
step = 360.0 / N
th = np.radians(np.arange(N) * step)

# 中心米色圆盘 + 分区刻痕 + 类目文字
from matplotlib.patches import Circle
disk_r = (-1.95 + 3.40) / 5.50 * 0.5             # 屏幕半径占比(transAxes)
ax.add_patch(Circle((0.5, 0.5), disk_r, transform=ax.transAxes,
                    fc='#F4E1D2', ec='black', lw=1.1, zorder=10,
                    clip_on=False))
k = 0
for cname, _, cnt in cat_mid:
    tb = np.radians(k * step)
    ax.plot([tb, tb], [-1.95, -1.78], color='black', lw=0.8, zorder=11)
    tmid = np.radians((k + cnt / 2) * step)
    ax.text(tmid, -2.18, cname, ha='center', va='center', fontsize=4.0,
            color='#3A3A3A', linespacing=1.05, zorder=11)
    k += cnt
# 中心标题拆 3 行短行, 最长行半宽≈0.48 盘半径, 与左右域标签(内缘≈0.62 盘半径)零相交
ax.text(0.5, 0.5, 'PT 2 (n=173)\npsychosomatic\ngroup',
        transform=ax.transAxes, ha='center', va='center', fontsize=6.0,
        fontweight='bold', linespacing=1.35, zorder=11)

for i in range(N):
    t = th[i]
    w = np.radians(step * 0.62)
    val = z[i]
    color = cmap(norm(val))
    if val >= 0:
        ax.bar(t, val, width=w, bottom=0, color=color, ec='none', zorder=11)
        tip = val
    else:
        ax.bar(t, -val, width=w, bottom=val, color=color, ec='none',
               zorder=11)
        tip = 0.0
    # 柱端误差帽 + 内圈灰色短刻线
    ax.plot([t - w * 0.45, t + w * 0.45], [tip + 0.02, tip + 0.02],
            color='#555555', lw=0.6, zorder=12)
    ax.plot([t, t], [-0.62, -0.40], color='#B8B8B8', lw=0.9, zorder=11)
    # 外侧指标标签: 统一放外圈, 切向旋转, 隔一根错位半径防重叠
    tdeg = np.degrees(t) % 360
    rot = -tdeg if tdeg <= 90 or tdeg > 270 else 180 - tdeg
    rr = 1.64 if i % 2 == 0 else 1.80
    ax.text(t, rr, metrics[i], rotation=rot, rotation_mode='anchor',
            ha='center', va='center', fontsize=4.1,
            color='#6E6E6E', zorder=12)

# 右上色条
cax = fig.add_axes([0.905, 0.795, 0.016, 0.135])
sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])
cb = fig.colorbar(sm, cax=cax)
cb.set_ticks([1.5, 0, -1.5])
cb.set_ticklabels(['+1.5 SD', 'Patient\naverage', '\u22121.5 SD'])
cb.ax.tick_params(labelsize=5.5, length=2)
cb.outline.set_visible(False)

save(fig, 'case_seg094.png')
