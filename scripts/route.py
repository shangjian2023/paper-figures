# -*- coding: utf-8 -*-
"""场景路由器: 把用户的一句话需求精确映射到最合适的图库案例。

用法:
  python scripts/route.py "三组处理组的酶活性比较, 要有显著性"
  python scripts/route.py "物种组成随时间演变" --n 9 --log
  python scripts/route.py "展示这些数据" --data data.csv
  python scripts/route.py "要一张高级的图" --min-wow 2 --json

五轮迭代后的架构(意图理解, 详见 reference/routing/_iteration_log.md):
  查询理解  routing/query.py    归一化 + 同义词组扩展 + 槽位(组数等)与反指界限机器比对
  规则通道  routing/rule.py     触发词/用途词表/场景重合/气质与受众(最人工精心的一路)
  词面通道  routing/lexical.py  jieba+BM25Okapi, 字段加权语料(默认启用)
  语义通道  routing/semantic.py bge 行级向量(可选: _weights.json sem>0 且装了模型才启用;
                                 未装则自动降级, skill 默认零重依赖)
  融合      routing/fusion.py   语义关=线性(rule + 2.2×BM25); 语义开=RRF 三通道
  重排      routing/diversity.py MMR λ=0.85 + 硬约束(家族≤2/用途≤3) + 探索槽
  反馈      routing/feedback.py route_log 事件分型衰减 + taste.md 口味加权
数据适配: --data 逐候选 validate(); 拒绝机制: 三通道全弱时如实说"没有合适的"。
"""
import json
import os
import re
import glob
import argparse
import datetime
from collections import Counter

import sys as _sys
try:                            # Windows GBK 控制台打印生僻字符不崩(降级为替换符)
    _sys.stdout.reconfigure(errors='replace')
except Exception:
    pass
import warnings as _warnings
_warnings.filterwarnings('ignore', message='.*pkg_resources.*')

import routing.query as query
import routing.rule as rule
import routing.lexical as lexical
import routing.semantic as semantic
import routing.fusion as fusion
import routing.diversity as diversity
import routing.feedback as feedback
import routing.datashape as datashape


def _load_weights():
    p = os.path.join(ROOT, 'reference', 'routing', '_weights.json')
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return {'lex': 2.2, 'sem': 0.0}

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
ROUTING = os.path.join(ROOT, 'reference', 'routing')
LOG = os.path.join(ROOT, 'route_log.jsonl')


def load_all():
    cat = json.load(open(os.path.join(ROOT, 'catalog.json'), encoding='utf-8'))['cases']
    profiles = {}
    for p in glob.glob(os.path.join(ROUTING, 'seg*.json')):
        try:
            r = json.load(open(p, encoding='utf-8'))
            profiles[int(r['seg'])] = r
        except Exception:
            pass
    pm_path = os.path.join(ROOT, 'gallery', 'cards', '_purposes.json')
    purposes = json.load(open(pm_path, encoding='utf-8')) if os.path.exists(pm_path) else {}
    return cat, profiles, purposes



def data_penalty(df, segs):
    """对候选逐个 validate, 缺必需列的重罚。返回 {seg: (delta, note)}。"""
    import sys
    sys.path.insert(0, HERE)
    try:
        import data_io
    except Exception:
        return {}
    out = {}
    for seg in segs:
        try:
            rep = data_io.validate(df, seg, verbose=False)
        except Exception:
            continue
        if not rep['ok']:
            out[seg] = (-2.8, '数据缺口: ' + '; '.join(rep['errors'][:2]))
        elif rep['warnings']:
            out[seg] = (0.0, '数据提醒: ' + rep['warnings'][0])
        else:
            out[seg] = (0.6, '数据契约通过(%s)' % rep['format'])
    return out


def recent_shows(k=3):
    """route_log.jsonl 最近 k 次路由展示过的 seg → 出现次数。"""
    cnt = Counter()
    if not os.path.exists(LOG):
        return cnt
    lines = open(LOG, encoding='utf-8').read().splitlines()[-k:]
    for ln in lines:
        try:
            for s in json.loads(ln).get('top', []):
                cnt[int(s)] += 1
        except Exception:
            continue
    return cnt


def diversify(ranked, n):
    """多样性硬约束: 每 family<=2, 每用途<=3; 池不够时放宽补齐。"""
    fam, pur = Counter(), Counter()
    picked = []
    for c in ranked:
        f = c['family']
        p = (c.get('_purposes') or ['组间比较'])[0]
        if fam[f] >= 2 or pur[p] >= 3:
            continue
        picked.append(c)
        fam[f] += 1
        pur[p] += 1
        if len(picked) >= n:
            return picked
    for c in ranked:   # 放宽补齐
        if c not in picked:
            picked.append(c)
            if len(picked) >= n:
                break
    return picked


