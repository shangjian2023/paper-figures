# -*- coding: utf-8 -*-
"""索引重建器: 从 catalog.json 重建 gallery/index.md(项目) 与 reference/gallery-index.md(skill)。

索引头部列用途词与张数(供选图时 grep), 每图一行: seg/案例/类型/用途/参考图。
用法: python scripts/build_index.py [--root DIR] [--prune]
  --prune: 删除 catalog 中已不存在的卡片/缩略图残留
"""
import json
import os
import glob
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

FAM_NAMES = {
    'bar': '柱形/条形', 'scatter': '散点/排序/降维', 'distribution': '分布(箱线/小提琴/云雨/蜂群)',
    'heatmap': '热图/点阵/相关矩阵', 'volcano': '火山/森林/曼哈顿/富集', 'curve': '曲线/时序',
    'ridge': '山脊/密度/等高线', 'flow': '流程/网络/桑基/UpSet/和弦/三元', 'polar': '极坐标/雷达/环形',
    'tree_geo': '发育树/地图/组合'}


def purposes_of(seg, purpose_map):
    return purpose_map.get('%03d' % seg, [])


def build_index(cat, purpose_map, preview_prefix):
    fams = {}
    for c in cat['cases']:
        fams.setdefault(c['family'], []).append(c)
    purpose_cnt = {}
    for c in cat['cases']:
        for t in purposes_of(c['seg'], purpose_map):
            purpose_cnt[t] = purpose_cnt.get(t, 0) + 1
    out = ['# Gallery 索引 — %d 个案例参考图\n\n' % len(cat['cases']),
           '用途词（grep 这些词筛图）：%s\n\n' % '、'.join(
               '%s(%d)' % (k, v) for k, v in sorted(purpose_cnt.items(), key=lambda kv: -kv[1]))]
    # 高级感速查(wow=3): 用户要"高级/惊艳"时从这里起手
    wow3 = sorted((c for c in cat['cases'] if c.get('wow', 1) >= 3), key=lambda c: c['seg'])
    out.append('高级感 TOP（wow=3 镇场级，%d 张；下表类型栏标 ★）：\n\n' % len(wow3))
    out.append('、'.join('%03d %s' % (c['seg'], c['type_zh']) for c in wow3))
    out.append('\n\n')
    for fam in ['bar', 'distribution', 'scatter', 'heatmap', 'volcano', 'curve', 'ridge', 'flow', 'polar', 'tree_geo']:
        cs = sorted(fams[fam], key=lambda c: c['seg'])
        out.append('\n## %s（%s，%d 例）\n\n' % (fam, FAM_NAMES[fam], len(cs)))
        out.append('| seg | 案例 | 类型 | 用途 | 参考 |\n|---|---|---|---|---|\n')
        for c in cs:
            star = ' ★' if c.get('wow', 1) >= 3 else ''
            out.append('| %03d | %s | %s%s | %s | [%s](%sgallery/case_seg%03d.png) |\n' % (
                c['seg'], c['case'], c['type_zh'], star,
                '、'.join(purposes_of(c['seg'], purpose_map)) or '组间比较',
                c.get('preview', 'gallery/case_seg%03d.png' % c['seg']), preview_prefix, c['seg']))
    return ''.join(out)


def load_catalog(root):
    for p in (os.path.join(root, 'catalog.json'),
              os.path.join(root, 'reference', 'catalog.json')):
        if os.path.exists(p):
            return json.load(open(p, encoding='utf-8'))
    raise FileNotFoundError('catalog.json not found under ' + root)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=ROOT)
    ap.add_argument('--prune', action='store_true')
    args = ap.parse_args()
    root = args.root
    cat = load_catalog(root)
    pm_path = os.path.join(root, 'gallery', 'cards', '_purposes.json')
    purpose_map = json.load(open(pm_path, encoding='utf-8')) if os.path.exists(pm_path) else {}

    idx = build_index(cat, purpose_map, '../')
    open(os.path.join(root, 'gallery', 'index.md'), 'w', encoding='utf-8').write(idx)
    skill_idx = os.path.join(root, 'reference', 'gallery-index.md')
    if os.path.isdir(os.path.dirname(skill_idx)):
        open(skill_idx, 'w', encoding='utf-8').write(build_index(cat, purpose_map, '../'))

    if args.prune:
        valid = {'case_seg%03d.png' % c['seg'] for c in cat['cases']}
        for f in glob.glob(os.path.join(root, 'gallery', 'case_seg*.png')):
            if os.path.basename(f) not in valid:
                os.remove(f)
                print('pruned', f)
    print('index rebuilt at gallery/index.md')


if __name__ == '__main__':
    main()
