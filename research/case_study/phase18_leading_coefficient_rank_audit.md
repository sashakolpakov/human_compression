# Independent review of the fixed-excess leading coefficient

10 October 2026. Written mathematical review by the classification-track
agent, independent of the root author. The accompanying JSON binds the
exact reviewed proof and retained dependencies. No earlier frozen file
was edited.

**PASS, conditional on the explicitly retained canonical-core, support,
and first-excess classification theorems.** The argument proves the
leading coefficient for every fixed excess, and the asymptotic prevalence
of class at most three, in the ordered marked category only.

I checked the exact pattern count, including its boundary conventions.
A pole of order k+1 requires k support intervals, positive end gaps,
and every internal gap at least three. The closed neighborhoods of
successive intervals then have no joining edge. Their distant marked
generators commute, and actual IP makes their intersection trivial.
The core is therefore an actual internal direct product, not merely a
product of group orders.

The normal component kernels have positive excesses adding to k.
With k components each has excess one. The fully internal first-excess
cores have four choices when the support is an edge, and one when it
is a triple. Their attachment is automatic by the retained central-join
theorem, so these choices really are independent. The minimum gaps
contribute z^(3(k-1)+2), and the supports contribute (4z^2+z^3)^k.
Thus the exact maximal-pole subseries is

    z^(5k-1)(4+z)^k/(1-z)^(k+1).

Its numerator at z=1 is 5^k, yielding leading coefficient 5^k/k!.
Every other pattern has pole order at most k, including finite-support
terms with no variable gap. This is an exact finite-library argument,
not a fit to any computed sequence.

For the higher-class restriction, each order-two normal component
kernel is central in the whole group. Consequently a marking with k
support components has central gamma3, and all higher-class markings
have at most k-1 components. Whether the kernel is central is a property
of the core alone: outside generators centralize it in the central join.
Restricting the bounded library is therefore legitimate and does not
introduce a dependence on free gap lengths. Its rank-count coefficients
are eventually polynomial of degree at most k-1. This proves the claimed
difference bound and limiting proportion.

The logarithmic expansion follows from the positive leading term with
a relative O_k(1/d) error. The proof correctly separates a conditional
class index from the cost of its decoder, rank, excess, mathematical
proof and certificates. It asserts neither efficient core enumeration
nor a measured proof-compression ratio.

This review does not execute a finite checker, prove the retained
canonical-core theorem anew, determine publication priority, classify
unmarked abstract groups, or formalize the result in Lean. The exact
lower coefficients outside class three remain unresolved by this note.
