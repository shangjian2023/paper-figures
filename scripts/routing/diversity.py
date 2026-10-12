# -*- coding: utf-8 -*-
"""多样性重排层(R4): MMR(Maximal Marginal Relevance) 在相关性与多样性间权衡。

流程: 先按相关性排好 → 硬约束可行性过滤(家族/用途上限, 与旧逻辑一致) → 在可行集上
贪心 MMR: 每步选 argmax( λ*rel - (1-λ)*max_sim(候选, 已选) )。
sim 用候选档案文本的 TF-IDF 字符 n-gram 余弦(近重复检测), 无需额外依赖。
λ 由 _weights.json 的 mmr_lambda 控制: 1=纯相关性, 0=纯多样性。
"""
import os
import json
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))


def _weights():
    p = os.path.join(ROOT, 'reference', 'routing', '_weights.json')
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return {}


def _doc(c):
    prof = c.get('_prof') or {}
    parts = []
    for f in ('use_when', 'triggers', 'anti_when', 'style'):
        v = prof.get(f)
        if isinstance(v, list):
            v = ' '.join(map(str, v))
        if v:
            parts.append(str(v))
    return ' '.join(parts) or c.get('type_zh', '')


def _sim_matrix(docs):
    """文档两两余弦(char_wb 1-3 gram)。docs 少(<=146), 直接稠密算。"""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        vec = TfidfVectorizer(analyzer='char_wb', ngram_range=(1, 3), min_df=1)
        mat = vec.fit_transform(docs)
        return cosine_similarity(mat)
    except Exception:
        n = len(docs)
        return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def mmr_diversify(scored, n, lambda_=None, fam_cap=2, pur_cap=3, exposure=None, explore_slot=None):
    """scored: 已按相关性降序的候选列表(需含 family/_purposes/_prof)。
    返回 top-n 列表。硬约束(家族/用途上限) skip-not-drop 保持; 在可行集内做 MMR。
    explore_slot=True 时最后一个名额给"可行集里累计曝光最低"的候选(确定性 ε-greedy),
    保证图库不被头部案例垄断。"""
    w = _weights()
    lambda_ = lambda_ if lambda_ is not None else float(w.get('mmr_lambda', 0.85))
    if explore_slot is None:
        explore_slot = bool(w.get('explore_slot', False)) and exposure is not None
    rel = [c['_score'] for c in scored]
    hi, lo = max(rel), min(rel)
    rng = (hi - lo) or 1.0
    reln = [(r - lo) / rng for r in rel]           # 归一化相关性 0-1

    docs = [_doc(c) for c in scored]
    sim = _sim_matrix(docs)

    fam, pur = Counter(), Counter()
    picked, picked_idx = [], []

    def feasible(i):
        f = scored[i]['family']
        p = (scored[i].get('_purposes') or ['组间比较'])[0]
        return fam[f] < fam_cap and pur[p] < pur_cap

    while len(picked) < n:
        last_slot = explore_slot and (len(picked) == n - 1)
        best, best_val = None, -1e9
        for i in range(len(scored)):
            if i in picked_idx or not feasible(i):
                continue
            if last_slot:
                # 探索槽: 曝光最低者优先, 同曝光按相关性
                val = -exposure.get(scored[i]['seg'], 0) * 10 + reln[i]
            else:
                div_pen = max((sim[i][j] for j in picked_idx), default=0.0)
                val = lambda_ * reln[i] - (1 - lambda_) * div_pen
            if val > best_val:
                best, best_val = i, val
        if best is None:   # 可行集耗尽: 放宽硬约束补齐
            for i in range(len(scored)):
                if i not in picked_idx:
                    best = i
                    break
            if best is None:
                break
        picked.append(scored[best])
        picked_idx.append(best)
        fam[scored[best]['family']] += 1
        pur[(scored[best].get('_purposes') or ['组间比较'])[0]] += 1
    return picked
