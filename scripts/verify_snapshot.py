#!/usr/bin/env python3
"""Check tracked publication and pinned archive separately; ignore local Markdown.

Historical proof replay requires the intake checkout. This is an integrity
check, not a rerun of the mathematical proofs or their computations.
"""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT/'provenance/publication_manifest.json'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return sha256(data).hexdigest()

def load(path):
    return json.loads((ROOT/path).read_text())

def archive_blobs(commit, paths):
    need(re.fullmatch(r'[0-9a-f]{40}',commit) is not None,'Use the full archive commit.')
    for path in paths:
        need(not Path(path).is_absolute() and '..' not in Path(path).parts and '\n' not in path,
             'Invalid archive path: '+path)
    requests = ''.join(commit+':'+p+'\n' for p in paths).encode()
    proc = subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=requests,
                          capture_output=True,check=True)
    data, offset, result = proc.stdout, 0, {}
    for path in paths:
        end = data.find(b'\n',offset)
        need(end >= offset,'Incomplete Git response.')
        fields = data[offset:end].split()
        need(len(fields)==3 and fields[1]==b'blob',
             'Archive object missing: '+path+'. Use a full clone or fetch the intake tag.')
        size = int(fields[2]); start = end+1
        result[path] = data[start:start+size]
        need(len(result[path])==size and data[start+size:start+size+1]==b'\n','Invalid Git response.')
        offset = start+size+1
    need(offset==len(data),'Unexpected Git output.')
    return result

def check_archive():
    intake = load('audit/intake.json'); archive = load('audit/archive_markdown.json')
    need(archive['commit']==intake['baseline_commit'],'Archive commit mismatch.')
    raw = (ROOT/'provenance/snapshot_manifest.json').read_bytes()
    need(digest(raw)==intake['baseline_snapshot_sha256'],'Historical snapshot manifest changed.')
    baseline = json.loads(raw)
    notes = {r['path']:r for r in archive['files']}
    need(len(notes)==len(archive['files'])==992,'Incomplete Markdown archive.')
    revised = intake['historical_files_changed_in_transition']
    blobs = archive_blobs(archive['commit'],sorted(set(notes)|set(revised)))
    count = 0
    for row in baseline['files']:
        name = row['file']; path = ROOT/name
        if 'symlink' in row:
            need(path.is_symlink() and str(path.readlink())==row['symlink'],'Changed link: '+name)
            continue
        if name in notes or name in revised:
            data = blobs[name]
            if name in notes:
                need(notes[name]['bytes']==row['bytes'] and notes[name]['sha256']==row['sha256'],
                     'Archived note differs from snapshot: '+name)
                count += 1
        else:
            need(path.is_file() and not path.is_symlink(),'Missing historical artifact: '+name)
            data = path.read_bytes()
        need(len(data)==row['bytes'] and digest(data)==row['sha256'],'Changed historical bytes: '+name)
    need(count==len(notes),'Unmatched archived notes.')
    return len(baseline['files']), count

def check_lean():
    formal = ROOT/'research/case_study/formal'; names = []
    for source in sorted(formal.glob('*.lean')):
        if source.name=='lakefile.lean':
            continue
        report = json.loads(source.with_suffix('.check.json').read_text())
        need(report['exit_code']==0 and report['sha256']==digest(source.read_bytes()),
             'Stale Lean report: '+source.name)
        need('sorryAx' not in report.get('stdout','') and
             re.search(r'\b(sorry|admit)\b',source.read_text()) is None,'Placeholder: '+source.name)
        native = re.findall(r'\b\w+\._native\.native_decide\.ax_\d+_\d+',report.get('stdout',''))
        expected = ([f'{s}._native.native_decide.ax_1_1' for s in
                    ('third_difference','terminal_basis_fixed','fourth_difference','newton_coefficients')]
                    if source.stem=='Phase23TransferAnnihilator' else [])
        need(native==expected,'Changed Lean trust boundary: '+source.name)
        names.append(source.stem)
    need(len(names)==96,'Changed canonical Lean inventory without audit.')
    roots = re.findall(r'`([A-Za-z0-9_]+)',(formal/'lakefile.lean').read_text())
    need(set(roots)==set(names) and len(roots)==len(names),'Default build omits or duplicates modules.')
    return names

