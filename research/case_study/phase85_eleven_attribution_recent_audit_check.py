#!/usr/bin/env python3
"""Independent attribution integrity/rejection checks, without shared-engine imports."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

def digest(data): return hashlib.sha256(data).hexdigest()
def require(condition, message):
    if not condition: raise ValueError(message)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study-root', type=Path, required=True)
    p.add_argument('--replay-dir', type=Path, required=True)
    p.add_argument('--rebuilt-sidecar', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    require(not a.report.exists() and not a.report.is_symlink(), 'New report required')
    b = a.study_root
    manifest_name = 'phase79_eleven_attribution_manifest.json'
    raw = (b / manifest_name).read_bytes()
    require(digest(raw) == 'a5a0cad845640dd6c5c484f1b96a5568f0e8d52a7104b0b4f436f27721e5a50c', 'Author manifest changed')
    m = json.loads(raw)
    bindings = m['export_allowlist'] + m['immutable_inputs']
    for r in bindings:
        data = (b / r['path']).read_bytes()
        require(len(data) == r['bytes'] and digest(data) == r['sha256'], 'Changed bound artifact: ' + r['path'])
    sidecar_raw = (b / 'phase79_eleven_attribution.json').read_bytes()
    require(a.rebuilt_sidecar.read_bytes() == sidecar_raw, 'Sidecar rebuild mismatch')
    d = json.loads(sidecar_raw)
    source = (b / d['manuscript']['path']).read_bytes()
    text = source.decode()
    require(len(source) == 229791 and digest(source) == d['manuscript']['sha256'], 'Proof binding')
    notes = sorted(d['notes'], key=lambda r:(r['insert_after_codepoint'],r['id']))
    require(len(notes) == 35 and len({r['id'] for r in notes}) == 35, 'Note inventory')
    counts = dict(Counter(c for r in notes for c in r['markers']))
    require(counts == {'B':33,'I':15,'R':20,'C':7,'V':9,'L':1}, 'Marker inventory')
    for r in notes:
        span = r['anchor']; snippet = text[span['start_codepoint']:span['end_codepoint_exclusive']]
        require(digest(snippet.encode()) == span['sha256_utf8'] and snippet.startswith(span['exact_prefix']), 'Anchor: ' + r['id'])
        require(span['start_codepoint'] < r['insert_after_codepoint'] <= span['end_codepoint_exclusive'], 'Insertion outside span')
        require('I' not in r['markers'] or r['historical_novelty'] == 'not established', 'Priority overclaim')
    original_old = json.loads((b / 'phase61_ten_source_attribution.json').read_text())
    old = {('S24' if r['id']=='S23' else 'S25' if r['id']=='S24' else r['id']):r for r in original_old['notes']}
    changes = {}
    for r in notes:
        if r['id'] not in old:
            changes[r['id']] = ['NEW']
        else:
            changes[r['id']] = [k for k in r if k not in {'id','label','anchor','insert_after_codepoint'} and r[k] != old[r['id']].get(k)]
    require({k for k,v in changes.items() if v == ['NEW']} == {'K03','O00','S23','APPE'}, 'New notes changed')
    require({k for k,v in changes.items() if v and v != ['NEW']} == {'INTRO','S02','S18','E01','S24','S25','REFS'}, 'Unexpected semantic change')
    ledger = (a.replay_dir / 'ledger.md').read_text()
    recoveries = {}
    for filename, frozen, pandoc in [('reader.md','phase79_eleven_attribution_reader.md',False),
                                    ('reader.pandoc.md','phase79_eleven_attribution_reader.pandoc.md',True)]:
        written = (a.replay_dir / filename).read_text()
        require(written.encode() == (b / frozen).read_bytes(), 'Fresh reader mismatch')
        start = written.index(text.splitlines()[0] + '\n')
        require(written.endswith('\n\n' + ledger), 'Ledger boundary')
        body = written[start:-(len(ledger)+2)]
        shift = 0
        insertions = []
        for r in notes:
            content = '**' + ' '.join('['+c+']' for c in r['markers']) + ' — ' + r['id'] + '.** ' + r['summary']
            addition = ('\n\n::: {.audit-margin data-note="' + r['id'] + '" data-codes="' + ' '.join(r['markers']) + '"}\n' + content + '\n:::\n') if pandoc else '\n\n> ' + content + '\n'
            point = r['insert_after_codepoint'] + shift
            require(body[point:point+len(addition)] == addition, 'Written note differs: ' + r['id'])
            insertions.append((point,point+len(addition)))
            shift += len(addition)
        for lo,hi in reversed(insertions): body = body[:lo]+body[hi:]
        require(body.encode() == source, 'Independent actual-reader stripping mismatch')
        recoveries[filename] = dict(sha256=digest(body.encode()), bytes=len(body.encode()), notes_removed=35)
    require((a.replay_dir / 'ledger.md').read_bytes() == (b/'phase79_eleven_attribution.md').read_bytes(), 'Ledger mismatch')
    before = {p.name:digest(p.read_bytes()) for p in a.replay_dir.iterdir() if p.is_file()}
    run = subprocess.run([sys.executable,'-O',str(b/'phase79_eleven_attribution_generate.py'),'--output-dir',str(a.replay_dir)], capture_output=True)
    require(run.returncode != 0 and b'output directory exists' in run.stderr, 'Existing directory accepted')
    require(before == {p.name:digest(p.read_bytes()) for p in a.replay_dir.iterdir() if p.is_file()}, 'Existing replay changed')
    rejections = []
    with tempfile.TemporaryDirectory(prefix='phase85-annotation-controls-', dir='/private/tmp') as temporary:
        temp = Path(temporary)
        for kind in ['stale_anchor','wrong_proof_hash','M_marker','O_marker']:
            altered = copy.deepcopy(d)
            if kind == 'stale_anchor': altered['notes'][0]['anchor']['sha256_utf8'] = '0'*64
            elif kind == 'wrong_proof_hash': altered['manuscript']['sha256'] = '0'*64
            else: altered['notes'][0]['markers'].append(kind[0])
            path = temp/(kind+'.json'); path.write_text(json.dumps(altered))
            output = temp/(kind+'-output')
            run = subprocess.run([sys.executable,'-O',str(b/'phase79_eleven_attribution_generate.py'),'--sidecar',str(path),'--output-dir',str(output)],capture_output=True)
            require(run.returncode != 0 and not output.exists(), 'Bad sidecar accepted: '+kind)
            expected = b'stale span' if kind=='stale_anchor' else b'stale binding' if kind=='wrong_proof_hash' else b'eleven measurement/priority not cleared'
            require(expected in run.stderr, 'Unexpected rejection: '+kind)
            rejections.append(dict(case=kind, exit_code=run.returncode, no_output_created=True))
    for r in bindings:
        require(digest((b/r['path']).read_bytes()) == r['sha256'], 'Original changed afterward')
    result = dict(status='PASS_independent_integrity_and_controls', author_bound_files=len(bindings),
                  manifest_sha256=digest(raw), note_count=35, marker_counts=counts,
                  rebuilt_sidecar_identical=True, independent_written_recovery=recoveries,
                  unchanged_semantic_notes=sum(not v for v in changes.values()), semantic_delta=changes,
                  no_clobber_preserved_files=len(before), optimized_python_rejections=rejections,
                  all_inputs_unchanged=True, new_GAP_Lean_or_PDF_layout_check=False,
                  semantic_audit='See companion written audit; these integrity checks alone do not establish attribution truth.')
    a.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__ == '__main__': main()
