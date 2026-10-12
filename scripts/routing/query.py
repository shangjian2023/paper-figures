# -*- coding: utf-8 -*-
"""查询理解层(R1): 把用户的一句话翻译成路由器可用的规范化文本、同义词扩展与意图槽位。

route.rank() 的前置步骤。三层:
  normalize  全角→半角/小写/去空白/中文数字→阿拉伯数字(组数槽位用)
  expand     同义词组命中任一别名 → 把整组规范词追加进查询(消"山脊一样"≠"山脊图"的字面形态差)
  slots      抽取 组数/类别数/变量数/样本数/时间点 等数值槽位, 与 anti_when 里的
             可判定界限(如"组数 >8")做机器比对, 违反则硬惩罚
"""
import re

# 中文数字 → 阿拉伯(只处理槽位常用的)
CN_NUM = {'零': 0, '一': 1, '两': 2, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7,
          '八': 8, '九': 9, '十': 10, '十一': 11, '十二': 12, '十几': 12, '二十': 20,
          '三十': 30, '四十': 40, '五十': 50, '百': 100}

# 同义词组: 命中任一别名 → 整组词都追加进查询(供触发词子串匹配扩面)
SYNONYM_GROUPS = {
    '山脊图': ['山脊', 'ridgeline', 'joyplot', '峰峦', '山峦', '山峰', '群山', '连绵'],
    '蜂群图': ['蜂群', 'beeswarm', '蜜蜂', '密密麻麻的散点'],
    '云雨图': ['云雨', 'raincloud', '半小提琴'],
    '边际分布': ['边际', '边缘', 'marginal', '边上带', '旁边带', '侧边'],
    '镜像图': ['镜像', '蝴蝶图', '对称', '左右各一半'],
    '配对图': ['配对', '成对', 'paired', '治疗前后', '用药前后', '前后对比'],
    '连线': ['连线', '连成线', 'spaghetti', '个体走向'],
    '火山图': ['火山', 'volcano'],
    '富集分析': ['富集', 'enrichment', 'GO', 'KEGG'],
    '桑基图': ['桑基', 'sankey', '冲击图', 'alluvial', '流量', '流向'],
    '和弦图': ['和弦', 'chord', '弦图', 'circos'],
    'UpSet图': ['upset', '交集', 'venn', '韦恩'],
    '地图': ['地图', 'choropleth', '世界地图', '中国地图', '地理'],
    '发育树': ['发育树', '进化树', '系统发育', 'phylo', '进化关系'],
    '三元图': ['三元', 'ternary', '三成分'],
    '雷达图': ['雷达', 'radar', '蜘蛛图'],
    '热图': ['热图', 'heatmap', '点阵'],
    '箱线图': ['箱线', 'boxplot', '盒须'],
    '小提琴图': ['小提琴', 'violin'],
    '散点图': ['散点', 'scatter'],
    '折线图': ['折线', 'line chart', '曲线'],
    '柱形图': ['柱形', '柱状', '条形', 'bar'],
    '堆叠': ['堆叠', '堆积', 'stacked', '构成'],
    '显著性': ['显著性', '显著', 'p值', 'p value', '星号', '统计学意义'],
    '误差棒': ['误差棒', '误差线', 'error bar', '标准差', 'sem'],
    '置信区间': ['置信', 'ci', '置信带'],
    '拟合': ['拟合', '回归线', '趋势线', 'regression'],
    '相关系数': ['相关系数', '相关性', 'pearson', 'spearman'],
    '分群': ['分群', '聚类', 'cluster', '降维'],
    '时间序列': ['时间序列', '时序', '随时间', '纵向', '时间点', '动态变化'],
    '原始数据': ['原始数据', '原始观测', '数据点', '每个样本', '个体点'],
    '排名': ['排名', '排序', 'ranking', 'benchmark', '跑分'],
    '泳道': ['泳道', 'swimmer'],
}

# 槽位: (意图里的正则, 维度名)
SLOT_PATTERNS = [
    (r'(\d+)\s*个?(组|处理组|实验组|分组)', '组数'),
    (r'([一二两三四五六七八九十十几]+)\s*个?(组|处理组|实验组|分组)', '组数'),
    (r'(\d+)\s*个?(变量|指标|基因|因子)', '变量数'),
    (r'([一二两三四五六七八九十十几]+)\s*个?(变量|指标|基因|因子)', '变量数'),
    (r'(\d+)\s*个?(类别|物种|亚群|簇|细胞类型)', '类别数'),
    (r'([一二两三四五六七八九十十几]+)\s*个?(类别|物种|亚群|簇|细胞类型)', '类别数'),
    (r'(\d+)\s*个?(时间点|采样点)', '时间点'),
    (r'(\d+)\s*(个样本|例|名患者|个被试)', '样本数'),
]

