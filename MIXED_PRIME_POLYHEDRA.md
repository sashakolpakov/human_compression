# Affine periods and mixed-prime polyhedra

The [nine-page application](research/case_study/phase250_mixed_prime_application.pdf)
([readable source](research/case_study/phase250_mixed_prime_application.md))
recovers the specified principal results of Hou, Feng and Leemans,
*Regular 3-polytopes of order* $2^n p$. It uses a separate
[five-page affine theory paper](research/case_study/phase250_affine_lattice_umbrella.pdf)
([readable source](research/case_study/phase250_affine_lattice_umbrella.md)),
the supported extensions of [Topic A](TOPIC_A.md), and the previously
proved cubic $\{6,6\}$ component. The
[independent review](research/case_study/phase254_review.md) accepts the
complete declared principal contract, with an explicit source correction.

The source edition is [arXiv:2001.02945v2](https://arxiv.org/abs/2001.02945v2),
14 July 2024, seventeen pages. The later journal edition has not been
collated. The original results remain attributed to their authors.

| Source results | Complete recovery | Required inputs and qualifications |
|---|---|---|
| Theorems 1.2 and 3.1 | The full type restriction for groups of order $2^n p$, including the stronger algebraic statement with generators of order at most two | Burnside solvability and elementary finite-group structure are retained |
| Theorem 4.1 and Corollary 4.2 | The exact odd-factor presentations, orders, types, intersection property and solvability for all stated parameters | The complete supported-extension and square-group arguments from Topic A are used |
| Theorem 1.3 | For $n\ge7$, type $\{6,2^s\}$ and order $3\cdot2^n$ occur exactly when $2\le s\le n-2$ and $s\ne n-3$ | Corrected extension presentations; the actual exceptional seed; Lucchini's cyclic-core bound; a complete order-384 catalogue exclusion |
| Theorem 4.3 and Corollary 4.4 | All three $\{6,4\}$ families, of orders $96m^3$, $192m^3$, $384m^3$, and the stated power-of-two specialization | Exact abstract kernel and integral period lattices; valid for every $m\ge1$ |
| Theorem 5.1 and Corollary 5.2 | All three $\{6,6\}$ families, of orders $192m^3$, $384m^3$, $768m^3$, and the stated specialization | Reuses the complete earlier cubic proof and its programs; this component earns no second source credit |

## The reusable argument

For an affine group, the finite group of linear parts does not by itself
determine the marked quotient. The theory paper separates three tasks:
prove the abstract presentation kernel is free abelian, compute its actual
translation lattice, and compare lifts of common elements of adjacent
subgroups. Normalized Schreier transitions give the lattice. Invariant
period sublattices then give the exact quotient orders, while finitely
many translation differences control intersection for every period.

The application combines that criterion with supported cyclic
extensions. The existence statements follow from uniform constructions;
Lucchini's original cyclic-core bound reduces the missing existence case
to a finite base. The base computation exhausts all 20,169 groups of
order 384 in SmallGroups 1.5.4. Catalogue completeness and GAP's exact
presentation algorithms remain retained inputs.

**[B] Earlier mathematics.** Hou–Feng–Leemans supply the principal
results and source presentations. Burnside's theorem, Lucchini's 1998
proposition, classical Schreier theory and the group–polytope
correspondence retain their attribution. The earlier repository umbrella
and cubic proof are reused with their complete dependencies.

**[I] Replacement organization.** The affine criterion and common
extension interface expose the repeated kernel, lattice and intersection
arguments. The [33-row ledger](research/case_study/phase250_source_ledger.json)
locates every promised source clause in fourteen complete proof spans.
No historical priority claim is made for this organization.

**[E] Source correction.** The first period equality in the first branch
of the bound source's Lemma 4.5 needs exponent $-2M$, rather than $+2M$.
The literal pair of positive signs forces an extra rotation relation.
At $n=10,s=4$, its group has order 1536 and rotation order eight; the
corrected construction has order 3072 and rotation order sixteen.
The uniform corrected construction supplies the main theorem. This is
an edition-specific correction, not a new open-question result.

Independent review also repaired the first draft's unnormalized
Schreier formula and made the affine intersection criterion's
nondegeneracy hypotheses explicit before the author freeze. The accepted
manuscripts and the unchanged historical cubic program have the required
proofs of these conditions.

## Verification and costs

The [fresh public replay](research/case_study/phase259_replay/report.json)
runs both exact abstract-kernel calculations, the complete finite base
search and the finite source-presentation checks. An independently
written program verifies eighteen affine quotients and all 64 subset
intersections for each. Six independently transcribed presentations
check the odd-factor construction, including composite, noncoprime
factors. Relevant false weakenings and bad quotients are rejected.

Lean verifies [three general period-word and sign declarations](research/case_study/formal/PeriodSignObstruction.scope.md).
It does not verify the full positive classification or the catalogue.
The [publication record](provenance/phase127_review.md) distinguishes the
fresh computation from the independent full mathematical and source review.

The seventeen source pages, five theory pages and nine application pages
are an inventory, **not a compression ratio**. A matched comparison must
also charge the full retained Topic A umbrella, cubic proof, required
programs and other dependencies under the stated topic-cost policy. The
general classification problem, full source Table 1 census and ancillary
seed-uniqueness assertion are outside this principal contract. A larger
multi-application topic built from this affine theory remains unfinished.

From the repository root, use local tool paths and a fresh output directory:

```sh
python3 -B -O research/case_study/phase259_check.py \
  --out /tmp/NEW-mixed-prime-check \
  --gap GAP --lean LEAN_4_32_2 --packages PINNED_PACKAGES
```

This public adapter preserves the frozen author and reviewer programs.
It reruns their mathematical checks without requiring redistributed
primary files. The original full-source review remains separately bound.
The sole omitted review export is a cached `.olean` build product, rebuilt
from source in the fresh replay. Frozen pending-review headers record
their historical stage; the later review and admission establish acceptance.
