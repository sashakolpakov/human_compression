Nonfree O'Nan endpoint orbits
============================

This portable certificate gives a conditional nongeneration obstruction for
all **1,776 nonfree rows** in the accepted 31,988-row L026 endpoint index.
The two endpoints contribute 771 and 1,005 rows, with inner orbit masses
89,879 and 63,351. A nonidentity orbit stabilizer centralizes the marks and
both rotation generators; generation would contradict the borrowed
centerlessness of the named ambient group. See the
`proof <certificate/proof/original_argument.rst>`_ and
`scope <certificate/SCOPE.rst>`_.

The standalone stdlib checker **passed from an isolated copy** on
2026-10-23 under the retained 512 MiB / 150 s limits. It verified the complete
literal family and the optional historical overlap: 192 already-paid
nonfree rows and 1,584 additional family rows. The run took about 0.101 s;
sampled peak RSS was 28,098,560 bytes. The
`validation attestation <validation/attestation.json>`_ binds the exact
`result <validation/result.json>`_, receipt, genuine Tool return and closed
scope records. The idle observation belongs to that completed run.

Reproduce from the repository root
---------------------------------

Use Python 3.9 or newer. No project installation, GAP, network or third-party
Python package is required. These commands create fresh outputs outside the
checkout:

.. code-block:: sh

   repo_dir="$(pwd -P)"
   package_dir="$repo_dir/october_corpus/research/onan/nonfree_orbits/certificate"
   results_dir="$(mktemp -d /tmp/l026-nonfree.XXXXXX)"
   results_dir="$(cd "$results_dir" && pwd -P)"
   python3 -I -B -S "$package_dir/check.py" --out "$results_dir/family.json"
   python3 -I -B -S "$package_dir/check.py" \
     --parent-ledger examples/borrowed_parent_ledger.json \
     --parent-ledger-sha256 77737f74601f12979d11d2367567557ff014a3f3e06e80bff46b0bf8a5e9fea7 \
     --out "$results_dir/borrowed_overlap.json"

The first result checks the family alone. The optional second result checks
overlap arithmetic against the explicitly borrowed historical parent; it
does not verify that parent's 18 generating or three invariant-subset claims.
Neither command writes a ledger, gate or accepted checkpoint.

Preserved Sources and limits
----------------------------

The 16 files under certificate/ are byte-exact copies of the tested package.
Its preparation-era README and scope statements remain historical snapshots;
the completed portable-run status is recorded above and in validation/.
`SourceManifest.json <certificate/SourceManifest.json>`_ maps needed original
references to local relative files. Unmapped private provenance remains
opaque; the checker has no original-host-path fallback. Large permutation
maps, partition tapes and private runtime archives are not included.

Named O'Nan, the original/faithful-model identification, endpoint subgroup
meaning and exact historical orbit weights remain borrowed premises. This
package replays no group classification or partition computation and decides
no free row. L026 remains unfinished. The corpus count stays **102/105**
fully treated originals; this artifact adds no whole Original, Aut/IP,
reversal, census-completion, measurement, novelty or Lean credit.
