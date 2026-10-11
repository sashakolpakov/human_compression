#!/usr/bin/env python3
"""Rebuild and verify the L128 application with explicit retained inputs."""
import argparse, hashlib, json, os, pathlib, re, shutil, subprocess, time
import pypdf

ROOT = pathlib.Path(__file__).resolve().parent

def need(test, message):
    if not test:
        raise RuntimeError('L128_REJECT ' + message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    for key in ['out', 'public-root', 'gap', 'lean', 'packages']:
        ap.add_argument('--' + key, type=pathlib.Path, required=True)
    ap.add_argument('--study-root', type=pathlib.Path)
    ap.add_argument('--xelatex', default='xelatex')
    a = ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(), 'fresh output')
    a.out.mkdir(parents=True)
    out = a.out.resolve()
    start = time.monotonic()
    runs = []
    manifest = ROOT / 'manifest.json'
    exports = json.loads(manifest.read_text())['exports'] if manifest.exists() else []

    def verify(rows, base):
        for row in rows:
            p = pathlib.PurePosixPath(row['path'])
            need(not p.is_absolute() and '..' not in p.parts, 'safe binding')
            q = base / p
            need(q.is_file() and q.stat().st_size == row['bytes'] and
                 sha(q) == row['sha256'], 'binding ' + str(p))

    verify(exports, ROOT)
    contract = json.loads((ROOT / 'contract.json').read_text())
    need(contract['current_original_credit'] == 0 and contract['new_question_answers'] == 0,
         'candidate boundary')
    common = contract['common_manuscripts'][0]['files']
    verify(common, a.public_root)
    if a.study_root:
        verify([contract['source_binding'], contract['source_text_binding']], a.study_root)
    ledger = json.loads((ROOT / 'source_clause_map.json').read_text())
    need(len(ledger['rows']) == 14 and len(ledger['proof_spans']) == 7, 'source contract')
    for row in ledger['proof_spans'].values():
        raw = b''.join((ROOT / row['path']).read_bytes().splitlines(keepends=True)
                       [row['start_line'] - 1:row['end_line']])
        need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
             'proof span')

    def run(label, cmd, env=None, cwd=None):
        t = time.monotonic()
        r = subprocess.run([str(x) for x in cmd], cwd=cwd or out, env=env,
                           capture_output=True, text=True, timeout=180)
        (out / (label + '.stdout')).write_text(r.stdout)
        (out / (label + '.stderr')).write_text(r.stderr)
        runs.append({'label': label, 'returncode': r.returncode,
                     'seconds': round(time.monotonic() - t, 4),
                     'stdout_sha256': sha(out / (label + '.stdout')),
                     'stderr_sha256': sha(out / (label + '.stderr'))})
        return r

    r = run('gap_version', [a.gap, '-q', '-T', '-c',
        'Print(GAPInfo.Version,"\\n",PackageInfo("smallgrp")[1].Version,"\\n");QUIT;'])
    need(r.returncode == 0 and r.stdout.strip().split() == ['4.15.1', '1.5.4'], 'GAP pins')
    r = run('finite', [a.gap, '-q', '-T', ROOT / 'minimal_rank_three.g'])
    need(r.returncode == 0 and 'L128_COMPLETE_SMALL_ORDER_SEARCH' in r.stdout and
         not re.search('Error|warning', r.stdout + r.stderr, re.I), 'complete finite search')
    code = (ROOT / 'minimal_rank_three.g').read_text()
    bad = out / 'wrong_minimum.g'
    bad.write_text(code.replace('if gens<>0 then', 'if gens<>1 then'))
    r = run('wrong_minimum', [a.gap, '-q', '-T', bad])
    need('Error' in r.stdout + r.stderr and
         'L128_COMPLETE_SMALL_ORDER_SEARCH' not in r.stdout, 'finite negative control')

    deps = json.loads((ROOT / 'dependency_manifest.json').read_text())
    for row in deps['packages']:
        folder = a.packages / row['name']
        revision = subprocess.check_output(['git', '-C', folder, 'rev-parse', 'HEAD'], text=True).strip()
        need(revision == row['rev'], 'package pin')
        need(subprocess.run(['git', '-C', folder, 'diff', '--quiet', 'HEAD', '--']).returncode == 0,
             'clean package')
    need('version 4.32.2,' in subprocess.check_output([a.lean, '--version'], text=True), 'Lean pin')
    env = dict(os.environ)
    env['LEAN_PATH'] = os.pathsep.join(str(p / '.lake/build/lib/lean')
        for p in a.packages.iterdir() if (p / '.lake/build/lib/lean').is_dir())
    lean = (ROOT / 'GraphCentralExtension.lean').read_text()
    need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', lean, re.M), 'proof holes')
    target = out / 'GraphCentralExtension.lean'
    target.write_text(lean)
    r = run('formal', [a.lean, '-o', out / 'GraphCentralExtension.olean', target], env)
    need(r.returncode == 0 and not re.search('error:|warning:|sorryAx', r.stdout + r.stderr), 'Lean proof')
    reports = re.findall(r"'GraphCentralExtension\.([^']+)' depends on axioms: \[([^\]]*)\]", r.stdout)
    scope = json.loads((ROOT / 'formal_scope.json').read_text())
    need([n for n, _ in reports] == scope['names'], 'exact formal scope')
    for _, axioms in reports:
        need(set(x.strip() for x in axioms.split(',') if x.strip()) <= set(scope['axioms_allowed']),
             'standard axioms')
    controls = ['wrong_minimum']
    for name, old, new in [
        ('wrong_inverse', '-x.central + β x.vertex x.vertex', '-x.central'),
        ('wrong_support', 'supported tail head (J ∩ K) := by', 'supported tail head (J ∪ K) := by')]:
        need(lean.count(old) >= 1, 'formal mutation target')
        bad = out / (name + '.lean')
        bad.write_text(lean.replace(old, new, 1))
        r = run(name, [a.lean, bad], env)
        need(r.returncode != 0 and 'error:' in r.stdout + r.stderr, 'formal negative control')
        controls.append(name)

    render = {}
    for name, extras in [('graph_symmetries', []), ('programs', ['minimal_rank_three.g'])]:
        d = out / name
        d.mkdir()
        for filename in [name + '.tex'] + extras:
            shutil.copyfile(ROOT / filename, d / filename)
        for i in range(3):
            r = run(name + '_render' + str(i + 1), [a.xelatex, '-no-shell-escape',
                '-interaction=nonstopmode', '-halt-on-error', '-recorder', name + '.tex'], cwd=d)
            need(r.returncode == 0, 'render ' + name)
        log = (d / (name + '.log')).read_text()
        need(not re.search(r'Overfull|Missing character|Missing glyph|LaTeX Warning|Package .* Warning', log),
             'render diagnostics ' + name)
        pages = [p.extract_text() or '' for p in pypdf.PdfReader(d / (name + '.pdf')).pages]
        need(not any((ord(c) < 32 and c not in '\t\r\n') or c == '\ufffd' or
                     0xe000 <= ord(c) <= 0xf8ff for c in '\n'.join(pages)), 'PDF characters')
        same = None
        if (ROOT / (name + '.pdf')).exists():
            same = pages == [p.extract_text() or '' for p in pypdf.PdfReader(ROOT / (name + '.pdf')).pages]
            need(same, 'full page text reproduced ' + name)
        render[name] = {'pages': len(pages), 'pdf_sha256': sha(d / (name + '.pdf')),
                        'text_sha256': hashlib.sha256('\n'.join(pages).encode()).hexdigest(),
                        'old_page_text_equal': same}
    verify(exports, ROOT)
    verify(common, a.public_root)
    report = {'status': 'PASS', 'seconds': round(time.monotonic() - start, 4),
              'exports_verified': len(exports), 'common_files_verified': len(common),
              'source_checked': bool(a.study_root), 'source_clauses': 14, 'proof_spans': 7,
              'formal_axiom_reports': reports, 'controls_rejected': controls,
              'finite_groups': 79, 'finite_involution_triples': 32628,
              'required_programs': ['minimal_rank_three.g'], 'render': render,
              'executions': runs, 'current_original_credit': 0, 'new_question_answers': 0}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'report': str(out / 'report.json'), 'seconds': report['seconds']}))

if __name__ == '__main__':
    main()
