# -*- coding: utf-8 -*-
"""词面检索层(R2): jieba 分词 + BM25Okapi, 字段加权拼接的档案语料。

比"触发词子串匹配"多出的能力:
  - 查询里的词不需要逐字命中 triggers, 在 use_when/anti_when/type_en 里出现同样得分
  - BM25 的 IDF 自动压低泛词(如"数据""展示")权重, 突出鉴别性词(如"云雨""桑基")
字段权重: triggers×3(人工精选, 最可信) / type_zh×2 / use_when×2 / type_en×1.5 /
          anti_when×1 / style×1。
"""
import os
import re
import json
import glob

try:
    import jieba
except ImportError:            # 未装 jieba 时降级为字符 bigram 分词, 路由不至于崩
    jieba = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
ROUTING = os.path.join(ROOT, 'reference', 'routing')

FIELD_WEIGHTS = [('triggers', 3.0), ('type_zh', 2.0), ('use_when', 2.0),
                 ('type_en', 1.5), ('anti_when', 1.0), ('style', 1.0)]

_STOP = {'的', '了', '和', '是', '在', '有', '个', '要', '想', '看', '我', '那', '这种',
         '怎么', '可以', '使用', '进行', '一个', '一种', '数据', '展示', '显示', '画',
         '图', '的图', '出来', '需要', '希望', '请', '帮', '给我'}

_tok = None


def _tokenizer():
    global _tok
    if jieba is None:          # 降级: 字符 bigram(对中文召回尚可, 精度略降)
        return lambda s: [s[i:i+2] for i in range(0, len(s)-1)
                          if s[i:i+2].strip() and s[i:i+2] not in _STOP]
    if _tok is None:
        # 档案里的触发词/类型名注册为整词, 防止被切碎(如"云雨图"→"云雨"+"图")
        for p in glob.glob(os.path.join(ROUTING, 'seg*.json')):
            try:
                r = json.load(open(p, encoding='utf-8'))
            except Exception:
                continue
            for t in (r.get('triggers') or []):
                if 2 <= len(t) <= 12:
                    jieba.add_word(t.lower(), freq=1000)
            for t in re.findall(r'[\u4e00-\u9fffA-Za-z0-9+\-]+', r.get('type_zh', '') or ''):
                if 2 <= len(t) <= 12:
                    jieba.add_word(t.lower(), freq=500)
        _tok = lambda s: [w for w in jieba.lcut(s.lower())
                          if w.strip() and w not in _STOP and not w.isspace()]
    return _tok


def build_corpus(profiles):
    """档案 → {seg: 加权拼接文本}。"""
    corpus = {}
    for seg, prof in profiles.items():
        parts = []
        for field, w in FIELD_WEIGHTS:
            v = prof.get(field)
            if not v:
                continue
            if isinstance(v, list):
                v = ' '.join(map(str, v))
            parts.append((' %s ' % str(v)) * int(w))
        corpus[seg] = ' '.join(parts)
    return corpus


def bm25_scores(query_text, profiles, corpus=None):
    """返回 {seg: min-max 归一化的 BM25 得分}。rank_bm25 缺失时返回全 0(优雅降级)。"""
    try:
        from rank_bm25 import BM25Okapi
    except Exception:
        return {s: 0.0 for s in profiles}
    w = (lambda p: json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {})(
        os.path.join(ROOT, 'reference', 'routing', '_weights.json'))
    k1 = float(w.get('bm25_k1', 1.2))   # 短文档(30-80词)低 k1/低 b, 依调研建议
    b = float(w.get('bm25_b', 0.3))
    corpus = corpus or build_corpus(profiles)
    tok = _tokenizer()
    segs = sorted(corpus)
    docs = [tok(corpus[s]) for s in segs]
    bm25 = BM25Okapi(docs, k1=k1, b=b)
    q = tok(query_text)
    if not q:
        return {s: 0.0 for s in segs}
    raw = bm25.get_scores(q)
    lo, hi = min(raw), max(raw)
    rng = (hi - lo) or 1.0
    return {s: float((r - lo) / rng) for s, r in zip(segs, raw)}


def bigram_scores(query_text, profiles, corpus=None):
    """字符 bigram 覆盖率通道(调研 Top1): 对切分边界/错别字/中英混写稳健的词面保障。
    score = |查询bigram ∩ 档案bigram| / |查询bigram| —— 天然 0-1 不做 min-max:
    归一化会把"只沾一个词"的查询拉满, 拒绝机制就失效了(P1 教训)。max 分数也是
    拒绝判据(查询覆盖率过低 = 图库没有相关内容)。"""
    import re as _re

    stop_bi = {'一个', '这个', '那个', '数据', '可以', '展示', '显示', '一张', '哪个',
               '什么', '怎么', '画好', '好看', '一样', '帮我', '我想', '还有', '以及',
               '进行', '需要', '希望', '就是', '但是', '然后'}
    def bigrams(t):
        t = _re.sub(r'\s+', '', t.lower())
        bs = {t[i:i + 2] for i in range(len(t) - 1)} if len(t) > 1 else {t}
        return bs - stop_bi

    corpus = corpus or build_corpus(profiles)
    qb = bigrams(query_text)
    if len(qb) < 2:      # 内容 bigram 不足 2 个 → 证据太弱, 不作为强信号
        return {s: 0.0 for s in profiles}
    raw = {}
    for s, doc in corpus.items():
        db = bigrams(doc)
        raw[s] = len(qb & db) / len(qb)
    return raw
