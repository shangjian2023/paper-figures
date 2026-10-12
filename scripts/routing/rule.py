# -*- coding: utf-8 -*-
"""规则通道(R0 起, R5 收编): 触发词子串 + 用途同义词 + 场景重合 + 气质/受众调权。

这是三通道融合(rule/lex/sem)里最"人工精心"的一路: 词表来自卡片 purpose 体系,
命中即强信号。语义/词面通道作为补充, 见 lexical.py 与 semantic.py。
"""
import re

# 意图 → 用途词(与卡片 purpose 词表一致) 的同义词触发
PURPOSE_SYNONYMS = {
    '组间比较': ['组间', '比较', '对比', '差异', '处理组', '对照组', '给药', '剂量组',
               '显著性', '显著', '有无效果', '哪个好', '哪个高', '谁高谁低', '高低',
               '疗效', '药效', '组内', '两组', '三组', '多组', 'p值', 't检验', 'anova'],
    '分布形态': ['分布', '离散', '集中趋势', '偏态', '正态', '波动', '分散', '原始数据',
               '数据点', '每次测量', '个体差异'],
    '相关关系': ['相关', '关联', '关系', '拟合', '回归', '随.*增加', '随.*下降', '线性',
               '协变', '一致性'],
    '构成占比': ['组成', '构成', '占比', '比例', '份额', '百分比', '物种组成', '群落结构',
               '细胞比例', '百分比堆积'],
    '趋势变化': ['时间', '时序', '随时间', '纵向', '动态', '时间点', '演变', '变化趋势',
               '剂量', '响应', '浓度', '生长曲线'],
    '网络与流向': ['流向', '流量', '路径', '转化', '来源', '去向', '迁移', '网络', '互作',
                '连接', '弦', '交集', 'venn', ' upstream', 'downstream'],
    '空间分布': ['地图', '地理', '国家', '省份', '地区', '空间', '区域', '经纬', '全球',
               '分布图'],
    '多指标综合': ['多指标', '综合', '评价', '评估', '维度', '指标体系', '多项', '性能',
                '综合得分'],
    '差异展示': ['火山', '上调', '下调', '倍数变化', 'fc', 'log2', '富集', '差异基因',
               '差异蛋白', '差异代谢物', '曼哈顿', '森林图', 'meta'],
    '排序降维': ['umap', 'pcoa', 'nmds', 'pca', '排序', '降维', '聚类', '分群', '样本分开',
               'beta多样性'],
}
PURPOSE_BOOST_CAP = 2   # 最多计入 2 个命中用途

WOW_UP = re.compile(r'高级|惊艳|顶刊|华丽|吸睛|漂亮|好看|酷炫|夺目|封面|汇报亮点')
PLAIN = re.compile(r'朴素|简单|简洁|干净|基础|常规|低调|不花哨|审稿人')
AUDIENCE_HINTS = [('组会', '组会'), ('汇报', '组会'), ('答辩', '组会'),
                  ('投稿', '期刊正文'), ('期刊', '期刊正文'), ('发表', '期刊正文'),
                  ('正文', '期刊正文'), ('补充材料', '补充材料'), ('附图', '补充材料'),
                  ('si\b', '补充材料'), ('海报', '海报')]


def hit_purposes(intent):
    """意图里命中了哪些用途(含同义词), 返回用途列表(最多 4 个)。"""
    out = []
    for pur, words in PURPOSE_SYNONYMS.items():
        for w in words:
            if re.search(w if w.startswith('随') else re.escape(w), intent, re.I):
                out.append(pur)
                break
    return out[:4]


def _negated(intent_norm, t):
    """触发词前 3 字窗内有否定词则不算命中(吸收 NL4DV 的否定窗口设计)。"""
    i = intent_norm.find(t)
    while i != -1:
        ctx = intent_norm[max(0, i - 3):i]
        if any(neg in ctx for neg in ('不', '别', '无', '非', '无需')):
            return True
        i = intent_norm.find(t, i + 1)
    return False


def score_case(c, prof, purposes, intent, intent_norm, pur_hits, wow_mode, recent=None):
    """返回 (score, match_reasons)。wow_mode: 'up'|'plain'|None"""
    s, why = 0.0, []
    # 1) triggers 子串匹配(词长加权: 越具体的词命中越可信; 否定窗口豁免)
    for t in prof.get('triggers', []):
        if t.lower() in intent_norm and not _negated(intent_norm, t.lower()):
            s += 1.0 + 0.08 * len(t)
    if s:
        why.append('触发词')
    # 2) 用途类别命中
    case_purs = purposes.get('%03d' % c['seg'], [])
    hit = [p for p in pur_hits if p in case_purs]
    if hit:
        s += 2.2 * min(len(hit), PURPOSE_BOOST_CAP)
        why.append('/'.join(hit))
    # 3) use_when 词面重合(意图里的 2+ 字片段出现在场景描述中)
    frag = set(re.findall(r'[\u4e00-\u9fff]{2,4}', intent))
    best = 0
    for uw in prof.get('use_when', []):
        n = sum(1 for f in frag if f in uw)
        best = max(best, n)
    if best >= 2:
        s += 0.6 * min(best, 4)
        why.append('场景描述')
    # 4) 气质调权
    wow = c.get('wow', 1)
    if wow_mode == 'up' and wow >= 2:
        s += 0.9 * wow
        why.append('气质符合(wow%d)' % wow)
    elif wow_mode == 'plain':
        s += 1.5 if wow == 1 else -0.6
    # 5) 受众
    for pat, aud in AUDIENCE_HINTS:
        if re.search(pat, intent, re.I) and prof.get('audience') == aud:
            s += 0.8
            why.append('受众匹配(%s)' % aud)
            break
    return s, why
