Marked involution extension: bounded formal replay

Run from any working directory:
  python3 -B -O audit/lean-extension/check.py --out /fresh/absolute/path
Pass --lean and --packages for other local installations. Lean4.32.2 and
the exact dependency revisions are required. This runner reads the canonical
Lean source and formal paper directly; no Markdown, primary PDF, network,
or author .olean is needed. Nine declarations compile with standard axioms;
two false formal weakenings and an altered finite countermodel must reject.

The general theorems prove actual four-marker injectivity, involutions, string
commutation, group generation and prefix preservation. They do not construct
PSL tori or prove maximal-subgroup classification or the complete application.
Old96-module fresh-build evidence is unchanged; this is a separately compiled
97th module. See ../lean_extension.json for the additive audit.
