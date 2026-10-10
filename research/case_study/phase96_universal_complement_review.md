# Independent review of the universal local-completion bridge

10 October 2026. **PASS without required correction.** This review is independent of the phase90 author. It covers the complete frozen manuscript, its complete dependency ledger, all four contracts UC1–UC4, and the exact author manifest. The mathematical conclusions remain conditional on the stated classical and source inputs. This review does not admit a public theorem, source count, compression factor, new Lean component, or historical-priority claim.

The reviewed manuscript is `phase90_universal_complement_bridge.md`, SHA-256 `685ad72ffa0c9964693d54a52e3ee79d6b7d754c1b4c520d2b0eabe7087c50c3`. Its ledger is `2b4d84af8550e242560acd70d1f3557b109d7158fdcf4b9cb733851b6ceaa2f9`; its manifest is `b30ddbcf0cecca56ab7584f21aa4ec47fd12ca077c3adb6a29d6b1a6e1c51d7c`. No author or public file was edited.

## 1. The graph, its cells, and the actual free factor

The edge convention is consistent throughout: the right coset Cg labels an edge from Bg to Ag. With a=Cg, b=Cr3g, c=Cr0g and d=Cr3r0g, the boundary d^-1 c a^-1 b is a composable closed path beginning at Ar3g. The use of r0r3=r3r0 is valid in G; it is not used as an equality in the amalgam J before its extra relator is imposed.

For a rooted spanning tree, the equality t_e=h_initial^-1 s_e h_terminal is an invertible change of generators of the free group on the original edge labels. The tree labels remain free generators, while each non-tree s_e is the corresponding based loop. Every closed cell word has only an overall conjugation by its initial tree path, so its normal closure lies in the loop factor. This proves the displayed free product, and shows specifically that killing those *original tree-edge generators* gives the fundamental group. It is stronger than an abstract numerical free-rank match. Neither cancellation of unspecified free factors nor equivariance of the chosen splitting is assumed.

The defect t_C^-1 t_Ci is based at the selected root A because i belongs to A∩B. Its tree words cancel literally. The dependence on a right coset rather than its representative is harmless: (ci)_B^-1(ci)_A=i_B^-1 i_A for c∈C, using the identified amalgam copy of C.

## 2. The kernel identification and orientation

The standard amalgam normal-form theorem gives the left-coset tree J/A, J/B, J/C. N0=ker(J→G) acts freely because its intersection with each conjugate of either local factor is trivial. The inversion map jA↦Aπ(j)^-1, with its B and C versions, identifies its quotient with exactly the right-coset graph above. With left deck action and left-to-right path concatenation, the endpoint map is a homomorphism: the second lifted path translated by n1 ends at n1n2A.

The cell attachment can also be checked without relying on a diagram. For g=1, lift its initial vertex to r3A. Representatives of the four successively traversed edges may be chosen as

```text
r3r0 C, r3r0r3 C, r3r0r3r0 C, r3r0r3r0r3 C.
```

Their endpoint is (r3r0r3r0)r3A. Thus the closed cell has the inverse outer-commutator as its deck element, up to the stated base path. This gives the same normal closure as r0r3r0r3. Left translation by a lift of g^-1 gives the cell indexed by g. A different lift changes only its N0 conjugacy. Consequently all the cells impose exactly the J-normal closure of the extra commutator, not a smaller collection of unrelated relations. Van Kampen yields the claimed kernel K=ker(W→G).

The two-edge defect lifts from A to B and then along i_B^-1 C. It ends at i_B^-1 A=(i_B^-1 i_A)A, giving the exact element e_i claimed in the manuscript. These conventions agree, including the possible reversal of the square relator.

## 3. Finite kernel classes and the complete local scope

Theorem 2 correctly uses a nonempty class of finite groups closed under subgroups, isomorphism and finite direct products. A class satisfying these requirements contains the trivial group, so the empty-defect case I=C is covered too.

For a separating homomorphism K→L, its kernel M is K-normal but need not be W-normal. The core M0 has at most |G| distinct conjugates: K-normality and W/K=G are exactly what makes this finite. Each K/M^w is isomorphic to K/M and K/M0 embeds in their product, keeping the desired kernel class. M0 contains no nontrivial defect, since M0≤M. The quotient W/M0 is finite, embeds both actual local groups, and has end intersection precisely the marked C. The retained rank-four recursive recognition theorem then applies. In the converse direction, exact local injectivity supplies the epimorphism from W and forces every nontrivial defect to survive. Individual separating maps combine by a finite product, and the free-product splitting permits restriction or extension of maps. No coprimality, Sylow splitting, abelian kernel, or normality of C in I is hidden in this argument.

