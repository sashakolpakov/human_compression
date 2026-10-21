L029: a chiral coset geometry with disconnected residues
=======================================================

This package gives a reviewed counterexample to Theorem 1.1 in Dimitri
Leemans and Philippe Tranchida, On residual connectedness in chiral
geometries, Algebraic Combinatorics 4(3) (2021), 491–499,
https://doi.org/10.5802/alco.162. The fixed published PDF has ten physical
pages including its cover. The target theorem is on printed page 491.
This is a principal refutation, not an ordinary recovery of the paper.

Read proof/counterexample.pdf and its complete five-page TeX source.
The source has no adjacent TeX inputs. The geometry has 112 objects and
4368 chambers. Its specified C-plus group is PSL(2,13), of order 1092,
whereas its full type-preserving automorphism group is PSL(2,13) x C2,
of order 2184. The full group has two alternating chamber orbits, exactly
as required by the source's definition of chirality on printed page 493.
An actual rank-two residue consists of two disjoint six-cycles.

The proof verifies the entire right-coset Construction 3.2, the independence
of the generators and all subset intersection identities. It proves the
full automorphism group by an elementary local graph argument. The source
proof on printed page 496 transfers proper-flag transitivity from the full
group to the specified group; their index-two difference is essential here.
Rank-three Proposition 4.11 is not refuted, nor is a version that separately
requires the specified group to have the two alternating chamber orbits.
Other results in the paper are not thereby recovered. No historical-priority,
later-edition, absence-of-errata, named-question, Lean or measurement claim
is made. Complete source routes and qualifications are in scope_routes.json.

Evidence and roles
------------------

The author is l044_resume. Root independently read the complete source,
proof and code, and wrote a second GAP implementation without author imports.
Its successful call checks all 256 subgroup intersections, 4704 literal
right-coset incidence pairs and the disconnected residue. The preceding
failed call remains intact. Root is the distinct mathematical reviewer;
this package does not manufacture a separate adoption as another review.
Publication_recovery prepares the exact transport and fresh public replay.

The proof uses decorated-vector vocabulary also found in L041, but gives
all arguments it needs. The exact three L041 manifests are preserved as
provenance leaves; their proofs are not imported. The old owner checkpoint
and abandoned working route are preserved verbatim as history. Its unrelated
task pointers are not acquired premises. These boundaries are explicit in
portable_policy.json and are checked against exact path and hash inventories.
Frozen author metadata still says review pending; the unchanged later root
review is the operative mathematical acceptance.

Public replay
-------------

programs/finite.py is the unchanged standard-library certificate, with
programs/expected.json giving its exact output. The convenient independent
GAP script alias is byte-identical to the reviewed original. Neither program
replaces the written full-automorphism proof.

The portable checker restores every scientific and audit byte, checks all
50 exports of the three retained manifest records and every acquiring nested
pin, verifies the historical GAP call closure, then runs the unchanged Python
certificate and three damaged-example controls. It checks optimization guards
and builds all five native pages using ordinary Python 3 with pypdf, pdflatex
and Ghostscript on PATH. The native pages match the accepted proof exactly.
There is no private fallback or runtime text patching. The original wrapper,
whose dependency paths are private and absolute, is retained unchanged; the
explicit public adapter is documented in portable_adaptation.json.

Eight documentary assets are hash-only: the two original articles and six
source-page renders. No scientific proof, program, numerical input, validation
output, failure receipt or mathematical review is omitted. The three provenance
manifests and historical checkpoint are retained files, not omitted documents.
Every reused public object is Git tracked, so a clean checkout is sufficient.
The manifest lists all exact logical and stored identities. Full replay is:

  python corrections/chiral-residues/v1/portable_check.py --repo . --out NEW_DIRECTORY --expected-transport ec0f1c2b49b91d32cc53e138ebba4ae7f0ab6500a702778f0269eb811445d234 --expected-policy 7a9d43fc9eba221330a9f14a90a064fa0071f88719d45621420dda95701ec5e0 --expected-adapter 5d53fe8973fd2708811609ac6e7ed10c64dd9e14303b8346f34abf6c1838dd7a

Registration remains separate
-----------------------------

This private payload changes no public file or count. After L041 is published,
the proposed L029-only transition is from 85 recoveries plus one refutation
to 85 recoveries plus two refutations: 87 handled and 18 pending among the
105 mathematical originals. The 53 measured and 32 unmeasured recoveries stay
unchanged. The final root gate belongs at audit/principal-refutations/L029/v1.
Operational transport review, exact predecessor binding, distinct registration
review and root integration are still required. Root is the sole public writer.
