# -*- coding: utf-8 -*-
"""桑基/冲击图助手 — 纯 matplotlib: 多层节点矩形 + 贝塞尔流带。"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Rectangle


def sankey(layers, links, node_colors=None, node_w=0.02, gap=0.04,
           alpha=0.5, fs=8, ax=None, label_side='auto'):
    """layers: [{'name': size, ...}, ...] 每层节点高度(和可不同, 层内归一)。
    links: [(layer_i, src_name, layer_j, dst_name, value, color), ...] j=i+1。
    返回 ax。"""
    if ax is None:
        fig, ax = plt.subplots(figsize=(7.2, 4.2))
    n_layers = len(layers)
    xs = np.linspace(0, 1, n_layers)
    node_pos = {}   # (l, name) -> (y0, y1) 高度
    for li, layer in enumerate(layers):
        tot = sum(layer.values())
        avail = 1.0 - gap * (len(layer) - 1)
        y = 1.0
        for name, v in layer.items():
            h = v / tot * avail
            node_pos[(li, name)] = (y - h, y)
            y -= h + gap
    # 流带: 每个节点维护出/入游标
    out_cur = {k: v[1] for k, v in node_pos.items()}
    in_cur = {k: v[1] for k, v in node_pos.items()}
    layer_tot = [sum(l.values()) for l in layers]
    for (li, src, lj, dst, val, color) in links:
        h_s = val / layer_tot[li] * (1.0 - gap * (len(layers[li]) - 1))
        h_d = val / layer_tot[lj] * (1.0 - gap * (len(layers[lj]) - 1))
        y0s = out_cur[(li, src)] - h_s
        out_cur[(li, src)] = y0s
        y0d = in_cur[(lj, dst)] - h_d
        in_cur[(lj, dst)] = y0d
        x0, x1 = xs[li] + node_w, xs[lj]
        # 三次贝塞尔带
        xm = (x0 + x1) / 2
        verts = [(x0, y0s + h_s), (xm, y0s + h_s), (xm, y0d + h_d), (x1, y0d + h_d),
                 (x1, y0d), (xm, y0d), (xm, y0s), (x0, y0s), (x0, y0s + h_s)]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(verts, codes), facecolor=color,
                               edgecolor='none', alpha=alpha, zorder=1))
    # 节点
    for (li, name), (y0, y1) in node_pos.items():
        col = 'k'
        if node_colors is not None:
            col = node_colors.get(name, 'k')
        ax.add_patch(Rectangle((xs[li], y0), node_w, y1 - y0,
                               facecolor=col, edgecolor='white', lw=0.5, zorder=2))
    ax.set_xlim(-0.18, 1.22)
    ax.set_ylim(-0.05, 1.05)
    ax.axis('off')
    # 标签
    for (li, name), (y0, y1) in node_pos.items():
        ym = (y0 + y1) / 2
        if label_side == 'auto':
            if li == 0:
                ax.text(xs[li] - 0.01, ym, name, ha='right', va='center', fontsize=fs)
            else:
                ax.text(xs[li] + node_w + 0.01, ym, name, ha='left', va='center', fontsize=fs)
    return ax
