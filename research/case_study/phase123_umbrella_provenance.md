# Umbrella U: attribution, dependencies and exact consumer obligations

Private author ledger, 10 October 2026. This records a new organization of existing proofs plus the explicitly identified changes below. The old monolith is a source bank only. The scientific comparison baseline remains the derivations in the original papers. Neither its length nor any predecessor byte continuity is a benchmark for this manuscript.

## Attribution convention

Four labels are used in this ledger. **Established input** is a classical theorem retained without a new proof. **Reused proof** means that an earlier complete project proof is being used again at a checked signature. **Reorganized proof** means the earlier argument has been separated from source-specific premises or rewritten without a new source-result claim. **New integration step** identifies work developed in this revision; it does not assert historical priority. These labels can become margin symbols in the eventual rendered manuscripts. No theorem here is labeled as an open conjecture proved.

The original authors retain attribution for their source theorems. In particular, the two-group applications concern Hou–Feng–Leemans, Hou–Schulte, Cunningham–Feng–Hou–Schulte, and Gomi–Loyola–De Las Peñas. Cameron–Cara and Archer–Cara–Krempa supply the source context for the relative-generation and Frattini branch. The application volume credits the exact named result and edition at each source contract. U does not absorb that attribution into its own theorem numbering.

## Reusable proof inventory

| Stable U statement | Origin and treatment | Actual dependency or retained input |
|---|---|---|
| U.K0 | Reused phase78 K(0), elementary image/kernel lifting | Group homomorphisms and subgroup closure |
| U.K | Reused phase78 K(a) | U.K0; marked images of generated subgroups |
| U.Q | Reused phase78 K(d), exact image-intersection criterion | Elementary kernel factorizations; set products, not joins |
| U.Coset | Reused phase78 K(b) | Exact inverse images and subgroup correspondence |
| U.D | Reused phase78 §8 deletion proof | Equality of homomorphisms on generators |
| U.SK | New integration step from mutable phase117 and independent phase122 challenge | U.K; distinct finite supports, genuine deletions and all proper-parabolic injectivity |
| U.SK.Local | Reorganized local recognition | U.SK's exact kernel profile and antichain condition |
| U.SK.Delete | New simplification of the previous interface | U.SK hypotheses already give local deletions; U.D |
| U.SK.Central | Reorganized lower-central proof with the same support induction | U.SK; lower central series commute with epimorphic images |
| U.SK.Separator | Reused supported-factor argument at the new interface | U.SK; pure kernels normal in the ambient fiber group |
| U.Fiber | Reused phase78 §8 compatible-product proof | Two explicitly split deletions to the same marked subgroup |
| U.Nilpotent | Reorganized and generalized phase78 Q5.5 | U.K, U.D; retained graded commutator calculus and finite-p-group nilpotence; an expressly assumed exact class-two quotient |
| U.Ladder | Reused phase78 Q5.6 | Burnside basis theorem; odd number of nonzero binary characters |
| U.Order | Reused phase78 §8 order comparison | Product of normal subgroups and finite index |
| U.Helly | Reused phase36 anchored criterion | Right cosets and induction on the number of types |
| U.Compare | Reused complete phase36 all-parabolic comparison | U.Helly; protected product injectivity and exact exceptional membership |
| U.Compare.Matrix | Reused phase36 bounded-entry specialization | U.Compare hypotheses, integer divisibility and complete passing witnesses |
| U.Geometry | Reused phase78 O0/O1 | Flag extension by common representatives, IP, gallery induction |
| U.Action | Reused phase78 K(c) | U.Geometry; actual encoding and retained equivariant surjection |
| U.Orbits | Reused phase110 K(e) action/normalizer proof | Transitive G-set classification; normalizer convention explicitly proved |
| U.ExtensionOrbits | Reused phase78 §21.1 orbit reduction | Equivariance and stabilizer action on a fiber |
| U.RelativeBound | Reused phase78 R(a), with Cameron–Cara source context | Irredundancy and quotient word substitution |
| U.Relative | Reused phase78 R(b) in its pure subgroup-family form | Distinct indexed intersections; residual maximality |
| U.Maximal | Reused phase78 E1 | Zorn's lemma, retained |
| U.FrattiniTransport | Reused phase78 E4 with its necessary infinite-scope hypothesis | U.Maximal as one sufficient route; maximal-overgroup condition |
| U.FrattiniLadder | Reused phase78 E2 | U.Maximal; distinct intersections and one maximal chain |
| U.Phi | Reused phase78 S, with Archer–Cara–Krempa source context | Burnside's basis theorem; coordinate subspaces |
| U.Amalgam | Reorganized phase78 Q9.1, generalized from 2 to an arbitrary prime p | Free-product universal property and amalgam normal forms, explicitly retained |

