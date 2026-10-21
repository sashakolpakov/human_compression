#!/usr/bin/env python3
"""Freshly compile every canonical Lean module, with an explicit pinned cache.

Example (all three paths are supplied by the caller):
  python3 -B scripts/check_lean.py --lean LEAN --packages PACKAGES --out NEW_DIR

The output directory must not exist. Sources are copied there and built in
dependency order; no project .olean files or inherited LEAN_PATH are used.
The cached external dependencies remain an explicit trust boundary. Ordinary
`lake build` in research/case_study/formal also targets every canonical module.
This checks Lean files, not all written proofs or finite group computations.
"""
from __future__ import annotations

import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "research/case_study/formal"
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
LEGACY_MODULE = "Phase23TransferAnnihilator"
LEGACY_SOURCE_SHA256 = "0ee15f12f7cb9583380cf49ff5467da3001fb184ca912002487e6d35044f198f"
LEGACY_AXIOMS = {
    name + "._native.native_decide.ax_1_1"
    for name in ("third_difference", "terminal_basis_fixed", "fourth_difference", "newton_coefficients")
}
AXIOM_RE = re.compile(
    r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
)


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_hash(path):
    return digest(path.read_bytes())


def without_comments(text):
    """Mask nested Lean block and line comments; retain all source positions."""
    out = list(text)
    i = depth = 0
    quoted = False
    while i < len(text):
        if depth:
            if text.startswith("/-", i):
                out[i:i+2] = "  "
                depth += 1
                i += 2
            elif text.startswith("-/", i):
                out[i:i+2] = "  "
                depth -= 1
                i += 2
            else:
                if text[i] != "\n":
                    out[i] = " "
                i += 1
        elif quoted:
            if text[i] == "\\":
                i += 2
            else:
                quoted = text[i] != '"'
                i += 1
        elif text[i] == '"':
            quoted = True
            i += 1
        elif text.startswith("/-", i):
            out[i:i+2] = "  "
            depth = 1
            i += 2
        elif text.startswith("--", i):
            end = text.find("\n", i)
            end = len(text) if end < 0 else end
            out[i:end] = " " * (end-i)
            i = end
        else:
            i += 1
    need(depth == 0 and not quoted, "unterminated source comment/string")
    return "".join(out)


def source_check(name, data):
    text = without_comments(data.decode("utf-8"))
    need(not re.search(r"\b(?:sorry|admit|sorryAx)\b", text), name + ": proof hole")
    need(not re.search(r"\baxiom\s+", text),
         name + ": explicit axiom declaration")
    if re.search(r"\bnative_decide\b", text):
        need(name == LEGACY_MODULE and digest(data) == LEGACY_SOURCE_SHA256,
             name + ": unapproved native evaluation")
    imports = parse_imports(name, text)
    printed = re.findall(r"^\s*#print\s+axioms\s+(\S+)", text, re.M)
    need(printed, name + ": no axiom reports requested")
    return imports, printed


def parse_imports(name, text):
    imports = []
    for tail in re.findall(r"^\s*(?:(?:public|meta)\s+)*import\s+(?:all\s+)?([^\n]+)", text, re.M):
        names = tail.split()
        need(all(re.fullmatch(r"[\w.]+", n) for n in names), name + ": unsupported import syntax")
        imports.extend(names)
    return imports


def axiom_reports(name, stdout, expected_count):
    rows = [dict(declaration=n, axioms=re.findall(r"[\w.]+", a))
            for n, a in AXIOM_RE.findall(stdout)]
    need(len(rows) == expected_count, name + ": missing/extra axiom reports")
    need(len({r["declaration"] for r in rows}) == len(rows), name + ": repeated axiom report")
    unexpected = {a for row in rows for a in row["axioms"]} - STANDARD_AXIOMS
    allowed = LEGACY_AXIOMS if name == LEGACY_MODULE else set()
    need(unexpected == allowed, name + ": changed nonstandard axioms " + repr(sorted(unexpected)))
    return rows


def check_roots(modules, lake_text):
    roots = re.findall(r"`([\w.]+)", lake_text)
    need(len(roots) == len(set(roots)), "duplicate Lake root")
    need(set(roots) == set(modules),
         "Lake roots differ from discovered modules: missing=" + repr(sorted(set(modules)-set(roots)))
         + ", extra=" + repr(sorted(set(roots)-set(modules))))


