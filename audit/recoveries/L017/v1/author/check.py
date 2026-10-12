#!/usr/bin/env python3
"""Portable bounded replay of the complete L017 author proposal.

No primary PDF/text/font is exported. The optional study-root binds the supplied
source. New exact finite construction and graph certificates are rerun; unchanged
accepted predecessor computations are not. Native rendering is opt-in.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bindings(root, rows):
    for row in rows:
        p = root / row['path']
        require(p.is_file(), 'missing payload: ' + row['path'])
        require(p.stat().st_size == row['bytes'] and digest(p) == row['sha256'],
                'changed whole payload: ' + row['path'])
    return len(rows)


def run(command, cwd, timeout=120):
    p = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    require(p.returncode == 0, 'command failed: ' + repr(command) + '\n' + p.stdout + p.stderr)
    return p.stdout + p.stderr


def metadata(root):
    scope = json.loads((root / 'scope.json').read_text())
    require(scope['source_authors'] == ['Dimitri Leemans', 'Klara Stokes', 'Philippe Tranchida'],
            'complete source attribution')
    require(scope['new_original_credit'] == scope['new_question_credit'] == scope['new_lean_declarations'] == 0,
            'no automatic new credit')
    require(scope['compression_factor'] is None and scope['source_software_cost'] is None,
            'unknown cost is not zero; no ratio')
    source = json.loads((root / 'source_map.json').read_text())
    require(len(source['rows']) == 53 and source['named_result_count'] == 13, 'complete disposition roster')
    named = {row['source_label'] for row in source['rows']}
    require(all((('Theorem' if n in (11, 13) else 'Lemma') + f' 3.{n}') in named for n in range(1, 14)),
            'all thirteen named source results')
    require(source['source_pdf']['pages'] == 17, 'whole primary edition')
    require(len([row for row in source['rows'] if row['disposition'] == 'REFUTED_BY_COMPLETE_NORMALIZED_MARKING_EXHAUSTION']) == 1,
            'literal q7 negative scope is explicit')
    return scope, source


def native(root, out, compiler):
    from pypdf import PdfReader
    rows = json.loads((root / 'native.json').read_text())
    reports = []
    for number, row in enumerate(rows):
        tex = root / row['tex']
        build = out / f'native-{number}'
        build.mkdir()
        command = [compiler, '-interaction=nonstopmode', '-halt-on-error',
                   '-output-directory=' + str(build), tex.name]
        run(command, tex.parent)
        run(command, tex.parent)
        log = (build / (tex.stem + '.log')).read_text(errors='replace')
        require(not any(s in log for s in ('LaTeX Warning:', 'Overfull', 'Underfull', '! LaTeX Error')),
                'native diagnostics for ' + row['tex'])
        pages = [p.extract_text() or '' for p in PdfReader(build / (tex.stem + '.pdf')).pages]
        actual = [hashlib.sha256(p.encode()).hexdigest() for p in pages]
        require(len(pages) == row['pages'] and actual == row['page_text_sha256'],
                'exact native page texts for ' + row['tex'])
        reports.append({'tex': row['tex'], 'pages': len(pages), 'exact_page_texts': True})
    return reports


def controls(root, out, manifest, compiler):
    accepted = []
    for path in ('absolute_geometry.tex', 'finite_comparison.tex', 'finite_graphs.cpp',
                 'graph_certificate.py', 'automorphism_witnesses.json', 'source_map.json',
                 'scope.json', 'accepted_inputs/odd_completion/odd_completion.tex'):
        row = next(r for r in manifest['exports'] if r['path'] == path)
        bad = dict(row, sha256='0' * 64)
        try:
            bindings(root, [bad])
        except ValueError:
            accepted.append('whole-byte binding: ' + path)
        else:
            raise ValueError('binding control accepted corruption')

    needed = ['graph_certificate.py', 'automorphism_witnesses.json']
    needed += [p.name for p in root.glob('graph_q*.json')]
    for label in ('actual_edge', 'nonpermutation', 'missing_group_generators', 'invented84vertex_graph'):
        work = out / ('control-' + label)
        work.mkdir()
        for name in needed:
            shutil.copyfile(root / name, work / name)
        if label == 'actual_edge':
            p = work / 'graph_q5_r3.json'; d = json.loads(p.read_text()); d['edges'].pop()
        elif label == 'invented84vertex_graph':
            p = work / 'graph_q7_r0.json'; d = json.loads(p.read_text()); d['edges'] = d['edges'][:42]
        else:
            p = work / 'automorphism_witnesses.json'; d = json.loads(p.read_text())
            if label == 'nonpermutation':
                perm = d['q5_r3_moving']['automorphism_generators'][0]; perm[0] = perm[1]
            else:
                d['q5_r3_moving']['automorphism_generators'] = []
        p.write_text(json.dumps(d) + '\n')
        process = subprocess.run([sys.executable, '-B', '-O', str(work / 'graph_certificate.py'),
                                  '--out', str(work / 'should_not_pass.json')],
                                 capture_output=True, text=True, timeout=30)
        require(process.returncode != 0, 'actual graph control must reject: ' + label)
        accepted.append(label)

    source = (root / 'finite_graphs.cpp').read_text()
    changes = [('nonfield_modulus', '{3,3,0,1}', '{0,3,0,1}'),
               ('wrong_q7_seed', '{57,38,190,228}', '{58,38,190,228}')]
    for label, old, new in changes:
        require(source.count(old) == 1, 'precise C++ mutation locator')
        work = out / ('control-' + label); work.mkdir()
        (work / 'bad.cpp').write_text(source.replace(old, new))
        run([compiler, '-std=c++17', '-O2', '-o', str(work / 'bad'), str(work / 'bad.cpp')], work)
        process = subprocess.run([str(work / 'bad')], cwd=work, capture_output=True, text=True, timeout=30)
        require(process.returncode != 0, 'field/seed control must reject: ' + label)
        accepted.append(label)
    return accepted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--study-root', type=Path)
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--cxx', default=shutil.which('clang++') or 'c++')
    parser.add_argument('--pdflatex', default=shutil.which('pdflatex') or '/opt/homebrew/bin/pdflatex')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    out = args.out.resolve()
    require(not out.exists(), 'output directory must be fresh')
    out.mkdir(parents=True)
    manifest = json.loads((root / 'manifest.json').read_text())
    payloads = bindings(root, manifest['exports'])
    inherited = bindings(root, json.loads((root / 'inherited_bindings.json').read_text()))
    scope, source = metadata(root)
    source_bound = False
    if args.study_root:
        p = args.study_root / source['source_pdf']['path']
        require(digest(p) == source['source_pdf']['sha256'], 'exact original PDF')
        text = args.study_root / 'sources/absolute_triality2024.txt'
        require(digest(text) == source['source_text_sha256'], 'exact read original text')
        source_bound = True

    build = out / 'finite'; build.mkdir()
    run([args.cxx, '-std=c++17', '-O2', '-Wall', '-Wextra', '-o', str(build / 'finite_graphs'),
         str(root / 'finite_graphs.cpp')], build)
    stdout = run([str(build / 'finite_graphs')], build)
    (out / 'finite_stdout.txt').write_text(stdout)
    actual_files = sorted([*build.glob('graph_q*.json'), *build.glob('orbits_q*.json')])
    expected_names = sorted([p.name for p in root.glob('graph_q*.json')] + [p.name for p in root.glob('orbits_q*.json')])
    require([p.name for p in actual_files] == expected_names, 'complete finite output roster')
    for path in actual_files:
        require(json.loads(path.read_text()) == json.loads((root / path.name).read_text()),
                'fresh exact field/coset output: ' + path.name)
    graph_report = out / 'graph_report.json'
    run([sys.executable, '-B', '-O', str(root / 'graph_certificate.py'), '--out', str(graph_report)], root)
    require(json.loads(graph_report.read_text()) == json.loads((root / 'graph_report.json').read_text()),
            'exact fresh complete graph certificate')
    rejected = controls(root, out, manifest, args.cxx)
    renders = native(root, out, args.pdflatex) if args.render else []
    report = {'status': 'PASS', 'whole_export_bindings': payloads, 'exact_inherited_files': inherited,
              'source_dispositions': len(source['rows']), 'named_source_results': 13,
              'exact_primary_bound': source_bound, 'fresh_finite_outputs': len(actual_files),
              'source_marking_q7_exhaustion': 336, 'q7_representatives': 7,
              'actual_full_automorphism_certificates': 6, 'negative_controls': rejected,
              'native': renders, 'new_scientific_credit': 0, 'new_questions': 0,
              'new_lean': 0, 'ratios': None}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
