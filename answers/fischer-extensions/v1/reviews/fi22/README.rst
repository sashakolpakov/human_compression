Independent review of the explicit Fi22:2 geometries
===================================================

The corrected author v2 is accepted for a regular polytope of type {6,13}
and a regular hypertope with triangular diagram (6,6,13), both with full
type-preserving automorphism group Fi22:2. This supplies the Fi22 possible
exception in Theorem 5.3 of arXiv:2605.04646v2. It is separate from the
source's ten affirmative cases, and leaves Fi24prime untouched.

Read review.json, proof_reading.json and source_and_status.json for the
exact roles and retained inputs. The complete three-page proof was read;
all pages were visually inspected. Two full author GAP programs and the
literal witness were freshly replayed. The independent literal_cosets.g
uses the saved permutations but none of the author geometry helpers: it
checks actual subgroup element sets and incident left-coset flags.
data_audit.py parses the witness without executing it and verifies the
corrected catalogue route. The extra loader-index binding supplements the
author's exact catalogue/loader pins; the named-group identification and
GAP algorithms remain retained. Optional maximal-subgroup classification
checks are present in full, but direct generated-group equality is the
generation proof.

The status ledger records a bounded search, not proof of historical
priority. Its seven queries were read, not independently repeated in full.
The primary arXiv and Atlas metadata were independently checked. This
review makes no automatic source, question or formal credit change.

Bounded replay (no GAP, primary only with the optional flag)::

  python3 -B -O check.py --study-root /path/to/study \
    --verify-primary --out /fresh/output

Add ``--programs --gap /path/to/gap`` to copy only the 21 author exports
plus manifest to a fresh directory and rerun the full finite certificate
and independent literal-coset check. This requires the exact retained GAP
packages. No primary PDF is copied. ``--packet-root`` and ``--status-root``
can explicitly route relocated immutable author and status packets.

The default replay checks exact review/author/status bindings, the two
markings' scope, saved fresh output, literal-data grammar and eight scope
mutations. It does not turn the checker into a proof-assistant kernel.
No Lean declaration is claimed. Unknown external proof costs are null.

The author v1 wrong gps35 pin is preserved as history and is not accepted.
The current v2 binds gps34, and the runtime degree3510 index was checked.
