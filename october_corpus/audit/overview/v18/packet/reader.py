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
Overview v18: transitive string markings\end{center}
This edition covers 19 topics and 52 measured originals. The 106 accessible originals comprise 52 measured mathematical originals, 53 awaiting mathematical recovery and measurement, and one editorial, L022. The 55 unavailable originals remain archived. L022 contains no principal mathematical result to recover: it stays accessible, with no factor or measured credit.

L047 joins B. All 18 other whole-topic records and all 51 earlier individual records retain their exact v17 values. B's whole factor changes from $1.094035$ to $0.971866$: the enlarged replacement is a written expansion. The new L047 conditional is $3.629111$, after acquisition of both whole common papers and all required topic premises. The complete written factor for each topic is $\sum_i c(S_i)/(c(U)+\sum_i c(A_i))$: full common theory and all complete applications are paid once within that topic.

Each topic retains its adopted nonwhitespace-character coordinate. There is no pooled factor or cross-topic deduction, and no inferred minimum proof length. Executable software is excluded on both sides; mathematical proof and algorithm prose remain counted.
\begin{center}\small\begin{tabular}{lrrrrr}\toprule
Topic & Originals & Sources & Common & Applications & Factor\\\midrule
'''+topics+r'''
\bottomrule\end{tabular}\end{center}
The \href{topics.csv}{19-topic CSV} and \href{applications.csv}{52-original CSV} preserve exact fractions and complete component costs. Factors below one mean written expansion and remain visible. The separate source admissions define the corrected principal contracts; this overview creates no additional proof, question or formalization credit.
\newpage
\section*{Individual comparisons: first 26 originals}
The conditional factor is $c(S_i)/c(A_i)$ after acquiring the \emph{whole} common theory and all actual required mathematical, computational and data premises. Every complete local application or companion bundle remains charged.
'''+table(pairs[:26])+r'''
B pays the entire old 16-page common paper and the whole 10-page addition, plus all six applications (30 pages):
\[R_B=\frac{144,877}{44,905+29,398+74,768}=0.971866.\]
The replacement is 4,194 characters longer overall. The common addition costs 29,398 characters, separately visible as a new acquisition stage in B's reader. L047 contributes its full twelve-page source and three-page application: $19,971/5,503=3.629111$ conditionally. The five earlier conditional records are unchanged in all thirty coordinates.
\newpage
\section*{Individual comparisons: remaining 26 originals}
'''+table(pairs[26:])+r'''
B's separate inventory contains 17 whole distinct files: eight required or auxiliary programs, two optional validations, five operational drivers and two partial Lean files. The required files occupy 24,859 original bytes. The roster file \texttt{run.g} remains a required premise. Both complete seven-page code appendices and all ten raw programs are disclosed as alternatives; they are not added together or used for a software-inclusive factor.

L047's corrected principal contract retains 23 finer ancillary Table 3 reports as attributed statements, not regenerated results. The source's conjecture was already resolved in L044; this comparison credits no new answer. N001 remains a complete authored rendering, with its original PDF unknown. The source side otherwise retains five whole PDFs, including L040's identification cover. Fourteen inherited Lean declarations remain partial evidence.

All software-inclusive and pooled factors remain null. Historical software, external proofs, complete graphics and full formalization costs are unknown. Operations retains its text-only sensitivity; E retains the source's Magma/$L_2$-quotient attribution and all source qualifications. Prior overviews remain historical records.
\newpage
\section*{Whole topics}
Grey bars show the complete originals in each row's adopted coordinate. Replacement bars stack the entire common theory and all applications. The axis starts at zero; the table gives the factors.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
The 57 bars cover all 19 topics. Necessary finite certificates and retained external premises do not become optional because their software or external proof costs are outside this manuscript comparison.
\newpage
\section*{Conditional lengths: first 26 originals}
Whole common theory and required premises are acquired in advance. Grey and teal bars compare complete source and local application text; the whole-topic table still pays the common theory.
\begin{center}\includegraphics[width=\linewidth]{conditional_1.pdf}\end{center}
\newpage
\section*{Conditional lengths: remaining 26 originals}
All complete companion papers remain charged. Source order is documentary, not an optimal acquisition order or a claimed sawtooth.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
This edition supplies 71 exact manuscript comparisons and 161 plotted bars. The B6 numerical author is enumeration\_volume; root distinctly reviewed and adopted those calculations and their inputs. The new L047 science is by enumeration\_review and the input author is rewrite\_termination. Earlier B authorship and the bounded finite-neighbor review roles remain disclosed in the topic packet. This overview reuses accepted costs. L022 has no mathematical recovery credit or numerical bar; no new conjecture or priority claim is made.
\end{document}
'''
if __name__=='__main__':(HERE/'reader.tex').write_text(render_text(read('results.json')))
