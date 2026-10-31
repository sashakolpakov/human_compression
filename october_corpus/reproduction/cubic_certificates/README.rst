Cubic certificates for forty-two original quartets
=================================================

This supplement verifies forty-two intersection-property failures in the
natural seven-dimensional G2(11) model used by F004. It adds to the earlier
matrix_certificates package. The original classification remains unfinished.
The source is Malcolm Hoong Wai Chen, *Abstract regular polytopes of G2(q)
in even characteristic*, arXiv:2609.25004v1, Section 4's q=11 census.

The verifier checks the original catalogue and frame calculations, all four
marked involutions and the string commutations. For each left subgroup it
checks a nonzero row satisfying an irreducible cubic relation of order 133,
and all eight sign systems that could give a common rational invariant line.
THEORY.rst explains why those facts imply failure of the intersection property.
It preserves the reviewed proof edition; REPLAY.json records the completed runs.

The original identification with G2(11), faithful model, full orbit and
transporter proofs, and the cited subgroup classification remain imported
premises. SOURCE_PROVENANCE.json records that boundary. Its historical paths
are documentary: the commands below open only this relative bundle.
These certificates are not complete Lean proofs or a new conjecture result.

Reproduce the finite checks
---------------------------

Python 3.9 or later and its standard library suffice. From this directory,
run the controls and certificates in separate processes::

    python3 -E -B -S controls.py --manifest-sha256 f10a3e710a523922c4a4ade238be8d9f408dff3867b0f6b60cbd917b2a0fb4fa
    python3 -E -B -S verify.py --manifest-sha256 f10a3e710a523922c4a4ade238be8d9f408dff3867b0f6b60cbd917b2a0fb4fa

Do not enable Python optimization. All 33 controls and 42 certificates passed
the initial guarded run. The evidence directory records its output, resource
receipts and independent source reviews; REPLAY.json records final validation.

For the bundled resource supervisor, install requirements.txt in an isolated
environment. Use a fresh result directory on the same filesystem as the clone.
For example, with REPRO_PYTHON set to that environment's Python::

    REPRO_BUNDLE="$(pwd -P)"
    REPRO_RUN="$(mktemp -d "${REPRO_BUNDLE%/*}/.cubic-certificate-results.XXXXXX")"
    env -u COVERAGE_PROCESS_START -u COVERAGE_PROCESS_CONFIG \
        -u OPENSSL_CONF -u OPENSSL_MODULES \
        "$REPRO_PYTHON" -E -B runtime/supervise_validation.py \
        --volume "$REPRO_BUNDLE" --output "$REPRO_RUN/resources" \
        --rss-cap-mib 128 --timeout 150 -- \
        "$REPRO_PYTHON" -E -B -S "$REPRO_BUNDLE/verify.py" \
        --manifest-sha256 f10a3e710a523922c4a4ade238be8d9f408dff3867b0f6b60cbd917b2a0fb4fa

Run controls.py under the same supervisor in a separate fresh output directory.
The supervisor samples memory and known child processes. It requires 4 GiB
available RAM and 10 GiB free disk at admission, with floors of 3 and 8 GiB.
The finite verifier keeps its existing limits of 128 MiB, 100 seconds,
400,000 matrix products, 200,000 rank operations and 2 MiB of input reads.
The outer timeout is 150 seconds. Full input hashes are checked again at exit.
