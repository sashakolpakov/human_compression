# Independent review of the odd-prime cover-family theorem

10 October 2026. Reviewer: `review_unified_seven`, who did not author the construction. This is internal independent mathematical review, not external peer review. Exact execution results and final hashes are in the companion JSON and manifest.

**The written all-parameter argument passes, conditional on its openly retained source construction and standard geometric correspondence.** For the specified family with odd prime `p`, integer `α≥2` and `1≤k≤p−1`, it proves two rank-preserving nonisomorphic minimal regular polytope covers. This is a verified family case of the older proposed multiplicity assertion. It is not a certification that this case was still open, that this is its first proof, or that the complete conjecture has been settled.

The exact reviewed theorem is `phase49_cover_family_theorem.md`, SHA-256 `769ddbf891597c3c0d6246ad3f93b354dd02226e02d90cff1eaa250b7bbd4725`; the frozen author manifest has SHA-256 `7b3d83c2078641708612deb206ed668ed32bf05e431d77ab66608e29ac7c0003`. I read the complete eight-section proof, full ledger and intake, every line of the 6,328-byte GAP certificate, and the complete runner. I independently checked each new algebraic interface below. No frozen source or public-repository file was changed.

## Exact source and attribution contract

The input is the Γ1 row of Table 2 and Theorem 4.7 in the author version of Cunningham–Pellicer, [*Tight chiral polytopes*](https://arxiv.org/pdf/2009.04566). Here `q=p^α`, `h=p^(α−1)`, `d=kh`, and the exact rotation presentation is

```
a^(2p)=b^q=c^(2p)=1,
(ab)^2=(bc)^2=(abc)^2=1,
b a²=a² b^(1+d),     c² b=b^(1+d)c².
```

The source's two parameters must be equal and nonzero modulo the odd prime. The family is the first **chiral-facet/chiral-vertex** row of Table 4, not its first row overall, and is one of the five families cited in Example 3.5 of Cunningham's [smallest-regular-cover author manuscript](https://gabrielcunningham.com/WhichChiralPolytopes.pdf). The theorem does not apply to every polytope of the same Schläfli type, to `p=2`, or to `k=0`.

I checked the bound Table 2 presentation and the complete extracted Theorem 4.7 argument and local Lemma 4.6 context. I freshly reopened the primary Table 2 context through the web tool, and checked the bound Table 4 row and the subsequent smallest-cover manuscript's Example 3.5 and Section 4. The saved source captures are text extractions, not local PDF-byte bindings. A fresh attempt to inspect PDF screenshots failed with cache-miss errors; no successful visual formula audit is claimed. This does not change the explicit source-version limitation. I did not reread or verify the whole 43-page classification or acquire its publisher-version proof.

The retained older work is substantial: Theorem 4.7 identifies the exact bare presentation with a tight chiral polytope and supplies its precise generator orders, full order `4p²q`, unique tight normal form and intersection property. Its earlier atomic-polyhedron classification and recognition arguments remain part of that imported theorem. Atomicity itself is not used after the input is identified. The new argument does not need to import Proposition 4.2's classification of chirality groups; it derives the relevant cyclic normal subgroup and full mirror mix directly from the displayed relations.

Standard recursive string-C/C+ recognition, the marked group/polytope correspondence and the universal property of the smallest regular maniplex cover are also retained. Elementary semidirect products, subgroup quotients and finite vector spaces are ordinary mathematical background. The fiber-product lemma is proved in the manuscript; the already-reviewed cover-kernel theory gives the last defect-set interpretation but is not a substitute for the concrete calculations.

The attribution boundary for the new construction matters. Cunningham's older Section 4 already takes the smallest regular maniplex, mixes it with the trivial extension of a facet and with its dual, and uses prime covering degree for minimality in the finite `p=3, α=2, k=1` example. The repository did not invent that strategy. Its new written contribution here is a uniform proof for all stated parameters: explicit normal coordinates, the exact common quotient and normal closure, all cover orders and intersection properties, a character-based distinction of the dual covers, and the shared interval/join-density conclusion. “New in this repository” is not a historical-priority verdict.

## Review of the all-parameter proof

**Source coordinates and the full mirror mix (§2).** I checked the relation manipulations, including the direction of right conjugation. With `x=b^h`, `u=a²`, `y=c²`, the congruence `d²≡0 mod q` gives the inverse action `1−d`. From `(ab)²=1`, the displayed calculation indeed gives `a b^d=b^(−d)a`; since `k≠0`, this proves inversion of `x`. The presentation duality sends `(a,b,c)` to `(c⁻¹,b⁻¹,a⁻¹)` and exchanges the two extra relations, so the corresponding action of `c` is valid. The actions on `u,y` and the inverse action of `a` follow with the stated signs.

On `P/⟨x⟩`, the proposed mirror preserves every defining relation, including the quotient relation and the extra relations. The use of `p|h` is valid for every `α≥2`. The rotation-square identities make `a²(bc)` an involution. Applying the mirror twice fixes the generators; it is an automorphism, not just an unverified assignment.

For `R≤P×P`, the equality `B^h=(x,x)` follows because `a²b=a b⁻¹ a⁻¹` and `a` inverts `x`. I independently recomputed the facet relator's second coordinate as `x^(−2k)`. Oddness and nonzero `k` are exactly what make this generate the full second cyclic kernel. This matches the fiber-product upper bound and proves `|R|=4p³q` for all parameters. Its unique normal form follows from the retained normal form of `P` and the exact projection kernel. No finite sample or pre-existing chirality-group identification is used for this step.

**The bad intersection and normal closure (§3).** The word identities `Z=[C²,B]=[A²,B]⁻¹` have the correct signs in both coordinates. In particular, `y^(a²)=y x^(−2k)` is necessary in the second coordinate and follows from the preceding action formulas. The diagonal `B^h` and antidiagonal `Z=(x^k,x^(−k))` generate both cyclic coordinates because their determinant is nonzero modulo `p`. Thus each end has its full projection kernel, giving the precise end orders and

`F∩V=⟨B⟩×⟨Z⟩`, of order `pq`.

The claimed independence from `⟨B⟩` uses oddness correctly. Local cyclic intersections are trivial by source IP and exact generator orders; no global IP of the nonpolytopal `R` is assumed. The intrinsic vertex mirror includes the required conjugation by `A⁻¹`; it sends the two vertex generators to the proper mirror marking.

I checked every entry of the action table for `W=⟨C²,Z⟩`. Source cyclic IP proves that it is elementary abelian of order `p²`. The action table proves normality and mirror stability, while commutation with `B` generates `Z` from `C²`; hence it is the **actual normal closure**, not a subgroup guessed from its order. The equalities `W≤V`, `W∩F=⟨Z⟩` and `W∩⟨B⟩=1` follow from source IP as stated.

**The trivial extension and exact largest common quotient (§4).** In `T=F⋊⟨t⟩`, the three reflections `t,tA,tAB` verify the marked rotation relations directly. The last rotation lies outside `F`, giving the exact index-two vertex intersection and the full local IP. The mirror fixes this last rotation. The conjugation character of `J=⟨Z⟩` is `(-,+,+)` and the mirror acts by `−1`; the final positive sign uses both inversions in the displayed word.

The proof of `R/W≅T/J` uses the embedded copy of `F/J` and genuine index-two normal forms. I checked `CBC=B⁻¹` and `CAC=AB²` in both groups. The last generator is outside the facet image, so no missing coset collapses the argument. Since every common marked quotient must kill `C²`, it must kill its entire normal closure `W`. This proves maximality of the common quotient. The manuscript's subdirect-product argument then correctly identifies the mix with the full fiber product.

**Polytopality, global minimality and distinction (§§5–6).** The degree-`p` kernel and order `4p⁴q` follow from that exact common quotient. The facet lift is the identity graph; the vertex lift is the graph of the explicitly identified dihedral quotient `V/W`. Both restrictions to `R` are injective. For an arbitrary element `B^jZ^s` of the bad end intersection, its two lifts agree exactly when `s=0`. This proves the needed global IP. Local IP comes from the ends and regularity from the componentwise mirrors, so the group is an actual regular polytope cover.

Minimality is among all regular polytope covers of the specified `P`, not merely those guessed in the construction. Any regular marked quotient still covering `P` must lie above its smallest regular maniplex `R`; the prime index leaves only `Q` and the nonpolytopal `R`. The source self-duality and the universal property give the dual cover with the same injective local restrictions and minimality.

The two cyclic kernel characters are `(-,+,+)` and `(+,+,-)`. They cannot be identified by a marked isomorphism because inversion differs from identity for odd `p`. A rank-preserving isomorphism of regular polytopes can be adjusted by a flag automorphism to preserve the chosen base flag, so this also proves the asserted rank-preserving nonisomorphism. The objects remain dual and are not asserted to have nonisomorphic abstract groups. The dual mirror sign `+1` follows from the full reflection signs `(-,+,+,+)`; I checked this conversion separately.

**The shared interval and global family join-density (§7).** The kernel of `H=Q⋄Q′→R` projects onto both cyclic kernels. A proper subdirect subgroup would identify their one-dimensional modules, which the different `A` signs exclude. Thus its exact kernel is `C_p²` and `|H|=4p⁵q`. The end groups are graphs over the ends of `R`. Projection to the polytopal `Q` is injective on each end, which transports IP to `H`; regularity again comes from the mirror.

The two coordinate axes are precisely its nonzero proper conjugation-invariant subspaces: the `A` action already has distinct eigenvalues over the odd-characteristic field. Both axes are mirror-stable and yield the two polytopal quotients, whereas the whole kernel yields nonpolytopal `R`. Hence these are exactly the two maximal admissible kernels in this interval. This does not classify other covers outside `H`.

Pullback of the join of those axes gives the full universal kernel of `R`. Both quotient covers are finite, and every regular cover kernel of `P` lies in that monodromy kernel by its universal property. This proves the stated join-density for this family. The passage between the rotation universal group and the full reflection group is valid: all covers of the orientable `P` are orientable, and mirror stability is precisely the extra normality condition. The defect set has size `p` and no nonidentity point on either axis; the resulting one-edge support description does not require pretending that the defect set itself is a subgroup.

No substantive correction to the frozen theorem is required by this review.

## Computation and formalization boundary

I read the entire GAP program and safe runner before fresh replay. The program builds the **bare source presentation**, checks its permutation isomorphism and literal relators, forms the mirror mix, constructs the semidirect trivial extension, and checks the exact normal closure, subgroup intersections and marked common quotient. It then checks `Q,Q′,H`, local injectivity, mirrors and all character signs for the eight declared parameter triples. The expected counts are assertions after construction, not imported witnesses. The full p-primary modules are checked by elementary-abelian order/exponent and exact action computations.

The fresh replay passed under GAP 4.15.1 in 86.202524875 seconds. Its complete output is byte-identical to the author's frozen log, SHA-256 `e89d679dc4de9be0c049002235ccee4bef8548ef7ac3c8ab2197a584e8f77a77`. The command is recorded in the JSON; outputs were directed to new private scratch paths. The runner validates all bound predecessor packages before and after execution. The frozen phase49 manifest and its context hashes were also checked independently, before and after the run. Both existing-output refusal paths preserve their inputs. These eight exact diagnostics corroborate the formulas; they are not an all-parameter proof. Stock GAP finite-presentation and permutation-group algorithms remain trusted. This is not a formally verified decision procedure or a new Lean family theorem.

The GAP program is standalone. The original Python runner additionally validates private predecessor manifests that reference primary-text captures. It must not be advertised as independently runnable from a public export that excludes those captures. A new public wrapper may run the exact standalone GAP bytes and bind the public evidence; that wrapper requires its own review. No source capture is in this audit's export allowlist.

The directly relevant formal status is narrow: the previously admitted phase48 image-intersection/kernel-product criterion is a related Lean-checked algebraic core. The coordinates, fiber products, rank-four geometry, minimality and family join-density in phase49 are written proofs. This review admits **zero additional Lean components** and no end-to-end Lean certificate for this family.

## Per-claim attribution and novelty labels

| Portion | Attribution and status | Verification |
|---|---|---|
| Exact input presentation, existence, orders, tight normal form, source IP | Retained Table 2/Theorem 4.7 construction, with its older dependencies | Selected primary-source match; not reproved here |
| Mix with trivial facet extension and dual; prime-degree minimality idea | Present in Cunningham's earlier single finite example | Explicitly attributed; not a newly invented strategy |
| Uniform coordinates, full mirror fiber product, normal closure and exact common quotient | New all-parameter derivation written in this repository | Complete independent written proof review; finite diagnostics corroborate |
| Two covers for every stated parameter, exact orders and IP, character distinction | Extension of the earlier example to the specified entire family | Complete independent written proof review; historical novelty unverified |
| Shared `C_p²` interval and family join-density | Repository theorem using the now-proved concrete module/interface | Complete independent written proof review; no arbitrary-kernel generalization |
| Geometric recognition and universal smallest-cover property | Retained standard background | Exact scope checked; not newly formalized |
| Family theorem as a whole | Verified instance of the older proposed multiplicity assertion | No cleared “previously open conjecture solved” or priority marker |
| Manuscript compression | No new source replacement or length experiment in this package | No ratio, no added whole-paper credit |

The companion structured audit records the same boundaries for any later margin or sidecar annotation. None of its repository-contribution labels licenses erasing earlier attribution.

The bounded current-status note `phase55_cover_family_source_status.md` found no competing all-parameter resolution, while explicitly declining to certify priority or current openness. I read that note; I did not turn its negative search results into a mathematical theorem or conduct a comprehensive new priority search. The live arXiv HTML date discrepancy it records is not a new submitted version. The warranted conclusion is a reviewed proof of the named family assertion, subject to the retained construction. The remaining four source families, the arbitrary-monodromy conjecture, and a classification of every minimal cover of a family member remain outside this result. It creates no infinite manuscript-length ratio.
