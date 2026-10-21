"""Readable full48-original consolidation; no lifecycle claims in the PDF."""
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
Overview v15: two-source Representation\end{center}
There are 18 topics and 48 recovered originals among 106 accessible originals; 58 remain pending and 55 earlier indexed originals remain archived. Representation now includes L126 alongside F010. The other 17 topic records and 46 individual records retain their exact v14 boundaries. The complete Representation factor is $60,472/82,152=0.736099$: written expansion, not achieved whole-topic compression.

For each topic the complete written factor is $\sum_i c(S_i)/(c(U)+\sum_i c(A_i))$. Whole common theory and all complete applications are paid once within that topic. Each row retains its independently adopted nonwhitespace-character coordinate; there is no cross-topic discount, pooled factor or inferred minimum proof complexity. Concrete software listings are excluded on both sides. Proof and mathematical algorithm prose remain counted.
\begin{center}\small\begin{tabular}{lrrrrr}\toprule
Topic & Originals & Sources & Common & Applications & Factor\\\midrule
'''+topics+r'''
\bottomrule\end{tabular}\end{center}
The \href{topics.csv}{18-topic CSV} and \href{applications.csv}{48-original CSV} preserve exact fractions, complete component lengths and historical observations. Factors below one remain visible. The source maps and separate admissions determine the recovered principal contracts; this numerical overview adds no separate proof or question credit.
\newpage
\section*{Individual comparisons: first 24 originals}
After acquiring the \emph{whole} common theory and all actual required mathematical, computational and data premises, the conditional factor is $c(S_i)/c(A_i)$. The complete local application or companion bundle remains charged.
'''+table(pairs[:24])+r'''
Representation pays the complete 13-page shared theory and both applications of four and twelve pages: \[36,715+10,985+34,452=82,152.\] The sources total $25,348+35,124=60,472$ characters. The primary remains calibrated selected text, NFC, excluding whitespace. The finite-normal-pair existence proof is now fully in the common paper; no sibling application is free.

After paying whole U and retained premises, F010 has factor $2.307510$; L126 has factor $1.019505$. These conditional reuse figures do not undo the expansion of the full proof. L126 additionally requires the complete graph certificate and full 19,326-byte JSON; nine validation programs are optional.
\newpage
\section*{Individual comparisons: remaining 24 originals}
'''+table(pairs[24:])+r'''
The Representation source contract retains six F010 blocks and 31 L126 dispositions, with finite-field/small-case corrections and an explicit chamber-connectivity hypothesis for splitting. The broader Section 6.2 and Section 8 programmes remain unresolved. The exact source editions and independent proof/input/numerical records are linked by its admission.

The 16-page program appendix prints all ten programs. Its 35,723 characters and the raw programs' 34,823 are alternatives, never added twice. The mandatory JSON contributes 19,315 raw nonspace characters separately; it is not replaced by the appendix. Two current helpers and four partial Lean modules/22 declarations are separate inventories. Neither full source is formalized.

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
\section*{Conditional lengths: remaining 24 originals}
All complete companion papers remain charged. The source order is documentary, not an optimal acquisition order or a claimed sawtooth.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
This edition supplies 66 exact written comparisons and 150 plotted bars. The active programme remains 106 originals, with 48 recovered and 58 pending. Only L126 is newly reflected from its separate scientific admission; F010 was already admitted. No new question or priority claim is made.
\end{document}
'''
if __name__=='__main__':(HERE/'reader.tex').write_text(render_text(read('results.json')))
