# Exact scope of OddKernelWord

The [source](OddKernelWord.lean) proves two declarations in namespace
`MathCompression.OddKernelWord`:

* `defect_square`: for an arbitrary group K and function t:ℕ→K, the
  35 literal cell equations imply `((t 1)⁻¹ * t 40)^2 = 1`.
* `defect_trivial_of_odd_card`: with finite K and odd cardinality,
  those same equations imply `t 1 = t 40`.

All 34 intermediate eliminations and the final conjugation are checked by
Lean. Membership of each used cell in the literal hypothesis list uses
kernel evaluation. The first axiom report contains `propext` and
`Quot.sound`; the second additionally contains `Classical.choice`.
There is no native-evaluation axiom or proof placeholder.

The [independent review](../phase86_nonabelian_cover_recent_audit.md) and
its separate implementations check that all 35 cells belong to the actual
1024-cell orbit of the reviewed 128-point permutation model. That orbit
membership is an external exact check. The source-family identification,
Sylow normalization, local intersection criterion and polytopal recognition
are written proofs, not formalized by this file.

Read the [complete manuscript](../phase83_nonabelian_cover_theorem.md)
with its [required conjugation erratum](../phase83_nonabelian_cover_erratum.md).
The geometric theorem excludes finite odd kernels only when both end maps
are injective. It does not establish unrestricted uniqueness of covers,
historical priority or a certified open-conjecture resolution.

Fresh compilation and orbit checking, using the pinned dependencies:

```sh
python3 -O research/case_study/phase83_nonabelian_cover_check.py \
  --packages /path/to/pinned/packages --lean /path/to/lean-4.32.2 \
  --output-dir /tmp/human-compression-odd-kernel-new
```

Run from the repository root and use a new output directory. The outer
publication manifest binds the exact manuscript and its retained inputs;
the runner checks regeneration and the formal/computational implication.
Existing compiled dependency libraries remain trusted build inputs.
