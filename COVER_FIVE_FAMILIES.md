# Minimal covers throughout the five specified families

The reviewed proofs establish the multiplicity assertion for all five
families in the checked author version of Cunningham's cover proposal.
Each member has at least two distinct minimal regular polytopal covers.
The new [surface construction](INFINITE_MINIMAL_COVERS.md) proves
**infinitely many** in the four two-primary families, for every source
parameter and both independent signs.
**Historical priority and current openness remain unverified.** The
general conjecture for arbitrary polytopes is unresolved here.

The [root admission](research/case_study/phase119_five_family_root_admission.md)
combines the [uniform construction](research/case_study/phase109_cover_families_generalization_theorem.md),
its [independent mathematical review](research/case_study/phase112_cover_families_review_audit.md),
the earlier [odd-prime theorem](COVER_FAMILY.md), and the
[independent five-row scope audit](research/case_study/phase118_five_family_scope_review.md).

| Source family | Type | Complete parameter range | Distinct minimal covering degrees over the smallest regular maniplex |
|---|---|---|---|
| Gamma1 | {2m,m^alpha,2m} | m odd prime, alpha >= 2, equal end parameter 1 <= k < m | m and m, distinguished by kernel actions |
| Gamma2 | {8,2^beta,8} | beta >= 5; both independent signs | For every odd prime ell, a degree ell^e with 1 <= e <= 34; infinitely many minimal covers |
| Gamma3 | {2^(beta-1),2^beta,2^(beta-1)} | Same | Same |
| Gamma4 | {8,2^beta,2^(beta-1)} | Same | Same |
| Dual Gamma4 | {2^(beta-1),2^beta,8} | Same; duality exchanges signs | Same |

These are five ordered-type rows, four families up to rank reversal.
The scope audit checks their literal marked presentations and source
parameters. They are not all eleven atomic families or all tight chiral
polytopes. The checked editions and uncollated publisher versions remain
explicit in the [source report](research/case_study/phase113_five_family_priority_report.md).

## Earlier construction over two fields

Every two-primary source group maps onto the same marked group D of
order 256. The quotient preserves the offending intersection outside
the medial subgroup. Over each of F3 and F5, a permutation module on
two coset spaces produces an affine extension. Quotienting the orbit
span of the medial relation leaves a translation kernel of dimension 34.
Exact linear algebra verifies every required subgroup intersection.

A general coprime pullback theorem then transports the fixed construction
to every parameter and sign. It establishes generation of each full
parabolic pullback, not just the existence of a homomorphism. The two
resulting regular covers have degrees 3^34 and 5^34, types {3p,q,3r}
and {5p,q,5r}, end kernels of dimensions nine and injective medial maps.

Finite descent gives minimal quotients of positive 3-power and 5-power
degree. The different degrees prove distinctness. Their exact exponents
and quotient kernels are not selected; the large constructed covers
are not themselves proved minimal. Coprime indices also establish the
family-specific join equality for finite admissible universal kernels.

The independent checker uses different coset representatives, dense
coefficient vectors and pivot order. It checks all 16 parabolics and
all 136 unordered subset pairs in each field, 272 pairs in total.
Fresh public author and independent replays pass, together with changed
input and occupied-output controls. Computation treats the fixed finite
model; the written proof supplies transport to unbounded parameters.

## Attribution and reproduction

Cunningham–Pellicer's source constructions, exact orders, tightness,
chirality and intersection property remain inputs. Standard mix,
covering and geometric recognition theorems remain credited. The
repository supplies the particular common quotient, affine witnesses,
complete intersection certificates and uniform transport argument.
The [new proof](INFINITE_MINIMAL_COVERS.md) replaces the two selected
fields by a surface argument valid for every odd prime, retaining the
common quotient and its maps. It includes six general Lean theorems;
the surface argument and complete family result remain written proofs.
The bounded later-literature comparison leaves material unread sources.
This result therefore receives no newly solved open-conjecture marker.

From the repository root, use fresh output directories:

```sh
python3 -B -O research/case_study/phase109_cover_families_generalization_check.py \
  --expected-certificate research/case_study/phase109_cover_families_generalization_certificate.json \
  --output-dir /tmp/human-compression-five-author
python3 -B -O research/case_study/phase112_cover_families_review_check.py \
  --output-dir /tmp/human-compression-five-independent
python3 -B -O research/case_study/phase112_cover_families_review_controls.py \
  --output-dir /tmp/human-compression-five-controls
```

These commands reproduce the earlier two-field construction using
Python and public files only. The new surface proof has its
[own replay](INFINITE_MINIMAL_COVERS.md#reproduction). Neither result
adds a manuscript to the compression assembly or a length factor.
