# -*- coding: utf-8 -*-
"""语义检索层(R3b): 意图文本 vs 档案文本的向量相似度, 补 BM25 的语义鸿沟。

设计(依 _research_semantic_routing.md Top2):
  - 行级编码: 每条 use_when / triggers / anti_when / plain / style / type_zh 单独成向量,
    查询取"对每档案所有行向量的最大余弦"——一条意图往往只和档案里某一行对得上,
    整段平均会稀释这个信号。
  - 模型链: 本地 bge-small-zh-v1.5(ModelScope, 24M/512维, 中文原生) → HF multilingual MiniLM
    → 降级 tfidf 字符 n-gram(无 torch 环境的保底)。
  - 档案向量按内容指纹缓存 _sem_cache.npz; 档案变更自动重建。
  - bge 短查询按官方建议加检索指令前缀。
"""
import os
import json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
ROUTING = os.path.join(ROOT, 'reference', 'routing')
CACHE = os.path.join(ROUTING, '_sem_cache.npz')

BGE_PREFIX = '为这个句子生成表示以用于检索相关文章：'
ST_MODEL = 'paraphrase-multilingual-MiniLM-L12-v2'

_model = None
_model_kind = None


def _find_local_model():
    """本地模型目录探测链: ModelScope 缓存 bge-small-zh(两种布局) → HF 缓存 multilingual MiniLM。"""
    home = os.path.expanduser('~')
    cands = [
        os.path.join(home, '.cache', 'modelscope', 'models', 'AI-ModelScope--bge-small-zh-v1.5',
                     'snapshots', 'master'),
        os.path.join(home, '.cache', 'modelscope', 'hub', 'models', 'AI-ModelScope',
                     'bge-small-zh-v1.5'),
    ]
    hf = os.path.join(home, '.cache', 'huggingface', 'hub',
                      'models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2',
                      'snapshots')
    if os.path.isdir(hf):
        cands += [os.path.join(hf, d) for d in os.listdir(hf) if os.path.isdir(os.path.join(hf, d))]
    return next((p for p in cands if os.path.exists(os.path.join(p, 'config.json'))), None)


def _get_model():
    global _model, _model_kind
    if _model is not None:
        return _model, _model_kind
    try:
        from sentence_transformers import SentenceTransformer
        local = _find_local_model()
        _model = SentenceTransformer(local or ST_MODEL)
        _model_kind = 'bge-zh' if (local and 'bge' in local.replace('\\', '/').lower()) else 'st'
        return _model, _model_kind
    except Exception:
        return None, None


def _rows(seg, prof):
    """档案 → 行级文本列表。"""
    rows = []
    for field in ('use_when', 'triggers', 'anti_when'):
        for v in prof.get(field) or []:
            v = str(v).strip()
            if v:
                rows.append(v)
    for field in ('plain', 'style', '_type_zh'):
        v = prof.get(field)
        if v:
            rows.append(str(v).strip())
    return rows or [seg]


def _fingerprint(profiles):
    h = json.dumps({''.join(sorted(profiles)): {s: _rows(s, profiles[s]) for s in sorted(profiles)}},
                   ensure_ascii=False, sort_keys=True, default=str)
    import hashlib
    return hashlib.md5(h.encode('utf-8')).hexdigest()


def _build_index(profiles, model, kind):
    segs, rows = [], []
    for s in sorted(profiles):
        rs = _rows(s, profiles[s])
        rows += rs
        segs += [s] * len(rs)
    enc = model.encode([BGE_PREFIX + r for r in rows] if kind == 'bge-zh' else rows,
                       batch_size=64, show_progress_bar=False)
    enc = np.asarray(enc, dtype=np.float32)
    n = np.linalg.norm(enc, axis=1, keepdims=True)
    n[n == 0] = 1.0
    enc = enc / n
    try:
        np.savez_compressed(CACHE, fp=_fingerprint(profiles),
                            segs=np.array(segs), rows=np.array(rows, dtype=object), mat=enc)
    except Exception:
        pass
    return segs, enc


def _load_index(profiles, model, kind):
    if os.path.exists(CACHE):
        try:
            z = np.load(CACHE, allow_pickle=True)
            if str(z['fp']) == _fingerprint(profiles):
                return list(z['segs']), np.asarray(z['mat'], dtype=np.float32)
        except Exception:
            pass
    return _build_index(profiles, model, kind)


def scores(query_text, profiles, backend=None):
    """返回 ({seg: 0-1 归一余弦分}, 使用的后端名)。行级 max 余弦。"""
    segs = sorted(profiles)
    model, kind = _get_model() if backend in (None, 'st') else (None, None)
    if model is not None:
        try:
            idx_segs, mat = _load_index(profiles, model, kind)
            q = model.encode([BGE_PREFIX + query_text] if kind == 'bge-zh' else [query_text])[0]
            q = np.asarray(q, dtype=np.float32)
            qn = np.linalg.norm(q) or 1.0
            sims = (mat @ q) / qn
            best = {}
            for s, v in zip(idx_segs, sims):
                if s not in best or v > best[s]:
                    best[s] = float(v)
            return _norm(best), kind
        except Exception:
            pass
    return _tfidf_scores(query_text, profiles), 'tfidf'


def _tfidf_scores(query_text, profiles):
    """降级后端: 字符 n-gram TF-IDF 余弦(整段)。"""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    segs = sorted(profiles)
    docs = [' '.join(_rows(s, profiles[s])) for s in segs]
    vec = TfidfVectorizer(analyzer='char_wb', ngram_range=(1, 3), min_df=1)
    try:
        mat = vec.fit_transform(docs)
        sim = cosine_similarity(vec.transform([query_text]), mat)[0]
    except ValueError:
        return {s: 0.0 for s in segs}
    return _norm(dict(zip(segs, (float(x) for x in sim))))


def _norm(d):
    lo, hi = min(d.values()), max(d.values())
    rng = (hi - lo) or 1.0
    return {k: (v - lo) / rng for k, v in d.items()}
