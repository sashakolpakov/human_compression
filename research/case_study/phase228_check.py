#!/usr/bin/env python3
"""Replay frozen bindings/provenance/scope, not the mathematical proof or Lean kernel."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent
AUTHOR_SHA = 'f24684afc5f8ac39817e04878003feb9bc5becc97e7d204cbb6cc16e468240b9'
STANDARD = {'propext', 'Classical.choice', 'Quot.sound'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def binding(row):
    rel = Path(row['path'])
    require(not rel.is_absolute() and '..' not in rel.parts, 'unsafe binding path')
    data = (ROOT / rel).read_bytes()
    require(digest(data) == row['sha256'], f'hash mismatch: {rel}')
    if 'bytes' in row:
        require(len(data) == row['bytes'], f'byte mismatch: {rel}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path, help='New report path, never overwritten.')
    parser.add_argument('--verify-retained', action='store_true', help='Also require all private retained inputs, including original PDF.')
    parser.add_argument('--rebuild', action='store_true', help='Freshly run the provenance builder; requires both retained predecessor manuscripts.')
    args = parser.parse_args()
    require(not args.out.exists() and not args.out.is_symlink(), 'output already exists or is a symlink')
    out = args.out.resolve()
    require(out.parent.is_dir(), 'output parent must exist')
    author_bytes = (ROOT / 'phase207_export.json').read_bytes()
    require(digest(author_bytes) == AUTHOR_SHA, 'wrong author freeze')
    author = json.loads(author_bytes)
    require(len(author['exports']) == 15 and len(author['retained_bindings']) == 14, 'author binding counts')
    for row in author['exports']:
        binding(row)
    if args.verify_retained:
        for row in author['retained_bindings']:
            binding(row)
    review = read_json('phase228_manifest.json')
    for row in review['exports']:
        binding(row)
    text = (ROOT / 'phase207_topic_A_umbrella.md').read_text(encoding='utf-8')
    provenance = read_json('phase207_umbrella_provenance.json')
    require(digest(text.encode()) == provenance['manuscript_sha256'], 'provenance manuscript binding')
    cursor = 0
    for part in provenance['parts']:
        require(part['start_codepoint'] == cursor, 'gap or overlap in provenance')
        stop = part['end_codepoint_exclusive']
        require(cursor < stop <= len(text), 'bad provenance endpoint')
        data = text[cursor:stop].encode('utf-8')
        require(digest(data) == part['sha256_utf8'] and len(data) == part['utf8_bytes'], 'bad provenance span')
        cursor = stop
    require(cursor == len(text) and len(provenance['parts']) == 22, 'incomplete provenance')
    rebuild = None
    if args.rebuild:
        import tempfile
        with tempfile.TemporaryDirectory(prefix='phase228-builder-') as temp:
            target = Path(temp) / 'output'
            subprocess.run([sys.executable, '-B', '-O', str(ROOT / 'phase207_write_umbrella.py'), '--output-dir', str(target)], cwd=ROOT, check=True, capture_output=True, text=True)
            for name in ('phase207_topic_A_umbrella.md', 'phase207_umbrella_provenance.json'):
                require((target / name).read_bytes() == (ROOT / name).read_bytes(), f'builder not byte exact: {name}')
            rebuild = 'BYTE_EXACT_UMBRELLA_AND_PROVENANCE'
    costs = read_json('phase228_cost_scope.json')
    for name, row in costs['manuscripts'].items():
        data = (ROOT / name).read_bytes()
        normalized = unicodedata.normalize('NFC', data.decode('utf-8'))
        observed = (digest(data), len(data), len(normalized), sum(not c.isspace() for c in normalized), len(normalized.split()))
        expected = tuple(row[k] for k in ('sha256','raw_UTF8_bytes','NFC_characters','NFC_nonwhitespace_characters','NFC_whitespace_tokens'))
        require(observed == expected, f'native metric mismatch: {name}')
    require(costs['ratio'] is None and costs['full_topic_umbrella_charged'], 'cost boundary')
    contract = read_json('phase228_source_contract.json')
    require(contract['author_manifest_sha256'] == AUTHOR_SHA and len(contract['clauses']) == 24, 'contract binding')
    require(contract['credit']['new_principal_sources'] == 0 and contract['credit']['new_open_conjecture_results'] == 0, 'credit inflation')
    require(contract['formal']['new_declarations'] == 0 and not contract['formal']['whole_application_Lean'] and not contract['formal']['whole_umbrella_Lean'], 'formal overclaim')
    require(contract['product']['matched_compression_ratio'] is None and not contract['product']['cross_topic_umbrella_deduplication'], 'topic accounting boundary')
    lean = read_json('phase228_retained_lean_report.json')
    require(lean['status'] == 'PASS' and len(lean['builds']) == 5, 'retained Lean evidence status')
    inherited = 0
    formal_bindings = {row['path']:row for row in author['retained_bindings'] if row['path'].startswith('formal/')}
    for build in lean['builds']:
        require(build['exit_code'] == 0 and build['source_sha256'] == formal_bindings['formal/' + build['source']]['sha256'], 'wrong formal source evidence')
        log_name = 'phase228_' + Path(build['source']).stem + '.log'
        require(digest((ROOT / log_name).read_bytes()) == build['log_sha256'], 'formal log mismatch')
        for name, axioms in build['axiom_reports'].items():
            require(set(axioms) <= STANDARD, f'nonstandard axiom: {name}')
            inherited += 1
    require(inherited == 34, 'inherited report count')
    render = read_json('phase228_render_report.json')
    require(render['visual_review']['completed'] and render['matched_ratio'] is None, 'render scope')
    pages = {}
    for name, paper in render['papers'].items():
        require(digest((ROOT / paper['source']).read_bytes()) == paper['source_sha256'], 'render source changed')
        require(digest((ROOT / f'phase228_{name}.pdf').read_bytes()) == paper['pdf_sha256'], 'archived render changed')
        require(paper['AST_math_table_code_preserved'], 'render structural loss')
        require(not any('Overfull' in s or 'Missing character' in s for s in paper['diagnostics']), 'render overflow/glyph loss')
        pages[name] = paper['pages']
    require(pages == {'umbrella':15, 'application':4}, 'render page evidence')
    report = {'status':'PASS_BINDINGS_PROVENANCE_AND_SCOPE', 'author_manifest_sha256':AUTHOR_SHA,
              'review_manifest_sha256':digest((ROOT / 'phase228_manifest.json').read_bytes()),
              'author_exports_verified':15,'review_exports_verified':len(review['exports']),
              'retained_bindings_verified':14 if args.verify_retained else 0,
              'provenance_spans':22,'builder_replay':rebuild,
              'inherited_Lean_reports_bound':inherited,'new_Lean_compilation_in_this_command':False,
              'archive_render_pages':pages,'new_rendering_or_visual_review_in_this_command':False,
              'new_principal_credit':0,'matched_compression_ratio':None,
              'scope':'Binding/provenance replay. Mathematical proof, source reading and visual judgments are the independent human-readable review; fresh Lean/render commands are separate.'}
    out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