U.SK's substantive change is the inclusion induction. A kernel word supported on S has no coordinate at a T not contained in S, because proper-parabolic injectivity kills it. Already isolated kernels at smaller supports remove the remaining unwanted coordinates. This replaces the previous separate list of isolated normal-generator words. It also removes a separate local Boolean-deletion assumption: each proper local parabolic is already isomorphic to the corresponding base parabolic. Phase122 independently proposed and challenged this strengthening before this umbrella rendering.

U.Nilpotent does not silently generalize forest quotient rigidity. Its statement explicitly assumes that each target has the specified canonical class-two quotient. Application A pays for the forest graded-support proof and the concrete vertex/edge model once. The universal finite quotient, kernel-profile criterion and index-two ladder are then reused.

## Application A's precise bindings

The mutable companion is phase117_two_group_application.md. Its author is responsible for the complete local proofs. These are intended bindings, not a declaration that the complete application has passed independent review.

| Application | U call and exact obligation |
|---|---|
| A §2, forest quotient and finite search | U.Phi applies after IP proves irredundancy. A must prove the canonical class-two quotient is the vertex/edge model, including independence of all forest-edge commutators and its marked IP. U.Nilpotent then takes F to be the involution/nonedge-commutation presentation and k the exact order excess. A must identify every target map from F and the label-permutation equivalence group. |
| A §2 and §7, finite census | U.Ladder enumerates actual U-normal kernels; the program must retain the original markers, exact subgroup equality, every hyperplane preimage and the full U.K profile condition. Tables, presentations, terminal counts and universal-order certificates remain application costs. |
| A §4, edge inflation | In U.SK take supports to be selected edges, local E_e=D_(2m_e), base parabolic D_(2q_e), with the actual marked quotient and q_e dividing m_e. A proves every required deletion and the singleton/reflection injectivity. Antichain local recognition fixes selected pair orders. Unselected pair orders require the application proof; they do not follow from the order formula alone. |
| A §4, consecutive square sections | In U.SK take the canonical class-two path model as B, supports the selected consecutive triples and local E_S=H_(n_S) mapping to H_5. A proves the marked map, all proper-parabolic injectivity, the exact lattice kernel and its equality to gamma_3(E_S). U.SK.Central then proves the global gamma_3 identity. |
| A §4, path separation and flatness | U.SK.Separator requires an actual set-product equality B=B_L B_M and that every support is contained in one side. A proves that equality from the concrete base model and then proves the geometric incidence interpretation of the resulting H_L H_M factorization. |
| A §4, fork | U.Fiber requires literal deletion maps to the same marked common facet. A must identify its constructed group with the full compatible product, prove all missing cross-coordinate conditions and discharge the retained geometric FAP theorem. A local diagram alone is not a universal presentation. |
| A §4, universal presentation | U.Order applies only after A proves normality and complete finite upper bounds for the kernel factors, the order bound of the remaining quotient, and a marked quotient attaining the bound. The four-marker centralization argument remains proved in A and has its own exact existing Lean theorem. |
| A §5, cyclic-core classification | U.Phi supplies only the exact Frattini coordinates used by A. The retained cyclic-core theorem, all eight extension models, completeness branches and bounded seed remain A's proof and certificate obligations. |
| A §§6–7, central descent | U.Q applies to the displayed actual quotient and its two facet subgroups. A must prove the kernel product condition (or a stated sufficient special case), injectivity/type validity where used, and the subsequent rank-three marking criterion. |
| A §7, exceptional decomposition | U.Phi supplies coordinate characters only after A identifies an irredundant generating family of the actual finite group. The semidirect decomposition and center calculation remain explicit application proofs. |
| A §8, three free extensions | U.Amalgam applies after A supplies the exact retained geometric amalgam identification, embeddings of the common subgroup, properness in both factors, finite generation and p-primary finite torsion of each factor. In the chiral case the embedded facet rotation group and its index-two full-facet extension must be distinguished. |

