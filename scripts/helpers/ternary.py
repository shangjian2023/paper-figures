# -*- coding: utf-8 -*-
"""三元图 (ternary plot) 助手: 顶点 A(上) B(左下) C(右下)。

坐标定义(重心坐标, 归一化后 fa+fb+fc=1):
    P = fa*A + fb*B + fc*C,  A=(0.5, H), B=(0,0), C=(1,0), H=sqrt(3)/2
    即 x = 0.5*fa + fc, y = fa*H
网格线: fa=t 平行底边 BC; fb=t 平行右边 CA; fc=t 平行左边 AB。
"""
import numpy as np
from matplotlib.patches import FancyArrowPatch


class Ternary:
    """三元坐标 → 直角坐标。fA+fB+fC=1。"""

    H = np.sqrt(3) / 2  # 单位边三角形高度

    def __init__(self, ax, vertex_labels=('A', 'B', 'C')):
        self.ax = ax
        self.vl = vertex_labels

    @staticmethod
    def xy(fa, fb, fc):
        s = fa + fb + fc
        fa, fb, fc = fa / s, fb / s, fc / s
        x = 0.5 * fa + fc
        y = fa * Ternary.H
        return x, y

    def setup(self, grid_values=(20, 40, 60, 80), grid_colors=('r', 'g', 'b'),
              show_grid=True, tick_labels=True, fs=8):
        ax = self.ax
        ax.set_xlim(-0.08, 1.08)
        ax.set_ylim(-0.06, self.H + 0.10)
        ax.set_aspect('equal')
        ax.axis('off')
        A = (0.5, self.H)
        B = (0.0, 0.0)
        C = (1.0, 0.0)
        # 外框
        for p, q in [(A, B), (B, C), (C, A)]:
            ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=1.0)
        if show_grid:
            for v, col in zip(grid_values, grid_colors):
                t = v / 100.0
                # fa=t: 平行 BC, 端点 (t/2, tH)-(1-t/2, tH)
                ax.plot([t / 2, 1 - t / 2], [t * self.H] * 2, ls=':', lw=0.8, color=col)
                # fb=t: 平行 CA, 端点 (1-t, 0)-(0.5(1-t), (1-t)H)
                ax.plot([1 - t, 0.5 * (1 - t)], [0, (1 - t) * self.H], ls=':', lw=0.8, color=col)
                # fc=t: 平行 AB, 端点 (t, 0)-(0.5+0.5t, (1-t)H)
                ax.plot([t, 0.5 + 0.5 * t], [0, (1 - t) * self.H], ls=':', lw=0.8, color=col)
        if tick_labels:
            for v in grid_values:
                t = v / 100.0
                # fa 刻度: 左斜边 AB 上 (t/2, tH), 向左外偏
                ax.text(t / 2 - 0.035, t * self.H, str(v), fontsize=fs - 1,
                        color='k', ha='right', va='center')
                # fb 刻度: 底边上 x=1-t, 向下偏
                ax.text(1 - t, -0.03, str(v), fontsize=fs - 1, ha='center', va='top')
                # fc 刻度: 右斜边 CA 上 (0.5+0.5t, (1-t)H), 向右外偏
                ax.text(0.5 + 0.5 * t + 0.035, (1 - t) * self.H, str(v), fontsize=fs - 1,
                        ha='left', va='center')
        # 顶点标签
        ax.text(A[0], A[1] + 0.03, self.vl[0], ha='center', fontsize=fs + 1, fontweight='bold')
        ax.text(B[0] - 0.02, B[1] - 0.02, self.vl[1], ha='right', va='top',
                fontsize=fs + 1, fontweight='bold')
        ax.text(C[0] + 0.02, C[1] - 0.02, self.vl[2], ha='left', va='top',
                fontsize=fs + 1, fontweight='bold')
        return self

    def edge_arrows(self, labels, colors=('g', 'b', 'r'), fs=8):
        """三条边中点画顺时针箭头, 标注对应分量名。
        labels = (fa_name, fb_name, fc_name); 箭头所在边: fa→底边BC, fb→右边CA, fc→左边AB。"""
        ax = self.ax
        A = np.array([0.5, self.H]); B = np.array([0.0, 0.0]); C = np.array([1.0, 0.0])
        # (起点, 终点, 外法线方向): 底边 C→B 法线向下; 右边 A→C 法线右下; 左边 B→A 法线左上
        edges = [(C, B, np.array([0.0, -1.0])),
                 (A, C, np.array([0.87, -0.5])),
                 (B, A, np.array([-0.87, 0.5]))]
        for (start, end, normal), lab, col in zip(edges, labels, colors):
            d = end - start
            arrow_pos = start + 0.35 * d
            ax.add_patch(FancyArrowPatch(arrow_pos, arrow_pos + 0.12 * d / np.linalg.norm(d),
                                         arrowstyle='-|>', mutation_scale=10, color=col, lw=1.2))
            lbl_pos = arrow_pos + normal * 0.09
            ax.text(lbl_pos[0], lbl_pos[1], lab, color=col, fontsize=fs,
                    ha='center', va='center')

    def scatter(self, fa, fb, fc, **kw):
        pts = [self.xy(a, b, c) for a, b, c in zip(np.atleast_1d(fa), np.atleast_1d(fb), np.atleast_1d(fc))]
        xs, ys = zip(*pts)
        return self.ax.scatter(xs, ys, **kw)

    def density(self, fa, fb, fc, cmap='Purples', levels=10, thresh=0.05, **kw):
        from scipy.stats import gaussian_kde
        P = np.array([self.xy(a, b, c) for a, b, c in zip(fa, fb, fc)])
        kde = gaussian_kde(P.T)
        xg, yg = np.meshgrid(np.linspace(-0.05, 1.05, 200), np.linspace(-0.05, self.H + 0.05, 200))
        Z = kde(np.vstack([xg.ravel(), yg.ravel()])).reshape(xg.shape)
        Zm = np.ma.masked_where(Z < thresh * Z.max(), Z)
        # 只画三角形内部: 给定 y → fa=y/H, x ∈ [0.5*fa, 1-0.5*fa]
        tri_mask = (yg < 0) | (xg < yg / (2 * self.H)) | (xg > 1 - yg / (2 * self.H))
        Zm = np.ma.masked_where(tri_mask, Zm)
        self.ax.contourf(xg, yg, Zm, levels=levels, cmap=cmap, **kw)
