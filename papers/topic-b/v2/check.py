#!/usr/bin/env python3
"""Replay the finite hypothesis controls, actual Lean proof and TeX bindings.

No finite enumeration is an input to a uniform theorem in this volume.
The small models below test necessity of hypotheses of UB.Relative.
"""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError('TOPIC_B_REJECT: ' + message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subsets(items):
    items = list(items)
    return [set(x) for n in range(len(items) + 1)
            for x in itertools.combinations(items, n)]


def span(elements):
    values, pending = {0}, [0]
    for a in pending:
        for b in elements:
            c = a ^ b
            if c not in values:
                values.add(c)
                pending.append(c)
    return values


def model(order, stabilizers, chosen):
    G = set(range(order))
    need(order in (2, 4), 'only declared XOR groups')
    # Check the group and every subgroup used, rather than accepting their labels.
    need(all((a ^ b) ^ c == a ^ (b ^ c) for a, b, c in
             itertools.product(G, repeat=3)), 'group associativity')
    subgroups = [H for H in subsets(G) if 0 in H and
                 all(a ^ b in H for a in H for b in H)]
    need(all(P in subgroups for P in stabilizers), 'literal stabilizers')
    I = set(range(len(stabilizers)))
    need(len(chosen) == len(I), 'one choice per type')

    def fixed(S):
        return set.intersection(G, *(stabilizers[i] for i in I - S))

    def maximal(A, B):
        return A < B and all(not A <= H <= B or H in (A, B)
                             for H in subgroups)

    hmem = all(chosen[i] in stabilizers[j] for i in I for j in I if i != j)
    hout = all(chosen[i] not in stabilizers[i] for i in I)
    hmax = all(any(maximal(fixed(S - {i}), fixed(S)) for i in S)
               for S in subsets(I) if S)
    borel = fixed(set())
    generated = span(borel | set(chosen))
    return dict(group_order=order, stabilizers=[sorted(x) for x in stabilizers],
                chosen=chosen, off_diagonal_membership=hmem, outside=hout,
                residual_maximality=hmax, generated_order=len(generated),
                whole_group_generated=generated == G,
                all_subgroups_checked=len(subgroups))


def controls(altered=False):
    rows = [model(4, [{0}], [1]), model(2, [{0}], [1 if altered else 0]),
            model(4, [{0, 1}, {0, 2}], [3, 3])]
    expected = [(True, True, False), (True, False, True), (False, True, True)]
    for row, hyp in zip(rows, expected):
        need(tuple(row[k] for k in ('off_diagonal_membership', 'outside',
                                   'residual_maximality')) == hyp,
             'countermodel hypotheses exactly as declared')
        need(not row['whole_group_generated'], 'false weakening really fails')
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--lean', type=Path, default=Path(
        '/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'))
    ap.add_argument('--packages', type=Path, default=Path(
        '/Users/sasha/bogachev/formal/.lake/packages'))
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--xelatex', type=Path, default=Path('/opt/homebrew/bin/xelatex'))
    ap.add_argument('--verify-primary', action='store_true')
    ap.add_argument('--sources-root', type=Path, default=ROOT.parent)
    args = ap.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output directory')
    out = args.out.resolve()
    out.mkdir(parents=True)
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    for row in manifest['exports']:
        p = ROOT / row['path']
        need(p.is_file() and p.stat().st_size == row['bytes'] and sha(p) == row['sha256'],
             'bound export ' + row['path'])
    if args.verify_primary:
        for row in manifest['private_retained_bindings']:
            p = args.sources_root / row['path']
            need(p.is_file() and sha(p) == row['sha256'], 'private source ' + row['path'])
    proof_map = json.loads((ROOT / 'proof_map.json').read_text())
    nodes = {row['id']: row for row in proof_map['nodes']}
    external = {row['id'] for row in proof_map['external_inputs']}
    need(len(nodes) == 29 and len(nodes) == len(proof_map['nodes']), '29 unique proof nodes')
    for row in nodes.values():
        body = (ROOT / row['file']).read_text()
        span_text = body[row['start_codepoint']:row['end_codepoint_exclusive']]
        need(hashlib.sha256(span_text.encode()).hexdigest() == row['sha256_utf8'],
             'actual complete TeX span ' + row['id'])
        need(all(n in nodes or n in external for n in row['direct_dependencies']),
             'declared proof dependency ' + row['id'])
    contract = json.loads((ROOT / 'source_contract_map.json').read_text())
    need(len(contract['rows']) == 30 and len({r['adapter'] for r in contract['rows']}) == 30,
         'exact 30-row source contract')
    for row in contract['rows']:
        need([n['id'] for n in row['new_tex_spans']] == row['new_tex_nodes'],
             'complete row proof mapping ' + row['adapter'])
        for item in row['new_tex_spans']:
            need(all(nodes[item['id']][k] == v for k, v in item.items()),
                 'source row span equals proof map ' + row['adapter'])
    if args.verify_primary:
        previous = json.loads((args.sources_root / 'phase141_module_B_review.json').read_text())
        original = {row['adapter']: row for row in previous['source_contracts']}
        for row in contract['rows']:
            need(all(row[k] == original[row['adapter']][k] for k in
                     ('source_id', 'source_reference', 'source_contract', 'verdict', 'source_span')),
                 'unaltered accepted source clause ' + row['adapter'])
    scope = json.loads((ROOT / 'formal/scope.json').read_text())
    pins = json.loads((ROOT / 'formal/dependency_manifest.json').read_text())
    for row in pins['packages']:
        p = args.packages / row['name']
        rev = subprocess.check_output(['git', '-C', p, 'rev-parse', 'HEAD'], text=True).strip()
        need(rev == row['rev'], 'package revision ' + row['name'])
        need(subprocess.run(['git', '-C', p, 'diff', '--quiet', 'HEAD', '--']).returncode == 0,
             'tracked package change ' + row['name'])
    version = subprocess.check_output([args.lean, '--version'], text=True).strip()
    need('version 4.32.2,' in version, 'pinned Lean')
    env = dict(os.environ)
    env['LEAN_PATH'] = os.pathsep.join(str(p / '.lake/build/lib/lean')
        for p in args.packages.iterdir() if (p / '.lake/build/lib/lean').is_dir())
    source = (ROOT / 'formal/ResidualGeneration.lean').read_text()
    need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', source, re.M),
         'no proof hole or custom axiom')
    runs = []

    def compile_case(label, content, positive):
        p = out / (label + '.lean')
        p.write_text(content)
        start = time.monotonic()
        r = subprocess.run([args.lean, '-o', p.with_suffix('.olean'), p], cwd=out,
                           env=env, text=True, capture_output=True, timeout=180)
        for key, data in [('stdout', r.stdout), ('stderr', r.stderr)]:
            (out / (label + '.' + key)).write_text(data)
        runs.append(dict(label=label, returncode=r.returncode,
                         seconds=round(time.monotonic() - start, 3)))
        if positive:
            need(r.returncode == 0 and not re.search('warning:|error:|sorryAx', r.stdout + r.stderr),
                 'clean actual theorem compilation')
        else:
            need(r.returncode != 0 and 'error:' in r.stdout + r.stderr,
                 'false weakening rejected: ' + label)
        return r

    positive = compile_case('ResidualGeneration', source, True)
    axioms = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", positive.stdout)
    need([name for name, _ in axioms] == scope['reported_declarations'],
         'exact six declaration reports')
    need(all(set(re.findall(r'[\w.]+', a)) <= {'propext', 'Classical.choice', 'Quot.sound'}
             for _, a in axioms), 'standard axioms only')
    hypotheses = {
        'without_membership': '(hmem : ∀ i j, i ≠ j → s i ∈ P j)',
        'without_outside': '(hout : ∀ i, s i ∉ P i)',
        'without_maximality': '(hmax : ∀ S : Finset I, S.Nonempty →\n'
                             '      ∃ i ∈ S, MaximalIn (fixed P (S.erase i)) (fixed P S))'}
    for label, old in hypotheses.items():
        need(old in source, 'exact weakening target ' + label)
        binder = old[1:old.index(' :')]
        compile_case(label, source.replace(old, '(' + binder + ' : True)'), False)
    finite = controls()
    rejected = False
    try:
        controls(altered=True)
    except RuntimeError as exc:
        rejected = 'countermodel hypotheses' in str(exc)
    need(rejected, 'altered finite witness rejected')

    rendered = []
    if args.render:
        from pypdf import PdfReader
        documents = json.loads((ROOT / 'documents.json').read_text())['documents']
        for row in documents:
            job = out / row['id']
            job.mkdir()
            for item in row['tex_inputs']:
                p = job / item
                p.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / item, p)
            for turn in range(2):
                run = subprocess.run([args.xelatex, '-interaction=nonstopmode',
                    '-halt-on-error', row['tex']], cwd=job, capture_output=True, text=True,
                    timeout=120)
                (job / ('render-' + str(turn + 1) + '.txt')).write_text(run.stdout + run.stderr)
                need(run.returncode == 0, 'render ' + row['id'])
            log = (job / Path(row['tex']).with_suffix('.log')).read_text()
            need(not re.search(r'Missing character:|Overfull \\[hv]box|undefined references|'
                               r'Label\(s\) may have changed|LaTeX Warning: Reference', log),
                 'clean final glyph/layout/reference diagnostics ' + row['id'])
            pdf = job / Path(row['tex']).with_suffix('.pdf')
            pages = [p.extract_text() for p in PdfReader(pdf).pages]
            old = [p.extract_text() for p in PdfReader(ROOT / row['pdf']).pages]
            need(pages == old, 'every-page authoritative text equality ' + row['id'])
            need(not any('\ufffd' in p for p in pages), 'no replacement glyph ' + row['id'])
            rendered.append(dict(id=row['id'], pages=len(pages),
                                 page_text_sha256=[hashlib.sha256(p.encode()).hexdigest() for p in pages]))
    report = dict(status='PASS', author_manifest_sha256=sha(ROOT / 'manifest.json'),
        lean_version=version, source_sha256=sha(ROOT / 'formal/ResidualGeneration.lean'),
        axioms=[dict(name=n, axioms=re.findall(r'[\w.]+', a)) for n, a in axioms],
        executions=runs, finite_hypothesis_countermodels=finite,
        altered_countermodel_rejected=rejected, rendered=rendered,
        scope='UB.Relative subgroup induction and corollaries only; geometry and source applications remain written mathematics.',
        verified_source_rows=30, verified_tex_proof_spans=29,
        required_mathematical_computation=False, new_source_credits=0, new_question_credits=0)
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status='PASS', declarations=6, controls=4,
                         rendered_documents=len(rendered), report=str(out / 'report.json'))))


if __name__ == '__main__':
    main()
