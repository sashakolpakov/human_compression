Ordinary centre halves: a complete relative replay
=================================================

This bundle enumerates the ordinary, unrooted half domains H_b for b=1,2,3,4
used in the centre-three reduction for order-32 quintic graphs. It includes
the incidence-margin argument, all-root ordinary identification, fourteen
side-domain templates, four collection templates and bounded runtime guards.
Read THEORY.tex for the mathematics and SOURCE_PROVENANCE.json for attribution.
The underlying cage problem and original count are due to Cambie, Goedgebeur,
Jooken and Van den Eede; these computations recover known results. They do not
claim a new conjecture solution or, by themselves, complete the full order-32
composition argument.

The installed bundle has completed a fresh replay of 57 synthetic controls,
all fourteen raw domains and four complete ordinary unions. The four complete
ordinary streams match the initial replay and earlier accepted streams byte
for byte. REPLAY.json gives the resulting counts and stream identities.
These are comparison data, never inputs to enumeration or collection.

Files and dependencies
----------------------

Use a POSIX shell and Python 3 with its standard library. The guards also need
the version of psutil pinned in requirements.txt: psutil==7.2.2. The scientific
child runs with -E -B -S; the supervisor runs with -E -B so that psutil remains
available. No Lean, graph library, previous output tree or private SDK store is
needed to run the local computation.

The functional files are declared by manifest.json. Its SHA256 is
a2afc046ed7d962b22021e57c1c0cf26f8c3534d87ad36d1cb83bb65b0884e5f.
Do not edit its source, policy or templates for this replay. The active source
union is 65,524 bytes: run.py, halves.py, controls.py and the two runtime files.
The source cap is 65,536 bytes per worker. The shell commands and small metadata
readers below dispatch separate bounded workers; they are external instructions,
not an additional scientific launcher or part of that worker-source invoice.
The total reproduction instructions and mathematical manuscript have separate
written lengths; the source cap does not measure their compression.

Every worker retains the existing 128 MiB sampled RSS cap, 150 second outer
limit and 120 second scientific limit. Admission requires 4 GiB available RAM
and 10 GiB free disk, with 3 GiB RAM and 8 GiB disk floors. Data, records,
compatible evaluations and declared reads retain their manifest limits. The
guards sample known process families; they do not impose kernel quotas or
prove that no unseen detached process exists. Run the workers sequentially.
If admission or a guard fails, stop and keep the recorded reason; do not raise
the limits to obtain this replay.

Start from a clean copy
----------------------

A fresh clone contains the static bundle but no jobs/ or runs/. A clean copy
of the manifest-declared files works as well. Run the following blocks in the
same shell, starting inside this directory. Existing jobs or runs cause a
deliberate refusal. Use a fresh copy for another complete replay; the commands
do not remove previous evidence.

If a suitable Python environment already has requirements.txt installed, set
HC_PY to its absolute interpreter path. Otherwise create an environment outside
the clone, for example::

    python3 -m venv "$HOME/.venvs/centre-halves"
    HC_PY="$HOME/.venvs/centre-halves/bin/python"
    "$HC_PY" -m pip install -r requirements.txt

Set up the fresh relative workspace and the unchanged guard invocation::

    set -eu
    HC_BUNDLE="$(pwd -P)"
    HC_MANIFEST_SHA=a2afc046ed7d962b22021e57c1c0cf26f8c3534d87ad36d1cb83bb65b0884e5f
    test -n "$HC_PY"
    test ! -e jobs
    test ! -e runs
    mkdir jobs runs runs/guards

    hc_guard() {
        hc_guard_name=$1
        shift
        /usr/bin/env -u COVERAGE_PROCESS_START -u COVERAGE_PROCESS_CONFIG \
            -u OPENSSL_CONF -u OPENSSL_MODULES \
            "$HC_PY" -E -B "$HC_BUNDLE/runtime/supervise_validation.py" \
            --volume "$HC_BUNDLE" \
            --output "$HC_BUNDLE/runs/$hc_guard_name" \
            --rss-cap-mib 128 --timeout 150 -- "$@"
    }

    hc_template_sha() {
        "$HC_PY" -E -B -S -c \
            'import json,sys; m=json.load(open("manifest.json")); print(next(r["sha256"] for r in m["files"] if r["path"]==sys.argv[1]))' \
            "$1"
    }

    hc_job_sha() {
        "$HC_PY" -E -B -S -c \
            'import hashlib,pathlib,sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())' \
            "$1"
    }

Controls, fourteen domains, then four unions
------------------------------------------

First run the 57 synthetic checks. The guard writes its child stdout directly
to runs/controls/stdout.log, which is the exact relative report path used by
every template. These controls do not run any census domain::

    hc_guard controls "$HC_PY" -E -B -S \
        "$HC_BUNDLE/controls.py" "$HC_MANIFEST_SHA"

