# Excess two: the remaining noncentral kernels

10 October 2026. Research proof; the phase18 class-three package
remains frozen. Internal written reviews and finite diagnostics are
separately bound records. No finite census is an input to the theorem.

Let G be a finite two-group with an ordered generating involution
marking r_1,...,r_d, d>=3, satisfying the string commutations, actual
intersection property, and adjacent product orders at least four.
Suppose |G|=2^(2d+1). Counts always mean ordered marked isomorphism
classes, not isomorphism classes of abstract groups.

**Theorem.** There are exactly

    a_2(d)=(25d^2−107d+122)/2

such markings. The class-at-most-three contribution is
(25d^2−125d+162)/2. The remaining 9d−20 markings have class four:
4d−8 have cyclic gamma3, and 5d−12 have elementary-abelian gamma3.
Their kernel support has size at most three. In particular their
canonical closed-neighborhood cores have rank at most five.

The complete type counts are:

| Adjacent orders | Number |
|---|---:|
| All four | binomial(d−1,2) |
| One eight, all others four | 4(d−2)^2 |
| Two eights, all others four | 8d^2−40d+52 |
| One sixteen, all others four | 4d−8 |

## 1. Retained inputs and exact local identities

The [forest quotient theorem](phase15_graded_support.md) gives
K=gamma3(G) of order four, with G/K the standard marked class-two
path group C_d. It also gives the exact parabolic restriction

    K intersect G_S = gamma3(G_S).                                 (1)

The nontrivial terms of a nilpotent lower-central series decrease
strictly; since |gamma3(G)|=4, gamma4 has order at most two and
gamma5 is trivial. Thus class(G)<=4. If K is central, the frozen
[class-three classification](phase18_class_three.md) applies. We
classify only the case that K is noncentral below. Then G has class
exactly four, K is either C4 or C2^2, and gamma4(G) has order two.
Write its nonidentity element as z. The conjugation image of the
two-group G in Aut(K) has order two, so its common fixed subgroup
is precisely <z>.

Use right conjugation and [x,y]=x^(-1)y^(-1)xy. Set

    c_i=[r_i,r_(i+1)],  alpha_i=c_i^2,
    beta_i=[c_i,r_(i+2)].

The alpha and beta words normally generate K. Indeed the elementary
weight-three collection gives K=<alpha_i,beta_i,gamma4>; taking the
normal closure of the displayed words and using nilpotency removes
gamma4 from this generation statement.

We use the exact [class-four collection table](phase15_common_quotient_class_four.md),
section 2. In particular,

    [alpha_i,r_(i−1)] = beta_(i−1)^2,
    [alpha_i,r_i] = [alpha_i,r_(i+1)] = alpha_i^2,
    [alpha_i,r_(i+2)] = beta_i^2,                                  (2)

and all its other marked commutators vanish. With
q_i=[c_i,c_(i+1)] and h_i=[beta_i,r_(i+3)], the beta table is

    [beta_i,r_(i−1)] = h_(i−1),
    [beta_i,r_i] = [beta_i,r_(i+2)] = beta_i^2,
    [beta_i,r_(i+1)] = q_i beta_i^2,
    [beta_i,r_(i+3)] = h_i,                                       (3)

with all other entries trivial. Undefined boundary terms are one.
These identities retain the weight-four corrections; a class-three
table alone would not justify the analysis.

An element of K with two marked supports belongs to their intersection
parabolic by actual IP. In particular no nonidentity element of K
has a one-vertex support. This support argument always takes place
inside G, rather than in an unproved quotient.

## 2. The cyclic-kernel family

Suppose K is cyclic of order four. If some beta_i had order four,
its square would be z. Equation (2) would force both alpha_i and
alpha_(i+1) to be noncentral, hence generators of K. Thus K would
lie in two different edge parabolics, whose intersection is a
one-marker subgroup. This contradicts (1). Consequently every beta
has order at most two, and is central.

Since alpha and beta normally generate noncentral K, some alpha_e
has order four. Put u=alpha_e. All other alphas are trivial: any
nonzero value would contain z in a different edge support. A beta
can equal z only if its triple contains the edge E={e,e+1}; otherwise
its intersection with E has at most one vertex. Thus the entire
parameter list is

    alpha_e=u of order four; all other alpha=1;
    beta_(e−1), beta_e independently in {1,u^2}, when defined;
    all other beta=1.                                             (4)

Equation (2) also determines the whole conjugation action on K:
r_e and r_(e+1) invert u, and every other marker centralizes u.
No further action parameter remains.

There are two choices at either end edge and four at each interior
edge, giving 4d−8. These markings have one adjacent product of order
sixteen, and all the other adjacent products of order four.

## 3. The elementary-abelian family

Now K=C2^2. Equations (2) show that every alpha is central, because
all alpha and beta squares are one. Thus each alpha is either 1 or z.
At least one beta_i is noncentral. Its minimal marked support is
its full triple T_i={i,i+1,i+2}: by (1) any proper subset of that
triple has kernel generated by central edge alphas, or has trivial
kernel.

