# -*- coding: utf-8 -*-
"""数据输入层 — load / validate / 适配器, 打通"用户数据 → 配方数据段"。

约定: 任何案例的数据接入都走这里, 三步:
    df  = load('data.csv')                      # 读 csv/tsv/xlsx/json
    report = validate(df, '005')                # 对照 reference/data-schemas.json 校验
    data = as_groups(df, 'group', 'value')      # 按配方形态适配(见下)

适配器(返回值直接赋给配方的数据变量):
    as_groups(df, group, value)     -> [np.array, ...]      每组一组值(bar/distribution/ridge)
    as_wide(df, index, cols...)     -> (labels, [np.array])  宽表按列分组
    as_xy(df, x, y, ...)            -> (x, y, group, label)  散点/曲线
    as_matrix(df, row, col, value)  -> (rows, cols, M)       热图/点阵
    as_edges(df)                    -> [(s, t, v), ...]      桑基/和弦/冲击
    as_ternary(df, fa, fb, fc)      -> (fa, fb, fc) 归一化   三元图
    as_sets(df, name, elements)     -> {集合名: set(...)}    UpSet
"""
import json
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
SCHEMAS = os.path.join(ROOT, 'reference', 'data-schemas.json')

# 允许技能安装在任意位置时向上/向旁探测 schemas
_FALLBACKS = [
    SCHEMAS,
    os.path.join(ROOT, 'catalog.json'),  # 占位: schema 文件缺失时报错用
]


def _schemas():
    for p in _FALLBACKS:
        if os.path.exists(p) and p.endswith('data-schemas.json'):
            return json.load(open(p, encoding='utf-8'))['schemas']
    # junction 安装副本: reference/ 同级
    alt = os.path.join(os.path.dirname(ROOT), 'reference', 'data-schemas.json')
    if os.path.exists(alt):
        return json.load(open(alt, encoding='utf-8'))['schemas']
    raise FileNotFoundError('data-schemas.json not found (run build_schemas.py)')


def load(path, **kw):
    """读 csv/tsv/txt/xlsx/xls/json → DataFrame。编码自动尝试 utf-8/gbk。"""
    ext = os.path.splitext(str(path))[1].lower()
    if ext in ('.csv', '.txt', '.tsv'):
        sep = '\t' if ext == '.tsv' else None
        for enc in ('utf-8-sig', 'utf-8', 'gbk'):
            try:
                return pd.read_csv(path, sep=sep, encoding=enc,
                                   engine='python' if sep is None else 'c', **kw)
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
        raise IOError('cannot decode %s' % path)
    if ext in ('.xlsx', '.xls'):
        return pd.read_excel(path, **kw)
    if ext == '.json':
        return pd.read_json(path, **kw)
    raise ValueError('unsupported: %s' % ext)


def schema(seg):
    return _schemas()['%03d' % int(seg)]


def validate(df, seg, max_missing=0.4, verbose=True):
    """对照案例 schema 校验 DataFrame。返回 report(dict); 有 error 时抛 AssertionError
    的同时也会在 report['errors'] 里给出(便于 agent 读取)。"""
    s = schema(seg)
    errors, warns = [], []
    for col in s['columns']:
        names = [col['name']] + col.get('aliases', [])
        hit = next((nm for nm in names if nm in df.columns), None)
        if hit is None:
            if col['required']:
                errors.append("missing column '%s' (%s)" % (col['name'], col['desc']))
            continue
        v = df[hit]
        miss = float(v.isna().mean())
        if miss > max_missing:
            errors.append("column '%s' has %.0f%% missing (>%.0f%%)" % (col['name'], miss * 100, max_missing * 100))
        t = col['type']
        if t == 'number' and miss < 1:
            try:
                pd.to_numeric(v.dropna())
            except Exception:
                errors.append("column '%s' is not numeric" % col['name'])
    if s['format'] == 'long' and any(c['name'] == 'group' for c in s['columns']):
        if 'group' in df.columns:
            k = df['group'].nunique()
            if k < 2:
                warns.append('group 列仅 %d 个取值(分组图通常 >=2)' % k)
    report = {'seg': '%03d' % int(seg), 'format': s['format'], 'rows': len(df),
              'errors': errors, 'warnings': warns, 'ok': not errors}
    if verbose:
        print('validate seg%s: %s (%d rows)' % (report['seg'], 'OK' if report['ok'] else 'FAIL', len(df)))
        for e in errors:
            print('  ERROR:', e)
        for w in warns:
            print('  warn :', w)
    return report


