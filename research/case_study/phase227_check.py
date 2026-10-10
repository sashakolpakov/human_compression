#!/usr/bin/env python3
"""Check the immutable bindings of a bounded literature audit.

This verifies file identities and the declared query/source inventory. It does
not certify historical priority, search completeness, or a mathematical proof.
No network access or optional dependencies are required.
"""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "phase227_manifest.json").read_text())
    checked = []
    for row in manifest["exports"] + manifest["retained_bindings"]:
        path = root / row["path"]
        data = path.read_bytes()
        if len(data) != row["bytes"]:
            raise SystemExit(f"Byte count mismatch: {row['path']}")
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise SystemExit(f"SHA256 mismatch: {row['path']}")
        checked.append(row["path"])
    queries = json.loads((root / "phase227_queries.json").read_text())
    if queries["query_count"] != len(queries["queries"]) or len(queries["queries"]) != 37:
        raise SystemExit("Query inventory mismatch")
    if [r["id"] for r in queries["queries"]] != [f"Q{i:02}" for i in range(1, 38)]:
        raise SystemExit("Query identifiers are not consecutive")
    sources = json.loads((root / "phase227_sources.json").read_text())
    if len(sources["primary_sources"]) != 6:
        raise SystemExit("Primary source inventory mismatch")
    verdict = json.loads((root / "phase227_verdict.json").read_text())
    if verdict["historical_priority_verified"] is not False:
        raise SystemExit("This packet does not verify priority")
    print(json.dumps({
        "status": "PASS",
        "bindings_checked": len(checked),
        "queries": 37,
        "primary_records_with_bound_fulltexts": 6,
        "scope": "File and inventory verification only; no exhaustive-priority certificate."
    }, indent=2))


if __name__ == "__main__":
    main()
