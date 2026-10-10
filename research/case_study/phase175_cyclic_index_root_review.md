# Review of the completed cyclic-index classification

The completed note **Large cyclic subgroups in two-group polytopes** is
accepted as a deduction of the corrected Theorem 4.1 and the structural
content of Proposition 4.2 in Mark L. Loyola's 2016 paper. It is a
separately costed attachment to Module A, not a seventh complete source
contract for the existing 24-page manuscript.

The reviewed completion has SHA-256
`800392187b8ccadab85fb786663ad28772da1806f6a0452f53e28d6e682001fb`.
The frozen author manifest has SHA-256
`36f5051cc73fd92df2f153f1d573f0aecd35f29d0e10734662c8de2d9deabd81`.
Its author independently reviewed the initial root-authored cyclic-index
argument and supplied the missing completion. This root review checks
those new arguments separately; it does not portray the root as having
had no role in the initial idea.

## Mathematical review

The full completion, its review, both arithmetic programs and their
standalone runner were read. The exact A2.1–A2.4 argument was reread:
actual IP supplies the disjoint subgroups in the descending-lift proof;
IP of an intermediate quotient is not assumed. The resulting quotient
has order 2^(2d−1) and exponent four. A cyclic image therefore has order
at most four, giving the index bound 2^(2d−3). In the rank-three equality
case the full third lower-central term is contained in a largest cyclic
subgroup, and has order M/4.

The subsequent reduction uses this conclusion correctly. Two adjacent
orders at least eight would share the unique involution of that cyclic
term, contradicting actual IP. The proof of K = <r^4,h> establishes both
normality of the proposed subgroup and the class-two property of its
quotient. The M=8 elementary-abelian-derived-group argument and the M=4
boundary avoid extrapolating the M≥16 cyclic argument into invalid small
parameters.

The central product defining N has the claimed order and independent
normal coordinates. The two stated automorphisms preserve its identified
half-rotation exactly in the allowed cases, commute and square to one.
The square computations bound the exponent in each of the four cosets;
the parabolic normal forms prove all three maximal intersections and
hence the full rank-three IP. The center computation distinguishes the
two unmarked groups when M≥8, including the exclusion of elements outside
N. Thus the classification is of abstract groups as well as the exhibited
markings.

The identity h^b = (abcb)^2 is valid already under the common Coxeter
relations. With the extra source relator it supplies the collecting
relations and central half-rotation. The normal-form upper bound and the
model of the same order identify the literal universal presentation,
rather than just a finite image. Both directions of the substitutions
between (a,b,c) and the source's (p,q,rho) were checked. The complete
actions on the two product factors specify the semidirect products
unambiguously. The affine [4,4] quotient proves the required infinitude
of [4,M], and exact adjacent orders prove smoothness.

Finally, the disconnected-component argument uses commuting factors and
IP to obtain an internal direct product. The largest exponent argument
excludes additional nontrivial components beside a rank-three component,
and excludes two nonabelian dihedral components at cyclic index at most
eight. The remaining elementary-abelian and dihedral products give all
four smaller or disconnected clauses of Theorem 4.1.

## Source contract and attribution

The source is *String C-groups from groups of order 2^m and exponent at
least 2^(m−3)*, arXiv:1607.01457v1. This review read the full extracted
Theorem 4.1, its partial proof, Proposition 4.2 and its proof, the source
conclusion, and the surrounding catalogue scope. It separately displayed
the source's printed pages 11 and 13. It did not independently verify the
31-page abstract-group catalogue entry by entry. The earlier independent
review records its broader source reading separately.

The displayed pages confirm that the last parameter assignment in
Theorem 4.1(5) is opposite to the assignment in Proposition 4.2. The new
proof and actual product actions agree with Proposition 4.2 and the
conclusion: the inner product is direct for epsilon=0 and nontrivially
semidirect for epsilon=1. This is an explicit correction to the checked
edition, with no claim of correction priority or of checking every later
version.

Loyola retains attribution for the classification and source
presentations. The new deduction uses the already proved forest-quotient
recognition in Module A and the cyclic-index argument to avoid the
separate exhaustive abstract-group lists. The 123+14 lists, their
completeness, involution tables and individual catalogue exclusions are
not recovered by this note. Their omission is the reason that this is a
partial source contract even though the complete C-group classification
is recovered. The source is an auxiliary comparison outside the fixed
161-entry registry; no registry or complete-module count is increased.

## Verification and accounting

A fresh root replay passed with GAP 4.15.1. The coordinate checker covers
11 allowed cases with M=4,8,16,32,64,128 and all 704 marked-subset
intersections. The literal-presentation program independently covers the
seven allowed cases through M=32, checks both inverse presentation maps,
and confirms that the excluded M=4,epsilon=1 presentation collapses to
order 16 with right adjacent order two. These are corroborating finite
checks; the uniform conclusion rests on the written proof. The previously
recorded nine wrapper controls remain historical checked evidence and
are not described as a fresh root rerun.

The complete new proof costs 14,968 UTF-8 bytes. Required shared inputs
are the exact A second edition and U third edition named in the manifest.
The full optional finite-validation and replay programs are recorded
separately; they are not hidden inside a proof-length saving. No matched
length ratio, full Lean certificate, new open-conjecture solution or
historical mathematical novelty is claimed by this attachment.
