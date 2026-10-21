# TransvectionForms: exact certificate scope

This certificate proves that a matrix fixed by all elementary-transvection
congruences is zero in dimension at least three. It uses actual matrix
products and transposes, over an arbitrary ring. It assumes neither
symmetry of the matrix nor odd characteristic.

For an elementary matrix $E_{ij}$, suppose

$$ (I+E_{ij})^{\mathsf T}B(I+E_{ij})=B. $$

If $b\ne j$, its $(j,b)$ entry gives
$B_{jb}+B_{ib}=B_{jb}$, hence $B_{ib}=0$. To kill an arbitrary entry,
choose $j$ distinct from $i$ and $b$, and apply the corresponding
transvection. The general theorem takes this third-index condition as an
explicit hypothesis. The final theorem instantiates it for `Fin 4`.

The three lemmas in [TransvectionForms.lean](TransvectionForms.lean) prove
the entry calculation, the arbitrary-index vanishing theorem and its
four-dimensional instance. Lean reports only `propext`, `Classical.choice`
and `Quot.sound`; there are no admitted lemmas.

This simplifies the exact-invariance step in the
[linear/unitary application](../phase9_linear_unitary.md), §4: isolating an
entry directly avoids subtracting the two transvection equations. The
earlier written odd-characteristic argument remains valid and is preserved
with its original review hashes.

The reduction from projective similarities to exact transvection invariance
is still written mathematics: in characteristic $p$, a nonzero form's
multiplier for an element of order $p$ must be a $p$-th root of unity, hence
one. This certificate does not formalize that step, group simplicity,
the unitary torus argument, the inherited representation classification,
or the full rank bound. Its characteristic-free entry lemma does not
extend that odd-characteristic rank theorem to characteristic two.

The [saved report](TransvectionForms.check.json) comes from a fresh public
source compilation with the pinned dependency environment. It records
which compiler, sources and dependencies were checked; it does not claim
an independent rebuild of mathlib's compiled cache.
