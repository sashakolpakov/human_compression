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

The [October overview](october_corpus/README.md) records **101 complete reviewed
treatments out of 104 mathematical originals**. F004, F009 and L026 remain.
Its [intake status](october_corpus/INTAKE_STATUS.json) distinguishes accepted
partial results from completed manuscripts. Measurements remain at 53
applications across 19 topics while intake finishes.

The [November directory](november_corpus/README.md) is prepared. Its researcher,
bibliography and source editions await registration.

Follow each corpus's reproduction guide and each package's stated inputs,
commands and verification scope. October's [reproduction guide](october_corpus/REPRODUCING.md)
links its mathematical checks and evidence. From a clean, committed checkout,
check preservation of the directory migration with:

```sh
python3 -E -B scripts/check_corpus_layout.py
```
