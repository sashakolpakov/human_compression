# Review of the uniform label-eight construction

10 October 2026. **PASS for the stated all-rank finite construction.**
The complete argument gives a finite string C-group of order
\(2^{5d-7}\) and nilpotency class exactly four in every rank
\(d\geq3\), with exact adjacent order eight, all required additional
power relations, an explicit parity homomorphism, and the stated formula
for every parabolic. The full general conjecture and the universal source
group are not identified by this result.

## Edition, reading and independence

The frozen author manifest is `phase161_label_eight_manifest.json`,
SHA-256 `cc42875b6f23ff6b938066c0158bbb246e49b59950ea8777cf60ae30340a2ca3`.
The complete manuscript is 19,333 UTF-8 bytes, SHA-256
`131c75b8aed958d0d032a2e660058068627b45026e1067e528a5c27bb8b8a0d6`.
The collector is 7,030 bytes, SHA-256
`f9d8b925b982484635e717cefde854e2999bb5d6d02cef569af28da53de5f12c`.
Root read the entire final proof, collector, mutation/no-clobber controls,
dependency map and exact scope. The independent program
`phase168_label_eight_independent.py` rebuilds the printed table directly
and reduces the rightmost available pair; it imports no author code.

Root previously supplied exploratory nilpotent-quotient data and the
class-at-most-three obstruction. This review is independent of the
author's positive-presentation proof and collector, not an assertion that
root had no role in the research. The new consistency and support-transfer
arguments are read and checked below; the exploratory groups are not a
proof premise.

The accompanying reader repairs 97 missing or one-sided inline-math
delimiters. Its exact edit list binds the original and resulting bytes;
all formula content and prose are preserved. The original frozen author
status remains visible there and is superseded by this separate review.
No PDF rendering or all-page visual audit is claimed for this note.

## Uniform mathematical proof

**Termination.** The recursive order compares occurrences of the least
letter and then the fixed-length lexicographic tuple of higher-letter
blocks. Each level is well founded; deleting a nonempty suffix strictly
decreases the induced order. A square removes two least-letter occurrences,
a swap moves one left and shortens its preceding block, and a higher-letter
step decreases one block recursively. Later block growth cannot reverse
the earlier strict decrease. Triangularity of the actual table supplies
every required hypothesis.

**Transfer of every ambiguity.** A critical overlap has three input
letters, hence at most twelve supported indices in at most three connected
components. Translating these components with one missing index between
them places the support inside fourteen indices. The map is a bijection
on every permitted interval letter, preserving its type, anchor order
and boundary existence. Connected pairs translate by the same shift.
Disconnected pairs retain a gap and have no correction in either table.
Thus this is a rule-system isomorphism on the restricted supports, not
just a comparison of initial words. Support preservation keeps every
intermediate word in that subsystem. It transports complete joining
paths from rank fourteen back to the original rank. Disjoint reductions
commute, so all local ambiguities join. The terminating-rewriting diamond
argument then supplies confluence without assuming a consistent group.

**Actual group and all parabolics.** The irreducible words are precisely
the increasing binary subsets of the alphabet. Confluence identifies
monoid congruence classes with these words. The power relations make every
letter a unit, giving exactly \(2^{5d-7}\) group elements. The commutator
identities generate each auxiliary letter from the distinguished generators
on its own interval. Consequently normal forms supported in S constitute
exactly the marked subgroup on S: products and inverses preserve support,
and every allowed letter is generated there. Uniqueness of normal form
gives the intersection subgroup on \(S\cap T\), including disconnected
and empty supports. Counting its coordinates gives the declared parabolic
order formula. No quotient is presumed to preserve IP.

**Type, relators, class and parity.** Adjacent squares are the x letters,
whose squares are nonzero w letters of order two, so the adjacent order
is exactly eight. The eight local power words reduce to the empty word;
period eight and the support embedding give every integer exponent in
every consecutive triple. The displayed three subgroup levels form a
central filtration of length four. The commutator w0*w1 is a nonempty
normal form, making the class exactly four. Each distinguished-generator
count is invariant modulo two under every rule, so these counts give an
actual homomorphism to the binary coordinate group and then its sum
character. This is the parity needed by the mix theorem.

For the separate lower bound, a class-at-most-three group has commuting
adjacent commutators. The k=2 power word would identify the two nontrivial
fourth powers. Their common value is a rotation and cannot be the shared
reflection; it therefore contradicts the rank-three parabolic intersection.
This proves optimality of class four among nilpotent constructions under
these exact hypotheses, not among all possible groups.

## Finite and formal evidence

The fresh author replay of the final frozen collector passes all 2,016
rules, all 43,680 overlapping critical pairs, 49 auxiliary-generator
identities, all eight printed local normal forms and their squares, exact
adjacent powers and the nonzero class-four witness. The fresh ten controls
reject four algebraically plausible changes through failed critical pairs,
two structurally invalid rules, and four occupied output paths without
altering their contents or link targets.

The independently written rightmost collector passes the same 43,680
overlaps and the explicit local word table. Its critical-normal-form digest
is `c5f150119dbd84877056d3f6d97672f76463a7d9f54f325b81847d949bb1dd38`,
agreeing with the author result despite the different reduction strategy
and table implementation. Matching digests are output comparisons; the
actual exhaustive executions and the complete uniform proof above supply
the evidence. The fresh reports are separately bound in this review's
export record.

The phase167 Lean package is a separate formalization of the finite
rewriting lemma. Its exact source review, fresh build and alphabet boundary
must be recorded separately before formal admission. This written review
does not infer that all-rank termination, locality, confluence, the group
quotient or the complete polytope theorem have been formalized.

## Additive labels and source audit

The separate `phase168_label_eight_mix.md` discharges the exact input
hypotheses of the previously reviewed parity-fiber theorem. It gives
label 8n in every rank for
\(n=3\), \(n=2^e+1\) with \(e\geq2\), and
\(n=2^e-1\) with \(e\geq3\). The odd-label factor uses the actual
even-dimensional nondegenerate ambient quadratic space before restricting
its Dickson character, or the ordinary sign character for n=3. The new
factor is the finite two-group just proved. Exact adjacent order follows
from lcm(8,n), and the power words vanish in both coordinates.

That consumer was authored by root and independently read by the author
of phase161 against the exact earlier parity theorem and odd-factor
attachment. The consumer review passed at SHA-256
`ca08f4ea400e12f031963058978c9d432c430a09ecd63098fe60609673105fff`.
This independence concerns the new consumer; it is not a second independent
review of its author's own phase161 input.

Root freshly checked [Li–Zhang, Conjecture 3.7](https://arxiv.org/html/2505.09505v1)
and the finite-group convention in Definition 2.2. The request is existence
with exact constant type and the stated extra relations; identifying the
entire universal presentation is stronger. The [arXiv record](https://arxiv.org/abs/2505.09505)
still lists only the May 2025 v1. Four bounded title, author, conjecture
and label searches located no later resolution of these cases, but this
does not establish their current openness or priority. No priority claim
is made. The already published rank-three existence theorem remains
attributed to the source authors.

The normal-form construction and support-transfer argument are the new
proof contributions in this repository. Classical rewriting theory,
elementary commutator facts and the string-C-group/polytope correspondence
remain retained mathematics. The 8n consequence also retains the earlier
quadratic intersection theorem, Dickson character and marked mixing.
The three new author proof/check bodies cost 30,208 UTF-8 bytes before
the independent checker, consumer and review infrastructure. These are
acquisition costs, not a source-length compression ratio. The result
extends a question track; it does not add a completed source replacement
or an infinite compression factor.
