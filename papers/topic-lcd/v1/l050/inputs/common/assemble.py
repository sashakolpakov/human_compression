#!/usr/bin/env python3
"""Rework already reviewed arguments into one common manuscript.

This only assembles TeX. It grants no new scientific or numerical credit.
The inherited packets remain immutable.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
routes = []


def fragment(path, start, stop, labels, title):
    source = BASE / path
    text = source.read_text()
    body = text[text.index(start):text.index(stop)]
    for old, new in labels.items():
        body = body.replace("{" + old + "}", "{" + new + "}")
    routes.append({"source": path, "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                   "start": start, "stop_excluded": stop, "labels": labels,
                   "destination_section": title})
    return "\\section{" + title + "}\n\n" + body


preamble = r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=27mm]{geometry}
\usepackage{amsmath,amssymb,amsthm,booktabs,hyperref}
\hypersetup{hidelinks}
\setlength{\emergencystretch}{1em}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\numberwithin{equation}{section}
\newcommand{\im}{\operatorname{im}}
\newcommand{\rank}{\operatorname{rank}}
\newcommand{\wt}{\operatorname{wt}}
\title{Incidence operators, orthogonal codes and permutation modules}
\author{Common theory for two applications}
\date{}
\begin{document}\maketitle

The starting point is a symmetric operator on a space with its coordinate
bilinear form. An orthogonal decomposition of its image can often be
read from a short polynomial identity, or transferred from a much smaller
incidence space. This separates the questions of dimension and duality
from the questions of minimum weight and group action. The latter require
additional arguments: averaging over coordinate permutations reduces a
distance search, a matrix algebra certifies irreducibility, and refinement
of a support incidence structure bounds the full automorphism group.
Each argument is proved once here and then applied to literal matrices
and finite data in the accompanying papers.

Our two source manuscripts are Leemans and Rodrigues,
\emph{Linear codes with complementary duals from some strongly regular
subgraphs of the McLaughlin graph}, Math. Commun.\ 21 (2016), 239--249
(L050), and Key and Rodrigues, \emph{LCD codes from adjacency matrices of
graphs}, the seventeen-page manuscript dated 4 August 2017 (F017).
The graph constructions, original code assertions, and results quoted
from their predecessors remain attributed to those sources in the
applications. Orthogonal projections, incidence counting, the simplex
chain contraction, MacWilliams duality and elementary module theory are
classical tools. Our contribution here is their common derivation and
the explicitly checked passage to the stated applications. Historical
priority for these methods is not asserted.

The common complement theorem includes the possible one-dimensional
defect and does not require an integral spectrum. The subset and Hamming
calculations give families of consequences of the same operator tests.
The binary incidence argument also determines all minimum words, whereas
the ternary triple-incidence calculation corrects a dimension in F017.
Other corrections, retained classification results and finite computation
premises are stated with the exact source assertions in each application.
No numerical compression factor is assigned by this draft.

The whole of this common paper is a prerequisite for the applications
when lengths are compared. A theorem used by only one application is
still charged here in full. Executable certificates have a separate
inventory; any manuscript comparison excludes executable programs on
both sides. The nine generic Lean declarations already associated with
the projection and averaging arguments retain their limited stated
scope. They do not formalize all the proofs in this paper.

"""

projectors = fragment(
    'topic_LCD_L050_F017_recovery/umbrella_projectors.tex',
    'Let $F$ be a field', r'\paragraph{Outstanding obligations.}',
    {'lem:projector': 'ULCD.Projector', 'thm:complement': 'ULCD.Complement',
     'cor:graph': 'ULCD.Graph', 'prop:reflexive': 'ULCD.Reflexive', 'prop:srg': 'ULCD.SRG'},
    'Symmetric operators and graph duality')
start = projectors.index(r'\paragraph{Attribution and scope.}')
stop = projectors.index(r'\begin{lemma}', start)
projectors = projectors[:start] + projectors[stop:]

distance = fragment(
    'topic_LCD_transitive_distance_candidate/transitive_code_certificates.tex',
    r'Let $C\leq', r'\paragraph{The finite field models.}',
    {'thm:average': 'ULCD.TransitiveDistance', 'cor:minwords': 'ULCD.MinimumEnumeration',
     'lem:rank': 'ULCD.Rank'}, 'Transitive distance searches and rank')
distance = distance.replace(
    r'\begin{lemma}\label{ULCD.Rank}',
    r'''For a proposed invariant set of minimum words, the hypothesis in
Corollary~\ref{ULCD.MinimumEnumeration} can also be checked by counting.
If its intersection with the restricted message set has the same size
as the complete restricted minimum set, inclusion and equality of these
finite sizes prove equality of sets. No disjointness or orbit count is
assumed without checking it.

\begin{lemma}\label{ULCD.Rank}''')

incidence = fragment(
    'topic_LCD_L050_F017_recovery/steiner_incidence.tex',
    r'\begin{lemma}', r'\paragraph{A literal qualification in the source.}',
    {'lem:transfer': 'ULCD.IncidenceTransfer', 'thm:three': 'ULCD.ResidualSteiner',
     'prop:recognition': 'ULCD.SteinerRecognition'}, 'Incidence transfer and residual designs')
