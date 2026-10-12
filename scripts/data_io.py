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
import csv
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
        for enc in ('utf-8-sig', 'utf-8', 'gbk', 'utf-16'):
            try:
                return pd.read_csv(path, sep=sep, encoding=enc,
                                   engine='python' if sep is None else 'c', **kw)
            except (UnicodeDecodeError, pd.errors.ParserError, UnicodeError):
                continue
        raise IOError("cannot decode %s (若来自 PowerShell 'Unicode' 导出请另存为 UTF-8)" % path)
    if ext in ('.xlsx', '.xls'):
        xls = pd.ExcelFile(path, **kw)
        df = xls.parse(xls.sheet_names[0])
        df.attrs['sheet_names'] = xls.sheet_names   # 供 validate 在缺列时提示"数据可能在其他表"
        return df
    if ext == '.json':
        import json as _json
        with open(path, encoding='utf-8-sig') as f:
            head = _json.load(f)
        if isinstance(head, dict) and any(isinstance(v, (list, dict)) for v in head.values()):
            raise IOError('嵌套 JSON(dict 套 list/dict)，请先展平成"一行一观测"的 CSV 长表: %s' % path)
        return pd.read_json(path, **kw)
    if ext in ('.dta', '.sav', '.rds', '.h5', '.hdf5'):
        raise ValueError('统计软件格式 %s: 请先在原软件(SPSS/Stata/R)导出为 CSV 再导入' % ext)
    raise ValueError('unsupported: %s' % ext)


def schema(seg):
    return _schemas()['%03d' % int(seg)]


