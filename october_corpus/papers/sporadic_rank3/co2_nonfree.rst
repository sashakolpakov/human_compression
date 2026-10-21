An obstruction from nonfree orbits and its Co2 application
==========================================================


This component is a partial result with an arithmetic certificate. It does
not classify the remaining Co2 markings or complete the source paper L026.
The original classification and endpoint framework are due to Dimitri Leemans
and Jessica Mulpas, The string C-group representations of the Suzuki, Rudvalis
and O'Nan sporadic groups, Art of Discrete and Applied Mathematics 5 (2022),
#P3.09, DOI 10.26493/2590-9770.1405.4ce. No new classification or priority is
claimed for the elementary orbit-stabilizer implication below.

In that source, Section 3 gives the rank-three algorithm; Section 4.5, Table 2
(PDF page 10), lists Co2, and Section 5.4 (PDF page 11) describes its order,
degree 2300, three involution classes and printed rank-three total 60,370.
That total is documentary context, never a checker input, target or stop rule.

Abstract proof
--------------

Let G be a finite centerless group, let a, b, c belong to G, and let
S=C_G(a,c) be the subgroup of elements that centralize both specified end
marks. When S acts on b by conjugation, the stabilizer is

  C_S(b)=C_G(a,b,c).

If a, b, c generate G, an element centralizing all three centralizes G.
Their centralizer is therefore Z(G)=1. The orbit-stabilizer theorem gives
|b^S|=|S|. Thus a genuine S-orbit smaller than |S| cannot contain a middle
mark that generates G together with those end marks. This implication needs
no involution assumption, maximal-subgroup classification, permutation
representation or transitivity criterion.

An orbit of full size supplies no converse: it is not a generation
certificate. A nongenerating conclusion supplies no exact order of the proper
generated subgroup. A setwise end stabilizer T cannot replace S here; its
elements can exchange a and c instead of centralizing both. No intersection
property or reversal/duality assertion is inferred.

Conditional numerical application
--------------------------------

The application imports the acquired named centerless group G=A=Co2, its
actual end marks and class-1 middles b=y^r with r in G. It also imports that
S12=C_G(a,c) is the full pointwise centralizer of order 1280, that U=C_G(y)
has order 1474560, and that the supplied rows form the complete disjoint
S12-orbit partition. In that actual double-coset interpretation, a row of
mass m has S12-orbit length ell with m=|U|*ell. These are mathematical and
acquisition premises. Scalar mass equalities or the displayed group orders
alone do not establish them.

The twelve accepted normalized scopes cover 178 top blocks and 24,690 row
keys. Each included normalized literal_rows.json is copied byte-for-byte
from its accepted source, as are its block ranges and small acceptance
record. The checker reconstructs every top-local and slice row coordinate,
checks strict integer masses and orbit lengths, positive divisors of 1280,
and each block's exact sum. Their total mass is 42305421312000. It then
applies the obstruction to the actual normalized rows with ell<1280,
rather than inferring row IDs from an aggregate bound.

The expected complete replay identifies 3,627 nonfree row keys and 21,063
full-size rows. The entire ordered nonfree table has canonical compact-JSON
SHA256 cff24d4358470572aa7b1000bc08661c61a9e9334a703de870492ba2eac27e7f.
The full table, not a count alone, is regenerated into the external output.
Its five fields are top_index, top_row, slice_row, orbit_size and
double_coset_mass. The 21,063 full-size rows remain undecided by this
criterion. No generating, self-dual or whole-cell parity count is supplied.

Named-model membership, normalized permutation/hash correctness, genuine
centralizers and the complete disjoint S-orbit partition remain imported
accepted premises. The old positive_orbit_bijection_checked=false
qualification is preserved. This arithmetic replay does not re-establish
those premises by parsing the 288 MB raw permutation rosters, recomputing a
group or orbit action, or merely trusting a displayed group order. It
includes no such raw rosters, model archives, native executable or installed
library. The same boundary is recorded in premises.json.

