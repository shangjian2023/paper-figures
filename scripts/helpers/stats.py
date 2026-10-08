# -*- coding: utf-8 -*-
"""统计检验助手 — 配方里"写死的星号"换真实数据后由这里实算。

用法:
    from helpers.stats import vs_control
    stars, pvals = vs_control(data_groups, control=0)   # data_groups: [array, ...]
                                                     # control: 对照组下标
- Welch t 检验(各组 vs 对照) + Bonferroni 校正, 返回 '*','**','***','ns' 列表与校正后 p。
- 需要 Dunnett 时若装了 statsmodels 自动用之(更严谨), 否则回退 Bonferroni。
"""
import numpy as np
from scipy import stats


def p_to_stars(p):
    if p < 0.001:
        return '***'
    if p < 0.01:
        return '**'
    if p < 0.05:
        return '*'
    return 'ns'


def vs_control(groups, control=0, two_sided=True):
    """groups: list of 1D arrays; 返回 (stars_list, adjusted_p_list)。
    优先 statsmodels 的 Dunnett(若可用), 否则 Welch t + Bonferroni。"""
    ctrl = np.asarray(groups[control], dtype=float)
    tests = [i for i in range(len(groups)) if i != control]
    try:
        from statsmodels.stats.multicomp import pairwise_dunnett  # noqa
        have_dunnett = True
    except Exception:
        have_dunnett = False
    stars, padj = [], []
    if have_dunnett:
        try:
            from statsmodels.stats.oneway import dunnett  # scipy>=1.11 提供
            res = dunnett(*[np.asarray(groups[i], float) for i in tests],
                          control=ctrl, alternative='two-sided' if two_sided else 'less')
            raw = np.asarray(res.pvalue)
        except Exception:
            have_dunnett = False
    if not have_dunnett:
        raw = np.array([stats.ttest_ind(np.asarray(groups[i], float), ctrl,
                                        equal_var=False).pvalue for i in tests])
        raw = np.minimum(raw * len(tests), 1.0)  # Bonferroni
    it = iter(raw)
    for i in range(len(groups)):
        if i == control:
            stars.append('-')
            padj.append(np.nan)
        else:
            p = next(it)
            padj.append(p)
            stars.append(p_to_stars(p))
    return stars, padj
