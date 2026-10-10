# Proof and dependency ledger

Author candidate, 10 October 2026. This package adds conditional theorems and an exact finite interval computation. It does not add a completed source manuscript to the compression count.

| Result | Exact hypotheses | Proof/evidence | Boundary |
|---|---|---|---|
| Lemma 1 | Arbitrary group H, subgroups A,B, normal M | Complete two-way factorization proof in §1 | AB is a subset product, not necessarily a subgroup |
| Defect reduction and size | Normal L, L∩A=L∩B=1; M normal and contained in L; finiteness for cardinality | Lemma 1 and explicit lift-fiber bijection | No automatic group structure on D=L∩AB |
| Polytopal quotient test | Marked regular polytope group, injective end restrictions | Algebra plus retained recursive string-C recognition | Rotation variant also requires mirror stability and C+ recognition |
| Global minimality from interval maximality | R is the smallest regular maniplex cover of P | Universal marked-kernel factorization, §2 | Completeness is only among covers covered by H; isomorphisms preserve ranks |
| Theorem 2 | Finite H; elementary abelian L with explicit pairwise nonisomorphic simple direct-sum decomposition | Complete module proof and defect-support hypergraph proof | Neither semisimplicity nor this cover's existence is assumed automatically |
| Global join-density from Theorem 2 | Every simple constituent avoids D nontrivially | Each constituent itself admissible; inverse images preserve joins | A constituent meeting D obstructs only this interval's density |
| Theorem 3 | Finite H; central elementary abelian L; scalar mirror action in rotation version | Central lift homomorphism; complements as graphs of linear maps | Formula p^(e(d−e)) is conditional; source example's L is noncentral |
| Cunningham example interval | Frozen phase41 presentations; H=Q⋄Q′ | Exact GAP reconstruction, word/action/set/subgroup/quotient tests | Exactly two minimal covers among quotients of H, not all covers of P |
| Defect need not be normal | Actual Cunningham example | Exact D=⟨uv⟩ and explicit conjugation table | Valid inside the finite-polytope monodromy-cover setting |
| Defect need not be a subgroup | Tetrahedral S4→S4/V4, injective on both ends | Exact set and complete source IP checked in GAP | Target collapses nonadjacent marks; not a polytope-monodromy counterexample |

Retained mathematical inputs are the standard string-C/C+ group/polytope correspondence, its recursive end-intersection recognition, and the universal marked-kernel interpretation of smallest regular maniplex covers. The source example's presentations, their original interpretation, and exact first-stage certificates are bound through the frozen phase41 package. Phase44 supplies the earlier source-status investigation and global-poset context; no phase44 result replaces the new proofs in §§1–4.

The certificate uses stock GAP exact finitely presented group and permutation group algorithms. Its complete added GAP program is embedded in `phase46_cover_check.py`; the runner prepends the hash-bound frozen phase41 GAP source without altering it. It checks every phase41 and phase44 manifest entry before and after execution. Replays require new output paths, for example:

    python3 phase46_cover_check.py --report /private/tmp/phase46-fresh.json --log /private/tmp/phase46-fresh.log

The bound report records GAP 4.15.1 and a successful 1.71-second author run. It certifies the finite example and counterexample, not a finite sampling argument for Theorems 2 or 3. Those have all-parameter written proofs. No additional Lean component is included in this freeze.

The conjectural existence of multiple minimal regular covers for every nonpolytopal finite monodromy quotient remains open in this investigation. None of the five infinite tight families is newly settled. No claim of literature priority is made. The bounded source-status search is inherited with all limitations from phase44; this package contains no additional status search.
