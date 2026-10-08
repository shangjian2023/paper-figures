# -*- coding: utf-8 -*-
"""案例57 (seg55) - Nature 网络条形图: 放射状网络 + 外圈径向条形。
参考: frames/seg_055.jpg — 中心彩色类别圆点 + 细曲线放射连到外圈径向条形(条长∝权重,
色随类别), 外缘沿半径旋转标签, 类别名彩色粗体在中心区。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *
set_style()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Wedge

r = rng(55)

# (类别名, 颜色, 条目, 条目角度半径微调) — 按参考图顺时针排布
cats = [
    ('Miscellaneous\nMetabolism', '#E88C2A',
     ['Fur_1', 'Rex_1', 'NreC', 'Rex_2', 'Fur_2', 'PhoR', 'FadR', 'FMN', 'MntR',
      'Oxoproline metabolism', 'Ascorbate transport']),
    ('Stress\nResponse', '#C7325A',
     ['SigB', 'Vras2_2', 'SigS', 'Vras2_1', 'BelR', 'Beta lactam resistance', 'LrgAB', 'TA system']),
    ('Carbon\nMetabolism', '#2E8B57',
     ['CcpA_1', 'CcpA_2', 'CggR', 'LacR', 'FruR', 'GlpR', 'ManR']),
    ('Uncharacterized', '#3D3D3D',
     ['Uncharacterized_1', 'Uncharacterized_7', 'Uncharacterized_2', 'Uncharacterized_4',
      'scfm2 artefact', 'Uncharacterized_9', 'Uncharacterized_8', 'Uncharacterized_3',
      'Uncharacterized_5', 'Uncharacterized_6']),
    ('Cellular\nProcesses', '#2B7BBA', ['Translation_1', 'Translation_2', 'Autolysin', 'LTA']),
    ('Prophages', '#D02E2E', ['Phi_Sa3_1', 'Phi_Sa3_2', 'Phi_Sa3_3', 'Genomic island 3']),
    ('Other', '#4A4A4A', ['Itaconate response', 'SCCMec/ACME']),
    ('Single\nGenes', '#C9A83A', ['SG_8', 'SG_6', 'SG_5', 'SG_4', 'SG_2', 'SG_3', 'SG_1']),
    ('Virulence', '#8C2D2D',
     ['Capsule biosynthesis', 'ArlRS', 'AgrA', 'PSM', 'HssR', 'SaeR_2', 'SaeR_1',
      'Vir_1', 'Vir_2', 'MgrA']),
    ('AA/Nucleotide\nMetabolism', '#5B4EA8',
     ['CodY_1', 'CodY_2', 'CymR', 'PurR', 'CtsR', 'ILVopor', 'PyrR', 'Purine',
      'ArgR', 'TPP', 'ArcR', 'PurR accessory']),
]
boost = {'CcpA_1': 0.95, 'SigB': 0.88, 'MgrA': 0.82, 'CodY_1': 0.80, 'CodY_2': 0.55,
         'PurR accessory': 0.86, 'Fur_1': 0.78, 'Vras2_1': 0.62, 'SG_8': 0.55,
         'SaeR_1': 0.72, 'Uncharacterized_3': 0.30}
# 中心类别标签: 贪婪自动布点(检查标签/圆点互不相交), 模拟参考图的错落布局
FIG_W_IN = 16 / 2.54
SPAN = 3.9

def _hw(text, fs):
    return 0.5 * max(len(t) for t in text.split('\n')) * fs * 0.64 / 72 / (FIG_W_IN / SPAN)

def _hh(text, fs):
    return 0.5 * len(text.split('\n')) * fs * 1.25 / 72 / (FIG_W_IN / SPAN)

def place_label(text, th_c, placed, dots, fs=9):
    """稠密螺旋扫描: 从理想角度向四周找第一个不与已放标签/圆点重叠的位置。"""
    hw, hh = _hw(text, fs), _hh(text, fs)
    for rad in np.arange(0.46, 1.00, 0.04):
        hits = []
        for dth in np.arange(-95, 96, 5):
            th = th_c + np.deg2rad(dth)
            x, y = rad * np.cos(th), rad * np.sin(th)
            if any(abs(x - px) < hw + pw + 0.06 and abs(y - py) < hh + ph + 0.03
                   for px, py, pw, ph in placed):
                continue
            if any(abs(x - dx) < hw + 0.09 and abs(y - dy) < hh + 0.09
                   for dx, dy in dots):
                continue
            hits.append((abs(dth), x, y))
        if hits:
            hits.sort()
            _, x, y = hits[0]
            placed.append((x, y, hw, hh))
            return x, y
    placed.append((0, 0, hw, hh))
    return 0.0, 0.0

items = [(name, c, it) for name, c, its in cats for it in its]
n_items = len(items)
slot = 2 * np.pi / n_items
r0, rc = 1.02, 0.30                      # 条形内半径 / 中心点半径

fig, ax = plt.subplots(figsize=cm2in(16, 16))
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-1.95, 1.95); ax.set_ylim(-1.95, 1.95)

cat_centers = []
cum = 0.0
for name, col, its in cats:
    k = len(its)
    thetas = [np.deg2rad(90) - (cum + i + 0.5) * slot for i in range(k)]
    cat_centers.append((name, col, its, thetas, float(np.mean(thetas))))
    cum += k

dots = [(rc * np.cos(t[4]), rc * np.sin(t[4])) for t in cat_centers]
placed = []
texts = []
for (name, col, its, thetas, th_c), (dx, dy) in zip(cat_centers, dots):
    ax.scatter([dx], [dy], s=150, color=col, zorder=5)
    lx, ly = place_label(name, th_c, placed, dots, fs=9)
    texts.append(ax.text(lx, ly, name, color=col, fontsize=9, fontweight='bold',
                         ha='center', va='center', zorder=6))

# 实测包围盒 + 松弛迭代: 彻底消除中心标签互叠(估计盒偏小导致的视觉重叠)
fig.canvas.draw()
ren = fig.canvas.get_renderer()
inv = ax.transData.inverted()
GAP = 0.04
for _ in range(400):
    boxes = []
    for t in texts:
        bb = t.get_window_extent(renderer=ren)
        (bx0, by0), (bx1, by1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        boxes.append((bx0, by0, bx1, by1))
    moved = 0.0
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = boxes[i], boxes[j]
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > -GAP and oy > -GAP:            # 重叠(含安全间隙) -> 沿中心连线推开
                ca = ((a[0] + a[2]) / 2, (a[1] + a[3]) / 2)
                cb = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
                ddx, ddy = cb[0] - ca[0], cb[1] - ca[1]
                if abs(ddx) >= abs(ddy):
                    step = min(0.05, 0.5 * (ox + GAP)) * (1 if ddx >= 0 else -1)
                    for k, sg in ((i, -1), (j, 1)):
                        px, py = texts[k].get_position()
                        texts[k].set_position((px + sg * step, py))
                else:
                    step = min(0.05, 0.5 * (oy + GAP)) * (1 if ddy >= 0 else -1)
                    for k, sg in ((i, -1), (j, 1)):
                        px, py = texts[k].get_position()
                        texts[k].set_position((px, py + sg * step))
                moved = max(moved, abs(step))
    for t in texts:                                # 不压中心圆点, 不越出内圈
        px, py = t.get_position()
        rr = np.hypot(px, py)
        if rr > 1.02:
            t.set_position((px * 1.02 / rr, py * 1.02 / rr))
            moved = max(moved, 0.01)
        for ddx, ddy in dots:
            if abs(px - ddx) < 0.17 and abs(py - ddy) < 0.13:
                vx, vy = px - ddx, py - ddy
                nn = np.hypot(vx, vy) or 1.0
                t.set_position((px + 0.03 * vx / nn, py + 0.03 * vy / nn))
                moved = max(moved, 0.01)
                break
    if moved == 0:
        break
    fig.canvas.draw()

cum = 0.0
for name, col, its in cats:
    k = len(its)
    thetas = [np.deg2rad(90) - (cum + i + 0.5) * slot for i in range(k)]
    cum += k
    th_c = float(np.mean(thetas))
    # 条目
    for it, th in zip(its, thetas):
        val = boost.get(it, r.uniform(0.15, 0.62))
        # 曲线: 中心点 -> 条形根部 (二次贝塞尔)
        p0 = np.array([rc * np.cos(th_c), rc * np.sin(th_c)])
        p2 = np.array([r0 * np.cos(th), r0 * np.sin(th)])
        p1 = np.array([(rc + r0) / 2 * np.cos(th), (rc + r0) / 2 * np.sin(th)])
        patch = PathPatch(Path([p0, p1, p2], [Path.MOVETO, Path.CURVE3, Path.CURVE3]),
                          fc='none', ec=col, lw=0.55, alpha=0.6, zorder=1)
        ax.add_patch(patch)
        # 径向条形(环形扇)
        ln = 0.14 + val * 0.42
        w = np.degrees(slot) * 0.52
        ax.add_patch(Wedge((0, 0), r0 + ln, np.degrees(th) - w / 2,
                           np.degrees(th) + w / 2, width=ln, facecolor=col,
                           edgecolor='none', alpha=0.95, zorder=3))
        # 外缘旋转标签
        rt = np.degrees(th) % 360
        if 90 < rt < 270:
            rot, ha = rt - 180, 'right'
        else:
            rot, ha = rt, 'left'
        rr = r0 + ln + 0.05
        ax.text(rr * np.cos(th), rr * np.sin(th), it, rotation=rot,
                rotation_mode='anchor', ha=ha, va='center', fontsize=6.8, color=col)

save(fig, 'case_seg055.png')
