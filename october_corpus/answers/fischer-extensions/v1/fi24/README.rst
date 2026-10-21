Fi24-prime:2 finite incidence certificate
========================================

The saved words define a regular polytope of type {6,35} and a regular
rank-three hypertope with triangular labels (6,6,35), both with full
type-preserving automorphism group Fi24-prime:2. The four-page manuscript
contains the generation, incidence, residue and automorphism arguments.
This is a separate candidate answer to the possible exception in N006,
Theorem 5.3, arXiv:2605.04646v2, subject to independent acceptance. It makes
no claim of historical priority or a construction for the simple socle.

Replay with Python 3, GAP 4.15.1 and CTblLib 1.3.11::

  python3 -B -O check.py --atlas-root /path/to/atlas/files --out /fresh/path

The external directory must contain both complete files whose exact hashes
and primary URLs are in retained_inputs.json:

* F24d2G1-p306936B0.g1 (2,152,215 bytes; literal assignment b11)
* F24d2G1-p306936B0.g2 (2,273,175 bytes; literal assignment b21)

The driver verifies the hashes and validates the complete literal
permutation syntax and disjoint cycle labels before GAP execution. It
copies the inputs into a fresh output directory. Existing paths and dangling
symlinks are refused. Installed catalogue table/index hashes are checked;
no search is rerun and no ambient group-order enumeration is attempted.

Generation uses an actual outer involution and actual words of orders 23
and 29. The complete retained maximal-subgroup classification says that
only the socle among the twenty-one maximal subgroup types has order
divisible by both primes. The note prints the full table and proves the
exclusion argument. Named-group identification, outer class and complete
classification remain external mathematical inputs. Standard-generator
identities and catalogue checks do not replace them.

Both markings pass 49 proper-subset intersection tests; the remaining
15 pairs per marking are elementary full-subset identities. The six exact
flag equations use 1,168 and 1,824 complete product tests, respectively.
The halved marking has a directly checked generation inverse. The sixteen
controls include actual saved-word mutations, a genuine marking satisfying
IP but failing the flag equations, and malformed external-input fixtures.
GAP errors with a zero process exit are rejected rather than treated as
successful proofs.

The complete two GAP programs, compact word file and Python driver are
exported. The 4,425,390 external permutation bytes and all required
catalogue inputs stay visible as retained dependencies. They are not
redistributed here. Their costs are not replaced by the word-file size.
No Lean declarations or kernel verification of GAP are claimed. Search
programs/traces, source PDFs and primary web pages remain private and are
not part of the distributed certificate. There is no dependency on the
separate nine-case, HN or Fi22 packets for this replay.

The manuscript can be rebuilt with XeLaTeX, normally twice for references::

  xelatex -interaction=nonstopmode -halt-on-error fischer24.tex

The bounded edition/literature check in source_status.json distinguishes
an answer to this specified possible-exception case from any claim of
priority. No source count, question credit or compression factor is changed
by the author freeze.
