from plotting import SHORT
def tex(r):
    n=lambda x:'--' if x is None else f'{x:,}';f=lambda q:'--' if q is None else f"{float(q['decimal']):.3f}";short=lambda t:SHORT.get(t,t)
    s=r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=23mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,array,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\newcommand{\tabsetup}{\small\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.10}}
\begin{document}
\begin{center}\Large\textbf{Complete papers and shared theories}\\[4pt]
\normalsize Seventeen topics, forty original texts\end{center}
This candidate preserves all fifteen topic records from the admitted thirty-seven-original overview. It adds Locally projective quotients (L084 and L095) and the Mathieu census (L073), using their distinctly accepted complete numerical boundaries. This consolidated overview still requires independent acceptance. Earlier editions remain preserved, with committed baseline and new packet hashes bound directly.

For each topic, $S=\sum_i c(L_i)$ counts its complete original texts, $U$ every complete common paper, and $A=\sum_i c(A_i)$ every complete application. The comparisons are
\[
 R=\frac{S}{U+A},\qquad r_i=\frac{c(L_i)}{c(A_i)}
 \quad\text{after acquiring the whole theory and declared software/data.}
\]
Each topic pays its common theory independently, even when proofs overlap another topic. A factor above one means a shorter replacement in that coordinate; a factor below one means a longer one. Conditional factors do not include acquisition a second time, and are not standalone application savings.

\textbf{Complete written costs.} All rows use NFC characters without whitespace at their stated representations. Full-document boundaries include introductions, context, proofs and references.
\begin{center}\tabsetup\begin{tabular}{lrrrrrr}\toprule
Topic & Originals & Sources & Common & Applications & Written & Factor\\\midrule
"""
    for t in r['topics']:s+=' & '.join([short(t['topic']),str(t['source_count']),n(t['source_sum']),n(t['common_theory']),n(t['applications_sum']),n(t['written_denominator']),f(t['written'])])+r' \\'+'\n'
    s+=r"""\bottomrule\end{tabular}\end{center}
\textbf{Representations remain distinct.} B and C use complete authored-text renderings for N001 and L108, with raw untrimmed PDFs for their other documents. Those originals' unavailable-PDF costs remain unknown. Rank contraction and the Mathieu census also use complete raw untrimmed PDFs. Locally projective and other rows use their accepted selected, calibrated PDF coordinate. Operations' encoded-event graphical proxies retain raw and text-only sensitivities. No pooled factor is formed.

\textbf{Scope.} These are 40 candidate measured originals in 17 topics within the 161-item programme. This is not the number of recovered or accessible originals, nor completion of the programme. Recovery and retrieval progress are reported separately. All corrections, retained premises and ancillary exclusions remain. The two new written factors, 0.707 and 0.332, are below one: both replacements are longer in their respective coordinates. No scientific, source, question or formal credit changes.
\newpage
\textbf{Complete common theories and applications.}
Dark bars are whole original sums. Blue segments are whole common papers; green segments are all complete applications. Unified B pays its entire current common paper once. C still pays its complete additional incidence note. The N006 application retains all three companions. Locally projective common theory includes both the proof and its complete tables; the Mathieu application includes the main paper, all class tables and all source-row dispositions.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
All earlier common and application boundaries remain unchanged. Locally projective pays 7+5 common pages and both applications (2+3 pages). Mathieu pays its two-page common paper and all 5+10+9 application pages. Companion tables are complete papers in these denominators, not free outputs. Text length is not minimum proof complexity or originality.
\newpage
\textbf{Complete programs and prior acquisition.}
The written comparison remains first. These alternatives add the entire declared code representation and any separately measured mandatory data. Raw and printed code are never added together. The new data column is separate from code in both denominators.
\begin{center}\tabsetup\begin{tabular}{lrrrrrr}\toprule
Topic & Printed code & Data & With printed & Raw code & With raw & Upfront\\\midrule
"""
    for t in r['topics']:s+=' & '.join([short(t['topic']),n(t['printed_program_cost']),n(t.get('mandatory_data_cost')),f(t['including_printed_programs']),n(t['raw_program_alternative']),f(t['including_raw_programs']),n(t['conditional_prepaid']['total'])])+r' \\'+'\n'
    s+=r"""\bottomrule\end{tabular}\end{center}
