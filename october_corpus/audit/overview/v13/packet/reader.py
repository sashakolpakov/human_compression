"""Complete 46-original reader with explicit expanded-topic scope."""
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
Overview v13: expanded projective and mixes topics\end{center}
The current comparison contains 19 topics and 46 recovered originals among 106 accessible originals; 60 remain pending and 55 earlier indexed originals remain archived. E now covers five originals, including L056 and L043, and Mixes covers F005 and L016. The other 17 topic records and 39 individual records retain their exact v12 boundaries, including the three symmetric listing corrections. Unified A and F007 are outside this edition.

The complete written factor is $\sum_i c(S_i)/(c(U)+\sum_i c(A_i))$ within each topic. Whole common theory and every complete local application are paid, without a cross-topic discount. Each row retains its adopted nonwhitespace-character coordinate. Expanded E uses raw-untrimmed NFC extraction, an explicit change from the earlier E coordinate; this primary was independently fixed and accepted. There is no pooled factor or inferred minimum proof complexity.
\begin{center}\small\begin{tabular}{lrrrrr}\toprule
Topic & Originals & Sources & Common & Applications & Factor\\\midrule
'''+topics+r'''
\bottomrule\end{tabular}\end{center}
The exact \href{topics.csv}{19-topic CSV} and \href{applications.csv}{46-original CSV} preserve complete component costs, current fractions and historical observations. Factors below one remain visible. The accepted scientific source maps determine what each recovery covers; the numerical consolidation adds no separate proof or question credit.
\newpage
\section*{Individual comparisons: first 23 originals}
After acquiring the \emph{whole} common theory and all actual required mathematical, computational and data premises, the conditional factor is $c(S_i)/c(A_i)$. It charges the full local application or complete companion bundle. Optional validation is not silently made a theorem premise.
'''+table(pairs[:23])+r'''
E pays its whole 20-page common paper, all five applications and all exact source qualifications. The five-source numerator uses 67 source pages. Application routes remain L083 to A1, L079 to A2, L021 to A3, L056 to A4 and L043 to A5. The broader quoted classifications and ancillary censuses remain retained where the source map says so; they are not newly claimed as regenerated results.

L043 names \emph{Magma} and the $L_2$-quotient algorithm. GAP and Python describe the replacement implementation. Its accepted corrections, L056's characteristic-two qualification, the L021 corrections, and the exclusion of L079's P$\Sigma$L$(2,25)$ clause remain explicit. E's 42 scoped Lean declarations are partial evidence, not full source formalization.
\newpage
\section*{Individual comparisons: remaining 23 originals}
'''+table(pairs[23:])+r'''
Mixes pays both complete common papers, with costs 12,615 and 11,641. F005's application pays both its main and exceptional papers (20,788 plus 10,289); L016's complete local paper costs 15,125. Both required finite certificates remain required, while four validation programs remain optional. Six scoped formal declarations do not formalize the full sources.

The three final F005 problems remain unanswered. L016's literal thin-cover Lemma 3.5 is corrected under faithfulness; Proposition 5.4 is stated without CIP. Ancillary smallest-example/Atlas census and further-cover questions remain outside the accepted principal recovery. A corrected source theorem is not assigned a new solved-question credit.

Executable listings are excluded symmetrically, while proof and mathematical algorithm prose remain. All required program/data and optional validation inventories are preserved separately. Historical software, external proofs, complete graphics and full formalization costs are unknown; software-inclusive and pooled factors remain null. Operations retains its separate text-only sensitivity. Prior overviews remain historical records.
\newpage
\section*{Whole topics}
Grey bars show the complete original manuscript text in each row's adopted coordinate. Replacement bars stack the entire common theory and every local application. The axis starts at zero; the tables contain ratios.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
The 57 bars account for all 19 complete topics. Shared theory remains charged even when only some applications invoke a section. No required code or external premise is treated as mathematically unnecessary because its cost is outside the manuscript coordinate.
\newpage
\section*{Conditional lengths: first 23 originals}
Whole common theory and required premises are acquired in advance. Grey and teal bars compare complete source and local application text; these bars do not remove the prerequisite cost from the whole-topic table.
\begin{center}\includegraphics[width=\linewidth]{conditional_1.pdf}\end{center}
\newpage
\section*{Conditional lengths: remaining 23 originals}
All complete companion papers remain charged. The source sequence is documentary, with no optimized acquisition order, sawtooth or proof-node factor implied.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
\end{document}
'''
if __name__=='__main__':(HERE/'reader.tex').write_text(render_text(read('results.json')))
