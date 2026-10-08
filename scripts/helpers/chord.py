# -*- coding: utf-8 -*-
"""和弦图 (chord diagram) 助手 — 纯 matplotlib 实现(d3 风格贝塞尔带)。"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path

DEG = np.degrees


def _arc_patch(c, r, th1, th2, width, color, alpha=1.0):
    """环形弧段(外半径 r, 等宽 width)。th1>th2 亦可。"""
    if th2 < th1:
        th1, th2 = th2, th1
    n = max(int(abs(th2 - th1) / np.radians(2)), 4)
    ts = np.linspace(th1, th2, n)
    xs_o = c[0] + r * np.cos(ts)
    ys_o = c[1] + r * np.sin(ts)
    xs_i = c[0] + (r - width) * np.cos(ts)
    ys_i = c[1] + (r - width) * np.sin(ts)
    verts = list(zip(xs_o, ys_o)) + list(zip(xs_i[::-1], ys_i[::-1]))
    codes = [Path.MOVETO] + [Path.LINETO] * (2 * n - 2) + [Path.CLOSEPOLY]
    return PathPatch(Path(verts, codes), facecolor=color, edgecolor='white',
                     lw=0.4, alpha=alpha)


def _pt(c, r, th):
    return (c[0] + r * np.cos(th), c[1] + r * np.sin(th))


def _ribbon(c, r, a1, a2, b1, b2, color, alpha=0.45, k=0.55):
    """带状: 外缘从 a1..a2, 对端 b1..b2(角度), 三次贝塞尔过渡。"""
    p1 = np.array(_pt(c, r, a1)); p2 = np.array(_pt(c, r, b1))
    p3 = np.array(_pt(c, r, b2)); p4 = np.array(_pt(c, r, a2))
    rc = r * (1 - k)
    c1 = np.array(_pt(c, rc, a1)); c2 = np.array(_pt(c, rc, b1))
    c3 = np.array(_pt(c, rc, b2)); c4 = np.array(_pt(c, rc, a2))
    verts = [tuple(p1), tuple(c1), tuple(c2), tuple(p2),
             tuple(p3), tuple(c3), tuple(c4), tuple(p4), tuple(p1)]
    codes = [Path.MOVETO] + [Path.CURVE4] * 3 + [Path.LINETO] + [Path.CURVE4] * 3 + [Path.CLOSEPOLY]
    return PathPatch(Path(verts, codes), facecolor=color, edgecolor='none', alpha=alpha)


def chord_diagram(labels, matrix, colors=None, ax=None, gap_deg=4, r_label=1.10,
                  label_fs=8, ribbon_alpha=0.45, start_angle=90, arc_width=0.035):
    """labels: 节点名; matrix: 方阵(行=源); colors: 每节点颜色(带用行色)。返回 ax。"""
    if ax is None:
        fig, ax = plt.subplots(figsize=(6.8, 6.8))
    ax.set_aspect('equal')
    ax.axis('off')
    M = np.asarray(matrix, dtype=float)
    n = len(labels)
    if colors is None:
        cmap = plt.get_cmap('tab20')
        colors = [cmap(i % 20) for i in range(n)]
    colors = list(colors) + [plt.get_cmap('tab20')(i % 20) for i in range(n - len(colors))] if len(colors) < n else list(colors)
    total = M.sum()
    sizes = M.sum(axis=1)
    circle = 360.0 - gap_deg * n
    # 每节点弧段(顺时针)
    angles = []
    a0 = start_angle
    for i in range(n):
        span = sizes[i] / total * circle
        angles.append((a0 - span, a0))
        a0 -= span + gap_deg
    c = (0.0, 0.0)
    R = 1.0
    # 列方向的累计比例(入带分配)
    col_frac = M / np.where(M.sum(axis=0, keepdims=True) == 0, 1, M.sum(axis=0, keepdims=True))
    row_frac = M / np.where(M.sum(axis=1, keepdims=True) == 0, 1, M.sum(axis=1, keepdims=True))
    # 行游标(出带)与列游标(入带)
    row_pos = np.zeros(n)
    col_pos = np.zeros(n)
    # 先画带(底层)
    for i in range(n):
        a_hi = np.radians(angles[i][1])
        span = np.radians(angles[i][1] - angles[i][0])
        for j in range(n):
            if i == j or M[i, j] <= 0:
                continue
            w = row_frac[i, j] * span
            a1 = a_hi - row_pos[i]
            a2 = a1 - w
            row_pos[i] += w
            b_hi = np.radians(angles[j][1])
            bspan = np.radians(angles[j][1] - angles[j][0])
            w2 = col_frac[i, j] * bspan
            b1 = b_hi - col_pos[j]
            b2 = b1 - w2
            col_pos[j] += w2
            ax.add_patch(_ribbon(c, R, a1, a2, b1, b2, colors[i], alpha=ribbon_alpha))
    # 节点弧(顶层)
    for i in range(n):
        a1, a2 = angles[i]
        ax.add_patch(_arc_patch(c, R, np.radians(a1), np.radians(a2), arc_width, colors[i]))
        mid = (a1 + a2) / 2.0
        mrad = np.radians(mid)
        rot = mid if mid <= 180 else mid - 360
        if abs(rot) > 90:
            rot += 180
        ax.text(c[0] + r_label * np.cos(mrad), c[1] + r_label * np.sin(mrad),
                labels[i], ha='center', va='center', fontsize=label_fs, rotation=rot,
                rotation_mode='anchor')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    return ax