Source ancestry and evidence
---------------------------

The free-action observation was already an accepted check in the acquired
pointwise-chain protocol. Its application was written in
transitivity_reduction.rst, retained verbatim in provenance. Only its first
free-action section is used here; the separate maximal-subgroup/transitivity
converse and proposed generation, intersection-property and reversal routes
are not this replay. The accepted row-mass arithmetic was independently
authored/reviewed by /root/resource_cleanup_audit in
review_row_mass_plan.py, SHA256 prefix 4bef0119. The portable entry was
prepared by /root/c5_terminal_audit. Five complete mathematical AST spans
(the scope/row loop, two global invariants and ordered-key/digest steps) must
match the exact retained reference Source before any arithmetic can run.
That reference is parsed as text only, never imported or executed.

The original ROOT acceptance and distinct-review records are documentary
provenance. Their paths, actors, tool identities and old labels are preserved;
they are not commands or current runtime authorities. source_map.json joins
each original identity to exact bytes at a component-relative public path.
The checker uses those old names only as dictionary keys. It has no fallback
read from a private study, no installed runtime hash dependency, no ROOT
state or ownership-registry access and no mathematical Source imported from
outside the component. The complete normalized metadata occupies about 7 MB;
no packed binary or build product is needed.

Reproduction
------------

Use ordinary Python 3.11 or newer on macOS or Linux, without optimization.
Only the Python standard library is used. Python/stdlib correctness and the
stated group/orbit premises remain software and mathematical premises; this
is not a proof-assistant formalization. The declared version range needs
actual portable-interface acquisition; Source alone is not an execution
claim.

Obtain MANIFEST_SHA256 from the independently accepted publication record or
trusted commit. From the bundle or public checkout root, metadata-only mode
authenticates every declared byte and the exact arithmetic Source ancestry,
without executing the arithmetic or writing output::

  python3 -E -B scripts/sporadic_rank3/check_co2_nonfree.py \
      --manifest-sha256 MANIFEST_SHA256 --metadata-only

For the actual arithmetic select a fresh absolute directory outside the
canonical bundle or checkout, whose parent already exists::

  python3 -E -B scripts/sporadic_rank3/check_co2_nonfree.py \
      --manifest-sha256 MANIFEST_SHA256 \
      --out /absolute/external/co2-nonfree-check

Successful output contains started.json, the complete nonfree_keys.json and
result.json with the exact histogram, 178 block summaries, counts, total
mass and canonical key-table hash. The program stops at the first error,
never retries, and preserves any files already written. failure.json records
a diagnosed failure if its bounded write succeeds. A nonzero exit, failure
record, incomplete output or resource refusal must never be adopted as PASS.
No generated output belongs in the canonical publication payload.

The whole component is bounded at 8 MiB, a single input at 4 MiB, result at
128 KiB and the complete key table at 2 MiB. Reads use 64 KiB chunks, stable
file identities and Darwin F_NOCACHE where applicable. Shared 100 s and
observed 128 MiB checkpoints are refusals, not hard OS limits or a fit
theorem. Callers must provide any desired process-family, resource and
output protection. The ROOT intake acquisition uses a separately accepted
guard; that machine-specific guard is not bundled as a mathematical
premise. No actual run or timing claim is supplied by this Source staging
step.

Scope that remains open
----------------------

The proof rules out generation for 3,627 conditional normalized row keys.
These are not 3,627 new native candidate returns. Any overlap with older
accepted rows must be counted once by a separate typed union; the checker
does not claim 3,479 additional current ledger entries or mutate a checkpoint.
The provenance checkpoint is historical evidence, not a writable target or
completion oracle. The surviving rows, other end-pair domains, generation
and reversal results, whole-cell/parity joins and original L026 completion
remain open. No census, conjecture, Lean, compression measurement or
whole-original credit follows. This component changes neither the separate
completed L046 result nor any other original's status. No TeX/PDF
compilation is required for reproduction.
