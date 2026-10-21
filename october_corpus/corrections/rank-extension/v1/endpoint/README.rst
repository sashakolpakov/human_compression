Endpoint central extensions: a bounded correction
================================================

This packet concerns only the converse printed in Proposition 2.4 of
Cameron--Fernandes--Leemans, arXiv:2212.12723v2 (11 January 2023), L019.
The written two-page proof supplies a literal counterexample under the printed
sggi definition. The original marking is dependent, which that definition allows.
It is not a counterexample to a converse with additional unprinted hypotheses.

The forward endpoint result used in the accepted L010 constructions remains
valid and is explicitly preserved. Neither the main stability theorem nor
Theorem 6.4 is disproved by this example. No complete-source or question credit,
historical priority claim, or new numerical factor is assigned.

The full GAP file is a diagnostic of the elementary proof, not its premise.
There is no Lean certificate in this bounded packet. The checker verifies
frozen files and the exact primary PDF, reruns all subgroup checks, rejects
three concrete damaged examples, and optionally rebuilds both PDF pages::

  python -B -O check.py --study-root /path/to/leemans --out /fresh/path \
    --gap /path/to/gap --render --xelatex /path/to/xelatex

The complete primary PDF stays private. It is an existing closed-corpus input;
its exact hash and locators are recorded in scope.json. The rendering needs
STIXGeneral and STIX Two Math. Finite computation trusts the installed GAP;
the written vector-space proof is independent of that software.
