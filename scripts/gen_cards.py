# -*- coding: utf-8 -*-
"""鉴赏卡片生成器: 从 catalog.json 为每个案例生成 gallery/cards/case_segNNN.md。

卡片格式对齐 plot-is-all-you-need 的词表:
  frontmatter: title/kind/purpose/data/journal/recipe/preview/reference/pitfalls
  body: 一句话点评 + 部件亮点 + 复现提示
用法: python scripts/gen_cards.py [--root DIR]
"""
import json
import os
import re
import glob
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

# 用途词表(选图时按这些词 grep)
PURPOSE_RULES = [
    (r'堆积|镜像100|构成', ['构成占比']),
    (r'三元', ['构成占比', '相关关系']),
    (r'火山|森林|曼哈顿|差异', ['差异展示', '排序']),
    (r'地图|地理|发育树|进化', ['空间分布']),
    (r'桑基|冲击|和弦|网络|UpSet|circos|放射状', ['网络与流向']),
    (r'雷达|环形柱|环状|参与者|内向环形', ['多指标综合']),
    (r'山脊|密度|等高线|云雨|箱线|小提琴|蜂群|泳道', ['分布形态', '组间比较']),
    (r'UMAP|PCoA|NMDS|排序|拟合气泡', ['排序降维']),
    (r'相关|cluster|pairs|配对矩阵|Mantel|点阵', ['相关关系']),
    (r'时间序列|折线|曲线|剂量|响应|RCS|点线', ['趋势变化']),
    (r'FC-FC|哑铃|strip', ['组间比较', '差异展示']),
]

FAMILY_FALLBACK = {
    'bar': ['组间比较'], 'scatter': ['相关关系'], 'distribution': ['分布形态', '组间比较'],
    'heatmap': ['相关关系'], 'volcano': ['差异展示'], 'curve': ['趋势变化'],
    'ridge': ['分布形态'], 'flow': ['网络与流向'], 'polar': ['多指标综合'],
    'tree_geo': ['空间分布'],
}


def purposes_of(c):
    text = c['type_zh'] + ' ' + c.get('title', '')
    out = []
    for pat, tags in PURPOSE_RULES:
        if re.search(pat, text):
            out += [t for t in tags if t not in out]
    if not out:
        out = FAMILY_FALLBACK.get(c['family'], ['组间比较'])
    return out[:3]


CARD_BODY = """**一句话**：{summary}

**高级感**：{wow}

**适用场景**：{scene}

**有什么用**：{plain}

**部件亮点**
- 结构布局：{layout}
- 编码方式：{encoding}

**复现**：配方 `{recipe}` 可直接运行（合成数据，seed 固定）；换真实数据时保持列语义一致。
"""

WOW_LABEL = {3: '★★★ 镇场级（用户要"高级/惊艳"时优先摆）',
             2: '★★ 有设计感',
             1: '★ 常规扎实'}


def summarize(c):
    t = c['type_zh']
    j = c.get('journal', '')
    return '%s（%s 风格）' % (t, j) if j and j != '未标注' else t


def layout_of(c):
    p = c.get('panels', '')
    return p if p else '单面板'


def encoding_of(c):
    f = c.get('features', '')
    return (f[:110] + '…') if len(f) > 110 else f


def load_catalog(root):
    for p in (os.path.join(root, 'catalog.json'),
              os.path.join(root, 'reference', 'catalog.json')):
        if os.path.exists(p):
            return json.load(open(p, encoding='utf-8'))
    raise FileNotFoundError('catalog.json not found under ' + root)


def load_scene(root):
    """路由档案(reference/routing/segNNN.json)的 use_when[0] 与 plain, 缺档案返回空。"""
    rd = os.path.join(root, 'reference', 'routing')
    if not os.path.isdir(rd):
        return {}, {}
    scene, plain = {}, {}
    for p in glob.glob(os.path.join(rd, 'seg*.json')):
        try:
            r = json.load(open(p, encoding='utf-8'))
            uw = r.get('use_when') or []
            if uw:
                scene[int(r['seg'])] = uw[0]
            if r.get('plain'):
                plain[int(r['seg'])] = r['plain']
        except Exception:
            continue
    return scene, plain


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=ROOT)
    args = ap.parse_args()
    root = args.root
    cat = load_catalog(root)
    scene, plain_map = load_scene(root)
    schemas = {}
    sp = os.path.join(root, 'reference', 'data-schemas.json')
    if os.path.exists(sp):
        schemas = json.load(open(sp, encoding='utf-8'))['schemas']
    cards_dir = os.path.join(root, 'gallery', 'cards')
    os.makedirs(cards_dir, exist_ok=True)
    n = 0
    for c in cat['cases']:
        s = c['seg']
        purpose = purposes_of(c)
        data = c.get('data', '')
        fm = [
            'title: %s' % c['title'],
            'kind: 数据图',
            'purpose: [%s]' % ', '.join(purpose),
            'data: %s' % data.replace('\n', ' '),
            'input: %s (reference/data-schemas.json #%03d)' % (schemas.get('%03d' % s, {}).get('format', 'long'), s),
            'journal: %s' % c.get('journal', ''),
            'wow: %d' % c.get('wow', 1),
            'recipe: scripts/recipes/case_seg%03d.py' % s,
            'preview: ../case_seg%03d.png' % s,
        ]
        body = CARD_BODY.format(
            summary=summarize(c), layout=layout_of(c), encoding=encoding_of(c),
            wow=WOW_LABEL.get(c.get('wow', 1), WOW_LABEL[1]),
            scene=scene.get(s, '（路由档案待补：跑 reference/routing 档案流程后重生成卡片）'),
            plain=plain_map.get(s, '（审计待补 plain 字段）'),
            recipe='scripts/recipes/case_seg%03d.py' % s)
        open(os.path.join(cards_dir, 'case_seg%03d.md' % s), 'w', encoding='utf-8').write(
            '---\n' + '\n'.join(fm) + '\n---\n\n' + body)
        n += 1
    # 用途词统计（写进索引头部供 grep 选图）
    from collections import Counter
    cnt = Counter()
    for c in cat['cases']:
        for t in purposes_of(c):
            cnt[t] += 1
    print('cards written:', n)
    print('purpose stats:', dict(cnt.most_common()))
    json.dump({'%03d' % c['seg']: purposes_of(c) for c in cat['cases']},
              open(os.path.join(root, 'gallery', 'cards', '_purposes.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
