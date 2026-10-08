# -*- coding: utf-8 -*-
"""案例113 - Nature 火山图+富集图(三) 2x2:
上=IE vs non-IE (绿下调/黄上调) + 双向条形; 下=NYHA IV vs II,III
(淡紫下调/紫上调) + 双向条形。x=-log10FDR。参考: frames/seg_113.jpg"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from paper_style import *

import matplotlib.pyplot as plt
from matplotlib import patheffects as pe

set_style()
r = rng(113)


def volcano(ax, seed, up_c, dn_c, up_lab, dn_lab, legend, ylab,
            xlab='log$_2$FC (IE/non-IE)', dedup=False,
            legend_loc='lower right'):
    rr = rng(seed)
    n = 1700
    fc = rr.normal(0, 0.85, n).clip(-3.2, 5.2)
    pv = rr.exponential(4.5, n) + 0.9 * np.abs(fc) + rr.uniform(0, 1.5, n)
    pv = np.clip(pv, 0, 37)
    sig = (pv > 2) & (np.abs(fc) > 0.55)
    ax.scatter(fc[~sig], pv[~sig], s=10, color='#bdbdbd', alpha=0.85, lw=0)
    up = sig & (fc > 0)
    dn = sig & (fc <= 0)
    ax.scatter(fc[up], pv[up], s=13, color=up_c, alpha=0.9, lw=0)
    ax.scatter(fc[dn], pv[dn], s=13, color=dn_c, alpha=0.9, lw=0)
    ax.axvline(-0.55, color='0.35', ls='--', lw=0.9)
    ax.axvline(0.55, color='0.35', ls='--', lw=0.9)
    ax.axhline(2, color='0.35', ls='--', lw=0.9)
    # 统一防重叠: 按 y 排序 + 左右分侧最小间距钳制 + 短引线
    labs = [dict(g=g, x=x, y=y, ha=ha) for g, x, y, ha in up_lab + dn_lab]
    if dedup:
        ax_h_pt = ax.get_position().height * fig.get_figheight() * 72
        yspan = ax.get_ylim()[1] - ax.get_ylim()[0]
        gap = (7 * 1.25 + 1.6) / ax_h_pt * yspan   # 标签行高+pad → 数据单位
        for side in ('L', 'R'):
            idxs = sorted([i for i, lb in enumerate(labs)
                           if (lb['x'] < 0) == (side == 'L')],
                          key=lambda i: labs[i]['y'])
            prev = -1e9
            for i in idxs:
                ynew = max(labs[i]['y'], prev + gap)
                labs[i]['ynew'] = ynew
                prev = ynew
    for lb in labs:
        col = up_c if (lb['x'] > 0.5 or (lb['x'] > 0 and lb['ha'] == 'left')) else dn_c
        ynew = lb.get('ynew', lb['y'])
        # 白色描边光晕: 标签压在散点上仍清晰可读
        halo = [pe.Stroke(linewidth=2.2, foreground='white'), pe.Normal()]
        ax.text(lb['x'], ynew, italic_gene(lb['g']), fontsize=7, ha=lb['ha'],
                va='center', color=col, zorder=5, path_effects=halo)
        if ynew - lb['y'] > 1.0:   # 被钳制移位明显 → 画短引线连回原位
            ax.plot([lb['x'], lb['x']], [lb['y'] + 0.35, ynew - 1.0],
                    color=col, lw=0.6, zorder=4,
                    path_effects=[pe.Stroke(linewidth=1.6, foreground='white'),
                                  pe.Normal()])
    # 图例框
    handles = []
    from matplotlib.lines import Line2D
    for lab, c, mk in legend:
        handles.append(Line2D([], [], marker=mk, ls='none', color=c,
                              markersize=5, label=lab))
    ax.legend(handles=handles, loc=legend_loc, fontsize=7,
              frameon=True, framealpha=0.9, edgecolor='0.5',
              borderpad=0.5, handlelength=1.2)
    ax.set_xlim(-3.3, 5.4)
    ax.set_ylim(0, 38)
    ax.set_xticks([-2, 0, 2, 4])
    ax.set_yticks([0, 10, 20, 30])
    ax.tick_params(labelsize=7.5)
    ax.set_xlabel(xlab, fontsize=8.5)
    ax.set_ylabel(ylab, fontsize=8.5)


def diverging(ax, up_rows, dn_rows, up_c, dn_c, xlim, xticks):
    n = len(up_rows) + len(dn_rows)
    ys = list(range(n - 1, -1, -1))
    ysu = ys[:len(up_rows)]
    ysd = ys[len(up_rows):]
    ax.barh(ysu, [v for _, v in up_rows], height=0.62, color=up_c)
    ax.barh(ysd, [-v for _, v in dn_rows], height=0.62, color=dn_c)
    for y_, (lab, v) in zip(ysu, up_rows):
        ax.text(v + 0.25, y_, lab, fontsize=6.8, va='center', ha='left')
    for y_, (lab, v) in zip(ysd, dn_rows):
        ax.text(0.25, y_, lab, fontsize=6.8, va='center', ha='left')
    ax.axvline(0, color='0.2', lw=0.9)
    ax.set_xlim(*xlim)
    ax.set_ylim(-2.9, n - 0.4)
    ax.set_xticks(xticks)
    ax.tick_params(labelsize=7.5)
    ax.set_xlabel('-log$_{10}$FDR', fontsize=8.5)
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.set_yticks([])


fig = plt.figure(figsize=cm2in(18, 15))
gs = fig.add_gridspec(2, 2, left=0.075, right=0.965, top=0.96, bottom=0.075,
                      wspace=0.30, hspace=0.42)

# ---------------- 上排: IE vs non-IE ----------------
ax1 = fig.add_subplot(gs[0, 0])
volcano(ax1, 1131, '#e8c22e', '#4ba83c',
        [('CRP', 3.3, 33, 'left'), ('SAA1', 4.3, 31, 'left'),
         ('SAA2', 4.5, 29.5, 'left'), ('AHSG', 2.6, 24, 'left'),
         ('HP', 2.4, 21, 'left'), ('ACTB', 1.5, 17.5, 'left')],
        [('APOA1', -2.5, 35, 'left'), ('APOC1', -2.35, 32.5, 'left'),
         ('APOA2', -2.1, 31, 'left'), ('TGLI2', -1.6, 29.5, 'left'),
         ('RERG', -1.75, 26, 'left'), ('RMC1', -1.3, 24.5, 'left'),
         ('SNRPD1', -2.25, 22, 'left'), ('ABCE1', -1.7, 21, 'left'),
         ('CNK1', -1.0, 20, 'left')],
        [('upregulated in IE', '#e8c22e', 's'),
         ('not-significant', '#bdbdbd', 's'),
         ('downregulated in IE', '#4ba83c', 's')],
        '-log$_{10}$ FDR')
ax1.text(4.15, 33.5, '$\\cdot$', fontsize=9)
ax2 = fig.add_subplot(gs[0, 1])
diverging(ax2,
          [('Neutrophil_extracellular_trap_formation', 10.6),
           ('Complement_activation_classical_pathway', 10.1),
           ('Immunoglobulin_production', 6.4),
           ('Microtubule_based_process', 5.4),
           ('Complement_and_coagulation_cascades', 4.6),
           ('Cell_motility', 4.2), ('Innate_immune_response', 3.9),
           ('Mesenchymal_migration', 3.6), ('Acute_phase_response', 3.4),
           ('ECM_receptor_interaction', 1.3)],
          [('Plasma_lipoprotein_clearance', 5.5),
           ('Plasma_lipoprotein_assembly_remodeling', 4.7),
           ('Protein_ubiquitination', 3.9), ('Mitophagy', 3.2),
           ('Modification_dependent_protein_catabolic_process', 2.9)],
          '#e8c22e', '#4ba83c', (-6.5, 13.5), [-5, 0, 5, 10])
from matplotlib.lines import Line2D
ax2.legend(handles=[Line2D([], [], marker='s', ls='none', color='#e8c22e',
                           markersize=6, label='upregulated in IE'),
                    Line2D([], [], marker='s', ls='none', color='#4ba83c',
                           markersize=6, label='downregulated in IE')],
           loc='lower left', fontsize=7, frameon=False)

# ---------------- 下排: NYHA IV vs II,III ----------------
# 标注减半(上7→4, 下6→3) + 统一防重叠钳制; 图例移到右上角, 与标注带脱开
ax3 = fig.add_subplot(gs[1, 0])
volcano(ax3, 1133, '#5b2d8e', '#b8a0d8',
        [('VSIG4', 0.9, 4.1, 'left'), ('MIF4GD', 1.35, 3.6, 'left'),
         ('CD163', 1.25, 3.35, 'left'), ('ARHGEF1', 1.45, 3.1, 'left')],
        [('APOA1', -2.6, 3.85, 'left'), ('SERPINC1', -2.95, 2.9, 'left'),
         ('TTR', -2.45, 3.05, 'left')],
        [('down-regulated', '#b8a0d8', 's'),
         ('not-significant', '#bdbdbd', 's'),
         ('up-regulated', '#5b2d8e', 's')],
        '-log$_{10}$ p value', dedup=True, legend_loc='upper right')
ax3.set_xlabel('log$_2$FC(NYHA class IV / class II, III)', fontsize=8.5)
ax4 = fig.add_subplot(gs[1, 1])
diverging(ax4,
          [('Neutrophil_degranulation', 4.6),
           ('Intracellular_protein_transport', 3.1),
           ('Signaling_by_Rho_GTPases', 2.7),
           ('Mitotic_prometaphase', 2.5), ('Spliceosome', 1.7)],
          [('Negative_regulation_of_endopeptidase_activity', 5.9),
           ('Complement_and_coagulation', 4.4),
           ('Vitamin_transport', 2.6), ('Platelet_degranulation', 2.3)],
          '#5b2d8e', '#b8a0d8', (-6.5, 6.5), [-5, 0, 5])
ax4.legend(handles=[Line2D([], [], marker='s', ls='none', color='#5b2d8e',
                           markersize=6, label='upregulated'),
                    Line2D([], [], marker='s', ls='none', color='#b8a0d8',
                           markersize=6, label='downregulated')],
           loc='lower left', fontsize=7, frameon=False)

save(fig, 'case_seg113.png')
