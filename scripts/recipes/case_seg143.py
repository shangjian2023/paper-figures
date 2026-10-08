# -*- coding: utf-8 -*-
"""案例148 (seg143) - 真3D双层悬空地图 (mpl_toolkits.mplot3d):
底层径流 YlOrRd (z=0 平面 Poly3DCollection) + 上层降雨 Blues 悬空 (z=1),
立方体坐标框只留三条轴, view_init(22, -55) 接近参考视角,
2×2 四面板(a-d 各一场事件), 右侧两条竖色标(Rainfall / Runoff, 0-1)。
参考: frames/seg_143.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

set_style()

LON0, LON1, LAT0, LAT1 = 115.0, 120.0, 29.0, 35.0
NX, NY = 12, 10
DX, DY = (LON1 - LON0) / NX, (LAT1 - LAT0) / NY
Z_RAIN, Z_RUN = 1.0, 0.0                 # 上层降雨悬空, 底层径流贴地

panels = [('a  2020-06-21  P: 0-45 mm', 0), ('b  2020-07-05  P: 30-95 mm', 1),
          ('c  2020-07-17  P: 55-140 mm', 2), ('d  2020-08-15  P: 10-70 mm', 3)]

fig = plt.figure(figsize=cm2in(19, 15))
r0 = rng(143)

cmap_rain = plt.cm.Blues
cmap_run = plt.cm.YlOrRd


def trim_islands(fld, min_nb=2):
    """剔除孤立网格(正交邻居数 < min_nb), 避免游离单格。"""
    keep = ~np.isnan(fld)
    out = np.full_like(fld, np.nan)
    for iy in range(NY):
        for ix in range(NX):
            if not keep[iy, ix]:
                continue
            nb = 0
            for yy, xx in ((iy + 1, ix), (iy - 1, ix), (iy, ix + 1), (iy, ix - 1)):
                if 0 <= yy < NY and 0 <= xx < NX and keep[yy, xx]:
                    nb += 1
            if nb >= min_nb:
                out[iy, ix] = fld[iy, ix]
    return out


# 每场降雨/径流场(高斯团块, 低于噪声化阈值的网格留空 → 不规则团簇轮廓)
rain_flds, run_flds = [], []
for p in range(4):
    cx, cy = r0.uniform(LON0 + 1, LON1 - 1), r0.uniform(LAT0 + 1.2, LAT1 - 1.2)
    gx, gy = np.meshgrid(np.linspace(LON0, LON1, NX), np.linspace(LAT0, LAT1, NY))
    rain = np.exp(-((gx - cx) ** 2 + (gy - cy) ** 2) / 4.5) * r0.uniform(0.75, 1.0)
    rain += r0.uniform(0, 0.18, (NY, NX))
    rain = (rain - rain.min()) / (rain.max() - rain.min() + 1e-9)
    runoff = np.roll(rain, (2, -1)) * 0.85 + 0.1 * r0.random((NY, NX))
    runoff = (runoff - runoff.min()) / (runoff.max() - runoff.min() + 1e-9)
    thr = 0.14 + 0.12 * r0.random((NY, NX))       # 锯齿化团簇边界
    rain = np.where(rain > thr, rain, np.nan)
    runoff = np.where(runoff > thr, runoff, np.nan)
    rain_flds.append(trim_islands(rain))
    run_flds.append(trim_islands(runoff))

cmap_rain = plt.cm.Blues
cmap_run = plt.cm.YlOrRd


def layer_quads(ax, fld, z, cmap, edge):
    """每网格单元一个四边形的 3D 平面层(无效网格跳过)。"""
    verts, cols = [], []
    for iy in range(NY):
        for ix in range(NX):
            v = fld[iy, ix]
            if np.isnan(v):
                continue
            x0, y0 = LON0 + ix * DX, LAT0 + iy * DY
            verts.append([(x0, y0, z), (x0 + DX, y0, z),
                          (x0 + DX, y0 + DY, z), (x0, y0 + DY, z)])
            cols.append(cmap(v))
    pc = Poly3DCollection(verts, facecolors=cols, edgecolors=edge,
                          linewidths=0.3, shade=False)
    ax.add_collection3d(pc)


def panel(ax, rain, runoff, title):
    layer_quads(ax, runoff, Z_RUN, cmap_run, '#B84A20')
    layer_quads(ax, rain, Z_RAIN, cmap_rain, '#4A7BA6')
    # 立方体坐标框: 只留三条轴
    ax.set_xlim(LON0, LON1)
    ax.set_ylim(LAT0, LAT1)
    ax.set_zlim(0, 1.3)
    ax.set_xticks(range(115, 121))
    ax.set_xticklabels(['115', '116', '117', '118', '119', '120'], fontsize=5)
    ax.set_yticks([29, 31, 33, 35])
    ax.set_yticklabels(['29', '31', '33', '35'], fontsize=5)
    ax.set_zticks([])
    ax.set_xlabel('Longitude (°E)', fontsize=6, labelpad=-6)
    ax.set_ylabel('Latitude (°N)', fontsize=6, labelpad=-6)
    ax.set_zlabel('Rainfall / Runoff', fontsize=6, labelpad=-2)
    ax.view_init(elev=22, azim=-55)
    ax.set_box_aspect((1.0, 1.1, 0.55))
    ax.set_title(title, fontsize=7, loc='left', pad=1)
    ax.tick_params(pad=-1)
    # pane 白/浅灰, 网格线淡
    for axx in (ax.xaxis, ax.yaxis, ax.zaxis):
        axx.set_pane_color((0.975, 0.975, 0.975, 1.0))
        axx.pane.set_edgecolor('#CCCCCC')
        axx.pane.set_linewidth(0.5)
        axx._axinfo['grid'].update(color='#E6E6E6', linewidth=0.4)


for k, (title, p) in enumerate(panels):
    ax = fig.add_subplot(2, 2, k + 1, projection='3d')
    panel(ax, rain_flds[p], run_flds[p], title)

# 右侧两条竖色标: 明确标注"全局共享、对应哪一层", 否则各面板另一半色块不可解码
sm_r = ScalarMappable(norm=Normalize(0, 1), cmap=cmap_rain)
sm_o = ScalarMappable(norm=Normalize(0, 1), cmap=cmap_run)
cax1 = fig.add_axes([0.925, 0.56, 0.012, 0.33])
cb1 = fig.colorbar(sm_r, cax=cax1)
cb1.set_ticks([0, 1])
cb1.ax.tick_params(labelsize=6)
cb1.set_label('Rainfall (upper layer, all panels)', fontsize=6.5, labelpad=1)
cax2 = fig.add_axes([0.925, 0.12, 0.012, 0.33])
cb2 = fig.colorbar(sm_o, cax=cax2)
cb2.set_ticks([0, 1])
cb2.ax.tick_params(labelsize=6)
cb2.set_label('Runoff (lower layer, all panels)', fontsize=6.5, labelpad=1)
fig.text(0.9315, 0.505, 'shared by a-d', rotation=90, fontsize=5.8,
         ha='center', va='center', color='0.35')

fig.subplots_adjust(left=0.04, right=0.90, top=0.94, bottom=0.05,
                    wspace=0.02, hspace=0.10)
save(fig, 'case_seg143.png')