Upfront means the whole common theory, complete printed code when available, and separately measured mandatory data. A dash in the Data column for an older record does not mean its external data is free; those historical boundaries remain unchanged. Locally projective adds all 28,574 data characters (39,150 literal bytes), and Mathieu all 48,686 (83,965 bytes), to both code alternatives. For Operations it uses all twenty-three whole mathematical/validation files plus both required decoding drivers. Its complete printed route is unavailable: the two partial appendices cover only four named raw files. Operations conditionals also assume acquisition of all required external data, separately inventoried as 21,960,689 representation bytes and 2,516,249 listed installed bytes. Byte storage is not added to character units. Large witnesses are not discounted.

E retains its separate optional-validation sensitivity: another 5,173 characters gives a program-inclusive factor of 1.372. No unadmitted raw-code alternative is invented for E.

\textbf{Roles.} A includes five full files. B includes a finite premise, two validations and an auxiliary example. C includes its three complete GAP files, counting the identical shared construction once within C and retaining its exhaustive census. D includes five required and three diagnostic programs. E separates its required program from optional validation. F's three programs and Representation's two are validations. G retains four finite computations, two certificate bridges and seven validations. Affine retains six mathematical programs; Chamber one required and one diagnostic program; Matching its census; Chiral enumeration all three files. Operations includes seventeen finite proof/witness files, six validations and both required decoders. Gluing pays all three complete validation programs, with three drivers and two partial Lean files separate. Rank contraction keeps its whole finite-example program, driver and four partial Lean declarations separate. Locally projective requires six complete programs and whole historical reconciliation JSON; Mathieu requires seven programs and both entire JSON inputs. Their three drivers each and eleven/ten generated outputs are separate; neither has Lean declarations. Other inventories stay unchanged.

\textbf{Limits.} Complete external proofs, unprovided historical software, full graphics and end-to-end formalization have unknown costs, not zero. Every topic retains its underlying multi-unit and source-cover sensitivities. B's source costs are unchanged from the prior edition. This table does not compare a theorem closure with a complete original or use a node-count ratio.
\newpage
\textbf{Every complete application after full acquisition.}
The entire common theory and all declared software/data have already been acquired. Every local page is charged, including context, references and companions. DG2 includes all N006 papers; MC1 includes all 24 Mathieu application pages.
\begin{center}\tabsetup\renewcommand{\arraystretch}{1.03}\begin{tabular}{lllrrr}\toprule
Topic & Original & Application & Source cost & Application cost & Conditional\\\midrule
"""
    for t in r['topics']:
        for q in t['pairs']:s+=' & '.join([short(t['topic']),q['source'],q['application'],n(q['source_cost']),n(q['application_cost']),f(q['conditional'])])+r' \\'+'\n'
    s+=r"""\bottomrule\end{tabular}\end{center}
All fifteen previous topic records remain unchanged. Three complete applications are added. Forty measured originals is not inferred to be the total recovered; no scientific credit is assigned.
\newpage
\textbf{Individual source and application costs: first seventeen originals.}
Dark bars show complete original texts; green bars show complete applications. Factors at right assume full prior acquisition. The source and replacement bars share the same scale within each chart.
\begin{center}\includegraphics[width=\linewidth]{conditional_1.pdf}\end{center}
Source IDs remain stable catalogue cross-references. LP1 is the complete 2006 erratum; LP2 uses the full fifteen-page 2003 arXiv edition, not the unseen journal text. Their source-column corrections remain qualified. MC1 gives the corrected 81/431-class census and all 431 literal-row dispositions, not unavailable historical \texttt{geo[]} identities. Its 48-page predecessor is retained notation, not a newly recovered original.
\newpage
\textbf{Individual source and application costs: remaining twenty-three originals.}
The same conventions apply. LP1 and LP2 assume acquisition of the whole Locally projective proof, common tables, all six programs and mandatory JSON. The final MC1 bar contains all three Mathieu application papers, after whole common theory, all seven programs and both JSON inputs. Other topics remain separately paid; no overlap is deducted.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
\textbf{Data and provenance.} Exact integers and rational comparisons are in \texttt{results.json}, \texttt{topics.csv} and \texttt{applications.csv}. The protocol pins committed unchanged numerical/admission records and the two new frozen numerical packets and their distinct root acceptances directly. No primary text is copied or extracted. Bar segments use complete document costs, not theorem counts. Distinct review is required before this overview becomes the public current edition.
\end{document}
"""
    return s

