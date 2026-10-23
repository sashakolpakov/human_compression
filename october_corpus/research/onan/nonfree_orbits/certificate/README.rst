Nonfree O'Nan endpoint orbits: a finite conditional nongeneration certificate
==========================================================================

This package contains all1776 nonfree representative records from the accepted
L026 endpoint index, their whole original keys/weights and a Python stdlib
checker. The general proof is simple: a nonfree inner endpoint orbit has a
nonidentity stabilizer centralizing the three marks, hence both rotation
generators; those generators cannot generate a centerless ambient group.
See proof/original_argument.rst and SCOPE.rst for the exact borrowed premises.

The complete copied index has31988 representative rows:11581 and20407 at the
two endpoints. Inner group orders are256 and144. Its771 and1005 nonfree rows
have total inner masses89879 and63351. These are inner orbit counts/masses,
not automorphism or reversal class counts. The checker verifies every index
row, ALL and ONLY the1776 literal family rows, their individual nontrivial
stabilizer quotients, both complete endpoint masses and each full-file SHA.

Reproduce from this directory in a fresh isolated copy
----------------------------------------------------

Use Python3.9 or newer. No GAP, project install, network, compiled extension
or third-party Python library is needed. After copying/cloning this directory,
change into it and run the following. All generated results are outside the
package/checkout; the checker refuses an existing output or an output inside
this directory.

.. code-block:: sh

   package_dir="$(pwd -P)"
   results_dir="$(mktemp -d "${TMPDIR:-/tmp}/l026-nonfree.XXXXXX")"
   results_dir="$(cd "$results_dir" && pwd -P)"
   python3 -I -B -S "$package_dir/check.py" --out "$results_dir/family.json"

The expected finite result has family_count1776, nonfree_counts[771,1005],
family_inner_masses[89879,63351], and one exact stabilizer quotient greater
than one per family row. Read the whole result for the retained qualifications.
These are expected results from the mathematical/metadata contract; this
portable checker has NOT been executed by its preparer. Root must inspect and
run the isolated reproduction before publishing a portable-run attestation.
The prior private checker ran successfully; that is a separate historical
artifact and is not a portable execution claim.

Optional explicitly borrowed parent overlap
------------------------------------------

examples/borrowed_parent_ledger.json is a7124-byte historical Root ledger,
SHA25677737f74601f12979d11d2367567557ff014a3f3e06e80bff46b0bf8a5e9fea7.
It is NOT a proof package for its18 generating or3 invariant-subset rows.
To check only its structural overlap with this nonfree family:

.. code-block:: sh

   python3 -I -B -S "$package_dir/check.py" \
     --parent-ledger examples/borrowed_parent_ledger.json \
     --parent-ledger-sha256 77737f74601f12979d11d2367567557ff014a3f3e06e80bff46b0bf8a5e9fea7 \
     --out "$results_dir/borrowed_overlap.json"

This optional result should report192 already-paid nonfree rows and1584 new
family rows. Its213 parent-paid rows plus1584 give1797 by union arithmetic.
The other21 parent decisions remain borrowed; their generating/subset
certificates are not verified here. No parent file, ledger, gate or checkout
is modified, and this optional calculation is not a new adoption or claim
about the latest private ledger.

Contents and provenance
-----------------------

data/representatives.json and data/nonfree_family.json are byte-exact copies
of the accepted index and literal certificate. premises/ holds exact copied
accepted index/setup/T1/T2 metadata. Their historical JSON contains original
absolute references. SourceManifest.json maps only the needed original refs
to local relative paths with the SAME byte counts and hashes. The checker has
no fallback that opens an original host path. All other historical refs stay
opaque and are not recursively opened or claimed verified.

proof/ contains byte-exact existing mathematical Sources. Their historical
UNRUN/preparation statements remain as originally frozen. source/original_checker.py
is the unmodified private Source ancestor for attribution; do not execute it
as the portable entrypoint. check.py is the new relative-path publication
edition. SourceDerivation.json records its explicit changed Source and whole
ancestry. SourceManifest.json lists original locations/pins; no private runtime
binaries, maps, large group/partition tapes or whole proof-DAG archive is copied.

Scope
-----

This is a conditional finite family certificate. Named centerless O'Nan,
the original/faithful model identification, exact endpoint subgroup meaning
and historical exact orbit weights remain borrowed premises. The checker
authenticates their retained metadata; it does not reprove them, classify
groups, replay a partition or perform a group computation. It decides no
free row and awards no full generation census, Aut/IP/reversal/Original,
measurement, novelty or Lean credit.
