#!/usr/bin/env python3
"""Check the nine-original A edition, unique L121 registration and overview51."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, re, subprocess, sys, tempfile
from pypdf import PdfReader

def need(x, message):
    if not x:
        raise ValueError('PROGRAMME51: ' + message)

def verify(root):
    def read(path):
        return json.loads((root / path).read_text())
    def bind(row):
        path = Path(row['path'])
        need(not path.is_absolute() and '..' not in path.parts, 'safe binding')
        data = (root / path).read_bytes()
        need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'],
             'exact bytes ' + str(path))
    def manifest(row, pin):
        bind(row)
        need(row['sha256'] == pin, 'accepted packet identity')
        parent = Path(row['path']).parent
        for export in read(row['path'])['exports']:
            bind(dict(export, path=str(parent / export['path'])))

    science_path = 'audit/topic-a/extensions/locally-toroidal/v1/admission.json'
    numbers_path = 'audit/topic-a/v4/admission.json'
    editorial_path = 'audit/corpus/editorial/L022/v1/admission.json'
    for path, pin in [
        (science_path, '0c6baf27745cc39ae0c83c46e37e62e3c87ff56d2929a97f8f35a54c6f2157ba'),
        (numbers_path, 'b3ff441b1263f249fb7affd1d1c41b0a85a33c6e9241ad21e85c7b139cb4a406'),
        (editorial_path, '14a4e65655b552d0e4b187285251bb55f5d5a209fdf3089141f178755a323d5f')]:
        need(hashlib.sha256((root/path).read_bytes()).hexdigest() == pin, 'root admission ' + path)
    science, numbers, editorial = [read(p) for p in (science_path, numbers_path, editorial_path)]
    for admission in (science, numbers, editorial):
        for row in admission['frozen_payloads']:
            bind(row)
    need(science['original_id'] == 'L121' and science['source_dispositions'] == 27 and
         science['application_pages'] == 11 and science['common_pages'] == 23 and
         science['required_programs'] == 8 and science['required_data_files'] == 1 and
         science['operational_runners'] == 4 and science['new_partial_Lean_declarations'] == 6 and
         not science['whole_source_formalized'] and science['new_question_credit'] == 0,
         'complete corrected scientific scope')
    need(editorial['original_id'] == 'L022' and editorial['accessible_original_retained'] and
         editorial['measured_original_credit'] == 0 and editorial['factor'] is None and
         editorial['recovery_status'] == 'NO_PRINCIPAL_MATHEMATICAL_RESULT_TO_RECOVER',
         'editorial has no mathematical credit or factor')
    for key, pin in [
        ('numerical_author', '0f071b3d9098d48bfdadd8273239c4459ab35c549e2ddae59f6a9c622fa9a90e'),
        ('numerical_distinct_review', '2d071fbfffb2288d5b0d6f434b2c0d4b63fb95f187216b8d0bf5fc093397d04d'),
        ('numerical_root_adoption', '000bced9618afa28c1e4e65424f464d29ea50682eb6f0e2e95509eab065d5599')]:
        manifest(numbers[key], pin)
    result = read(numbers['measurement']['path'])
    need(numbers['primary'] == result['primary']['written'] and
         numbers['conditionals'] == result['primary']['conditional'] and
         numbers['source_ids'] == result['source_ids'] and len(numbers['source_ids']) == 9 and
         numbers['exact_fractions'] == 300 and numbers['old_conditionals_preserved'] == 240,
         'accepted nine-original numbers')
    need(numbers['symmetric_program_exclusion'] and numbers['software_inclusive_factor'] is None and
         numbers['complete_enlarged_printed_program_representation'] is None and
         numbers['whole_raw_files'] == 45 and numbers['required_program_or_data_files'] == 20,
         'symmetric software boundary and complete required inventory')
    with tempfile.TemporaryDirectory(prefix='a9-distinct-snapshot-') as temporary:
        output = Path(temporary) / 'check'
        command = [sys.executable, '-B', '-O', str(root/'audit/topic-a/v4/measurement/independent_review/check.py'),
                   '--author-root', str(root/'audit/topic-a/v4/measurement/packet'), '--out', str(output)]
        replay = subprocess.run(command, capture_output=True, text=True)
        need(replay.returncode == 0, 'distinct numerical replay: ' + replay.stdout + replay.stderr)
        need(json.loads((output/'report.json').read_text())['exact_fractions'] == 300,
             'all sensitivity fractions replayed')

    base = 'audit/programme51/v1/'
    old, current = read(base+'previous_corpus_pointer.json'), read('audit/corpus/latest.json')
    registration = read(base+'new_original_registration.json')
    need(registration['source_ids'] == ['L121'] and registration['principal_originals_added'] == 1 and
         registration['new_intake_originals'] == registration['new_question_credit'] == registration['new_formal_credit'] == 0,
         'only one new mathematical original')
    for key in ['added_admissions', 'added_measurements']:
        need(current[key][:-1] == old[key] and current[key][-1]['path'] == base+'new_original_registration.json',
             'unique additive ' + key)
        bind(current[key][-1])
    measured, pending, editors = [set(current[k]) for k in
                                  ['measured_original_ids', 'accessible_pending_original_ids', 'editorial_original_ids']]
    need(measured == set(old['measured_original_ids']) | {'L121'} and
         pending == set(old['accessible_pending_original_ids']) - {'L121', 'L022'} and editors == {'L022'},
         'exact new partition')
    need((len(measured), len(pending), len(editors)) == (51, 54, 1) and
         measured | pending | editors == set(current['active_original_ids']) and
         not (measured & pending or measured & editors or pending & editors), 'all106 originals accounted for')
    need(current['active_original_ids'] == old['active_original_ids'] and
         current['archived_original_ids'] == old['archived_original_ids'] and
         len(current['archived_original_ids']) == 55 and not current['source_retrieval_in_scope'],
         'fixed accessible and archived catalogues')
    for key in ['active_catalogue', 'snapshot', 'previous_snapshot']:
        bind(current[key])
    need(read(current['snapshot']['path']) == {k: v for k, v in current.items() if k != 'snapshot'},
         'current corpus snapshot exact')
    before = {x['original_id']: x for x in read(old['active_catalogue']['path'])['entries']}
    after = {x['original_id']: x for x in read(current['active_catalogue']['path'])['entries']}
    need(set(before) == set(after) and len(after) == 106 and
         {k for k in before if before[k] != after[k]} == {'L121', 'L022'}, '104 original records unchanged')
    for key in after:
        need(after[key]['source_access'] == before[key]['source_access'] and
             after[key]['historical_proof_status'] == before[key]['historical_proof_status'],
             'historical source evidence retained')
    need(after['L121']['current_principal_recovery']['status'] == 'ADMITTED_AND_MEASURED' and
         after['L022']['current_principal_recovery']['factor'] is None and
         not after['L022']['current_principal_recovery']['count_as_measured_mathematical_recovery'],
         'exact mathematical/editorial disposition')

    oldcat, cat = read(base+'previous_full_catalogue.json'), read('papers/catalogue.json')
    need(cat['papers'] == oldcat['papers'] and cat['new_editions'][:len(oldcat['new_editions'])] == oldcat['new_editions'],
         'historical build catalogue unchanged')
    additions = cat['new_editions'][len(oldcat['new_editions']):]
    need(len(additions) == 10 and sum(row['physical_pages'] for row in additions) == 79 and
         additions[0]['physical_pages'] == 23 and additions[-1]['physical_pages'] == 11,
         'complete common and nine applications')
    need(cat['current_topic_editions']['A'] == [row['id'] for row in additions] and
         {k:v for k,v in cat['current_topic_editions'].items() if k != 'A'} ==
         {k:v for k,v in oldcat['current_topic_editions'].items() if k != 'A'}, 'only A build pointer changes')
    for row in additions:
        need(len(PdfReader(root/row['pdf']).pages) == row['physical_pages'], 'whole PDF pages')
        title = re.search(r'\\title\{([^{}]*)\}', (root/row['tex']).read_text()).group(1)
        need(title == row['title'], 'literal manuscript title')
        for path in row['tex_inputs']:
            need((root/path).is_file(), 'declared TeX input')
    need(all(row['compiler'] == 'xelatex' for row in additions[:-1]) and
         additions[-1]['compiler'] == 'pdflatex', 'exact compilers')
    latest = read('papers/latest_catalogue.json')
    bind(latest['affine_topic_consolidated_into_A']['current_pointer'])
    pointer = read('papers/topic-a/latest.json')
    for key in ['admission', 'reader', 'measurement']:
        bind(pointer[key])
    need(pointer['common'] == 'papers/topic-a/v3/umbrella.pdf' and len(pointer['applications']) == 9 and
         pointer['catalogue_entries'] == additions, 'current complete A interface')

    review = read(base+'publication_review.json')
    for key in ['checker', 'registration_report', 'integration_corrections',
                'catalogue_compatibility', 'root_replay']:
        bind(review[key])
    compatibility = read(review['catalogue_compatibility']['path'])
    accepted_artifacts = {}
    for admission in compatibility['source_admissions']:
        bind(admission)
        accepted_artifacts.update({r['path']:r for r in read(admission['path'])['frozen_payloads']})
    for row in compatibility['scientific_reviews'] + compatibility['artifacts']:
        bind(row)
    required_paths = {p for row in additions for p in [row['tex'], row['pdf']] + row.get('tex_inputs', [])}
    need(len(required_paths) == 54 and compatibility['artifacts'] ==
         [accepted_artifacts[p] for p in sorted(required_paths)],
         'catalogue compatibility uses already accepted literal artifacts')
    manifest(review['proposal_manifest'],
             '58f0626ae3f5ddedbea85bc3d8cbf95dedaab60b2f0eb03e12a0e12a0f05e391')
    manifest(review['independent_manifest'],
             '553d4eb8f16667f70cffb6c2fcfba40e6113e67bead32fe2ee3f157a2107adc6')
    need(review['status'] == 'ROOT_ACCEPTED_PROGRAMME51_PUBLICATION' and
         review['role_disclosure'] and not review['unresolved_findings'], 'root publication review')
    report = read(review['registration_report']['path'])
    for key in ['current_corpus', 'current_catalogue', 'active_original_catalogue',
                'current_snapshot', 'original_registration']:
        bind(report[key])
    need(report['new_originals'] == ['L121'] and report['editorial_originals'] == ['L022'] and
         report['expected_partition'] == dict(recovered=51, mathematical_pending=54,
                                             editorial=1, active=106, archived=55, topics=19),
         'final actual registration')
    with tempfile.TemporaryDirectory(prefix='programme51-distinct-') as temporary:
        output = Path(temporary) / 'check'
        command = [sys.executable, '-B', '-O', str(root/base/'independent_review/check.py'),
                   '--proposal', str(root/base/'proposal'), '--public-root', str(root),
                   '--public-stage', '--out', str(output)]
        replay = subprocess.run(command, capture_output=True, text=True)
        need(replay.returncode == 0, 'distinct publication replay: ' + replay.stdout + replay.stderr)
        need(json.loads((output/'report.json').read_text()) == read(review['root_replay']['path']),
             'exact bounded publication findings')

    overview = read('audit/overview/v17/admission.json')
    for key in ['author_manifest', 'independent_manifest', 'current_corpus', 'current_catalogue',
                'active_original_catalogue', 'original_registration', 'registration_report', 'programme_review']:
        bind(overview[key])
    manifest(overview['author_manifest'], 'f70c8ac7eb978bea55db674216998641d13dcc58368dd3aaa716899d620732e1')
    manifest(overview['independent_manifest'], '1c1e81b1403bc0f952149f32272889199eaeec66e1d16a79e6330966f122d43f')
    spec = importlib.util.spec_from_file_location('overview51_distinct', root/'audit/overview/v17/independent_review/check.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    need(module.check(root/'audit/overview/v17/packet', root) == read('audit/overview/v17/independent_review/report.json'),
         'independent overview arithmetic and actual geometry')
    rows = read('audit/overview/v17/packet/results.json')
    need(set(rows['original_ids']) == measured, 'current overview and original registry agree')
    pointer = read('audit/overview/latest.json')
    for key in ['admission', 'reader', 'counts_source', 'measurement_policy', 'measurement_policy_reader', 'measurement_policy_review']:
        bind(pointer[key])
    need(pointer['admission']['path'] == 'audit/overview/v17/admission.json' and
         pointer['recovered_originals'] == pointer['current_conditional_factors'] == 51 and
         pointer['current_whole_factors'] == 19 and pointer['mathematical_pending_originals'] == 54 and
         pointer['editorial_original_ids'] == ['L022'], 'actual current overview pointer')
    text = (root/'README.rst').read_text()
    need('51 accessible originals' in text and 'fifty-one individual' in text and
         'first twenty-six' in text and 'audit/overview/v17/packet/reader.pdf' in text, 'readable current overview')
    return dict(status='PASS_PROGRAMME51', recovered=51, mathematical_pending=54, editorial=1,
                active=106, archived=55, topic_count=19, topic_fractions=300, overview_fractions=70,
                overview_bars=159, new_originals=['L121'], new_question_credit=0,
                scientific_pages_built=79, software_inclusive_factor=None)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(verify(args.repo), indent=2))