Corollary 3 also holds for an infinite W: one locally faithful polytopal cover separates its ends, so their intersection in W is already C. If K is finite, W is finite because G is finite. All marked covers with these exact ends are quotients W/N over G. The equality E=K∩BA follows from π(b)=π(a)^-1 for ba∈K, using injectivity on both local factors. E is a set; the argument never requires it to be a subgroup. Avoiding E outside the identity is exactly the end-intersection criterion.

This classification is restricted to covers whose two ends map injectively. It does not exclude covers enlarging an end, and does not identify groups after a type permutation. A future explicit finite completion must establish its exact marked quotient and defect images. In particular, no phase92 finite-order or two-cover conclusion is accepted here from cancellation of an abstract free factor.

## 4. Uniform source interface

I read the complete Proposition 4.2 and Theorems 4.8–4.10 with their proofs in the bound Cunningham–Pellicer 2020v1 text, and visually inspected Table 2 on PDF page 23. The parameter scope is q=2^β, β≥5, all four independent sign choices. The endpoint orders are exactly (8,8), (q/2,q/2), and (8,q/2), with the last pair reversed under duality. Proposition 4.2 makes the global chirality group a prime-order subgroup of <b>; since q is a power of two this is <b^(q/2)>, of order two. It also supplies the corresponding local chirality groups. These source existence, tightness, intersection, order and chirality results remain substantial retained inputs. This was a bounded fresh reading, not a claim to reread the whole source or reprove its classification.

With the retained mirror-mix interpretation, the first-projection kernel is <κ> and occurs in both ends. Taking their full preimages gives the stated rotation intersection and full end intersection. Centrality of x follows from normality of a subgroup of order two. The relations (ab)^2=1 and a²b=a b^-1 a^-1 imply Brot^(q/2)=(x,x). Coordinate interchange then gives κ^r1=Brot^(q/2)κ, and the dihedral reflection relation gives Brot^r1=Brot^-1. Since κ is central in R, z=Brot^(q/4)κ centralizes C and has square Brot^(q/2), a nonidentity element. It is correctly allowed to have order four. It is not assumed to centralize G. Its nonmembership in C follows by taking first projections of κ=Brot^j. Thus the exact index-two, centralizing-defect interface is valid for every admitted parameter.

The coset degrees 2pr and free ranks p+r−1 give the three displayed table rows. A normal subgroup contained in C changes numerator and denominator of all relevant indices by the same factor, proving the stated obstruction to a parameter-independent bounded-degree *full* coset action by that particular quotient route. No Γ3/Γ4 torsion identity or broader nonexistence statement follows.

## 5. Independent finite checks and preservation controls

The new standard-library checker `phase96_universal_complement_review_check.py` imports no author graph, spanning-tree, elimination or phase92 code. It reconstructs the finite group and all right-coset partitions directly from the bound phase66 permutation model. A second case is generated independently from the four adjacent transpositions of S5. These are diagnostics of the exact conventions, not evidence substituting for a uniform proof.

| Case | Orders G / A / B / C / I | Edges | A/B vertices | Tree edges | Ordered square cells checked |
|---|---|---:|---|---:|---:|
| Bound Γ2 quotient | 1024, 128, 128, 8, 16 | 128 | 8 / 8 | 15 | 1024 |
| S5 control | 120, 24, 24, 6, 6 | 20 | 5 / 5 | 9 | 120 |

For both cases the checker verifies every endpoint, connectedness, an explicit spanning tree, both directions of the free-generator change, every square's path composition and tree-word telescope, and every defect's root-loop and tree-free expression. Deliberately reversing the first edge of each boundary is rejected in all cases. The program does not compute an amalgam kernel, infer a completion order, classify normal subgroups or prove a family theorem by sampling.

The optimized-Python run passed with explicit exceptions still active. A second invocation refuses to overwrite its output; a modified-copy manuscript hash is rejected before output creation. Every author and retained source binding checked before and after remained identical. The check report and controls are included in this review package. Replay to a fresh path:

```text
python3 -O research/leemans/phase96_universal_complement_review_check.py --output /private/tmp/NEW-phase96-incidence.json
```

## 6. Retained backgrounds, exports and admission

The complete phase83 theorem and its required conjugator erratum were read. Their reviewed mathematical scope is preserved. The present uniform bridge retains amalgam normal form and its tree, elementary covering-space and graph fundamental-group theory, van Kampen, free products, recursive string C-group recognition, and the explicitly listed primary family results and mirror conventions. No new acquisition or full reading of a classical topology/Bass–Serre reference is claimed.

The author export allowlist is exactly its three frozen bridge files. Primary captures, the exploratory phase90 programs and unfinished computations are outside it. The independent review manifest binds this report, its machine-readable counterpart, the fresh checker and its report, and preservation controls. Root review and public admission remain separate actions. Historical novelty has not been established, and no source-count, length-ratio, general minimal-cover, new formalization or additional-family torsion claim is made.
