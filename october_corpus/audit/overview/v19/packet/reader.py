"""Readable nineteen-topic overview, with the editorial disposition separate."""
from decimal import Decimal,localcontext
from build import HERE,read
def esc(s):return str(s).replace('&',r'\&').replace('_',r'\_')
def shown(f,places=3):
 with localcontext()as c:c.prec=50;return format(Decimal(f['numerator'])/Decimal(f['denominator']),'.'+str(places)+'f')
def render_text(r):
 topics='\n'.join(f"{esc(t['topic'])} & {t['source_count']} & {t['source_sum']:,} & {t['common_theory']:,} & {t['applications_sum']:,} & {shown(t['written'])} \\\\"for t in r['topics']);pairs=[(t,a)for t in r['topics']for a in t['pairs']]
 def table(rows):
  body='\n'.join(f"{a['source']} & {esc(t['topic'])} & {a['source_cost']:,} & {a['application_cost']:,} & {shown(a['conditional'])} \\\\"for t,a in rows)
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
Overview v19: hexagonal extensions and shared periods\end{center}
This edition covers 19 topics and 53 measured originals. The 106 accessible originals comprise 53 measured mathematical originals, 52 awaiting mathematical recovery and measurement, and one editorial, L022. The 55 unavailable originals remain archived. L022 contains no principal mathematical result to recover: it stays accessible, with no factor or measured credit.

L003 joins A. All 18 other topic records and 51 earlier individual records retain their exact v18 values. A's complete factor decreases from $1.354347$ to $1.210825$. L121's local factor becomes $12.288729$, because its proofs move into the fully charged common supplement; the new L003 conditional is $1.063284$. The complete factor is $\sum_i c(S_i)/(c(U)+\sum_i c(A_i))$: the entire common theory and all complete applications are paid once within each topic.

Each topic retains its adopted nonwhitespace-character coordinate. There is no pooled factor or cross-topic deduction, and no inferred minimum proof length. Executable software is excluded on both sides; mathematical proof and algorithm prose remain counted.
\begin{center}\small\begin{tabular}{lrrrrr}\toprule
Topic & Originals & Sources & Common & Applications & Factor\\\midrule
'''+topics+r'''
\bottomrule\end{tabular}\end{center}
The \href{topics.csv}{19-topic CSV} and \href{applications.csv}{53-original CSV} preserve exact fractions and complete component costs. Factors below one mean written expansion and remain visible. The separate source admissions define the corrected principal contracts; this overview creates no additional proof, question or formalization credit.
\newpage
\section*{Individual comparisons: first 27 originals}
The conditional factor is $c(S_i)/c(A_i)$ after acquiring the \emph{whole} common theory and all actual required mathematical, computational and data premises. Every complete local application or companion bundle remains charged.
'''+table(pairs[:27])+r'''
A pays three complete common manuscripts (23+14+4 pages), eight unchanged applications (45 pages), the complete one-page L121 adapter, and all four L003 application papers (7+4+4+2 pages):
\[R_A=\frac{319,016}{108,271+155,199}=1.210825.\]
The common addition costs 42,131 characters. The moved L121 proofs reduce its local application by 23,322 characters; the new L003 bundle adds 42,396. The net replacement increase is 61,205. Each complete proof remains charged.
\newpage
\section*{Individual comparisons: remaining 26 originals}
'''+table(pairs[27:])+r'''
A's separate inventory contains 203 complete contents from 253 occurrences: 28 required programs, 71 required data, 17 operational files, five optional validations, 16 partial formal files and 66 output receipts. All 99 required contents remain prerequisites. The old printed appendices cover only an eleven-file subset; there is no complete enlarged printed-code factor. Overlapping roles are retained without adding them as disjoint costs.

L003's complete corrected contract preserves all 125 source dispositions, including 73 table rows. Corrected orders, nonsplitting, local-period qualifications and the correlation hypotheses remain explicit. The source's experimental diagram-(5) flag-transitivity/existence claim and questions receive no new answer. Drawing-font aliases remain literal representation tokens; complete graphics and unextracted labels are not priced.

All software-inclusive and pooled factors remain null. Historical software, external proofs, complete graphics and full formalization costs are unknown. Operations retains its text-only sensitivity; E retains the source's Magma/$L_2$-quotient attribution and all source qualifications. Prior overviews remain historical records.
\newpage
\section*{Whole topics}
Grey bars show the complete originals in each row's adopted coordinate. Replacement bars stack the entire common theory and all applications. The axis starts at zero; the table gives the factors.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
The 57 bars cover all 19 topics. Necessary finite certificates and retained external premises do not become optional because their software or external proof costs are outside this manuscript comparison.
\newpage
\section*{Conditional lengths: first 27 originals}
Whole common theory and required premises are acquired in advance. Grey and teal bars compare complete source and local application text; the whole-topic table still pays the common theory.
\begin{center}\includegraphics[width=\linewidth]{conditional_1.pdf}\end{center}
\newpage
\section*{Conditional lengths: remaining 26 originals}
All complete companion papers remain charged. Source order is documentary, not an optimal acquisition order or a claimed sawtooth.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
This edition supplies 72 exact manuscript comparisons and 163 plotted bars. Root authored the new A10 numerical packet; enumeration\_volume independently reviewed its arithmetic, while disclosing earlier input and numerical-mechanics authorship. The scientific component authors and distinct reviews remain explicit in the complete topic admission. This overview reuses accepted costs. L022 has no mathematical recovery credit or numerical bar; no new conjecture or priority claim is made.
\end{document}
'''
if __name__=='__main__':(HERE/'reader.tex').write_text(render_text(read('results.json')))
