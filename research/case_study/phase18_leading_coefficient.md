# The leading coefficient and the prevalence of class three

10 October 2026. Research draft consequence of the frozen bounded-core and
first-excess theorems. Root developed the maximal-pole count below;
the survey agent also proposed the shorter normal-component argument
in section 2. A separate review must identify its own scope. Earlier
proofs remain unchanged. Publication priority is unverified.

Fix k>=1. Let a_k(d) count all ordered marked nondegenerate string
C-group two-groups of rank d and order 2^(2d−1+k). Let c_k(d) count
those of nilpotency class at most three, as in the separate
[class-three classification](phase18_class_three.md).

**Theorem.** For fixed k and d tending to infinity,

    a_k(d) = (5^k/k!) d^k + O_k(d^(k−1)),                         (1)
    a_k(d) − c_k(d) = O_k(d^(k−1)).                              (2)

The first function is already known to be a polynomial for d>=6k−1.
The second is also eventually a polynomial of degree at most k−1.
Consequently c_k(d)/a_k(d) tends to one. This is a statement about
uniform choice among ordered marked isomorphism classes, not among
unmarked abstract groups, presentations, or individual group elements.
For k=1 the difference is identically zero in the stated rank range.

## 1. Extracting the coefficient from the exact core patterns

Retain the exact canonical-core bijection and pattern generating
function from [the central-join theorem](phase16_central_join.md),
section 5. A pattern has t<=k support intervals, records each internal
gap as 1, 2 or at least 3, and records each end gap as zero or positive.
Its contribution is

    m z^b/(1−z)^r,

where r is the number of long internal gaps plus positive end gaps.
It satisfies r<=t+1<=k+1. A degree-k term is possible only when
r=k+1. This forces t=k, both ends positive, and all k−1 internal
gaps at least three.

In precisely those patterns, the closed neighborhoods of the support
intervals are disjoint induced path components, with no edges between
them. Actual IP and their distant commutation relations identify the
marked core as their internal direct product. The normal kernel
decomposition in [the support theorem](phase16_fixed_excess.md),
section 3, assigns positive excesses k_j whose sum is k. Thus every
component has excess one. Its canonical support is either an edge
or a consecutive triple.

Because both external ends and all internal gaps supply at least one
neighbor on each side, each edge support has a four-marker canonical
core, with its support on the middle edge. The first-excess theorem
gives exactly four such marked cores, the two independent neighboring
beta choices. Each triple support has a five-marker canonical core,
with the support on the middle triple; there is exactly one such core.
These are all possibilities by the complete
[first-excess classification](phase17_k1_classification.md).

Conversely, any ordered choice of these component cores forms a direct
product with the required induced-forest marking and canonical kernel
support. The central-join theorem attaches it automatically and uniquely.
Thus the component choices really are independent; no multiplicity is
being inferred just from an upper bound on support size.

Summing all patterns with r=k+1 gives the following exact subseries of
the full rank generating function:

    D_k(z) = z^(3(k−1)+2) (4z^2+z^3)^k /(1−z)^(k+1)
           = z^(5k−1)(4+z)^k /(1−z)^(k+1).                      (3)

The prefactor records the minimum internal gaps and the two positive
end gaps; z^2 and z^3 record the support lengths. Every omitted pattern
has r<=k and therefore contributes eventual degree at most k−1.
The coefficient of d^k from (3) is its numerator at z=1 divided by
k!, namely 5^k/k!. This proves (1) without enumerating any larger
core library. The fixed-k leading coefficient is exact; no interpolation
or finite experiment supplies it.

## 2. Higher nilpotency class is a lower-degree contribution

The frozen support theorem decomposes K=gamma3(G) along its t support
intervals as a direct product of nontrivial subgroups K_j, each normal
in the whole G. Their orders are 2^(k_j), with k_j>=1 and sum k_j=k.
If t=k, all K_j have order two. Every normal subgroup of order two is
central, so their product K is central in G. Hence gamma4(G)=1 and
G has class at most three.

Therefore every group of class at least four has t<=k−1. Restrict the
finite pattern/core library to those groups. A fixed core determines
whether the attached group has class at most three: the central join
has gamma3(G)=gamma3(H), and outside generators centralize this kernel.
Thus centrality in H and in G are equivalent. The restriction depends
only on the bounded core, not on the lengths of its long gaps.

The same exact generating function now has r<=t+1<=k for every term.
Its coefficients are eventually polynomial of degree at most k−1.
They count exactly a_k(d)−c_k(d), proving (2). Dividing by (1) gives
the stated limiting proportion and an O_k(1/d) upper bound for the
proportion of higher-class markings. This assertion does not require
an explicit classification of their cores.

## 3. Description cost and limits

For fixed k,

    log2 a_k(d) = k log2 d + k log2 5 − log2(k!) + O_k(1/d).      (4)

This refines the previous O_k(1) description bound. Conditional on d,
k and an agreed enumeration/decoder, a fixed-length class index needs
ceil(log2 a_k(d)) bits. The rank, excess, decoder, proof and certificates
are additional costs when they are not already shared. Formula (4)
does not measure the length of a source proof or assert efficient
enumeration of the finite library.

The exact lower coefficients for unrestricted k>=2 remain uncomputed
here. The class-three transfer matrix computes them in that subclass;
it cannot substitute for class-four and higher cores. No whole-paper
credit, current-priority certification, infinity marker or new Lean
formalization follows just from this asymptotic theorem.
