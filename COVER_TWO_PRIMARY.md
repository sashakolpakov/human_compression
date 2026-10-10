# Two-primary covers and an integral obstruction

For one specified infinite family, the facet and cofacet construction routes
produce **the same minimal double cover**. A second theorem excludes covers
with **odd abelian kernel and injective maps on both ends**. These results
restrict the search for further minimal covers; global uniqueness remains
unproved.

The input is Cunningham–Pellicer, [*Tight chiral polytopes*, author
version](https://arxiv.org/pdf/2009.04566v1), Table 2 row Γ2 and Theorem 4.8:
`β≥5`, `q=2^β`, with two independent signs. Its marked type is `{8,q,8}`.
The exact presentation, existence, tight normal form, orders and intersection
property are retained source results. The theorems here concern that
presentation, rather than every polytope with this type.

## What the two constructions give

The [complete proof](research/case_study/phase58_2primary_cover_theorem.md)
and [independent mathematical review](research/case_study/phase73_2primary_cover_recent_audit.md)
establish the following for every parameter and both signs independently.
All orders in this table are **rotation-group orders**.

| Object | Order | Result |
|---|---:|---|
| Retained source P | `64q` | Tight chiral polytope |
| Smallest regular maniplex R | `128q` | Fails the top intersection property |
| Facet and cofacet mixes Qf,Qv | `512q` each | Polytopal; cyclic-four kernels over R |
| Their reduced cover S | `256q` | Both reductions are the same marked cover; degree two over R |
| Shared raw mix H | `1024q` | Polytopal; kernel `C4×C2` over R |

The prime degree and nonpolytopality of R prove that S is globally minimal
over P. The two reductions coincide by an exact presentation, rather than
just having equal orders. In the kernel of H, every proper invariant subgroup
lies inside the even-coordinate subgroup `C2²`. That subgroup is the unique
maximal admissible kernel, so S is the unique minimal cover **among quotients
of H**. Covers outside this interval are not classified.

A separate complete finite computation treats only `β=5`, signs `(+,+)`.
Here the **full** group of R has order 8,192. There is one marked double cover
and 29 marked degree-four covers: 16 with cyclic kernel, two with central
`V4` kernel, and eleven with noncentral `V4` kernel. Every degree-four cover
has a proper polytopal double quotient. Written finite class bounds make
the extension search exhaustive in this degree scope. Eight parameter
cross-checks do not enlarge that census to all β.

## A cover question becomes one integer identity

The [second manuscript](research/case_study/phase66_coprime_cover_theorem.md)
and [independent review](research/case_study/phase74_coprime_cover_recent_audit.md)
give a general affine construction and its converse. For a finite marked
2-group G with regular ends A,B, write `C=⟨r1,r2⟩`. Assume their intersection
is `C⟨z⟩`, with index two over C and z centralizing C.

An odd abelian cover with injective ends exists exactly when an odd finite
abelian G-module has a vector w satisfying

```text
w r1 = w r2 = w,
w(1−r3)(1−r0) = 0,
w(z−1) ≠ 0.
```

The proof uses explicit averaging to split the extension and align its
local complements. These are standard affine and averaging ideas, with
their required hypotheses proved in the manuscript.

Use the integral permutation module `Z[C\G]`, and set
`y=e_C(1−r3)(1−r0)`, `d=e_C(z−1)`. Every possible w defines a module map
from this one module. An identity `2^a d ∈ ⟨y·g : g∈G⟩_Z` therefore rules
out every such odd abelian cover. Over an odd finite field, the nonvanishing
of d in the corresponding quotient module is also sufficient to construct
a cover. This is an exact linear criterion, with the stated geometric inputs.

For the Γ2 family, the proof identifies one common marked quotient of order
1,024 and one common action on 128 cosets, valid for all β and signs.
The [55-term certificate](research/case_study/phase66_coprime_cover_coefficients.json)
then gives the literal integer identity

```text
2d = Σ nᵤ (y·u).
```

An independent sparse integer checker verifies every coordinate. This fixed
certificate and the written quotient reduction prove the all-parameter
obstruction. Finite-field samples or a rational rank calculation alone would
not give the same conclusion.

## Attribution, reproduction and remaining scope

The source-family construction and standard group-to-polytope recognition
remain imported. The mix with trivial end extensions comes from Cunningham's
earlier cover example. The repository derives the uniform coincidence,
restricted interval, finite census and integral obstruction. Historical
priority has not been established.

Run the public verifier with stock GAP 4.15.1 and a new output directory:

```sh
python3 research/case_study/phase80_two_primary_verify.py \
  --output-dir /tmp/human-compression-two-primary-new
```

It checks the exact model and 55 terms, runs all three complete GAP programs,
and compares both complete logs with the reviewed originals. The
[root admission](research/case_study/phase80_two_primary_root_audit.md)
records the fresh public replay. The historical author wrappers additionally
require private source captures; the public verifier requires only distributed
files. An [independent interface review](research/case_study/phase81_two_primary_interfaces.md)
repeats the run from only those files under optimized Python and checks
altered-input and overwrite rejection. These packages introduce no new Lean component or measured length
factor, and add no manuscript to Compress_11.

Nonabelian odd kernels, noninjective ends, mixed kernels, new even-kernel
covers, the other source families and unrestricted multiplicity remain
outside these conclusions. The [odd-prime theorem](COVER_FAMILY.md) and
[general cover-kernel criteria](COVER_KERNELS.md) retain their separate scopes.
