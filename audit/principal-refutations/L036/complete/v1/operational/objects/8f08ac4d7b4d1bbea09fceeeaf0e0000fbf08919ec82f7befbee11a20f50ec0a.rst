Stored mark data for the remaining L036 counts and suborbits
==========================================================

This is a single library-data acquisition for eleven named tables. The six
automorphism groups are M12.2, J2.2, J3.2, HS.2, McL.2 and He.2; the five
simple groups needed for the source's suborbit tables are M11, M12, M22,
M23 and J1. It constructs no groups or cosets and searches for no fusion.
The installed character files already contain a FusionToTom record for
each group. The exporter requires that record before accessing it.

Each row consists of the requested name, table identifier, group order,
subgroup orders, sparse nonzero column positions and corresponding marks,
element centralizer orders, square map, element orders, stored fusion from
element classes to cyclic subgroup classes, and (for the five simple
groups) maximal character-table names and the optional fusion permutation
as a list of images. Absence of that optional permutation means identity,
as the Character Table Library explicitly documents. For the six outer
cases, the final two lists are empty because their identification uses the
socle classes in the complete mark table instead.

The accepted proof character_application/theory.tex gives the mathematics.
For A=Aut(G), the unique subgroup class of order |A|/2 is G. Maximal proper
classes below G give the A-classes of its maximal subgroups M. Their
normalizers have order |M| or 2|M|, determined by the diagonal mark. In the
second case, a containing subgroup of order 2|M| must normalize M, since
M has index two in it; uniqueness follows. Thus the mark rows of these
normalizers give the fixed-point character of A on all maximal subgroups
of G. Burnside's lemma, with the square map, then counts unordered pairs
under the full automorphism action required by the source.

For a simple group G, pointwise products of two maximal mark rows decompose
uniquely as nonnegative integer combinations of mark rows. A coefficient
at L contributes that many orbits of length |H|/|L| for H on G/K. All
suborbit multisets therefore follow by independent triangular arithmetic.
The character-table maximal names and their documented permutation provide
an additional source-label join; equal orders alone are not sufficient.
The actual source row/column matches and native superscripts remain separate
application obligations. Counts do not establish the 37 M11 graphs,
intersection group names, girths, diameters or design parameters.

The independent application must check complete sparse array shapes,
positive marks, diagonal and identity marks, order divisibilities,
triangular containment, the unique socle, all maximal/normalizer choices,
cyclic orders against fusion, class-size sums, square-map ranges, integral
fixed-point and Burnside values, and exact row-product decompositions.
Printed source totals are comparison outputs only, never arithmetic inputs.

The data are explicit borrowed premises: the named groups, simplicity and
full automorphism groups are classical identifications; TomLib supplies
complete subgroup-class tables, and CTblLib supplies compatible class
centralizers, powers and fusion. Internal numerical consistency does not
prove that a table belongs to its named group or is complete. The exact
library data, loader sources and documentation are pinned. The mathematics
is conditional on these premises and on installed GAP 4.15.1 behavior.
No new classification credit is inferred from exporting library data.

The marks of He.2 occupy about 18.7 MB in their uncompressed library file.
The single request therefore permits 64 MiB total stdout/stderr, a 60-second
external deadline and a fixed 512 MiB GAP workspace. It preserves the
existing 4 GiB prelaunch reserve and 2 GiB emergency floor. A terminal
failure or partial output is retained literally; no automatic successor
or retry is authorized. Root must read the frozen request before execution.

Edition 02 changes only process supervision. SIGINT, SIGTERM and polling
exceptions enter terminal cleanup; the owned process group is terminated and
the direct child is waited for before a receipt is written. Final elapsed
time, output size and disk reserve are checked even when a child returns
between polls. Every bound input and the request are freshly rehashed after
the process returns. Any mismatch is recorded as a failed terminal condition.
Four small disposable Python children exercise normal completion, an injected
interrupt, a changed input and output exceeding the cap just before exit.
These controls do not invoke GAP or acquire mathematical data.
