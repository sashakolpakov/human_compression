"""Readable full50-original consolidation; no lifecycle claims in the PDF."""
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
Overview v16: incidence operators and codes\end{center}
There are 19 topics and 50 recovered originals among 106 accessible originals; 56 remain pending and 55 earlier indexed originals remain archived. LCD adds L050 and F017. All 18 previous topic records and 48 individual records retain their exact v15 boundaries and all 66 prior factors. The complete LCD factor is $58,756/99,186=0.592382$: written expansion, not achieved whole-topic compression.

For each topic the complete written factor is $\sum_i c(S_i)/(c(U)+\sum_i c(A_i))$. Whole common theory and all complete applications are paid once within that topic. Each row retains its independently adopted nonwhitespace-character coordinate; there is no cross-topic discount, pooled factor or inferred minimum proof complexity. Concrete software listings are excluded on both sides. Proof and mathematical algorithm prose remain counted.
\begin{center}\small\begin{tabular}{lrrrrr}\toprule
Topic & Originals & Sources & Common & Applications & Factor\\\midrule
'''+topics+r'''
\bottomrule\end{tabular}\end{center}
The \href{topics.csv}{19-topic CSV} and \href{applications.csv}{50-original CSV} preserve exact fractions, complete component lengths and historical observations. Factors below one remain visible. The source maps and separate admissions determine the recovered principal contracts; this numerical overview adds no separate proof or question credit.
\newpage
\section*{Individual comparisons: first 25 originals}
After acquiring the \emph{whole} common theory and all actual required mathematical, computational and data premises, the conditional factor is $c(S_i)/c(A_i)$. The complete local application or companion bundle remains charged.
'''+table(pairs[:25])+r'''
LCD pays its entire 14-page common paper and complete 15-page and 12-page applications: \[32,300+37,432+29,454=99,186.\] The sources total $24,674+34,082=58,756$ characters. Its primary is calibrated selected text, NFC, excluding whitespace. No sibling application is a free premise.

After paying the full common theory, complete required file collection and retained mathematics, L050 has factor $0.659169$ (also expansion) and F017 has factor $1.157126$. Conditional reuse does not undo whole-topic expansion. Optional validation is not a proof premise.
\newpage
\section*{Individual comparisons: remaining 25 originals}
'''+table(pairs[25:])+r'''
LCD retains 54 L050 and 104 F017 source dispositions, including exact corrections and explicitly retained code/classification inputs. The source questions about all SRG$(253,140,87,65)$, the other fifteen-dimensional modules, general further families and efficient decoding are not newly solved. Its source maps define the corrected principal contracts.

The raw inventory discloses 127 occurrences of 102 unique whole contents (548,250 original bytes). The conditional convention conservatively acquires all 83 required programs/certificates/data/finite records, occupying 422,956 original bytes. Three optional validation files, eleven drivers and five partial-formal files are separate; nine inherited generic declarations do not formalize either full source. No software-inclusive factor is computed.

Historical software, retained external proofs, complete graphics and full formalization costs remain unknown. All software-inclusive and pooled factors are null. Operations retains its separate text-only sensitivity; expanded E retains its accepted source qualifications and the source's Magma/$L_2$-quotient attribution. Prior overviews remain historical records.
\newpage
\section*{Whole topics}
Grey bars show the complete original manuscript text in each row's adopted coordinate. Replacement bars stack the entire common theory and all applications. The axis starts at zero; the tables give the ratios.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
The 57 bars account for all 19 topics. No necessary finite certificate or external premise becomes optional merely because software and retained external proof costs are outside the manuscript coordinate.
\newpage
\section*{Conditional lengths: first 25 originals}
Whole common theory and required premises are acquired in advance. Grey and teal bars compare complete source and local application text; the whole-topic table still pays the common theory.
\begin{center}\includegraphics[width=\linewidth]{conditional_1.pdf}\end{center}
\newpage
\section*{Conditional lengths: remaining 25 originals}
All complete companion papers remain charged. The source order is documentary, not an optimal acquisition order or a claimed sawtooth.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
This edition supplies 69 exact manuscript comparisons and 157 plotted bars. The active programme remains 106 originals, with 50 recovered and 56 pending. Only L050 and F017 are newly reflected from their separate scientific admissions; L121 is not admitted by this edition. No new question or priority claim is made.
\end{document}
'''
if __name__=='__main__':(HERE/'reader.tex').write_text(render_text(read('results.json')))