U.Compare, U.Action, U.Orbits and the relative subgroup-family results have concrete earlier consumers in the original case studies, but no second new application volume is declared complete here. Their acquisition is visible; future use will be credited only when a complete consumer binding is present. A suggested consumer or a textual occurrence is not measured proof reuse.

## Existing Lean proofs: precise coverage

The existing files were inspected at the declaration level for the statements listed here. This phase has not rerun the compiler. Their earlier public build evidence remains historical evidence, and root is preparing the exact new formal bridge. There is no end-to-end Lean certificate for U.

| U statement | Existing declaration | Exact scope and remaining bridge |
|---|---|---|
| U.K0 | LeemansLift.intersection_of_image_and_kernel in LiftCertificate.lean | Proves the substantive reverse implication with arbitrary subgroup C, exact image equality and kernel containment. The forward implication is elementary but is not the declaration's conclusion. |
| U.K | The same lifting declaration | Supplies the pointwise algebraic implication; the quantified actual-marking equivalence is still to be connected explicitly. |
| U.Q | MathCompression.QuotientIntersectionCriterion.image_inf_iff_kernel_product and quotient_inf_iff_kernel_product | Complete arbitrary-homomorphism and actual-quotient equivalences with set products. The special-case application hypotheses still require their own proofs. |
| U.D | MathCompression.BooleanRetractions.range_intersection | Proves range intersection from an already supplied Boolean composition law. It does not supply the actual deletions, their marked images, kernel normal closure or semidirect decomposition. |
| U.SK | LeemansCoordinates.coordinate_kernel_meet and intersection_transport_with_coordinates | Proves the coordinate meet and final transport once an actual kernel-product isomorphism and exact hcoords membership profile are supplied. It does not prove supported-fiber generation, isolation or those premises. |
| U.Compare | MathCompression.ParabolicMarkedComparison.quotient_marking_comparison, with ParabolicProductComparison and its imports | Complete IP and typed-Helly equivalences for actual source-generated and image-generated parabolics, including generation of the target under surjectivity. Formal rank scope is more general than U's finite rank statement. Arithmetic and geometric applications remain outside. |
| Other U statements | No exact complete bridge established in this phase | Existing narrower modules are not promoted to whole-theorem coverage. In particular BinaryFrattiniActions does not formalize U.Phi, and ChamberOrbit does not by itself formalize all of U.Geometry. |

The important new formal obligation is U.SK's support induction, with actual local maps and the generated subgroup of the full fiber product. A coordinate profile assumed as a premise would omit that proof. The existing exact U.Q and U.Compare declarations should be reused instead of reconstructed.

## GKM-derived accounting and draft checkpoints

The acquisition/reuse method is attributed to the local Gödel–Kolmogorov Machine project, specifically its README, COLIMIT_CONE_APPROACH.md, transduction/COFIBRATION_AB.md and transduction/TRANSFER_VALUE.md, previously read in phase121 and with the README reread during this revision. This is methodological attribution, not a group-theoretic input and not a theorem saying all research has a short universal description.

Every checkpoint binds the exact complete U text, each statement and proof body, and its declared consumers. The initial checkpoint is a gross acquisition cost. Later checkpoints record signed token growth, gross token additions, gross token removals and unchanged statement/proof hashes separately. The lexical edit calculation is a reproducible accounting convention, not a measure of mathematical novelty or necessity. A fall in cost can come from refactoring; it does not prove that a deleted argument was redundant. No semantic-necessity claim follows from dependency ablation.

For an eventual replacement package, charge every reachable U proof once, every application proof and hypothesis binding, all required programs/data/decoders, and retained source inputs at the declared comparison convention. Keep a complete-package measure distinct from an individual application's marginal reuse cost. The numerical compression ratio remains unmeasured until a complete reviewed U+A package and the exact original-paper baseline are fixed in the same representation. Consolidating five papers into one application volume is a manuscript count, not that ratio.

No original open conjecture has been resolved by this umbrella manuscript. A future verified resolution must be reported independently; it is new mathematical output rather than an infinite value of a finite source-length ratio.
