# Phase219: formal coset certificates

This is a verification extension of the reviewed phase212/214/215 label-eleven obstruction. It does not create an additional conjecture resolution or replace another historical manuscript.

## What is proved

- The general coset-deduction rules are sound for actual right cosets of an arbitrary subgroup.
- Complete derived transitions on a finite name set imply finiteness and an index upper bound. A finite facet also yields a genuine finite-group order bound.
- An executable finite trace checker has a soundness theorem and an interface to the actual group defined by the generator squares and the listed relators.
- Two kernel-checked traces prove the label-eleven dihedral facet bound eleven and group-order bound twenty-two.
- A direct proof-carrying replay of the frozen rank-three table proves all 3072 transitions and the actual universal-presentation index bound 1024. A separate kernel-checked equation binds its relator list to the three pair words and all ten source triple-power words.

The concrete rank-three file uses individual Derives proof terms, rather than claiming that the Boolean checker evaluated a million-row table. The two smaller examples also test the Boolean checker itself. Both routes are proved and have their own exact scope.

## Canonical theorem files

1. phase219_formal/CosetUpperCertificate.lean — inference rules, actual coset semantics, executable checker, presented-group interface and order consequence.
2. phase219_formal/CosetUpperExamples.lean — complete small traces, dihedral order bound and four formal rejection controls.
3. phase219_formal/LabelElevenRankThree.lean — literal source relators, tree-word definitions, 3072 checked edge proofs, proof-carrying row array and index theorem.

The prose manuscript is phase219_coset_certificates.md. The independent review of the prior computational result remains phase215 and is not rewritten here. This new author package requires its own admission/review.

## Replay

Use Python3, Lean4.32.2 and the nine package revisions pinned by formal/dependency_manifest.json. The packages must have their ordinary compiled dependencies available. The runner compiles the additionally needed Mathlib PresentedGroup dependency modules into a fresh local cache. Existing cached dependency objects remain an explicit trust boundary.

```sh
python3 -B -O phase219_check.py \
  --out /tmp/phase219-fresh \
  --lean /path/to/lean-4.32.2/bin/lean \
  --packages /path/to/.lake/packages
```

The output path must not exist, including as a dangling symbolic link. The runner verifies package revisions and tracked-source cleanliness, regenerates both concrete source files byte-for-byte, compiles all three theorem files, checks their 25 selected axiom reports, and rejects two semantic mutations that remove the tree-word or relator-membership check. The four small rejection controls are themselves Lean theorems. No native_decide, proof hole, concrete group-order axiom, GAP process or C++ process is used by this replay.

Only phase214_tables.json and phase214_certificates/table3.txt.gz are needed from the earlier certificate data. The rank-four and rank-five compressed tables are not inputs to this runner. The two untrusted generators can also be run separately with fresh --out directories; their emitted proof text is subject to Lean checking.

## Limits and costs

Rank-four and rank-five tables are not Lean verified by this package. The phase212 finite-field group orders, simplicity and signed memberships remain outside it. The complete F014 conjecture refutation is therefore not an end-to-end Lean theorem. The earlier source-edition and historical-priority qualifications remain unchanged.

The large generated Lean file is part of the proof artifact, not an invisible output to omit from measurement. The manifest records exact byte counts for it, the general kernel, the examples, the prose, the generators and the verification evidence. No matched compression ratio is assigned. New principal-source credits: zero. Additional conjecture resolutions: zero.

The trace generator, the original naming oracle and ACE are not logical premises of the Lean result. Lean checks the individual proof terms against the exact universal presentation. The compiler, Lean kernel, pinned Mathlib infrastructure and already compiled dependency objects retain their stated roles.
