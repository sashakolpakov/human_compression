# Independent review of the odd-cover algebra certificate

10 October 2026. **PASS for the six stated general algebra/order theorems and their compilation interface. No correction required.** This review admits no proposed affine construction, intersection property, family theorem or open-conjecture solution.

I read the entire frozen Lean source, scope note, compilation wrapper, author manifest and both author execution/control reports. I verified all eight exported author files, including manifest SHA256 `751538c486b332aec54437dd49e17d84b76ecddacedbc83fb2ddfc6373301628`, and the retained dependency-manifest binding. The Lean source is SHA256 `3ae3d89b561edf9b5e536863383405b4476b692ada4cc95ac1b5cbc9d0aadec1`. No author or public file was modified.

## Mathematical scope

For homomorphisms pi:H->G, sigma:J->G and a surjective q:H->J satisfying sigma composed with q equals pi, every y in ker(sigma) has a q-preimage x; commutativity forces x into ker(pi). The defined `kernelMap` therefore maps the entire first kernel onto the second. Applying Mathlib's `Subgroup.card_dvd_of_surjective` proves the second kernel's natural cardinal divides the first.

The first five statements require neither H nor the base G to be finite, nor pi or sigma to be surjective. They use `Nat.card`. Its oddness hypothesis excludes its infinite-type value zero, so there is no hidden inference from an infinite cardinal to odd finite degree. No abelian-kernel hypothesis occurs. The oddness and no-even/no-double-factor conclusions follow correctly from divisibility by two; the existential factorization being excluded includes both surjectivity of q and the commuting equation.

The sixth theorem explicitly assumes `[Finite H]` and accepts an arbitrary predicate `admissible : Subgroup H -> Prop` with `admissible bottom`. It proves that some N is normal, contained in ker(pi), admissible, and inclusion-maximal among subgroups with those properties. Its proof obtains finiteness of all subgroups from the injection into the finite powerset, then applies finite-set maximality. It proves a maximal element, not a greatest or unique one, and supplies no algorithm for selecting a concrete quotient.

The informal minimal-cover interpretation is correct **conditional on** a finite marked polytopal cover, the intended quotient predicate, and the marked cover/normal-quotient correspondence. The scope note states these inputs and does not disguise the predicate as an already formalized polytope condition. A further polytopal quotient would pull back to a larger admissible normal subgroup. Odd kernel order passes to such quotients, so they cannot factor onto a double cover over the same base. Applying this to any particular chiral source also needs its relation to the smallest regular maniplex, as explicitly disclosed.

No construction from the pending expanded-end package is a formal hypothesis, imported theorem or verified conclusion here. In particular this file does not prove existence of the proposed large odd cover, its exact degree, its IP, its uniform transport, the odd minimal descendant's exact order, or a specific source conjecture.

## Fresh independent replay and controls

I copied **only** the exact author wrapper, Lean source and dependency manifest into an isolated directory and ran the wrapper using optimized Python from an unrelated working directory. This tests its relative-layout portability without relying on other study files. The explicit external Lean executable and package directory remain necessary.

The fresh Lean 4.32.2 compile completed in **4.715548999956809 seconds**, exit zero, empty stderr. Its entire 698-byte axiom log is byte-identical to the author's log, SHA256 `ce78b8fd3fb04497335bbb768ca5ac0f528f81307a812551b199505da17e304d`.

| Theorem | Reported axioms |
|---|---|
| `kernelMap_surjective` | `propext`, `Quot.sound` |
| `kernel_card_dvd` | `propext`, `Classical.choice`, `Quot.sound` |
| `odd_kernel_of_quotient` | `propext`, `Classical.choice`, `Quot.sound` |
| `no_even_kernel_factor` | `propext`, `Classical.choice`, `Quot.sound` |
| `no_double_cover_factor` | `propext`, `Classical.choice`, `Quot.sound` |
| `exists_maximal_admissible_kernel` | `propext`, `Classical.choice`, `Quot.sound` |

There is no `sorry`, admitted axiom, `sorryAx`, native-evaluation axiom or compiler warning. The source has six theorems and one auxiliary definition; it does not claim seven independent results.

My separate controls rejected an existing populated output directory, ordinary file and dangling symlink. All three successful build artifacts were unchanged. Two isolated mutations, to the Lean source and dependency manifest, were rejected before any output directory was created. The copied input bytes were restored, and all original author bindings were rechecked unchanged. These are fresh independent controls, not just a reading of the author's control report.

## Retained inputs and limits

The wrapper verifies the Lean version, all nine declared package HEAD revisions and tracked-file cleanliness, and compiles the exact source under the resulting explicit library path. Mathlib is pinned at `905b95818eb32af7874a58b427f50c1711a5e96c`; dependency manifest SHA256 is `4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3`. I also read the precise Mathlib cardinal-divisibility and finite-maximality lemmas used by the source.

As the author states, existing compiled dependency objects remain trusted inputs. This review does not rebuild every Mathlib dependency or claim that Git cleanliness hashes those compiled objects. Source/dependency hash checks and exact axiom reports delimit the local certificate; the outer author manifest is separately verified by the independent runner. A hostile concurrent filesystem mutation is outside these ordinary no-overwrite controls.

The attribution is proportionate: these are standard group/order arguments using Mathlib's Lagrange/cardinality and finite-set maximality results. The repository contributes the explicit commuting kernel map and scoped formal statements. No historical novelty, additional source manuscript, compression factor or whole-polytope Lean verification is claimed.

The independent replay can be repeated into a new directory using `phase107_odd_cover_formal_review_check.py --output-dir NEW --packages PINNED_PACKAGES --lean LEAN_4_32_2`. The final review manifest binds that runner, the exact fresh execution record and compiler log, and this semantic audit. Compiled `.olean` files are not exported. Mathematical review of the frozen expanded-end construction remains separate.
