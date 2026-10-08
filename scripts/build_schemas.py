# -*- coding: utf-8 -*-
"""数据输入 Schema 生成器: 按 family 模板 + 特殊 case override,
为 catalog 全部 146 案例生成机器可读的输入数据契约 → reference/data-schemas.json。

schema 结构:
{
  "<seg>": {
    "case": "案例1", "title": "...", "family": "bar",
    "format": "long",                    # long|wide|matrix|edges|ternary|xy|tree|newick|geo
    "columns": [ {"name":"group","type":"category","required":true,"desc":"..."} ...],
    "notes": "...",                       # 组数/重复数/值域等约束
    "source_text": "<catalog.data 原文>"  # 供 agent 对照语义
  }
}
用法: python scripts/build_schemas.py   # 重新生成(手工 override 写在本文件 OVERRIDES)
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

# ---- family 级模板: (format, columns, note_tpl)
def _c(name, typ, desc, required=True, aliases=None):
    d = {'name': name, 'type': typ, 'required': required, 'desc': desc}
    if aliases:
        d['aliases'] = aliases
    return d

FAMILY_TPL = {
    'bar': ('long', [
        _c('group', 'category', '分组/处理名'),
        _c('value', 'number', '测量值'),
        _c('pair_id', 'string', '配对个体 ID(配对图必填)', False),
    ], '2-8 组, 每组 n>=3; 若做显著性需对照组'),
    'distribution': ('long', [
        _c('group', 'category', '分组/细胞类型/物种'),
        _c('value', 'number', '单观测值(分布原始值, 非统计量)'),
    ], '每组 n>=30 才能撑起 KDE; 小样本请走 bar 家族'),
    'scatter': ('long', [
        _c('x', 'number', '自变量'),
        _c('y', 'number', '因变量'),
        _c('group', 'category', '系列/分组', False),
        _c('label', 'string', '点标注(基因名等, 仅重点点需要)', False),
        _c('xerr', 'number', 'x 误差', False),
        _c('yerr', 'number', 'y 误差', False),
    ], ''),
    'curve': ('long', [
        _c('time', 'number', '时间/浓度/频率(自变量)'),
        _c('value', 'number', '响应值'),
        _c('group', 'category', '系列'),
        _c('err', 'number', 'SEM/CI 半宽', False),
    ], '时序类每组 5-20 个时间点'),
    'heatmap': ('matrix', [
        _c('row', 'string', '行标签(基因/代谢物/变量)'),
        _c('col', 'string', '列标签(细胞类型/样本/变量)'),
        _c('value', 'number', '矩阵值(相关系数/表达/能量)'),
        _c('pvalue', 'number', '显著性 p 值(星号点阵用)', False),
    ], '矩阵维度按案例 notes; 相关矩阵需对称'),
    'volcano': ('long', [
        _c('feature', 'string', '基因/蛋白/代谢物名'),
        _c('log2fc', 'number', 'log2 倍数变化'),
        _c('pvalue', 'number', 'p 值(或已换算的 -log10p)'),
        _c('label', 'string', '重点标注名(仅关键基因)', False),
        _c('group', 'category', '分面/比较组(多组火山用)', False),
    ], 'rows>=1000 观感最佳; 标注基因 5-40 个'),
    'ridge': ('long', [
        _c('row', 'category', '山脊行(亚群/时间点/标记)'),
        _c('value', 'number', '单观测值'),
        _c('facet', 'category', '分面列(标记/条件)', False),
    ], '每行 n>=100'),
    'flow': ('edges', [
        _c('source', 'string', '源节点'),
        _c('target', 'string', '目标节点'),
        _c('value', 'number', '流量/权重'),
    ], '桑基/和弦/冲击图共用边表; UpSet 用 sets 列表(见 notes)'),
    'polar': ('long', [
        _c('axis', 'category', '角度轴(指标/组织/城市)'),
        _c('series', 'category', '系列(处理/分组)', False),
        _c('value', 'number', '径向值'),
        _c('sig', 'string', '显著性字母/星号', False),
    ], ''),
    'tree_geo': ('long', [
        _c('name', 'string', '地点/类群名'),
        _c('lon', 'number', '经度', False),
        _c('lat', 'number', '纬度', False),
        _c('value', 'number', '数量/丰度', False),
        _c('composition', 'string', '构成(如 A:B:C=5:3:2)', False),
    ], '地图类需 lon/lat 或国家/省名; 发育树类另备 Newick 文件'),
}

# ---- 特殊 case override(与 family 模板不同形的知名案例)
SPECIAL = {
    2: ('xy', [_c('PC1', 'number', 'PCo1 得分'), _c('PC2', 'number', 'PCo2 得分'),
               _c('group', 'category', '分组')], '排序图: 附各轴解释率于列名或 notes'),
    3: ('xy', [_c('PC1', 'number', 'PCo1'), _c('PC2', 'number', 'PCo2'),
               _c('group', 'category', 'control/IBD'), _c('study', 'category', '研究来源')], ''),
    12: ('newick', [_c('newick', 'string', 'Newick 树文件路径')], '另需每叶注释长表: leaf,phylum,type,...'),
    13: ('newick', [_c('newick', 'string', 'Newick 树文件路径')], '另需每叶注释长表'),
    14: ('newick', [_c('newick', 'string', 'Newick 树文件路径')], '另需每叶注释长表'),
    15: ('newick', [_c('newick', 'string', 'Newick 树文件路径')], '另需每叶注释长表'),
    20: ('long', [_c('x', 'number', '基因组总大小(bp)'), _c('y', 'number', 'CDS 数'),
                  _c('group', 'category', 'SAG/MAG/WGS')], 'log-log 轴, n≈5000'),
    21: ('long', [_c('x', 'number', '基因组总大小(bp)'), _c('y', 'number', 'CDS 数'),
                  _c('group', 'category', 'SAG/MAG/WGS')], 'log-log 轴, n≈5000'),
    27: ('edges', [_c('source', 'string', '源'), _c('target', 'string', '目标'),
                   _c('value', 'number', '流量')], '和弦图: 方阵亦可, 行=源'),
    28: ('long', [_c('feature', 'string', '基因'), _c('log2fc', 'number', 'log2FC'),
                  _c('padj', 'number', '校正 p')], '另需基因集成员表(gene, set, direction)'),
    36: ('long', [_c('feature', 'string', '基因'), _c('log2fc_a', 'number', '处理 A log2FC'),
                  _c('log2fc_b', 'number', '处理 B log2FC'),
                  _c('sig_a', 'number', 'A 显著(0/1)', False),
                  _c('sig_b', 'number', 'B 显著(0/1)', False)], 'FC-FC 类共用此形'),
    37: ('long', [_c('feature', 'string', '基因'), _c('log2fc_a', 'number', 'log2FC A'),
                  _c('log2fc_b', 'number', 'log2FC B'),
                  _c('p_a', 'number', 'A 的 p', False), _c('p_b', 'number', 'B 的 p', False)], ''),
    43: ('long', [_c('x', 'number', '变量 1'), _c('y', 'number', '变量 2'),
                  _c('group', 'category', '组别')], '联合密度: 每组数百点'),
    45: ('edges', [_c('source', 'string', '源(时间点)'), _c('target', 'string', '目标(基因)'),
                    _c('value', 'number', '带宽值')], '三层桑基: 两个边表(层1→2, 层2→3)'),
    46: ('edges', [_c('source', 'string', '源'), _c('target', 'string', '目标'),
                    _c('value', 'number', '占比')], '四层桑基: 三个边表'),
    91: ('edges', [_c('source', 'string', '源'), _c('target', 'string', '目标'),
                    _c('value', 'number', '计数')], '冲击图: 各流标 n'),
    114: ('sets', [_c('set_name', 'string', '集合名'), _c('elements', 'string', '元素列表(分号分隔)')],
          'UpSet 输入: 每行一个集合'),
    115: ('sets', [_c('set_name', 'string', '集合名'), _c('elements', 'string', '元素列表(分号分隔)')], ''),
    116: ('long', [_c('term', 'string', '目/类目'), _c('log2fc', 'number', 'log2FC'),
                   _c('abundance', 'number', '丰度(气泡大小)'),
                   _c('group', 'category', '比较组(分层面板)')], ''),
    124: ('long', [_c('TE', 'number', '顶点 TE(上)', True, ['fa']), _c('EPI', 'number', '顶点 EPI(左下)', True, ['fb']),
                   _c('PrE', 'number', '顶点 PrE(右下)', True, ['fc']), _c('group', 'category', '归属/分期', False)],
          '三元图: 三分量和为 100(或 1, 自动归一)'),
    125: ('long', [_c('TH1', 'number', '顶点 TH1', True, ['fa']), _c('TH2', 'number', '顶点 TH2', True, ['fb']),
                   _c('TH17', 'number', '顶点 TH17', True, ['fc']), _c('group', 'category', 'Young/Older')], ''),
    126: ('long', [_c('TH1', 'number', '顶点 TH1', True, ['fa']), _c('TH2', 'number', '顶点 TH2', True, ['fb']),
                   _c('TH17', 'number', '顶点 TH17', True, ['fc']), _c('age', 'number', '年龄(着色)')], ''),
    127: ('long', [_c('Nodule', 'number', '顶点 Nodule', True, ['fa']), _c('Root', 'number', '顶点 Root', True, ['fb']),
                   _c('Rhizosphere', 'number', '顶点 Rhizosphere', True, ['fc']), _c('size', 'number', '丰度(气泡)'),
                   _c('enriched', 'category', '富集生境/灰色', False)], ''),
    128: ('long', [_c('Control', 'number', '顶点 Control', True, ['fa']), _c('NPK', 'number', '顶点 NPK', True, ['fb']),
                   _c('NPKM', 'number', '顶点 NPKM', True, ['fc']), _c('size', 'number', '丰度'),
                   _c('genus', 'category', '属(着色)')], ''),
    129: ('long', [_c('ISC_TA', 'number', '顶点 ISC/TA', True, ['fa']), _c('Diff_int', 'number', '顶点 Diff.int.', True, ['fb']),
                   _c('Non_canonical', 'number', '顶点 Non-canonical', True, ['fc'])], '三元 KDE: n>=200'),
    132: ('long', [_c('freq', 'number', '频率'), _c('value', 'number', '摩尔体积'),
                   _c('temp', 'number', '温度(K, 系列色)')], 'log x 曲线族'),
    134: ('xy', [_c('umap_1', 'number', 'UMAP1'), _c('umap_2', 'number', 'UMAP2'),
                 _c('celltype', 'category', '细胞类型'),
                 _c('timepoint', 'category', '时间点', False),
                 _c('condition', 'category', '条件', False)], 'UMAP 类共用'),
    137: ('long', [_c('patient', 'string', '患者 ID'), _c('start', 'number', '起点(天)'),
                   _c('end', 'number', '终点(天)'), _c('event', 'category', '事件类型'),
                   _c('note_col', 'category', '注释列 1-3', False)], '泳道图: 长事件表'),
    140: ('xy', [_c('umap_1', 'number', 'UMAP1'), _c('umap_2', 'number', 'UMAP2'),
                 _c('cluster', 'category', '簇标签')], ''),
    141: ('xy', [_c('umap_1', 'number', 'UMAP1'), _c('umap_2', 'number', 'UMAP2'),
                 _c('cluster', 'category', 'T 亚群标签')], ''),
    142: ('long', [_c('variable', 'string', '变量名'), _c('hr', 'number', 'HR'),
                   _c('lo', 'number', 'CI 下限'), _c('hi', 'number', 'CI 上限'),
                   _c('p', 'number', 'p 值'), _c('group', 'category', '分组(Mono/TAM/DC)', False)],
          '森林图类共用'),
    144: ('long', [_c('variable', 'string', '疾病/变量'), _c('beta', 'number', 'β'),
                   _c('lo', 'number', 'CI 下限'), _c('hi', 'number', 'CI 上限'),
                   _c('padj', 'number', '校正 p'), _c('count', 'number', 'Count', False)], ''),
    145: ('matrix', [_c('site', 'string', '位点(S11..N27)'), _c('aa', 'string', '氨基酸单字母'),
                     _c('energy', 'number', '结合能量')], '长表或 57×20 宽表均可'),
    147: ('long', [_c('variable', 'string', '变量'), _c('hr', 'number', 'HR'),
                   _c('lo', 'number', 'CI 下限'), _c('hi', 'number', 'CI 上限'),
                   _c('p', 'number', 'p 值')], ''),
    149: ('long', [_c('variable', 'string', '疾病'), _c('beta', 'number', 'β'),
                   _c('lo', 'number', 'CI 下限'), _c('hi', 'number', 'CI 上限'),
                   _c('padj', 'number', '校正 p')], ''),
    143: ('matrix', [_c('lon', 'number', '经度格点'), _c('lat', 'number', '纬度格点'),
                     _c('rain', 'number', '降雨(归一化)'), _c('runoff', 'number', '径流(归一化)'),
                     _c('event', 'string', '场次(a-d)')], '3D 地图: 网格化长表'),
}

# Volcano/森林/FC-FC 相关 case 批量归并
VOLCANO_CASES = [108, 109, 110, 111, 112, 113, 135, 136]
FCFC_CASES = [81, 82, 83]
FOREST_CASES = [147, 149]
UPSET_CASES = [114, 115]

# 迭代8 精度 override: family 模板形态与案例实际数据结构错位的案例
PRECISION = {
    39: ('matrix', [_c('cluster', 'string', '簇标签 c01-c20'),
                    _c('isotype', 'string', 'isotype 类别(9 类)'),
                    _c('frac', 'number', '构成比例 0-1'),
                    _c('shm_rate', 'number', 'SHM rate(右侧点列)', False)],
         '两条 100% 堆积条(簇×类构成矩阵)+右列 rate 值'),
    47: ('long', [_c('hospital', 'string', '医院(x 轴)'), _c('inc_type', 'string', '质粒 Inc 类型(y 轴)'),
                  _c('species_comp', 'string', '物种构成(A:B:C=5:3:2)'),
                  _c('count', 'number', '菌株数(饼径)')],
         '散点饼图: 每行=网格上一个观测'),
    48: ('long', [_c('participant', 'string', '参与者 ID'), _c('ring1', 'number', '环 1 指标'),
                  _c('ring2', 'number', '环 2 指标'), _c('ring3', 'number', '环 3 指标'),
                  _c('age', 'number', '年龄', False), _c('bmi', 'number', 'BMI', False),
                  _c('gender', 'category', '性别', False)],
         '约 100 参与者沿弧排布'),
    55: ('long', [_c('category', 'string', '中心类别(9 类)'), _c('item', 'string', '外圈条目'),
                  _c('weight', 'number', '条长权重')],
         '放射网络条形: 两层树表'),
    56: ('long', [_c('category', 'string', '中心类别'), _c('item', 'string', '外圈气泡'),
                  _c('size', 'number', '气泡大小')],
         '放射网络气泡: 两层树表'),
    66: ('long', [_c('x', 'number', '自变量(暴露)'), _c('hr', 'number', 'HR'),
                  _c('lo', 'number', 'CI 下限'), _c('hi', 'number', 'CI 上限'),
                  _c('facet', 'string', '面板(a-d)', False)],
         'RCS: 每面板一条 HR 曲线带 CI 带, 另注 Poverall/Pnonlinear'),
    67: ('long', [_c('cellstate', 'string', '细胞态(9 行)'), _c('outcome', 'category', 'PFS/OS(左右面板)'),
                  _c('direction', 'category', 'Protective/Risk'), _c('count', 'number', '癌种计数')],
         '镜像堆积: 每 行×面板 一条水平堆叠'),
    68: ('long', [_c('gene', 'string', '基因签名(11 行)'), _c('score', 'number', 'M1/M2 得分'),
                  _c('side', 'category', 'M1/M2(左右镜像)')],
         '镜像小提琴: 每行背靠背两组分布'),
    73: ('long', [_c('block', 'string', '时间块(4-24wks)'), _c('mouse', 'string', '处理组'),
                  _c('subgroup', 'category', '亚群(4-5 类)'), _c('pct', 'number', '百分比')],
         '分块堆积: 每 块×组 一根 100% 柱'),
    76: ('matrix', [_c('var_a', 'string', '变量 A'), _c('var_b', 'string', '变量 B'),
                    _c('r', 'number', 'Pearson r'), _c('p', 'number', 'p 值')],
         '左网络: 变量对 r/p 边表; 右上散点矩阵另需 6 变量原始观测长表'),
    83: ('long', [_c('group', 'category', '排放分组(4 组)'), _c('value', 'number', '排放量')],
         'A 面板小提琴; B/C NMDS 另备坐标表(sample, NMDS1, NMDS2, group)'),
    86: ('long', [_c('ecosystem', 'category', '红树/盐沼/海草(列)'), _c('initial_C', 'number', '初始碳库'),
                  _c('loss', 'number', '变化量'), _c('duration', 'number', '时长'),
                  _c('disturbance', 'category', '干扰类型(点色)')],
         '2×3 拟合散点: 行=变化量/时长'),
    89: ('matrix', [_c('var_a', 'string', '环境变量 A'), _c('var_b', 'string', '环境变量 B'),
                    _c('r', 'number', 'Pearson r'), _c('p', 'number', 'p 值'),
                    _c('mantel_r', 'number', 'Mantel r(群落边)', False),
                    _c('mantel_p', 'number', 'Mantel p', False),
                    _c('community', 'string', '所属群落(连边用)', False)],
         '右上 Pearson 矩阵 + Mantel 连边同表'),
    105: ('matrix', [_c('motif', 'string', '抑制基序(行)'), _c('layer', 'string', '皮层柱(列)'),
                     _c('frac', 'number', 'Frac Syn 0-1')],
          '气泡矩阵: 4 档大小编码'),
}


# ---- recipe_vars: 程序化提取配方顶层"数据变量"(适配器输出的落点)
_DATA_NAMES = {'data', 'groups', 'links', 'edges', 'sets', 'values', 'M', 'matrix',
               'layers', 'samples', 'coords', 'items', 'bar', 'records'}


def recipe_vars(seg):
    """收录强语义数据变量: 名字在数据词典内, 或 RHS 为 load/as_*/pd.read 等数据装载调用。"""
    path = os.path.join(ROOT, 'scripts', 'recipes', 'case_seg%03d.py' % seg)
    if not os.path.exists(path):
        return []
    hits = []
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        s = line.rstrip()
        if s.startswith((' ', '	', '#')):
            continue
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.{0,60})', s)
        if not m:
            continue
        name, rhs = m.group(1), m.group(2)
        if name.startswith(('fig', 'ax', 'cax', 'cb')) or name in ('plt', 'np', 'pd', 'r'):
            continue
        is_data_name = name in _DATA_NAMES or name.endswith(('_data', '_groups', '_matrix'))
        is_loader = re.match(r'^(load\(|as_\w+\(|pd\.read|np\.(array|loadtxt)|json\.load)', rhs)
        if is_data_name or is_loader:
            hits.append({'name': name, 'line': i, 'rhs': rhs.strip()[:40]})
        if len(hits) >= 5:
            break
    return hits


def build():
    cat = json.load(open(os.path.join(ROOT, 'catalog.json'), encoding='utf-8'))
    out = {}
    for c in cat['cases']:
        seg = c['seg']
        if seg in SPECIAL:
            fmt, cols, notes = SPECIAL[seg]
        elif seg in PRECISION:
            fmt, cols, notes = PRECISION[seg]
        else:
            fmt, cols, notes = FAMILY_TPL[c['family']]
        entry = {
            'case': c['case'], 'title': c['title'], 'family': c['family'],
            'format': fmt, 'columns': cols,
            'notes': (notes + (' | ' if notes and c.get('data') else '') + c.get('data', '')).strip(' |'),
            'source_text': c.get('data', ''),
        }
        rv = recipe_vars(seg)
        if rv:
            entry['recipe_vars'] = rv
        out['%03d' % seg] = entry
    dst = os.path.join(ROOT, 'reference', 'data-schemas.json')
    json.dump({
        'note': '数据输入契约。format: long=每行一观测 / wide=每列一组 / matrix=行列矩阵 / '
                'edges=边表 / sets=集合表 / xy=坐标表 / newick=树文件 / ternary 见 columns。'
                '使用: scripts/data_io.py 的 load/validate/as_* 适配器。',
        'schemas': out,
    }, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # 覆盖统计
    from collections import Counter
    print('schemas:', len(out), '| formats:', dict(Counter(v['format'] for v in out.values())))
    print('saved:', dst)


if __name__ == '__main__':
    build()
