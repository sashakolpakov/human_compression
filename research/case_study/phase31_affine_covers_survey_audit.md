# Independent review of the regular affine-cover family

Date: 10 October 2026. Reviewer: survey_audit. Verdict: **PASS within the explicit retained-input scope**. I read the complete frozen six-section proof, inspected the entire new checker and independently replayed it. I did not enumerate a homology cover or the resulting affine group, and I make no novelty claim. I previously developed the general graph-cover framework used elsewhere in this project; this review is independent of the present surface-cover and column-collision argument.

The reviewed proof is `phase31_affine_covers.md`, SHA256 `ecd97b2a3eb5fc64f1b790f39ceff291c0c439e3ff7a01d7abf8ad9b797e7b64`. The companion JSON binds all reviewed and executed bytes.

## 1. Surface and lift extension

The seed has embedded pentagonal faces and circular vertex/edge/face links. Thinness and connectedness give a closed connected triangulated surface. The exchange of permutation points6 and7 supplies a homomorphism that changes on every flag adjacency; orienting barycentric triangles according to this sign is consistent across common sides. Euler characteristic−6 therefore gives genus4. The new checker verifies the local topology separately from the older affine-code certificate.

Every combinatorial seed automorphism acts simplicially on the barycentric surface. For a regular connected cover, the group of lifts has the asserted exact sequence and order120t. Its flag action is free and transitive: a lift followed by a deck transformation reaches any lifted flag, and a flag fixer must be a deck transformation fixing an interior point. This argument needs neither a splitting of the extension nor orientation preservation. Embedded closed disks and their boundary vertices/edges lift homeomorphically, so the five-edge local blocks and exactly-two-common-edge incidences survive.

## 2. Local code transport

The map summing coefficients over edge fibers sends every lifted defining row to its base row, hence descends to the surjection on code quotients. A lifted block has a five-term relation, giving dimension at most4, and surjects onto a dimension4 base block. Thus its restriction is an isomorphism. This is the critical reason no assumption about the full lifted code rank is hidden in the argument.

For an incident vertex-face pair, the intersection injects under that local isomorphism into the certified two-dimensional base intersection. The two actual common lifted edge columns map to independent base columns and lie in both spaces. The intersection therefore equals their span exactly. This uses no quotient-IP assertion. Once column distinctness is established, the same local injectivity proves the precise membership condition q_e∈W_B iff e∈B.

## 3. Collision contradiction

I checked the strongest part of the proof without assuming an abelian deck group. A same-fiber collision produces a nonidentity element of the column stabilizer in D. That stabilizer has order at leastp, and the orbit contains at mostt/p distinct columns. Since the full lift group is edge-transitive and normalizes D, stabilizers of all edge columns are conjugate; the bound therefore applies to every one of the30 base fibers. It is not necessary that the initially chosen deck element fix any other column.

The distinct columns span Q′, so dimQ′≤30t/p≤6t. Independently, the sum of all vertex rows is zero and the sum of all face rows is zero. Bounding each row-family rank separately yields dimQ′≥6t+2. This does not count the two relations as independent within an already combined family; summing the two separate upper bounds is valid even if the row spaces overlap. The strict contradiction also works atp=5. The generalized numerical condition is sufficient for exactly the same reason, with the minimum nontrivial deck-element order replacingp.

## 4. Infinite family and exact conclusions

The subgroup [Π,Π]Π^p is characteristic, and the genus4 presentation gives quotient(C_p)^8. Thus the relevant covers exist with degreep^8 for every primep≥5. Characteristicity, including its invariance under inner automorphisms, handles the basepoint/outer-automorphism issue and lifts every seed symmetry. A lift of the inverse gives an inverse homeomorphism. This establishes the all-parameter step from standard covering theory, not from selected homology computations.

I checked the affine-construction hypotheses against the frozen phase30 argument: nonzero/distinct columns, exact block membership, local one-relation spans, invariant code, and the common two-column intersections are precisely what its chamber and residue proof uses. The covered map's actual regular marking supplies the same local dihedral actions. Consequently the local order160 parabolics and the order8-versus-order4 meet failure transfer unchanged.

The full affine group order120p^8·2^(m_p), lower boundm_p≥6p^8+2, object counts and failed-residue count all agree. For example, the60p^8 incident base vertex-face labels each produce2^(m_p−2) compatible affine pairs, giving15p^8·2^(m_p) disconnected halved residues. The odd parts15p^8 distinguish different primes, independently of the unknown code dimensions. The conclusion is genuinely an infinite family at one connected rank-four diagram; no exact formula for m_p is claimed.

The source qualification is correct: the family defeats RC/hypertope preservation in the inspected2024 preprint, not its literal coset-isomorphism assertion; the revised journal body and priority remain unverified.

## 5. Retained primary inputs and fresh execution

I independently downloaded the primary [Hatcher chapter1 PDF](https://pi.math.cornell.edu/~hatcher/AT/ATch1.pdf) into scratch space and read Proposition1.33 and its lifting proof, Theorem1.38 and the surrounding classification argument, and Proposition1.39 and proof (printed pages61–62,67,71). Their hypotheses hold for the closed connected surface. The separate [Hidalgo primary introduction](https://arxiv.org/html/2407.05442v1) corroborates the characteristic homology-cover construction and lift extension. The proof explicitly supplies the orientation-reversing case; it does not import a conformal-only assertion for those symmetries. No whole-book or whole-paper reading is claimed, and no third-party full text belongs in the public export.

Fresh command, executed from the workspace root:

```sh
python3 research/leemans/phase31_seed_surface_check.py \
  --seed research/leemans/phase30_affine_map_check.json \
  --output research/leemans/phase31_affine_covers_survey_run.json
```

Exit0, PASS. The output is byte-identical to the authored report, SHA256 `7c3fb1ddeff1c1cb7dc4466d86577a6ae6ddc661e5dce05bcb910d5679341092`. The new finite checks cover12 embedded pentagons,54 circular links,180 panels, integer boundary composition/cancellation,14400 character products, adjacency colors and homology ranks at primes2,3,5,7,11. Their scope is the retained finite seed and selected homology diagnostics. The uniform topology, collision inequality and infinite-family construction remain written mathematics. No corrections are outstanding.
