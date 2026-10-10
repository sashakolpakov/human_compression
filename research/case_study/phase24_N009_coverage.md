# N009: complete principal-result coverage and a literal statement ledger

Private review candidate, 10 October 2026. This note closes the remaining presentation examples in Gomi–Loyola–De Las Peñas, *String C-groups of order 1024*, Contributions to Discrete Mathematics 13(1) (2018), 1–22, DOI [10.55016/ojs/cdm.v13i1.62475](https://doi.org/10.55016/ojs/cdm.v13i1.62475). The [primary PDF](https://cdm.ucalgary.ca/article/download/62475/46803) has been read completely across the source audits. Its printed page 10 was also inspected visually for the discrepancies below.

The combined packages recover the principal nondegenerate classification: 125 rank-three classes, 105 rank-four classes and eight rank-five classes, together with the unique rank-two dihedral marking, under the source's generator-set-preserving isomorphism convention, together with the named facets and universal orders in Table 6, the two exceptional presentations in Theorem 5.5, the central-extension mechanism, and the remaining finite examples. This is a proposed coverage conclusion subject to independent review, **not** an assertion that every printed sentence or table entry is correct. The literal ledger records the bottom boundary in Corollary 3.7 and three inconsistent right-hand sides in Table 4. No correction-priority or matched-length claim is made.

## 1. Common method and retained inputs

For a marked group write $G_I=\langle r_i:i\in I\rangle$. The actual intersection property (IP) is

\[
G_I\cap G_J=G_{I\cap J}
\]

for every pair of subsets. The group is always considered with its marking. A connected string diagram is a path, so its only possible marking permutations are the identity and reversal. Thus ordered counts are converted to the source convention by the reversal involution; an abstract-group isomorphism alone is insufficient.

The classification uses the following reusable components, whose existing proofs and certificates remain unchanged:

* [Central quotient and relator lifting](phase21_central_quotient.md): a safe central involution for every nondegenerate rank-three string 2-group, and a complete presentation order sandwich for its three possible lifting patterns.
* [The invariant normal-kernel ladder](phase21_kernel_ladder.md) and its [rank-three, excess-five application](phase22_N009_rank3.md): exhaustive normal kernels in a universal nilpotent path group, followed by actual IP and reversal tests. The source totals or presentations are not candidate filters.
* [Exact named-facet and universal-order comparison](phase22_N009_table_labels.md): all 107 Table 6 rows, with marked isomorphisms to the primary Atlas objects and complete coset enumerations for the 106 finite universal presentations. The one infinite universal group is a retained source theorem.
* [The two affine/Frattini adapters](phase22_N009_lemma_adapters.md) for Lemmas 5.2 and 5.4, and [the exceptional raw presentations](phase21_N009_presentations.md) for Theorem 5.5.

Retained mathematical inputs are stated rather than credited as new results: the Burnside basis theorem and elementary finite 2-group facts; standard dihedral and Coxeter facts; the lower-central/forest support theorem used to bound the census class; exact finite-group algorithms in GAP/NQ; and the following specifically quoted prior results in N009:

1. **Theorem 4.2**, the universal-presentation quotient principle, quoted from McMullen–Schulte. The computations below verify the required finite presentations and facet embeddings; they do not re-prove the general theory of abstract regular polytopes.
2. **Lemma 5.1**, the two square-lattice families of finite smooth quotients of ([4,4]), quoted from McMullen–Schulte.
3. **Theorem 5.3**, the infinite exceptional universal group's decomposition $(W_1\times W_2)\rtimes C_2^2$, with $W_i\cong[4,4]$, quoted from McMullen–Schulte's earlier work.

Lemmas 2.2–2.4 are retained instances of the usual string intersection criterion, attributed in N009 to Conder–Oliveros. Every finite check here tests *all* subset pairs directly, so those shortcuts are not hidden computational hypotheses. Primary Atlas permutations fix named objects; their inclusion is data attribution, not a claim that this project originally classified them. No SmallGroups catalogue is used for the new finite checks.

## 2. Short adapters for the remaining preliminary statements

### Endpoint cosets and the rank bound: Lemma 2.5

Let $a=r_0,b=r_1,H=G_{\{1,\ldots,d-1\}}$, and $m=|ab|$. Actual IP gives

\[
H\cap\langle a,b\rangle=\langle b\rangle.
\]

Two right cosets $H(ab)^i,H(ab)^j$, for $0\le i,j<m$, can agree only if $(ab)^{i-j}\in\langle b\rangle$. A dihedral rotation subgroup meets this reflection subgroup trivially. Hence $i=j$. Iterating the resulting index inequality yields

\[
|G|\ge2\prod_{i=0}^{d-2}|r_ir_{i+1}|.
\]

For a nondegenerate 2-group all adjacent orders are at least four. Order 1024 therefore forces $d\le5$. This proves both the coset assertion and the numerical exclusion of higher nondegenerate ranks; it does not rely on a search cutoff.

### The two quotient-IP adapters: Lemmas 3.1–3.2

Let $L=\langle a,b\rangle,R=\langle b,c\rangle$, with actual rank-three IP, and let $\pi:G\to G/N$ be the quotient by a normal subgroup.

If $N\cap RL=1$, both facets embed. If $\pi(l)=\pi(r)$, then $r^{-1}l\in N\cap RL$, so $l=r\in L\cap R=\langle b\rangle$. The rank-three criterion gives IP in the quotient, and the adjacent orders are unchanged. This is Lemma 3.1, without an assumption that $N$ is central.

If instead $N\le L$ and $L/N$ remains rank two with the **displayed images** of $a,b$, then $N\cap R\le L\cap R=\langle b\rangle$, and $b\notin N$; thus $R$ embeds. Since $LN=L$, the preimage calculation gives

\[
\pi(L)\cap\pi(R)=\pi(L\cap R)=\langle\pi(b)\rangle.
\]

This proves Lemma 3.2; the case $N\le R$ is symmetric. The qualification on the displayed marking is essential: it is not enough for an abstract quotient to admit an unrelated C-group marking.

The coordinate characters in Lemma 2.8 are the coordinate linear functionals on the Frattini quotient: a minimal generating list of a finite 2-group maps to a basis of $G/\Phi(G)$. The smooth Coxeter map in Theorem 2.7 follows by sending each Coxeter generator to the marked involution and using the stipulated adjacent orders. These are elementary adapters retaining the standard Frattini and Coxeter inputs.

A disconnected string diagram gives commuting component subgroups. Actual IP makes each component meet the subgroup generated by the others trivially, so multiplication identifies $G$ with their direct product. This covers the source's preliminary reduction to nondegenerate markings. It does not add a separate enumeration of all degenerate products to the principal census.

## 3. Exact finite-presentation verification

[The GAP checker](phase24_N009_examples_check.g) passes the raw defining relators to a **complete Todd–Coxeter coset enumeration at the trivial subgroup**. For every resulting table it checks that the induced regular permutation group has exactly the table index, that the specified marked involutions generate the entire group, that every relator holds, and that every one of the $4^d$ marked subgroup intersections is correct. Consequently the recorded order is the order of the raw finitely presented group, not merely an order of a nilpotent quotient.

Generator-preserving isomorphisms identify the objects and distinguish the eight order-1024 type-$\{4,8\}$ markings. Each of those eight is also matched, individually and bijectively, to a saved witness from the independent unfiltered rank-three census. That last adapter reconstructs the census's class-seven universal group with NQ; it is not used to establish any raw-presentation order. Its binary pc-coordinate guard and source hashes are recorded by the runner.

The new execution covers **34 raw presentations and 3,328 actual IP meets**: 28 rank-three presentations and six rank-four presentations. It also certifies five primary Atlas order-512 labels and ten exact facet identities. The [run report](phase24_N009_examples_run.json) records the software, executable inputs and output hashes. The mathematical data include a data-only extraction from five primary Atlas pages; no downloaded GAP code is executed.

### Example 3.9 and Tables 2–3

Use $a,b,c$ for the three marked involutions. Let $R_1,R_2$ denote the two additional words in a Table 2 row; their exact letter arrays are in the checker. The four raw Table 2 presentations each have order 512, are pairwise inequivalent as ordered markings, and agree with their named Atlas objects.

Class I would require an order-512 quotient of the type-$\{2,8\}$ Coxeter group, which has order 32. Thus it contributes nothing. Class II starts with the type-$\{4,4\}$ order-512 group, fixes $\tau=(bc)^4$, and chooses $(abcb)^8=1$ or $\tau$; these are the two distinct order-1024 groups labelled $a,b$ in the source. Here and below $\tau$ is constrained to be a central element of order dividing two.

For each Table 2 row, all three Class III choices

\[
(R_1,R_2)=(\tau,1),(1,\tau),(\tau,\tau)
\]

are checked. Quotienting each result by the actual subgroup generated by $\tau$ recovers exactly that Table 2 marking. The outcomes reproduce all twelve Table 3 entries:

| Base label | $(\tau,1)$ | $(1,\tau)$ | $(\tau,\tau)$ |
|---|---|---|---|
| $512a$ | $1024c$ | $1024d$ | $1024e$ |
| $512b$ | $1024a$ | $1024c$ | $1024f$ |
| $512c$ | $1024c$ | $1024g$ | $1024h$ |
| $512d$ | $512d$ | $1024a$ | $512d$ |

In the two order-512 outcomes, the putative kernel generator $\tau$ is the identity. This illustrates why the relator-lift theorem still requires exact order and IP checks.

### Literal Table 4 and the three right-hand sides

The checker separately preserves the printed relations of every Table 4 row. Its exact marked-isomorphism result is

\[
(a,b,c,d,e,f,g,h)_{\rm printed}
\longmapsto(a,b,c,d,c,a,g,c)_{\rm Table\,3}.
\]

Thus the rows labelled $e,f,h$ do not define the distinct groups assigned those labels in Table 3. In each of these three rows, replace the right-hand side **1 of the second displayed additional relation by $\tau$**. The resulting presentations are precisely the already checked $(\tau,\tau)$ lifts of Table 2 rows $a,b,c$, respectively. No change to the group count, Table 3 or the other five Table 4 rows is needed.

This conclusion is about the literal 2018 PDF: the page was checked visually, so the discrepancy is not an OCR inference. It does not assert that these transcription issues were previously unknown. The [machine-readable literal map](phase24_N009_table4_literal_matches.json) keeps the printed and corrected objects distinct.

## 4. Examples 4.3–4.5 and universality

The complete raw presentations have the following results. Facet identities are ordered marked isomorphisms, not order-only matches.

| Source object | Raw order | Type | Ordered facets |
|---|---:|---|---|
| Example 4.3 universal group | 512 | $\{4,4,4\}$ | $\{4,4\}*32, \{4,4\}*128$ |
| Example 4.4 universal group | 1024 | $\{4,4,4\}$ | $\{4,4\}*32, \{4,4\}*256$ |
| Example 4.5 universal group | 2048 | $\{4,4,8\}$ | $\{4,4\}*64, \{4,8\}*128a$ |
| Example 4.5, first central quotient | 1024 | $\{4,4,8\}$ | the same $64,128a$ facets |
| Example 4.5, second central quotient | 1024 | $\{4,4,8\}$ | the same $64,128a$ facets |
| Example 4.5, third central quotient | 1024 | $\{4,4,4\}$ | not a smooth quotient of type $\{4,4,8\}$ |

The five named facet presentations are complete presentations from the earlier raw Atlas check. Their extra words are the same as the source words, up to cyclic conjugation; for the $\{4,8\}*128a$ relation the Atlas word moves the final letter of the source word to the beginning. Consequently the combined presentations are exactly the universal presentations in Definition 4.1. The finite groups have actual IP and embed both intended facets, so Theorem 4.2 applies. Example 4.3 cannot have an order-1024 quotient, and Example 4.4 is itself the unique such quotient of its universal group.

For Example 4.5 the checker evaluates the three printed central-involution words and independently enumerates **all** central involutions, obtaining exactly the same three-element set. Each added word is then treated as a new raw relator and its quotient presentation is independently enumerated. The first two quotients are distinct marked groups, have unchanged type and facets, and the third has final adjacent order four.

Every normal subgroup of order two is central. Since the universal group has order 2048, any order-1024 quotient has such a kernel. Therefore this list of three kernels is exhaustive, and exactly the first two give the prescribed smooth class. These are the source's labels $\{4,4,8\}*1024e,f$. This conclusion does not extrapolate the central-kernel argument to larger kernels.

## 5. Every numbered item and table

The detailed, source-page-bound record is [phase24_N009_coverage.json](phase24_N009_coverage.json). It has one record for **each of the 27 numbered items**, including definitions and examples; one for each of Tables 1–6; and separate preliminary/conclusion scope records. It distinguishes definitions, retained prior results, reproduced statements, corrected boundaries and computationally diagnosed discrepancies.

| Source items | Coverage |
|---|---|
| Definitions 2.1, 2.6, 4.1 | Adopted marking, equivalence and universal-presentation conventions. |
| Lemmas 2.2–2.4 | Retained standard string-IP criterion; finite certificates test full IP directly. |
| Lemma 2.5; Theorem 2.7; Lemma 2.8 | Section 2 and the elementary presentation/Frattini adapters. |
| Lemmas 3.1–3.2 | Section 2 quotient-IP arguments, with the displayed quotient marking explicit. |
| Corollary 3.3; Lemmas 3.4–3.5; Theorem 3.6 | Reviewed central-quotient note. Lemma 3.4(iii) also follows from the stronger exclusion proved for Lemma 3.5. |
| Corollary 3.7 | Correct with the order-eight terminal boundary: iterate down to $C_2^3$, not to a rank-three group of order four. Literal unrestricted wording is not asserted. |
| Theorem 3.8; Table 1 | Complete three-case relator-lift order sandwich, retaining a complete base presentation. |
| Example 3.9; Tables 2–3 | All raw base/lift cases, exact labels, collapsed kernels and census comparison checked above. |
| Table 4 | All printed presentations checked; three right-hand sides diagnosed and corrected as specified above. |
| Theorem 4.2 | Explicitly retained quoted universal-group input. |
| Examples 4.3–4.5 | Complete raw orders, actual IP, exact facets and exhaustive order-two quotient kernels checked above. |
| Table 5 | Complete unfiltered rank-three order-1024 census; every type count matches. |
| Table 6 | All 107 rows, named facets, 106 finite universal orders, retained exceptional infinite case, and exact per-row counts. The earlier orientation caveat remains explicit. |
| Lemma 5.1 | Explicitly retained quoted square-lattice classification. |
| Lemma 5.2 | Uniform lattice/faithful-action proof with its small-parameter boundaries and exact finite checks. |
| Theorem 5.3 | Explicitly retained quoted infinite semidirect decomposition. |
| Lemma 5.4 | Uniform Frattini-character proof conditional on that decomposition. |
| Theorem 5.5 | Two raw finite presentations, exact named facets and exhaustive matching census subfamily. |

The principal-result conclusion concerns the stated nondegenerate classification and its constructive mechanisms. It does not re-run the original authors' GAP session, establish novelty for a correction, prove the three quoted prior inputs, or address the concluding suggestion to investigate geometric realizations. No assertion of an entirely correct literal document, zero retained input, or whole-paper compression ratio follows from this ledger.

## 6. Reproduction and provenance

From a directory containing this package and its retained data files:

```sh
python3 phase24_N009_examples_run.py --gap gap --output-dir /tmp/N009-phase24-review
```

The runner copies its four mathematical inputs to a fresh temporary directory, runs the checker and requires its complete terminal PASS marker. It saves the log, five result files and a hash-bound report in the requested directory. Re-running does not mutate the frozen inputs. The only nonstandard execution dependencies are GAP and NQ. The retained `phase22_N009_atlas_library.g` and `phase22_N009_rank3.accepted.json` are required and explicitly hashed.

Re-extracting the five new Atlas objects is an optional provenance operation using `phase24_N009_atlas_extract.py`, BeautifulSoup and the private primary snapshots. It is unnecessary for the mathematical replay. The extractor accepts only numeric cycle and word data, requires disjoint displayed cycles, and never evaluates downloaded program text. Primary PDFs, extracted article text, raw Atlas HTML and source-page images are excluded from export; their URLs and hashes remain in the metadata.

The source PDF SHA256 is `0618a57cb5ff35c13587877818a2e77bce442cf2c561f204b6d5e5e095fa2fda`; the saved extraction SHA256 is `091caf4266f2ac595aec76def47d451700fff7c80f6d0f3eabeee2e6f31f38e7`. Independent review records are separate from this authored coverage note. The package itself creates no registry promotion.
