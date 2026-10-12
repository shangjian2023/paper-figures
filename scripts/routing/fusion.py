# -*- coding: utf-8 -*-
"""通道融合层(R3b, 依 _research_semantic_routing.md Top1):

RRF (Reciprocal Rank Fusion): score(seg) = Σ_c w_c / (k + rank_c(seg))。
  - 按排名而非分数融合, 各通道分数量纲无关, 免归一免调参(Elasticsearch 同款, k=60);
  - 通道: rule(触发词/用途/场景/受众/气质) · lex(BM25) · sem(bge 行级余弦);
  - 权重 w_c 由 _weights.json 控制, w=0 即关闭该通道。
罚分(反指违反/数据缺口)与反馈信号(近期展示/口味)不进通道, 在融合后叠加。
"""
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
K_DEFAULT = 60


def load_weights():
    p = os.path.join(ROOT, 'reference', 'routing', '_weights.json')
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return {}


def rrf(channels, k=K_DEFAULT):
    """channels: {通道名: {seg: 分数}}; 返回 {seg: rrf 分}。"""
    out = {}
    for name, scores in channels.items():
        if not scores:
            continue
        ordered = sorted(scores.items(), key=lambda kv: -kv[1])
        for rank, (seg, _sc) in enumerate(ordered, 1):
            out[seg] = out.get(seg, 0.0) + 1.0 / (k + rank)
    return out


def weighted_rrf(channels, weights, k=K_DEFAULT):
    """带通道权重的 RRF; 权重 0/缺失的通道不参与。"""
    out = {}
    for name, scores in channels.items():
        w = float(weights.get(name, 1.0))
        if w <= 0 or not scores:
            continue
        ordered = sorted(scores.items(), key=lambda kv: -kv[1])
        for rank, (seg, _sc) in enumerate(ordered, 1):
            out[seg] = out.get(seg, 0.0) + w / (k + rank)
    return out