def check_catalogue():
    papers = load('papers/catalogue.json')['papers']
    need(len({r['id'] for r in papers})==len(papers),'Duplicate paper IDs.')
    intake = load('audit/intake.json')
    archived_notes = {r['path']:r for r in load('audit/archive_markdown.json')['files']}
    baseline = {r['file']:r for r in load('provenance/snapshot_manifest.json')['files']}
    migration_rows = load('audit/tex_migration.json')['papers']
    migration = {r['id']:r for r in migration_rows}
    need(len(migration)==len(migration_rows) and set(migration)=={r['id'] for r in papers},
         'Migration report does not cover exactly the canonical papers.')
    for row in papers:
        for key, suffix in [('tex','.tex'),('pdf','.pdf')]:
            name = row[key]
            need(name.startswith('papers/') and '..' not in Path(name).parts and name.endswith(suffix)
                 and (ROOT/name).is_file(),'Missing canonical artifact: '+name)
        old = row['archived_source']; note = archived_notes.get(old['path'])
        need(old['commit']==intake['baseline_commit'] and note is not None and
             old['sha256']==note['sha256'] and old['bytes']==note['bytes'],
             'Unbound archived proof source: '+row['id'])
        old_pdf = row['archived_pdf']; config = row['conversion']
        need(old_pdf['sha256']==baseline[old_pdf['path']]['sha256'] and
             config['config_sha256']==baseline[config['config']]['sha256'],
             'Unbound archived PDF or rendering configuration: '+row['id'])
        saved = migration[row['id']]
        need(saved['tex']==row['tex'] and saved['tex_sha256']==digest((ROOT/row['tex']).read_bytes())
             and saved['new_pdf_sha256']==digest((ROOT/row['pdf']).read_bytes())
             and saved['archived_pdf_sha256']==old_pdf['sha256'],
             'Stale TeX migration evidence: '+row['id'])
        need(saved['identical_extracted_text'] is True and
             saved['old_text_sha256']==saved['new_text_sha256'] and
             saved['old_pages']==saved['new_pages'] and saved['new_pages']>0,
             'Migration does not preserve recorded PDF text/pages: '+row['id'])
    spec = importlib.util.spec_from_file_location('registry',ROOT/'scripts/build_paper_registry.py')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    view = mod.registry_view(); saved = load('audit/source_registry.json'); intake = load('audit/intake.json')
    need(view['current_counts']==saved['counts']==intake['counts_at_cutoff'],'Intake counts drifted.')
    need(view['entries']==saved['entries'],'Intake entries drifted.')
    need({r['id'] for r in view['entries'] if r['full_principal_results']}==
         set(intake['admitted_principal_contracts']),'Principal contract list drifted.')
    return len(papers)

def publication_rows():
    names = subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')[:-1]
    need(not any(p.lower().endswith('.md') for p in names),'Markdown must stay local and untracked.')
    rows = []
    for name in sorted(names):
        path = ROOT/name
        if path==MANIFEST:
            continue
        if path.is_symlink():
            need(path.resolve().is_relative_to(ROOT),'External symbolic link: '+name)
            rows.append({'file':name,'symlink':str(path.readlink())})
        else:
            need(path.is_file(),'Missing tracked file: '+name)
            data = path.read_bytes(); rows.append({'file':name,'bytes':len(data),'sha256':digest(data)})
    return rows

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write-manifest',action='store_true',help='Record already staged publication bytes.')
    args = ap.parse_args()
    if args.write_manifest:
        changed = subprocess.check_output(['git','diff','--name-only','-z'],cwd=ROOT).decode().split('\0')
        changed = [p for p in changed if p and p!='provenance/publication_manifest.json']
        need(not changed,'Stage all publication edits before recording their bytes: '+repr(changed))
    historical, markdown = check_archive(); lean = check_lean(); papers = check_catalogue()
    rows = publication_rows()
    if args.write_manifest:
        MANIFEST.write_text(json.dumps({
            'scope':'Tracked file integrity, archive preservation and saved Lean agreement. No new proof or measurement.',
            'baseline_commit':load('audit/intake.json')['baseline_commit'],
            'canonical_lean_modules':lean,'files':rows},indent=2)+'\n')
    need(load('provenance/publication_manifest.json')['files']==rows,'Publication differs from manifest.')
    print(f'PASS: {len(rows)} tracked artifacts; zero tracked Markdown.')
    print(f'PASS: {historical} historical bindings; {markdown} notes checked in Git, not local files.')
    print(f'PASS: {len(lean)} saved Lean reports and default build entries; {papers} TeX/PDF papers.')
    print('Trust: 95 reports without native axioms; one legacy report has four recorded native axioms.')
    print('Historical computations require the pinned intake checkout.')

if __name__=='__main__':
    main()
