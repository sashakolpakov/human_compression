# Formal review of the finite label-eight rewrite certificate

10 October 2026. **PASS for the two actual finite-alphabet rewriting
theorems.** Every descending triple on the 63-letter rank-fourteen
alphabet has joining rewrite branches, and each of the eight rank-three
source words reduces to the empty word. All intermediate words stay in
the specified alphabet. This certifies the finite lemma used in the
separately reviewed all-rank construction; it does not formalize that
entire construction.

## Frozen sources and independent reading

The author manifest `phase167_label_eight_manifest.json` has SHA-256
`205eb9133601dc9570d082fda6ada69b7d6930e872751c99d30569f729d01f44`.
Its three sources are:

| Source | SHA-256 |
|---|---|
| `formal/LabelEightCriticalPairs.lean` | `22dce0b70cba3f4a9c9e3608bda7ee829e7d3d7352ec96d887e2a2b3a07a092d` |
| `formal/LabelEightFiniteCertificate.lean` | `7e8955c729a052f24075197e24371abdbcf77efd0f45f972b85320cfa4cffec4` |
| `formal/LabelEightAlphabet.lean` | `31a97fdde7ed8c518c8251a90a82498e4041cc58dce2d94a29bd7e6d75f7a24b` |

Root independently read all three complete Lean sources, the complete
scope, the dedicated build wrapper and controls. The table was compared
entry by entry with the already reviewed positive presentation, including
its index blocks at ranks fourteen and three. Root requested the explicit
finite-alphabet restriction after reviewing the first two files; the final
third file supplies it without changing their sources. Root did not author
these Lean proofs. Root's contribution to the wider mathematical research
is disclosed in the separate phase168 written review.

All thirteen author exports and four retained bindings were checked against
the frozen manifest. The exported source files are unchanged. A display
reader repairs inline math delimiters and one control-character typo in
the scope's binomial-count expression; its exact edit record preserves the
original author file. The corrected count is \(\binom{65}{3}=43,680\).
No mathematical or Lean-source correction was needed.

## What the formal proof establishes

`Step` is an actual contextual application of the declared power or
commutation rule, with an arbitrary prefix and suffix. Induction on the
input word proves that `next` selects such a step. Induction on fuel then
proves that the bounded collector's output is reachable from its input.
The zero-fuel case is reflexivity. Thus this proof assumes neither that
fuel suffices for normalization nor that normalization terminates.

Equality of the two collected critical branches supplies a common
descendant through their two proved reachability paths. The range adapter
covers exactly all a<63, b≤a and c≤b, including equal indices and square
overlaps. Sixty-three row lemmas use ordinary kernel `decide`; their
aggregation supplies the entire finite check. The eight source words are
the literal concatenations of the two adjacent products, squared, with
natural exponents k<8. Their empty collected outputs become proved rewrite
paths, rather than imported Python results.

The generic relation accepts natural-number labels, so merely proving
reachability there would leave a finite-alphabet obligation. The final
module checks rule closure at (rank,bound)=(14,63) and (3,8), proves
preservation under a contextual step, and inducts over every rewrite path.
Its `AlphabetStep` requires both endpoints to be bounded. The final
critical-pair and source-word theorems use the closure of this restricted
relation. In particular no joining path can leave the alphabet and later
return. All input branch and source-word bounds are proved.

None of these theorems assumes confluence, a group structure, the desired
intersection property or the target joinability statement. No external
finite answer is installed as an axiom. The independent Python computation
is additional evidence for the same literal table, not a formal premise.

## Fresh public compilation and controls

Root registered all three files in the public generic runner and Lake
library, then freshly compiled the exact public sources with:

```sh
python3 -B research/case_study/formal/verify_lean.py LabelEightAlphabet.lean --packages /Users/sasha/bogachev/formal/.lake/packages --lean /Users/sasha/.elan/bin/lean --output-dir /private/tmp/phase171_label_eight_public_build
```

All three local sources were selected and rebuilt successfully in
**92.615 seconds**. The three saved `.check.json` files are these fresh
public reports, not relabelled author executions. Root checked every one
of the 15 printed declaration reports; all use only standard axioms, and
the source-word Boolean certificate needs no axioms. Sixty-three row
helpers and three further support lemmas are also kernel checked in the
same files. These declarations comprise one finite proof package, not
81 independent research results.

The pinned environment is Lean 4.32.2 and mathlib revision
`905b95818eb32af7874a58b427f50c1711a5e96c`. Exact dependency revisions
and tracked-file cleanliness were checked. No missing Mathlib object had
to be built. The installed compiler and cached dependency objects remain
trusted build inputs; this is not a rebuild of all Mathlib. Neither
`native_decide` nor an unproved placeholder occurs in these sources.

The separate author five-file portable replay took 91.085 seconds, with
peak child memory about **4.76 GiB**. This is a substantial kernel
calculation. The bound author controls pass twelve cases: four changed
inputs, four occupied-output cases, and four deliberately altered
mathematical table entries. For each mathematical alteration, the modified
generic core still compiles, its selected Boolean critical comparison is
kernel-proved false, and the assertion that it is true is rejected.
This establishes sensitivity of the check, not a theorem that the altered
rewrite system has no possible joining path. Root read those controls and
their exact results; they were not needlessly rerun after the independent
positive public compilation.

The public build and dependency records are
`phase171_label_eight_public_build.json` and
`phase171_label_eight_dependency_builds.json`. The exact exported files,
saved reports, display reader and this review are bound separately in
`phase171_label_eight_export.json`.

## Boundary of admission

The remaining all-rank steps are the well-founded termination order,
support preservation and compression to rank fourteen, confluence,
normal forms and the presented group, group/parabolic orders, generation,
exact type, class, parity and IP. Extending the eight local words to every
integer exponent and the geometric correspondence are also written steps.
Their complete written review is phase168. The 8n corollary additionally
uses the separately proved parity-mix theorem and actual odd-factor inputs.

The project now has 66 scoped Lean modules: 65 without native-evaluation
axioms and one historical module retaining four explicitly recorded
native-evaluation axioms. This finite package adds no principal-source
replacement, conjecture-count entry, historical-priority clearance or
compression factor. It replaces the computational trust requirement for
this finite lemma by an ordinary kernel proof under the stated compiler
and dependency trust boundary.
