# Universal regular objects when two or three divides the parameter

Date:2026-10-10. Corollary combining the frozen even and multiples-of-three
constructions. No change is made to their original statements.

Let $U_s$ and $P_s$ be the exact full and rotational presentations defined
in [the universal-even note](phase33_L003_universal_even.md). For every
integer $s\ge2$ divisible by two or three, $U_s$ is the full type-preserving
automorphism group of a regular rank-four hypertope with ordered residues
$((3,0),(2,0),(1,1),(s,0))$. It is universal among marked regular objects
with this diagram and these ordered marked residues, and

$$U_s\cong P_s\rtimes C_2.$$

For even $s$, this is the previously frozen corollary. For $s=3m$, use the
finite group supplied by [the multiples-of-three construction](phase34_L003_triple_family.md).
The defining words give an epimorphism from $U_s$ to this group. Each
universal maximal parabolic is a quotient of the standard finite local
toroidal group with order36,12s²,48 or108. Its finite image attains that
order, so every maximal parabolic injects. The original all-maximal
quotient theorem lifts full IP and typed Helly. Their chamber argument
proves the regular hypertope and exact residues. Every other marked
regular object satisfies the same defining relations; its quotient map
is an isomorphism on each finite local group. This proves the specified
universality.

The rotation identification in the earlier note's section3 requires only
that the four local parameters have form(a,0) or(a,a). Its lattice and
normal-closure argument is independent of the parity of s. It therefore
applies verbatim here: reflection invariance makes the even normal closure
stable, and the surviving sign with its distinguished involution gives
the stated semidirect product. No extra rotational relators are imposed.

Whenever6 divides s, the epimorphism $U_s\to U_6$ proves infinitude as
before. No further universal finiteness or infinitude assertion is made
here. The two finite families can give different quotients at a shared
parameter; their groups are not identified with each other or with $U_s$.
Uniform existence for parameters coprime to6 and current priority remain
unverified. This is a written corollary using the separately certified
finite constructions, not a new finite computation or complete Lean proof.
