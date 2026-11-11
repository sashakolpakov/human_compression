# Reproducing the October corpus

Paths in corpus records are relative to `october_corpus/`, unless they identify
a historical commit or an external source location.

## Current corpus checks

From the repository root, run:

```sh
python3 -E -B scripts/check_corpus_scope.py
```

This checks membership, manuscript grouping, completion and measurement counts,
current metadata bindings, and documentation links. It uses the Python standard
library and does not execute mathematical searches or build papers.

The [source catalogue](audit/corpus/catalogue.json) records the 103 components
of 102 manuscripts, including source URLs, editions and retained input hashes.
The [intake status](INTAKE_STATUS.json) records all 101 mathematical treatments
as complete. The [measurement overview](audit/overview/README.md) covers the
53 measured applications and 19 topics.

## Selected mathematical checks and builds

Choose an application from the [manuscript catalogue](papers/latest_catalogue.json)
and follow its publication guide. Reproduce its full common theory, local proofs,
declared certificates and retained inputs. Source PDFs may require separate access;
their exact editions and hashes belong to the source contract.

In a checkout containing the selected packages:

```sh
cd october_corpus
python3 -E -B scripts/smoke_check.py --quick --timeout 600
python3 -E -B scripts/build_papers.py --help
python3 -E -B scripts/check_project_lean.py --help
```

The quick suite runs three selected certificate checks. Other mathematical,
rendering and Lean checks have the scopes and dependencies declared by their
packages. Keep build outputs outside the checkout and select one package at a time.

## Storage and archived evidence

A partial clone avoids downloading all historical evidence:

```sh
git clone --filter=blob:none --no-checkout https://github.com/sashakolpakov/human_compression.git
cd human_compression
git sparse-checkout set --cone scripts november_corpus
git checkout main
```

Materialize the specific October guides and packages needed for a replay.
Keep the referenced Git history and tags; frozen records may use commit-addressed
objects. Historical snapshot and layout checkers validate their named editions.
Their earlier corpus counts are not current intake statistics.
