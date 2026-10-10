# Second independent review of the nilpotent abelian-Frattini theorem

10 October 2026. Internal review by the rank-stability agent, separate from
the author of the odd-prime extension. **PASS: no mathematical gap found.**

I read phase11_nilpotent_frattini.md in full. The induction is within the
subgroup- and quotient-closed class of finite p-groups with abelian Frattini
subgroup. Central quotient absorption preserves TPP and its ratio; the
proper-pair reduction uses only a coset injection. The maximal-subgroup
restriction forces ratio p, and the disjoint cyclic conjugates give minimum
factor order at least p². Actual abelianness, not numerical equality, then
gives Φ(P)=A^p×B^p×C^p with three nontrivial cyclic factors.

The right-conjugation norm identities have the stated signs. On the
three-dimensional quotient, the norm equals (S−I)^(p−1). For p≥5 this
vanishes by dimension. For p=3, a regular nilpotent block N would force
its commuting unipotent T to have form I+αN+βN². Fixing y independently
of ker N=<x> forces α=0, so (T−I)²=0, and the norm identity then forces
Ny=0, a contradiction. Interchanging the actions deals with the other
norm. This covers both nontrivial and identity actions without an unstated
semisimplicity assumption.

Both x and y are fixed modulo pΦ(P). If either corresponds to a cyclic
factor of maximal order, its order-p element lifts to a fixed element. If
neither does, z is strictly longer than both and all correction terms die
at the maximal power. The resulting element is nonidentity and centralizes
a,b, contradicting the initial center-free reduction. Finally finite
nilpotent groups, their Frattini subgroups, and the cyclic factors split
into Sylow components, where TPP restricts; multiplication proves the
stated nilpotent theorem.

The binary theorem is a retained companion result; its own independent
review and diagnostics are separately recorded. This review adds no claim
of a complete Lean formalization, external peer review, or publication
priority. It is a written mathematical review; no odd-prime computation is
claimed by this reviewer. The unrestricted cyclic-TPP problem remains open.
