#!/usr/bin/env python3
"""Replay finite and formal certificates for the four-family theorem.

This checks an author's bounded certificates, not the complete written
proof or historical priority. The manifest is verified before execution.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError('PHASE257_REJECT ' + message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--gap', type=Path, required=True)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--packages', type=Path, required=True)
    parser.add_argument('--verify-primary', action='store_true')
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output path')
    out = args.out.resolve()
    need(not out.exists(), 'fresh resolved output path')
    out.mkdir(parents=True)
    manifest = json.loads((ROOT / 'phase257_manifest.json').read_bytes())

    def bound(row):
        rel = PurePosixPath(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts, 'relative artifact path')
        path = ROOT / rel
        need(path.stat().st_size == row['bytes'] and digest(path) == row['sha256'],
             'bound bytes: ' + str(rel))

    for row in manifest['exports']:
        bound(row)
    retained = [row for row in manifest['retained_bindings']
                if args.verify_primary or not row['path'].startswith('sources/')]
    for row in retained:
        bound(row)
    ledger = json.loads((ROOT / 'phase257_source_ledger.json').read_bytes())
    need(len(ledger['clauses']) == 12, 'twelve source/interface dispositions')
    for name, row in ledger['proof_spans'].items():
        data = b''.join((ROOT / row['path']).read_bytes().splitlines(keepends=True)
                        [row['start_line'] - 1:row['end_line']])
        need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'],
             'proof span ' + name)
    need(all(all(span in ledger['proof_spans'] for span in clause['proof_spans'])
             for clause in ledger['clauses']), 'clause span references')
    executions = []

    def run(label, command, env=None, timeout=240):
        start = time.monotonic()
        result = subprocess.run([str(x) for x in command], cwd=out, env=env,
                                capture_output=True, text=True, timeout=timeout)
        stdout, stderr = out / (label + '.stdout'), out / (label + '.stderr')
        stdout.write_text(result.stdout)
        stderr.write_text(result.stderr)
        executions.append(dict(label=label, returncode=result.returncode,
                               seconds=round(time.monotonic() - start, 4),
                               stdout_sha256=digest(stdout), stderr_sha256=digest(stderr)))
        return result

    version_program = out / 'gap_version.g'
    version_program.write_text('Print(GAPInfo.Version,"\\n");QUIT_GAP(0);\n')
    result = run('gap_version', [args.gap, '-q', '-T', version_program])
    need(result.returncode == 0 and result.stdout.strip() == '4.15.1', 'GAP version 4.15.1')
    program = ROOT / 'phase257_families.g'
    result = run('families', [args.gap, '-q', '-T', program])
    need(result.returncode == 0 and 'PHASE257_FAMILIES_PASS SAMPLES16' in result.stdout
         and not re.search(r'Error|warning', result.stdout + result.stderr), 'finite family replay')
    rows = re.findall(r'P257_SAMPLE (\w+) PRIME (\d+) ORDER (\d+) ENDS\s*\[\s*(\d+),\s*(\d+)\s*\]',
                      result.stdout)
    expected = dict(PGL_PGL=[7, 11, 19, 31], PSL_PGL=[5, 17, 29, 53],
                    S4_PGL=[11, 13, 19, 37], A5_PGL=[11, 29, 31, 89])
    need(len(rows) == 16, 'sixteen parsed marked groups')
    observed = {}
    for tag, prime, whole, left, right in rows:
        p, n, a, b = map(int, [prime, whole, left, right])
        need(tag in expected and n == p * (p*p - 1) and b == n, 'whole and right end')
        wanted = dict(PGL_PGL=n, PSL_PGL=n//2, S4_PGL=24, A5_PGL=60)[tag]
        need(a == wanted, 'left end for ' + tag)
        observed.setdefault(tag, []).append(p)
    need(observed == expected, 'exact finite scope')

    # Changing the constructed object must fail actual algebraic checks.
    text = program.read_text()
    bad = text.replace('[[1,-2],[2,-1]]', '[[1,-2],[2,0]]')
    need(bad != text, 'matrix mutation applied')
    path = out / 'bad_matrix.g'
    path.write_text(bad)
    result = run('control_matrix', [args.gap, '-q', '-T', path])
    need(result.returncode != 0 and 'PHASE257_REJECT four distinct involutions' in result.stdout,
         'altered matrix rejected')
    bad = text.replace('r:=List(mats,M->Image(X.hom,M));',
                       'r:=List(mats,M->Image(X.hom,M));r[4]:=r[1];')
    need(bad != text, 'mark collapse applied')
    path = out / 'bad_marking.g'
    path.write_text(bad)
    result = run('control_marking', [args.gap, '-q', '-T', path])
    need(result.returncode != 0 and 'PHASE257_REJECT four distinct involutions' in result.stdout,
         'collapsed marking rejected')

    pins = json.loads((ROOT / 'formal/dependency_manifest.json').read_bytes())
    dependencies = []
    for row in pins['packages']:
        path = args.packages / row['name']
        revision = subprocess.check_output(['git', '-C', path, 'rev-parse', 'HEAD'], text=True).strip()
        need(revision == row['rev'], 'dependency revision ' + row['name'])
        need(subprocess.run(['git', '-C', path, 'diff', '--quiet', 'HEAD', '--']).returncode == 0,
             'clean dependency source ' + row['name'])
        dependencies.append(dict(name=row['name'], rev=revision))
    lean_version = subprocess.check_output([args.lean, '--version'], text=True).strip()
    need('version 4.32.2,' in lean_version, 'Lean version')
    source = ROOT / 'phase257_formal/FourProjectiveMarks.lean'
    lean_text = source.read_text()
    need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', lean_text, re.M),
         'formal proof-hole scan')
    target = out / source.name
    target.write_text(lean_text)
    env = dict(os.environ)
    env['LEAN_PATH'] = os.pathsep.join(str(path / '.lake/build/lib/lean')
                                     for path in args.packages.iterdir()
                                     if (path / '.lake/build/lib/lean').is_dir())
    result = run('formal', [args.lean, '-o', out / 'FourProjectiveMarks.olean', target], env=env)
    need(result.returncode == 0 and not re.search(r'error:|warning:|sorryAx', result.stdout + result.stderr),
         'clean formal compilation')
    axioms = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", result.stdout)
    need(len(axioms) == 11 and all(set(re.findall(r'[\w.]+', body)) <=
         {'propext', 'Classical.choice', 'Quot.sound'} for _, body in axioms),
         'eleven standard-axiom declarations')
    # The false p | n+1 period is already contradicted by n=0.
    changed = lean_text.replace('↔ p ∣ n := by', '↔ p ∣ (n + 1) := by')
    need(changed != lean_text, 'false period mutation applied')
    control = out / 'FalsePeriod.lean'
    control.write_text(changed)
    result = run('control_period', [args.lean, control], env=env)
    need(result.returncode != 0 and 'error:' in result.stdout, 'false projective period rejected')
    report = dict(status='PASS', scope='Finite and scoped formal certificates; written proof independently reviewed separately.',
                  exports_checked=len(manifest['exports']), retained_checked=len(retained),
                  primary_checked=args.verify_primary, source_clauses=12,
                  samples=observed, parsed_orders=rows, executions=executions,
                  dependencies=dependencies, lean_version=lean_version, gap_version='4.15.1',
                  axiom_reports=axioms,
                  controls=['altered nonscalar matrix rejected', 'collapsed fourth marker rejected',
                            'false lower-unipotent projective period rejected'],
                  limits=['Not a Lean proof of all four infinite families.',
                          'Finite samples do not establish the all-prime quantifiers.',
                          'Giudici, finite Coxeter presentations, quadratic characters and Dirichlet are retained.',
                          'One answer to the bound source conjecture, no historical-priority or compression claim.'])
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status='PASS', samples=16, lean_declarations=11,
                          report=str(out / 'report.json'))))


if __name__ == '__main__':
    main()
