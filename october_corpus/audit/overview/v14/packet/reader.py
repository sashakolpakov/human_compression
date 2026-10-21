"""Readable full47-original consolidation; no lifecycle claims in the PDF."""
from build import HERE,read

def esc(s):return str(s).replace('&',r'\&').replace('_',r'\_')
def render_text(r):
 topics='\n'.join(f"{esc(t['topic'])} & {t['source_count']} & {t['source_sum']:,} & {t['common_theory']:,} & {t['applications_sum']:,} & {float(t['written']['decimal']):.3f} \\\\"for t in r['topics']);pairs=[(t,a)for t in r['topics']for a in t['pairs']]
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
Overview v14: unified A and three-source Mixes\end{center}
There are 18 topics and 47 recovered originals among 106 accessible originals; 59 remain pending and 55 earlier indexed originals remain archived. A combines the eight originals previously assigned to A and Affine. Mixes now includes F007 alongside F005 and L016. The other 16 topic records and 36 individual records retain their exact v13 boundaries, including expanded E and the symmetric listing corrections.

For each topic the complete written factor is $\sum_i c(S_i)/(c(U)+\sum_i c(A_i))$. Whole common theory and all complete applications are paid once within that topic. Each row retains its independently adopted nonwhitespace-character coordinate; there is no cross-topic discount, pooled factor or inferred minimum proof complexity. Concrete software listings are excluded on both sides. Proof and mathematical algorithm prose remain counted.
\begin{center}\small\begin{tabular}{lrrrrr}\toprule
Topic & Originals & Sources & Common & Applications & Factor\\\midrule
'''+topics+r'''
\bottomrule\end{tabular}\end{center}
The \href{topics.csv}{18-topic CSV} and \href{applications.csv}{47-original CSV} preserve exact fractions, complete component lengths and historical observations. Factors below one remain visible. The source maps and separate admissions determine the recovered principal contracts; this numerical overview adds no separate proof or question credit.
\newpage
\section*{Individual comparisons: first 24 originals}
After acquiring the \emph{whole} common theory and all actual required mathematical, computational and data premises, the conditional factor is $c(S_i)/c(A_i)$. The complete local application or companion bundle remains charged.
'''+table(pairs[:24])+r'''
Unified A pays its full 23-page common paper and all 45 application pages. Its source total is 246,570 characters and its replacement is $66,140+110,576=176,716$, giving $123285/88358$. The primary coordinate remains calibrated selected extraction, NFC, without whitespace. Neither earlier A theory nor earlier Affine theory is free. Graphical structure and unextracted image labels remain unknown costs.

All eleven required program/data files remain required even though software is outside this manuscript factor. Three inherited auxiliary files, two current drivers and fourteen partial formal files remain separately inventoried. Their whole-file costs are preserved; no full-formalization claim or software-inclusive factor follows.
\newpage
\section*{Individual comparisons: remaining 23 originals}
'''+table(pairs[24:])+r'''
Mixes pays three common papers: $12,615+11,641+10,501=34,757$. The complete applications cost 31,077 for F005, 15,125 for L016 and 22,491 for F007. Thus its full comparison is $156570/(34757+68693)=15657/10345$. Its primary is raw untrimmed extraction, NFC, without whitespace. Both required finite certificates remain required; the REQ appendix prints both files. Six validation programs remain optional; six drivers and three partial formal files are separately inventoried.

F005's three final problems remain unanswered. L016 retains the faithful repair of its thin-cover lemma and its ancillary exclusions. F007's page-25 chain-class paragraph is not recovered; Problems 1 and 2 remain unanswered. Its Problem 3 result has the stated natural-reconstruction and finite connected-flag-graph scope, with no general infinite or priority claim. Twelve partial Lean declarations are not full source formalization.

Historical software, retained external proofs, complete graphics and full formalization costs remain unknown. All software-inclusive and pooled factors are null. Operations retains its separate text-only sensitivity; expanded E retains its accepted source qualifications and the source's Magma/$L_2$-quotient attribution. Prior overviews remain historical records.
\newpage
\section*{Whole topics}
Grey bars show the complete original manuscript text in each row's adopted coordinate. Replacement bars stack the entire common theory and all applications. The axis starts at zero; the tables give the ratios.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
The 54 bars account for all 18 topics. No necessary finite certificate or external premise becomes optional merely because software and retained external proof costs are outside the manuscript coordinate.
\newpage
\section*{Conditional lengths: first 24 originals}
Whole common theory and required premises are acquired in advance. Grey and teal bars compare complete source and local application text; the whole-topic table still pays the common theory.
\begin{center}\includegraphics[width=\linewidth]{conditional_1.pdf}\end{center}
\newpage
\section*{Conditional lengths: remaining 23 originals}
All complete companion papers remain charged. The source order is documentary, not an optimal acquisition order or a claimed sawtooth.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
This edition supplies 65 exact written comparisons and 148 plotted bars. The active programme remains 106 originals, with 47 recovered and 59 pending. Only F007 is newly reflected from its separate scientific admission; the A--Affine merger changes topic organization, not the number of originals.
\end{document}
'''
if __name__=='__main__':(HERE/'reader.tex').write_text(render_text(read('results.json')))
