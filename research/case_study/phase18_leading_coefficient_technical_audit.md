# Technical audit of the leading coefficient

10 October 2026. Written review of
[phase18_leading_coefficient.md](phase18_leading_coefficient.md).
The accompanying JSON binds the exact proof bytes. Earlier frozen
sources and proofs were not changed.

**Review-role disclosure:** this reviewer co-developed the normal-component
argument in §2 of the reviewed note. This is an additional technical check,
not a wholly independent review. The maximal-pole and local multiplicity
argument in §1 was checked independently. A separate reviewer provides
the independent whole-proof audit.

**Verdict: PASS under the retained exact core-pattern theorem and
the first-excess classification.** For each fixed positive excess k,
the unrestricted ordered-marking count has leading term
5^k d^k/k!, and the higher-than-class-three contribution has degree
at most k−1. The limiting proportion is about ordered marked
isomorphism classes, as explicitly stated in the proof.

I reread the two required frozen structural inputs. The support
theorem decomposes γ3(G) into nontrivial support-component factors
K_j, each normal in the whole group, with orders 2^(k_j) and
Σk_j=k. The central-join theorem gives an exact canonical bijection
and finite pattern contribution m z^b/(1−z)^r, where r is the
number of long internal gaps plus nonzero end gaps. It is an exact
count with r≤t+1 for t kernel-support components, rather than only
an upper bound or a count of presentations.

## Maximal-degree patterns and their multiplicities

A degree-k contribution requires r=k+1. Thus t=k, both ends are
positive, and every internal gap has length at least three. If two
support intervals have exactly three omitted vertices between them,
their closed neighborhoods still have a vertex between them.
Consequently they have no common vertex or connecting edge. Larger
gaps preserve this property. The induced core is therefore a union
of separate paths.

The associated marked subgroups commute, and actual IP makes their
intersections trivial. Their generated core is their internal direct
product. Each has excess one because the k positive component
excesses sum to k. The phase-seventeen classification then gives
exactly the stated local possibilities: an edge support with two
available neighboring triple coefficients, hence four cores, or an
intrinsic triple support with one core. Positive end gaps ensure
that neither component loses a neighboring marker at the ambient
boundary. This explains why the interior counts four and one apply
uniformly to every component in these particular patterns.

Conversely, their direct product is an admissible marked forest
core, and the central-join theorem supplies the unique attachment.
The independence of the local choices follows from this direct
product and reconstruction, not from a multiplication of unrelated
local upper bounds. An ordered list of component supports and its
gap lengths recovers its canonical support J. Distinct core choices
remain distinct after extraction, so no quotient by component
permutations, reversal, or group automorphisms is needed.

The minimum rank is the sum of support lengths, plus 3(k−1) for
the internal gaps and two for the positive ends. Each support has
weight 4z²+z³. Every gap beyond its minimum adds one freely chosen
nonnegative integer. Thus the exact maximal-pole subseries is

    z^(3(k−1)+2)(4z²+z³)^k/(1−z)^(k+1)
      = z^(5k−1)(4+z)^k/(1−z)^(k+1).

Its coefficient of d^k is the numerator evaluated at one, divided
by k!, namely 5^k/k!. All omitted patterns have poles of order at
most k and therefore lower eventual degree. Finite-rank correction
terms do not affect this conclusion. As a boundary check, k=1
gives the interior subcount 5d−16 at sufficiently large rank; the
six omitted boundary markings recover the known total 5d−10.

## Why higher class has lower degree

If t=k, every normal factor K_j has order two and hence is central
in G. Their product γ3(G) is central, so γ4(G)=1. The contrapositive
therefore gives t≤k−1 whenever G has class at least four. The
normality in the whole group is crucial; normality only inside an
individual component would not suffice. It is explicitly proved
in the frozen support theorem and used correctly here.

Filtering the finite core library by this property is legitimate.
Attachment preserves γ3(H), and all outside-core generators
centralize it. Thus its centrality in H is equivalent to centrality
in the attached G, independently of how far the long gaps are
extended. The filtered exact generating series has r≤t+1≤k for
each term. It follows that the higher-class count is eventually a
polynomial of degree at most k−1. There is no assumption here that
those cores have already been explicitly classified.

Dividing by the positive leading term gives proportion 1−O_k(1/d)
for class at most three. At k=1 there is no higher-class contribution
at any admissible rank, since the full γ3 itself has order two.
The logarithmic expansion and its fixed-length-index interpretation
follow from the positive leading coefficient; the ceiling cost is
kept distinct from the expansion for log2 of the count. The note
also correctly charges the decoder, rank, excess, proof and
certificates separately when they are not shared.

This is a written consequence of the stated structural theorems.
No finite extrapolation, new finite-group census, Lean execution,
unmarked enumeration, efficient-decoding assertion or priority
finding is part of this audit.
