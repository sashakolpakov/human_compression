Topic F: regular and chiral odd-kernel polyhedra
================================================

This private author edition extends the accepted L014 application by the
complete corrected principal contract of L007. It has not itself been
independently admitted. No source, question or numerical credit is asserted.
The three scientific papers are ``umbrella.tex/pdf``,
``odd-kernel-polyhedra.tex/pdf`` and ``chiral-odd-kernels.tex/pdf``.
Their entire common theory is part of this edition, with no free proof
crossing from the old application or an archived proof bank.

The common paper contains the full previous intersection/orbit/character/
cyclotomic theory. The complete split construction formerly in L014's
application now appears here, with only its label and internal references
changed. The former application theorem retains its full statement and
cites this shared proof. All seven other original section files remain
byte-identical. The exact source records, migration and current proof
spans are in ``scope.json`` and ``migration.json``.

The second application recovers L007 Theorems 1.1, 1.2 and 1.4, including
all odd primes and the complete stated odd/even parameter ranges. The
uniform small-order argument replaces the source's classification and
small-prime lookup by class-three collection and exact presentation bounds.
The cyclotomic carry construction proves order, generation, type,
intersection, non-tightness and absence of reversal for the literal
source presentations. The even construction is an explicit module fibre.

All four regular byproducts of Remark 1.3 are addressed. The first three
exist for every odd prime. The fourth, of type {p,2p^2} and order 4p^4,
exists exactly at p=3; the written obstruction rules out p>=5. The source's
Section 6, Claim 4 map to C_(p^2) x C_p fails a reflection relation; the
valid cyclic quotient and complete module construction repair that proof
route. These are literal source qualifications, not new conjecture credits.
The previously proved central lift covers the remaining small even range,
with its old proof and kernel hypothesis reproduced. Section 7's literal
word “tight”, its intended context and the absence of a new priority or
current-literature claim are kept separate.

Source and proof boundary
-------------------------

The exact L007 source is the 22-page accepted manuscript, accepted
19 January 2026, DOI 10.26493/1855-3974.3716.b64, SHA256
``a3c3587427fd87c162af0d825fb1547e66fcfb74aa6ca96379ab46d6d43112a2``.
All pages were read in the existing full extraction and viewed in private
renders. The 25 inherited L014 records remain intact. The 38 additional
L007 dispositions cover the principal clauses, all four Section 3 lemmas,
all seven Section 6 claims, retained inputs, corrections and explicit
background exclusions. A disposition is not a new theorem count.

The classical group-to-polyhedron correspondences, Burnside basis theorem,
and elementary finite-group/ring background remain retained. The tight
characterization uses the exact odd bicyclic/metacyclic facts attributed
to Huppert and Iwasawa via Schmidt at the point of use. Their complete
original book proofs are not locally retained or priced. L014's
Cunningham--Pellicer tight classification remains an explicit retained
input; its complete PDF and full-text cost are unavailable. No finite
sample replaces these statements. Source historical discussion, Conder's
introductory census and Cunningham's separately cited tight constructions
are not regenerated. The full general metabelian collection theorem and
full small-group classifications are not claimed merely from the smaller
interfaces proved here.

Complete code and formal scope
------------------------------

``program-appendix.tex/pdf`` prints all nine complete validation files.
The raw files are under ``programs/``. They comprise the three unchanged
L014 programs, the new carry and regular-family model checks, two complete
exploratory small-group/subgroup scans, and the two previous central-lift
checks. Historical comments in the exploratory files describe their role
when written; every file is now explicitly disclosed as validation. None
is required for the quantified written proof. No diagnostic file has been
pruned to reduce a future comparison. Printed versus raw code are alternative
representations, not additive charges. GAP and its SmallGroups catalogue
are trusted only for the bounded diagnostics that use them.

The two complete historical operational drivers are preserved separately
under ``drivers/``. The current ``check.py`` calls their mathematical
programs directly. The current formal checker is also operational code.
No primary source text, page raster, package object or output model data
is exported as a mathematical source in this packet.

Three whole Lean files provide twelve distinct declarations: five unchanged
prime-index/reflection statements; four unchanged lift/intersection
statements, of which three are used by this lift; and three new generic
carry-obstruction statements. Standard axioms are reported per declaration.
The module, group-extension, class-three, small-order and geometric
application proofs are not formalized. The formal checker compiles the
local files freshly, privately rebuilding absent pinned mathlib objects;
other pinned package objects remain trusted. No full mathlib rebuild or
full source formalization is claimed.

Replay
------

Use Python with pypdf, GAP, pinned Lean 4.32.2/packages and XeLaTeX with
STIXGeneral, STIX Two Math and Menlo::

    python3 -B -O check.py --out /fresh/output \
      --programs --formal --render \
      --gap /path/to/gap --xelatex /path/to/xelatex \
      --lean /path/to/lean --packages /path/to/pinned/packages

Optional ``--study-root /path/to/study`` verifies exact primary and prior
proof bindings. A copied packet otherwise replays independently of its
original directory. The old explicit lift script intentionally runs
without Python's optimization switch because its assertions are its
finite checks. All output paths must be fresh, including symlink checks.
The runner checks all63 dispositions, whole-code inclusion and18 binding/
hypothesis controls. Formal replay adds the two inherited countermodels.
No GAP or Lean claim is inferred from a previously saved report alone.

No ratio has been computed for this expanded edition. A future comparison
must acquire the entire common paper once, both whole applications, and
state whether it includes the complete validation appendix/raw alternative.
External proof and source-graphics costs remain unknown rather than zero.