def rank(intent, n=9, min_wow=0, df=None, data=None, use_log=True):
    """路由核心：意图 → 三通道 RRF 融合 → 罚分/反馈 → MMR 多样性 → top-n。

    use_log=False 时不读展示日志与探索槽(评测用, 保证可复现)。"""
    cat, profiles, purposes = load_all()
    if not profiles:
        raise SystemExit('routing 档案为空: 先跑 reference/routing 下的档案生产流程')
    # R1 查询理解: 归一化 + 同义词扩展 + 槽位
    q = query.normalize(intent)
    q_exp, syn_hits, exclusions = query.expand(q)
    slots = query.extract_slots(q)
    intent_norm = q_exp.lower()
    pur_hits = rule.hit_purposes(q_exp)
    wow_mode = 'up' if rule.WOW_UP.search(intent) else ('plain' if rule.PLAIN.search(intent) else None)

    if df is None and data:
        import sys
        sys.path.insert(0, HERE)
        import data_io
        try:
            df = data_io.load(data)
        except Exception as e:
            raise SystemExit('读不了数据文件 %s: %s（检查路径/格式/是否空文件）' % (data, e))

    w = fusion.load_weights()
    k = int(w.get('rrf_k', 60))

    # ---- 三通道分数(RRF 按排名融合, 免归一) ----
    # 通道1 rule: 触发词/用途/场景重合/受众气质
    rule_scores, why_map = {}, {}
    for c in cat:
        if c['seg'] not in profiles:
            continue
        s, why = rule.score_case(c, profiles[c['seg']], purposes, q_exp, intent_norm,
                                 pur_hits, wow_mode)
        rule_scores[c['seg']] = s
        why_map[c['seg']] = why
    # 通道2 lex: BM25 字段加权
    channels = {'rule': rule_scores}
    lex = lexical.bm25_scores(q_exp, profiles) if w.get('lex_linear', w.get('lex', 1.0)) > 0 else {}
    lex2 = lexical.bigram_scores(q_exp, profiles)   # 始终计算: 兼作拒绝判据(原始覆盖率)
    # P4: 查询零内容(rule 全零 + bigram 覆盖弱)时, 纯审美调权减半——防"好看"一词让 wow3 尾部垄断
    weak_wow = (wow_mode == 'up' and max(rule_scores.values(), default=0) <= 0
                and max(lex2.values(), default=0) < 0.25)
    if weak_wow:
        wow_by_seg = {c['seg']: c.get('wow', 1) for c in cat}
        for seg, wow in wow_by_seg.items():
            if wow >= 2 and seg in rule_scores:
                rule_scores[seg] -= 0.9 * wow * 0.5
                why_map[seg].append('纯审美减半')
    # P4: 查询零内容(rule 全零 + bigram 覆盖弱)时, 纯审美调权减半——防"好看"一词让 wow3 尾部垄断
    if wow_mode == 'up' and max(rule_scores.values(), default=0) <= 0             and max(lex2.values(), default=0) < 0.25:
        wow_mode = 'up_weak'
        wow_by_seg = {c['seg']: c.get('wow', 1) for c in cat}
        for seg, wow in wow_by_seg.items():
            if wow >= 2 and seg in rule_scores:
                rule_scores[seg] -= 0.9 * wow * 0.5
                why_map[seg].append('纯审美减半')
    sem, sem_backend = {}, None
    if lex:
        channels['lex'] = lex
    # 通道3 sem: bge 行级 max 余弦(可选: 默认 sem=0 关闭——skill 保持零重依赖;
    # 本地装了模型且 _weights.json sem>0 时才启用, 未装自动降级 tfidf)
    if w.get('sem', 0.0) > 0:
        prof2 = {s: dict(p, _type_zh=next((c['type_zh'] for c in cat if c['seg'] == s), ''))
                 for s, p in profiles.items()}
        sem, sem_backend = semantic.scores(q_exp, prof2)
        channels['sem'] = sem
    else:
        sem_backend = None

    # 融合: 语义关=线性(rule + lex_linear×BM25 归一分, R2 验证的最优默认);
    #       语义开=RRF 三通道按排名融合(免归一免调参)
    if sem_backend is None:
        wlex = float(w.get('lex_linear', 2.2))
        w2 = float(w.get('lex2_linear', 0.0))
        fused = {seg: rule_scores.get(seg, 0.0) + wlex * lex.get(seg, 0.0) + w2 * lex2.get(seg, 0.0)
                 for seg in set(rule_scores) | set(lex) | set(lex2)}
    else:
        fused = fusion.weighted_rrf(channels, w, k=k)

    # ---- 融合后叠加: 罚分/解释/反馈 ----
    scored = []
    for c in cat:
        seg = c['seg']
        if seg not in fused:
            continue
        prof = profiles[seg]
        why = list(why_map.get(seg, []))
        s = fused[seg]
        # 反指界限 vs 意图槽位(档案有结构化 constraints 字段则优先, 否则正则解析文本)
        bounds = prof.get('constraints') or query.parse_bounds(prof.get('anti_when'))
        pen, bad = query.constraint_penalty(slots, bounds)
        if pen:
            s += pen * 0.2   # RRF 分数量级 ~1/60, 罚分同步缩放
            why += ['违反反指:%s' % b for b in bad]
        if w.get('lex', 1.0) > 0 and lex.get(seg, 0) > 0.5:
            why.append('BM25%.2f' % lex[seg])
        if sem_backend and w.get('sem', 1.0) > 0 and sem.get(seg, 0) > 0.5:
            why.append('语义%.2f(%s)' % (sem[seg], sem_backend))
        # 用户点名排除的图型: 类型名/触发词命中即重罚(否定窗口在 expand 已滤注入)
        for canon, surface in exclusions:
            if (surface in str(c.get('type_zh', '')) or canon in str(c.get('type_zh', ''))
                    or any(surface in str(t) or canon in str(t) for t in prof.get('triggers', []))):
                s -= 4.0
                why.append('用户排除:%s' % surface)
                break
        cc = dict(c)
        cc['_score'], cc['_why'] = s, why
        cc['_purposes'] = purposes.get('%03d' % seg, [])
        cc['_prof'] = prof
        scored.append(cc)

    # R4a: 反馈信号(展示衰减/口味加权/否决) —— 评测模式(use_log=False)跳过以保证可复现
    if use_log:
        scored = feedback.apply_feedback(scored)
    scored.sort(key=lambda x: -x['_score'])

    # R5: 拒绝机制——三通道全弱时如实说"没有合适的", 比硬凑候选诚实
    # (semantic-router 的空返回 + GPTCache 低阈值教训: 阈值必须保守)
    reject = None
    top5 = [c['seg'] for c in scored[:5]]
    strong_rule = any(rule_scores.get(s, 0) > 0 for s in top5)
    strong_lex = max(lex2.values()) >= 0.25 if lex2 else False   # 查询 bigram 有 ≥1/4 被某档案覆盖
    strong_sem = any(sem.get(s, 0) > 0.55 for s in top5) if sem else False
    if not (strong_rule or strong_lex or strong_sem):
        fam_hint = Counter(c['family'] for c in scored[:9]).most_common(1)
        reject = ('图库里没有和这句话对得上的图。建议换说法(带图型名或数据形状), '
                  '或从用途词入手: %s' % (fam_hint[0][0] if fam_hint else '组间比较'))

    # 推荐模式通道: 数据画像 → 场景 → 按用途匹配加分(用户说不出图型名时的兜底)
    feat, scenarios = (None, {})
    if df is not None:
        try:
            feat, scenarios = datashape.infer_scenarios(df)
        except Exception:
            feat, scenarios = None, {}   # 画像失败仅降级, 不阻塞路由
        # 模糊反指的数据驱动版: 组均值跨度比 <50 时"截断轴"类不该上推荐位; >100 时加分
        num = df.select_dtypes('number')
        span_ratio = None
        if len(num.columns) and len(df):
            mx, mn = float(num.values.max()), float(num.values.min())
            if mn > 0 and mx > 0:
                span_ratio = mx / mn
        for c in scored:
            if '截断' in str(c.get('type_zh', '')) and span_ratio is not None:
                if span_ratio < 50:
                    c['_score'] -= 1.0
                    c['_why'] = c['_why'] + ['数据未跨量级, 截断轴不适']
                elif span_ratio > 100:
                    c['_score'] += 0.5
        # 数据画像当槽位, 让反指约束在推荐模式也能机器比对
        # (意图槽位优先; 数据槽位补足 组数/变量数/样本数/类别数)
        if feat:
            for dim, v in (('组数', feat.get('group_nunique')),
                           ('变量数', feat.get('n_numeric')),
                           ('样本数', feat.get('rows')),
                           ('类别数', feat.get('max_obj_card'))):
                if v and dim not in slots:
                    slots[dim] = int(v)
        w_scen = float(w.get('scen_linear', 1.2))
        for c in scored:
            boost = sum(conf for pur, (conf, _ev) in scenarios.items()
                        if pur in (c.get('_purposes') or []))
            if boost:
                c['_score'] += w_scen * boost * 0.15
                c['_why'] = c['_why'] + ['数据形状:%s' % '/'.join(
                    pur for pur in (c.get('_purposes') or []) if pur in scenarios)]
        scored.sort(key=lambda x: -x['_score'])

    # 数据适配: 只对前 24 个候选做 validate(省时), 重排
    notes = {}
    if df is not None:
        cand = [c['seg'] for c in scored[:24]]
        notes = data_penalty(df, cand)
        # R5 数据画像软约束: 行和≈100/时间列/组列 三条规则的家族加分
        boosts = datashape.shape_boosts(datashape.profile_dataframe(df), purposes)
        for c in scored:
            if c['seg'] in notes:
                d, _ = notes[c['seg']]
                c['_score'] += d * 0.02   # 与 RRF 量纲对齐
            if c['seg'] in boosts:
                c['_score'] += boosts[c['seg']] * 0.15
        scored.sort(key=lambda x: -x['_score'])

    # R4b: MMR 多样性重排(硬约束家族/用途上限 skip-not-drop; 探索槽只在实际路由时启用)
    exposure = feedback.exposure_counts() if use_log else None
    top = diversity.mmr_diversify(scored, n, exposure=exposure,
                                  explore_slot=None if use_log else False)
    # wow3 上限 = top 的一半(至少 2): "怎么画好看"也需要能干活的基础图型兜底,
    # 不能整个领奖台都是展品; 超出由最高分工作马(wow<3)按序补位
    wow_cap = max(2, len(top) // 2)
    if sum(1 for c in top if c.get('wow', 1) >= 3) > wow_cap:
        kept, wow3_kept = [], 0
        for c in top:
            if c.get('wow', 1) >= 3:
                if wow3_kept < wow_cap:
                    kept.append(c); wow3_kept += 1
            else:
                kept.append(c)
        picked_ids = {id(c) for c in kept}
        from collections import Counter as _C
        fam_cnt = _C(c['family'] for c in kept)
        pur_cnt = _C((c.get('_purposes') or ['组间比较'])[0] for c in kept)
        for c in scored:
            if len(kept) >= len(top):
                break
            if id(c) in picked_ids or c.get('wow', 1) >= 3:
                continue
            if fam_cnt[c['family']] >= 2 or pur_cnt[(c.get('_purposes') or ['组间比较'])[0]] >= 3:
                continue
            kept.append(c)
            picked_ids.add(id(c))
            fam_cnt[c['family']] += 1
            pur_cnt[(c.get('_purposes') or ['组间比较'])[0]] += 1
        top = kept
    missing = [c['seg'] for c in cat if c['seg'] not in profiles]
    for c in top:
        c.setdefault('_note', notes.get(c['seg'], ('', ''))[1])
    return top, {'purposes': pur_hits, 'wow_mode': wow_mode, 'profiles': len(profiles),
                 'coverage_missing': missing, 'sem_backend': sem_backend, 'reject': reject,
                 'feat': feat, 'scenarios': scenarios}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('intent', nargs='?', default=None, help='用户的一句话需求(中英皆可); 只记事件时可省')
    ap.add_argument('--data', default=None, help='数据文件(csv/tsv/xlsx/json), 会做契约适配')
    ap.add_argument('--n', type=int, default=9, help='候选数(默认 9, 一轮样板册的量)')
    ap.add_argument('--min-wow', type=int, default=0, choices=[0, 1, 2, 3])
    ap.add_argument('--log', action='store_true', help='把本次展示追加到 route_log.jsonl(防重复)')
    ap.add_argument('--pick', type=int, default=None, help='记录用户选中的 seg(picked 事件, 反馈不罚)')
    ap.add_argument('--veto', type=int, default=None, help='记录用户否决的 seg(vetoed 事件, 反馈重罚)')
    ap.add_argument('--json', action='store_true', help='机器可读输出')
    ap.add_argument('--fresh', action='store_true',
                    help='可复现模式: 不读展示日志/不启用探索槽(评测与对比用)')
    args = ap.parse_args()
    event_only = args.pick is not None or args.veto is not None
    if args.pick is None and args.veto is None and not args.intent and not args.data:
        ap.error('给一句话意图; 说不出图型名时只给 --data 数据文件也可(推荐模式)')
    if event_only and not args.intent:
        top, meta = [], {'purposes': [], 'wow_mode': None, 'profiles': 0,
                         'coverage_missing': [], 'sem_backend': None, 'reject': None,
                         'feat': None, 'scenarios': {}}
    else:
        top, meta = rank(args.intent or '', n=args.n, min_wow=args.min_wow, data=args.data,
                         use_log=not args.fresh)
    profiles = load_all()[1]
    notes = {c['seg']: c.get('_note', '') for c in top}
    pur_hits, wow_mode = meta['purposes'], meta['wow_mode']

    recorded = None
    if args.pick is not None:
        feedback.record_event(args.pick, 'picked')
        recorded = 'picked seg%03d' % args.pick
    if args.veto is not None:
        feedback.record_event(args.veto, 'vetoed')
        recorded = 'vetoed seg%03d' % args.veto
    if args.json:
        print(json.dumps({'intent': args.intent, 'n': len(top), 'reject': meta.get('reject'),
                          'recorded': recorded,
                          'coverage_missing': meta['coverage_missing'][:20],
                          'candidates': [{'seg': c['seg'], 'name': c['type_zh'], 'family': c['family'],
                                          'wow': c.get('wow', 1), 'score': round(c['_score'], 2),
                                          'why': c['_why'], 'note': notes.get(c['seg'], ''),
                                          'use_when': profiles[c['seg']].get('use_when', []),
                                          'anti_when': profiles[c['seg']].get('anti_when', [])}
                                         for c in top]}, ensure_ascii=False, indent=1))
    else:
        recommend_mode = not args.intent
        if recommend_mode:
            feat = meta.get('feat') or {}
            print('推荐模式（基于你的数据画像，不必知道图型名——每张图附直白解释）')
            print('数据: %d 行 × %d 列, 数值列 %d' % (feat.get('rows', 0), feat.get('cols', 0),
                                                     feat.get('n_numeric', 0)))
            scen = meta.get('scenarios') or {}
            if scen:
                print('从数据形状看，可以讲这几个故事:')
                for pur, (conf, ev) in sorted(scen.items(), key=lambda kv: -kv[1][0]):
                    print('  ◆ %s — %s' % (pur, ev))
            else:
                print('（数据形状太特殊，没认出场景——补充一句意图会推荐得更准）')
            print()
        else:
            print('路由: "%s"' % args.intent)
            if meta.get('reject'):
                print('[提示] %s' % meta['reject'])
            print('命中用途: %s | 气质: %s | 档案覆盖: %d/146\n' % (
                '、'.join(pur_hits) or '(未识别)', wow_mode or '中性', meta['profiles']))
        for i, c in enumerate(top):
            tag = chr(ord('A') + i)
            star = '★' * (1 if c.get('wow', 1) >= 3 else 0)
            if recommend_mode:
                plain = profiles[c['seg']].get('plain', '')
                line = '%s. seg%03d %s%s — %s' % (tag, c['seg'], c['type_zh'], star,
                                                  plain or c['type_zh'])
                line += '\n     适合: %s' % (profiles[c['seg']].get('use_when', [''])[0] or '见卡片')
            else:
                line = '%s. seg%03d %s%s (wow%d, %s) — %s' % (
                    tag, c['seg'], c['type_zh'], star, c.get('wow', 1), c['family'],
                    '；'.join(c['_why']) or '备选')
            if notes.get(c['seg']):
                line += '  [%s]' % notes[c['seg']]
            anti = profiles[c['seg']].get('anti_when', [])
            if anti:
                line += '\n     注意: %s' % anti[0]
            print(line)
        items = ' '.join('"%d::%s"' % (c['seg'], c['type_zh']) for c in top)
        print('\n样板册命令:')
        print('python scripts/make_contact_sheet.py sheet --out /tmp/route.png %s --open' % items)

    if recorded and not args.json:
        print('[事件] %s%s' % (recorded, '（已记录, 路由结果不受影响）' if not event_only else ''))
    if args.log:
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'ts': datetime.datetime.now().isoformat(timespec='seconds'),
                                'intent': args.intent, 'data': args.data,
                                'top': [c['seg'] for c in top]}, ensure_ascii=False) + '\n')
        print('\n(已记录到 route_log.jsonl, 连续路由时这些候选会被降权)')


if __name__ == '__main__':
    main()
