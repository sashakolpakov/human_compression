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

def check_bindings(rows):
    for row in rows:
        name = row.get('path', row.get('file'))
        need(isinstance(name,str) and not Path(name).is_absolute() and
             '..' not in Path(name).parts, 'Invalid binding path.')
        data = (ROOT/name).read_bytes()
        need(digest(data)==row['sha256'] and len(data)==row['bytes'],
             'Changed audited artifact: '+name)

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
    extension = load('audit/lean_extension.json')
    need(extension['status']=='PASS_ROOT_REVIEWED_SEPARATE_MODULE_EXTENSION',
         'Unreviewed Lean extension.')
    check_bindings(extension['old_artifact_preservation']['bindings'])
    check_bindings(extension['artifacts'])
    old = load(extension['old_run']['path'])
    expected_names = old['discovered_modules'] + [extension['module']]
    need(len(names)==97 and set(names)==set(expected_names),
         'Changed canonical Lean inventory without audit.')
    fresh = load(extension['new_independent_root_replay']['report']['path'])
    need(fresh['status']=='PASS' and len(fresh['declarations'])==9 and
         fresh['source_sha256']==extension['new_source']['sha256'],
         'New Lean source lacks its fresh independent report.')
    roots = re.findall(r'`([A-Za-z0-9_]+)',(formal/'lakefile.lean').read_text())
    need(set(roots)==set(names) and len(roots)==len(names),'Default build omits or duplicates modules.')
    return names

def check_catalogue():
    catalogue = load('papers/catalogue.json')
    papers = catalogue['papers']
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
    editions = catalogue.get('new_editions', [])
    need(len({r['id'] for r in papers+editions})==len(papers)+len(editions),
         'Duplicate mathematical edition ID.')
    for row in editions:
        review = load(row['review_record'])
        need(review['status'].startswith('PASS'), 'Unreviewed proof edition: '+row['id'])
        check_bindings(review['artifacts'])
        recorded = {r['path']:r for r in review['artifacts']}
        for key,suffix in [('tex','.tex'),('pdf','.pdf')]:
            name = row[key]
            need(name.startswith('papers/') and name.endswith(suffix) and name in recorded,
                 'New proof edition missing from its review: '+row['id'])
    return len(papers), len(editions)

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

def check_topic_measurement():
    review = load('audit/topic-e/v2/measurement_admission.json')
    need(review['status']=='PASS_ROOT_ADMITTED_MEASUREMENT', 'Unadmitted topic measurement.')
    check_bindings(review['artifacts'])
    measured = load('audit/topic-e/v2/measurement.json')
    recounted = load('audit/topic-e/v2/root_recount.json')
    protocol_hash = digest((ROOT/'audit/topic-e/v2/protocol.json').read_bytes())
    need(protocol_hash == review['measurement_protocol_sha256'] ==
         measured['protocol_sha256'] == recounted['protocol_sha256'],
         'Measurement reports refer to different editions.')
    costs = {key:value for group in measured['costs'].values() for key,value in group.items()}
    cells = 0
    for key,forms in recounted['costs'].items():
        for form,metrics in forms.items():
            for metric,value in metrics.items():
                need(costs[key][form][metric]==value, 'Independent recount differs: '+key)
                cells += 1
    need(cells==150, 'Incomplete three-source comparison.')
    need(measured['historical_program_cost'] is None and
         measured['retained_library_cost'] is None and
         measured['full_Lean_cost'] is None and
         measured['exact_all_artifact_factor'] is None, 'Unknown costs cannot become zero.')
    summary = load('audit/topic-e/v2/summary.json')
    c = {k:v['NFC']['characters_without_whitespace'] for k,v in costs.items()}
    total = sum(c[k] for k in ('L083','L079','L021'))
    denominator = sum(c[k] for k in ('New_U','New_A1','New_A2','New_A3'))
    need(summary['historical_manuscripts']==total and
         summary['common_theory']==c['New_U'] and
         summary['all_applications']==denominator-c['New_U'] and
         summary['complete_written_denominator']==denominator,
         'Summary costs differ from the complete manuscript counts.')
    need(summary['overall_written_factor']==total/denominator,
         'Overall factor does not charge the common theory once.')
    expected_pairs = {('L083','New_A1'), ('L079','New_A2'), ('L021','New_A3')}
    rows = summary['per_result_contract']
    need(len(rows)==3 and {(r['source'],r['application']) for r in rows}==expected_pairs,
         'Conditional comparison must cover exactly the three result contracts.')
    need(summary['required_program']==c['New_Code'] and
         summary['optional_validation_program']==c['New_Validation'] and
         summary['overall_with_required_program_known_cost']==total/(denominator+c['New_Code']) and
         summary['overall_with_required_and_validation_known_cost']==
         total/(denominator+c['New_Code']+c['New_Validation']),
         'Program-inclusive figures must charge the complete programs.')
    for row in summary['per_result_contract']:
        need(row['full_source_length']==c[row['source']] and
             row['complete_application_length']==c[row['application']] and
             row['conditional_factor']==c[row['source']]/c[row['application']] and
             row['already_acquired_common_theory_and_required_program']==c['New_U']+c['New_Code'],
             'Incorrect conditional result factor.')

