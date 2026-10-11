#!/usr/bin/env python3
"""Read-only bounded Topic B publication review; no Lean/PDF rebuild.

The in-memory load overrides test semantic guards independently of byte
bindings. They do not modify the checkout or model an attacker changing the
global publication manifest.
"""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
BASELINE = '9d33ab1'
PINS = {
    'papers/topic-b/v2/manifest.json':
        '9029bb003c3b419bb9aa3b2edeefca473b2143b25cc6b30dab0c9dfd663e02c0',
    'papers/topic-b/v2/mapping_correction/manifest.json':
        '2f958b2991b71c983efa09984629045f4c1b748b1eddd29b8555b4b868f15750',
    'audit/topic-b/v2/independent_review/manifest.json':
        'd224742e25167983954dc1421cbb4a09853aad47feb5ef9b84378249e6d1e6c5'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dump(node):
    return ast.dump(node, include_attributes=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--public-root', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    a = ap.parse_args()
    root = a.public_root.resolve()
    need(not a.out.exists() and not a.out.is_symlink(), 'fresh output')
    path = root / 'scripts/verify_snapshot.py'
    spec = importlib.util.spec_from_file_location('topic_b_snapshot_review', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    actual = module.load
    admission = actual('audit/topic-b/v2/admission.json')
    module.check_bindings(admission['artifacts'])
    preserved = 0
    for name, expected in PINS.items():
        need(digest((root / name).read_bytes()) == expected, 'independently pinned packet: ' + name)
        manifest = actual(name)
        for row in manifest['exports']:
            p = root / Path(name).parent / row['path']
            need(p.stat().st_size == row['bytes'] and digest(p.read_bytes()) == row['sha256'],
                 'exact frozen export: ' + str(p))
            preserved += 1
    need(module.check_topic_b_proofs() == (30, 6), 'positive B check')
    need(module.check_catalogue() == (10, 21), 'positive catalogue check')

    previous = subprocess.check_output(
        ['git', 'show', BASELINE + ':scripts/verify_snapshot.py'], cwd=root, text=True)
    current = path.read_text()
    old = {n.name: n for n in ast.parse(previous).body if isinstance(n, ast.FunctionDef)}
    new = {n.name: n for n in ast.parse(current).body if isinstance(n, ast.FunctionDef)}
    need(set(new) - set(old) == {'check_topic_b_proofs'}, 'only one new verifier function')
    need(set(old) <= set(new), 'old verifier functions preserved')
    need(all(dump(old[k]) == dump(new[k]) for k in old if k != 'main'),
         'every old non-main function AST unchanged')
    filtered = copy.deepcopy(new['main'])
    original_statements = [dump(n) for n in old['main'].body]
    extra = [n for n in filtered.body if dump(n) not in original_statements]
    need(len(extra) == 2 and any('check_topic_b_proofs' in dump(n) for n in extra)
         and any('b_declarations' in dump(n) for n in extra), 'only B call and result line added')
    filtered.body = [n for n in filtered.body if dump(n) in original_statements]
    need(dump(filtered) == dump(old['main']), 'old main order and statements preserved')
    for name in ['scripts/build_papers.py', 'research/case_study/formal/lakefile.lean']:
        previous_bytes = subprocess.check_output(['git', 'show', BASELINE + ':' + name], cwd=root)
        need(previous_bytes == (root / name).read_bytes(), 'unchanged existing build: ' + name)

    catalogue = actual('papers/catalogue.json')
    previous_catalogue = json.loads(subprocess.check_output(
        ['git', 'show', BASELINE + ':papers/catalogue.json'], cwd=root))
    expected = [('umbrella', 'U_B', [], 5),
                ('inductively-minimal-geometries', 'B1', ['N001'], 3),
                ('maximal-symmetric-markings', 'B2', ['N003'], 5),
                ('frattini-coordinate-geometries', 'B3', ['N008'], 4),
                ('disjoint-subset-geometries', 'B4', ['L030'], 5)]
    rows = [r for r in catalogue['new_editions'] if r['topic'] == 'B']
    need([(r['id'].split('/')[-1], r['application_id'], r['source_contracts'], r['physical_pages'])
          for r in rows] == expected, 'five exact B scope/page entries')
    need(catalogue['current_topic_editions']['B'] == [r['id'] for r in rows],
         'current B edition routes to all five papers')
    stripped = copy.deepcopy(catalogue)
    stripped['new_editions'] = [r for r in stripped['new_editions'] if r['topic'] != 'B']
    del stripped['current_topic_editions']['B']
    need(stripped == previous_catalogue, 'catalogue unchanged outside five B entries/current route')

    replay = actual(admission['root_public_replay'])
    independent = actual('audit/topic-b/v2/independent_review/author_replay.json')
    for key in ['axioms', 'source_sha256', 'rendered', 'finite_hypothesis_countermodels']:
        need(replay[key] == independent[key], 'fresh public/independent agreement: ' + key)
    need(admission['compression_ratio'] is None and admission['external_proof_cost'] is None,
         'no invented measured or external cost')
    need(admission['new_source_credit'] == admission['new_question_credit'] == 0,
         'no new credits')
    need(admission['formal_scope']['canonical_default_library_modules_unchanged'] == 100 and
         not admission['formal_scope']['complete_source_contract_formalized'],
         'separate scoped formal module')
    need(admission['authoritative_source_map'] ==
         'papers/topic-b/v2/mapping_correction/source_contract_map.json', 'corrected map route')

    cases = [
        ('invented_ratio', 'audit/topic-b/v2/admission.json', lambda d: d.update(compression_ratio=2)),
        ('new_credit', 'audit/topic-b/v2/admission.json', lambda d: d.update(new_source_credit=1)),
        ('wrong_delta_hash', 'audit/topic-b/v2/admission.json',
         lambda d: d.update(mapping_correction_manifest_sha256='0' * 64)),
        ('wrong_review_hash', 'audit/topic-b/v2/admission.json',
         lambda d: d.update(independent_review_manifest_sha256='0' * 64)),
        ('old_map_route', 'audit/topic-b/v2/admission.json',
         lambda d: d.update(authoritative_source_map='papers/topic-b/v2/source_contract_map.json')),
        ('custom_axiom', admission['root_public_replay'],
         lambda d: d['axioms'][0]['axioms'].append('sorryAx')),
        ('missing_declaration', admission['root_public_replay'], lambda d: d['axioms'].pop()),
        ('missing_control', admission['root_public_replay'], lambda d: d['executions'].pop()),
        ('altered_source_clause', admission['authoritative_source_map'],
         lambda d: d['rows'][0].update(source_contract='ALTERED')),
        ('wrong_catalogue_source', 'papers/catalogue.json',
         lambda d: next(r for r in d['new_editions'] if r.get('application_id') == 'B1').update(source_contracts=['N008'])),
        ('incomplete_current_edition', 'papers/catalogue.json',
         lambda d: d['current_topic_editions']['B'].pop())]
    controls = []
    for name, route, edit in cases:
        changed = copy.deepcopy(actual(route))
        edit(changed)
        module.load = lambda p, route=route, changed=changed: (
            copy.deepcopy(changed) if str(p) == route else actual(p))
        try:
            module.check_topic_b_proofs()
        except (ValueError, KeyError) as exc:
            controls.append({'name': name, 'rejected': True, 'reason': str(exc)})
        else:
            controls.append({'name': name, 'rejected': False})
        finally:
            module.load = actual
    need(all(r['rejected'] for r in controls), 'all semantic controls rejected: ' + str(controls))
    paths = ['scripts/verify_snapshot.py', 'papers/catalogue.json',
             'papers/topic-b/v2/README.rst', 'audit/topic-b/v2/admission.json'] + list(PINS)
    bindings = [{'path': n, 'bytes': (root / n).stat().st_size,
                 'sha256': digest((root / n).read_bytes())} for n in paths]
    report = dict(status='PASS_BOUNDED_TOPIC_B_PUBLICATION_INTEGRATION',
                  baseline_commit=subprocess.check_output(
                      ['git', 'rev-parse', BASELINE], cwd=root, text=True).strip(),
                  reviewed_public_bindings=bindings, frozen_exports_preserved=preserved,
                  admission_artifact_bindings=len(admission['artifacts']),
                  clauses=30, reported_declarations=6, catalogue_result=[10, 21],
                  unchanged_old_verifier_functions=len(old) - 1,
                  old_main_statements_preserved=True, existing_build_unchanged=True,
                  public_replay_matches_independent=True,
                  semantic_controls=controls,
                  semantic_controls_use_in_memory_load_overrides=True,
                  full_mathematical_or_compiler_replay_repeated=False,
                  public_files_changed_by_review=False,
                  root_summary_documents_reviewed=False)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in
                      ['reviewed_public_bindings', 'semantic_controls']}))


if __name__ == '__main__':
    main()
