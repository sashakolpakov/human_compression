"""Readable whole-document overview with exact historical and current tables."""
from build import HERE,read

def esc(s):return str(s).replace('&',r'\&').replace('_',r'\_')
def render_text(r):
 topics='\n'.join(f"{esc(t['topic'])} & {t['source_count']} & {t['source_sum']:,} & {t['common_theory']:,} & {t['applications_sum']:,} & {float(t['written']['decimal']):.3f} \\\\"for t in r['topics'])
 pairs=[(t,a)for t in r['topics']for a in t['pairs']]
 def table(rows):
  body='\n'.join(f"{a['source']} & {esc(t['topic'])} & {a['source_cost']:,} & {a['application_cost']:,} & {float(a['conditional']['decimal']):.3f} \\\\"for t,a in rows)
  return r'''\begin{center}\small\begin{tabular}{llrrr}\toprule
Original & Topic & Source & Application & Factor\\\midrule
'''+body+r'''\bottomrule\end{tabular}\end{center}'''
 return r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=27mm]{geometry}
\usepackage{fontspec,booktabs,array,hyperref,graphicx}
\setmainfont{STIXGeneral}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\begin{document}
\begin{center}{\Large Complete manuscript comparison}\\[3pt]
Overview v12: symmetric manuscript counts\end{center}
This additive edition restores three whole-topic comparisons and the three affected individual comparisons after exact executable-listing exclusions on both sides. It retains 19 topics and 43 recovered originals among 106 accessible originals; 63 remain pending. Scientific admissions, required proof inputs and the 55 archived originals are unchanged. Expanded E and enlarged Mixes are outside this edition.

The complete written factor is $\sum_i c(S_i)/(c(U)+\sum_i c(A_i))$ within each topic: the whole common paper and every complete application are paid. No theory is free because another topic proves a similar statement. The primary unit is characters without whitespace; each topic retains its published source representation and extraction convention. These are observed manuscript costs, not minimum proof complexities. No pooled factor is formed.
\begin{center}\small\begin{tabular}{lrrrrr}\toprule
Topic & Originals & Sources & Common & Applications & Factor\\\midrule
'''+topics+r'''
\bottomrule\end{tabular}\end{center}
The exact 19-row \href{topics.csv}{topic CSV} retains historical costs and fractions alongside current values. Chamber, ChiralEnumeration and Operations now use the matched listing boundary. The other 16 topic records are unchanged. A factor below one remains visible.
\newpage
\section*{Individual comparisons: first 22 originals}
After acquiring the \emph{whole} common theory and all required proof, program and data premises for that topic, the conditional factor is $c(S_i)/c(A_i)$. Every complete local application or companion bundle is charged. Optional validation is not relabeled as a premise.
'''+table(pairs[:22])+r'''
Only L008, L028 and N006 change. Their source listings were previously included while replacement code was excluded. Current source costs remove the exact reviewed blocks; application costs remain unchanged. The other 40 conditional fractions retain their earlier values, including N016, N005 and N007. All 43 rows, exact fractions and acquisition conditions are in \href{applications.csv}{applications.csv}.

Programs implementing proofs keep that logical role even when their listing text is excluded symmetrically from a manuscript comparison. The complete program and mandatory-data inventories remain separately bound. There is no software-inclusive or optional-validation-inclusive scalar: historical source software costs are unknown.
\newpage
\section*{Individual comparisons: remaining 21 originals}
'''+table(pairs[22:])+r'''
\textbf{Exact exclusions.} L008: three Magma functions, section 5, physical pages 8--10. L028: the ChiralPolytopes, OrderedSubsetsGroups and DiagramPlus implementations, section 4.2, physical pages 9--12. N006: the McL search pseudocode in the Theorem 5.3 proof, physical page 20. Seven blocks are removed in twelve page chunks; surrounding proof, comments outside those blocks, Lemma 4.5, mathematical algorithm prose, presentations and tables remain. No whole section is discarded.

\textbf{Limits and sensitivity.} The listing audit covers the measured text and supplied replacement TeX; it is not a claim about unseen software or unextracted graphics. Operations retains its proposed text proxies for source diagrams, with a separate text-only sensitivity in the matched numerical packet. That sensitivity is not substituted for the primary coordinate; graphic complexity remains unknown. The matched packet preserves all 30 coordinates per topic, plus ten text-only Operations coordinates. Unknown external proofs, source software, historical costs and complete formalization costs are null, not zero. Partial Lean checks are not full source formalization.

The prior v10 and v11 costs, factors and held statuses remain historical records. This edition supplies current graphs without changing scientific admissions or adding source, question or formalization credit.
\newpage
\section*{Whole topics}
Grey bars show complete original manuscript text under each row's declared convention. Replacement bars stack whole common theory and all applications. The axis starts at zero. These are lengths; ratios are shown in the tables.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
The entire common contribution remains visible, including theory needed only by some applications. The 57 actual bars correspond to all 19 topics.
\newpage
\section*{Conditional lengths: first 22 originals}
The common theory and required premises are acquired in advance. Grey and teal bars compare complete source and local application text; they do not remove that prerequisite cost from the whole-topic table.
\begin{center}\includegraphics[width=\linewidth]{conditional_1.pdf}\end{center}
\newpage
\section*{Conditional lengths: remaining 21 originals}
The acquisition condition is identical for every row. There is no cross-topic discount and no inferred sawtooth or node-count factor.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
\end{document}
'''
if __name__=='__main__':(HERE/'reader.tex').write_text(render_text(read('results.json')))