First, the whole K has a connected support of size at most four.
Choose a marker r_j not centralizing beta_i. Then beta_i and its
conjugate are the two distinct noncentral elements of K and generate
K. Both belong to G_(T_i union {j}); if j lies outside T_i, literal
string commutation forces it to neighbor this triple. Therefore
K has support contained in an interval of at most four vertices.
Every other noncentral beta must have its full three-vertex support
inside that interval, by actual IP and the preceding minimal-support
observation.

There cannot be two such betas. They would have adjacent triple
supports T_i and T_(i+1), and their values must be distinct, because
their intersection edge has only central kernel. Equation (3) fixes
beta_i under r_i,r_(i+2) and beta_(i+1) under r_(i+1),r_(i+3).
The same nontrivial automorphism of K moves both noncentral elements;
hence all four of these markers centralize K. Every marker outside
the four vertices commutes literally with at least one of the two
triples, and therefore fixes a noncentral element of K and centralizes
K as well. This would make K central, a contradiction.

There is consequently exactly one noncentral beta_i; put u=beta_i.
For all other indices the beta value is central. The two possible
outside actions in (3) vanish: for example

    [beta_i,r_(i−1)]=h_(i−1)=[beta_(i−1),r_(i+2)]=1,

and likewise on the right. The endpoint actions also vanish.
Thus the only nontrivial marked action is

    u^r_(i+1)=u z; all other markers centralize K.                  (5)

In particular z=[u,r_(i+1)] has support inside T_i, and K itself
has the same three-vertex support. Any nonzero alpha must be one
of the two edges in T_i. Both cannot occur, since their common
vertex cannot support z. This gives the following exhaustive cases.

* No alpha is nonzero. Then every beta other than beta_i is trivial:
  otherwise z would have support in the intersection of two distinct
  triples, an edge with zero alpha or a smaller set.
* The left edge alpha_i equals z. Besides beta_i=u, the only possible
  nonzero beta is beta_(i−1), independently equal to 1 or z when it
  exists. All other alphas and betas are trivial.
* The right edge alpha_(i+1) equals z. Symmetrically beta_(i+1) may
  be 1 or z when defined, and all other values are trivial.

For each triple there is one first case. Summing the left-edge cases
over all triples gives 1+2(d−3)=2d−5, and so does the right-edge
case. The total is (d−2)+2(2d−5)=5d−12. Of these, d−2 have all
adjacent orders four; the other 4d−10 have a single eight.

## 4. An explicit noncentral elementary-abelian seed

The necessity argument has not assumed that its candidates exist.
Here is a concrete rank-three seed, with no subgroup catalogue.
Let V=(Z/4Z)^2, and let D8 act by the signed coordinate permutations.
In H=V semidirect D8, use the affine product

    (v,A)(w,B)=(v+A w,AB).

With e1=(1,0), set

    r1=(0,diag(1,−1)),
    r2=(0,[[0,1],[1,0]]),
    r3=(e1,diag(−1,1)).                                           (6)

These are involutions and r1 commutes with r3. The first two generate
the linear D8, whose element diag(−1,1) together with r3 supplies
translation e1. Conjugating by r2 supplies translation e2. They
therefore generate H, of order 16*8=128.

Both adjacent products have order four, so both alpha values are
one. Direct affine multiplication gives

    beta_1=translation(2e1)=u,
    [u,r2]=translation(2e1+2e2)=z,
    u^r1=u^r3=u,  u^r2=u z.                                      (7)

Modulo 2V the two edge commutators are central, so gamma3(H)<=2V.
The conjugates of beta_1 span 2V, giving gamma3(H)=2V and
gamma4(H)=<z>. Thus H/2V has order 32 and is the canonical C_3.
Every proper parabolic has trivial intersection with 2V: the edge
parabolics are dihedral of order eight, the endpoint parabolic is
C2^2, and the single-marker parabolics have order two, exactly as
in C_3. Quotient IP therefore lifts to actual IP in H (for two
proper parabolics the common kernel is trivial). This proves the
seed's order, class, type and IP directly.

## 5. Realizing every parameter list

We retain the explicit [central join](phase16_central_join.md) and
the [elementary edge/triple covers](phase17_k1_classification.md).
They preserve the ordered marking and have exact coordinate
parabolics. The following fiber constructions do not infer IP
merely from the quotient.

For (4), start with the dihedral group D32 on edge E, whose alpha
is u of order four, and attach it to the full path by the central
join. All beta values are initially trivial. For each desired
nonzero neighboring beta, take the fiber product over C_d with
the elementary triple cover having that beta as its single kernel
coordinate v. The diagonal marker lifts generate the full fiber:
alpha_e isolates u, and each chosen beta word isolates its v.
Identify every such central v with u^2. These are central quotient
relations, and the result has kernel C4 and the parameters (4).

The exact parabolic kernel in this quotient is K if E is contained
in its marker set, and one otherwise. Indeed every added triple
contains E. These kernels have the required intersection property;
lifting quotient intersections in C_d then proves actual IP.