def validate(df, seg, max_missing=0.4, verbose=True):
    """对照案例 schema 校验 DataFrame。返回 report(dict); 有 error 时抛 AssertionError
    的同时也会在 report['errors'] 里给出(便于 agent 读取)。

    除列存在性/缺失率/数值性外, 按格式做结构检查(造得出图 ≠ 画得对):
      edges   值必须 >0(和弦/桑基的带宽), 自环与重复 (s,t) 告警
      matrix  (row,col) 重复告警(会 silently 被 agg 平均), 行列数 <2 告警
      xy      x/y NaN 计数告警, 有效点 <3 告警
      long    group 取值 <2 告警, 任一组样本 <3 告警
      三元列(fa/fb/fc, 按列名或别名如 TE/EPI/PrE 识别)负值→error, 零和行→error"""
    s = schema(seg)
    errors, warns = [], []
    if len(df) == 0:
        errors.append('数据为空(0 行), 请检查导出/筛选条件')
        report = {'seg': '%03d' % int(seg), 'format': s['format'], 'rows': 0,
                  'errors': errors, 'warnings': warns, 'ok': False}
        if verbose:
            print('validate seg%s: FAIL (0 rows)' % report['seg'])
            for e in errors:
                print('  ERROR:', e)
        return report
    hits = {}   # schema 列名 → 实际列名(含别名命中)
    for col in s['columns']:
        names = [col['name']] + col.get('aliases', [])
        hit = next((nm for nm in names if nm in df.columns), None)
        hits[col['name']] = hit
        if hit is None:
            if col['required']:
                errors.append("missing column '%s' (%s)——中文表头请重命名或对照 desc 找同义列"
                              % (col['name'], col['desc']))
            continue
        v = df[hit]
        miss = float(v.isna().mean())
        if miss > max_missing:
            errors.append("column '%s' has %.0f%% missing (>%.0f%%)" % (col['name'], miss * 100, max_missing * 100))
        t = col['type']
        if t == 'number' and miss < 1:
            try:
                num = pd.to_numeric(v.dropna())
                n_inf = int(np.isinf(num).sum())
                if n_inf:
                    warns.append("column '%s' 含 ±Inf 值 %d 个(多为除零/导出错误), 画图前请清洗"
                                 % (col['name'], n_inf))
            except Exception:
                errors.append("column '%s' is not numeric——常见成因: 逗号小数点(1,5)/百分号(85%%)/"
                              "千分位(1,234)/货币符($3.2)，请先清洗" % col['name'])
    fmt = s['format']

    def _num(colname):
        hit = hits.get(colname)
        return pd.to_numeric(df[hit], errors='coerce') if hit else None

    # 结构检查按"角色列是否存在"触发(schema 里散点也是 long+xy 列, 不能只看 format)
    if hits.get('x') and hits.get('y'):          # 坐标表
        X, Y = _num('x'), _num('y')
        bad = int((X.isna() | Y.isna()).sum())
        if bad:
            warns.append('%d 行 x/y 坐标非数值, 画图时将被丢弃' % bad)
        ok = int((X.notna() & Y.notna()).sum())
        if ok < 3:
            errors.append('有效坐标点仅 %d 个(<3), 撑不起散点/曲线' % ok)
    elif hits.get('group') and fmt == 'long':    # 分组长表(散点的 group 可选, 不在此列)
        g = df[hits['group']].astype(str)
        k = g.nunique()
        if k < 2:
            warns.append('group 列仅 %d 个取值(分组图通常 >=2)' % k)
        cnt = g.value_counts()
        small = cnt[cnt < 3]
        if len(small):
            warns.append('组样本量 <3: %s(画分布/误差棒不可靠)' %
                         ', '.join('%s=%d' % kv for kv in small.items()))
    if hits.get('row') and hits.get('col'):      # 矩阵长表
        r, c = df[hits['row']].astype(str), df[hits['col']].astype(str)
        dup = int(df.duplicated(subset=[hits['row'], hits['col']]).sum())
        if dup:
            warns.append('%d 个重复 (row,col) 格, 将被均值聚合(确认是否本意)' % dup)
        if r.nunique() < 2 or c.nunique() < 2:
            warns.append('矩阵仅 %d 行 x %d 列(热图通常各 >=2)' % (r.nunique(), c.nunique()))
    if hits.get('source') and hits.get('target') and hits.get('value'):   # 边表
        V = _num('value')
        nonpos = int((V <= 0).sum())
        if nonpos:
            errors.append("%d 条边 value<=0(和弦/桑基的带必须为正)" % nonpos)
        pair = df[hits['source']].astype(str) + '\x00' + df[hits['target']].astype(str)
        dup = int(pair.duplicated().sum())
        if dup:
            warns.append('%d 条重复 (source,target) 边, 将叠加/取后(确认是否本意)' % dup)
        self_loops = int((df[hits['source']].astype(str) == df[hits['target']].astype(str)).sum())
        if self_loops:
            warns.append('%d 条自环边(source==target), 多数图型画不出' % self_loops)
    if hits.get('elements'):                     # 集合表
        el = df[hits['elements']].astype(str).str.replace(' ', '')
        empty = int((el == '').sum() + (el == 'nan').sum())
        if empty:
            warns.append('%d 个集合的 elements 为空' % empty)

    # 三元构成(fa/fb/fc 角色, 按列名或别名识别, 如 TE/EPI/PrE): 负值与零和行是硬错误
    role = {}
    for col in s['columns']:
        nm_set = {col['name']} | set(col.get('aliases', []))
        for r in ('fa', 'fb', 'fc'):
            if r in nm_set:
                role[r] = hits[col['name']]
    if all(role.get(r) for r in ('fa', 'fb', 'fc')):
        A, B, C = (pd.to_numeric(df[role[r]], errors='coerce') for r in ('fa', 'fb', 'fc'))
        if any(int((M < 0).sum()) for M in (A, B, C)):
            errors.append('三元列存在负值(构成不能为负)')
        zero_rows = int(((A + B + C) <= 0).sum())
        if zero_rows:
            errors.append('%d 行三元和<=0(无法归一化)' % zero_rows)
        over100 = int(((A + B + C) > 100.5).sum())
        if over100:
            warns.append('%d 行三元和>100, 将按行重新归一化(确认原始数据是否本该是百分数)' % over100)

    sheets = getattr(df, 'attrs', {}).get('sheet_names')
    if sheets and len(sheets) > 1 and any('missing column' in e for e in errors):
        errors.insert(0, '该工作簿有 %d 个工作表(%s…)，数据可能在其他表；公式列请先在 Excel 中存为值'
                      % (len(sheets), '、'.join(sheets[:3])))
    report = {'seg': '%03d' % int(seg), 'format': fmt, 'rows': len(df),
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
    """长表 → [np.array, ...] 每组一组值(bar/distribution/ridge/box/violin)。
    数值清洗丢弃率 >50% 时打印告警(绕过 validate 直接适配的防线)。"""
    g = df[group].astype(str)
    keys = order or list(pd.unique(g))
    out = []
    for k in keys:
        raw = df.loc[g == k, value]
        v = pd.to_numeric(raw, errors='coerce').dropna().values
        if len(raw) and len(v) < len(raw) * 0.5:
            print("warn: 列 '%s' 组 '%s' 有 %d/%d 个值无法转数值被丢弃(检查百分号/千分位/单位)"
                  % (value, k, len(raw) - len(v), len(raw)))
        out.append(v)
    return out, keys


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

    # ---- 负例: 坏数据必须被 validate 拦下 ----
    def _fails(df, seg, *must):
        rep = validate(df, seg, verbose=False)
        blob = ' | '.join(rep['errors'] + rep['warnings'])
        for m in must:
            assert m in blob, 'expect %r in report, got: %s' % (m, blob)
        return rep
    # 缺必需列 + 非数值
    _fails(pd.DataFrame({'group': ['A', 'B']}), 5, "missing column 'value'")
    _fails(pd.DataFrame({'group': ['A'] * 4 + ['B'] * 4,
                         'value': ['x', 'y', 'z', 'w', 1, 2, 3, 4]}), 5, 'not numeric')
    # 组样本量不足(warn)
    _fails(pd.DataFrame({'group': ['A'] * 2 + ['B'] * 2, 'value': [1, 2, 3, 4]}), 5, '样本量 <3')
    # edges: 值<=0 是硬错误; 自环/重复是告警
    _fails(pd.DataFrame({'source': ['A', 'A', 'B'], 'target': ['B', 'B', 'B'],
                         'value': [5, 0, -1]}), 45, 'value<=0')
    # matrix: 重复格(warn)
    _fails(pd.DataFrame({'row': ['A', 'A'], 'col': ['X', 'X'], 'value': [1, 2]}),
           19, '重复 (row,col) 格')
    # xy: NaN 坐标(warn) 与有效点过少(error)
    _fails(pd.DataFrame({'x': [1, np.nan, 3, 4, 5, 6], 'y': [1, 2, 3, np.nan, 5, 6]}),
           61, '坐标非数值')
    rep = _fails(pd.DataFrame({'x': [1, np.nan], 'y': [2, np.nan]}), 61, '有效坐标点仅 1 个')
    assert not rep['ok']
    # 三元(schema 124: TE/EPI/PrE 带别名): 负值与零和都是硬错误
    _fails(pd.DataFrame({'TE': [-10, 40], 'EPI': [30, 30], 'PrE': [30, 30]}), 124, '负值')
    _fails(pd.DataFrame({'TE': [0, 40], 'EPI': [0, 30], 'PrE': [0, 30]}), 124, '三元和<=0')
    # 好数据在 124 上应 OK
    ok_rep = validate(pd.DataFrame({'TE': [40, 20], 'EPI': [30, 50], 'PrE': [30, 30]}),
                      124, verbose=False)
    assert ok_rep['ok'], ok_rep['errors']
    print('NEGATIVE-CASE SELF-TEST OK')
