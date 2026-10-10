# Infinitely many minimal covers from one surface construction

Every polytope in the four specified two-primary families has infinitely
many pairwise nonisomorphic finite minimal regular polytopal covers.
This strengthens the earlier result giving two minimal covers. It holds
for every source parameter and every independent choice of signs.

The complete [manuscript](research/case_study/phase211_surface_covers.md)
and [independent review](research/case_study/phase218_surface_cover_review.md)
give the proof. The [general theorem](MINIMAL_REGULAR_COVERS.md) now
answers the unrestricted minimal-cover question. This surface construction
retains the stronger conclusion of infinitely many finite covers for its
four families.

## The uniform construction

The earlier family proof supplies a common marked quotient D of order 256.
Its Cayley graph, with disks attached along three commuting pairs and the
middle pair, forms a closed orientable surface X. Its Euler characteristic
is −32. Three explicit unions of marked subcomplexes have connected
complements in X.

For every prime ℓ, take the cover associated with the kernel of
π₁(X) → H₁(X; Fℓ). Mayer–Vietoris and the complement calculation prove the
three subgroup intersections needed for the intersection property. This
produces a regular polytope group over D with kernel $\mathbb F_\ell^{34}$. The proof works
uniformly in ℓ; the finite certificates verify its surface hypotheses.

A coprime pullback argument transports the construction to every member
of the four families for every odd prime ℓ. If the source type is {p,q,r},
the constructed cover has type {ℓp,q,ℓr}, degree ℓ³⁴ over the monodromy
group, end kernels of dimension nine, and trivial middle kernel.

Finite descent gives a minimal regular polytopal quotient of degree ℓᵉ,
where 1 ≤ e ≤ 34. The degree is nontrivial because the monodromy group
is not a string C-group. Distinct primes give distinct orders, hence
infinitely many nonisomorphic minimal covers. The construction does not
specify these minimal quotients or their individual exponents.

## Source families and attribution

In every row, β ≥ 5 and both source signs vary independently. Degrees
are measured over the smallest regular maniplex cover.

| Family | Source type | Result for every odd prime ℓ |
|---|---|---|
| Γ₂ | {8, 2ᵝ, 8} | A minimal regular polytopal cover of degree ℓᵉ, 1 ≤ e ≤ 34 |
| Γ₃ | {2ᵝ⁻¹, 2ᵝ, 2ᵝ⁻¹} | Same |
| Γ₄ | {8, 2ᵝ, 2ᵝ⁻¹} | Same |
| Dual Γ₄ | {2ᵝ⁻¹, 2ᵝ, 8} | Same; reverse the marking |

The odd-prime family Γ₁ retains its earlier two-cover result; no
infinite-family extension for Γ₁ is asserted. The
[five-family page](COVER_FIVE_FAMILIES.md) records both scopes together.

**[B] Borrowed:** Cunningham–Pellicer's source families, presentations,
orders and chirality; the standard group–polytope correspondence;
cellular homology and Mayer–Vietoris. The earlier reviewed construction
supplies the common quotient and its maps for all parameters.

**[I] Contribution here:** the surface criterion, its use to obtain covers
for every odd prime, and the resulting infinite multiplicity in the four
families. The general construction also applies to a nonorientable
surface when each relevant complementary component is nonorientable.
Its Tomotope application gives another construction of a result already
proved by Monson–Pellicer–Williams; it is not a newly solved question.

**[V] Verification:** independent Python and GAP calculations establish
the literal cells, complement components, orientations and boundary
cycles. The reviewer reconstructs all 192 Tomotope flags from the primary
incidence data. The [publication record](provenance/phase116_review.md)
records the fresh public execution and rejection controls.

**[L] Lean:** six general theorems in
[CoverKernelChains.lean](research/case_study/formal/CoverKernelChains.lean)
prove closure under directed unions and chains, existence of maximal
admissible kernels, uniqueness implying a greatest kernel, and two
coprime-power statements. The surface topology and complete family
theorem remain written proofs.

The unrestricted question is Cunningham–Pellicer's Problem 5 in
*Open problems on k-orbit polytopes*, also discussed in Cunningham's
*Chiral polytopes whose smallest regular cover is a polytope*, §4.
The F005 mix criteria are related inputs, rather than another source of
that exact conjecture. Neither historical priority nor a numerical
compression factor is established by this extension.

## Reproduction

Use a new output directory:

```sh
python3 -B -O research/case_study/phase218_check.py --out /tmp/NEW-surface-covers --gap GAP --lean LEAN --packages PACKAGES
```

This runs both implementations, six Lean declarations and six controls:
three independent GAP mutations, two author finite controls, and one
Lean hypothesis mutation. The recorded environment uses GAP 4.15.1,
Lean 4.32.2 and the pinned mathlib revision. See the
[formal scope](research/case_study/formal/CoverKernelChains.scope.md).
