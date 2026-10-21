Independent review of restriction kernels
=========================================

The exact five-page author manuscript is accepted. The root reviewer read all
statements and proofs and inspected all five freshly rendered pages. The
substantive induction and support arguments are recorded in review.json.
This supplies exact criteria for the stated leaf and separated split
constructions. It does not recover the complete source L019 or decide its
main high-rank stability theorem.

The full author replay passes its bounded GAP cases, mutation controls,
three Lean declarations and five-page render. A separate Python implementation,
using tuple permutations and closure enumeration without GAP or author code,
checks all 600 subgroup/root instances of the kernel equivalence in S4.
There are 480 positive and 120 negative instances. These tests support the
review; the quantified theorem rests on the written proof.

A separate direct Lean invocation compiles the complete generic subgroup
proofs with standard axioms only. The restriction-map application and string
induction are not claimed formalized. The pinned cached dependencies remain a
trust boundary. The author's internal impact audit of old public proofs is
retained as such; this review does not relabel it as a distinct rereading.

Run the distinct check from any directory::

  python3 -B -O check.py --packet /path/to/author --out /fresh/output

Optional --lean and --packages configure the pinned toolchain and dependency
location. The bound author runner supplies the complete source/dependency
and negative-control replay. No primary texts, rasters or compiled Lean
artifacts are exported here. No new original, conjecture or ratio is credited.
