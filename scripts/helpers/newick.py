# -*- coding: utf-8 -*-
"""Newick 系统发育树解析 + 环形布局助手 — 纯 numpy/matplotlib(笛卡尔坐标)。"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc


def random_newick(n_leaves, seed=0, names=None):
    """生成随机二叉树的 Newick 字符串(叶等长)。"""
    r = np.random.default_rng(seed)
    clusters = [(names[i] if names else 'T%d' % (i + 1)) for i in range(n_leaves)]
    while len(clusters) > 1:
        i, j = r.choice(len(clusters), 2, replace=False)
        a, b = clusters[i], clusters[j]
        clusters = [c for k, c in enumerate(clusters) if k not in (i, j)]
        clusters.append('(%s,%s)' % (a, b))
    return clusters[0] + ';'


def parse_newick(s):
    """返回嵌套 dict: {'name':..., 'children': [...]}"""
    s = s.strip().rstrip(';')
    pos = 0

    def parse_node():
        nonlocal pos
        children = []
        if pos < len(s) and s[pos] == '(':
            pos += 1
            while True:
                children.append(parse_node())
                if pos < len(s) and s[pos] == ',':
                    pos += 1
                elif pos < len(s) and s[pos] == ')':
                    pos += 1
                    break
                else:
                    break
        start = pos
        while pos < len(s) and s[pos] not in ',()':
            pos += 1
        name = s[start:pos].strip()
        return {'name': name, 'children': children}

    return parse_node()


def leaf_names(tree):
    if not tree['children']:
        return [tree['name']]
    out = []
    for ch in tree['children']:
        out += leaf_names(ch)
    return out


def _max_depth(node):
    if not node['children']:
        return 0
    return 1 + max(_max_depth(c) for c in node['children'])


def draw_circular_tree(ax, tree, color_fn=None, leaf_dot=2.5, lw=0.8,
                       tip_label_fs=5, tip_labels=True, r_label=1.06):
    """环形系统发育树(等支长)。color_fn(name, is_leaf, depth)->color。
    所有几何用笛卡尔坐标: (r·cosθ, r·sinθ)。"""
    leaves = leaf_names(tree)
    n = len(leaves)
    total = max(_max_depth(tree), 1)
    ang_of = {nm: 2 * np.pi * (i + 0.5) / n for i, nm in enumerate(leaves)}

    def pt(th, r):
        return (r * np.cos(th), r * np.sin(th))

    # 后序: 每个节点分配角度区间 [a0,a1](按叶数比例切分) 与中点角
    order = []
    nleaves = {}

    def count_leaves(node):
        if not node['children']:
            nleaves[id(node)] = 1
        else:
            nleaves[id(node)] = sum(count_leaves(c) for c in node['children'])
        return nleaves[id(node)]

    count_leaves(tree)

    def assign(node, a0, a1, depth):
        node['_a0'], node['_a1'], node['_d'] = a0, a1, depth
        order.append(node)
        if node['children']:
            k = nleaves[id(node)]
            pos = a0
            for ch in node['children']:
                w = nleaves[id(ch)] / k * (a1 - a0)
                assign(ch, pos, pos + w, depth + 1)
                pos += w
        node['_mid'] = ang_of[node['name']] if not node['children'] else 0.5 * (a0 + a1)

    assign(tree, 0.0, 2 * np.pi, 0)

    def r_of(d):
        return d / (total + 1.0)

    for node in order:
        depth = node['_d']
        r_in, r_out = r_of(depth), r_of(depth + 1)
        a0, a1, mid = node['_a0'], node['_a1'], node['_mid']
        is_leaf = not node['children']
        col = color_fn(node['name'], is_leaf, depth) if color_fn else 'k'
        if is_leaf:
            # 悬挂在父弧上: 父区间任取叶角 — 用叶自身角
            a = ang_of[node['name']]
            # 父节点弧半径 = r_in; 从 (r_in, a) 径向到 (r_out, a)
            x0, y0 = pt(a, r_in); x1, y1 = pt(a, r_out)
            ax.plot([x0, x1], [y0, y1], color=col, lw=lw, zorder=2)
            if leaf_dot:
                ax.plot([x1], [y1], 'o', ms=leaf_dot, color=col, zorder=3)
            if tip_labels:
                deg = np.degrees(a)
                rot = deg - 90 if 90 < deg % 360 <= 270 else deg + 90
                ax.text(*(pt(a, r_out * r_label)), node['name'], fontsize=tip_label_fs,
                        ha='center', va='center', rotation=rot, rotation_mode='anchor')
        else:
            # 径向连接: 从父半径沿本节点中点角
            x0, y0 = pt(mid, r_in); x1, y1 = pt(mid, r_out)
            ax.plot([x0, x1], [y0, y1], color=col, lw=lw, zorder=2)
            # 弧段: 覆盖本节点整个角度区间
            if abs(a1 - a0) > 1e-9:
                ax.add_patch(Arc((0, 0), 2 * r_out, 2 * r_out, angle=0,
                                 theta1=np.degrees(a0), theta2=np.degrees(a1),
                                 color=col, lw=lw, zorder=2))
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    ax.set_aspect('equal')
    ax.axis('off')


def draw_rect_tree(ax, tree, color_fn=None, lw=0.8, leaf_dot=2.5,
                   tip_label_fs=6, tip_labels=True):
    """矩形肘系统发育树(X=深度, Y=叶序)。"""
    leaves = leaf_names(tree)
    n = len(leaves)
    total = max(_max_depth(tree), 1)
    y_of = {nm: n - 1 - i for i, nm in enumerate(leaves)}
    order = []
    nleaves = {}

    def count_leaves(node):
        if not node['children']:
            nleaves[id(node)] = 1
        else:
            nleaves[id(node)] = sum(count_leaves(c) for c in node['children'])
        return nleaves[id(node)]

    count_leaves(tree)

    def assign(node, y0, y1, depth):
        node['_y0'], node['_y1'], node['_d'] = y0, y1, depth
        order.append(node)
        if node['children']:
            k = nleaves[id(node)]
            pos = y0
            for ch in node['children']:
                w = nleaves[id(ch)] / k * (y1 - y0)
                assign(ch, pos, pos + w, depth + 1)
                pos += w
        node['_ym'] = y_of[node['name']] if not node['children'] else 0.5 * (y0 + y1)

    assign(tree, -0.5, n - 0.5, 0)

    def x_of(d):
        return d / (total + 1.0)

    for node in order:
        is_leaf = not node['children']
        col = color_fn(node['name'], is_leaf, node['_d']) if color_fn else 'k'
        x_in, x_out = x_of(node['_d']), x_of(node['_d'] + 1)
        if is_leaf:
            ax.plot([x_in, x_out], [node['_ym']] * 2, color=col, lw=lw)
            if leaf_dot:
                ax.plot([x_out], [node['_ym']], 'o', ms=leaf_dot, color=col)
            if tip_labels:
                ax.text(x_out + 0.02, node['_ym'], node['name'], fontsize=tip_label_fs,
                        va='center', ha='left')
        else:
            ax.plot([x_in, x_out], [node['_ym']] * 2, color=col, lw=lw)
            for ch in node['children']:
                ax.plot([x_out, x_out], [node['_ym'], ch['_ym']], color=col, lw=lw)
    ax.set_xlim(-0.02, 1.25)
    ax.set_ylim(-0.8, n - 0.2)
    ax.axis('off')
