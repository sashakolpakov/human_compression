# Geometric intersection as a flag-constrained covering problem

This note revisits the geometric intersection property in P. Jacobs and
D. Leemans, *An algorithmic analysis of the intersection property*, LMS Journal
of Computation and Mathematics 7 (2004), 284–299,
[DOI 10.1112/S1461157000001133](https://doi.org/10.1112/S1461157000001133).
The target is the decision problem of Sections 2–3, including its residue and
weak variants. This is **geometric shadow-IP**, not the subgroup intersection
property of C-groups. The equivalence below supplies a common Boolean and
integer formulation; it does not by itself reproduce the paper's sporadic
classification tables or prove that this formulation is faster.

## 1. Retain the witness, not just the intersection

Let a finite typed incidence structure have vertex set $X$, type classes
$X_i$, and reflexive symmetric incidence $\sim$. Distinct vertices of the
same type are not incident. A flag is a pairwise incident subset; the empty
flag is allowed. Write

$$\sigma_i(T)=\{y\in X_i:y\sim v\text{ for all }v\in T\}$$

for an arbitrary subset $T$, which need not be a flag. For a vertex $x$ and
a flag $F$, set $U=\{x\}\cup F$ and $S=\sigma_i(U)$. The local shadow-IP
condition is automatic when $S$ is empty. Otherwise it requires a flag $C$
whose vertices are incident to all of $U$, and whose $i$-shadow is exactly
$S$. Requiring this for all $i,x,F$ in every residue of rank at least two
gives the source's IP. Requiring, in each such residue, at least one type
satisfying all its tests gives WIP. The existential type is chosen separately
for each residue. Rank-one tests are automatic; rank-zero residues are not
subjected to an existential type requirement. This is the rank range in the
source's Lemmas 2.1–2.2.

If $|S|=1$, its sole vertex is a witness. If $S=X_i$, the empty flag is a
witness. When $|S|\geq2$, no witness contains a vertex of type $i$: such a
vertex would restrict its shadow to at most one point.

Define the **eligible set**

$$E(U,S)=\{v\in X\setminus X_i:
 v\sim u\ (u\in U),\quad v\sim s\ (s\in S)\}.$$

Every possible witness must lie in this set. Its members already impose all
the positive requirements. Only exclusion of unwanted shadow points remains.

**Theorem (exact covering criterion).** If $|S|\geq2$, a witness exists if
and only if there is a pairwise incident subset $C\subseteq E(U,S)$ such
that, for each $y\in X_i\setminus S$, some $v\in C$ is not incident to $y$.

**Proof.** A witness is incident to $U$ and to every member of its shadow,
so lies in $E$. A point outside its shadow must fail incidence with at
least one of its vertices. Conversely an eligible flag has shadow containing
$S$, while the exclusion condition removes every point outside $S$. Its
shadow is therefore exactly $S$, and it is incident to $U$. This proves
both directions, including the empty flag when there is nothing to exclude.

For each $v\in E$ introduce $z_v\in\{0,1\}$. The complete feasibility
system is

$$z_v+z_w\leq1\quad(v\ne w,\ v\not\sim w),$$
$$\sum_{v\in E:\,v\not\sim y}z_v\geq1
       \quad(y\in X_i\setminus S).$$

The first inequalities include pairs of distinct vertices of the same type.
There are no omitted flag constraints. A feasible assignment is an immediately
checkable positive certificate. A failed heuristic search is not a negative
certificate: rejection requires exhaustive search or a separately verifiable
infeasibility proof. The implementation here uses exact enumeration, with no
floating-point solver.

## 2. A closure test is necessary but insufficient

Ignoring flag compatibility gives the cheaper condition

$$\sigma_i(E(U,S))=S.$$

Failure proves that no witness exists. Equality does not prove that the
needed vertices form a flag. This is where a bare matrix intersection or a
Galois-closure calculation loses mathematical information.

Here is an explicit rank-three geometry. Let the type classes be
$A=\{0,1,2,3\}$, $B=\{b_0,b_1\}$ and $D=\{d_0,d_1\}$. Every $B$ vertex
is incident with every $D$ vertex. Set

$$N_A(b_0)=N_A(d_0)=\{0,1,2\},\qquad
  N_A(b_1)=N_A(d_1)=\{0,1,3\}.$$

Every flag extends to a chamber: each cross-type edge has a triangle
extension, as does every vertex. Take $x=b_0$ and $F=\{b_1\}$.
Then $S=\{0,1\}$ and $E=\{d_0,d_1\}$. Their common $A$-shadow is
exactly $S$, but they have the same type and cannot be selected together.
Neither singleton has the required shadow. Thus closure passes and the
actual shadow-IP test fails. No rank-two IP or residual regularity is
claimed for this example.

This obstruction explains why a uniform encoding must preserve types and
flag compatibility. It also gives a small regression example independent of
any sporadic-group catalogue.

## 3. Recover the rank-two criterion uniformly

The source uses the established rank-two characterization by partial linear
spaces and generalized digons. The covering argument gives a short direct
proof. Consider any nonempty bipartite incidence structure with both type
classes nonempty. Its shadow-IP holds for both types if and only if its
bipartite graph has no four-cycle, or is complete bipartite.

Indeed the only potentially nontrivial flag $F$ is a single vertex of the
same type as $x$, distinct from $x$. A witness of the other type has singleton
shadow. A witness of their own type cannot be incident to both distinct
vertices. The empty witness has the whole opposite type as shadow.
Consequently two distinct vertices on either side must have zero or one
common neighbor, or have the entire opposite side as common neighbors.

If there is a four-cycle, its two vertices on one side therefore meet every
vertex on the other side. Every pair on that other side now has at least
two common neighbors, so meets the entire first side. The graph is complete.
Conversely a graph without four-cycles has only singleton or empty proper
intersections, and a complete bipartite graph satisfies the condition
directly. No transitivity assumption is needed for this argument.

For rank-two geometries this is precisely the partial-linear/digon test.
The argument is a rederivation of a known ingredient, not a new classification.

## 4. The same engine handles all ranks and residues

For a residue of a flag $R$, restrict to vertices of types outside $t(R)$
incident to all of $R$. Apply exactly the same system to its induced
incidence relation. Thus no separate algebra is needed for IP, $(IP)_k$,
WIP or $(WIP)_k$; only the quantifiers over residues and types change.

If a group acts by type-preserving automorphisms, it acts on all the data
$U,S,E$ and on the covering inequalities. One representative of each orbit
of tests suffices. In the flag-transitive case a nonempty shadow supplies
an incident pair $(p,x)$ with $p\in X_i$. Normalize that pair first and
then quotient the possible $F$ by its stabilizer. This recovers the orbit
normalization in Section 3 of the 2004 paper, while keeping the witness
condition in a reusable finite constraint format. Without flag transitivity,
all pair orbits must be retained.

In relation-matrix language, shadows are entrywise products of incidence
columns. Eligibility is another family of such products. The final step is
the flag-constrained covering system above. Ordinary linear similarity, or
just multiplying the columns, cannot replace that final step.

## 5. Computation, historical data, and scope

[phase4_shadow_ip_check.py](phase4_shadow_ip_check.py) compares two independent
decision procedures: direct enumeration of all possible witness flags and
the eligible-set covering test. It exhausts small incidence structures and
checks deterministic larger examples, including induced residues. It also
independently compares the rank-two characterization with direct shadow-IP.
The resulting [JSON report](phase4_shadow_ip_check.json) records exact finite
scope and the closure counterexample. These are implementation checks; the
all-size statements above are written proofs.

The original supplementary archive was recovered from the publisher:
[Appendix B](https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S1461157000001133/resource/name/S1461157000001133sup002.tar).
It contains the maximal parabolic data for geometries of eight sporadic
groups. The archive is a source input, not executable code trusted by this
project. Its metadata and checksums are recorded; third-party contents are
not redistributed here. Reconstructing the original tables requires explicit
data conversion, group identification, flag-transitivity verification and
the full tests. The generic equivalence and small checks alone do not do that.

The contribution of this note is therefore a precise common formulation,
a proof of its completeness, an obstruction to dropping the flag condition,
and a rederivation of the rank-two boundary. It connects a 2004 geometric
algorithm with the modern marked-action framework without identifying it
with the different C-group intersection problem.
