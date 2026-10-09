"""Retrieve publicly exposed PDF links; do not treat downloads as papers read."""
from pathlib import Path
import concurrent.futures
import hashlib
import json
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "sources"
PLAN = ROOT / "retrieval_plan.json"
OUT = ROOT / "bulk_retrieval_manifest.json"
# These were already retrieved manually, before the bulk matching step.
MANUAL = {"L009": "linear_triality2026.pdf", "L012": "regular_2np2025.pdf",
          "L014": "regular_4pm2025.pdf", "L015": "suzuki_triality2025.pdf",
          "L017": "absolute_triality2024.pdf", "L021": "psl2_maniplex2023.pdf",
          "L024": "schur_index2022.pdf"}

def retrieve(row):
    rec = dict(id=row["id"], title=row["title"], match_score=row["score"],
               matched_title=row["matched_title"], reading_scope="downloaded_not_read", attempts=[])
    target = SRC / ("catalogue_" + row["id"] + ".pdf")
    if row["id"] in MANUAL:
        target = SRC / MANUAL[row["id"]]
    if target.exists() and target.read_bytes().startswith(b"%PDF"):
        rec.update(filename=str(target.relative_to(ROOT)), sha256=hashlib.sha256(target.read_bytes()).hexdigest(), status="downloaded_existing")
        return rec
    for url in row["pdf_urls"]:
        with tempfile.NamedTemporaryFile(dir=SRC, suffix=".part", delete=False) as f:
            tmp = Path(f.name)
        try:
            p = subprocess.run(["curl", "-L", "--fail", "--silent", "--show-error", "--max-time", "22", url, "-o", str(tmp)], capture_output=True, text=True, timeout=25)
            data = tmp.read_bytes()
            attempt = {"url": url, "exit_code": p.returncode, "bytes": len(data), "error": p.stderr.strip()[:160]}
            rec["attempts"].append(attempt)
            if p.returncode == 0 and data.startswith(b"%PDF"):
                tmp.rename(target)
                rec.update(filename=str(target.relative_to(ROOT)), source_url=url, sha256=hashlib.sha256(data).hexdigest(), status="downloaded")
                return rec
        except Exception as exc:
            rec["attempts"].append({"url": url, "error": str(exc)[:160]})
        finally:
            if tmp.exists():
                tmp.unlink()
    rec.update(status="retrieval_failed", reading_scope="metadata_only_retrieval_attempted")
    return rec

def main():
    rows = [r for r in json.loads(PLAN.read_text()) if not r["existing"] and r["pdf_urls"] and (r["score"] >= .96 or r["id"] == "L076")]
    # L084 is an erratum, and its fuzzy match incorrectly identifies the original.
    rows = [r for r in rows if r["id"] != "L084"]
    results = json.loads(OUT.read_text()) if OUT.exists() else []
    done = {r["id"] for r in results if r["status"].startswith("downloaded")}
    rows = [r for r in rows if r["id"] not in done]
    print("retrieving", len(rows), "catalogue works", flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(retrieve, row): row["id"] for row in rows}
        for f in concurrent.futures.as_completed(futures):
            rec = f.result()
            results = [r for r in results if r["id"] != rec["id"]] + [rec]
            OUT.write_text(json.dumps(sorted(results, key=lambda x: x["id"]), indent=2) + "\n")
            print(rec["id"], rec["status"], flush=True)

if __name__ == "__main__":
    main()