# anti_when 里可解析的界限: "组数 >8" / "变量超过 50" / "类别少于 3"…
BOUND_RE = re.compile(
    r'(组数|变量数|类别数|时间点|样本数|组|变量|类别|物种|指标|基因|时间)'
    r'[^\d<>≥≤]{0,6}([<>≥≤]|超过|大于|少于|小于|不足|不多于|多于)\s*(\d+)')

_DIM_ALIAS = {'组': '组数', '变量': '变量数', '指标': '变量数', '基因': '变量数', '因子': '变量数',
              '类别': '类别数', '物种': '类别数', '亚群': '类别数', '簇': '类别数', '细胞类型': '类别数',
              '时间': '时间点', '时间点': '时间点', '采样点': '时间点', '样本数': '样本数'}


def normalize(intent):
    """全角→半角、小写、去多余空白。"""
    t = intent
    tbl = {ord(f): ord(t) for f, t in zip('ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９',
                                          'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')}
    t = t.translate(tbl).lower()
    return re.sub(r'\s+', ' ', t).strip()


def _to_num(cn):
    if cn in CN_NUM:
        return CN_NUM[cn]
    if cn == '十几':
        return 12
    if '十' in cn:
        parts = cn.split('十')
        tens = CN_NUM.get(parts[0], 1) if parts[0] else 1
        ones = CN_NUM.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
        return tens * 10 + ones
    return CN_NUM.get(cn)


_NEG_WORDS = ('不', '别', '无', '非', '无需', '排除', '去掉')


def _negated_at(intent, alias):
    """alias 在 intent 里的任意出现位置, 前 3 字窗含否定词即视为被否定。"""
    i = intent.find(alias)
    while i != -1:
        if any(n in intent[max(0, i - 3):i] for n in _NEG_WORDS):
            return True
        i = intent.find(alias, i + 1)
    return False


def expand(intent):
    """返回 (扩展后的查询文本, 命中的同义词组, 排除项)。

    排除项: 命中于否定语境("不要柱状图")的同义词组——不注入规范词,
    并由 rank() 对触发词/类型名含该 surface 的案例做重罚(用户点名不要的图型)。"""
    hits, exclusions = [], []
    for canon, aliases in SYNONYM_GROUPS.items():
        hit = None
        for a in aliases:
            if a in intent:
                hit = a
                break
        if hit is None:
            continue
        if _negated_at(intent, hit):
            exclusions.append((canon, hit))
        else:
            hits.append(canon)
    extra = ' '.join(hits)
    return (intent + ' ' + extra).strip(), hits, exclusions


def extract_slots(intent):
    """意图里的数值槽位 {维度: 数值}。"""
    slots = {}
    for pat, dim in SLOT_PATTERNS:
        m = re.search(pat, intent)
        if m:
            raw = m.group(1)
            v = int(raw) if raw.isdigit() else _to_num(raw)
            if v is not None:
                slots[dim] = v
    return slots


def parse_bounds(anti_when_list):
    """反指文本 → [(维度, 方向, 数值)]; 方向 'up' 表示超过该数会出问题, 'down' 表示少于该数会出问题。"""
    out = []
    for text in anti_when_list or []:
        m = BOUND_RE.search(text)
        if not m:
            continue
        dim, op, num = m.group(1), m.group(2), int(m.group(3))
        dim = _DIM_ALIAS.get(dim, dim)
        direction = 'down' if op in ('<', '≤', '少于', '小于', '不足') else 'up'
        out.append((dim, direction, num))
    return out


def constraint_penalty(slots, bounds):
    """意图槽位 vs 反指界限的机器比对。返回 (罚分, 违反描述列表)。

    bounds 支持两种形态:
      文本解析产物: [(维度, 'up'|'down', 数值)]   (query.parse_bounds 的输出)
      结构化字段:   [{'dim':'组数','op':'>','val':8, ...}]  (终审为档案补的 constraints)"""
    pen, bad = 0.0, []
    for b in bounds or []:
        if isinstance(b, dict):
            dim, num = b.get('dim'), b.get('val')
            direction = 'down' if b.get('op') in ('<', '≤') else 'up'
        else:
            dim, direction, num = b
        v = slots.get(dim)
        if v is None:
            continue
        if direction == 'up' and v > num:
            pen -= 3.0
            bad.append('%s=%d 超过反指界限 >%d' % (dim, v, num))
        elif direction == 'down' and v < num:
            pen -= 3.0
            bad.append('%s=%d 低于反指界限 <%d' % (dim, v, num))
    return pen, bad
