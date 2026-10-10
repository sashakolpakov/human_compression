# Odd kernels, two characters, and cyclotomic polyhedra

This private author package contains a complete eight-page replacement paper
for the principal contract of L014, Hou–Feng–Leemans–Qu, *String C-groups of
order 4p^m*, in the bound arXiv2407.10388v1 edition. It is submitted for
independent review. It is not a new coverage admission or a whole-paper
compression measurement.

Read `phase236_odd_kernel_manuscript.md` or its PDF, then
`phase236_contract.json` and `phase236_source_ledger.json`.

The paper proves the normal Sylow kernel and its two generators, the
abelian/tight classification, and the full nonabelian {p,2p} family for
every odd prime p and every m≥3. Its cyclotomic model is proved isomorphic
to the source's explicit marked presentation, including the individual
orders of generators and the automorphism formulas. The literal v1
Theorem1.2 marking has square x² rather than1; the corrected marking and
exponent assignment are stated explicitly. No journal-edition error or
open-conjecture solution is claimed.

The primary L014 PDF is locally bound. The retained Cunningham–Pellicer
Theorem1.1 was read in the primary at https://arxiv.org/pdf/1408.6703v2,
physical p.2. Local download failed DNS, so it has no local PDF hash in
this package. It is used only for tight⇒abelian and uniqueness among all
tight markings; our abelian classification and construction are proved
directly. The full retained source has not been rederived.

## Replay

Run from this directory, giving a fresh output path:

```sh
python3 -B -O phase236_check.py --out /private/tmp/phase236_fresh \
  --gap /opt/homebrew/bin/gap \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --packages /Users/sasha/bogachev/formal/.lake/packages
```

The checker creates exact mixed-modulus ring models, emits literal
permutations, and asks GAP to verify group orders, all source relators,
markings, maximal class and all64 intersection equalities. The seven
nonabelian parameters are (p,m)=(3,3),(3,4),(3,6),(5,3),(5,5),(7,3),(11,3).
The four abelian parameters (p,a,b) are (3,1,1),(3,1,2),(3,2,2),(5,1,2).
Three negative controls corrupt the cyclotomic relation, install the
literal faulty source marking, and corrupt the source generator orders.
The last two GAP processes may return0 after an Error; the driver checks
the expected rejection text and absence of the success marker, not just
the process status. Python optimization does not disable any validation.

Lean4.32.2 and the pinned Mathlib tree compile five declarations in
`phase236_formal/OddKernelIntersection.lean`. They prove the prime-index
intersection criterion, its generated-group form, two reflection-product
identities, and the square of the faulty marking. No custom axioms,
proof holes, or native decision procedure are used. The cyclotomic,
Sylow, character and retained-classification arguments remain written.

## Boundaries and costs

The required authored proof artifacts are the manuscript, model generator,
GAP checker, portable driver, Lean source and formal dependency manifest.
The driver generates the example permutation data; the data are not a
retained table or an uncharged source input. The PDF is another rendering
of the manuscript. Logs, ledger and manifest are audit support. A later
measurement must state how it charges the retained CP theorem and general
background; no numerical compression rate is assigned here.

`phase236_acquisition_and_scope.md` records the bounded, unsuccessful
attempts to obtain older sources L085/L089/L109. The supposed old L085
author PDF is actually later L074. None of these access attempts adds
primary intake or recovered-source credit. Earlier frozen packages and
the public repository are unchanged.
