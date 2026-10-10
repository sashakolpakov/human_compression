# Fixed nilpotency class and finite boundary states

10 October 2026. Research draft with separate internal written reviews
and bounded diagnostics. Frozen phases eighteen and nineteen remain unchanged. The
deletion quotient below is part of the state: overlap isomorphism of
two windows alone is not assumed sufficient.

Fix c>=2. Consider finite two-groups with ordered generating involutions,
path commutations, actual IP, no adjacent product of order two, and
nilpotency class at most c. Isomorphisms preserve every marked generator.

**Theorem.** This category, over all ranks d>=c, is in
bijection with the accepted walks of an effectively finite directed
graph. A state consists of a marked rank-c window H and a quotient
of its last c−1 parabolic. Its transitions are exact tests in bounded
finite groups. The order increment is determined by the new window.
Consequently the bivariate generating function counting by rank and
excess log2|G|−(2d−1) is rational. No efficiency bound on constructing
the finite alphabet or transition graph is claimed.

The proof has four ingredients: normal-closure locality; parabolic-coset
Helly for *string* C-groups; a compatible semidirect-product amalgam;
and an exact update rule for the deletion quotient. Each is given below.

## 1. Normal closure stays in a bounded final window

Let G=<r_1,...,r_d> have class at most c and the path commutations.
For now IP is not needed. The normal closure N of r_d is generated
by the left-normed commutators

    [r_d,r_(i1),...,r_(it)]  (0<=t<=c−1),                         (1)

where t=0 means r_d itself. Indeed conjugating any listed word by
a marked involution multiplies it by its next listed commutator;
at weight c the next commutator vanishes. The subgroup generated
by the list is therefore normal, contains r_d and is contained in
its normal closure.

A nontrivial word of weight w in (1) has support in the last w
vertices. At every stage, adjoining a generator separated from the
current support makes the commutator trivial by the literal string
relations. Otherwise its support remains a final interval and can
expand left by at most one vertex. Thus

    N <= G_{d−c+1,...,d}.                                         (2)

Moreover all markers r_j with j<=d−c centralize N. For a word of
weight w<c they commute literally with its support, which starts
at or after d−w+1>=d−c+2. For a word of weight c the extra commutator
has weight c+1 and vanishes. This proves the assertion on the
generating list (1), hence on N.

If P=G_{1,...,d−1}, H=G_{d−c+1,...,d}, and
B=G_{d−c+1,...,d−1}, then G=PN=PH. When G has actual IP,

    P intersect H=B,   |G|=|P||H|/|B|.                            (3)

In particular the normal closure need not intersect P trivially.
No deletion retraction onto P is asserted.

This already proves a uniqueness statement. Given the actual marked
P and H with their common B, impose their presentations, all string
relations and class at most c on the full marking. The resulting
group W maps onto G. By (2) it is a product of the images of P,H,
so its order is at most |P||H|/|B|, which is |G|. Hence W maps
isomorphically onto G. Induction shows that every actual group is
determined by its consecutive rank-c windows (with the initial
shorter prefix). Existence of a window sequence still requires the
conditions below.

## 2. The parabolic-coset Helly lemma

**Lemma.** In a string C-group, any finite pairwise-intersecting family
of left cosets of standard parabolic subgroups has a common element.

