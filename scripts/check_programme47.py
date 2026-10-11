#!/usr/bin/env python3
"""Check original identities and current manuscript routes for programme 47."""
import argparse
import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader


def verify(root):
    def need(ok, message):
        if not ok:
            raise ValueError('PROGRAMME47: ' + message)

    def read(path):
        return json.loads((root / path).read_text())

    def binding(row):
        path = Path(row['path'])
        need(not path.is_absolute() and '..' not in path.parts, 'Unsafe binding')
        data = (root / path).read_bytes()
        need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], str(path))

    base = 'audit/programme47/v1/'
    report = read(base + 'registration_report.json')
    for key in ['current_corpus', 'current_catalogue', 'active_original_catalogue',
                'current_snapshot', 'original_registration']:
        binding(report[key])
    for row in report['scientific_and_numerical_admissions']:
        binding(row)
    old = read(base + 'previous_corpus_pointer.json')
    current = read('audit/corpus/latest.json')
    added = {'F007'}
    admitted = set(old['admitted_original_ids']) | added
    active = set(old['active_original_ids'])
    archived = set(old['archived_original_ids'])
    need(current['status'] == 'CURRENT_PROGRAMME_47_ADMITTED_OF_106_ACTIVE_ORIGINALS', 'Current status')
    need(len(old['admitted_original_ids']) == 46 and not added & set(old['admitted_original_ids']),
         'New original already admitted')
    for key in ['admitted_original_ids', 'measured_original_ids']:
        need(len(current[key]) == 47 and set(current[key]) == admitted, 'Original omitted or repeated')
    need(current['admitted_principal_originals'] == current['currently_measured_originals'] == 47,
         'Recovery and measurement totals')
    need(current['active_original_ids'] == old['active_original_ids'] and len(active) == 106
         and current['archived_original_ids'] == old['archived_original_ids'] and len(archived) == 55
         and not active & archived and current['originals'] == current['accessible_originals'] == 106,
         'Intake changed')
    need(set(current['accessible_pending_original_ids']) == active - admitted
         and len(current['accessible_pending_original_ids']) == current['accessible_pending_complete_recovery'] == 59
         and current['pending_source_retrieval'] == 0 and current['retrieval_original_ids'] == []
         and current['measurement_pending_original_ids'] == [] and not current['source_retrieval_in_scope']
         and not current['all_original_proofs_recovered'] and not current['all_conjectures_resolved'],
         'Remaining work erased')
    for key in ['snapshot', 'base_inventory', 'previous_snapshot', 'active_catalogue', 'scope_admission', 'scope_archive']:
        binding(current[key])
    for key in ['added_admissions', 'added_measurements', 'access_additions', 'current_topic_replacements']:
        for row in current[key]:
            binding(row)
    need({k: v for k, v in current.items() if k != 'snapshot'} == read(current['snapshot']['path']),
         'Snapshot differs')
    registration = read(base + 'new_original_registration.json')
    need(registration['source_ids'] == ['F007'] and registration['principal_originals_added'] == 1
         and registration['new_intake_originals'] == registration['new_question_credit'] == registration['new_formal_credit'] == 0,
         'Unsupported credit')
    for key in ['added_admissions', 'added_measurements']:
        need(current[key][:-1] == old[key] and current[key][-1] == report['original_registration'],
             'Historical registration changed')
    sourceids = [s for row in current['added_measurements'] for s in read(row['path'])['source_ids']]
    need(len(sourceids) == len(set(sourceids)) and not set(sourceids) & set(current['historical_admitted_ids'])
         and set(sourceids) | set(current['historical_admitted_ids']) == admitted, 'Measurement double counting')
    need(current['current_topic_replacements'] == old['current_topic_replacements'] + report['scientific_and_numerical_admissions'],
         'Current topic registration changed')

    before = {r['original_id']: r for r in read(old['active_catalogue']['path'])['entries']}
    catalogue = read(current['active_catalogue']['path'])
    after = {r['original_id']: r for r in catalogue['entries']}
    affected = {'F005', 'F007', 'F013', 'F016', 'L012', 'L016', 'L032', 'L034', 'L035', 'L128', 'N009'}
    need(len(catalogue['entries']) == len(after) == 106 and set(after) == active, 'Original catalogue')
    need({k for k in before if before[k] != after[k]} == affected, 'Unrelated original record changed')
    for key, row in after.items():
        now = row['current_principal_recovery']
        need(row['active'] and row['original_count'] == 1 and row['source_access'] == before[key]['source_access']
             and (now['status'] == 'ADMITTED_AND_MEASURED') == (key in admitted), 'Source or proof status: ' + key)
        for entry in now['latest_admission_references']:
            binding(entry)
        if key in affected:
            need(row['historical_proof_status'] == before[key]['historical_proof_status']
                 and now['historical_admission_evidence'] == before[key]['current_principal_recovery']['historical_admission_evidence'],
                 'Historical evidence changed')
            need(now['current_application_routes'] and now['current_common_routes'], 'Missing proof route')

    previous_papers = read(base + 'previous_catalogue.json')
    papers = read('papers/latest_catalogue.json')
    need(papers == read('papers/catalogue_unified_a_faithfulness_measured.json')
         and len(papers['entries']) == len(previous_papers['entries']) + 15 == 80
         and set(papers['original_ids']) == set(previous_papers['original_ids']) | added
         and len(papers['original_ids']) == papers['new_principal_originals'] == 20
         and papers['active_source_catalogue'] == current['active_catalogue'], 'Paper catalogue')
    changed_papers = set()
    for prior, now in zip(previous_papers['entries'], papers['entries']):
        if prior != now:
            need(prior.get('id') == now.get('id'), 'Paper identity changed')
            changed_papers.add(now['id'])
    need(changed_papers == set(report['updated_current_catalogue_ids']) and len(changed_papers) == 7,
         'Unrelated paper row changed')
    new_rows = papers['entries'][len(previous_papers['entries']):]
    need([x['id'] for x in new_rows] == report['added_current_catalogue_ids'], 'Added paper routes')
    current_rows = [r for r in papers['entries'] if r.get('id') in changed_papers] + new_rows
    need(len(current_rows) == 22 and len({r['id'] for r in current_rows}) == 22, 'Duplicate current paper route')
    for row in current_rows:
        tex = (root / row['tex']).read_text()
        title = re.search(r'\\title\{([^}]+)\}', tex) or re.search(r'\\section\*\{([^}]+)\}', tex)
        need(title and row['title'] == title.group(1), 'Paper title differs from TeX')
        need(len(PdfReader(root / row['pdf']).pages) == row['physical_pages'], 'Incomplete PDF')
        need(row['status'] == 'ROOT_ADMITTED_CURRENT_EDITION' and row['measurement_status'] == 'admitted', 'Paper status')
        for path in row['tex_inputs']:
            need((root / path).is_file(), 'Missing TeX input')
    for topic, folder in [('A', 'a'), ('Mixes', 'mixes')]:
        pointer = read('papers/topic-' + folder + '/latest.json')
        for key in ['admission', 'reader', 'measurement']:
            binding(pointer[key])
        admission = read(pointer['admission']['path'])
        need(admission['source_ids'] == pointer['source_ids'] and admission['software_inclusive_factor'] is None
             and not admission['whole_source_formalized'] and admission['new_question_credit'] == 0,
             'Topic scope or asymmetric program claim')
        expected = {r['id']: r for r in current_rows if r['topic'] == topic}
        need({r['id']: r for r in pointer['catalogue_entries']} == expected
             and len(pointer['catalogue_entries']) == len(expected), 'Current topic paper routes')
    affine = read('papers/topic-affine/latest.json')
    binding(affine['current_topic_pointer']); binding(affine['admission'])
    need(affine['source_ids'] == ['L012'] and affine['separate_topic_counted'] is False
         and affine['historical_editions_preserved'] and papers['affine_topic_consolidated_into_A']['separate_topic_counted'] is False,
         'Affine original counted twice')
    return dict(status='PASS_PROGRAMME47', active=106, recovered=47, pending=59,
                archived_unavailable=55, changed_originals=sorted(affected), unchanged_originals=95,
                new_originals=['F007'], added_paper_rows=15, updated_paper_rows=7,
                literal_titles_and_PDF_lengths=22, new_question_credit=0, software_inclusive_factors=None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    print(json.dumps(verify(parser.parse_args().repo), indent=2))
