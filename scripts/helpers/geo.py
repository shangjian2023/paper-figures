# -*- coding: utf-8 -*-
"""GeoJSON 地图助手 — 纯 matplotlib 画世界/中国地图(无 geopandas 依赖)。"""
import json
import os

import numpy as np
from matplotlib.patches import PathPatch
from matplotlib.path import Path

MAP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'map_data'))
WORLD = os.path.join(MAP_DIR, 'world.geo.json')
CHINA = os.path.join(MAP_DIR, 'china.geo.json')


def _poly_rings(geom):
    """从 geometry 提取所有外环(忽略内洞, 简化处理)。返回 [ [(lon,lat),...], ... ]"""
    if geom['type'] == 'Polygon':
        return [geom['coordinates'][0]]
    if geom['type'] == 'MultiPolygon':
        return [poly[0] for poly in geom['coordinates']]
    return []


def load_features(path):
    """返回 [(props, [ring1, ring2...]), ...]"""
    data = json.load(open(path, encoding='utf-8'))
    feats = []
    for f in data['features']:
        feats.append((f.get('properties', {}), _poly_rings(f['geometry'])))
    return feats


def mercator(lon, lat):
    x = np.radians(lon)
    y = np.log(np.tan(np.pi / 4 + np.radians(lat) / 2))
    return x, y


def draw_map(ax, features, facecolor_fn=None, edgecolor='white', lw=0.4,
             extent=None, projection='mercator'):
    """facecolor_fn(props) -> color 或 None(跳过)。extent=(lon0,lon1,lat0,lat1)"""
    for props, rings in features:
        fc = facecolor_fn(props) if facecolor_fn else '#DDDDDD'
        if fc is None:
            continue
        for ring in rings:
            arr = np.array(ring)
            if projection == 'mercator':
                pts = np.array([mercator(lo, la) for lo, la in arr])
            else:
                pts = arr[:, :2]
            verts = list(map(tuple, pts))
            codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 2) + [Path.CLOSEPOLY]
            if len(verts) < 3:
                continue
            ax.add_patch(PathPatch(Path(verts, codes), facecolor=fc,
                                   edgecolor=edgecolor, lw=lw, zorder=1))
    if extent:
        lon0, lon1, lat0, lat1 = extent
        if projection == 'mercator':
            x0, y0 = mercator(lon0, lat0)
            x1, y1 = mercator(lon1, lat1)
            ax.set_xlim(x0, x1)
            ax.set_ylim(y0, y1)
        else:
            ax.set_xlim(lon0, lon1)
            ax.set_ylim(lat0, lat1)
    ax.set_aspect('equal')
    ax.axis('off')


def world_map(ax, facecolor_fn=None, extent=(-180, 180, -60, 85), **kw):
    return draw_map(ax, load_features(WORLD), facecolor_fn, extent=extent, **kw)


def china_map(ax, facecolor_fn=None, extent=(73, 136, 16, 55), **kw):
    """中国省级地图(properties['name']=省名)。"""
    return draw_map(ax, load_features(CHINA), facecolor_fn, extent=extent, **kw)


def china_names():
    return [p['name'] for p, _ in load_features(CHINA) if 'name' in p]
