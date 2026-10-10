# Phase-twelve review record

10 October 2026. This phase completes the specified principal-result
reduction of a 2002 paper, proves an infinite unitary parameter family,
extends the cyclic TPP theorem through class three, and constrains any
remaining minimum 2-group counterexample to a bounded quotient over
powerful eighth powers. It also records an all-rank counterexample to
specified auxiliary claims in a 2026 preprint. All reviews here are
internal mathematical reviews, not external peer review or priority
determinations.

## Complete 2002 principal-result reduction

Root and the proof author read all twelve pages of the Cameron–Cara
primary manuscript and the complete
[replacement proof](../research/case_study/phase12_N003_reduction.md).
All eight numbered statements are covered: general bounds for finite
groups, and both full generator/geometry classifications and their
corollaries for n≥7. Whiston's maximum-family theorem and exact omission
trichotomy are distinct retained inputs. Their CFSG dependence remains.
The source's unnumbered small-degree census and open questions are
excluded. This is the ninth work in the conservative principal-result
ledger; it is not a reduction of every result ever associated with it.

The common forest formula now supplies a short reconstruction of both
generator forms. A sign kernel gives every generated subgroup, and
weighted laminar cuts with one parity type give the second geometry.
The adapters include a full permutation-module argument, all three
counts, the relative-B bound, and a panel argument eliminating a
possible balanced-cut overgroup in the last corollary. The foundational
1997 geometry classification is unnecessary for this separate reduction.

Root reviewed and freshly ran the original standard-library checker.
Its report is byte-identical to the frozen report: 716 markings,
11,124 actual subset groups, 182,672 intersections, 369,093 typed
partial flags, and 44,696 module triples, with the exact recorded
finite ranges. Source-span metadata identifies all eight targets but
does not assign a matched-length numerator. A complete comparison must
still charge the shared core and every adapter on the same background.

## An infinite unitary family

Root and a second reviewer read the complete
[parameter argument](../research/case_study/phase12_unitary_parameters.md).
Both independently checked the necessary passages in the author-hosted
Katz primary text: Euler characteristic, trace formula, the compact
cohomology weight bound, and Lang character sheaves for connected
commutative groups. The independent audit explicitly verifies that
the nonsplit torus Lang map becomes t↦t^(q+1) over the algebraic closure,
so the geometric character retains its exact order.

The four distinct ramification points give the mixed 2√q estimate.
The one-character boundary term contributes exactly plus two to the
primitive indicator expansion. The divisor estimate and seven exact
arithmetic cases make the count positive for every q=9^e. The Cayley
identity then gives four distinct eigenvalues and projective middle
order q²−1. A separate proper-subfield order bound supplies the full
square-field hypothesis without using generation circularly.

The frozen phase-eleven generation and intersection proofs apply.
Together with the separately retained rank obstruction, the result
is maximum rank four and type {4,q²−1,6} for PSU₄(9^e), every e≥1.
It does not settle existence for all odd field sizes or all diagonal
extensions. The bounded seven-query source search does not establish
priority or identify this family as a separate named conjecture.

Root freshly ran the SymPy arithmetic checker in a scratch copy and
the GAP finite-field checker. Arithmetic reports agree apart from
execution timestamp. GAP output agrees after newline normalization;
the only raw-byte difference is CRLF versus LF on its initial blank
line. All 7,376 nonzero x in four sample fields were tested, with
successful counts 8,64,456,4800. Matrix and square-field checks pass.
These samples do not replace the written all-exponent argument.

## Class-three cyclic TPP and the remaining power layers

Root independently reviewed the complete
[class-three proof](../research/case_study/phase12_class_three.md),
including dependent marked vectors in low dimension and the permitted
relabeling in dimension three. Factoring by fourth powers makes the
marked Frattini commutator calculation small enough for the retained
binary action lemma. It forces a powerful Frattini subgroup and the
previously reviewed contradiction. The induction is within the
subgroup- and quotient-closed class-three family.

The exact GAP/NQ identities hold in the free torsion-free class-three
group. The separate order-4096 example has nonpowerful Frattini subgroup
and shows that the new sufficient condition is not contained in the
earlier hereditary-powerful-Frattini condition. Root's fresh transcript
matches the frozen one byte for byte. The odd-order theorem then gives
the bound for every finite nilpotent group whose Sylow 2-subgroup has
class at most three, with no restriction on its odd Sylow classes.

The [power-layer theorem](../research/case_study/phase12_power_layers.md)
was also reviewed in full. Its weak-embedding induction does not assume
an equality of iterated and ordinary power subgroups. The low-dimensional
action equations force both first Frattini ranks to be three in a
minimum counterexample. A collection upper bound identifies P/P⁴ with
the specified order-32 presentation, independently of its NQ quotient
check. Small linear actions and weak embedding then make P⁸ powerful
of index 256, with genuine ordered cyclic coordinates at all deeper
power levels.

This last step retains the earlier small-factor theorem and its
marked-isobicyclic classification input. Some eighth-power cyclic
factors may be trivial, as the proof permits. Root's fresh linear and
presentation outputs match the frozen files exactly. The included
linear counterexample shows why a common fixed vector need not be
a marked coordinate; that shortcut cannot finish the unrestricted
conjecture. No global multiplication injectivity is presumed.

## Exact correction to the specified 2026 statements

Root's [path cocycle](../research/case_study/phase12_path_cocycle.md)
and its all-rank Frattini calculation were independently reviewed
against Hou–Schulte arXiv:2605.20691v1, equations (7)–(9) and Theorem
4.2, and against the Section 3 presentation. The source PDF and
extraction hashes identify the checked text. The HTML and PDF header
dates differ; the finding is tied to the identical specified claims.

For the source's own minimal class-two group of rank d≥4, the stated
C has order 2^(d−3), rather than one. Thus the kernel order in (c),
quotient order/identification in (d), and equality with γ₃ in (e)
fail. The quotient still has the string C-group intersection property,
with degenerate interior adjacent orders. The separate main common-
quotient existence claims are not refuted: this family maps to the
claimed group by the identity. No replacement universal theorem is
asserted in this phase.

The coordinate checker and an independent fresh run agree exactly
through rank six, with 299,584 cocycle comparisons and 5,456 subgroup
intersections. An independently constructed NQ presentation witness at
rank four verifies all 256 intersections and Frattini orders 4,8,4.
Root freshly reran that independent script, matching its log exactly.
The written proof supplies the all-rank extension. This is a correction
to specified assertions, not an open-conjecture resolution.

## Export, formal scope and measurement

[Original-file provenance](phase12_original_files.json) records 52
byte-identical original artifacts. Historical private/draft labels
describe their original context; the later bound reviews and this
record state the completed internal review. Third-party full texts,
scratch directories and subsequent exploratory work are excluded.
Earlier proof artifacts and all seventeen saved Lean reports remain
unchanged. This phase adds no Lean module; the existing binary-action
certificate remains a precisely bounded dependency.

The registry now has 152 works, 93 retrieved full texts, 41 specified
encodings/reductions, 29 rederived components or principal targets,
and nine principal-result reductions. These overlapping counts are
coverage measures. The only matched-proof ratio remains 127/38≈3.34
for the specified two L066 formulas. The corpus ratio is unmeasured,
and no verified-new-resolution infinity marker is assigned.