# ---------------- 适配器 ----------------
def as_groups(df, group='group', value='value', order=None):
    """长表 → [np.array, ...] 每组一组值(bar/distribution/ridge/box/violin)。"""
    g = df[group].astype(str)
    keys = order or list(pd.unique(g))
    return [pd.to_numeric(df.loc[g == k, value], errors='coerce').dropna().values for k in keys], keys


def as_wide(df, index_col=None):
    """宽表 → (行/组标签, [np.array,...])(每列一组)。index_col 给定时作为标签列。"""
    if index_col:
        labels = df[index_col].astype(str).values
        nums = df.drop(columns=[index_col])
    else:
        labels = list(df.columns)
        nums = df
    return labels, [pd.to_numeric(nums[c], errors='coerce').dropna().values for c in nums.columns]


def as_xy(df, x='x', y='y', group=None, label=None):
    """长表 → 散点/曲线四元组。"""
    X = pd.to_numeric(df[x], errors='coerce').values
    Y = pd.to_numeric(df[y], errors='coerce').values
    G = df[group].values if group else None
    L = df[label].values if label else None
    return X, Y, G, L


def as_matrix(df, row='row', col='col', value='value', agg='mean'):
    """长表 → 热图矩阵。返回 (row_labels, col_labels, M[np.array 2D])。"""
    p = df.pivot_table(index=row, columns=col, values=value, aggfunc=agg)
    return list(p.index), list(p.columns), p.values


def as_edges(df, source='source', target='target', value='value'):
    """边表 → [(s, t, v), ...](sankey/chord)。"""
    return [(r[source], r[target], float(r[value])) for _, r in df.iterrows()]


def as_ternary(df, fa, fb, fc):
    """三元长表 → 归一化 (fa, fb, fc) 各自 np.array(和=1)。"""
    A = pd.to_numeric(df[fa], errors='coerce').values
    B = pd.to_numeric(df[fb], errors='coerce').values
    C = pd.to_numeric(df[fc], errors='coerce').values
    S = A + B + C
    return A / S, B / S, C / S


def as_sets(df, name='set_name', elements='elements', sep=';'):
    """集合表 → {集合名: set(元素)}(UpSet)。"""
    return {str(r[name]): set(str(r[elements]).split(sep)) for _, r in df.iterrows()}


if __name__ == '__main__':
    # 自检: 造三个迷你数据集走 load→validate→适配器
    tmp = os.path.join(ROOT, 'gallery', '_smoke')
    os.makedirs(tmp, exist_ok=True)
    r = np.random.default_rng(0)
    # long 组比较
    df1 = pd.DataFrame({'group': ['Vehicle'] * 8 + ['Low'] * 8 + ['High'] * 8,
                        'value': np.r_[r.normal(1, .3, 8), r.normal(1.6, .3, 8), r.normal(2.2, .3, 8)]})
    p1 = os.path.join(tmp, '_demo_groups.csv')
    df1.to_csv(p1, index=False)
    d = load(p1)
    rep = validate(d, 5)  # 云雨图 schema(long: group,value)
    g, keys = as_groups(d)
    assert len(g) == 3 and all(len(x) == 8 for x in g)
    # matrix 相关阵
    df2 = pd.DataFrame({'row': ['A'] * 3 + ['B'] * 3, 'col': list('XYZ') * 2,
                        'value': [.9, .2, .1, .2, .8, .3]})
    p2 = os.path.join(tmp, '_demo_matrix.csv')
    df2.to_csv(p2, index=False)
    d2 = load(p2)
    validate(d2, 19)
    rows, cols, M = as_matrix(d2)
    assert M.shape == (2, 3)
    # edges 桑基
    df3 = pd.DataFrame({'source': ['ZT0', 'ZT0', 'ZT6'], 'target': ['GeneA', 'GeneB', 'GeneA'],
                        'value': [25, 15, 10]})
    p3 = os.path.join(tmp, '_demo_edges.csv')
    df3.to_csv(p3, index=False)
    d3 = load(p3)
    validate(d3, 45)
    E = as_edges(d3)
    assert len(E) == 3
    # 三元
    df4 = pd.DataFrame({'fa': [40, 20], 'fb': [30, 50], 'fc': [30, 30]})
    fa, fb, fc = as_ternary(df4, 'fa', 'fb', 'fc')
    assert np.allclose(fa + fb + fc, 1)
    # sets
    df5 = pd.DataFrame({'set_name': ['D1_Apo', 'D2_Apo'], 'elements': ['a;b;c', 'b;c;d']})
    S = as_sets(df5)
    assert S['D1_Apo'] == {'a', 'b', 'c'}
    for p in (p1, p2, p3):
        os.remove(p)
    print('DATA IO SELF-TEST OK')