For (5), attach the affine seed (6) on T_i to the full path by the
central join. Its kernel K=C2^2 is supported on T_i. In the case
with no active alpha no further operation is needed.

To set one adjacent alpha to z, take the fiber product with the
elementary cover on that edge E and identify its central coordinate
with z. If the extra neighboring beta is desired, also take its
elementary triple cover and identify that coordinate with z.
Before these identifications, beta_i isolates u and its commutator
with r_(i+1) isolates z; the new alpha and optional beta words isolate
their auxiliary coordinates. The diagonal markers thus generate
the full fiber. All identifying elements are central, so the
quotient has the prescribed kernel of order four and no loss in
the canonical quotient.

Its parabolic kernels are exactly

    K  if T_i is contained in S,
    <z> if E is contained in S but T_i is not,
    1 otherwise.                                                  (8)

The optional extra triple contains E, so creates no additional
kernel-support condition. These nested support conditions have
exact meets. As in the cyclic family, an element common to two
parabolics is lifted from their intersection in C_d and corrected
inside the common kernel, proving actual IP. This realizes every
case in section 3. Choosing both adjacent edges would instead put
z in two distinct edge parabolics and violate IP, as necessity
already showed.

## 6. Complete marked presentations and counts

The lists above contain every parameter and the full conjugation
action on the abstract four-element K. They determine the marked
group uniquely. To see this without an unstated extension-class
assumption, present the markers together with K, impose its known
multiplication table and marked actions, the involution and string
relations, and the prescribed alpha and beta words.

Modulo K, each c_i has square one and commutes with its endpoints
and right neighbor. It also commutes with its left neighbor: write
a=r_(i−1), b=r_i, c=r_(i+1). The preceding edge commutator [a,b]
commutes with b and c. Since a commutes with c, conjugating [b,c]
by a just replaces b by b[a,b], leaving that commutator unchanged.
All more distant commutations are literal. Thus the quotient is
class two and has order at most |C_d| by ordinary collection.
Since K was specified as a normal group of order at most four, the
whole presented group has order at most 4|C_d|. The constructions
in section 5 attain that order. This proves the complete presentation
and marked uniqueness. The alpha, beta and action words recover
the displayed parameters under any marked isomorphism.

Adding the noncentral counts gives 9d−20. Adding the frozen
class-three coefficient yields a_2(d). The type counts
in the opening table follow by separating the class-three parameters
according to their number of active edges: zero, one and two give
binomial(d−2,2), 4d^2−20d+26 and 8d^2−40d+52 respectively. The
new elementary-abelian cases add d−2 to the first and 4d−10 to the
second; the cyclic cases supply the sixteen family.

The proof uses no interpolation, opaque finite group catalogue,
or assertion that a quotient automatically inherits IP. Computational
checks and source-table comparisons will be recorded separately.
This proof makes no publication-priority or full Lean claim.

## 7. Current diagnostics and primary-source comparison

The [standard-library affine checker](phase19_k2_affine_check.py)
directly constructs the seed (6), without GAP or a group catalogue.
Its [report](phase19_k2_affine_check.json) confirms 128 elements,
lower-central orders 128,16,4,2,1, all eight parabolic kernels and
orders, and all 64 actual parabolic intersections.

The separate [GAP/NQ family checker](phase19_k2_check.g) constructs
every proposed noncentral parameter list in ranks three through five.
The [transcript](phase19_k2_check.log) records 7,16,25 groups,
respectively, and 1,112 exact parabolic kernel/order checks and
30,144 actual intersections in total. All pass. This tests all
proposed families in those ranks; it is not an independent search
for additional families. It uses GAP 4.15.1 and NQ 2.5.11, preserving
the distinguished free-generator images through the actual NQ
epimorphism. The analytic existence argument does not rely on NQ.

The primary [Conder author census, June 2012](https://www.math.auckland.ac.nz/~conder/RegularPolytopesWithFewFlags-ByOrder.txt)
lists nondegenerate regular polytopes up to 2,000 flags, with one
record per isomorphism/duality class and an SD or NSD flag. Its
rank-three/order-128 entries give eight duality classes, three
self-dual, hence 13 ordered markings. Rank four/order 512 gives
26 duality classes, five self-dual, hence 47 ordered markings.
The type multiplicities also agree with the table above.

The [portable header parser](phase19_k2_source_check.py) and its
[report](phase19_k2_source_check.json) record those comparisons and
the source checksum. This comparison identifies counts and types,
not individual source presentations. Rank-five/order-2,048 is beyond
that census limit. The source text remains a private input and is
not distributed with these original artifacts. These known finite
counts preclude treating the corresponding numerical cases as new;
priority for the uniform classification has not been established.

Reproduction, from the artifact directory:

    python3 phase19_k2_affine_check.py --output /tmp/phase19_affine.json
    gap -q -T phase19_k2_check.g
    python3 phase19_k2_source_check.py --source downloaded_census.txt --output /tmp/phase19_source.json

The saved family transcript strips only leading GAP line-control
characters. All three computations are bounded diagnostics or source
comparisons, not proof inputs to the all-rank theorem.
