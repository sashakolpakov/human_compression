"""Readable complete manuscript comparisons; no asymmetric software factors."""

SHORT = {'Representation': 'Represent.', 'ChiralEnumeration': 'Chiral',
         'RankContraction': 'Rank contr.', 'LocallyProjective': 'Locally proj.',
         'MathieuCensus': 'Mathieu', 'RankAugmentation': 'Rank augm.'}


def number(value):
    return '--' if value is None else f'{value:,}'


def factor(value):
    return f"{float(value['decimal']):.3f}"


def tex(result):
    topics = []
    applications = []
    programs = []
    for row in result['topics']:
        name = SHORT.get(row['topic'], row['topic'])
        topics.append(' & '.join([name, str(row['source_count']), number(row['source_sum']),
                                  number(row['common_theory']), number(row['applications_sum']),
                                  number(row['written_denominator']), factor(row['written'])]) + r' \\')
        programs.append(' & '.join([name, number(row['printed_program_cost']),
                                    number(row['raw_program_alternative']), number(row.get('mandatory_data_cost'))]) + r' \\')
        for pair in row['pairs']:
            applications.append(' & '.join([name, pair['source'], pair['application'], number(pair['source_cost']),
                                            number(pair['application_cost']), factor(pair['conditional'])]) + r' \\')
    return r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=23mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,array,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\newcommand{\tabsetup}{\small\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.10}}
\begin{document}
\begin{center}\Large\textbf{Common theories and their applications}\\[4pt]
\normalsize Nineteen topics, forty-three original manuscripts\end{center}
For each topic, $S=\sum_i c(L_i)$ is the length of the complete original
manuscripts, $U$ the length of the whole common theory, and $A=\sum_i c(A_i)$
the length of all complete applications. We report
\[
R=\frac{S}{U+A},\qquad r_i=\frac{c(L_i)}{c(A_i)}.
\]
The second comparison assumes acquisition of the whole common theory and
the declared required dependencies. Each topic pays its common theory
independently. A factor greater than one indicates a shorter written replacement.

\textbf{Complete manuscript costs.} The unit is NFC characters without
whitespace, at each topic's stated representation. Introductions, context,
proofs, companions and references remain included.
\begin{center}\tabsetup\begin{tabular}{lrrrrrr}\toprule
Topic & Originals & Sources & Common & Applications & Written & Factor\\\midrule
''' + '\n'.join(topics) + r'''
\bottomrule\end{tabular}\end{center}
\textbf{Scope.} The active catalogue contains 106 accessible originals:
43 admitted principal-result recoveries with measurements and 63 awaiting
complete recovery. The 55 unavailable originals from the historical catalogue
of 161 remain archived outside the analysis. No singleton is excluded.
An admission covers the specified principal results, corrections and retained
inputs; it does not establish every auxiliary claim or answer every conjecture.

\textbf{Representations.} B and C include complete authored-text renderings
where original PDFs are unavailable. F, Mixes, rank contraction, rank
augmentation and the Mathieu census use raw untrimmed PDFs. Other topics
retain their declared calibrated and selected text. No pooled factor is
formed across these different representations.
\newpage
\textbf{The complete common theory and every application.}
The dark bar is the sum of the original manuscript costs. Blue segments
are complete common papers; green segments are complete applications.
All companions and complete written tables remain charged.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
F now comprises two originals. Its entire seven-page common theory costs
15,876 characters and its five- and six-page applications cost 11,504 and
15,894. Thus $69{,}825/43{,}274=1.613555\ldots$.
The eighteen other topics retain their previous written costs. This is a
measurement of the present proofs' written length, not of minimum proof
complexity or originality.
\newpage
\textbf{Each complete application after acquisition.}
The entire common theory and all required dependencies have already been
acquired. Optional validation is not a mathematical prerequisite. Every
application, companion and reference is still charged.
\begin{center}\fontsize{8.5}{10.2}\selectfont\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.10}\begin{tabular}{lllrrr}\toprule
Topic & Original & Application & Source cost & Application cost & Conditional\\\midrule
''' + '\n'.join(applications) + r'''
\bottomrule\end{tabular}\end{center}
DG2 includes all N006 companions. MC1 includes all 24 Mathieu application
pages. RA1 includes its application and counterproof; MX1 includes both
local papers. F1 and F2 use the same whole common theory. In F, all nine
programs are optional validation and none is a premise of the uniform proofs.
\newpage
\textbf{Original and application costs: first twenty-one originals.}
Dark bars show whole original manuscripts and green bars show whole
applications. The bars share one scale within each chart. The factors
assume prior acquisition of the complete common material.
\begin{center}\includegraphics[width=\linewidth]{conditional_1.pdf}\end{center}
The numerical input retains the exact edition, source qualifications and
all alternative counting coordinates for each topic. F's primary coordinate
now counts raw page furniture consistently; the old selected L014 cost of
25,115 is not substituted for its current raw cost of 25,574.
\newpage
\textbf{Original and application costs: remaining twenty-two originals.}
The same complete-document convention applies. A large conditional factor
does not mean that the shared theory was free to establish.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
The locally projective source L084 is the complete erratum; L095 uses the
available fifteen-page arXiv edition. The Mathieu application contains the
corrected 81/431-class census and every literal source-row disposition.
L020's false third case has a corrected criterion and complete counterproof.
The Mixes paper's three final problems remain unanswered. These qualifications
remain part of the scientific admissions.
\newpage
\textbf{Program and data inventory.}
Validation must be excluded on both sides or included on both sides.
The earlier software-inclusive fractions added only our programs and are
withdrawn as compression measures. An inclusive comparison requires
\[
\frac{S+c(\text{original validation})}{U+A+c(\text{our validation})}.
\]
Original software costs are not yet established under a common inclusion
rule, so this ratio is unavailable. The following replacement costs remain
visible as inventory. Printed and raw programs are alternatives.
\begin{center}\tabsetup\begin{tabular}{lrrr}\toprule
Topic & Printed programs & Raw programs & Mandatory data\\\midrule
''' + '\n'.join(programs) + r'''
\bottomrule\end{tabular}\end{center}
E additionally retains 5,173 characters of optional printed validation,
separate from its 7,565-character required program. F's printed and raw
entries both represent all nine optional validation files; they are not
additional to each other. Operations' whole raw inventory includes both
required decoding programs. Its separately inventoried external data uses
byte units, which are not added to these character costs.

\textbf{Mathematical role.} A program, certificate or data file needed to
establish a theorem remains required evidence. A manuscript-length factor
does not measure the complete cost of an executable proof when such
premises lie outside the manuscript. Missing source software, full external
proofs and graphical information retain unknown costs. Partial Lean
certificates do not establish full formalization of the source theorems.

\textbf{Embedded listings.} Separate validation is excluded from both
manuscript operands. F's two original papers and three replacement papers
were checked for embedded validation listings and contain none. This
specific check has not yet been completed for all older topics, so their
unchanged complete-manuscript figures are not universally described as
program-free comparisons.

\textbf{Evidence.} Exact integers, rational comparisons, cost inventories
and document boundaries are supplied in the accompanying JSON and CSV
files. This overview adds no proof, conjecture answer or formal declaration.
Distinct review of the consolidation is required before publication.
\end{document}
'''