We retain the established string-C-group/regular-polytope correspondence
and the identification of standard parabolics with stabilizers of
subflags. These statements are given in Schulte,
[*Regular Incidence Complexes, Polytopes, and C-Groups*](https://arxiv.org/pdf/1711.02297),
Lemma 3.1 and section 5, by specialization of Theorems 4.1–4.2.

Here is the resulting Helly argument, including arbitrary parabolics.
Choose a base flag. The coset gP_S consists precisely of the
automorphisms taking its faces of types outside S to the corresponding
partial flag under g. If two such cosets intersect, their prescribed
partial flags are compatible. In a pairwise-intersecting family every
two prescribed faces are comparable, and prescribed faces of the same
rank agree. The union is therefore a chain. Extend that chain to a
full flag. Flag transitivity supplies an automorphism taking the base
flag to this full flag; it lies in every coset in the family.

This does not infer coset Helly from subgroup IP alone. The string
condition supplies an actual regular polytope, whose flags are chains.
The assertion is not being extended to arbitrary C-groups or arbitrary
coset incidence geometries.

## 3. Bounded data for an extension step

Suppose P has rank n>=c. Its last c−1 parabolic is

    B=<r_(n−c+2),...,r_n>.

Let A denote the set of old marked generators
{r_1,...,r_(n−c+1)}; it is a set, not an additional parabolic symbol.
The quotient P/normal_closure_P(A) is generated by B. Record its
kernel on B as

    R = B intersect normal_closure_P(A),
    P/normal_closure_P(A) = B/R.                                  (4)

This is the deletion quotient, not a claim that killing A fixes B
injectively. The state records the preceding rank-c window

    H_old=<t,B>,  t=r_(n−c+1),

together with R as a concrete normal subgroup of its marked B.

Choose a candidate marked rank-c group H with first c−1 parabolic
identified with B and final generator u. This identification is a
marked isomorphism and hence is unique if it exists. Require H to
belong to the same class-at-most-c, nondegenerate string C-group
category. Compute, entirely inside H,

    N = normal_closure_H(u),    J=N intersect B.                    (5)

The candidate transition is accepted exactly when both tests hold:

* (A) the conjugation action of B on N kills R;
* (B) the generator t in H_old centralizes J, with J viewed as a
  subgroup of the shared marked B.

All these are tests on the finite state and candidate window. They
are necessary for any actual extension G. Locality shows that all
old markers centralize N, so its P-action factors through (4),
proving (A). Also J=P intersect N in an actual extension, proving
(B). Its normal closure under H equals its normal closure under G,
because P is generated by B and old markers centralizing N.

## 4. The compatible semidirect construction

Tests (A) and (B) are sufficient to embed the groups with the exact
intersection. Use left conjugation for this construction. Test (A)
gives the unique action

    alpha:P -> B/R -> Aut(N)                                      (6)

that extends the action of B from H and kills every old marker.

The subgroup J is normal in P. It is normal in B because N is
normal in H. The last old marker t centralizes J by (B), while
all earlier old markers commute literally with every generator of
B. Thus the inclusion of J in N is P-equivariant. For j in J,
alpha(j) is conjugation by that same element in N, since this is
already true in H.

Form the semidirect product N semidirect_alpha P with product

    (v,p)(w,q)=(v alpha(p)(w),pq).

Inside it the diagonal subgroup

    D={(j^(-1),j):j in J}                                         (7)

is normal. It is a subgroup because alpha(j) is inner conjugation
by j. It is normalized by P by equivariance, and centralized by N
by the inner-action identity. Its intersection with either factor
is trivial. Define

    G=(N semidirect_alpha P)/D.                                   (8)

Both P and N embed; their intersection is exactly the identified J.
The subgroup generated by N and B is isomorphic to H, since
H=NB with N intersect B=J and the same conjugation action. Hence

    P intersect H=B,   G=PH,
    |G|=|P||H|/|B|.                                              (9)

The generators are the original marking of P followed by u.
Every old marker centralizes N and hence u. All remaining string
relations hold in H. The marked involutions generate G, and each
adjacent product has its unchanged order in P or H.

The group G is a finite two-group. It has class at most c. To see
this, consider a left-normed commutator in marked generators of
weight c+1. A word containing no u lies in P and vanishes; a word
containing no old marker lies in H and vanishes. If it contains
both, consider the first occurrence of u. If an old marker occurs
earlier, the initial commutator lies in P and has trivial image
under alpha, so it commutes with u and the word vanishes. Otherwise
the initial commutator involving u lies in N, and the first later
old marker centralizes N and makes the word vanish. The same
argument applies if the initial letter itself is u. Thus every
weight-(c+1) marked commutator is trivial. Such commutators generate
gamma_(c+1)/gamma_(c+2); in a finite nilpotent group equality of
successive lower-central terms implies they are trivial. Therefore
gamma_(c+1)=1.

## 5. Actual IP of the extension

For a subset S of the full marking, let P_S and H_S denote the
subgroups on its selected prefix and window markers. Then

    G_S=P_S H_S.                                                  (10)

If u is absent this is immediate. If u is present, its normal closure
under the subgroup on S is its normal closure under H_S: old markers
act trivially on N, while its selected boundary markers are in H_S.
Thus G_S=P_S N_S and H_S=B_S N_S, giving (10). The equalities
P intersect H=B and actual IP in P,H imply

    P_S intersect H_S=B_S,
    P intersect G_S=P_S,    H intersect G_S=H_S,                   (11)

where B_S is the subgroup on the boundary markers selected by S.

Let x belong to G_S intersect G_T. Write x=p h=p' h', with
p in P_S, p' in P_T, h in H_S, h' in H_T. Then

    p'^(-1)p=h'h^(-1) in P intersect H=B.

The left coset pB consequently meets both P_S and P_T. These two
parabolics meet each other at the identity. The Helly lemma in P
gives p0 in P_S intersect P_T intersect pB. By actual IP in P,
p0 lies in P_(S intersect T). Moreover p0^(-1)p lies in B_S and
p0^(-1)p' lies in B_T. It follows that p0^(-1)x lies in both H_S
and H_T, hence in H_(S intersect T). Equation (10) gives
x in G_(S intersect T). This proves actual IP; the reverse inclusion
is immediate. There is no assumption that an arbitrary quotient
preserves IP.

## 6. Exact deletion-kernel update

Let b be the first marker of the old boundary B. The next boundary
B_new is the last c−1 parabolic of H. Its omitted old markers are
A together with b. The next deletion quotient is exactly

    Q_new = H/normal_closure_H(R union {b}),
    R_new = B_new intersect normal_closure_H(R union {b}).         (12)

To justify this without forgetting relations from the past, give G
the following universal presentation: the presentations of P and H,
identified on B, together with [a,v]=1 for every old generator a
and every v in N. The imposed conjugation relations are exactly
the action alpha in (6): they are the existing B-action and the
trivial action of every old marker. Hence N semidirect_alpha P
maps onto this presentation group. The diagonal D maps to the
identity because the two copies of J have been identified, so
(N semidirect_alpha P)/D maps onto it. Its order is therefore at
most |N||P|/|J|. It also maps onto (8), which has exactly that order.
Thus this is a presentation of G itself, without assuming that
the factors embed in an arbitrary presentation quotient beforehand.

Killing A in that presentation replaces P by B/R and makes every
extra commuting relation trivial. The remaining presentation is
exactly H with R killed. Killing b gives (12). The quotient is
generated by the images of B_new, so its kernel there is exactly
the recorded R_new. This update is a computation in H alone.

In particular two prefixes with the same state admit precisely the
same transitions, with the same next state and order increment.
Their full groups need not be isomorphic; their retained boundary
information is exactly sufficient for all future extension tests.

## 7. A genuinely finite alphabet and exact accepted walks

There are finitely many marked rank-c groups of class at most c
generated by involutions. A crude explicit bound suffices. Each
lower-central quotient is generated by at most c^j marked
commutators of weight j. These quotients have exponent two, because
their degree-one generators have order two and the associated
graded commutator is multilinear. Thus their orders are at most
2^(c^j), and every such group has order at most

    2^(c+c^2+...+c^c).                                           (13)

One can therefore enumerate finite multiplication tables up to this
bound, ordered markings, and test the defining conditions, removing
marked duplicates. This is an effective finite procedure, with no
claim that it is practical. For each marked H, there are finitely
many normal subgroups R of its last c−1 parabolic B. This supplies
a finite state set, including states that may never be reached.

At initial rank d=c, each group H supplies its unique initial state:

    R=B intersect normal_closure_H(first marker).

Apply the tests in section 3, the construction in sections 4–5,
and update (12). Necessity proves that every actual group gives
an accepted walk. Sufficiency constructs an actual group for every
walk. The state update is deterministic once the next marked window
has been chosen; overlap identifications are unique because all
generators are marked. Finally the uniqueness argument in section 1,
or the exact universal presentation in section 6, shows that two
different window walks cannot give the same ordered marking.
Thus this is a classification by accepted walks, not merely an
upper bound on the number of groups.

## 8. The weighted transfer and its precise limits

For counting by excess, retain the proved
[forest canonical quotient](phase15_graded_support.md). Give an
initial state arising from H the weight

    x^(log2|H|−(2c−1)).

Give an accepted transition with new window H and overlap B weight

    x^(log2|H:B|−2).                                              (14)

These are nonnegative integer powers. The canonical quotient and
its parabolic restriction identify the latter exponent with
log2(|gamma3(H)|/|gamma3(B)|). By (9), the exponents telescope to
log2|G|−(2d−1) along every walk.

Let v(x) be the finite vector of initial weights, M_c(x) the
finite polynomial transition matrix, and 1 the terminal all-ones
vector. Then, with row-vector convention,

    sum_(d>=c,k>=0) a_(c,k)(d) t^d x^k
      = t^c v(x) (I−t M_c(x))^(-1) 1.                            (15)

Ranks below c add only a finite polynomial. Thus the joint count is
rational, and the unweighted rank count satisfies a constant-coefficient
linear recurrence. This supplies a uniform finite-state framework
for every fixed nilpotency class, extending the role of the explicit
two-state class-three transfer without asserting that this larger
automaton is minimal.

The proof does not classify arbitrary nilpotency class with a fixed
finite alphabet, give efficient bounds for the alphabet size, or
assert that matching windows alone suffice. The quotient R in (4)
retains relations caused by deleting old generators; dropping it
would remove a necessary compatibility test. No group catalogue,
finite interpolation, publication-priority determination or Lean
formalization is an input or conclusion here.

## 9. Smaller window alphabets for a prescribed excess

Fix k>=1 without imposing a nilpotency-class bound in advance. The
forest quotient gives |gamma3(G)|=2^k. Successive nontrivial terms
of the lower-central series of a finite nilpotent group decrease
strictly. There can consequently be at most k nontrivial terms
starting at gamma3, so the class is at most k+2.

Apply the theorem with c=k+2. Every rank-c window H satisfies

    gamma3(H)=gamma3(G) intersect H,
    log2|H|−(2c−1)<=k.

Thus it suffices to use windows of rank k+2 and order at most

    2^(2(k+2)−1+k)=2^(3k+3).                                    (16)

Discard the other windows, and perform the transfer calculation
in the polynomial quotient ring with x^(k+1)=0. All weights are
nonnegative, so this removes only walks already exceeding the
chosen budget. The coefficient of x^k is exactly the unrestricted
fixed-excess count. Ranks d<c can be handled separately; their
groups have order at most 2^(3k+1).

For k=0 the class-two case gives the unique path cocycle marking
in each rank. For k=2, the necessary rank-four alphabet through
excess two has 1+10+47=58 windows and maximum order 512, by the
separately proved first- and second-excess classifications.

This is a bound on the local groups required for the transition
algorithm. It does not assert that the canonical whole core from
the fixed-excess support theorem has rank k+2, nor compare unrelated
description-cost conventions. Both state enumeration and the normal
subgroup computations may still be expensive.

## 10. Reproducible bounded diagnostics

The uniform proof above does not depend on these computations.

The [class-two/three checker](phase20_finite_state_check.g) starts
from the universal rank-three class-three involutory path group of
order 256. It tests all 16 subgroups of its central gamma3 of order
eight, with no alpha/beta parameter filter, and retains all 13
actual-IP quotients. They give 13 reachable states and 89 transitions.
The checker constructs all 89 resulting rank-four groups through
the semidirect product and diagonal quotient, then checks their
orders, class, factor embeddings, deletion kernels and all actual
parabolic intersections. Including the alphabet tests, this gives
1,552 parabolic closures and 23,808 intersections. Weighted walk
counts through rank ten agree coefficient by coefficient with the
independent class-three formula: the first totals are 13, 89, 610.
The unique class-two D8 window, its trivial deletion kernel and
trivial attachment intersection are also checked.

The [class-four checker](phase20_finite_state_class4_check.g) rebuilds
that class-three pool and adds the sixteen noncentral rank-four
second-excess windows from the separately proved
[second-excess classification](phase19_k2_classification.md).
Filtering to excess at most two gives 58 windows, 58 reachable
states and 258 transitions. Every one of the 258 rank-five
semidirect/diagonal constructions passes the same group checks.
There are 44 nontrivial diagonal subgroups; all are central in
these examples. This second run performs 9,808 parabolic closures
and 288,000 intersections in total, including its repeated
class-three pool construction. Its truncated walk counts through
rank twelve agree with

    [x^0]=1, [x^1]=5d−10, [x^2]=(25d^2−107d+122)/2.

The class-four alphabet's stated completeness through excess two
retains the earlier class-three and second-excess classifications.
It is not an enumeration of all class-four windows. In both bounded
automata every overlap-compatible transition passes tests (A) and
(B). Thus the diagnostics test positive constructions, updates and
counts, but do not exhibit a genuine extra compatibility rejection
or a noncentral diagonal subgroup. The general proofs of those
cases are the written arguments in sections 3–6.

With GAP and its NQ package available, run:

    gap -q -T phase20_finite_state_check.g
    gap -q -T phase20_finite_state_class4_check.g

The saved logs remove only any initial carriage-return/newline
emitted by GAP. The accompanying JSON records bind the executed
source bytes, logs, versions and exact finite scope. No external
group catalogue or copyrighted source file is needed to run them.

## 11. Retained inputs and status

The classification construction in sections 1–7 uses elementary
finite nilpotent-group facts and the established string-C-group /
regular-polytope correspondence. The latter supplies the precise
Helly bridge: Schulte's source cited in section 2, axiom (I2) on
printed page 2, Lemma 3.1 on page 5, and the specialization in
section 5 on pages 13–14. The retained result is standard background,
not a new claim that arbitrary C-groups have coset Helly.

The excess grading and window-order improvement additionally use
the forest canonical quotient and its exact gamma3 restriction,
with their separate proof and review records. Earlier explicit
class-three and second-excess counts are comparison inputs for
the finite diagnostics, not ingredients in the uniform transition
proof. Primary-source locators, retrieval checksums and reading
scope are recorded in the [source intake](phase20_finite_state_source_intake.json).

This is an internally reviewed research proof, not a claim of
external peer review, complete publication-priority clearance or
Lean formalization. The finite tests do not prove the uniform
theorem; its force comes from the explicit necessity, construction,
actual-IP, update and uniqueness arguments above.
