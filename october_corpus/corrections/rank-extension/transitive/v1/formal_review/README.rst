Independent Lean review of the transitive output obstruction
============================================================

All sixteen declarations were freshly compiled by a separate driver after
reading the complete source. Only propext, Classical.choice and Quot.sound
occur in the reported axioms. The old input C-property, source hypotheses
and standard end criterion remain written, not formalized.

Run ``python -B -O check.py --packet /path/to/formal --correction
/path/to/written --lean /path/to/lean --packages /path/to/packages
--out /fresh/directory`` with Lean4.32.2 and the pinned packages. Cached
upstream oleans are explicit trusted dependencies; this freshly compiles
the actual permutation/subgroup obstruction.
