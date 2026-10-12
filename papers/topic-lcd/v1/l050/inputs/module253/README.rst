The Steiner augmentation module
===============================

Read modules.pdf (three pages) and scope.json. This bounded author packet
recovers L050 Theorem1(d), and corrects the extra dual-code assertions in
Proposition5. It does not admit the complete original.

The common incidence factorization, minimum-support recognition, matrix-algebra
criterion and elementary incidence refinement are reused. Whole enumeration
data, exact old bases and the previously reviewed complete method are retained.
No full enumeration is repeated. Atlas classification and finite-field module
descent remain explicit outside inputs for the least-degree uniqueness sentence.

Replay with the global Python, NumPy and GAP:

  python -B -O check.py --out /fresh/directory --render

The complete bound is23*22*21*20*16*3=10200960, attained by the explicit
point group identified as M23. There are484 independent matrix words for
the22-dimensional augmentation. The driver checks frozen inputs, three
weakening controls and a clean two-pass proof render. It requires no source
PDF or discovery graph software. Required files and retained classifications
are listed in scope.json; source software cost is unknown, not zero.
