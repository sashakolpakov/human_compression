# Root admission of two design-residue corrections

Date: 2026-10-10. This admission concerns specified assertions of L092,
not a replacement of its entire fourteen-page source. The source is
D. Leemans, *A Generalization of a Construction due to Van Nypelseer*,
Beiträge zur Algebra und Geometrie46 (2005), 561–574. The primary PDF
has SHA256 f76a72aeec658ace5d821519a686c3041e455d3a1c5c4276988bd711ba830403.

## Mathematical conclusions and attribution

For the source's iterated deleted-line construction, q>3, the accepted
uniform proof shows firmness and (IP)2 for all q, residual connectedness
exactly when q>4, and flag transitivity exactly when q=4 or8. The
conjunction selects q=8, correcting the value q=4 in printed Theorem6.
The preceding full-automorphism assertion also omits a factor two:
the dual net permits exchange of its two omitted parallel classes.

The proof recovers all automorphisms intrinsically from the Hamming
noncollinearity graph, then proves that its coordinate permutations are
semiaffine. The chamber orbits reduce to field automorphisms and inversion
on F_q*\{1}. Both rank-two residue calculations and global connectivity
are explicit. No unexamined supergroup can supply additional chamber
transitivity, because the constructed geometry recovers the underlying
net and all its flag objects.

For the classical subline designs S(3,q+1,q^e+1), q≥3,e≥2, Construction2
is firm and residually connected exactly when e=2. This corrects printed
Lemma5. The full group and chamber counts, with the explicitly retained
Kantor classification, still select q=4 in dimension two. Thus this
correction does not refute the source's subline branch of Theorem11.

The construction, classical designs and elementary projective theory
remain attributed inputs. The subline automorphism upper bound is retained
from Kantor, *Homogeneous designs and geometric lattices*, JCTA38 (1985),
66–74, Theorem3 and its proof on p.73. It is not obtained merely by
quoting the abbreviated Theorem10 in L092. The independent reviewer
recovered the full primary PDF, SHA256
36532c56e2af68c0b043c3b21818dbc71fe5ce250e9f380315e122842de308a2.
The frozen root manuscript's earlier unsuccessful acquisition report
is historical and does not describe a current gap.

Neither correction is counted as an open-conjecture solution. Historical
priority has not been established. The source's Hermitian-unital question
and the existing proof attempt remain in their separate question track.

## Review and independent computation

The root read the complete L092 extracted text and visually checked the
primary definitions and contested statements, including printed pages565,
568 and571. The source author is identified from the primary title page;
the occurrence of Van Nypelseer's name in its title is not coauthorship.
The root read the entire independently written deleted-line proof,
its Lean source and source bridge, both finite root programs, and the
complete independent subline review and its GAP/Python programs.
The retained Kantor proof on printed p.73 was checked in the primary PDF.

The deleted-line proof was written by an agent before reading the root's
finite checker. The root independently checked its group reconstruction,
duality, all panel counts, the two residue graphs, and the Frobenius/inversion
orbit argument. The subline proof was written by the root and independently
reviewed by another agent in phase183. Its native-GAP arithmetic,
cross-ratio block construction, typed Cartesian flag enumeration and
component-merging algorithm differ from the root's custom field, PGL
orbit, recursive flag generation and breadth-first search.

For q=3,e=2 the two full incidence encodings agree after an explicit
field isomorphism. There are230 objects,2160 chambers and1881 connected
residues of rank at least two. The independent program also checks all1650
rank-two partial-linear-or-digon conditions. Exhausting the7! permutations
fixing a projective triple proves the normalized full-design stabilizer
has order2. With sharp triple transitivity and the written geometry-group
reconstruction, the full geometry group order is1440. The argument does
not confuse a subgroup's two chamber orbits with a full-group exclusion.

A wording correction to the frozen phase183 review: in Section1,
Theorem6's input is a **rank-two residue of a rank-three construction**,
not a rank-three input geometry. This descriptive slip does not affect
the reviewed Construction2 incidences, proofs or acceptance decisions.

## Lean and fresh public replay

The fresh public run of `phase185_corrections_check.py` passed in17.404
seconds on this machine. Its complete records are in
`phase185_public_replay/`. It checked q=4 andq=8 directly, reran the
independent q=3 subline check and exact incidence comparison, compiled
`formal/DeletedLineFourResidue.lean`, and rejected all four targeted
mathematical mutations. Two mutations alter the subline disjointness
rules; two alter the literal F4 flag-center equation or the cycle modulus.
These controls do not claim exhaustive mutation coverage.

The formal file constructs F4 as two copies of ZMod2 with the specified
multiplication and verifies its field-table laws. It parametrizes both
residue types by the nonzero powers and defines incidence by the literal
equation x=a(y+t). The component invariant is a proved consequence.
An explicit bijection identifies its eighteen vertices and every edge
with three disjoint6-cycles; a reachability argument proves disconnection.
Seven exact named axiom reports contain only propext, Classical.choice
and Quot.sound. The root read the complete formal proof and the written
source-isomorphism bridge. The source-to-residue identification and both
uniform classification proofs remain written mathematics.

The run checked the pinned Lean version, every dependency git revision
and tracked-file cleanliness. Compiled dependency objects remain trusted
build inputs. It did not rebuild Mathlib or formalize GAP's computations.
The author wrapper requires its original private primary PDF; the new
public driver avoids that input and records the primary bindings through
this review instead. No primary full text or raster capture is distributed.

## Accounting and remaining full-source work

One new scoped Lean component brings the public total to70:69 have
standard axiom reports, and the one historical transfer component retains
its four explicitly recorded native-evaluation axioms. This is a component
count, not a count of complete formalized manuscripts.

The published known-result coverage totals and compression rates are
unchanged. There is no matched-source ratio for this correction package,
no extra complete principal-source credit, and no established new sawtooth
drop. The private continuation is working toward the whole L092 contract:
the reusable derived-design residue reduction, all projective and affine
cases, the Mathieu extension conditions, and the remaining diagram and
group annotations. That unfinished work is excluded from this admission.