def check_topic_dag():
    review = load('audit/topic-e/v2/dag_admission.json')
    need(review['status']=='PASS_ROOT_REVIEWED_PAIRED_DAG', 'Unreviewed paired graph.')
    check_bindings(review['artifacts'])
    prefix = 'audit/topic-e/v2/dag/'
    need((ROOT/(prefix+'measurement_protocol.json')).read_bytes()==
         (ROOT/'audit/topic-e/v2/protocol.json').read_bytes() and
         (ROOT/(prefix+'accepted_measurement.json')).read_bytes()==
         (ROOT/'audit/topic-e/v2/measurement.json').read_bytes(),
         'Graph and headline figures refer to different manuscript editions.')
    result = load(prefix+'result.json')
    fresh = load(prefix+'root_replay.json')
    dag = load(prefix+'dag.json')
    measured = load('audit/topic-e/v2/measurement.json')
    costs = measured['costs']['sources'] | measured['costs']['new']
    need(result['status']==fresh['status']=='PASS_PAIRED_ACCOUNTING_AND_BOUND_DOCUMENTARY_DAGS',
         'Graph accounting replay did not pass.')
    need(result['costs']==fresh['costs'] and len(result['costs'])==9,
         'Public graph replay differs from the recorded costs.')
    cells = 0
    for key,forms in result['costs'].items():
        for form,metrics in forms.items():
            for metric,value in metrics.items():
                need(costs[key][form][metric]==value, 'Graph partition loses text: '+key)
                cells += 1
    need(cells==90 and dag['no_node_count_ratio'] and dag['measurement_pays_all_text'],
         'Graph must preserve complete costs and stated granularity.')
    need(result['headline_from_accepted_measurement']==fresh['headline_from_accepted_measurement'],
         'Graph headline differs on replay.')

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write-manifest',action='store_true',help='Record already staged publication bytes.')
    args = ap.parse_args()
    if args.write_manifest:
        changed = subprocess.check_output(['git','diff','--name-only','-z'],cwd=ROOT).decode().split('\0')
        changed = [p for p in changed if p and p!='provenance/publication_manifest.json']
        need(not changed,'Stage all publication edits before recording their bytes: '+repr(changed))
    historical, markdown = check_archive(); lean = check_lean(); papers, editions = check_catalogue()
    check_topic_measurement()
    check_topic_dag()
    rows = publication_rows()
    if args.write_manifest:
        MANIFEST.write_text(json.dumps({
            'scope':'Tracked file integrity, archive preservation and saved Lean agreement. No new proof or measurement.',
            'baseline_commit':load('audit/intake.json')['baseline_commit'],
            'canonical_lean_modules':lean,'files':rows},indent=2)+'\n')
    need(load('provenance/publication_manifest.json')['files']==rows,'Publication differs from manifest.')
    print(f'PASS: {len(rows)} tracked artifacts; zero tracked Markdown.')
    print(f'PASS: {historical} historical bindings; {markdown} notes checked in Git, not local files.')
    print(f'PASS: {len(lean)} saved Lean reports and default build entries; {papers} preserved and {editions} new TeX/PDF editions.')
    print('Trust: 96 reports without native axioms; one legacy report has four recorded native axioms.')
    print('Lean evidence: 96 unchanged modules from the prior fresh run, plus one separately compiled module.')
    print('PASS: 150 independent metric cells; overall and conditional factors have separate denominators.')
    print('PASS: paired proof graphs preserve all 90 current source/application/program cost coordinates.')
    print('Historical computations require the pinned intake checkout.')

if __name__=='__main__':
    main()
