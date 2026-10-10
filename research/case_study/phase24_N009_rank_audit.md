# Independent audit of the N009 completion and statement ledger

10 October 2026. **PASS, with the retained-input and literal-source boundaries below.** I reviewed the frozen [coverage note](phase24_N009_coverage.md), the complete 27-item [numbered ledger](phase24_N009_coverage.json), the raw-presentation checker, and its transport to the prior census. No mathematical gap was found. The combined packages support credit for reproducing N009's principal nondegenerate classification and its stated constructive mechanisms. They do not support a claim that every literal printed statement is true, that no prior theorem is retained, or that a whole-paper proof-length compression ratio has been measured.

The reviewed note has SHA256 `1d496637805873209448b2f6931e5a6a56ad2ec53870e32ae58dd8d0d49e3eeb`; the author manifest has SHA256 `6bb4948a8711beccef5b5ab6b09ff0b797f2dc3c143a4a8425b457440a4cfd48`. Exact review and execution bindings are in the companion audit JSON.

## Literal Table 4 and the proposed repairs

I independently rendered and inspected printed p.10 of the [primary 2018 PDF](https://cdm.ucalgary.ca/article/download/62475/46803), including Tables 2, 3 and 4. Each of Table 4's rows labelled `e`, `f` and `h` prints the identity on the right of its second additional relation. In particular, rows `c` and `e` are literally identical presentations once the common Coxeter and central-kernel relations are included. This is visible in the page image and is not an OCR inference.

The checker transcribes the full Table 2 words correctly. It constructs all twelve Table 3 lifts, with the actual auxiliary generator constrained to be central and of order dividing two. The first three base rows have three order-1024 outcomes each, while the first and third lifts of the fourth base row collapse the auxiliary generator and retain order 512. Exact generator-preserving maps reproduce the Table 3 labels and distinguish all eight order-1024 target markings. Each of the eight is also matched uniquely to one of the eight unfiltered census kernels of ordered type `{4,8}`.

The separately encoded literal Table 4 presentations have marked-label map

\[
(a,b,c,d,e,f,g,h)\longmapsto(a,b,c,d,c,a,g,c).
\]

Thus `e`, `f` and `h` do not define the distinct objects assigned those names by Table 3. Changing the second right-hand side in each of those three rows from the identity to `tau` gives exactly the already verified `(tau,tau)` lifts of base rows `a`, `b` and `c`, respectively. This is a specific, verified repair consistent with Table 3. It is not a claim of unique possible editorial repair, authorial intent, or correction priority. The original and repaired presentations remain separate in the evidence.

## Raw orders, actual IP and the remaining examples

I inspected `Build24` and the complete checker. A complete Todd–Coxeter table at the trivial subgroup gives a finite presentation order; the script then constructs the coset-action permutation group, checks its order equals that index, verifies the raw relators, and checks that the displayed marked generators generate the entire group. It tests every pair of marked subgroups directly. Hence the order statements are not just orders of NQ images, and the auxiliary central symbol cannot silently produce an extra direct factor outside the marking.

Fresh execution reproduced all **34 raw presentations and 3,328 actual-IP comparisons**. All five generated mathematical JSON outputs were byte-identical to the author's saved outputs. The new primary-data check independently parsed the five Atlas canonical names, composed their 15 permutations from the displayed cycles, checked the literal relator words, and matched every numerical GAP record to its JSON entry. No downloaded program text was executed.

The Example 4.3, 4.4 and 4.5 words match the source statements on pp.12–14, including the three displayed central-involution words in Example 4.5. Their raw universal orders are respectively 512, 1024 and 2048; the facet identities are exact marked isomorphisms to the named objects. The source facet presentations agree with the complete Atlas presentations up to cyclic conjugation of a defining word, which leaves its normal closure unchanged.

For Example 4.5, the three printed words form the entire set of central involutions of the computed universal group. The three independently enumerated raw quotient presentations have order 1024. Two preserve type `{4,4,8}` and the exact facets, and are distinct as marked groups; the third has type `{4,4,4}`. Any order-1024 quotient of this order-2048 group has a normal kernel of order two, and any such subgroup is central. The three-kernel enumeration is therefore exhaustive. This reasoning is specific to kernels of order two and is not being extended to arbitrary normal kernels.

## Numbered coverage and principal-result assessment

I compared the ledger with all 27 numbered source items and all six tables. I also reread the written central-quotient/relator-lift adapter and the affine-center/Frattini adapter. Their arguments support the recorded uniform claims: the dihedral product normal form and Frattini argument exclude the unwanted central candidate; actual facet intersections justify the safe central quotient; a complete base presentation gives the relator-lift order sandwich; the affine models give the stated center formulas with their small-parameter cases; and the two Frattini characters locate the exceptional quotient kernel inside the retained product factor.

The new endpoint-coset argument proves the source order bound directly from actual IP. For nondegenerate 2-groups it excludes rank at least six at order 1024. Thus the absence of higher ranks is a theorem, not a finite search cutoff. The recorded rank-three, rank-four and rank-five classifications have respectively 125, 105 and eight classes under the source's generator-set convention. The unique rank-two dihedral marking is explicitly recorded as well. Ordered marked counts are passed to this convention using the path reversal, not abstract-group isomorphism.

The earlier unfiltered kernel censuses supply completeness. The independently reviewed Table 6 adapter supplies all 107 named rows and all 106 finite universal orders. The exceptional two presentations and their exhaustive source subfamily were checked in the earlier phase21 package. The present raw checks close the remaining example and presentation-label obligations; agreement of the three total counts alone would not have done so.

The ledger correctly distinguishes the following boundaries:

* Definitions are adopted, not presented as newly proved results.
* The standard string-IP criteria in Lemmas 2.2–2.4, and the quoted Theorem 4.2, Lemma 5.1 and Theorem 5.3, remain explicit prior inputs. The infinite exceptional decomposition is not inferred from a computation.
* The literal unrestricted Corollary 3.7 fails at the order-eight endpoint: a rank-three marking cannot survive in a group of order four. The valid iteration stops at `C2^3`; the ledger claims this corrected scope.
* Lemma 3.2 uses the displayed images as the rank-two quotient marking. Lemma 5.2 does not acquire an unstated extra parameter case. Table 6 retains the previously recorded dual-orientation interpretation for four printed labels.
* Table 4's three inconsistent right-hand sides are diagnosed explicitly rather than counted as successful literal reproduction. The geometric-realization direction and a separate enumeration of all degenerate products remain outside the principal target.

With those qualifications, **principal-result coverage is justified**. This is a review recommendation about the precise stated classification and its mechanisms; it does not itself edit the registry or grant whole-document validity. The proof ingredients, exact computational algorithms, prior classification inputs, and primary named-object data remain part of the cost and trust boundary.

## Reproduction and review limits

[The independent replay](phase24_N009_rank_audit.py) verifies all 17 original manifest bindings and ten retained dependency bindings, checks the complete numbered/table index and every evidence path, and reruns the unchanged author checker in a disposable directory. With the private source snapshots available, run:

```sh
python3 phase24_N009_rank_audit.py --primary-sources --output fresh-review.json
```

Omit `--primary-sources` for a replay using only the original mathematical artifacts. GAP is selected by `GAP`, `PATH`, or `--gap`. The [fresh report](phase24_N009_rank_audit.run.json) binds the exact executable/input bytes, complete output, five reproduced data files, and optional primary-data checks.

This audit combines a mathematical and source review, independent literal-data parsing, and fresh execution of the author's finite verification. It does not claim a newly implemented independent group census, fresh execution of every prior package, proof-assistant verification of N009, priority for any correction, or a quantitative proof-compression measurement. Author files and frozen public artifacts were not modified.
