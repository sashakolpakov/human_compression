# Flag relations and triangle geometries

The complete corrected principal results of Delaby–Leemans–Tranchida,
*Geometries with trialities arising from linear spaces* (2026), now follow
from a five-page common theory and an eight-page application, together
with the explicitly retained classifications and geometric proofs.

| Paper | Complete text | Role |
|---|---|---|
| Flag relations and reconstruction | [PDF](research/case_study/phase265_flag_relations.pdf); [source](research/case_study/phase265_flag_relations.md) | Literal incidence relation, reconstruction, correlations, residues, determinant torsors and the projective-line normalizer |
| Triangle geometries of finite linear spaces | [PDF](research/case_study/phase265_triangle_application.pdf); [source](research/case_study/phase265_triangle_application.md) | Corrected full action classification, geometric classification, every principal diagram and corrected Table 1 |

For flags (p,L) and (q,M), the directed relation is p ∈ M and q ∉ L.
Its matrix is (A−I)(B−I), where A and B record equality of points and lines.
Common-neighbor counts recover the original point fibers. This turns a
triangle-geometry automorphism into an automorphism of the original linear
space. The same relation gives an explicit description of every residue.

The other reusable ingredient is a torsor of invertible matrices of fixed
determinant. Semilinear transitivity reduces to the induced action on
determinants, provided the group contains SL. This replaces a false
GL-containment necessity in the source and yields an explicit counterexample
over F9. The application also states the source's circle, affine-group,
correlation and morphism qualifications precisely.

The [independent review](research/case_study/phase271_review.md) covers the
entire declared contract. The [44 source dispositions](research/case_study/phase265_source_ledger.json)
and [dependency graph](research/case_study/phase265_dependency_dag.json)
separate reconstructed arguments, source corrections and retained inputs.
The Buekenhout–Dehaye–Leemans classification, classical automorphism and
three-transitive group results, and the [Hermitian-unital proof](HERMITIAN_UNITALS.md)
remain credited dependencies. They do not become new results by being reused.

Four [Lean proofs](research/case_study/formal/DeterminantFibers.lean) verify
actual determinant transport, semilinear matrices and subgroup orbits.
The full incidence classifications remain written. Independent finite
checks include 540,910 signature pairs, all UH(4) residue distances, a
separate A7 construction and circles on three through six points.

```sh
python3 -B -O research/case_study/phase272_check.py \
  --out /tmp/NEW-triangle-review \
  --gap GAP --lean LEAN --packages PACKAGES
```

This recovers one principal source contract. It excludes auxiliary square
and Desargues examples and an external hypermap identifier. The separate
[point-cloning answer](POINT_CLONING.md) remains in the question catalogue.
The thirteen new pages alone are not the full cost: required programs,
retained proofs and the full common theory must be charged. No matched
compression ratio has yet been measured for this topic.

See the [admission record](provenance/phase134_review.md) and
[root review](research/case_study/phase272_root_review.md).