incidence = incidence.replace(
    'The complementary-projection theorem in the common paper yields',
    r'Theorem~\ref{ULCD.Complement} yields')
incidence = incidence.replace(r'\tag{1}', r'\tag{2.1}\label{ULCD.ResidualIdentity}')
incidence = incidence.replace('By (1)', r'By \eqref{ULCD.ResidualIdentity}')
incidence = incidence.replace('since (1)', r'since \eqref{ULCD.ResidualIdentity}')
incidence = incidence.replace(
    'This invocation pays for that common theorem;\nit is not an independent derivation of it.', '')
incidence = incidence.replace(
    'The usual identification $\\operatorname{Aut}(S(4,7,23))\\cong M_{23}$ is\na separate retained classical input. The hypothesis on minimum words in\nProposition~\\ref{ULCD.SteinerRecognition} requires its own exact certificate.\nNeither this proposition nor the incidence calculation establishes the\nirreducibility of the $22$-dimensional summand.',
    r'''The minimum-word hypothesis in Proposition~\ref{ULCD.SteinerRecognition}
requires its own exact certificate. The application also identifies the
full design group by literal permutations attaining an incidence-refinement
bound, using Theorem~\ref{ULCD.Refinement}. Neither incidence transfer nor
recognition alone establishes irreducibility of the augmentation summand.''')

simplex = fragment(
    'topic_LCD_simplex_candidate/simplex_code_theory.tex',
    r'Let $\Omega$', r'\paragraph{Consequences and source corrections.}',
    {'lem:complex': 'ULCD.Simplex', 'thm:johnson': 'ULCD.Johnson',
     'thm:minwords': 'ULCD.SimplexMin'}, 'Binary incidence spaces')

simplex = simplex.replace('an $n$-element set.', 'an $n$-element set with $n>0$.')

ternary = fragment(
    'topic_LCD_ternary_kneser_candidate/manuscript.tex',
    r'Let $\Omega$', r'\paragraph{Relation to the source.}',
    {'lem:rank': 'ULCD.TernaryIncidence', 'thm:dimension': 'ULCD.TernaryKneser',
     'eq:incidence': 'ULCD.TernaryIdentity'}, 'Ternary incidence on triples')
ternary = ternary.replace(
    'For any symmetric idempotent,\n$\\ker R=(\\im R)^\\perp$ and $V=\\im R\\oplus\\ker R$; indeed\n$x=Rx+(x-Rx)$ gives the decomposition, whose intersection is zero.\nThus both summands are LCD.',
    r'Lemma~\ref{ULCD.Projector} gives $\ker R=(\im R)^\perp$ and the orthogonal decomposition; both summands are LCD.')

association = fragment(
    'topic_LCD_association_candidate/association_code_criteria.tex',
    r'Write $C_M', r'\paragraph{Verification and limits.}',
    {'thm:test': 'ULCD.Scalar', 'eq:subset': 'ULCD.SubsetCounts',
     'tab:families': 'ULCD.SubsetFamilies', 'eq:hamming': 'ULCD.HammingCounts',
     'cor:oddq': 'ULCD.HammingOddAlphabet', 'thm:cube': 'ULCD.Cube'},
    'Intersection counts for subset and Hamming graphs')
association = association.replace('The remaining claims in part~2 are the common projection theorem, applied',
                                   r'The remaining claims in part~2 follow from Theorem~\ref{ULCD.Complement}, applied')
association = association.replace('The common LCD rank lemma sums precisely',
                                   r'Lemma~\ref{ULCD.Rank} sums precisely')
association = association.replace('the separate simplex\nboundary theorem',
                                   r'Theorems~\ref{ULCD.Johnson} and~\ref{ULCD.SimplexMin}')

end = r'''
\paragraph{Required finite arithmetic.}
The polynomial identities and complete residue lists for
Table~\ref{ULCD.SubsetFamilies} are certified by
\path{check_association_counts.py}. The proof explains why these finite
identities settle every prime and every admissible parameter, rather than
inferring an infinite statement from sampled graphs. The applications
specify the further code and group certificates they require. No finite
distance, irreducibility or full automorphism assertion follows merely
from an adjacency spectrum or a congruence test.
\end{document}
'''
body = preamble + projectors + incidence + simplex + ternary + association + (HERE/'finite_criteria.tex').read_text() + distance + end
(HERE/'umbrella.tex').write_text(body)
(HERE/'migration.json').write_text(json.dumps({
    'status': 'DRAFT_ASSEMBLY_REQUIRES_DISTINCT_REVIEW',
    'inherited_fragments': routes,
    'new_or_generalized_proofs': ['Full matrix algebra and rank-one criterion',
        'Filtration and complete intertwiner spaces', 'Incidence refinement order bound',
        'MacWilliams identity included with full classical proof',
        'Restricted minimum-set equality by finite counting'],
    'moved_to_applications': ['All twelve generalized Paley rows and actual field construction',
        'Source-by-source dimension, distance and wording corrections',
        'Individual finite module, support, orbit and group data'],
    'new_original_credit': 0, 'new_question_credit': 0,
    'compression_factor': None,
}, indent=2)+'\n')
print(json.dumps({'status': 'ASSEMBLED_NOT_REVIEWED', 'inherited_fragments': len(routes),
                  'tex_sha256': hashlib.sha256(body.encode()).hexdigest()}))
