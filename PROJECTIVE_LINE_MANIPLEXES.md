# Centralizer extensions of projective-line maniplexes

**Topic E has a third complete application: the principal PSL₂ results of
Leemans and Toledo's 2023 maniplex paper.** The
[nine-page paper](research/case_study/phase258_projective_maniplexes.pdf)
([complete text](research/case_study/phase258_projective_maniplexes.md))
uses the full [Topic E umbrella](PROJECTIVE_LINE_POLYTOPES.md), proves the
additional interface needed when the intersection property is absent, and
recovers the source's two infinite families for their full stated ranges.

| Intake: May 15, 2023 author edition, L021 | Complete result recovered |
|---|---|
| Rank restriction and Theorem 3.10 | Rank at most four for every prime power; no rank-four example in characteristic two; each rank-three end is S₄, A₅ or the whole group. |
| Proposition 4.2 | With both ends proper, exactly the marked 11-cell and 57-cell, including uniqueness, intersection property and stated geometry. |
| Theorem 4.4 | Every source map satisfying the odd-divisor torus condition extends with the same PSL₂(q) group. |
| Lemma 4.5 and Corollary 4.6 | Both ends are PSL₂(p) for every prime p ≡ 1 modulo 12; infinitely many nonorientable examples. |
| Proposition 4.7 and Corollary 4.8 | A₅/full-PSL₂(p) for every prime p ≡ ±1 modulo 20, p ≠ 19; infinitely many nonorientable examples. |

The [contract](research/case_study/phase258_contract.json) and
[32-row source ledger](research/case_study/phase258_source_ledger.json)
identify each claim, its proof and retained inputs. The primary is the
[eleven-page author manuscript](https://dipot.ulb.ac.be/dspace/bitstream/2013/359689/3/projectivemaniplexes_final.pdf),
read in full. The source's separate PGL conjecture has its own
[proof and question record](PGL_MANIPLEX_FAMILIES.md). This application adds
one principal-source recovery and no question entry.

## What is reused and what the application adds

The umbrella proves that the common centralizer of two noncommuting
projective involutions has at most one nonidentity element and descends to
their field. This gives the rank and proper-end restrictions without an
intersection-property assumption. The application independently checks all
432 rank-three string markings of S₄ and A₅ and proves they do satisfy that
property. Only then can the umbrella's ten exact universal presentations
classify the two-proper-end case.

The extension argument takes the half-turn of an even cyclic torus. Its
centralizer and distinctness properties provide the new marker. The
application checks generation and the opposite end, not only the local
relations. The source's constant matrices are preserved up to an explicit
change of basis. The rank restrictions, two source families and construction
idea retain their original attribution. Dickson's classification, Giudici's
exact maximal-subgroup cases, cyclic tori, Dirichlet and the Suzuki
fixed-point theorem are explicit retained inputs.

## Corrections to the bound source edition

- The introduction and conclusion omit S₄ as a single proper end. The paper
  proves an additional infinite S₄/full-PSL₂(p) family for every prime
  p ≡ ±1 modulo 24. Its explicit PSL₂(23) example has type {3,4,12}, one
  vertex and 253 facets.
- The concluding assertion that no Class 1 example is self-dual is false.
  An explicit PSL₂(13) marking of type {3,7,3} has both ends full and an
  actual conjugator reversing all four generators. The face-count
  obstruction applies to Class 2.
- The blanket maximality claim for involution centralizers fails already
  in PSL₂(5) ≅ A₅: a centralizer of order four lies in A₄. The displayed
  source formula also needs its characteristic qualification.
- Source Lemmas 3.7–3.8 require **natural subfield embeddings**, not merely
  abstract isomorphism to a smaller projective group. Otherwise A₅ ≅ PSL₂(5)
  and S₄ ≅ PGL₂(3) contradict their literal statements. The replacement
  proves the qualified exclusions explicitly.
- The {5,3} facets are hemi-dodecahedral, consistently with the marking;
  the source later calls them hemi-icosahedral.

The [independent review](research/case_study/phase263_review.md) records these
qualifications. They are corrections to this exact edition, with no
historical-priority or additional solved-question claim. Unneeded blanket
uniqueness clauses are not retained. A full census of every rank-four PSL
marking is outside this principal contract.

## Verification and cost

The complete proof received independent agent review and root review;
external peer review is not claimed. The independent Python implementation
checks all 27,648 subset intersections for the 432 local markings and both
literal correction witnesses. Separate native group constructions check
four further prime cases and extensions over fields of orders 25 and 49.
The [fresh public replay](research/case_study/phase264_public_replay/report.json)
also reruns all ten shared universal presentations and rejects altered data.

[StringCentralizerBridge.lean](research/case_study/formal/StringCentralizerBridge.lean)
proves three actual general statements: commutation extends from generators,
the first pair cannot commute in a centre-free string marking, and the
common-centralizer condition bounds the rank by four. Two earlier
characteristic-two interface declarations are replayed separately. The
[formal scope](research/case_study/formal/StringCentralizerBridge.scope.md)
keeps projective classification, finite presentation orders, torus existence
and the complete families outside Lean. GAP algorithms and the retained
classical theorems remain explicit dependencies.

The full U_E and shared program remain chargeable, alongside this complete
application and its new programs. The [Topic E measurement](TOPIC_E_MEASUREMENT.md)
is the frozen **two-application baseline** for E₁ and E₂. It excludes E₃;
no three-application factor or new sawtooth measurement is claimed here.

Use a fresh output directory:

```sh
python3 -B -O research/case_study/phase264_check.py \
  --out /tmp/NEW-PSL-maniplex-review \
  --gap GAP --lean LEAN --packages PACKAGES
```

The [admission record](provenance/phase129_review.md) binds the frozen proof
and review packets. Primary PDFs, extracted source text and images are
referenced by hash and acquisition link, and are not redistributed.
