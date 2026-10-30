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
The [current accepted intersection and census results](october_corpus/research/proof_collection/updates/verified_intake_results/accepted_intake_progress_checkpoint_11518/README.rst)
record 880 additional F004 exclusions and F009 checkpoint 11,518. October
has 101 complete reviewed treatments out of 104 mathematical originals.
The unchanged Fi22 ledger concerns one of 105 selectors; the full class
count remains unproved here.
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
