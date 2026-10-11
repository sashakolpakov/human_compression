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
\normalsize Fourteen topics, thirty-six original texts\end{center}
This candidate preserves all thirteen unaffected topic records from the admitted thirty-five-original overview. The earlier Diagonal record is replaced by the complete Operations topic, adding N005 and paying the whole new common theory and revised N006/N007 applications. The Operations science, inputs and numbers are distinctly accepted; this consolidated overview still requires independent acceptance. Exact candidate and baseline hashes are bound directly. Earlier overviews remain preserved.

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
\textbf{Representations remain distinct.} B and C use complete authored-text renderings for N001 and L108, with raw untrimmed PDFs for their other documents. Those originals' unavailable-PDF costs remain unknown. Other rows use their accepted selected, calibrated PDF coordinate. Operations' encoded-event graphical proxies retain raw and text-only sensitivities. No pooled factor is formed.

\textbf{Scope.} These are 36 candidate measured originals in 14 topics within the 161-item programme. This is not the number of recovered or accessible originals, nor completion of the programme. Recovery and retrieval progress are reported separately. All corrections, retained premises and ancillary exclusions remain. Gluing's written factor is below one: its complete replacement is longer in this coordinate. No scientific, source, question or formal credit changes.
\newpage
\textbf{Complete common theories and applications.}
Dark bars are whole original sums. Blue segments are whole common papers; green segments are all complete applications. Unified B pays its entire current common paper once. C still pays its complete additional incidence note. The N006 application is displayed as all three companion-paper segments; the whole 21-page Operations common paper is one paid acquisition.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
Operations retains N005, N006 and N007 and all three N006 companion papers. Gluing adds both complete common papers and the full application; its 0.677 written factor is not replaced by its 2.342 conditional factor. Text length is not minimum proof complexity or originality.
\newpage
\textbf{Complete programs and prior acquisition.}
The written comparison remains first. These separate alternatives add the entire declared program representation to the written denominator. Raw and printed forms are never added together.
\begin{center}\tabsetup\begin{tabular}{lrrrrr}\toprule
Topic & Printed code & With printed & Raw software & With raw & $U+$programs\\\midrule
"""
    for t in r['topics']:s+=' & '.join([short(t['topic']),n(t['printed_program_cost']),f(t['including_printed_programs']),n(t['raw_program_alternative']),f(t['including_raw_programs']),n(t['conditional_prepaid']['total'])])+r' \\'+'\n'
    s+=r"""\bottomrule\end{tabular}\end{center}
The final column uses the complete printed form when available. For Operations it uses all twenty-three whole mathematical/validation files plus both required decoding drivers. Its complete printed route is unavailable: the two partial appendices cover only four named raw files. Operations conditionals also assume acquisition of all required external data, separately inventoried as 21,960,689 representation bytes and 2,516,249 listed installed bytes. Byte storage is not added to character units. Large witnesses are not discounted.

E retains its separate optional-validation sensitivity: another 5,173 characters gives a program-inclusive factor of 1.372. No unadmitted raw-code alternative is invented for E.

\textbf{Roles.} A includes five full files. B includes a finite premise, two validations and an auxiliary example. C includes its three complete GAP files, counting the identical shared construction once within C and retaining its exhaustive census. D includes five required and three diagnostic programs. E separates its required program from optional validation. F's three programs and Representation's two are validations. G retains four finite computations, two certificate bridges and seven validations. Affine retains six mathematical programs; Chamber one required and one diagnostic program; Matching its census; Chiral enumeration all three files. Operations includes seventeen finite proof/witness files, six validations and both required decoders. Gluing pays all three complete validation programs, with three drivers and two partial Lean files separate. Other operational drivers and partial Lean inventories stay separate.

\textbf{Limits.} Complete external proofs, unprovided historical software, full graphics and end-to-end formalization have unknown costs, not zero. Every topic retains its underlying multi-unit and source-cover sensitivities. B's source costs are unchanged from the prior edition. This table does not compare a theorem closure with a complete original or use a node-count ratio.
\newpage
\textbf{Every complete application after full acquisition.}
All common papers and all declared software/data have already been acquired. The whole application is charged, including local context and references. DG2 includes every N006 companion paper.
\begin{center}\tabsetup\begin{tabular}{lllrrr}\toprule
Topic & Original & Application & Source cost & Application cost & Conditional\\\midrule
"""
    for t in r['topics']:
        for q in t['pairs']:s+=' & '.join([short(t['topic']),q['source'],q['application'],n(q['source_cost']),n(q['application_cost']),f(q['conditional'])])+r' \\'+'\n'
    s+=r"""\bottomrule\end{tabular}\end{center}
All thirteen unaffected topic records, including Gluing, remain unchanged from the committed admitted overview. Only the Operations record changes. This candidate does not equate 36 measured originals with all recoveries or add scientific credit.
\newpage
\textbf{Individual source and application costs: first seventeen originals.}
Dark bars show complete original texts; green bars show complete applications. Factors at right assume full prior acquisition. The source and replacement bars share the same scale within each chart.
\begin{center}\includegraphics[width=\linewidth]{conditional_1.pdf}\end{center}
Source IDs are stable catalogue cross-references. Descriptive topic titles, exact editions and current source-contract qualifications remain in the bound records; they are not new claims of this overview.
\newpage
\textbf{Individual source and application costs: remaining nineteen originals.}
The same conventions apply. The N006 bar retains all three companion papers. The final L010 bar is the complete Gluing application, conditional on both entire common papers and all declared diagnostic programs.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
\textbf{Data and provenance.} Exact integers and rational comparisons are in \texttt{results.json}, \texttt{topics.csv} and \texttt{applications.csv}. The protocol pins committed unchanged numerical/admission records and the frozen Operations numerical packet and its distinct root acceptance directly. No primary text is copied or extracted. Bar segments use complete document costs, not theorem counts. Distinct review is required before this overview becomes the public current edition.
\end{document}
"""
    return s

