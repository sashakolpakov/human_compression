# Independent review of the compact 2002 forest-and-parity proof

10 October 2026. **PASS: no mathematical gap found in the complete written proof.**
This is an internal independent review, not external peer review, a formal
verification, or a publication-priority claim. The reviewed replacement is
[phase15_N003_matched_proof.md](phase15_N003_matched_proof.md), SHA-256
`d626e5534cb0af9205a7349ff651b2a53f29d8a6f87053993040c2fd9a3d6d7c`.

## Source and exact coverage

I read the complete twelve-page author-manuscript extraction for Cameron–Cara,
*Independent generating sets and geometries for symmetric groups*, including
all proofs and references, and compared the replacement with the longer,
previously reviewed [phase12 derivation](phase12_N003_reduction.md).
The private source PDF has SHA-256
`43f3f2b1cbb7dacc55f12572ef78a5bb574bcfe745aba6cc0c10291256e611a2`;
the page-labelled extraction has SHA-256
`165ef2f20f7b5b3f04021205e002e0f22d2249b035bbc480de10f21986d14310`.
Third-party source files are not part of the original-artifact export.

The exact targets are Theorem 1.1 (manuscript pp.2–3), Theorem 2.1
(pp.3–5), Corollaries 2.2 (pp.5–6), 2.3 (p.6), 2.4 (p.7), Theorem 3.1
(pp.8–9), Theorem 3.2 (pp.9–10), and Corollary 3.3 (p.10). The general
bounds are claimed for finite groups; the symmetric-group classifications
retain n≥7. Small-degree remarks, open questions and arbitrary infinite-family
extensions are excluded. Both directions of the two classifications and all
three numerical counts are present.

Whiston's independent-family theorem W1 and omission-subgroup consequence W2
are distinct retained inputs. W2 is not inferred merely from W1. Their CFSG
dependency, Cayley's formula, elementary permutation theory, and the source
coset definitions/criteria (G1)–(G4) remain explicit. No proof of those retained
inputs is silently attributed to the forest argument.

## Points checked independently

* The quotient substitution works both for ordinary independence and the
  abelian normal-subgroup action refinement: conjugators can be represented
  by words in T because N acts trivially on itself.
* The imprimitive exclusion contains the needed module argument. In full
  dimension, an independent module basis forces every omitted coordinate
  hyperplane, and hence every basis line, invariant. Over F₂ this contradicts
  the nontrivial transitive block action. Equality forces the full S_m action
  by W1. A nonconstant vector generates a module containing every e_i+e_j;
  the codimension-one quotient then bounds module-independent families by two.
* Orbit-crossing edges form a tree, and the components after deleting e_i
  are precisely the omission-group orbits. Intersecting the other cut
  stabilizers restricts s_i to its one-edge or two-edge support. The even
  alternatives are exactly the claimed three-cycles and double transpositions.
* Forest intersection and the sign kernel give every marked subset subgroup,
  including the empty subset. The inverse sign on a generator leaves its
  cyclic subgroup unchanged; it is not incorrectly treated as a new subgroup.
* Multiplication by the unique odd member recovers a unique actual
  distinguished-edge tree. Independent endpoint switches preserve the
  contracted tree. Thus actual generating sets and inverse-identified sets
  have the different stated counts; no extra factor of two is introduced.
* The relative-B argument proves its slightly stronger μ′ formulation.
  At most one cut is balanced, and the sole extra proper overgroup there
  interchanges its halves. A different pendant cut forces B to fix a point,
  excluding that extra coset and giving B=1 by full subgroup IP.
* The geometry converse proves typed Helly for partial flags through laminar
  atoms, then adjusts parity using the distinguished transposition in every
  cut intersection. In parity-fixed residues the distinguished component
  supplies an odd correction for other symmetric factors. If it is the only
  nontrivial component, its alternating group has the required primitive
  natural action, including the A₃ boundary.
* The final Corollary 3.3 bridge is substantive and retained. Arbitrary
  parabolics may initially enlarge one balanced cut. Every panel containing
  that enlargement also contains another cut stabilizer, which prevents
  interchange of the balanced halves. Hence every panel is still <s_i>.
  Only then does repeated source (G2) recover all larger parabolics. The proof
  never assumes that the chosen independent marking alone identifies the
  original arbitrary geometry.

The compact text therefore retains all needed steps for the stated targets.
No new computation was performed for this written review. Earlier finite
checks are diagnostics rather than proofs of Whiston's inputs or the
all-parameter classification. This review makes no numerical compression
claim: exact source-span selection and accounting require their own protocol.
