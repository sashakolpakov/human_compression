# Finite minimal covers of square-torus pyramids

For every odd integer $n\ge3$, the pyramid over the regular square torus
$\{4,4\}_{(n,0)}$ has infinitely many pairwise nonisomorphic **finite minimal
regular polytopal covers**. The [complete proof](research/case_study/phase239_odd_toroidal_pyramids.md)
and [independent mathematical review](research/case_study/phase242_review.md)
are published with executable certificates.

More precisely, let $G_n$ be the marked monodromy group of that pyramid.
For every $n\ge3$ and every prime $\ell\nmid2n$, the construction gives

$$1\longrightarrow (\mathbb F_\ell)^{642}\longrightarrow H_{n,\ell}
\longrightarrow G_n\longrightarrow1,$$

where $H_{n,\ell}$ is a finite string C-group with the required marking.
When $n$ is odd, a minimal regular quotient of this cover has degree
$\ell^e$ over $G_n$, with $1\le e\le642$. Distinct primes give distinct
orders, hence nonisomorphic minimal covers. The proof does not determine
the individual minimal quotients or their exponents.

## One fixed calculation for all parameters

The torus flags have affine coordinates in
$(\mathbb Z/n\mathbb Z)^2\rtimes D_8$. The pyramid adds five layers.
Forgetting translations gives a fixed group $E$ of order 61,440, followed
by a fixed marked quotient $D$ of order 3,840:

$$G_n\longrightarrow E\longrightarrow D.$$

The key argument proves that the first map is injective on the common
intersection of the two end parabolics. Their translation kernels have
disjoint supports. On the three middle layers, the same affine map fixes
both a vertex and a face center; this restricts its orientation to the
identity or coordinate swap. A single exact subgroup calculation in $E$
then proves the required kernel intersection condition for **every** $n$.
The finite checks at $n=3,5$ test the flag conventions; they do not supply
the universal quantifier.

The quotient $D$ defines an orientable surface of genus 321. Its first
homology has dimension 642 over every prime field. The previously proved
surface theorem constructs covers of $D$ with this homology kernel.
Coprime pullbacks lift them to $G_n$, preserving every required parabolic
intersection. Finite descent and the known failure of the C-property for
odd $n$ give the infinitely many minimal covers.

## Attribution and scope

**[B] Earlier results used.** Cunningham, Pellicer and Williams,
[*Stratified operations on maniplexes*](https://alco.centre-mersenne.org/item/10.5802/alco.208.pdf)
(2022), supply the pyramid action and transfer through the marked smallest
reflexible cover of the base. Their Theorem 4.3 records the earlier
Pellicer–Williams classification of the exceptional odd square tori.
Monson and Schulte,
[*Finite Polytopes have Finite Regular Covers*](https://arxiv.org/abs/1209.1167),
already prove finite-cover existence in general. These results are cited
inputs. The surface and coprime pullback theorems are reused from the
project's earlier proofs.

**[I] Contribution here.** The uniform affine kernel argument reduces the
whole parameter family to one orientation group calculation. Together
with the reused surface theorem, it supplies the stated controlled
prime-power kernels and infinite multiplicity of finite minimal covers.
This identifies what is added to the cited inputs; historical priority has
not been established by a comprehensive literature search.

The same conclusion transfers to any finite base polyhedron whose
**marked** smallest reflexible cover is the specified square torus.
This hypothesis is an input, not a new classification of such bases.
The earlier [single-parameter proof](research/case_study/phase224_pyramid_covers.md)
is the case $n=3$ and is not counted again.

The [general minimal-cover theorem](MINIMAL_REGULAR_COVERS.md) allows
infinite covers. The stronger question of multiple **finite** minimal
covers for every finite polytope with non-C monodromy remains unresolved
in this repository. This family theorem adds neither a new question entry
nor a complete historical-paper replacement or measured compression ratio.

## Verification

Fresh [public replay](research/case_study/phase247_public_replay/report.json)
passes both author programs, an independently implemented GAP orientation
calculation and an independent Python surface construction. The checks
include actual subgroup equalities, surface links and orientations,
connected complements, and deliberately invalid inputs.

Lean verifies **four new and nine retained declarations**. They cover
support, congruence, restricted injectivity, intersection transport and
algebraic cover arguments. The affine geometry, surface topology, finite
GAP computations and complete theorem are not formalized in Lean. The
[formal scope](research/case_study/formal/PyramidKernelTransport.scope.md)
and [publication review](provenance/phase124_review.md) state the boundary.

From the repository root, with a fresh output directory and local paths
for the pinned tools:

```sh
python3 -B -O research/case_study/phase242_check.py \
  --out /tmp/NEW-pyramid-check \
  --gap GAP --lean LEAN_4_32_2 --packages PINNED_PACKAGES
```