def topological_order(dependencies):
    order = []
    pending = {k: set(v) for k, v in dependencies.items()}
    while pending:
        ready = sorted(k for k, v in pending.items() if not v)
        need(ready, "cycle in canonical Lean import graph")
        for name in ready:
            order.append(name)
            del pending[name]
        for deps in pending.values():
            deps.difference_update(ready)
    return order


def controls():
    cases = [
        ("proof_hole", lambda: source_check("Control", b"theorem bad : False := by sorry\n#print axioms bad\n")),
        ("explicit_axiom", lambda: source_check("Control", b"axiom bad : False\n#print axioms bad\n")),
        ("unapproved_native", lambda: source_check("Control", b"theorem ok : True := by native_decide\n#print axioms ok\n")),
        ("unexpected_reported_axiom", lambda: axiom_reports("Control", "'bad' depends on axioms: [newAxiom]", 1)),
        ("omitted_lake_root", lambda: check_roots({"A", "B"}, "roots := #[`A]")),
        ("import_cycle", lambda: topological_order({"A": {"B"}, "B": {"A"}})),
    ]
    passed = []
    for name, action in cases:
        try:
            action()
        except RuntimeError:
            passed.append(name)
        else:
            raise RuntimeError("negative control accepted: " + name)
    return passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path, help="Pinned Lean compiler executable")
    parser.add_argument("--packages", required=True, type=Path, help="Directory of pinned Lake package checkouts and cached objects")
    parser.add_argument("--out", required=True, type=Path, help="Fresh isolated build directory")
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--timeout", type=float, default=1800, help="Seconds per module")
    args = parser.parse_args()
    need(args.jobs > 0 and args.timeout > 0, "positive jobs and timeout required")
    need(not args.out.exists() and not args.out.is_symlink(), "output must be fresh (including symlinks)")
    out = args.out.resolve()
    need(not out.exists() and not out.is_relative_to(FORMAL.resolve()), "fresh output outside formal sources required")
    out.mkdir(parents=True)
    for sub in ["src", "lib", "logs", "dependency_src", "dependency_lib"]:
        (out/sub).mkdir()
    start = time.monotonic()
    report = dict(status="RUNNING", scope="Fresh compilation of every canonical Lean source and its printed axiom reports; not full manuscript verification.",
                  started_utc=datetime.now(timezone.utc).isoformat(), modules=[],
                  checker_sha256=file_hash(Path(__file__)), negative_controls=controls(),
                  cached_external_objects_trusted=True, local_objects_rebuilt=True)
    def save():
        report["elapsed_seconds"] = round(time.monotonic()-start, 3)
        (out/"report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n")
    try:
        lean = args.lean.resolve()
        packages = args.packages.resolve()
        pins_path = FORMAL/"dependency_manifest.json"
        pins = json.loads(pins_path.read_bytes())
        version = subprocess.check_output([str(lean), "--version"], text=True).strip()
        expected_version = pins["lean"].split(":v")[-1]
        need(re.search(r"version " + re.escape(expected_version) + r"[, ]", version), "Lean version mismatch")
        report.update(lean_version=version, lean_executable_sha256=file_hash(lean),
                      dependency_manifest_sha256=file_hash(pins_path),
                      lean_toolchain_sha256=file_hash(FORMAL/"lean-toolchain"),
                      lakefile_sha256=file_hash(FORMAL/"lakefile.lean"), dependencies=[])
        need((FORMAL/"lean-toolchain").read_text().strip() == pins["lean"], "toolchain manifest mismatch")
        libraries = []
        package_sources = []
        for pin in pins["packages"]:
            path = packages/pin["name"]
            package_sources.append(path)
            rev = subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
            need(rev == pin["rev"], "package revision mismatch: " + pin["name"])
            need(subprocess.run(["git", "-C", str(path), "diff", "--quiet", "HEAD", "--"]).returncode == 0,
                 "modified tracked package source: " + pin["name"])
            lib = path/".lake/build/lib/lean"
            if lib.is_dir():
                libraries.append(lib)
            report["dependencies"].append(dict(name=pin["name"], revision=rev, cached_objects_used=lib.is_dir()))
        modules = {p.stem: p for p in FORMAL.glob("*.lean") if p.name != "lakefile.lean"}
        need(modules, "no canonical modules discovered")
        need(not any(p for p in FORMAL.rglob("*.lean") if p.parent != FORMAL and ".lake" not in p.parts),
             "nested Lean sources require an explicit module-layout update")
        check_roots(modules, (FORMAL/"lakefile.lean").read_text())
        data, imports, printed, saved_names = {}, {}, {}, {}
        for name, path in modules.items():
            need(not path.is_symlink(), "canonical source symlink: " + name)
            data[name] = path.read_bytes()
            imports[name], printed[name] = source_check(name, data[name])
            saved = json.loads(path.with_suffix(".check.json").read_bytes())
            need(saved["sha256"] == digest(data[name]) and saved["exit_code"] == 0, name + ": stale saved report")
            saved_names[name] = [r["declaration"] for r in axiom_reports(name, saved["stdout"], len(printed[name]))]
            (out/"src"/path.name).write_bytes(data[name])
            for imp in imports[name]:
                need(imp in modules or imp.split(".")[0] in {"Mathlib", "Std", "Lean", "Init"},
                     name + ": unknown local/external import " + imp)
        deps = {n: set(imports[n]) & set(modules) for n in modules}
        order = topological_order(deps)
        report.update(discovered_modules=sorted(modules), module_count=len(modules),
                      local_import_edges=sum(map(len, deps.values())), topological_order=order,
                      standard_axioms=sorted(STANDARD_AXIOMS),
                      legacy_native_allowlist=dict(module=LEGACY_MODULE, source_sha256=LEGACY_SOURCE_SHA256,
                                                   axioms=sorted(LEGACY_AXIOMS)))
        # Lean resolves a namespace from its first matching search root, not
        # each individual object from successive roots. Construct one merged
        # read-only cache view before adding freshly compiled missing objects.
        cache_links = 0
        for library in libraries:
            for cached in sorted(library.rglob("*")):
                if cached.is_dir():
                    continue
                need(cached.is_file(), "broken cached object: " + str(cached))
                dest = out/"dependency_lib"/cached.relative_to(library)
                need(not dest.exists() and not dest.is_symlink(), "overlapping package cache paths: " + str(dest))
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.symlink_to(cached.resolve())
                cache_links += 1
        report["cached_external_files_linked"] = cache_links
        env = dict(os.environ)
        env["LEAN_PATH"] = os.pathsep.join(str(p) for p in [out/"lib", out/"dependency_lib"])
        env.pop("LEAN_SRC_PATH", None)
        # Some pinned caches contain only the material used in earlier papers.
        # Rebuild absent imports from pinned sources rather than borrowing an
        # undocumented object directory or modifying the supplied cache.
        prefix = Path(subprocess.check_output([str(lean), "--print-prefix"], text=True).strip())
        external_libraries = [out/"dependency_lib"] + libraries + [prefix/"lib/lean"]
        report["rebuilt_external_dependencies"] = []
        building = set()
        def ensure_external(name):
            rel = Path(*name.split("."))
            if any((base/rel.with_suffix(".olean")).is_file() for base in external_libraries):
                return
            need(name not in building, "external import cycle: " + name)
            candidates = [base/rel.with_suffix(".lean") for base in package_sources
                          if (base/rel.with_suffix(".lean")).is_file()]
            need(len(candidates) == 1, "missing/ambiguous pinned source for external import " + name)
            source = candidates[0]
            raw = source.read_bytes()
            building.add(name)
            for dep in parse_imports(name, without_comments(raw.decode("utf-8"))):
                ensure_external(dep)
            copied = out/"dependency_src"/rel.with_suffix(".lean")
            target = out/"dependency_lib"/rel.with_suffix(".olean")
            copied.parent.mkdir(parents=True, exist_ok=True)
            target.parent.mkdir(parents=True, exist_ok=True)
            copied.write_bytes(raw)
            for suffix in [".olean", ".olean.private", ".olean.server", ".ir", ".ilean"]:
                product = target.with_suffix(suffix)
                if product.is_symlink():
                    product.unlink()
                else:
                    need(not product.exists(), "external rebuild would overwrite a fresh object: " + str(product))
            t = time.monotonic()
            result = subprocess.run([str(lean), "-o", str(target), str(rel.with_suffix(".lean"))],
                                    cwd=out/"dependency_src", env=env, capture_output=True, timeout=args.timeout)
            stdout, stderr = result.stdout.decode("utf-8"), result.stderr.decode("utf-8")
            for suffix, contents in [("stdout", result.stdout), ("stderr", result.stderr)]:
                (out/"logs"/(name+"."+suffix)).write_bytes(contents)
            need(result.returncode == 0, "external dependency compilation failed: " + name)
            report["rebuilt_external_dependencies"].append(dict(module=name, source_sha256=digest(raw),
                object_sha256=file_hash(target), exit_code=result.returncode,
                seconds=round(time.monotonic()-t, 3), stdout=stdout, stderr=stderr,
                stdout_sha256=digest(result.stdout), stderr_sha256=digest(result.stderr)))
            building.remove(name)
            print("[dependency] " + name + ": rebuilt from pinned source", flush=True)
        for name in sorted({i for values in imports.values() for i in values if i not in modules}):
            ensure_external(name)
        save()
        def compile_one(name):
            t = time.monotonic()
            command = [str(lean), "-o", str(out/"lib"/(name+".olean")), name+".lean"]
            p = subprocess.run(command, cwd=out/"src", env=env, capture_output=True, timeout=args.timeout)
            stdout, stderr = p.stdout.decode("utf-8"), p.stderr.decode("utf-8")
            (out/"logs"/(name+".stdout")).write_bytes(p.stdout)
            (out/"logs"/(name+".stderr")).write_bytes(p.stderr)
            row = dict(module=name, source_path=str(modules[name].relative_to(ROOT)),
                       source_sha256=digest(data[name]), source_bytes=len(data[name]),
                       imports=imports[name], local_dependencies=sorted(deps[name]),
                       seconds=round(time.monotonic()-t, 3), exit_code=p.returncode,
                       stdout=stdout, stderr=stderr, stdout_sha256=digest(p.stdout), stderr_sha256=digest(p.stderr),
                       warnings=len(re.findall(r"\bwarning:", stdout+stderr)))
            need(p.returncode == 0 and not re.search(r"\berror:|\bsorryAx\b", stdout+stderr),
                 name + ": compilation failed; see isolated logs")
            row["axiom_reports"] = axiom_reports(name, stdout, len(printed[name]))
            need([r["declaration"] for r in row["axiom_reports"]] == saved_names[name], name + ": declarations differ from saved report")
            row["object_sha256"] = file_hash(out/"lib"/(name+".olean"))
            return row
        pending, done, running = set(modules), set(), {}
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            while pending or running:
                ready = [n for n in order if n in pending and deps[n] <= done]
                for name in ready[:max(0, args.jobs-len(running))]:
                    pending.remove(name)
                    running[pool.submit(compile_one, name)] = name
                need(running, "blocked dependency scheduler")
                completed, _ = wait(running, return_when=FIRST_COMPLETED)
                for future in completed:
                    name = running.pop(future)
                    row = future.result()
                    report["modules"].append(row)
                    done.add(name)
                    print(f"[{len(done)}/{len(modules)}] {name}: PASS ({row['seconds']}s)", flush=True)
                    save()
        need(done == set(modules), "not every discovered module compiled")
        need(all(file_hash(modules[n]) == digest(data[n]) for n in modules), "source changed during build")
        report["modules"].sort(key=lambda r: r["module"])
        report.update(status="PASS", compiled_modules=len(done),
                      axiom_declarations=sum(len(r["axiom_reports"]) for r in report["modules"]),
                      modules_with_only_standard_axioms=len(done)-1,
                      modules_with_explicit_legacy_native_axioms=1,
                      warnings=sum(r["warnings"] for r in report["modules"]))
        save()
        print(f"PASS: all {len(done)} canonical modules; {report['axiom_declarations']} declarations; report {out/'report.json'}")
    except Exception as exc:
        report.update(status="FAIL", error=str(exc))
        report["uncompleted_modules"] = sorted(set(report.get("discovered_modules", [])) - {r["module"] for r in report["modules"]})
        save()
        raise


if __name__ == "__main__":
    main()
