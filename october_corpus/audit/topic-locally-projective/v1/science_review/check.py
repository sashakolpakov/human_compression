#!/usr/bin/env python3
"""Distinct transfer audit; no import of the author's migration implementation."""
import argparse, hashlib, json, re, unicodedata
from pathlib import Path
from pypdf import PdfReader

PIN = '7bfce9d4a4c0acd3c898d852501550178d5d9a442cccd1603baddb0fdaa1fb85'

def need(value, message):
    if not value:
        raise ValueError(message)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text())

def block(h, row):
    t = (h / row['path']).read_text()
    t = '\n'.join(t.splitlines()[row['start_line'] - 1:row['end_line']])
    need(hashlib.sha256(t.encode()).hexdigest() == row['sha256'], 'exact line-delimited proof span')
    return t

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--packet', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args(); h = a.packet
    need(not a.out.exists(), 'fresh output'); a.out.mkdir(parents=True)
    need(sha(h / 'manifest.json') == PIN, 'correct modular edition')
    rows = read(h / 'manifest.json')['exports']
    for r in rows:
        name = Path(r['path'])
        need(not name.is_absolute() and '..' not in name.parts, 'safe export path')
        f = h / name
        need(f.stat().st_size == r['bytes'] and sha(f) == r['sha256'], 'changed frozen export')
    prior = list((h / 'accepted').rglob('manifest.json'))
    for manifest in prior:
        for r in read(manifest)['exports']:
            f = manifest.parent / r['path']
            need(f.stat().st_size == r['bytes'] and sha(f) == r['sha256'], 'changed accepted predecessor')
    migrate = read(h / 'migration.json')['rows']; exact = 0; placement = 0; rewrites = 0
    old_keys = set()
    for r in migrate:
        old_keys.add((r['old']['path'], r['old']['index']))
        old, new = block(h, r['old']), block(h, r['current'])
        if old == new:
            exact += 1
        elif old.replace('already printed and checked in the census packet',
                         'printed in full in the accompanying common program appendix') == new:
            placement += 1
        else:
            need(r['old']['path'] == 'accepted/L095/universal-locally-projective.tex' and
                 r['old']['index'] in [8, 9] and r['current']['path'] == 'universal-polytope.tex', 'unreviewed proof change')
            rewrites += 1
    need(len(old_keys) == 18 and (exact, placement, rewrites) == (15, 1, 2), 'complete distinct migration inventory')
    source = read(h / 'source_map.json')['rows']
    for key, n in [('L084', 18), ('L095', 34)]:
        previous = read(h / 'accepted' / (key + '_ledger.json'))['rows']
        current = [r['original_record'] for r in source if r['inherited_ledger'] == key]
        need(current == previous and len(current) == n, 'complete unchanged source records')
    sw = read(h / 'software_boundary.json')
    need(len(sw['programs']) == len({r['sha256'] for r in sw['programs']}) == 6, 'six unique required files')
    for r in sw['programs'] + sw['required_comparison_data']:
        need((h / r['path']).read_bytes() == (h / r['original']).read_bytes(), 'whole accepted input preserved')
    need(len(sw['complete_output_data']) == 11 and len(sw['operational_drivers']) == 2, 'complete separate evidence and drivers')
    docs = read(h / 'current_documents.json')['documents']
    need([d['pages'] for d in docs] == [7, 2, 3, 5, 6], 'complete five documents')
    pages = {}
    for d in docs:
        texts = [p.extract_text() or '' for p in PdfReader(h / d['pdf']['path']).pages]
        need(len(texts) == d['pages'] and [hashlib.sha256(t.encode()).hexdigest() for t in texts] == d['page_text_hashes'], 'whole PDF page texts')
        pages[d['id']] = len(texts)
    pack = lambda s: ''.join(unicodedata.normalize('NFKC', s).split())
    printed = ''.join('\n'.join(p.extract_text().splitlines()[:-1]) for p in PdfReader(h / 'required-programs.pdf').pages)
    for r in sw['programs']:
        need(pack((h / r['path']).read_text()) in pack(printed), 'full program included in print')
    for suffix in ['tex', 'pdf']:
        need((h / ('complete-census.' + suffix)).read_bytes() ==
             (h / 'accepted/L095/census' / ('corrected-census.' + suffix)).read_bytes(), 'complete census companion unchanged')
    scope = read(h / 'scope.json')
    need(scope['current_common_bundle'] == ['common.tex', 'complete-census.tex'] and
         scope['application_to_application_proof_edges'] == [] and
         scope['current_applications'] == {'L084': ['erratum.tex'], 'L095': ['universal-polytope.tex']}, 'common/application boundary changed')
    report = dict(status='PASS_DISTINCT_ROOT_MIGRATION',author_imports=False,
                  frozen_exports=len(rows),nested_accepted_manifests=len(prior),source_records=52,
                  old_proof_environments=18,exact=exact,placement_only=placement,reviewed_census_restatements=rewrites,
                  document_pages=pages,total_pages=sum(pages.values()),complete_required_programs=6,
                  whole_required_source_tables=True,complete_output_files=11,
                  finite_computation_repeated=False,new_source_credit=0,new_formal_credit=0,compression_factor=None)
    (a.out / 'report.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report))

if __name__ == '__main__':
    main()
