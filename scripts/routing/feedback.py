# -*- coding: utf-8 -*-
"""反馈信号层(R4): 让路由器从历史里学——展示过的不重复轰炸, 用户选过的好上浮。

两个信号源:
  1. route_log.jsonl(展示日志): 时间半衰期衰减的降权, 展示≠永久拉黑——
     半衰期默认 7 天, 一周前的展示几乎不再影响。
  2. taste.md(用户品味记录, 现有格式): "选了 seg005 的布局 + seg041 的配色" → 这些 seg
     轻度加权(用户真正选过的气质); "否决 segXXX" → 降权。
两者都只做温和调整, 不改变主排序的语义。
"""
import os
import re
import json
import datetime
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
LOG = os.path.join(ROOT, 'route_log.jsonl')
TASTE = os.path.join(ROOT, 'taste.md')


def _weights():
    p = os.path.join(ROOT, 'reference', 'routing', '_weights.json')
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return {}


def recency_penalty(now=None):
    """展示日志 → 惩罚分(事件分型 + 指数衰减 + 封顶)。

    只罚 shown 事件(用户最终选过的 picked 不罚, vetoed 单独重罚);
    惩罚 = w * 0.5^(age_days/half_life), 单 seg 封顶 cap, 防止"真正想要的图被永久压没"。"""
    w = _weights()
    base = float(w.get('recency_penalty', 0.6))
    half_life = float(w.get('recency_halflife_days', 2.0))
    cap = float(w.get('recency_cap', 2.5))
    max_track = int(w.get('recency_max_records', 6))
    if base <= 0 or not os.path.exists(LOG):
        return {}
    now = now or datetime.datetime.now()
    lines = open(LOG, encoding='utf-8').read().splitlines()[-60:]
    pen = Counter()
    try:
        records = [json.loads(ln) for ln in lines if ln.strip()]
    except Exception:
        return {}
    for rec in records[-max_track:]:
        if rec.get('event', 'shown') == 'picked':
            continue
        try:
            ts = datetime.datetime.fromisoformat(rec.get('ts', ''))
            age_days = max(0.0, (now - ts).total_seconds() / 86400.0)
        except Exception:
            age_days = 0.0
        p = base * (0.5 ** (age_days / max(half_life, 0.1)))
        for s in rec.get('top', []):
            pen[int(s)] += p
    return {s: min(v, cap) for s, v in pen.items()}


def exposure_counts():
    """各 seg 累计展示次数(供探索槽选低曝光候选)。"""
    cnt = Counter()
    if not os.path.exists(LOG):
        return cnt
    for ln in open(LOG, encoding='utf-8').read().splitlines()[-60:]:
        try:
            rec = json.loads(ln)
            if rec.get('event', 'shown') == 'shown':
                for s in rec.get('top', []):
                    cnt[int(s)] += 1
        except Exception:
            continue
    return cnt


def taste_signals():
    """taste.md → ({seg: 加分}, {seg: 减分})。格式: 日期 | 场合 | 选了 seg005 的布局 + seg041 的配色 | 否决 ... | 备注"""
    if not os.path.exists(TASTE):
        return {}, {}
    w = _weights()
    boost, veto = Counter(), Counter()
    up = float(w.get('taste_boost', 0.5))
    down = float(w.get('veto_penalty', 1.5))
    for ln in open(TASTE, encoding='utf-8'):
        if '|' not in ln or 'seg' not in ln.lower():
            continue
        parts = [p.strip() for p in ln.split('|')]
        pick_part = next((p for p in parts if '选了' in p or '选择' in p), '')
        veto_part = next((p for p in parts if '否决' in p or '不要' in p), '')
        for m in re.finditer(r'seg\s*(\d{1,3})', pick_part, re.I):
            boost[int(m.group(1))] += up
        for m in re.finditer(r'seg\s*(\d{1,3})', veto_part, re.I):
            veto[int(m.group(1))] += down
    return dict(boost), dict(veto)


def record_event(seg, event='picked'):
    """记录用户的选择/否决事件(picked/vetoed), 写进 route_log.jsonl 供反馈层用。"""
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'ts': datetime.datetime.now().isoformat(timespec='seconds'),
                            'event': event, 'seg': seg}, ensure_ascii=False) + '\n')


def apply_feedback(scored):
    """就地微调 scored 列表的 _score(温和信号)。"""
    w = _weights()
    pen = recency_penalty()
    boost, veto = taste_signals()
    if not (pen or boost or veto):
        return scored
    for c in scored:
        s = c['seg']
        if s in pen:
            c['_score'] -= pen[s]
            c['_why'] = c['_why'] + ['近期已展示-%.2f' % pen[s]]
        if s in boost:
            c['_score'] += boost[s]
            c['_why'] = c['_why'] + ['口味偏好']
        if s in veto:
            c['_score'] -= veto[s]
            c['_why'] = c['_why'] + ['已否决']
    scored.sort(key=lambda x: -x['_score'])
    return scored
