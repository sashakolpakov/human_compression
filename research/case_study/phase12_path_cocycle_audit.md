# Independent all-rank audit of the path cocycle correction

10 October 2026. **PASS: no gap found in the all-rank written proof.**
This review is independent of the root author and of the separate GAP/NQ
rank-four construction. The checker was also freshly executed in a temporary
directory. Internal review is not external peer review or a priority claim.

## Exact source comparison

I read the local primary manuscript Hou–Schulte,
[*String C-groups of 2-power order project onto a common string C-group*,
arXiv:2605.20691v1](https://arxiv.org/html/2605.20691v1): its nondegeneracy
definition, §3 defining presentation, §4 equations (7)–(9), Theorem 4.2,
and the surrounding proof. The exact local PDF and extraction hashes are
bound in the JSON. The source's A_i retains all adjacent rotations except
that rotation i is squared. It does not remove that squared generator or
take the Frattini subgroup of a different parabolic.

The hypothesis requires a finite string C-group, with every adjacent product
of order at least four. The reviewed family has every adjacent order exactly
four and satisfies the full subset intersection property. Thus it lies
inside the exact hypothesis, without an exception for its minimal order.
The source's common-quotient target has precisely the central-adjacent-square
presentation realized by the coordinate group.

## Written mathematics checked

The bilinear cocycle β(v,w)=Σ v_i w_(i−1)c_i is normalized and satisfies
the associative cocycle equation. The displayed inverse is correct. The
marked involutions have independent vertex coordinates, and their adjacent
commutators give every independent central edge coordinate. This proves the
order and generation, not merely an upper estimate from a presentation.

For every set I of vertices, products have support only on I and its
internal edges. Conversely the marked generators and their commutators
give every coordinate of that support space. Thus the exact subgroup
support formula holds and implies all pairwise intersection identities.
The source presentation collects to at most the same number of binary
normal forms, proving equality with the coordinate group. There is no
circular dependence on the source's Theorem 4.2.

Each A_i contains the entire central edge space: its ordinary rotations
supply their squares, and the missing one is explicitly retained. Its
vertex image has dimension d−2. For its Frattini subgroup, every square
of a word lies in the span of generator squares and pairwise commutators;
all those squares and commutators are central of exponent two. At an
endpoint the missing edge coordinate cannot appear, because every other
rotation vector has zero coordinate at that terminal vertex. At an internal
index it does appear as [σ_(i−1),σ_(i+1)]=c_i. There are no extra terms in
this commutator: the two supports have exactly one adjacent crossing.
Consequently

    Φ(A₁)=<c₂,…,c_(d−1)>,
    Φ(A_(d−1))=<c₁,…,c_(d−2)>,
    Φ(A_i)=Z for 2≤i≤d−2.

Their intersection is <c₂,…,c_(d−2)> of order 2^(d−3) for d≥3. At d=3
this is the empty span. At d=2 the separate direct calculation gives C=1.
These endpoint cases are correctly distinguished in the proof and code.

For d≥4 this contradicts the source's prescribed C-order, the prescribed
quotient order and identification, and C=γ₃(G). It does not disprove the
string C-group condition of the smaller quotient. Deleting central edge
coordinates preserves the same support-intersection argument; its interior
adjacent labels become two. Nor does it disprove the main common-quotient
existence theorem: this input group is itself the proposed common target.
All these boundaries are stated correctly in the reviewed note.

## Code inspection and fresh run

I inspected [phase12_path_cocycle_check.py](phase12_path_cocycle_check.py).
The low d bits encode vertices and the upper d−1 bits encode edges. Its
bitwise cocycle, multiplication, inverse and commutator match the written
convention. The closure routine computes actual finite generated subgroups.
The parabolic expectations are independently built by support predicates;
the Frattini subgroups are generated from squares of **every element** of
A_i, not merely from the potentially redundant supplied generator list.

I copied the checker unchanged into a fresh temporary directory and ran
Python there. It exited zero. Its generated JSON was byte-for-byte identical
to the author's report; the saved independent copy is
[phase12_path_cocycle_independent_run.json](phase12_path_cocycle_independent_run.json).
This covers ranks 2 through 6, with 299,584 cocycle comparisons and 5,456
pairwise parabolic intersection checks. The reported C-orders are 1,1,2,4,8.
The rank-four Frattini orders are exactly 4,8,4.

Centrality and generation checked by the program justify its reported
class two and trivial γ₃. The quotient orders follow by division; the
all-rank quotient intersection claim is a written support argument, not an
extra hidden Python test. The separate NQ rank-four audit checks that
quotient explicitly, but I did not rerun that already recorded independent
GAP script in this review.

The arbitrary-rank conclusion comes from the written cocycle/support proof.
The finite execution is a diagnostic certificate, not an extrapolation.
No claim is made here about a repaired kernel for general groups, a later
unexamined preprint revision, or a disproof of Theorems 1.1–1.2.
