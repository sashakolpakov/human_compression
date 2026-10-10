# Independent review of the family replay and character-separation interface

10 October 2026. Reviewer: `/root/review_unified_seven`.

**PASS for both precisely limited interfaces.** The new public wrapper
reproduces the eight finite diagnostics of the previously reviewed odd-prime
family. The Lean supplement proves the algebraic character-separation step
under explicit hypotheses. Neither is a formal proof of the whole geometric
family theorem or a proof by finite sampling of its unbounded parameters.

## Standalone GAP wrapper

I read the complete `phase67_cover_family_verify.py` and the complete bound
6,328-byte GAP program, and checked their interface with the already reviewed
phase49 theorem and phase59 review. The wrapper SHA-256 is
`2fcdbfd5c838ea6b1af6db65f78e3b7ac69c5ef21d259222685f55087344c079`.
The executed GAP program SHA-256 remains
`999a878716810ab4ce476ea2a45c6986d36ef9530a7d02ef3a3871074dab3cfe`.
The theorem and independent mathematical review are bound too. The distributed
private/public copies of these four files and all four saved replay artifacts
are byte-identical.

The program uses stock GAP constructions from the literal presentations:
finite-presentation/permutation isomorphisms, subgroups, intersections, marked
homomorphisms, semidirect products and generated mixes. It reads no private
primary capture, seed, source classification catalogue or external GAP file.
The standalone wrapper therefore removes the historical runner's private
file dependency without weakening the reviewed mathematical contract.

Before creating its new output directory, the wrapper rejects an existing
path, checks all three frozen input hashes and finds the GAP executable. It
copies the exact program into the output directory and runs that local copy.
Its PASS condition requires a successful exit without timeout or stderr, the
exact eight parameter rows in order, every expected group order, GAP 4.15.1,
the exact prior canonical log hash, and unchanged originals and executed
copy. A timeout or mismatching evidence cannot receive PASS. The parser's
whitespace/continued-line treatment is used for row extraction; it does not
weaken the separate full-log hash comparison.

The saved **root-executed fresh public run** took 71.156552 seconds. I checked
the actual scratch report, executed copy, raw stdout, empty stderr and
canonical stdout against their distributed copies. Only CRLF and bare CR are
converted to LF in canonicalization. The resulting log SHA-256 is exactly
`e89d679dc4de9be0c049002235ccee4bef8548ef7ac3c8ab2197a584e8f77a77`,
matching the two earlier successful certificate runs. I independently checked
the eight parameter tuples and all six order formulas in every report row:

