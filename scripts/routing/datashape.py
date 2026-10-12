# -*- coding: utf-8 -*-
"""数据画像软约束层(R5, 依 _research_nl2vis.md Top2 精简版):

--data 给了数据文件时, 除 schema 契约校验外, 再算最小画像, 给"数据形状暗示"的
图型家族温和加分。只做三条最可靠的规则(DeepEye/SeeDB 思想的轻量版):
  1. 数值行和 ≈ 100 → 构成占比类 +0.5
  2. 列名带 时间/日期/date/时间点 且数值可排序 → 趋势变化类 +0.4
  3. 组列取值数 2-8 且组内样本 >=3 → 组间比较类 +0.3
"""
import re
import pandas as pd


def profile_dataframe(df):
    """最小数据画像。"""
    f = {'rows': len(df), 'cols': len(df.columns)}
    num = df.select_dtypes('number')
    f['n_numeric'] = len(num.columns)
    # 规则1: 行和≈100 或 ≈1 → 构成
    if 2 <= f['n_numeric'] <= 30 and len(num):
        s = num.sum(axis=1)
        f['rowsum_100'] = bool(((s - 100).abs() <= 0.5).mean() > 0.8)
        f['rowsum_1'] = bool(((s - 1).abs() <= 0.005).mean() > 0.8)
    else:
        f['rowsum_100'] = f['rowsum_1'] = False
    # 规则2: 时间列
    time_like = [c for c in df.columns
                 if isinstance(c, str) and re.search(r'时间|日期|time|date|hour|month|day|周|月|年', c, re.I)]
    f['has_time_col'] = bool(time_like)
    # 规则3: 组列(取值 2-8 的非数值列)与组内样本量
    f['group_col'] = None
    f['min_group_n'] = None
    for c in df.columns:
        if c in num.columns:
            continue
        k = df[c].nunique()
        if 2 <= k <= 8:
            f['group_col'] = str(c)
            f['min_group_n'] = int(df[c].value_counts().min())
            break
    return f


def shape_boosts(feat, purposes_map):
    """画像 → {seg: 加分}。purposes_map: {'005': [用途...]}。"""
    out = {}
    if not feat:
        return out
    comp = feat.get('rowsum_100') or feat.get('rowsum_1')
    for seg, purs in purposes_map.items():
        b = 0.0
        if comp and '构成占比' in purs:
            b += 0.5
        if feat.get('has_time_col') and '趋势变化' in purs:
            b += 0.4
        if feat.get('group_col') and (feat.get('min_group_n') or 0) >= 3 and '组间比较' in purs:
            b += 0.3
        if b:
            out[int(seg)] = b
    return out


def infer_scenarios(df):
    """数据画像 → 场景推断: {用途词: (置信度0-1, 证据人话)}。

    规则按 DeepEye/data-to-viz 思想精简为"看列结构就能定"的七条,
    供推荐模式在用户说不出图型名时给出起点。"""
    import re as _re
    f = profile_dataframe(df)
    sc = {}
    num_cols = df.select_dtypes('number')
    obj_cols = [c for c in df.columns if c not in num_cols.columns]
    f['n_obj'] = len(obj_cols)
    # 反指比对用的槽位: 最大类别基数 / 组数 / 组均值跨度比
    f['max_obj_card'] = max((df[c].nunique() for c in obj_cols), default=0)
    if f.get('group_col'):
        f['group_nunique'] = int(df[f['group_col']].nunique())

    # 1) 组列 + 单数值 → 组间比较 / 分布形态
    if f.get('group_col') and f['n_numeric'] >= 1:
        gcol = f['group_col']
        k = df[gcol].nunique()
        n_per = int(df[gcol].value_counts().min())
        if n_per >= 15:
            sc['分布形态'] = (0.9, '%s 共 %d 组、每组约 %d 个观测，能撑起分布轮廓' % (gcol, k, n_per))
        if 2 <= k <= 12:
            sc['组间比较'] = (0.85, '%s 有 %d 组、每组 %d 个数值' % (gcol, k, n_per))
        # 配对信号: 列名/组名含前后语义
        joined = ' '.join(str(x) for x in df[gcol].unique()[:12])
        if _re.search(r'前|后|pre|post|before|after|treatment|ctrl|对照|处理', joined, _re.I):
            sc.setdefault('组间比较', (0.85, '%s 有 %d 组（含对照/处理语义，可能可配对）' % (gcol, k)))
    # 2) 时间列 → 趋势变化
    if f.get('has_time_col'):
        sc['趋势变化'] = (0.8, '存在时间/浓度类自变量列，适合看随时间的变化')
    # 3) 行和≈100 或 ≈1 → 构成占比
    if f.get('rowsum_100') or f.get('rowsum_1'):
        sc['构成占比'] = (0.85, '每行数值加起来≈100%%，是典型的构成/占比表')
    # 4) 2-3 个数值列 → 相关关系
    if 2 <= f['n_numeric'] <= 3 and f['rows'] >= 5:
        sc['相关关系'] = (0.7, '%d 个数值列，可以看两两之间的关系' % f['n_numeric'])
    # 5) 大量数值列(>=5) → 多指标综合 / 热图
    if f['n_numeric'] >= 5 and f['rows'] <= 60:
        sc['多指标综合'] = (0.6, '%d 个数值列 × %d 行，像一张"指标×条目"表' % (f['n_numeric'], f['rows']))
        sc['相关关系'] = (0.6, '%d 个数值列两两做相关也常见' % f['n_numeric'])
    # 6) 三列结构 source/target/value → 流向
    low = [str(c).lower() for c in df.columns]
    if len(df.columns) >= 3 and any('source' in c or '来源' in c for c in low)             and any('target' in c or '目标' in c or '去向' in c for c in low):
        sc['网络与流向'] = (0.9, '存在 来源→去向→数值 三列结构，是标准的流量表')
    # 7) 长表 row/col/value → 矩阵/热图
    if f.get('n_obj', 0) >= 2 and f['n_numeric'] == 1 and f['rows'] >= 8             and df[obj_cols[0]].nunique() >= 3 and df[obj_cols[-1]].nunique() >= 3:
        sc.setdefault('相关关系', (0.55, '两列文本 × 一列数值的长表，可透视成矩阵'))
    return f, sc
