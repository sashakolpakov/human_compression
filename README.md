# Human Compression

Can a few reusable mathematical ideas, developed with a strong language model
and agents, recover decades of published results in shorter, complete papers?
This project tests that question across separate research corpora. Its products
are mathematical theories, application papers, computational certificates and
Lean proofs, with explicit attribution and measured comparisons.

This README introduces the whole project. Each corpus has its own README for
its bibliography, mathematical results, progress and reproduction instructions.

## Corpora

| Corpus | Subject and status | Start here |
|---|---|---|
| **October** | Finite groups, polytopes and incidence geometry, drawn from work by Dimitri Leemans and collaborators. The existing project corpus, including its manuscripts, proofs, certificates and audits. | [Corpus overview](october_corpus/README.md) · [Detailed programme](october_corpus/README.rst) |
| **November** | A separate corpus from another researcher. The directory is prepared; its researcher, bibliography and source editions have not yet been registered. | [Corpus overview](november_corpus/README.md) |

Each corpus keeps its manuscripts, source register, evidence and reproduction
instructions in its own directory as they are added:

```text
human_compression/
├── README.md             Project purpose and principles shared by both corpora
├── corpora.json          Corpus register and entry points
├── october_corpus/
│   └── README.md         Leemans and collaborators: results, status and reproduction
└── november_corpus/
    └── README.md         Second corpus: scope and status
```

Adding a corpus does not change the scope or results of the others. The
[corpus register](corpora.json) records their entry points.

## What compression means

A topic has common theory **U** and complete application papers **A₁, A₂, …**
that recover the specified results of historical manuscripts **L₁, L₂, …**.
We report both:

- **Whole-topic compression:** `(c(L₁) + c(L₂) + …) / (c(U) + c(A₁) + c(A₂) + …)`.
- **Application compression after acquiring U:** `c(Lᵢ) / c(Aᵢ)`.

Every topic pays for its full common theory once, even when it overlaps another
topic's theory. Required local proofs and appendices count. A comparison must
state its cost measure, match the results proved and treat validation programs
symmetrically. A shorter account earns credit only when its stated results
follow from complete proofs. Paper counts alone are not compression ratios.

Attribution separates earlier ideas and borrowed theorems from contributions
made here. Answers to open questions and corrections to published claims have
their own records, separate from compression measurements. A verified lemma
does not imply that its entire manuscript has been formalized.

## Read and reproduce

For the October corpus, begin with its [current reproduction instructions](october_corpus/REPRODUCING.md).
October has **101 complete reviewed treatments out of 104 mathematical originals**.
F004, F009 and L026 remain unfinished. The [current intake status](october_corpus/INTAKE_STATUS.json)
records F004 job 24 at **3,397 additional exclusions**: 3,124 failures of the
intersection property and 273 nongenerating quartets, with **209 positions
unresolved**. Its original 173 paid positions are separate.

The [portable matrix certificates](october_corpus/reproduction/matrix_certificates/README.rst)
cover **2,308 exclusions**: 2,035 intersection failures and all 273
nongeneration certificates. The expanded guarded replay passed in 2.915 seconds,
using Python's standard library, 1,391,673 charged input bytes and 145,447
matrix products. Its observed peak memory was 62,291,968 bytes.
The [historical 1,089-case archive](october_corpus/research/proof_collection/updates/verified_intake_results/accepted_intake_progress_f004_1089/README.rst)
preserves the other exclusions. Earlier replay editions remain in Git history,
and every earlier case is retained in the current package. These exclusions
do not complete the positive classification or recover the manuscript.
The [prefix centralizer calculations](october_corpus/reproduction/prefix_centralizers/README.rst)
cover the 157 q11 prefixes pending before the polynomial closures below. One common argument excludes both
parabolic types for 81 prefixes, under the stated model, bank and Levi premises.
These support calculations add no completed job or manuscript.
The [polynomial certificates](october_corpus/reproduction/polynomial_prefixes/README.rst)
give ten whole-prefix exclusions by one common theorem. Their guarded replay
passed all ten identities and exact-order checks. F004 now has **125 of 272
q11 jobs complete, with 147 pending**; the manuscript remains unfinished.

F009 is locally accepted at checkpoint **11,584**, with one reserved debt among
193 pending families. The continuation completed 25 families and refined five;
the full census remains unfinished. The [public checkpoint 11,584 archive](october_corpus/research/proof_collection/updates/verified_intake_results/census_checkpoint_11584/README.rst)
preserves the accepted records, selected programs and computation outputs.
Its relative checker verifies archived byte integrity; fresh mathematical
Reader replay from a clone remains outstanding. The Fi22 ledger has **65 generation
certificates, 65 separate intersection proofs for those cases and 96
nongeneration certificates**. The earlier archive and the new
[24-case replay](october_corpus/reproduction/fi22_markings/README.rst)
together reproduce all 65/65/96 certificates.
The ledger concerns one of 105 selectors; the full class count remains unproved here.

The [earlier archived intake results](october_corpus/research/proof_collection/updates/verified_intake_results/README.rst)
preserve the accepted census checkpoint, classification records and generation
and exclusion certificates, with their verification scope and attribution.
The [latest finite certificate report](october_corpus/research/proof_collection/RUN_REPORT.rst)
records the completed relative replay, its inputs, results and remaining premises.
The [evidence supplement](october_corpus/research/proof_collection/supplement/RUN_REPORT.rst)
preserves additional accepted certificates and the current intake record.
The [later certificates and finite search](october_corpus/research/proof_collection/updates/literal132_cycles/PUBLICATION.rst)
record the next 132 adopted results, their checks and the remaining work.
The [Fi22 exclusions](october_corpus/research/proof_collection/updates/fi22_invariant_subsets/PUBLICATION.rst)
record twelve verified nongeneration certificates and the updated intake overview.
The [Fi22 generation certificates](october_corpus/research/proof_collection/updates/fi22_generation_certificates/PUBLICATION.rst)
add a further exclusion and three generating markings, with their intersection
property derived separately from an existing theorem.
From the repository root, check the directory migration and run the small
mathematical suite with:

```sh
python3 -E -B scripts/check_corpus_layout.py
cd october_corpus
python3 -E -B scripts/smoke_check.py --quick
```

Run the layout check from a clean, committed checkout. It verifies preservation
of the earlier Git tree. The quick suite
checks three selected mathematical certificates. Each paper's guide states the
additional inputs, tools and verification scope needed for its reproduction.
Historical audits retain their original paths and can be replayed at their
recorded commits.