\[
 (|P|,|R|,|T|,|Q|,|Q'|,|H|)
 =(4p^2q,4p^3q,4p^2q,4p^4q,4p^4q,4p^5q),\qquad q=p^\alpha.
\]

These cases are `(3,2,1)`, `(3,2,2)`, `(3,3,1)`, `(3,3,2)` and
`(5,2,k)` for `k=1,2,3,4`. The exact original program also checks the
local intersections, coordinate identities, normal closures, marked
covering/duality maps and action signs recorded in the earlier proof audit.

I did **not** repeat the eight-case computation. I did independently run the
public wrapper against the already existing scratch directory: it exited
with code 2 before GAP and preserved all **five** files byte-for-byte. The
original no-clobber prose had said six; root corrected that metadata to five
before this audit's final binding. The hash dictionaries and replay result
were unaffected. My fresh evidence checker and refusal transcript are part
of this package.

The bounded cases remain diagnostics. The all-parameter theorem is the
separately reviewed written argument for odd prime `p`, `α≥2`, and equal
nonzero parameters `k₁=k₂=k`. Its retained Table 2/Theorem 4.7 source
construction, tight order/normal form, intersection property and geometric
interfaces remain substantive. No current-openness or historical-priority
conclusion is drawn from the replay.

## Lean statement and mathematical meaning

I read the entire 65-line source, its scope note, the dedicated build wrapper,
the dependency manifest, and the saved root build report and complete axiom
log. The source SHA-256 is
`867acfc453c907055b0658340394c823068b636f1a46813fd4aa783b3b834d79`.
The three declarations are in `MathCompression.CoverCharacterSeparation`.

`no_marked_cover_iso` takes group homomorphisms `π : H →* G` and
`π' : H' →* G`, elements `a : H`, `a' : H'`, and `z : H`. Its
hypotheses are exactly:

* `π z = 1`;
* `a⁻¹ * z * a = z⁻¹`;
* `z ≠ z⁻¹`;
* every `w` with `π' w = 1` satisfies `a'⁻¹ * w * a' = w`.

It concludes that there is no group isomorphism `e : H ≃* H'` satisfying
both `e a = a'` and `π'.comp e.toMonoidHom = π`. There is no hidden
finiteness or surjectivity hypothesis. The proof sends `z` into the target
kernel, transports the conjugation identity through `e`, combines it with
the fixed-action hypothesis, and uses injectivity to contradict
`z ≠ z⁻¹`. The multiplication/conjugation convention is exactly
`z^a = a⁻¹ z a`, matching the written proof and GAP certificate.

`ne_inv_of_odd_prime_order` assumes `Nat.Prime p`, `p ≠ 2` and
`orderOf z = p`. If `z` equaled its inverse, then `z²=1`, so its order
would divide 2; prime divisibility would force `p=2`. The formal proof
uses those standard element-order and prime-divisibility lemmas explicitly.
Its assumptions exclude the characteristic-two case; it cannot be used to
separate the two-primary family merely by changing `p`.

`no_marked_cover_iso_of_odd_prime_order` combines those two results without
adding assumptions or strengthening the conclusion.

The exact interface to phase49 §6 is valid. Take `H` and `H'` to be the
rotation groups of `Q` and `Q'`, `G` the rotation group of `R`, and `a,a'`
their first marked rotation generators `A`. The written kernel characters
are respectively `(-,+,+)` and `(+,+,-)`, and the kernels have order the
odd prime `p`. Choose a generator `z` of the first kernel. The first `A`
inverts it; the second `A` fixes every element of its cyclic kernel. These
written facts supply precisely the Lean theorem's assumptions. A marked
isomorphism over `R` is therefore impossible.

This application retains the **existence and order of the groups and kernels,
the action tables, the covering maps, polytopality, and minimality** as written
results. It also retains the geometric passage from rank-preserving polytope
isomorphisms to the relevant marked-cover comparison. The source file does
not construct or verify those objects. It does not rule out an unmarked
abstract group isomorphism or the rank-reversing duality that the family
actually possesses. The root scope note states these boundaries correctly.

## Build evidence and exact trust boundary

The saved root build uses Lean 4.32.2 and the pinned package revisions in the
dependency manifest. The dedicated wrapper checks the chosen Lean version,
each dependency's git revision and tracked-file cleanliness, uses only those
package-library paths, refuses an existing output directory, rejects compiler
errors/warnings and unapproved axiom names, requires exactly one axiom report
per declaration, and checks the source is unchanged after compilation.

I independently bound the source, wrapper, dependency manifest, saved report
and log and compared every reported dependency revision with the manifest.
I did not perform another Lean build or inspect all transitive compiled
dependency objects. Those existing compiled objects remain trusted build
inputs, as the wrapper and report explicitly disclose.

| Declaration | Exact reported axioms |
| --- | --- |
| `no_marked_cover_iso` | `propext`, `Quot.sound` |
| `ne_inv_of_odd_prime_order` | `propext`, `Classical.choice`, `Quot.sound` |
| `no_marked_cover_iso_of_odd_prime_order` | `propext`, `Classical.choice`, `Quot.sound` |

The complete saved log SHA-256 is
`54939524bdf5ed5e4b3a830dbb4ac4402889d13e2d06197fbe637eb2bca84e6c`.
There are no `sorryAx` or native-evaluation axioms. These facts certify the
three stated implications; they do not certify every sentence of the family
manuscript or its retained source classification.

This review adds no manuscript to a compression assembly, no length ratio,
and no cleared historical-novelty or open-conjecture-solved marker. It changes
no public or frozen author file. Its manifest is the exact export allowlist
for this additive independent evidence.