Bind all fourteen enumeration templates to the current controls and source
identities, then run each full raw domain. The explicit list includes the two
zero domains, b1_s12 and b2_s7::

    HC_ENUM='b1_s8 b1_s9 b1_s10 b1_s11 b1_s12 b1_s13 b1_s14 b2_s4 b2_s5 b2_s6 b2_s7 b3_s2 b3_s3 b4_s1'
    for hc_label in $HC_ENUM; do
        hc_template="templates/$hc_label.json"
        hc_template_pin="$(hc_template_sha "$hc_template")"
        hc_guard "guards/bind_$hc_label" "$HC_PY" -E -B -S \
            "$HC_BUNDLE/run.py" --manifest manifest.json "$HC_MANIFEST_SHA" \
            --bind "$hc_template" "$hc_template_pin" --volume "$HC_BUNDLE"
    done

    for hc_label in $HC_ENUM; do
        hc_job="jobs/$hc_label.json"
        hc_job_pin="$(hc_job_sha "$hc_job")"
        hc_guard "guards/run_$hc_label" "$HC_PY" -E -B -S \
            "$HC_BUNDLE/run.py" --manifest manifest.json "$HC_MANIFEST_SHA" \
            --job "$hc_job" "$hc_job_pin" --volume "$HC_BUNDLE"
    done

    "$HC_PY" -E -B -S - $HC_ENUM <<'PY'
    import json
    import sys
    from pathlib import Path

    for label in sys.argv[1:]:
        receipt = json.loads(Path(f"runs/{label}/receipt.json").read_bytes())
        assert receipt["mode"] == "enumerate"
        assert receipt["scope_complete"] is True and receipt["frontier"] is None
        assert receipt["requested_raw_interval"] == [0, receipt["raw_domain"]]
        assert receipt["completed_raw_interval"] == [0, receipt["raw_domain"]]
    PY

Only after those domains have completed, bind the four collection templates.
Binding includes the freshly produced interval receipts and their data pins.
Then collect the complete ordinary union for each b::

    HC_COLLECT='b1_collect b2_collect b3_collect b4_collect'
    for hc_label in $HC_COLLECT; do
        hc_template="templates/$hc_label.json"
        hc_template_pin="$(hc_template_sha "$hc_template")"
        hc_guard "guards/bind_$hc_label" "$HC_PY" -E -B -S \
            "$HC_BUNDLE/run.py" --manifest manifest.json "$HC_MANIFEST_SHA" \
            --bind "$hc_template" "$hc_template_pin" --volume "$HC_BUNDLE"
    done

    for hc_label in $HC_COLLECT; do
        hc_job="jobs/$hc_label.json"
        hc_job_pin="$(hc_job_sha "$hc_job")"
        hc_guard "guards/run_$hc_label" "$HC_PY" -E -B -S \
            "$HC_BUNDLE/run.py" --manifest manifest.json "$HC_MANIFEST_SHA" \
            --job "$hc_job" "$hc_job_pin" --volume "$HC_BUNDLE"
    done

A PASS guard alone does not mean that a scientific interval is complete. The
scientific stdout reports scope_complete and frontier. Collection refuses gaps,
overlaps, missing shapes and inconsistent input pins. A complete collection
also checks every carried ordinary witness and every emitted ordinary code.

Read counts after all four complete outputs exist
------------------------------------------------

The following metadata reader prints nothing until all four receipts describe
complete unions and all four complete output bodies match their receipt pins.
It does not decode graph payloads or run scientific code::

    "$HC_PY" -E -B -S - <<'PY'
    import hashlib
    import json
    from pathlib import Path

    counts = []
    for b in range(1, 5):
        receipt = json.loads(Path(f"runs/b{b}_collect/receipt.json").read_bytes())
        assert receipt["schema"] == "HB_LOCAL_RECEIPT_V1"
        assert receipt["mode"] == "collect" and receipt["b"] == b
        assert receipt["scope_complete"] is True and receipt["frontier"] is None
        assert receipt["complete_ordinary_union"] is True
        assert receipt["record_interval"] == [0, receipt["record_domain"]]
        data = receipt["data"]
        raw = Path(data["path"]).read_bytes()
        assert len(raw) == data["bytes"]
        assert hashlib.sha256(raw).hexdigest() == data["sha256"]
        assert not raw or raw.endswith(b"\n")
        assert raw.count(b"\n") == receipt["records"] == receipt["h_b"]
        counts.append((b, receipt["h_b"], data["sha256"]))
    for b, count, digest in counts:
        print(f"h_{b} = {count}; stream SHA256 {digest}")
    PY

The recorded complete counts are 2, 5, 36 and 115. There are 159 marked
records before ordinary identification; in the b=3 case, 37 marked records
give 36 ordinary classes. Compare the complete stream hashes in REPLAY.json,
not just the four counts. None of these reference values enters a worker.

Evidence and local bindings
---------------------------

jobs/ contains fresh local bindings. runs/ contains the controls report,
guard records, interval receipts, complete data streams and union receipts.
Both directories are ignored by Git. Static source and documentation can be
cloned without retaining compiled files, environments or generated outputs.
Preserve the source pins with any run evidence you intend to cite.

HB_LOCAL_JOB_V1 and HB_LOCAL_RECEIPT_V1 bind local file identities. They are not
Root approvals, Root SDK events or independent execution provenance. A user
can reproduce the numerical result using these commands without acquiring any
such authority. The recorded initial and installed acceptance used separately
retained actual Root API records and independent metadata reviews; those records
are distinct from the local job and receipt schemas. The mathematical kernel
is shared with the earlier census, so this replay is not a second independent
graph algorithm, a new paper, a Lean certificate or a compression measurement.
