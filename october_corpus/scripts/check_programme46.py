#!/usr/bin/env python3
"""Check the exact original registration and current paper routes for programme 46."""
from pathlib import Path
import argparse, hashlib, json, re
from pypdf import PdfReader

def verify(root):
    def need(ok, message):
        if not ok: raise ValueError('PROGRAMME46: ' + message)
    def read(path): return json.loads((root / path).read_text())
    def binding(row):
        p = Path(row['path'])
        need(not p.is_absolute() and '..' not in p.parts, 'Unsafe binding')
        b = (root / p).read_bytes()
        need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'], str(p))
    base = 'audit/programme46/v1/'
    report = read(base + 'registration_report.json')
    for key in ['current_corpus', 'current_catalogue', 'active_original_catalogue',
                'current_snapshot', 'original_registration']:
        binding(report[key])
    for row in report['scientific_and_numerical_admissions']: binding(row)
    old = read(base + 'previous_corpus_pointer.json')
    current = read('audit/corpus/latest.json')
    extra = {'L016', 'L043', 'L056'}
    admitted = set(old['admitted_original_ids']) | extra
    active = set(old['active_original_ids'])
    archived = set(old['archived_original_ids'])
    need(current['status'] == 'CURRENT_PROGRAMME_46_ADMITTED_OF_106_ACTIVE_ORIGINALS', 'Current status')
    need(set(current['admitted_original_ids']) == set(current['measured_original_ids']) == admitted
         and len(admitted) == current['admitted_principal_originals'] == current['currently_measured_originals'] == 46,
         'An original was omitted or counted twice')
    need(current['active_original_ids'] == old['active_original_ids'] and len(active) == 106
         and current['archived_original_ids'] == old['archived_original_ids'] and len(archived) == 55
         and not active & archived and current['originals'] == current['accessible_originals'] == 106,
         'Intake changed')
    need(set(current['accessible_pending_original_ids']) == active-admitted
         and len(current['accessible_pending_original_ids']) == current['accessible_pending_complete_recovery'] == 60
         and current['pending_source_retrieval'] == 0 and current['retrieval_original_ids'] == []
         and current['measurement_pending_original_ids'] == [] and not current['source_retrieval_in_scope']
         and not current['all_original_proofs_recovered'] and not current['all_conjectures_resolved'],
         'Remaining work erased')
    for k in ['snapshot','base_inventory','previous_snapshot','active_catalogue','scope_admission','scope_archive']:
        binding(current[k])
    for k in ['added_admissions','added_measurements','access_additions','current_topic_replacements']:
        for row in current[k]: binding(row)
    need({k:v for k,v in current.items() if k!='snapshot'} == read(current['snapshot']['path']), 'Snapshot differs')
    registration = read(base+'new_original_registration.json')
    need(set(registration['source_ids']) == extra and registration['principal_originals_added'] == 3
         and registration['new_intake_originals'] == registration['new_question_credit'] == registration['new_formal_credit'] == 0,
         'Unsupported new credit')
    for k in ['added_admissions','added_measurements']:
        need(current[k][:-1] == old[k] and current[k][-1] == report['original_registration'], 'Historical registration changed')
    sourceids = [s for row in current['added_measurements'] for s in read(row['path'])['source_ids']]
    need(len(sourceids) == len(set(sourceids)) and not set(sourceids)&set(current['historical_admitted_ids'])
         and set(sourceids)|set(current['historical_admitted_ids']) == admitted, 'Measurement double counting')

    prior_catalogue = read(old['active_catalogue']['path'])
    catalogue = read(current['active_catalogue']['path'])
    before = {row['original_id']: row for row in prior_catalogue['entries']}
    after = {row['original_id']: row for row in catalogue['entries']}
    affected = extra | {'F005','L079','L083','L021'}
    need(len(catalogue['entries']) == len(after) == 106 and set(after) == active, 'Original catalogue')
    need({k for k in before if before[k] != after[k]} == affected, 'Unrelated record changed')
    for key,row in after.items():
        now = row['current_principal_recovery']
        need(row['active'] and row['original_count']==1 and row['source_access']==before[key]['source_access']
             and (now['status']=='ADMITTED_AND_MEASURED') == (key in admitted), 'Access or proof status: '+key)
        for b in now['latest_admission_references']: binding(b)
        if key in affected:
            need(row['historical_proof_status']==before[key]['historical_proof_status']
                 and now['historical_admission_evidence']==before[key]['current_principal_recovery']['historical_admission_evidence'],
                 'Historical proof record changed')
            need(now['current_application_routes'] and now['current_common_routes'], 'Missing current proof route')

    previous_papers = read(base+'previous_catalogue.json')
    papers = read('papers/latest_catalogue.json')
    need(papers == read('papers/catalogue_projective_covers_measured.json')
         and papers['entries'][:-15] == previous_papers['entries']
         and set(papers['original_ids']) == set(previous_papers['original_ids'])|extra
         and len(papers['original_ids']) == papers['new_principal_originals'] == 19,
         'Paper catalogue or historical entries changed')
    need(papers['active_source_catalogue'] == current['active_catalogue'], 'Catalogue routes disagree')
    routes = papers['entries'][-15:]
    for row in routes:
        tex = (root/row['tex']).read_text()
        match = re.search(r'\\title\{([^}]+)\}',tex) or re.search(r'\\section\*\{([^}]+)\}',tex)
        need(match and row['title']==match.group(1), 'Invented paper title')
        need(len(PdfReader(root/row['pdf']).pages)==row['physical_pages'], 'Incomplete PDF')
        need(row['status']=='ROOT_ADMITTED_CURRENT_EDITION' and row['measurement_status']=='admitted', 'Paper status')
        for p in row['tex_inputs']: need((root/p).is_file(), 'Missing TeX input')
    for topic, folder in [('E','e'),('Mixes','mixes')]:
        pointer=read('papers/topic-'+folder+'/latest.json')
        for k in ['admission','reader','measurement']: binding(pointer[k])
        a=read(pointer['admission']['path'])
        need(a['status']=='ROOT_ADMITTED_CORRECTED_PRINCIPAL_CONTRACTS_AND_SYMMETRIC_MEASUREMENT'
             and a['source_ids']==pointer['source_ids'] and a['software_inclusive_factor'] is None
             and not a['whole_source_formalized'] and a['new_question_credit']==0,
             'Topic scope or asymmetric software claim')
        need(pointer['catalogue_entries']==[x for x in routes if x['topic']==topic], 'Topic paper routes')
    return dict(status='PASS_PROGRAMME46', active=106, recovered=46, pending=60,
                archived_unavailable=55, changed_originals=sorted(affected),
                unchanged_originals=99, literal_titles_and_PDF_lengths=15,
                new_question_credit=0, software_inclusive_factors=None)

if __name__ == '__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    print(json.dumps(verify(ap.parse_args().repo),indent=2))
