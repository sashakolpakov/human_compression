#!/usr/bin/env python3
"""Check tracked publication and pinned archive separately; ignore local Markdown.

Historical proof replay requires the intake checkout. This is an integrity
check, not a rerun of the mathematical proofs or their computations.
"""
import argparse
import csv
from hashlib import sha256
from fractions import Fraction
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

def restored_lake(modules):
    text = (ROOT/'research/case_study/formal/lakefile.lean').read_text()
    for name in modules:
        line = '    `'+name+',\n'
        need(text.count(line)==1, 'New module must occur once in default build.')
        text = text.replace(line,'',1)
    return text.encode()

def check_previous_extension_artifacts(extension,kernels,retractions):
    lake = 'research/case_study/formal/lakefile.lean'
    for row in extension['artifacts']:
        if row['path']==lake:
            need(row==kernels['previous_lake'], 'Wrong previous default build.')
            restored = restored_lake(kernels['modules']+[retractions['module']])
            need(len(restored)==row['bytes'] and digest(restored)==row['sha256'],
                 'Default build changed beyond the reviewed additions.')
        else:
            check_bindings([row])

def check_previous_kernel_artifacts(kernels,retractions):
    for row in kernels['artifacts']:
        if row['path']=='research/case_study/formal/lakefile.lean':
            need(row==retractions['previous_lake'], 'Wrong previous kernel default build.')
            restored = restored_lake([retractions['module']])
            need(len(restored)==row['bytes'] and digest(restored)==row['sha256'],
                 'Default build changed beyond the commuting-retraction addition.')
        else:
            check_bindings([row])

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
    kernels = load('audit/normal-kernels/admission.json')
    need(kernels['status']=='PASS_ROOT_ADMITTED_NORMAL_KERNEL_PROOFS',
         'Unreviewed normal-kernel proofs.')
    need(kernels['previous_extension_sha256']==digest((ROOT/'audit/lean_extension.json').read_bytes()),
         'The previous extension audit changed.')
    retractions = load('audit/commuting-retractions/admission.json')
    need(retractions['status']=='PASS_ROOT_ADMITTED_COMMUTING_RETRACTIONS',
         'Unreviewed commuting-retraction proof.')
    need(retractions['previous_kernel_admission_sha256']==digest((ROOT/'audit/normal-kernels/admission.json').read_bytes()),
         'The previous normal-kernel audit changed.')
    check_bindings(retractions['artifacts'])
    check_previous_kernel_artifacts(kernels,retractions)
    check_previous_extension_artifacts(extension,kernels,retractions)
    old = load(extension['old_run']['path'])
    expected_names = old['discovered_modules'] + [extension['module']] + kernels['modules'] + [retractions['module']]
    need(len(names)==100 and set(names)==set(expected_names),
         'Changed canonical Lean inventory without audit.')
    fresh = load(extension['new_independent_root_replay']['report']['path'])
    need(fresh['status']=='PASS' and len(fresh['declarations'])==9 and
         fresh['source_sha256']==extension['new_source']['sha256'],
         'New Lean source lacks its fresh independent report.')
    replay = load(kernels['independent_public_replay'])
    need(replay['status']=='PASS' and len(replay['modules'])==2 and
         sum(len(m['declarations']) for m in replay['modules'])==14,
         'Incomplete fresh normal-kernel replay.')
    need([Path(m['source']['path']).stem for m in replay['modules']]==kernels['modules'],
         'Normal-kernel dependency order changed.')
    for module in replay['modules']:
        source = formal/module['source']['path']
        need(digest(source.read_bytes())==module['source']['sha256'] and
             module['exit_code']==0, 'Normal-kernel source differs from independent replay.')
        need(all(set(d['axioms']) <= {'propext','Classical.choice','Quot.sound'}
                 for d in module['declarations']), 'Unapproved normal-kernel axiom.')
    paired = load(retractions['independent_replay'])
    paired_source = formal/(retractions['module']+'.lean')
    need(paired['status']=='PASS' and len(paired['declarations'])==11 and
         paired['source_sha256']==digest(paired_source.read_bytes()),
         'Commuting-retraction source lacks its fresh independent replay.')
    need(all(set(d['axioms']) <= {'propext','Classical.choice','Quot.sound'}
             for d in paired['declarations']), 'Unapproved commuting-retraction axiom.')
    roots = re.findall(r'`([A-Za-z0-9_]+)',(formal/'lakefile.lean').read_text())
    need(set(roots)==set(names) and len(roots)==len(names),'Default build omits or duplicates modules.')
    return names

def check_completion():
    audit = load('audit/completion.json')
    intake = load('audit/intake.json')
    registry = {row['id']:row for row in load('audit/source_registry.json')['entries']}
    contracts = audit['contracts']
    ids = [row['source_id'] for row in contracts]
    need(len(ids)==len(set(ids))==27 and set(ids)==set(intake['admitted_principal_contracts']),
         'Completion audit must preserve exactly the admitted contracts.')
    totals = {k:v for k,v in intake['counts_at_cutoff'].items() if k!='reading_categories'}
    need(audit['counts_recomputed']==totals, 'Completion counts drifted.')
    need(audit['new_principal_credit']==audit['new_question_credit']==0 and
         audit['new_ratios_evaluated'] is False and audit['no_new_source_intake'] is True,
         'A completion map cannot create admissions or ratios.')
    assigned = [s for row in audit['bounded_completion_sequence'] for s in row['source_ids']]
    need(len(assigned)==27 and set(assigned)==set(ids), 'Completion topics omit or duplicate a contract.')
    table = audit['binding_table']
    need(len(table)==187, 'Completion evidence inventory changed without review.')
    by_revision = {}
    for key,row in table.items():
        need(key==row['git_revision']+':'+row['path'], 'Invalid completion binding.')
        by_revision.setdefault(row['git_revision'],[]).append(row)
    for rev,rows in by_revision.items():
        blobs = archive_blobs(rev,[r['path'] for r in rows])
        for row in rows:
            raw = blobs[row['path']]
            need(len(raw)==row['bytes'] and digest(raw)==row['sha256'],
                 'Changed completion evidence: '+row['path'])
    for row in contracts:
        need(row['principal_contract_admitted'] and
             not row['lean']['end_to_end_principal_contract_formalized'],
             'Completion map changed mathematical/formal scope.')
        record = registry[row['source_id']].get('current_record')
        if record:
            current = row['current_record']
            need(current is not None and current['binding'] in table and
                 table[current['binding']]['path']=='research/case_study/'+record,
                 'Completion view lost a later admission: '+row['source_id'])
    return len(contracts),len(table)

def check_catalogue():
    catalogue = load('papers/catalogue.json')
    builder_spec = importlib.util.spec_from_file_location('paper_builder', ROOT/'scripts/build_papers.py')
    builder = importlib.util.module_from_spec(builder_spec)
    builder_spec.loader.exec_module(builder)
    builder.select_papers(catalogue)
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
        builder.source_bundle(row)
        need(not row.get('tex_inputs'), 'Preserved TeX migrations cannot acquire unaudited inputs.')
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
        builder.source_bundle(row)
        review = load(row['review_record'])
        need(review['status'].startswith('PASS'), 'Unreviewed proof edition: '+row['id'])
        if row['review_record']=='audit/lean_extension.json':
            check_previous_extension_artifacts(review,load('audit/normal-kernels/admission.json'),
                                               load('audit/commuting-retractions/admission.json'))
        elif row['review_record']=='audit/normal-kernels/admission.json':
            check_previous_kernel_artifacts(review,load('audit/commuting-retractions/admission.json'))
        else:
            check_bindings(review['artifacts'])
        recorded = {r['path']:r for r in review['artifacts']}
        for name in row.get('tex_inputs', []):
            need(name in recorded, 'TeX input missing from the proof review: '+name)
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

def check_topic_a_measurement():
    prefix = 'audit/topic-a/v2/measurement/'
    admission = load(prefix+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_TOPIC_A_MEASUREMENT',
         'Topic A measurement has not been admitted.')
    check_bindings(admission['artifacts'])
    spec = load(prefix+'input_spec.json')
    check_bindings(spec['published_artifacts'])
    result = load(prefix+'results.json')
    independent = load(prefix+'accepted_current_recount.json')
    need(result['documents']==independent['documents'], 'Topic A independent counts differ.')
    sources = ['L032','L034','F016','F013','L035','N009']
    applications = ['A1','A2','A3','A4','A5','A6']
    need(spec['source_sequence']==admission['source_ids']==sources and
         spec['application_sequence']==admission['application_ids']==applications,
         'Topic A source/application correspondence changed.')
    metrics = ['whitespace_tokens','alphanumeric_units','characters_without_whitespace',
               'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
    need(spec['metrics']==metrics and spec['normalizations']==['NFC','NFKC'] and
         spec['variants']==['untrimmed','raw_selected','calibrated_selected'],
         'Topic A measurement conventions changed.')
    need(set(result['documents'])==set(sources+applications+['U_A','code']),
         'Topic A document set changed.')
    check_bindings(spec['required_programs'])
    need(len(spec['required_programs'])==len(result['complete_raw_program_files'])==4 and
         sum(r['bytes'] for r in spec['required_programs'])==56375,
         'Topic A complete program boundary changed.')
    fractions = 0
    def check_ratio(record, numerator, denominator):
        expected = Fraction(numerator, denominator)
        need(record=={'numerator':numerator,'denominator':denominator,
                      'reduced_fraction':str(expected),'decimal':float(expected)},
             'Topic A ratio has a changed numerator or denominator.')
    for form in spec['normalizations']:
        for variant in spec['variants']:
            for metric in metrics:
                c = {key:row['metrics'][form][variant][metric]
                     for key,row in result['documents'].items()}
                need(all(isinstance(v,int) and v>0 for v in c.values()),
                     'Invalid Topic A document cost.')
                total = sum(c[k] for k in sources)
                local = sum(c[k] for k in applications)
                written = c['U_A']+local
                raw = sum(r['metrics'][form][metric] for r in result['complete_raw_program_files'])
                saved = result['factors'][form][variant][metric]
                need(saved['costs']=={'full_sources':total,'full_umbrella':c['U_A'],
                     'six_applications':local,'full_written_papers':written,
                     'complete_printed_program_appendix':c['code'],
                     'full_program_inclusive':written+c['code'],'complete_raw_program_files':raw},
                     'Topic A acquisition costs changed.')
                check_ratio(saved['written_topic'],total,written)
                check_ratio(saved['program_inclusive_topic'],total,written+c['code'])
                check_ratio(saved['raw_program_representation_sensitivity'],total,written+raw)
                check_ratio(saved['printed_program_to_written_papers'],c['code'],written)
                rows = saved['conditional_applications']
                need(len(rows)==6, 'Topic A conditional list incomplete.')
                for source,application,entry in zip(sources,applications,rows):
                    need(entry['source_id']==source and entry['application_id']==application and
                         entry['given']=='Whole U_A and whole complete required program appendix already acquired.',
                         'Topic A conditional acquisition assumption changed.')
                    check_ratio(entry['factor'],c[source],c[application])
                fractions += 10
    need(fractions==300 and result['independent_metric_agreements']==420 and
         result['independent_text_hash_agreements']==84 and result['no_whole_visible_text_claim'],
         'Topic A review dimensions or visible-content limitation changed.')
    need(all(result[key] is None for key in ['missing_visible_text_cost',
         'graphical_structure_cost','external_proof_library_cost','historical_external_program_cost']),
         'Unknown Topic A costs must remain unknown.')
    primary = result['factors']['NFC']['calibrated_selected']['characters_without_whitespace']
    need(admission['primary']==primary, 'Topic A headline values differ from the complete ledger.')
    reader = load(prefix+'reader_admission.json')
    check_bindings(reader['artifacts'])
    need(reader['numerical_admission_sha256']==digest((ROOT/(prefix+'admission.json')).read_bytes()),
         'Topic A reader uses a different numerical admission.')
    return 420, fractions

def check_topic_a_dag():
    prefix = 'audit/topic-a/v2/dag/'
    admission = load('audit/topic-a/v2/dag_admission.json')
    need(admission['status']=='PASS_ROOT_REVIEWED_TOPIC_A_PAIRED_DAG',
         'Topic A paired graph has not been admitted.')
    check_bindings(admission['artifacts'])
    for name, original in [('measurement.json','results.json'),
                           ('measurement_admission.json','admission.json')]:
        need((ROOT/(prefix+'inputs/'+name)).read_bytes()==
             (ROOT/('audit/topic-a/v2/measurement/'+original)).read_bytes(),
             'Topic A graph uses a different numerical edition.')
    weights = load(prefix+'inputs/weighted/weights.json')
    partition = load(prefix+'inputs/weighted/partition.json')
    graph = load(prefix+'inputs/logical/logical_graph.json')
    measured = load('audit/topic-a/v2/measurement/results.json')
    forms = ['NFC','NFKC']
    metrics = ['whitespace_tokens','alphanumeric_units','characters_without_whitespace',
               'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
    need(weights['normalizations']==forms and weights['metrics']==metrics,
         'Topic A graph changed its measurement conventions.')
    need(set(partition['documents'])==set(weights['document_totals'])==set(measured['documents']),
         'Topic A graph omitted a document.')
    need(set(weights['owner_weights'])==set(partition['owners']),
         'Topic A owner weights and partition differ.')
    node_ids = {n['id'] for n in graph['nodes']}
    need(len(node_ids)==len(graph['nodes'])==236 and len(graph['edges'])==392,
         'Topic A documentary graph changed without review.')
    need(set(weights['logical_node_cost_interfaces'])==node_ids,
         'Topic A graph nodes lack cost interfaces.')
    cells = spans = 0
    for key, document in partition['documents'].items():
        owners = {owner for owner, row in partition['owners'].items() if row['document']==key}
        end = 0
        for span in document['spans']:
            need(span['start']==end and span['end']>end and span['node'] in owners,
                 'Topic A text partition has a gap, overlap or foreign owner.')
            end = span['end']; spans += 1
        need(end==document['selected_calibrated_codepoints'], 'Topic A partition omits trailing text.')
        for form in forms:
            for metric in metrics:
                total = sum(weights['owner_weights'][owner][form][metric] for owner in owners)
                expected = measured['documents'][key]['metrics'][form]['calibrated_selected'][metric]
                need(total==weights['document_totals'][key][form][metric]==expected,
                     'Topic A graph loses or duplicates paid text.')
                cells += 1
    need(cells==140 and spans==341 and len(partition['owners'])==337,
         'Topic A ownership review dimensions changed.')
    need(weights['whole_document_total_is_authoritative'] and
         weights['raw_node_count_ratio'] is None and weights['proof_count_ratio'] is None,
         'Topic A graph cannot create a ratio from node counts.')
    for key, value in weights['unknown_costs'].items():
        if key != 'note':
            need(value is None, 'Unknown Topic A dependency costs became numbers.')
    need(weights['program_representation']['raw_file_metrics_are_alternative_not_additional'] and
         weights['program_representation']['shared_across_A5_A6_charged_once'],
         'Topic A program must be paid once in its complete representation.')
    return cells

def check_topic_b_proofs():
    review = load('audit/topic-b/v2/admission.json')
    need(review['status']=='PASS_ROOT_ADMITTED_TOPIC_B_COMMON_PROOFS',
         'Unreviewed Topic B proof edition.')
    check_bindings(review['artifacts'])
    base = 'papers/topic-b/v2/'
    author = load(base+'manifest.json')
    for row in author['exports']:
        check_bindings([dict(row, path=base+row['path'])])
    need(digest((ROOT/base/'manifest.json').read_bytes())==review['author_manifest_sha256'],
         'Topic B author edition changed.')
    need(digest((ROOT/base/'mapping_correction/manifest.json').read_bytes())==
         review['mapping_correction_manifest_sha256'] and
         digest((ROOT/'audit/topic-b/v2/independent_review/manifest.json').read_bytes())==
         review['independent_review_manifest_sha256'], 'Topic B review or correction edition changed.')
    independent = load(review['independent_review'])
    need(independent['status']=='ACCEPT_WITH_DECLARED_SCOPE_AND_ADDITIVE_MAP_CORRECTION' and
         independent['author_manifest']['sha256']==review['author_manifest_sha256'] and
         independent['mapping_delta_manifest']['sha256']==review['mapping_correction_manifest_sha256'] and
         independent['current_source_contract_map']['sha256']==
         digest((ROOT/review['authoritative_source_map']).read_bytes()),
         'Topic B admission differs from its independent review.')
    documents = load(base+'documents.json')['documents']
    catalogue = load('papers/catalogue.json')
    editions = [r for r in catalogue['new_editions'] if r['topic']=='B']
    expected_sources = {'UB':[], 'B1':['N001'], 'B2':['N003'], 'B3':['N008'], 'B4':['L030']}
    need(len(editions)==5 and catalogue['current_topic_editions']['B']==[r['id'] for r in editions],
         'Topic B current catalogue must contain exactly its five scientific papers.')
    for doc, edition in zip(documents[:5], editions):
        need(edition['id']=='topic-b/v2/'+Path(doc['tex']).stem and
             edition['tex']==base+doc['tex'] and edition['pdf']==base+doc['pdf'] and
             edition['tex_inputs']==[base+p for p in doc['tex_inputs'] if p!=doc['tex']] and
             edition['source_contracts']==expected_sources[doc['id']] and
             edition['role']==('umbrella' if doc['id']=='UB' else 'application') and
             edition['application_id']==('U_B' if doc['id']=='UB' else doc['id']) and
             edition['physical_pages']==doc['physical_pdf_pages'] and
             edition['review_record']=='audit/topic-b/v2/admission.json',
             'Topic B catalogue changed a proof, input or source mapping.')
    original = load(base+'source_contract_map.json')
    corrected = load(review['authoritative_source_map'])
    old = {r['adapter']:r for r in original['rows']}
    rows = corrected['rows']
    need(len(rows)==len({r['adapter'] for r in rows})==len(old)==30 and
         {r['source_id'] for r in rows}=={'N001','N003','N008','L030'},
         'Topic B must preserve exactly four contracts and thirty clauses.')
    expected = {'C10':['B3.Coordinates','B3.Ladder'],
                'C11':['B3.Frattini','B3.Quotient']}
    for row in rows:
        prior = old[row['adapter']]
        for key in set(prior)|set(row):
            if row['adapter'] in expected and key in ('new_tex_nodes','new_tex_spans'):
                continue
            need(row.get(key)==prior.get(key), 'Changed Topic B source clause: '+row['adapter'])
        if row['adapter'] in expected:
            need(row['new_tex_nodes']==expected[row['adapter']], 'Wrong corrected proof owner.')
    proof = load(base+'proof_map.json')
    nodes = {r['id']:r for r in proof['nodes']}
    need(len(nodes)==len(proof['nodes'])==29, 'Incomplete Topic B proof map.')
    for node in nodes.values():
        body = (ROOT/base/node['file']).read_text()
        span = body[node['start_codepoint']:node['end_codepoint_exclusive']]
        need(digest(span.encode())==node['sha256_utf8'], 'Changed Topic B written proof span.')
    for row in rows:
        need([n['id'] for n in row['new_tex_spans']]==row['new_tex_nodes'],
             'Topic B mapping must retain each complete proof span.')
        for node in row['new_tex_spans']:
            need(all(nodes[node['id']][k]==v for k,v in node.items()),
                 'Topic B source mapping differs from written proof.')
    fresh = load(review['root_public_replay'])
    scope = load(base+'formal/scope.json')
    need(fresh['status']=='PASS' and fresh['author_manifest_sha256']==review['author_manifest_sha256']
         and fresh['source_sha256']==digest((ROOT/base/'formal/ResidualGeneration.lean').read_bytes()),
         'Topic B lacks the fresh public Lean replay.')
    need([r['name'] for r in fresh['axioms']]==scope['reported_declarations'] and
         len(fresh['axioms'])==6 and all(set(r['axioms']) <=
         {'propext','Classical.choice','Quot.sound'} for r in fresh['axioms']),
         'Topic B declaration or axiom scope changed.')
    need([(r['label'],r['returncode']) for r in fresh['executions']]==
         [('ResidualGeneration',0),('without_membership',1),('without_outside',1),
          ('without_maximality',1)] and fresh['altered_countermodel_rejected'] is True,
         'Topic B hypothesis controls incomplete.')
    need([(r['id'],r['pages']) for r in fresh['rendered']]==
         [('UB',5),('B1',3),('B2',5),('B3',4),('B4',5),('scope',2)],
         'Topic B lacks the complete PDF replay.')
    need(author['required_mathematical_programs']==[] and
         corrected['source_original_pdf_missing']==['N001'] and
         review['compression_ratio'] is None and review['new_source_credit']==0 and
         review['new_question_credit']==0,
         'Topic B publication cannot invent a measurement or new result credit.')
    return len(rows), len(fresh['axioms'])


def check_topic_b_measurement():
    base = 'audit/topic-b/v2/measurement/'
    packet = base+'packet/'
    admission = load(base+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_TOPIC_B_MEASUREMENT',
         'Unreviewed Topic B measurement.')
    check_bindings(admission['artifacts'])
    for relative, field in [('packet/manifest.json','packet_manifest_sha256'),
                            ('arithmetic_review/manifest.json','arithmetic_review_manifest_sha256')]:
        need(digest((ROOT/base/relative).read_bytes())==admission[field],
             'Changed Topic B measurement edition.')
    author = load(packet+'manifest.json')
    for row in author['exports']:
        check_bindings([dict(row, path=packet+row['path'])])
    counts = load(packet+'inputs/author_counts.json')
    recount = load(packet+'independent/recount.json')
    input_review = load(packet+'independent/review.json')
    review = load(base+'arithmetic_review/review.json')
    need(input_review['status']=='ACCEPT_INDEPENDENT_DOCUMENT_MEASUREMENT' and
         input_review['proposal_manifest_sha256']==
         digest((ROOT/packet/'inputs/manifest.json').read_bytes()),
         'Topic B measurement lacks accepted input recount.')
    need(review['status']=='ACCEPT_INDEPENDENT_ARITHMETIC_AND_READER_REVIEW' and
         review['author_manifest_sha256']==admission['packet_manifest_sha256'] and
         review['independent_input_review_manifest_sha256']==
         digest((ROOT/packet/'independent/manifest.json').read_bytes()),
         'Topic B arithmetic review refers to different inputs.')
    result = load(packet+'results.json')
    for relative, value in result['bindings'].items():
        need(not Path(relative).is_absolute() and '..' not in Path(relative).parts and
             digest((ROOT/packet/relative).read_bytes())==value,
             'Topic B arithmetic input changed.')
    spec = importlib.util.spec_from_file_location('topic_b_arithmetic',
        ROOT/base/'arithmetic_review/check.py')
    arithmetic = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(arithmetic)
    with (ROOT/packet/'overall_costs.csv').open(newline='') as stream:
        overall = list(csv.DictReader(stream))
    with (ROOT/packet/'conditional_costs.csv').open(newline='') as stream:
        conditional = list(csv.DictReader(stream))
    primary = arithmetic.audit(result, counts, recount, overall, conditional)
    need(primary==review['primary']==admission['primary'],
         'Topic B headline differs from the accepted full calculation.')
    binding = load(packet+'inputs/publication_binding.json')
    documents = binding['scientific_documents']
    need(set(documents)=={'U_B','B1','B2','B3','B4'},
         'Topic B measurement must charge all five scientific papers.')
    for name, row in documents.items():
        need(row['public_path'].startswith('papers/topic-b/v2/') and
             digest((ROOT/row['public_path']).read_bytes())==row['pdf_sha256']==
             counts['documents'][name]['pdf_sha256'] and
             row['pages']==counts['documents'][name]['pages'],
             'Topic B measured proof edition changed.')
    proof = binding['public_proof_admission']
    need(proof['path']=='audit/topic-b/v2/admission.json' and
         digest((ROOT/proof['path']).read_bytes())==proof['sha256'] and
         admission['new_source_credit']==admission['new_question_credit']==0 and
         admission['overall_factor'] is None,
         'Topic B measurement changed its mathematical scope or missing cost.')
    fresh = load(base+'root_replay.json')
    need(fresh['status']=='PASS_INDEPENDENT_ARITHMETIC_AND_READER_BINDINGS' and
         fresh['coordinates']==30 and fresh['exact_known_conditional_fractions']==90 and
         fresh['unknown_conditional_coordinates']==fresh['unknown_overall_coordinates']==30 and
         fresh['primary']==primary and len(fresh['controls'])==9 and
         all(row['status']=='REJECTED' for row in fresh['controls']),
         'Topic B arithmetic lacks complete replay and hypothesis controls.')
    need(admission['metric_cells']==240 and admission['normalized_text_hashes']==48 and
         admission['full_source_reextraction_in_arithmetic_review'] is False and
         admission['paired_dependency_audit_complete'] is False,
         'Topic B measurement review scope changed.')
    return 240, 90


def check_topic_b_dag():
    base = 'audit/topic-b/v2/dag/'
    admission = load(base+'admission.json')
    need(admission['status']=='PASS_ROOT_REVIEWED_TOPIC_B_PAIRED_DAG',
         'Topic B paired graph is not admitted.')
    check_bindings(admission['artifacts'])
    for folder, expected in admission['packet_manifests'].items():
        need(digest((ROOT/base/folder/'manifest.json').read_bytes())==expected,
             'Topic B graph packet changed: '+folder)
        for row in load(base+folder+'/manifest.json')['exports']:
            check_bindings([dict(row,path=base+folder+'/'+row['path'])])
    for reader_path, public_path in [
            ('logical/logical_graph.json',base+'logical/logical_graph.json'),
            ('logical/coverage.json',base+'logical/coverage.json'),
            ('weighted/partition.json',base+'weighted/partition.json'),
            ('weighted/weights.json',base+'weighted/weights.json'),
            ('ownership_review/review.json',base+'ownership_review/review.json'),
            ('measurement/results.json','audit/topic-b/v2/measurement/packet/results.json')]:
        need((ROOT/base/'reader/inputs'/reader_path).read_bytes()==(ROOT/public_path).read_bytes(),
             'Topic B reader differs from its accepted mathematical or numerical inputs.')
    logical_review = load(base+'logical_review/review.json')
    ownership = load(base+'ownership_review/review.json')
    need(ownership['status']=='PASS_ROOT_INDEPENDENT_OWNERSHIP_REVIEW' and
         ownership['accepted_packet']['sha256']==admission['packet_manifests']['weighted'] and
         ownership['logical_review']['sha256']==admission['packet_manifests']['logical_review'],
         'Topic B owner review refers to another packet.')
    need(logical_review['status']=='ACCEPTED_INDEPENDENT_MATHEMATICAL_DEPENDENCY_REVIEW' and
         logical_review['accepted_packet']['sha256']==admission['packet_manifests']['logical'] and
         admission['independent_logical_review_accepted'] and admission['independent_reader_review_accepted'],
         'Topic B graph lacks independent acceptance.')
    reader_review = load(base+'reader_review/review.json')
    need(reader_review['status']=='ACCEPTED_BOUNDED_INDEPENDENT_READER_REVIEW' and
         reader_review['author_manifest']['sha256']==admission['packet_manifests']['reader'] and
         reader_review['new_source_credit']==reader_review['new_question_credit']==0,
         'Topic B reader review refers to another edition or changed result credit.')
    partition = load(base+'weighted/partition.json')
    weights = load(base+'weighted/weights.json')
    graph = load(base+'logical/logical_graph.json')
    coverage = load(base+'logical/coverage.json')['rows']
    measured = load('audit/topic-b/v2/measurement/packet/independent/recount.json')['documents']
    owners = partition['owners']; costs = weights['owner_costs']
    forms = ['NFC','NFKC']
    metrics = ['whitespace_tokens','alphanumeric_units','characters_without_whitespace',
               'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
    need(set(costs)==set(owners) and set(partition['documents'])==set(measured) and
         len(owners)==214, 'Topic B ownership inventory changed.')
    def total(names):
        return {f:{m:sum(costs[n][f][m] for n in set(names)) for m in metrics} for f in forms}
    spans = cells = 0
    for key, row in partition['documents'].items():
        owned = {n for n,o in owners.items() if o['document']==key}
        end = 0
        for span in row['spans']:
            need(span['start']==end and span['end']>end and span['node'] in owned,
                 'Topic B ownership has a gap, overlap or foreign owner.')
            end=span['end']; spans+=1
        need(end==row['length'],'Topic B trailing text omitted.')
        expected = {f:{m:measured[key]['calibrated_selected'][f][m] for m in metrics} for f in forms}
        need(total(owned)==weights['document_costs'][key]==expected,
             'Topic B graph loses or duplicates complete-document cost.')
        cells+=10
    need(spans==217 and cells==80, 'Topic B ownership dimensions changed.')
    for name in ['h.N008.L3.6','h.N008.T3.4']:
        need(owners[name]['category']=='statement' and
             all(s['category']=='statement' for s in partition['documents']['N008']['spans'] if s['node']==name),
             'A source statement was mislabeled as a printed proof.')
    nodes = {n['id']:n for n in graph['nodes']}; links = weights['node_interfaces']
    need(len(nodes)==184 and len(graph['edges'])==348 and set(nodes)==set(links),
         'Topic B reviewed graph or interface count changed.')
    predecessors = {n:set() for n in nodes}
    for edge in graph['edges']:
        if edge['kind'] in graph['logical_edge_kinds']:
            predecessors[edge['target']].add(edge['source'])
    for name, interface in links.items():
        paid = interface['owners']; node=nodes[name]
        unknown = node['side'] in ('external','verification') or node['document']=='N001'
        need(paid==sorted(set(paid)) and set(paid)<=set(owners) and
             all(owners[n]['document']==node['document'] for n in paid) and
             interface['weight']==(None if unknown else total(paid)),
             'Topic B node interface has an invalid owner union or unknown cost.')
        need(not interface['charged_as_an_additional_item'] and interface['full_dependency_cost'] is None,
             'Topic B overlapping interfaces cannot become additional charges.')
    def check_route(targets, record):
        reached=set(targets); pending=list(targets)
        while pending:
            for n in predecessors[pending.pop()]-reached:
                reached.add(n); pending.append(n)
        paid={owner for n in reached for owner in links[n]['owners']}
        need(record['logical_nodes']==sorted(reached) and record['owners']==sorted(paid) and
             record['known_extracted_text_subtotal']==total(paid) and
             record['unknown_inputs']==sorted(n for n in reached if links[n]['weight'] is None) and
             record['expanded_dependency_cost'] is None,
             'Topic B prerequisite closure loses a premise, text or unknown input.')
    need(len(coverage)==len(weights['source_contract_closures'])==30, 'Topic B source clauses changed.')
    for clause, record in zip(coverage,weights['source_contract_closures']):
        need((clause['adapter'],clause['source_id'])==(record['adapter'],record['source_id']),
             'Topic B source-clause correspondence changed.')
        check_route([clause['historical_output']],record['historical'])
        check_route(clause['new_outputs'],record['replacement'])
    for key,target in graph['new_application_outputs'].items():
        check_route([target],weights['new_application_closures'][key])
    acquisition = load(base+'reader/acquisition.json'); paid=set()
    need(acquisition['sequence']==['U_B','B1','B2','B3','B4'], 'Topic B acquisition order changed.')
    for stage in acquisition['stages']:
        local={n for n,o in owners.items() if o['document']==stage['stage']}
        need(stage['previous_owner_ids']==sorted(paid) and stage['new_owner_ids']==sorted(local-paid) and
             stage['new_cost']==total(local), 'Topic B stage omitted context or paid for common theory again.')
        paid|=local
        need(stage['cumulative_owner_ids']==sorted(paid) and stage['cumulative_cost']==total(paid),
             'Topic B cumulative acquisition does not charge each complete paper once.')
    need(all(weights[k] is None for k in ['whole_historical_pdf_cost','expanded_external_proof_cost',
         'graphic_cost','compression_ratio']) and partition['N001_original_pdf_cost'] is None and
         acquisition['source_cumulative_numeric_curve'] is None and acquisition['raw_node_ratio'] is None and
         admission['new_source_credit']==admission['new_question_credit']==0,
         'Topic B graph invented an unknown cost, a graph factor or new result credit.')
    return cells


def check_topic_c_proofs():
    base = 'papers/topic-c/v2/'
    audit = 'audit/topic-c/v2/'
    admission = load(audit+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_TOPIC_C_COMMON_PROOFS',
         'Unreviewed Topic C mathematical edition.')
    check_bindings(admission['artifacts'])
    for prefix, key in [(base,'author_manifest_sha256'),
                        (audit+'independent_review/','independent_review_manifest_sha256')]:
        need(digest((ROOT/prefix/'manifest.json').read_bytes())==admission[key],
             'Topic C frozen edition changed.')
        for row in load(prefix+'manifest.json')['exports']:
            check_bindings([dict(row,path=prefix+row['path'])])
    scope = load(base+'scope.json')
    review = load(audit+'independent_review/review.json')
    need(review['status']=='ACCEPTED_EXACT_CONTRACT' and
         review['author_manifest']['sha256']==admission['author_manifest_sha256'],
         'Topic C independent review does not accept this author edition.')
    sources = ['L088','N013','L108','F014']
    need(admission['source_ids']==review['source_contract']['source_ids']==sources and
         [row['id'] for row in scope['sources']]==sources,
         'Topic C source boundary changed.')
    spec = importlib.util.spec_from_file_location('topic_c_scope',ROOT/base/'check.py')
    checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
    spans = checker.check_scope(ROOT/base,scope)
    statuses = {}
    for row in scope['source_result_rows']:
        statuses[row['coverage']] = statuses.get(row['coverage'],0)+1
    need(len(scope['source_result_rows'])==admission['contract_rows']==40 and spans==45 and
         statuses==admission['row_status_counts']==review['source_contract']['row_status_counts'],
         'Topic C contract lost corrections, exclusions or exact proof spans.')
    catalogue = load('papers/catalogue.json')
    entries = [row for row in catalogue['new_editions'] if row['topic']=='C']
    need(entries==admission['catalogue_entries'] and len(entries)==5 and
         catalogue['current_topic_editions']['C']==[row['id'] for row in entries],
         'Topic C catalogue changed its complete TeX routes.')
    need([row['application_id'] for row in entries]==['U_C','C1','C2','C3','C4'] and
         [row['source_contracts'] for row in entries]==[[],['L088'],['N013'],['L108'],['F014']] and
         [row['physical_pages'] for row in entries]==[10,4,6,4,3],
         'Topic C application boundary changed.')
    for row in entries:
        name = row['id'].removeprefix('topic-c/v2/')
        need(row['tex']==base+name+'.tex' and row['pdf']==base+name+'.pdf' and
             row['review_record']==audit+'admission.json' and
             row['role']==('umbrella' if row['application_id']=='U_C' else 'application'),
             'Topic C catalogue has an incorrect mathematical route.')
        inputs = re.findall(r'\\input\{([^}]+)\}',(ROOT/row['tex']).read_text())
        expected = [base+s+('' if s.endswith('.tex') else '.tex') for s in inputs]
        need(row['tex_inputs']==expected,'Topic C catalogue omitted a complete TeX input.')
    formal = load(base+'formal/scope.json')
    fresh = load(audit+'root_replay/formal.json')
    need(fresh['status']=='PASS' and fresh['formal_scope']==formal['formal_scope'] and
         fresh['not_formalized']==formal['not_formalized'] and len(fresh['countermodels'])==5,
         'Topic C fresh formal replay changed its scope.')
    need([m['source'] for m in fresh['modules']]==formal['modules'],
         'Topic C fresh Lean report refers to different sources.')
    for module in fresh['modules']:
        source = module['source']
        need(digest((ROOT/base/'formal'/source['file']).read_bytes())==source['sha256'] and
             [r['name'] for r in module['axioms']]==source['declarations'] and
             all(set(r['axioms']) <= {'propext','Classical.choice','Quot.sound'}
                 for r in module['axioms']), 'Topic C Lean declaration or axiom changed.')
    need(sum(len(m['axioms']) for m in fresh['modules'])==16 and
         admission['fresh_lean_declarations']==16 and admission['new_lean_declarations']==9 and
         admission['reused_lean_declarations']==7 and admission['end_to_end_source_formalization'] is False,
         'Topic C formal coverage was inflated.')
    programs = [r['file'] for r in scope['required_programs'] if r['required_mathematics']]
    need(programs==admission['required_mathematical_programs'] and len(programs)==2,
         'Topic C must preserve both complete required programs.')
    census = load(audit+'independent_review/replay/janko/phase150_module_C_j1_replay.json')
    for program in programs:
        need(census['programs'][Path(program['path']).name]==program['sha256'] and
             digest((ROOT/base/program['path']).read_bytes())==program['sha256'],
             'Topic C census used different program bytes.')
    need(census['status']=='PASS' and census['census']['rank4_classes']==6 and
         census['census']['rank5_classes_in_all_subgroups']==0 and
         census['census']['stages']==[[4,100016,40],[5,21352,0]] and
         census['source_geometry_list_read'] is False and admission['independent_full_Janko_replay'] is True,
         'Topic C lacks the full required census.')
    rendered = load(audit+'root_replay/render.json')
    need(rendered['status']=='PASS' and rendered['bound_exports']==38 and
         rendered['primary_bindings_checked']==4 and rendered['prior_contract_bindings_checked']==7 and
         [(r['document'],r['pages'],r['per_page_text_identical']) for r in rendered['fresh_renders']]==
         [('umbrella',10,True),('janko-geometries',4,True),('halving-generalized-cubes',6,True),
          ('petrials-and-faithful-actions',4,True),('equal-adjacent-parameters',3,True),
          ('required-programs',4,True)] and len(rendered['full_code_appendix'])==2,
         'Topic C complete render or code appendix changed.')
    need(admission['compression_ratio'] is None and admission['original_L108_pdf_cost'] is None and
         admission['new_source_credit']==admission['new_question_credit']==0,
         'Topic C publication cannot create a measurement or new result credit.')
    return 40,16


def check_topic_c_measurement():
    base = 'audit/topic-c/v2/measurement/'
    admission = load(base+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_TOPIC_C_MEASUREMENT',
         'Topic C measurement is not independently admitted.')
    check_bindings(admission['artifacts'])
    for folder, expected in admission['packet_manifests'].items():
        need(digest((ROOT/base/folder/'manifest.json').read_bytes())==expected,
             'Changed Topic C numerical packet: '+folder)
        for row in load(base+folder+'/manifest.json')['exports']:
            check_bindings([dict(row,path=base+folder+'/'+row['path'])])
    packet = base+'packet/'
    result = load(packet+'results.json')
    counts = load(packet+'inputs/author_counts.json')
    recount = load(packet+'independent/recount.json')
    specification = load(packet+'inputs/replacement_input_spec.json')
    input_review = load(packet+'independent/review.json')
    review = load(base+'arithmetic_review/review.json')
    need(input_review['status']=='ACCEPT_INDEPENDENT_DOCUMENT_MEASUREMENT' and
         input_review['proposal_manifest_sha256']==digest((ROOT/packet/'inputs/manifest.json').read_bytes()) and
         review['status']=='ACCEPT_INDEPENDENT_ARITHMETIC_AND_READER_REVIEW' and
         review['author_manifest_sha256']==admission['packet_manifests']['packet'] and
         review['independent_input_review_manifest_sha256']==digest((ROOT/packet/'independent/manifest.json').read_bytes()),
         'Topic C recount and arithmetic reviews refer to different inputs.')
    for path, value in result['bindings'].items():
        need(not Path(path).is_absolute() and '..' not in Path(path).parts and
             digest((ROOT/packet/path).read_bytes())==value,'Topic C arithmetic input changed.')
    spec = importlib.util.spec_from_file_location('topic_c_arithmetic',ROOT/base/'arithmetic_review/check.py')
    arithmetic = importlib.util.module_from_spec(spec); spec.loader.exec_module(arithmetic)
    with (ROOT/packet/'overall_costs.csv').open(newline='') as stream:
        overall = list(csv.DictReader(stream))
    with (ROOT/packet/'conditional_costs.csv').open(newline='') as stream:
        conditional = list(csv.DictReader(stream))
    primary = arithmetic.audit(result,counts,recount,specification,overall,conditional)
    need(primary==review['primary']==admission['primary'] and
         admission['headline_written_formula']==result['headline_formula'] and
         admission['required_program_inclusive_formula']==result['required_program_inclusive_formula'],
         'Topic C written and required-program figures changed.')
    previous = load(base+'previous/results.json')
    need(previous['coordinates']==result['coordinates'] and previous['primary']==primary and
         (ROOT/base/'previous/conditional_costs.csv').read_bytes()==(ROOT/packet/'conditional_costs.csv').read_bytes(),
         'Topic C additive presentation revision changed measured values.')
    binding = load(packet+'inputs/publication_binding.json')
    need(set(binding['scientific_documents'])=={'U_C','C1','C2','C3','C4','CODE'},
         'Topic C omitted a complete scientific paper or code appendix.')
    for name, row in binding['scientific_documents'].items():
        need(row['public_path'].startswith('papers/topic-c/v2/') and
             digest((ROOT/row['public_path']).read_bytes())==row['pdf_sha256']==counts['documents'][name]['pdf_sha256'],
             'Topic C measured proof PDF changed.')
    need(binding['admission']['path']=='audit/topic-c/v2/admission.json' and
         digest((ROOT/binding['admission']['path']).read_bytes())==binding['admission']['sha256'],
         'Topic C measurement changed the admitted mathematical edition.')
    for row in specification['required_mathematical_programs']:
        check_bindings([dict(path=row['public_path'],bytes=row['bytes'],sha256=row['sha256'])])
    fresh = load(base+'root_replay.json')
    need(fresh['status']=='PASS_INDEPENDENT_ARITHMETIC_AND_CSV_REVIEW' and
         fresh['author_manifest_sha256']==admission['packet_manifests']['packet'] and
         fresh['coordinates']==30 and fresh['exact_known_conditional_fractions']==90 and
         fresh['symbolic_overall_formulas']==90 and fresh['unknown_conditional_coordinates']==30 and
         len(fresh['controls'])==12 and all(r['rejected'] for r in fresh['controls']),
         'Topic C lacks complete independent arithmetic replay.')
    need(admission['metric_cells']==270 and admission['normalized_text_hashes']==54 and
         admission['raw_program_metric_cells']==20 and admission['overall_factor'] is None and
         admission['L108_original_pdf_cost'] is None and
         admission['new_source_credit']==admission['new_question_credit']==0 and
         admission['paired_dependency_audit_complete'] is False,
         'Topic C counting scope or unknown input changed.')
    return 270,90


def check_topic_d_proofs():
    base = 'papers/topic-d/v2/'
    audit = 'audit/topic-d/v2/'
    admission = load(audit+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_TOPIC_D_COMMON_PROOFS',
         'Unreviewed Topic D mathematical edition.')
    check_bindings(admission['artifacts'])
    for prefix, key in [(base,'author_manifest_sha256'),
                        (audit+'independent_review/','independent_review_manifest_sha256'),
                        (audit+'root_adoption/','root_adoption_manifest_sha256')]:
        need(digest((ROOT/prefix/'manifest.json').read_bytes())==admission[key],
             'Changed Topic D frozen packet.')
        for row in load(prefix+'manifest.json')['exports']:
            check_bindings([dict(row,path=prefix+row['path'])])
    scope = load(base+'scope.json')
    review = load(audit+'independent_review/review.json')
    need(review['status']=='ACCEPTED' and review['corrections_requested']==[] and
         review['author_manifest']['sha256']==admission['author_manifest_sha256'],
         'Topic D review does not accept this edition.')
    need(scope['intake_closed'] and scope['source_ids']==admission['source_ids']==['L066','L074','L104'],
         'Topic D changed the source boundary.')
    expected = [f'{s}.{i}' for s,n in [('L066',16),('L074',17),('L104',4)] for i in range(1,n+1)]
    need([r['id'] for r in scope['contracts']]==expected and
         scope['contract_count']==admission['contract_rows']==37 and
         len(scope['proof_spans'])==admission['proof_spans']==19,
         'Topic D omitted a source row or proof span.')
    statuses = {}
    for row in scope['contracts']:
        statuses[row['current_status']] = statuses.get(row['current_status'],0)+1
        need(row['current_proof_spans'] and
             all(s in scope['proof_spans'] for s in row['current_proof_spans']) and
             row['source_pages'] and
             all(1 <= p <= scope['sources'][row['source_id']]['pages'] for p in row['source_pages']),
             'Topic D source row lost its proof or exact page reference.')
    need(statuses==admission['row_status_counts'] and scope['contracts'][-1]['current_status']==
         'excluded_secondary_assertions_in_printed_main_article_and_supplement',
         'Topic D erased a qualification or excluded printed-body assertion.')
    for row in scope['proof_spans'].values():
        source = (ROOT/base/row['path']).read_text()
        a,b = row['start_codepoint'],row['end_codepoint_exclusive']
        need(0 <= a < b <= len(source) and digest(source[a:b].encode())==row['sha256_utf8'],
             'Topic D proof span changed.')
    for row in scope['documents']:
        check_bindings([dict(row,path=base+row['path'])])
    inventory = scope['program_inventory']
    need(inventory==admission['program_inventory'] and len(inventory)==10 and
         sum(r['category']=='mathematical_program' for r in inventory)==8 and
         sum(r['category']=='driver' for r in inventory)==2,
         'Topic D lost a complete program or driver.')
    for row in inventory:
        check_bindings([dict(path=base+row['copy'],bytes=row['bytes'],sha256=row['sha256'])])
    cost = scope['cost_scope']
    need(cost['full_common_paper_charged_once_in_this_topic'] and not cost['cross_topic_discount'] and
         cost['full_mathematical_programs']==8 and cost['required_programs']==5 and
         cost['additional_diagnostic_programs']==3 and cost['complete_drivers']==2 and
         cost['ratio'] is None and cost['historical_program_cost'] is None and cost['image_cost'] is None,
         'Topic D changed its full cost boundary or invented a measurement.')
    catalogue = load('papers/catalogue.json')
    entries = [r for r in catalogue['new_editions'] if r['topic']=='D']
    need(entries==admission['catalogue_entries'] and len(entries)==4 and
         catalogue['current_topic_editions']['D']==[r['id'] for r in entries] and
         [r['application_id'] for r in entries]==['U_D','D1','D2','D3'] and
         [r['source_contracts'] for r in entries]==[[],['L066'],['L074'],['L104']] and
         [r['physical_pages'] for r in entries]==[6,5,6,2],
         'Topic D catalogue changed its complete manuscript routes.')
    for row in entries:
        name = row['id'].removeprefix('topic-d/v2/')
        need(row['tex']==base+name+'.tex' and row['pdf']==base+name+'.pdf' and
             row['review_record']==audit+'admission.json' and
             row['role']==('umbrella' if row['application_id']=='U_D' else 'application'),
             'Topic D catalogue has an incorrect mathematical route.')
        inputs = re.findall(r'\\input\{([^}]+)\}',(ROOT/row['tex']).read_text())
        need(row['tex_inputs']==[base+s+('' if s.endswith('.tex') else '.tex') for s in inputs],
             'Topic D catalogue omitted a complete TeX input.')
    formal = load(base+'formal/scope.json')
    fresh = load(audit+'independent_review/fresh_formal_report.json')
    need(fresh['status']=='PASS' and fresh['formal_scope']==formal['formal_scope'] and
         fresh['not_formalized']==formal['not_formalized'] and len(fresh['countermodels'])==6 and
         [m['source'] for m in fresh['modules']]==formal['modules'],
         'Topic D fresh Lean report changed its hypotheses or scope.')
    for module in fresh['modules']:
        source = module['source']
        check_bindings([dict(path=base+'formal/'+source['file'],bytes=source['bytes'],sha256=source['sha256'])])
        need([r['name'] for r in module['axioms']]==source['declarations'] and
             all(set(r['axioms']) <= {'propext','Classical.choice','Quot.sound'} for r in module['axioms']),
             'Topic D Lean declarations or axioms changed.')
    need(sum(len(m['axioms']) for m in fresh['modules'])==10 and
         admission['fresh_lean_declarations']==10 and admission['new_lean_declarations']==8 and
         admission['reused_lean_declarations']==2 and not admission['end_to_end_source_formalization'] and
         review['formal_review']['later_support_formal_packet_included'] is False and
         admission['later_support_formal_packet_included'] is False,
         'Topic D formal coverage was inflated.')
    replay = load(audit+'independent_review/independent_checks.json')
    census = replay['fresh_replay']
    need(replay['status']=='PASS' and replay['author_manifest_sha256']==admission['author_manifest_sha256'] and
         census['anchors']==146 and census['augmentation_by_rank']==[644,1226,1931,271,0] and
         census['total_candidates']==4072 and census['fusion'][:3]==[[2,8,8],[3,24,19],[4,5,3]] and
         all(r[1:]==[0,0] for r in census['fusion'][3:]) and
         census['witness_semantic_comparison']['exact_groups']==170 and
         census['witness_semantic_comparison']['geometries']==30 and
         census['witness_semantic_comparison']['controls']==2,
         'Topic D lacks the full census and exact witness comparison.')
    packet = load(audit+'independent_review/fresh_packet_report.json')
    need(packet['status']=='PASS' and packet['program_replays']==['small','j2'] and
         packet['formal_replayed'] is True and len(packet['controls'])==7 and
         all(r['rejected'] for r in packet['controls']) and
         packet['code_pdf']['exact_nonspace_text'] is True and len(packet['code_pdf']['programs'])==8 and
         [(r['document'],r['pages'],r['per_page_text_identical']) for r in packet['render']]==
         [('umbrella',6,True),('commuting-involutions',5,True),('suzuki-polyhedra',6,True),
          ('hall-janko-geometries',2,True),('program-appendix',12,True)],
         'Topic D complete computation, code appendix or render evidence changed.')
    need(admission['compression_ratio'] is None and
         admission['new_source_credit']==admission['new_question_credit']==0,
         'Topic D mathematical admission cannot create a ratio or new result credit.')
    return 37,10


def check_topic_d_support_formal():
    base = 'papers/topic-d/v2/support-formal/'
    audit = 'audit/topic-d/v2/support-formal/'
    admission = load(audit+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_GLOBAL_SUPPORT_FORMALIZATION',
         'Unreviewed global support formalization.')
    check_bindings(admission['artifacts'])
    for prefix, key in [(base,'author_manifest_sha256'),
                        (audit+'first_supplement/','first_supplement_manifest_sha256'),
                        (audit+'independent_review/','independent_review_manifest_sha256')]:
        need(digest((ROOT/prefix/'manifest.json').read_bytes())==admission[key],
             'Changed support-formal packet.')
        for row in load(prefix+'manifest.json')['exports']:
            check_bindings([dict(row,path=prefix+row['path'])])
    scope = load(base+'scope.json')
    fresh = load(audit+'independent_review/fresh_report.json')
    review = load(audit+'independent_review/review.json')
    need(review['status']=='ACCEPT_INDEPENDENT_GLOBAL_SUPPORT_FORMAL_REVIEW' and
         review['author_manifest_sha256']==admission['author_manifest_sha256'] and
         review['both_actual_local_Lean_sources_read_completely'] is True and
         review['actual_exported_types_inspected']==6 and review['corrections_requested']==[] and
         fresh['status']=='PASS' and [m['source'] for m in fresh['modules']]==scope['modules'] and
         fresh['formal_scope']==scope['formal_scope'] and fresh['not_formalized']==scope['not_formalized'],
         'Support-formal review and compiled statements disagree.')
    need(digest((ROOT/audit/'independent_review/fresh_report.json').read_bytes())==
         review['fresh_replay_report_sha256'] and
         digest((ROOT/audit/'independent_review/actual_types.txt').read_bytes())==review['actual_types_sha256'],
         'Changed independent formal replay or actual type transcript.')
    for module in fresh['modules']:
        source = module['source']
        check_bindings([dict(path=base+source['file'],bytes=source['bytes'],sha256=source['sha256'])])
        need([r['name'] for r in module['axioms']]==source['declarations'] and
             all(set(r['axioms']) <= {'propext','Classical.choice','Quot.sound'} for r in module['axioms']) and
             digest((ROOT/audit/'independent_review/logs'/(Path(source['file']).stem+'.txt')).read_bytes())==module['log_sha256'],
             'Support-formal declaration, axiom or compiler log changed.')
    need([len(m['axioms']) for m in fresh['modules']]==[12,16] and
         admission['declaration_reports']==review['declaration_reports']==28 and
         admission['first_module_reports']==12 and admission['global_module_reports']==16 and
         (ROOT/base/'SupportCounting.lean').read_bytes()==
         (ROOT/audit/'first_supplement/SupportCounting.lean').read_bytes(),
         'The first formal module must be preserved and counted once.')
    need(len(fresh['Lean_mutations'])==7 and all(r['rejected'] for r in fresh['Lean_mutations']) and
         len(fresh['countermodels'])==10, 'Missing formal hypothesis controls.')
    for row in fresh['Lean_mutations']:
        need(digest((ROOT/audit/'independent_review/logs'/(row['name']+'.txt')).read_bytes())==row['log_sha256'],
             'Changed rejected-mutation log.')
    retained = load(base+'manifest.json')['retained_bindings']
    need([r['original_private_path'] for r in admission['retained_public_bindings']]==[r['path'] for r in retained],
         'Support formalization lost a retained manuscript or previous-source binding.')
    for original, public in zip(retained,admission['retained_public_bindings']):
        need(original['sha256']==public['sha256'] and original['bytes']==public['bytes'],
             'Support-formal retained input differs from the manuscript.')
        check_bindings([public])
    need(digest((ROOT/'audit/topic-d/v2/admission.json').read_bytes())==admission['proof_admission_sha256'] and
         admission['end_to_end_source_formalization'] is False and
         admission['source_specific_hypotheses_verified'] is False and
         admission['divisor_poset_and_number_theoretic_mobius_bridge_verified'] is False and
         admission['new_source_credit']==admission['new_question_credit']==0 and
         admission['compression_ratio'] is None,
         'Generic support formalization cannot inflate source scope or measured credit.')
    return 28


def check_project_lean_runner(legacy_modules):
    admission = load('audit/formal-project/admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_PROJECT_LEAN_RUNNER', 'Unreviewed project Lean runner.')
    check_bindings(admission['artifacts'])
    need((ROOT/'scripts/check_project_lean.py').read_bytes()==
         (ROOT/'audit/formal-project/author/check_project_lean.py').read_bytes(),
         'Published runner differs from its reviewed author source.')
    fresh = load('audit/formal-project/root_review/project_report.json')
    fixtures = load('audit/formal-project/root_review/fixture_report.json')
    need(fixtures['status']=='PASS_ORCHESTRATION_FIXTURES_ONLY' and fixtures['case_count']==14 and
         fixtures['actual_lean_compilations']==0, 'Runner fixture scope changed.')
    need(fresh['status']=='PASS_PARTIAL' and fresh['selected_components']==['topic-b'] and
         fresh['fresh_source_count']==1 and fresh['fresh_axiom_declaration_reports']==6 and
         fresh['all_configured_sources_recompiled_this_invocation'] is False and
         fresh['components']['legacy']['status']=='NOT_SELECTED', 'Runner validation inflated its coverage.')
    expected = {'research/case_study/formal/'+name+'.lean' for name in legacy_modules}
    need({r['path'] for r in fresh['unchecked_sources']}==expected and
         len(fresh['unchecked_sources'])==100, 'Runner lost the unselected library sources.')
    for component in fresh['input_inventory'].values():
        for path, value in component['input_bindings'].items():
            need(digest((ROOT/path).read_bytes())==value, 'Runner input changed: '+path)
    need(fresh['configured_source_count_inventory_only']==101 and
         admission['fresh_full_project_compilation'] is False,
         'Runner inventory must not be reported as a completed whole-project run.')


def check_topic_d_measurement():
    base = 'audit/topic-d/v2/measurement/'
    packet = base+'packet/'
    admission = load(base+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_TOPIC_D_MEASUREMENT',
         'Topic D numerical comparison is not independently admitted.')
    check_bindings(admission['artifacts'])
    for folder,expected in admission['packet_manifests'].items():
        need(digest((ROOT/base/folder/'manifest.json').read_bytes())==expected,
             'Changed Topic D frozen numerical packet: '+folder)
        for row in load(base+folder+'/manifest.json')['exports']:
            check_bindings([dict(row,path=base+folder+'/'+row['path'])])
    for folder,key in [('previous','original_input_manifest_sha256'),
                       ('inputs','corrected_input_manifest_sha256'),
                       ('independent','input_review_manifest_sha256')]:
        need(digest((ROOT/packet/folder/'manifest.json').read_bytes())==admission[key],
             'Topic D original, corrected or independent input packet changed.')
        for row in load(packet+folder+'/manifest.json')['exports']:
            check_bindings([dict(row,path=packet+folder+'/'+row['path'])])
    result = load(packet+'results.json')
    counts = load(packet+'inputs/author_counts.json')
    recount = load(packet+'independent/recount_corrected.json')
    specification = load(packet+'inputs/replacement_input_spec.json')
    boundary = load(packet+'inputs/source_contract_boundary.json')
    input_review = load(packet+'independent/review.json')
    review = load(base+'arithmetic_review/review.json')
    adoption = load(base+'root_adoption/review.json')
    need(input_review['measurement_inputs_accepted'] and input_review['unresolved_corrections']==[] and
         input_review['original_proposal_corrected_not_accepted'] and
         input_review['corrected_proposal_manifest_sha256']==admission['corrected_input_manifest_sha256'] and
         review['status']=='ACCEPT_EXACT_D_NUMERICAL_PACKET_AND_READER' and
         review['author_manifest_sha256']==admission['packet_manifests']['packet'] and
         review['accepted_input_review_sha256']==admission['input_review_manifest_sha256'] and
         review['requested_author_corrections']==[] and
         adoption['status']=='ACCEPT_ROOT_ADOPTION_OF_INDEPENDENT_D_MEASUREMENT' and
         adoption['independent_manifest_sha256']==admission['packet_manifests']['arithmetic_review'],
         'Topic D measurement acceptance refers to different inputs.')
    for path,value in result['bindings'].items():
        need(not Path(path).is_absolute() and '..' not in Path(path).parts and
             digest((ROOT/packet/path).read_bytes())==value, 'Changed Topic D arithmetic input.')
    documents = {'L066','L074','L104','U_D','D1','D2','D3','CODE'}
    need(set(counts['documents'])==set(recount['documents'])==documents and
         all(counts['documents'][n]['variants']==recount['documents'][n]['variants'] for n in documents),
         'Topic D author counts disagree with the independent corrected recount.')
    spec = importlib.util.spec_from_file_location('topic_d_arithmetic',ROOT/base/'arithmetic_review/check.py')
    arithmetic = importlib.util.module_from_spec(spec); spec.loader.exec_module(arithmetic)
    expected = arithmetic.derive(recount,specification)
    arithmetic.validate(result,expected,specification,boundary)
    arithmetic.check_csv(ROOT/packet,result,expected)
    arithmetic.reader_tables((ROOT/packet/'measurement.tex').read_text(),expected)
    primary = expected[('calibrated_selected','NFC','characters_without_whitespace')]
    need(primary==result['primary']==review['primary']==admission['primary'],
         'Topic D published combined or conditional fractions changed.')
    proof = load('audit/topic-d/v2/admission.json')
    scope = load('papers/topic-d/v2/scope.json')
    need(digest((ROOT/'audit/topic-d/v2/admission.json').read_bytes())==
         admission['proof_admission_sha256']==result['public_proof_admission_sha256']==
         input_review['mathematical_admission_sha256'] and
         admission['source_ids']==proof['source_ids']==scope['source_ids']==['L066','L074','L104'] and
         admission['source_contract_rows']==boundary['contract_count']==len(boundary['rows'])==37 and
         [r['id'] for r in boundary['rows']]==[r['id'] for r in scope['contracts']] and
         [r['current_status'] for r in boundary['rows']]==[r['current_status'] for r in scope['contracts']],
         'Topic D measurement changed its exact mathematical coverage.')
    binding = load(packet+'inputs/publication_binding.json')
    need(set(binding['scientific_documents'])=={'U_D','D1','D2','D3','CODE'},
         'Topic D omitted a complete measured replacement document.')
    for name,row in binding['scientific_documents'].items():
        need(row['public_path'].startswith('papers/topic-d/v2/') and
             digest((ROOT/row['public_path']).read_bytes())==row['pdf_sha256']==counts['documents'][name]['pdf_sha256'],
             'Topic D measured scientific PDF changed.')
    for category in ['complete_mathematical_programs','complete_drivers']:
        need(binding[category]==specification[category]==result[category], 'Topic D program specification drifted.')
        for row in specification[category]:
            check_bindings([dict(path=row['public_path'],bytes=row['bytes'],sha256=row['sha256'])])
    need(admission['complete_programs']==len(result['complete_mathematical_programs'])==8 and
         admission['required_programs']==sum(r['classification']=='required' for r in result['complete_mathematical_programs'])==5 and
         admission['diagnostics']==sum(r['classification']=='diagnostic' for r in result['complete_mathematical_programs'])==3 and
         admission['complete_drivers_separate']==len(result['complete_drivers'])==2,
         'Topic D program or separate driver summary changed.')
    fresh = load(base+'root_adoption/fresh_independent_arithmetic.json')
    need(fresh['status']=='PASS_INDEPENDENT_D_ARITHMETIC_CSV_AND_SCOPE' and
         fresh['author_manifest_sha256']==admission['packet_manifests']['packet'] and
         admission['policy_coordinates']==fresh['coordinates']==result['policy_coordinates']==30 and
         admission['exact_combined_fractions']==fresh['exact_combined_fractions']==90 and
         admission['exact_conditional_fractions']==fresh['exact_conditional_fractions']==90 and
         fresh['CSV_rows']==180 and fresh['reader_numeric_table_rows']==11 and
         len(fresh['controls'])==14 and all(r['rejected'] for r in fresh['controls']),
         'Topic D arithmetic evidence or summary lost a comparison.')
    need(admission['metric_cells']==recount['pdf_metric_cells']==240 and
         admission['normalized_text_hashes']==recount['normalized_PDF_text_hashes']==48 and
         admission['raw_program_and_driver_metric_cells']==recount['raw_program_and_driver_metric_cells']==100 and
         admission['unknown_external_costs']==review['unknowns'] and
         all(v is None for v in admission['unknown_external_costs'].values()) and
         not admission['source_specific_formalization'] and not admission['later_support_formal_counted'] and
         not admission['paired_dependency_audit_complete'] and
         admission['new_source_credit']==admission['new_question_credit']==admission['new_formal_credit']==0,
         'Topic D numerical scope invented a cost, proof, graph or result credit.')
    return 240,180


def check_affine_proofs():
    base = 'papers/topic-affine/v2/'
    audit = 'audit/topic-affine/v2/'
    admission = load(audit+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_AFFINE_COMMON_PROOFS',
         'Unreviewed affine mathematical edition.')
    check_bindings(admission['artifacts'])
    for prefix,key in [(base,'author_manifest_sha256'),
                       (audit+'independent_review/','independent_review_manifest_sha256')]:
        need(digest((ROOT/prefix/'manifest.json').read_bytes())==admission[key],
             'Changed frozen affine packet.')
        for row in load(prefix+'manifest.json')['exports']:
            check_bindings([dict(row,path=prefix+row['path'])])
    scope = load(base+'scope.json')
    review = load(audit+'independent_review/review.json')
    need(review['status']=='ACCEPT_INDEPENDENT_AFFINE_PRINCIPAL_EDITION' and
         review['author_manifest_sha256']==admission['author_manifest_sha256'] and
         review['outstanding_corrections']==[], 'Affine review does not accept this edition.')
    need(admission['source_ids']==review['source_ids']==[scope['source']]==['L012'],
         'Affine admission changed its source identity.')
    need([r['id'] for r in scope['source_rows']]==admission['source_row_ids'] and
         len(scope['source_rows'])==scope['ledger_rows']==admission['source_rows']==33 and
         len(scope['proof_regions'])==admission['proof_regions']==17,
         'Affine source rows or full proof regions changed.')
    for row in scope['source_rows']:
        need(row['id']==row['original_record']['id'] and row['new_credit']==0 and
             row['current_regions'] and all(k in scope['proof_regions'] for k in row['current_regions']),
             'Affine source attribution or proof reference changed.')
    for row in scope['proof_regions'].values():
        text = (ROOT/base/row['path']).read_text()
        need(row['start']==0 and row['end']==len(text) and digest(text.encode())==row['sha256'],
             'Affine proof region is not its complete accepted section.')
    expected_programs = {'phase250_affine_check.py','phase250_affine64_kernel.g',
                        'phase250_fixed_groups.g','phase250_base384_census.g',
                        'phase2_cubic_lattice_check.py','phase2_cubic_kernel_check.g'}
    need(len(scope['programs'])==admission['complete_programs']==6 and
         {Path(r['file']).name for r in scope['programs']}==expected_programs,
         'Affine complete program inventory changed.')
    for row in scope['programs']:
        check_bindings([dict(path=base+row['file'],bytes=row['bytes'],sha256=row['sha256'])])
    printed = re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{programs/([^}]+)\}',
                         (ROOT/base/'required-programs.tex').read_text())
    need(len(printed)==6 and set(printed)==expected_programs,
         'Affine appendix lost a complete program.')
    fresh = load(audit+'independent_review/fresh_replay/report.json')
    need(fresh['status']=='PASS' and fresh['source_rows']==33 and fresh['proof_spans']==17 and
         fresh['primary_checked'] and fresh['retained_bindings_checked']==6 and
         len(fresh['printed_programs'])==6 and all(r['complete'] for r in fresh['printed_programs']) and
         fresh['census']==dict(groups=20169,exponent_eligible=1178,adjacent_orbits=4436,generating_triples=0),
         'Affine full replay or catalogue evidence changed.')
    need([(r['paper'],r['pages'],r['exact_text']) for r in fresh['renders']]==
         [('umbrella',7,True),('mixed-prime-polyhedra',9,True),('required-programs',8,True)],
         'Affine complete manuscript or program render changed.')
    need(admission['scientific_pages']==review['scientific_pages']==
         sum(r['pages'] for r in fresh['renders'][:2])==16 and
         admission['complete_program_pages']==review['required_program_pages']==
         fresh['renders'][2]['pages']==8, 'Affine page summaries disagree with the renders.')
    formal = scope['formal_scope']
    names = {n for m in formal['modules'] for n in m['declarations']}
    need(len(names)==len(fresh['axiom_reports'])==9 and {r[0] for r in fresh['axiom_reports']}==names and
         all(set(re.findall(r'[\w.]+',r[1])) <= {'propext','Classical.choice','Quot.sound'}
             for r in fresh['axiom_reports']) and formal['new']==2 and formal['reused']==7 and
         formal['end_to_end'] is False and admission['end_to_end_source_formalization'] is False,
         'Affine scoped formal claims were inflated.')
    need(admission['fresh_lean_declarations']==review['fresh_formal_declarations']==len(names) and
         admission['new_lean_declarations']==review['new_formal_declarations']==formal['new'] and
         admission['reused_lean_declarations']==review['reused_formal_declarations']==formal['reused'],
         'Affine declaration summaries disagree with the checked statements.')
    matrices = load(audit+'independent_review/matrix_report.json')
    need(matrices['status']=='PASS_INDEPENDENT_AFFINE_MATRIX_REVIEW' and
         matrices['source_word_values_checked']==18 and matrices['author_programs_imported'] is False and
         [r['kernel_index'] for r in matrices['cubic_models']]==[4,16],
         'Affine independent matrix evidence changed.')
    catalogue = load('papers/catalogue.json')
    entries = [r for r in catalogue['new_editions'] if r['topic']=='Affine']
    need(entries==admission['catalogue_entries'] and len(entries)==2 and
         catalogue['current_topic_editions']['Affine']==[r['id'] for r in entries] and
         [r['source_contracts'] for r in entries]==[[],['L012']] and
         [r['physical_pages'] for r in entries]==[7,9], 'Affine catalogue routes changed.')
    for row in entries:
        inputs = re.findall(r'\\input\{([^}]+)\}',(ROOT/row['tex']).read_text())
        need(row['tex_inputs']==[base+x+('' if x.endswith('.tex') else '.tex') for x in inputs] and
             row['review_record']==audit+'admission.json', 'Affine TeX input or review omitted.')
    need(scope['principal_contracts']==admission['existing_principal_contracts']==1 and
         scope['project_total_preserved']==admission['project_total_preserved']==27 and
         scope['new_source_credit']==scope['new_question_credit']==admission['new_source_credit']==
         admission['new_question_credit']==0 and scope['compression_ratio'] is None and
         admission['compression_ratio'] is None and scope['cost_boundary']['historical_program_cost'] is None,
         'Affine proof admission invented credit, a ratio or a historical program cost.')
    return 33,9


def check_topic_c_dag():
    base = 'audit/topic-c/v2/dag/'
    admission = load(base+'admission.json')
    need(admission['status']=='PASS_ROOT_REVIEWED_TOPIC_C_PAIRED_DAG',
         'Topic C paired graph is not admitted.')
    check_bindings(admission['artifacts'])
    for folder, expected in admission['packet_manifests'].items():
        need(digest((ROOT/base/folder/'manifest.json').read_bytes())==expected,
             'Topic C graph packet changed: '+folder)
        for row in load(base+folder+'/manifest.json')['exports']:
            check_bindings([dict(row,path=base+folder+'/'+row['path'])])
    for kind, path in [('proof','audit/topic-c/v2/admission.json'),
                       ('measurement','audit/topic-c/v2/measurement/admission.json')]:
        need(digest((ROOT/path).read_bytes())==admission[kind+'_admission_sha256'],
             'Topic C graph uses another scientific or numerical admission.')
    logical_review = load(base+'logical_review/review.json')
    cost_review = load(base+'independent_review/review.json')
    need(logical_review['status']=='ACCEPT_CORRECTED_LOGICAL_GRAPH_WITH_RECORDED_SCOPE' and
         logical_review['accepted_manifest']['sha256']==admission['packet_manifests']['logical'] and
         cost_review['status']=='ACCEPTED_UNCHANGED_COST_DATA_WITH_ADDITIVE_READER_CORRECTION' and
         cost_review['accepted_author_manifest']['sha256']==admission['packet_manifests']['costs'],
         'Topic C dependency or cost review refers to another edition.')
    correction = load(base+'costs/correction.json')
    for name in correction['exact_unchanged_exports']:
        need((ROOT/base/'costs'/name).read_bytes()==(ROOT/base/'costs_previous'/name).read_bytes(),
             'Topic C reader correction changed frozen cost or mathematical data.')
    graph = load(base+'logical/logical_graph.json')
    coverage = load(base+'logical/coverage.json')
    expected = load(base+'logical_review/reviewed_interfaces.json')
    spec = importlib.util.spec_from_file_location('topic_c_graph_review',ROOT/base/'logical_review/check.py')
    review_check = importlib.util.module_from_spec(spec); spec.loader.exec_module(review_check)
    logical_result = review_check.validate(graph,coverage,expected,load('papers/topic-c/v2/scope.json'))
    need((logical_result['nodes'],logical_result['edges'],logical_result['closures'])==(156,249,85),
         'Topic C reviewed logical scope changed.')
    partition = load(base+'costs/partition.json'); weights = load(base+'costs/weights.json')
    view = load(base+'costs/view_data.json'); acquisition = load(base+'costs/acquisition.json')
    measured = load('audit/topic-c/v2/measurement/packet/independent/recount.json')['documents']
    variants = ['raw_untrimmed','raw_selected','calibrated_selected']; forms = ['NFC','NFKC']
    metrics = ['whitespace_tokens','alphanumeric_units','characters_without_whitespace',
               'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
    owners = partition['owners']; costs = weights['owner_costs']
    need(set(owners)==set(costs) and len(owners)==199 and len(measured)==9 and
         set(partition['documents'])==set(measured), 'Topic C complete ownership inventory changed.')
    def total(names):
        names=set(names)
        return {v:{f:{m:sum(costs[n][v][f][m] for n in names) for m in metrics}
                   for f in forms} for v in variants}
    cells = spans = 0
    for key, row in partition['documents'].items():
        local = {n for n,o in owners.items() if o['document']==key}
        need(row['pdf_sha256']==measured[key]['pdf_sha256'] and row['pages']==measured[key]['pages'],
             'Topic C graph changed a measured PDF binding.')
        for variant, data in row['variants'].items():
            end = 0
            for span in data['spans']:
                need(span['start']==end and span['end']>end and span['owner'] in local and
                     span['category']==owners[span['owner']]['category'],
                     'Topic C passage ownership has a gap, overlap or foreign owner.')
                end = span['end']; spans += 1
            need(end==data['length'], 'Topic C trailing measured text omitted.')
        expected_cost = {v:{f:{m:measured[key]['variants'][v][f][m] for m in metrics}
                            for f in forms} for v in variants}
        need(total(local)==weights['document_costs'][key]==expected_cost,
             'Topic C ownership loses or duplicates complete-document cost.')
        cells += 30
    need((cells,spans)==(270,703), 'Topic C document or span dimensions changed.')
    nodes = {n['id']:n for n in graph['nodes']}; links = weights['node_interfaces']
    reader_owners={key:{field:value for field,value in row.items() if field!='label'}
                   for key,row in view['owners'].items()}
    need(set(nodes)==set(links) and view['edges']==graph['edges'] and reader_owners==owners and
         view['owner_weights']==costs, 'Topic C reader changed logical or owner data.')
    predecessors = {n:set() for n in nodes}
    for edge in graph['edges']:
        if edge['kind'] in graph['logical_edge_kinds']:
            predecessors[edge['target']].add(edge['source'])
    for name, interface in links.items():
        paid = interface['owners']; node = nodes[name]
        unknown = node['side'] in ('external','verification') or node['document']=='L108'
        owner_document='CODE' if name in graph['required_mathematical_programs'] else node['document']
        need(paid==sorted(set(paid)) and set(paid)<=set(owners) and
             all(owners[n]['document']==owner_document for n in paid) and
             interface['known_weight']==(None if unknown else total(paid)) and
             not interface['charged_again'] and interface['expanded_dependency_cost'] is None,
             'Topic C node interface changed its unique owners or unknown cost.')
    def closure(targets):
        reached=set(targets); pending=list(targets)
        while pending:
            for n in predecessors[pending.pop()]-reached:
                reached.add(n); pending.append(n)
        return reached
    def union(names):
        return {owner for n in names for owner in links[n]['owners']}
    def check_route(targets, record):
        reached=closure(targets); paid=union(reached)
        need(record['logical_nodes']==sorted(reached) and record['owners']==sorted(paid) and
             record['known_extracted_subtotal']==total(paid) and
             record['unknown_inputs']==sorted(n for n in reached if links[n]['known_weight'] is None) and
             record['expanded_dependency_cost'] is None and record['graphics_cost'] is None,
             'Topic C prerequisite closure changed its cost union or unknown inputs.')
    rows={r['id']:r for r in weights['source_contract_closures']}
    need(len(rows)==len(coverage['rows'])==40, 'Topic C source clauses changed.')
    for clause in coverage['rows']:
        check_route(clause['historical_outputs'],rows[clause['id']]['historical'])
        check_route(clause['new_outputs'],rows[clause['id']]['replacement'])
    for field, result in [('new_application_outputs','new_application_closures'),
                          ('additional_current_comparisons','additional_current_comparisons')]:
        for key,targets in graph[field].items(): check_route(targets,weights[result][key])
    for node in view['nodes']:
        if node['id'] not in nodes: continue
        reached=closure([node['id']]); paid=union(reached)
        need(node['owners']==links[node['id']]['owners'] and node['weight']==links[node['id']]['known_weight'] and
             node['closure']['unique_owner_ids']==sorted(paid) and
             node['closure']['known_owned_text_subtotal']==total(paid) and
             node['closure']['unknown_external_nodes']==sorted(n for n in reached if links[n]['known_weight'] is None),
             'Topic C reader changed a proof route.')
        for locator in node['current_public_locators']:
            text=(ROOT/locator['path']).read_text()
            passage=text[locator['start_codepoint']:locator['end_codepoint_exclusive']]
            need(digest(passage.encode())==locator['sha256_utf8'], 'Topic C public proof locator changed.')
    paid=set()
    need(acquisition==view['acquisition'] and acquisition['sequence']==['U_C','CODE','C1','C2','C3','C4'],
         'Topic C acquisition sequence changed.')
    for step in acquisition['stages']:
        key=step['stage']; local={n for n,o in owners.items() if o['document']==key}
        used=union(closure([n for n,b in nodes.items() if b['document']==key and not n.startswith('program.')]))
        need(not (used-paid-local) and step['previous_owner_ids']==sorted(paid) and
             step['complete_local_owner_ids']==step['new_owner_ids']==sorted(local) and
             step['logical_route_owner_ids']==sorted(used) and step['reused_owner_ids']==sorted(used&paid) and
             step['local_text_outside_route']==sorted(local-used) and step['new_cost']==total(local) and
             step['reused_route_cost']==total(used&paid), 'Topic C acquisition omitted context or discounted reuse twice.')
        paid|=local
        need(step['cumulative_owner_ids']==sorted(paid) and step['cumulative_cost']==total(paid) and
             step['written_cumulative_cost']==total(n for n in paid if owners[n]['document']!='CODE'),
             'Topic C acquisition failed to charge whole theory and applications once.')
    need(view['measurement']==load('audit/topic-c/v2/measurement/packet/results.json'),
         'Topic C graph changed an admitted whole-document or conditional comparison.')
    dimensions={'source_contracts':len(graph['new_application_outputs']),
                'source_rows':len(coverage['rows']),'logical_nodes':len(nodes),
                'typed_edges':len(graph['edges']),'exclusive_owners':len(owners),
                'document_metric_cells':cells,'owner_metric_cells':len(owners)*30,
                'all_variant_spans':spans,'output_closures':logical_result['closures'],
                'known_conditional_fractions':view['measurement']['known_conditional_fractions'],
                'symbolic_combined_expressions':len(view['measurement']['coordinates'])*3}
    need(all(admission[key]==value for key,value in dimensions.items()) and
         admission['independent_logical_review_accepted'] is True and
         admission['independent_cost_and_reader_review_accepted'] is True,
         'Topic C admission summary contradicts the reviewed graph or ownership dimensions.')
    primary=next(row for row in view['measurement']['coordinates']
                 if (row['variant'],row['normalization'],row['unit'])==
                 ('calibrated_selected','NFC','characters_without_whitespace'))
    need(admission['primary_written_denominator']==primary['written_denominator'] and
         admission['primary_program_inclusive_denominator']==primary['complete_denominator'] and
         admission['primary_raw_program_alternative_denominator']==primary['raw_program_denominator'],
         'Topic C admission summary contradicts the complete measured denominators.')
    for row in weights['raw_program_alternative'].values():
        binding=row['binding'];check_bindings([dict(binding,path=binding['public_path'])])
    fresh = load(base+'root_adoption/fresh_cost_review.json')
    need(fresh['status']=='PASS_INDEPENDENT_COSTS_READER_AND_CORRECTION' and
         fresh['independent_arithmetic']['document_metric_cells']==270 and
         fresh['independent_arithmetic']['owner_metric_cells']==5970 and
         len(fresh['independent_arithmetic']['controls'])==15 and
         all(x['rejected'] for x in fresh['independent_arithmetic']['controls']) and
         fresh['independent_viewer']['selected_route_views']==180 and
         all(x['rejected'] for x in fresh['independent_viewer']['controls']),
         'Topic C lacks the independent ownership and reader replay.')
    need(all(weights[k] is None for k in ['complete_historical_pdf_cost','expanded_external_proof_cost',
         'graphic_cost','compression_ratio']) and partition['missing_L108_original_pdf_cost'] is None and
         partition['node_count_ratio'] is None and acquisition['historical_complete_numeric_curve'] is None and
         all(admission[k] is None for k in ['combined_factor','L108_original_pdf_cost','expanded_external_proof_cost',
                                           'graphic_cost','node_count_ratio']) and
         admission['new_source_credit']==admission['new_question_credit']==admission['new_formal_credit']==0 and
         admission['real_browser_layout_test'] is False,
         'Topic C dependency audit invented a missing cost, a ratio or scientific credit.')
    return cells,85


def check_affine_measurement():
    base = 'audit/topic-affine/v2/measurement/'
    packet = base+'packet/'
    admission = load(base+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_AFFINE_MEASUREMENT',
         'Affine numerical comparison lacks independent acceptance.')
    check_bindings(admission['artifacts'])
    need(set(admission['packet_manifests'])=={'packet','arithmetic_review','root_adoption'},
         'Affine measurement archive inventory changed.')
    for folder,pin in admission['packet_manifests'].items():
        need(digest((ROOT/base/folder/'manifest.json').read_bytes())==pin,
             'Changed affine numerical archive: '+folder)
        for row in load(base+folder+'/manifest.json')['exports']:
            check_bindings([dict(row,path=base+folder+'/'+row['path'])])
    for folder,key in [('inputs','input_manifest_sha256'),('independent','input_review_manifest_sha256')]:
        need(digest((ROOT/packet/folder/'manifest.json').read_bytes())==admission[key],
             'Changed affine input or independent review manifest.')
        for row in load(packet+folder+'/manifest.json')['exports']:
            check_bindings([dict(row,path=packet+folder+'/'+row['path'])])
    result = load(packet+'results.json')
    counts = load(packet+'inputs/author_counts.json')
    recount = load(packet+'independent/recount.json')
    specification = load(packet+'inputs/replacement_input_spec.json')
    boundary = load(packet+'inputs/source_contract_boundary.json')
    input_review = load(packet+'independent/review.json')
    review = load(base+'arithmetic_review/review.json')
    adoption = load(base+'root_adoption/review.json')
    need(input_review['status']=='ACCEPTED_ROOT_INDEPENDENT_AFFINE_MEASUREMENT_INPUTS' and
         input_review['requested_corrections']==[] and
         input_review['proposal_manifest_sha256']==admission['input_manifest_sha256'] and
         review['status']=='ACCEPTED_INDEPENDENT_AFFINE_NUMERICAL_AND_READER_REVIEW' and
         review['requested_corrections']==[] and
         review['author_manifest_sha256']==admission['packet_manifests']['packet'] and
         review['input_proposal_manifest_sha256']==admission['input_manifest_sha256'] and
         review['independent_input_review_manifest_sha256']==admission['input_review_manifest_sha256'] and
         adoption['status']=='ACCEPT_ROOT_ADOPTION_OF_INDEPENDENT_AFFINE_MEASUREMENT' and
         adoption['independent_manifest_sha256']==admission['packet_manifests']['arithmetic_review'] and
         adoption['independent_requested_corrections']==[],
         'Affine measurement acceptance refers to different inputs.')
    for path,pin in result['bindings'].items():
        need(not Path(path).is_absolute() and '..' not in Path(path).parts and
             digest((ROOT/packet/path).read_bytes())==pin, 'Changed affine arithmetic input.')
    documents = {'L012','U_Affine','AF1','CODE'}
    need(set(counts['documents'])==set(recount['documents'])==documents and
         all(counts['documents'][n]['variants']==recount['documents'][n]['variants'] for n in documents),
         'Affine author counts differ from the independently accepted recount.')
    spec = importlib.util.spec_from_file_location('affine_independent_arithmetic',ROOT/base/'arithmetic_review/check.py')
    arithmetic = importlib.util.module_from_spec(spec); spec.loader.exec_module(arithmetic)
    tables = arithmetic.audit(result,recount,specification)
    for name,expected in zip(['overall_costs.csv','conditional_costs.csv'],tables):
        with (ROOT/packet/name).open(newline='') as stream:
            need(list(csv.DictReader(stream))==[{k:str(v) for k,v in row.items()} for row in expected],
                 'Affine complete CSV comparison changed.')
    fresh = load(base+'root_adoption/fresh_independent_arithmetic.json')
    need(fresh['status']=='PASS_INDEPENDENT_AFFINE_RESULT_ARITHMETIC' and
         fresh['author_manifest_sha256']==admission['packet_manifests']['packet'] and
         fresh['primary']==result['primary']==admission['primary'] and
         fresh['combined_exact_fractions']==admission['exact_combined_fractions']==90 and
         fresh['conditional_exact_fractions']==admission['exact_conditional_fractions']==30 and
         fresh['CSV_rows']==120 and len(fresh['negative_controls'])==12,
         'Affine arithmetic evidence or primary fractions changed.')
    proof = load('audit/topic-affine/v2/admission.json')
    scope = load('papers/topic-affine/v2/scope.json')
    need(digest((ROOT/'audit/topic-affine/v2/admission.json').read_bytes())==
         admission['proof_admission_sha256']==result['public_proof_admission_sha256']==
         input_review['mathematical_admission_sha256'] and
         admission['source_ids']==proof['source_ids']==[scope['source']]==['L012'] and
         admission['source_contract_rows']==boundary['row_count']==len(boundary['source_rows'])==33 and
         boundary['source_rows']==scope['source_rows'] and
         admission['principal_contracts']==boundary['principal_contracts']==1 and
         admission['project_total_preserved']==boundary['project_total_preserved']==27,
         'Affine measurement changed its mathematical coverage.')
    binding = load(packet+'inputs/publication_binding.json')
    need(set(binding['documents'])=={'U_Affine','AF1','CODE'},
         'Affine omitted a complete replacement document.')
    for name,row in binding['documents'].items():
        need(row['public_path'].startswith('papers/topic-affine/v2/') and
             digest((ROOT/row['public_path']).read_bytes())==row['sha256']==counts['documents'][name]['pdf_sha256'],
             'Affine measured scientific PDF changed.')
    for category in ['complete_mathematical_programs','complete_auxiliary_scripts','complete_formal_files']:
        need(binding[category]==specification[category]==result[category], 'Affine file inventory changed.')
        for row in specification[category]:
            check_bindings([dict(path=row['public_path'],bytes=row['bytes'],sha256=row['sha256'])])
    need(admission['complete_required_programs']==len(result['complete_mathematical_programs'])==6 and
         all(r['classification']=='required' for r in result['complete_mathematical_programs']) and
         admission['complete_auxiliary_scripts_separate']==len(result['complete_auxiliary_scripts'])==3 and
         admission['complete_formal_files_separate']==len(result['complete_formal_files'])==3 and
         admission['existing_Lean_declarations']==sum(len(r['declarations']) for r in result['complete_formal_files'])==9,
         'Affine program or formal summary changed.')
    need(admission['metric_cells']==recount['pdf_metric_cells']==120 and
         admission['normalized_text_hashes']==recount['normalized_PDF_text_hashes']==24 and
         admission['required_program_metric_cells']==recount['required_program_metric_cells']==60 and
         admission['auxiliary_metric_cells']==recount['auxiliary_metric_cells']==30 and
         admission['formal_metric_cells']==recount['formal_metric_cells']==30 and
         admission['policy_coordinates']==result['policy_coordinates']==30 and
         admission['unknown_external_costs']==dict.fromkeys(['retained_external_proofs','historical_software',
             'algorithm_and_catalogue_construction','unextracted_graphics','intrinsic_minimum_complexity']) and
         not admission['source_specific_formalization'] and not admission['paired_dependency_audit_complete'] and
         admission['new_source_credit']==admission['new_question_credit']==admission['new_formal_credit']==0,
         'Affine numerical summary invented a cost, proof, dependency audit or credit.')
    return 120,120


def check_topic_d_dag():
    base = 'audit/topic-d/v2/dag/'
    admission = load(base+'admission.json')
    need(admission['status']=='PASS_ROOT_REVIEWED_TOPIC_D_PAIRED_DAG',
         'Topic D paired dependencies lack acceptance.')
    check_bindings(admission['artifacts'])
    exports = 0
    for folder,pin in admission['packet_manifests'].items():
        need(digest((ROOT/base/folder/'manifest.json').read_bytes())==pin,
             'Topic D frozen graph archive changed: '+folder)
        rows=load(base+folder+'/manifest.json')['exports']; exports+=len(rows)
        for row in rows: check_bindings([dict(row,path=base+folder+'/'+row['path'])])
    need(exports==admission['preserved_frozen_exports']==169 and len(admission['packet_manifests'])==10,
         'Topic D frozen graph inventory changed.')
    for kind,path in [('proof','audit/topic-d/v2/admission.json'),
                      ('measurement','audit/topic-d/v2/measurement/admission.json'),
                      ('support_formal','audit/topic-d/v2/support-formal/admission.json')]:
        need(digest((ROOT/path).read_bytes())==admission[kind+'_admission_sha256'],
             'Topic D graph changed its scientific, numerical or formal input.')
    logical_review=load(base+'logical_review/review.json')
    delta_review=load(base+'logical_delta_review/review.json')
    cost_review=load(base+'independent_review/review.json')
    adoption=load(base+'root_adoption/review.json')
    pins=admission['packet_manifests']
    need(logical_review['status']=='ACCEPTED_INDEPENDENT_SEMANTIC_REVIEW_OF_REVISED_LOGICAL_GRAPH' and
         logical_review['author_manifest_sha256']==pins['logical_previous'] and
         logical_review['requested_further_corrections']==[] and
         delta_review['status']=='ACCEPTED_BOUNDED_LOGICAL_DELTA' and
         delta_review['author_manifest_sha256']==pins['logical'] and
         delta_review['previous_review_manifest_sha256']==pins['logical_review'] and
         cost_review['status']=='ACCEPTED_INDEPENDENT_D_OWNERSHIP_AND_READER' and
         cost_review['author_manifest_sha256']==pins['costs'] and
         cost_review['logical_v3_manifest_sha256']==pins['logical'] and
         cost_review['requested_further_corrections']==[] and
         adoption['status']=='ACCEPT_ROOT_D_LOGICAL_V3_AND_COST_V2' and
         adoption['requested_further_corrections']==[], 'Topic D acceptance refers to another edition.')
    graph=load(base+'logical/logical_graph.json'); coverage=load(base+'logical/coverage.json')
    previous=load(base+'logical_previous/logical_graph.json')
    added=[e for e in graph['edges'] if e not in previous['edges']]
    need(graph['nodes']==previous['nodes'] and all(e in graph['edges'] for e in previous['edges']) and
         len(added)==1 and (added[0]['source'],added[0]['target'],added[0]['kind'])==
         ('UD.ExactSupport','D2.Support','proof_use'), 'Topic D exact logical correction changed.')
    spec=importlib.util.spec_from_file_location('topic_d_logical_review',ROOT/base/'logical_review/check_independent.py')
    logical=importlib.util.module_from_spec(spec); spec.loader.exec_module(logical)
    checked=logical.inspect(graph,coverage)
    need((checked['nodes'],checked['typed_edges'],checked['closures_checked'])==(137,284,116),
         'Topic D logical dimensions changed.')
    scope=load('papers/topic-d/v2/scope.json')
    need({r['id']:r['accepted_record'] for r in coverage['rows']}=={r['id']:r for r in scope['contracts']} and
         len(graph['accepted_scope_spans'])==len(scope['proof_spans'])==19,
         'Topic D graph changed accepted source clauses or proof contexts.')
    partition=load(base+'costs/partition.json'); weights=load(base+'costs/weights.json')
    old_weights=load(base+'costs_previous/weights.json')
    view=load(base+'costs/view_data.json'); acquisition=load(base+'costs/acquisition.json')
    measured=load('audit/topic-d/v2/measurement/packet/independent/recount_corrected.json')['documents']
    variants=['raw_untrimmed','raw_selected','calibrated_selected']; forms=['NFC','NFKC']
    metrics=['whitespace_tokens','alphanumeric_units','characters_without_whitespace',
             'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
    owners=partition['owners']; costs=weights['owner_costs']
    need(set(owners)==set(costs) and len(owners)==220 and set(partition['documents'])==set(measured) and
         len(measured)==8 and weights['owner_costs']==old_weights['owner_costs'] and
         weights['document_costs']==old_weights['document_costs'], 'Topic D complete cost inventory changed.')
    def total(names):
        names=set(names)
        return {v:{f:{m:sum(costs[n][v][f][m] for n in names) for m in metrics} for f in forms} for v in variants}
    spans=selected=0
    for key,row in partition['documents'].items():
        local={n for n,o in owners.items() if o['document']==key}
        need(row['pdf_sha256']==measured[key]['pdf_sha256'] and row['pages']==measured[key]['pages'],
             'Topic D ownership uses a different measured PDF.')
        for variant,data in row['variants'].items():
            end=0
            for span in data['spans']:
                need(span['start']==end and span['end']>end and span['owner'] in local and
                     span['category']==owners[span['owner']]['category'], 'Topic D passage gap, overlap or foreign owner.')
                end=span['end']; spans+=1; selected+=variant=='calibrated_selected'
            need(end==data['length'], 'Topic D measured trailing text omitted.')
        expected={v:{f:{m:measured[key]['variants'][v][f][m] for m in metrics} for f in forms} for v in variants}
        need(total(local)==weights['document_costs'][key]==expected, 'Topic D complete-document costs not conserved.')
    nodes={n['id']:n for n in graph['nodes']}; interfaces=weights['node_interfaces']
    need(set(nodes)==set(interfaces) and view['edges']==graph['edges'] and view['owner_weights']==costs and
         {n:{k:v for k,v in r.items() if k!='label'} for n,r in view['owners'].items()}==owners,
         'Topic D reader changed graph or cost data.')
    need(owners['h.L074.9']['category']=='statement' and
         'h.L074.composite_setup' in interfaces['h.L074.12']['owners'] and
         'D2.Polyhedra.setup' in interfaces['D2.Duality']['owners'], 'Topic D reviewed passage correction lost.')
    for name,interface in interfaces.items():
        paid=interface['owners']; node=nodes[name]
        unknown=node['side']=='external' or (node['side']=='verification' and not name.startswith('diagnostic.'))
        document='CODE' if name in graph['required_mathematical_programs']+graph['diagnostic_programs'] else node['document']
        need(paid==sorted(set(paid)) and set(paid)<=set(owners) and
             all(owners[o]['document']==document for o in paid) and
             interface['known_weight']==(None if unknown else total(paid)) and
             (not unknown or not paid) and not interface['charged_again'] and
             interface['expanded_dependency_cost'] is None, 'Topic D node owners or unknown cost changed.')
    predecessors={n:set() for n in nodes}
    for edge in graph['edges']:
        if edge['kind'] in graph['logical_edge_kinds']: predecessors[edge['target']].add(edge['source'])
    def closure(targets):
        reached=set(targets); pending=list(targets)
        while pending:
            for n in predecessors[pending.pop()]-reached: reached.add(n); pending.append(n)
        return reached
    def union(names): return {o for n in names for o in interfaces[n]['owners']}
    def route(names,record):
        paid=union(names)
        need(record['logical_nodes']==sorted(names) and record['owners']==sorted(paid) and
             record['known_extracted_subtotal']==total(paid) and
             record['unknown_inputs']==sorted(n for n in names if interfaces[n]['known_weight'] is None) and
             record['expanded_dependency_cost'] is None and record['graphics_cost'] is None,
             'Topic D prerequisite union or unknown input changed.')
    rows={r['id']:r for r in weights['source_contract_closures']}; routes=0
    need(len(rows)==len(coverage['rows'])==37, 'Topic D source clause inventory changed.')
    for row in coverage['rows']:
        for output,key in [('historical_outputs','historical'),('new_outputs','replacement')]:
            route(closure(row[output]),rows[row['id']][key]); routes+=1
        route(closure(row['retained_input_nodes'])|set(row['qualification_context_nodes']),
              rows[row['id']]['retained_and_qualification_context']); routes+=1
    for key,targets in graph['new_application_outputs'].items():
        route(closure(targets),weights['new_application_closures'][key]); routes+=1
    for key,record in weights['additional_current_comparisons'].items(): route(closure([key]),record); routes+=1
    locators=0
    for node in view['nodes']:
        if node['id'] not in nodes: continue
        names=closure([node['id']]); paid=union(names)
        need(node['owners']==interfaces[node['id']]['owners'] and node['weight']==interfaces[node['id']]['known_weight'] and
             node['closure']['unique_owner_ids']==sorted(paid) and node['closure']['known_owned_text_subtotal']==total(paid) and
             node['closure']['unknown_external_nodes']==sorted(n for n in names if interfaces[n]['known_weight'] is None),
             'Topic D reader changed a node prerequisite closure.')
        for locator in node['current_public_locators']:
            text=(ROOT/locator['path']).read_text(); passage=text[locator['start_codepoint']:locator['end_codepoint_exclusive']]
            need(digest(passage.encode())==locator['sha256_utf8'], 'Topic D exact public proof locator changed.'); locators+=1
    paid=set()
    need(acquisition==view['acquisition'] and acquisition['sequence']==['U_D','CODE','D1','D2','D3'],
         'Topic D acquisition order changed.')
    for step in acquisition['stages']:
        key=step['stage']; local={n for n,o in owners.items() if o['document']==key}
        used=union(closure([n for n,b in nodes.items() if b['document']==key and not n.startswith('program.')]))
        need(not (used-paid-local) and step['previous_owner_ids']==sorted(paid) and
             step['complete_local_owner_ids']==step['new_owner_ids']==sorted(local) and
             step['logical_route_owner_ids']==sorted(used) and step['reused_owner_ids']==sorted(used&paid) and
             step['local_text_outside_route']==sorted(local-used) and step['new_cost']==total(local) and
             step['reused_route_cost']==total(used&paid), 'Topic D acquisition omits context or discounts reuse twice.')
        paid|=local
        need(step['cumulative_owner_ids']==sorted(paid) and step['cumulative_cost']==total(paid) and
             step['written_cumulative_cost']==total(n for n in paid if owners[n]['document']!='CODE'),
             'Topic D acquisition does not pay whole manuscripts and programs once.')
    need(view['measurement']==load('audit/topic-d/v2/measurement/packet/results.json') and
         view['bindings']['topic_D_logical_dag_v3/manifest.json']==pins['logical'],
         'Topic D reader uses a different numerical comparison or logical edition.')
    for group in ['raw_program_alternative','raw_operational_drivers']:
        for row in weights[group].values():
            binding=row['binding']; check_bindings([dict(binding,path=binding['public_path'])])
    check_bindings(load(base+'costs/public_links.json')['proof_documents_and_source_locators'])
    dimensions=dict(source_contracts=len(graph['new_application_outputs']),source_rows=len(rows),logical_nodes=len(nodes),
         typed_edges=len(graph['edges']),exclusive_owners=len(owners),document_metric_cells=len(measured)*30,
         owner_metric_cells=len(owners)*30,all_variant_spans=spans,selected_text_spans=selected,
         output_and_context_unions=routes,individual_node_closures=len(nodes),policy_coordinates=30,
         complete_programs=len(weights['raw_program_alternative']),required_programs=len(graph['required_mathematical_programs']),
         diagnostics=len(graph['diagnostic_programs']),separate_operational_drivers=len(graph['operational_drivers']),
         initial_scoped_Lean_declarations=graph['formal_evidence']['initial_report_count'],
         later_scoped_Lean_declarations=graph['formal_evidence']['later_support_report_count'],
         later_Lean_components=graph['formal_evidence']['later_components'])
    primary=view['measurement']['primary']
    need(all(admission[k]==v for k,v in dimensions.items()) and
         admission['independent_logical_review_accepted'] is True and admission['independent_cost_and_reader_review_accepted'] is True and
         admission['primary_written_denominator']==primary['written_denominator'] and
         admission['primary_program_inclusive_denominator']==primary['comparisons']['including_printed_program']['denominator'] and
         admission['primary_raw_program_alternative_denominator']==primary['comparisons']['including_raw_program_alternative']['denominator'] and
         admission['primary_written_fraction']==primary['comparisons']['written_papers']['exact_fraction'] and
         admission['primary_conditionals']==[r['exact_fraction'] for r in primary['per_result']],
         'Topic D graph admission summary contradicts accepted data.')
    fresh=load(base+'root_adoption/fresh_allocation.json'); viewer=load(base+'root_adoption/fresh_viewer.json')
    need(fresh['status']=='PASS_INDEPENDENT_D_ALLOCATION_AND_UNIONS' and fresh['document_cells']==240 and
         fresh['owner_cells']==6600 and fresh['independent_route_unions']==116 and len(fresh['negative_controls'])==6 and
         viewer['status']=='PASS_INDEPENDENT_ACCEPTED_GRAPH_UI_PROJECTION' and viewer['selected_views']==168 and
         len(viewer['regression_controls'])==2, 'Topic D lacks its accepted independent replay evidence.')
    need(all(admission[k] is None for k in ['expanded_external_proof_cost','historical_software_cost','graphic_cost',
         'node_count_ratio','minimum_proof_complexity']) and not admission['complete_costs_changed'] and
         not admission['source_specific_full_formalization'] and not admission['real_browser_layout_test'] and
         admission['new_source_credit']==admission['new_question_credit']==admission['new_formal_credit']==0 and
         partition['node_count_ratio'] is None and weights['compression_ratio'] is None,
         'Topic D graph invents a cost, factor, proof or result credit.')
    return 240,116


def check_topic_f_proofs():
    base = 'papers/topic-f/v2/'
    audit = 'audit/topic-f/v2/'
    admission = load(audit+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_TOPIC_F_COMMON_PROOFS',
         'Unreviewed Topic F mathematical edition.')
    check_bindings(admission['artifacts'])
    for prefix,key,count in [(base,'author_manifest_sha256',49),
            (audit+'independent_review/','independent_review_manifest_sha256',31),
            (audit+'root_adoption/','root_adoption_manifest_sha256',3)]:
        manifest = load(prefix+'manifest.json')
        need(digest((ROOT/prefix/'manifest.json').read_bytes())==admission[key] and
             len(manifest['exports'])==count, 'Changed frozen Topic F packet.')
        for row in manifest['exports']:
            check_bindings([dict(row,path=prefix+row['path'])])
    scope = load(base+'scope.json')
    review = load(audit+'independent_review/review.json')
    adoption = load(audit+'root_adoption/review.json')
    need(review['status']=='ACCEPTED_NO_CORRECTION_REQUESTED' and
         review['author_manifest']['sha256']==admission['author_manifest_sha256'] and
         adoption['status']=='ROOT_ACCEPTED_WITH_EXPLICIT_RETAINED_INPUTS' and
         adoption['author_manifest_sha256']==admission['author_manifest_sha256'] and
         adoption['independent_manifest_sha256']==admission['independent_review_manifest_sha256'] and
         adoption['changes_requested']==[], 'Topic F acceptance refers to another edition.')
    need(scope['source_ids']==admission['source_ids']==review['source_contracts']==['L014'] and
         scope['intake_closed'] and len(scope['contracts'])==admission['source_rows']==25 and
         [r['id'] for r in scope['contracts']]==scope['inherited_row_ids']==admission['source_row_ids'] and
         len(scope['proof_spans'])==admission['proof_spans']==16,
         'Topic F source clauses or proof spans changed.')
    rows = {r['id']:r for r in scope['contracts']}
    reviewed = load(audit+'independent_review/source_rows.json')['rows']
    need([r['id'] for r in reviewed]==scope['inherited_row_ids'] and
         all(r['current_status']==rows[r['id']]['status'] and
             r['current_spans']==rows[r['id']]['current_spans'] for r in reviewed),
         'Topic F reviewed source dispositions changed.')
    for row in scope['contracts']:
        need(row['id']==row['inherited_record']['id'] and row['current_spans'] and
             all(k in scope['proof_spans'] for k in row['current_spans']),
             'Topic F source attribution or current proof reference changed.')
    for row in scope['proof_spans'].values():
        text = (ROOT/base/row['path']).read_text()
        start,end = row['start_codepoint'],row['end_codepoint_exclusive']
        need(0<=start<end<=len(text) and digest(text[start:end].encode())==row['sha256_utf8'],
             'Topic F exact proof passage changed.')
    need(rows['L014.T1.2.defect']['status']=='literal_preprint_marking_corrected' and
         all(rows[n]['status']=='excluded_not_recovered' for n in
             ['excluded.census','excluded.classification']) and
         rows['CP.T1.1']['status']=='retained_or_context',
         'Topic F erased a correction, exclusion or retained theorem.')
    retained = scope['retained_remote_primary']
    need(retained['not_reproved'] is True and
         all(retained[k] is None for k in ['local_pdf','local_pdf_sha256','full_text_cost']) and
         review['retained_external_costs']['CP_full_PDF'] is None and
         review['retained_external_costs']['CP_full_text_cost'] is None,
         'Topic F invented the retained classification proof or its cost.')
    programs = ['phase236_models.py','phase236_finite_check.g','phase248_presentation_check.g']
    drivers = ['phase236_check.py','phase248_check.py']
    need([r['original'] for r in scope['program_inventory']]==programs+drivers and
         admission['complete_programs']==3 and admission['required_mathematical_programs']==0 and
         admission['separate_operational_drivers']==2,
         'Topic F complete program or driver inventory changed.')
    for row in scope['program_inventory']:
        check_bindings([dict(path=base+row['copy'],bytes=row['bytes'],sha256=row['sha256'])])
        need(row['role']==('finite_validation' if row['original'] in programs else 'historical_operational_driver') and
             row['uniform_written_proof_premise'] is False,
             'Topic F finite validation promoted to a uniform proof premise.')
    printed = re.findall(r'\\VerbatimInput\[[^\]]*\]\{programs/([^}]+)\}',
                         (ROOT/base/'program-appendix.tex').read_text())
    need(printed==programs and not scope['validation_boundary']['uniform_written_proof_depends_on_finite_results'] and
         not admission['full_uniform_proofs_depend_on_finite_validation'],
         'Topic F omitted a printed program or changed its mathematical role.')
    fresh = load(audit+'independent_review/fresh_replay/report.json')
    public = load(audit+'publication_replay/render.json')
    for replay in [fresh,public]:
        need(replay['status']=='PASS' and replay['source_rows']==25 and replay['proof_spans']==16 and
             len(replay['integrity_controls'])==8 and all(x['rejected'] for x in replay['integrity_controls']) and
             replay['code_inclusion']['complete_files']==programs and
             [(r['document'],r['pages'],r['per_page_text_identical'],r['diagnostics']) for r in replay['render']]==
             [('umbrella',4,True,[]),('odd-kernel-polyhedra',5,True,[]),('program-appendix',4,True,[])],
             'Topic F complete public render, program inclusion or integrity evidence changed.')
    finite = fresh['finite_validation']
    need(finite['cyclotomic_models']==7 and finite['abelian_models']==4 and
         finite['source_presentations']==[[3,3,27],[3,6,729],[5,3,125],[5,5,3125],[11,3,1331]] and
         finite['subset_intersections_per_model']==64 and finite['semantic_rejections']==4 and
         finite['uniform_proof'] is False,
         'Topic F independent finite validation scope changed.')
    lattice = load(audit+'independent_review/lattice_result.json')
    need(lattice['status']=='PASS' and lattice['count']==len(lattice['models'])==40 and
         all(r['HNF_equal'] and r['conjugation_preserves_ideal'] and r['index']==r['p']**r['n']
             for r in lattice['models']) and lattice['controls'][0]['status']=='REJECTED',
         'Topic F independent lattice evidence changed.')
    formal = load(base+'formal/scope.json')
    compiled = load(audit+'independent_review/fresh_replay/formal/report.json')
    names = [n for m in formal['modules'] for n in m['declarations']]
    reports = [r for m in compiled['modules'] for r in m['axioms']]
    need(len(names)==len(set(names))==len(reports)==5 and [r['name'] for r in reports]==names and
         compiled['status']=='PASS' and all(set(r['axioms']) <= {'propext','Classical.choice','Quot.sound'} for r in reports) and
         len(compiled['countermodels'])==2 and formal['source_specific_claims'] is False and
         len(formal['not_formalized'])==6 and formal['new_declarations']==0 and
         admission['fresh_lean_declarations']==admission['reused_lean_declarations']==5 and
         admission['new_lean_declarations']==0 and admission['end_to_end_source_formalization'] is False,
         'Topic F scoped formal evidence was inflated.')
    need([r['declaration'] for r in scope['formal_statement_map']]==names and
         fresh['formal']['same_five_as_legacy_driver'] and fresh['formal']['not_added_twice'],
         'Topic F formal statement map changed or counts duplicate compilations.')
    catalogue = load('papers/catalogue.json')
    entries = [r for r in catalogue['new_editions'] if r['topic']=='F']
    need(entries==admission['catalogue_entries'] and len(entries)==2 and
         catalogue['current_topic_editions']['F']==[r['id'] for r in entries] and
         [r['source_contracts'] for r in entries]==[[],['L014']] and
         [r['physical_pages'] for r in entries]==[4,5] and admission['scientific_pages']==9 and
         admission['complete_validation_pages']==4, 'Topic F catalogue or page summaries changed.')
    for row in entries:
        inputs = re.findall(r'\\input\{([^}]+)\}',(ROOT/row['tex']).read_text())
        need(row['tex_inputs']==[base+x for x in inputs] and row['review_record']==audit+'admission.json',
             'Topic F catalogue omits a TeX input or proof review.')
    # Reconstruct the completion summary at this admission, using fixed editions.
    # Later topic editions must not change this historical boundary.
    baseline = load('audit/completion.json')['publication_summary']
    canonical = set(baseline['canonical_contract_ids'])
    prefixes = tuple('topic-'+topic+'/v2/' for topic in ['e','a','b','c','d','affine','f'])
    for row in catalogue['new_editions']:
        if row['id'].startswith(prefixes):
            canonical.update(row.get('source_contracts',[]))
    admitted = set(load('audit/intake.json')['admitted_principal_contracts'])
    remaining = admission['remaining_contracts_for_canonical_topic_editions']
    need(baseline['principal_contracts']==len(admitted)==27 and canonical <= admitted and
         len(canonical)==admission['canonical_complete_contract_count_at_this_admission']==23 and
         len(remaining)==len(set(remaining))==4 and
         set(remaining)==admitted-canonical=={'L092','F010','L008','N016'},
         'Topic F completion summary exceeds its fixed canonical edition boundary.')
    need(admission['existing_principal_contracts']==1 and admission['project_total_preserved']==27 and
         scope['cost_boundary']['full_common_paper_charged_once'] and
         not scope['cost_boundary']['cross_topic_discount'] and
         scope['new_source_credit']==scope['new_question_credit']==admission['new_source_credit']==admission['new_question_credit']==0 and
         all(admission[k] is None for k in ['compression_ratio','retained_CP_full_proof_cost','source_graphics_cost']),
         'Topic F invents source credit, a ratio or an external proof cost.')
    return 25,5


def check_topic_g_proofs():
    base, audit = 'papers/topic-g/v2/', 'audit/topic-g/v2/'
    admission = load(audit+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_TOPIC_G_COMMON_PROOFS',
         'Unreviewed Topic G mathematical edition.')
    check_bindings(admission['artifacts'])
    expected = [('current_edition',base,106),('original_author',audit+'original_author/',105),
                ('notation_delta',audit+'notation_delta/',9),
                ('program_formal_review',audit+'program_formal_review/',42),
                ('steiner_review',audit+'steiner_review/',7),
                ('root_adoption',audit+'root_adoption/',9),
                ('assembly_replay',audit+'assembly_replay/',3)]
    need([(r['role'],r['path']+'/',r['exports']) for r in admission['packets']]==expected,
         'Topic G frozen packet inventory changed.')
    pins = {}
    artifact_paths = {base+'PUBLICATION.rst',audit+'publication_replay/catalogue.json',
                      audit+'publication_replay/bindings.json'}
    for row in admission['packets']:
        prefix = row['path']+'/'
        manifest = load(prefix+'manifest.json')
        need(digest((ROOT/prefix/'manifest.json').read_bytes())==row['manifest_sha256'] and
             len(manifest['exports'])==row['exports'], 'Changed Topic G frozen packet.')
        check_bindings([dict(r,path=prefix+r['path']) for r in manifest['exports']])
        pins[row['role']] = row['manifest_sha256']
        artifact_paths.update(prefix+r['path'] for r in manifest['exports'])
        artifact_paths.add(prefix+'manifest.json')
    need(len(admission['artifacts'])==len(artifact_paths)==291 and
         {r['path'] for r in admission['artifacts']}==artifact_paths,
         'Topic G admission omits or duplicates a publication artifact.')
    adoption = load(audit+'root_adoption/review.json')
    steiner = load(audit+'steiner_review/review.json')
    program_review = load(audit+'program_formal_review/review.json')
    need(adoption['status']=='ROOT_ACCEPTED_WITH_EXPLICIT_RETAINED_INPUTS_AND_NOTATION_OVERLAY' and
         all(adoption[k+'_manifest_sha256']==pins[p] for k,p in
             [('author','original_author'),('notation_delta','notation_delta'),
              ('program_formal_review','program_formal_review'),('steiner_review','steiner_review')]) and
         adoption['changes_requested']==[] and
         steiner['status']=='ACCEPTED_WITH_EXPLICIT_SCOPE_AND_ADDITIVE_NOTATION_REPAIR' and
         steiner['author_manifest_sha256']==pins['original_author'] and
         steiner['notation_delta_manifest_sha256']==pins['notation_delta'] and
         program_review['status']=='ACCEPTED_BOUNDED_TOPIC_G_PROGRAM_AND_FORMAL_EVIDENCE' and
         program_review['author_manifest_sha256']==pins['original_author'],
         'Topic G review boundaries or accepted editions changed.')
    original = load(audit+'original_author/manifest.json')
    assembly = load(base+'assembly.json')
    delta = load(audit+'notation_delta/delta.json')
    replacements = ['sections/linear-bases.tex','steiner-geometries.pdf','scope.json']
    need(delta['replacement_files']==admission['accepted_notation_replacement_files']==replacements and
         assembly['original_author_manifest_sha256']==pins['original_author'] and
         assembly['notation_delta_manifest_sha256']==pins['notation_delta'] and
         assembly['root_adoption_manifest_sha256']==pins['root_adoption'] and
         assembly['changed_files']==sorted(replacements), 'Topic G overlay changed its scope.')
    mapping = {r['path']:r for r in assembly['mapping']}
    need(len(mapping)==len(assembly['mapping'])==105, 'Topic G assembly omits an original file.')
    for row in original['exports']:
        name = row['path']
        prefix = audit+('notation_delta/' if name in replacements else 'original_author/')
        current = (ROOT/base/name).read_bytes()
        need(current==(ROOT/prefix/name).read_bytes() and
             mapping[name]['original_sha256']==row['sha256'] and
             mapping[name]['current_sha256']==digest(current) and
             mapping[name]['origin']==('notation_delta' if name in replacements else 'original_author'),
             'Topic G current file differs from its accepted source: '+name)
    old_text = (ROOT/audit/'original_author/sections/linear-bases.tex').read_text()
    need(old_text.count(delta['old_literal'])==1 and
         old_text.replace(delta['old_literal'],delta['new_literal'],1)==
         (ROOT/base/'sections/linear-bases.tex').read_text() and
         delta['new_literal']==r'\(\mathbb F_{16}^{*}/\mathbb F_4^{*}\)',
         'Topic G multiplicative quotient correction changed.')
    scope = load(base+'scope.json')
    prior = load(audit+'original_author/scope.json')
    need(scope['rows']==prior['rows'] and scope['intake_closed'] and
         scope['principal_sources']==admission['source_ids']==['L009','L092'] and
         scope['counts']==dict(L009=44,L092=35,proof_spans=34) and
         len(scope['rows'])==admission['source_rows']==79 and
         admission['source_row_counts']=={'L009':44,'L092':35} and
         [r['id'] for r in scope['rows']]==admission['source_row_ids'] and
         len(scope['proof_spans'])==admission['proof_or_context_spans']==34,
         'Topic G source dispositions or proof contexts changed.')
    for name,row in scope['proof_spans'].items():
        text = (ROOT/base/row['path']).read_text()
        start = text.index(row['start_anchor']) if row['start_anchor'] else 0
        end = text.index(row['end_anchor'],start+len(row['start_anchor'] or '')) if row['end_anchor'] else len(text)
        data = text[start:end].encode()
        need(len(data)==row['bytes'] and digest(data)==row['sha256'], 'Topic G proof passage changed: '+name)
    rows = {r['id']:r for r in scope['rows']}
    triangle = load(audit+'root_adoption/L009_source_review.json')
    need(triangle['rows_checked']==len(triangle['source_rows'])==44 and
         all(all(r[k]==rows[r['id']][k] for k in ['source_locator','claim','status','proof_spans','qualification'])
             for r in triangle['source_rows']), 'Topic G triangle reading differs from source dispositions.')
    notes = load(audit+'steiner_review/proof_reading.json')['rows']
    need(len(notes)==35 and {r['id'] for r in notes}=={r['id'] for r in scope['rows'] if r['source']=='L092'} and
         all(r['author_status']==rows[r['id']]['status'] and r['proof_spans']==rows[r['id']]['new_proof_spans']
             for r in notes), 'Topic G Steiner reading differs from source dispositions.')
    need(rows['L092.Conj1']['status']=='previously admitted solution reused' and
         rows['L009.question.gonality3']['status']=='unresolved-here' and
         rows['L009.question.gonality2']['status']=='separate-question-track' and
         rows['L092.Pasini.names']['status']=='excluded unproved identification' and
         rows['L092.Abstract.generality']['status']=='excluded broader claim' and
         all(rows[n]['status']=='retained external theorem' for n in ['L092.T2','L092.T10']) and
         steiner['coverage']['whole_literal_source_recovered'] is False,
         'Topic G promoted an exclusion, retained proof or earlier question answer.')
    inventory = load(base+'program_inventory.json')
    reviewed_programs = load(audit+'program_formal_review/program_map.json')
    need(inventory['programs']==reviewed_programs['programs'] and
         inventory['operational_files']==reviewed_programs['operational_files'] and
         len(inventory['programs'])==admission['complete_programs']==13 and
         inventory['required_mathematical_programs']==admission['required_mathematical_programs']==4 and
         inventory['required_witness_or_certificate_programs']==admission['witness_or_certificate_programs']==2 and
         inventory['diagnostic_programs']==admission['validation_programs']==7 and
         len(inventory['operational_files'])==admission['separate_operational_files']==3,
         'Topic G whole program roles or operational inventory changed.')
    check_bindings([dict(r,path=base+r['path']) for r in inventory['programs']])
    replay = load(audit+'program_formal_review/replay/report.json')
    evidence = load(audit+'program_formal_review/audit.json')
    need(replay['status']=='PASS' and len(replay['program_replays'])==13 and
         len({r['label'] for r in replay['program_replays']})==13 and
         all(r['status']=='PASS' and r['returncode']==0 for r in replay['program_replays']) and
         len(replay['controls'])==8 and all(r['status']=='REJECTED' for r in replay['controls']) and
         evidence['roles']=={'mathematical':4,'witness_or_certificate':2,'validation':7} and
         evidence['regenerated_finite_Lean_source_equal'] and evidence['pinned_packages']==9 and
         len(evidence['independent_evidence_controls'])==6 and
         all(r['status']=='REJECTED' for r in evidence['independent_evidence_controls']),
         'Topic G independent finite execution or evidence scope changed.')
    formal = load(base+'formal/scope.json')
    declarations = evidence['formal_declarations']
    need(len(formal['modules'])==admission['formal_modules']==6 and
         formal['distinct_reports']==replay['distinct_formal_reports']==admission['reused_lean_declarations']==40 and
         len(declarations)==len({r['name'] for r in declarations})==40 and
         all(set(r['axioms'])<={'propext','Classical.choice','Quot.sound'} for r in declarations) and
         len(formal['unformalized'])==3 and admission['new_lean_declarations']==0 and
         admission['end_to_end_source_formalization'] is False and
         adoption['complete_source_specific_Lean_formalization'] is False,
         'Topic G formalization scope was inflated.')
    check_bindings([dict(r,path=base+r['path']) for r in formal['modules']])
    for module in formal['modules']:
        names = [r['name'].split('.')[-1] for r in declarations if r['module']==module['path']]
        need(names==module['declarations'] and len(names)==module['reports'], 'Topic G actual formal statements changed.')
    render = load(audit+'assembly_replay/render.json')
    need(render['status']=='PASS' and
         [(r['document'],r['pages'],r['same_text_as_bound'],r['diagnostics']) for r in render['documents']]==
         [('umbrella',12,True,[]),('triangle-geometries',8,True,[]),
          ('steiner-geometries',22,True,[]),('programs',20,True,[])] and
         render['complete_code_files']==[r['path'] for r in inventory['programs']] and
         admission['scientific_pages']==42 and admission['common_pages']==12 and
         admission['application_pages']==[8,22] and admission['whole_program_pages']==20,
         'Topic G whole documents or code inclusion changed.')
    public = load(audit+'publication_replay/catalogue.json')
    bindings = load(audit+'publication_replay/bindings.json')
    need(public['status']=='PASS' and
         [(r['document'],r['pages'],r['per_page_text_equal']) for r in public['bound_pdf_comparisons']]==
         [('umbrella',12,True),('triangle-geometries',8,True),('steiner-geometries',22,True)] and
         len(public['build']['papers'])==4 and
         all(r['status']=='compiled' and r['diagnostics']==[] for r in public['build']['papers']) and
         bindings['status']=='PASS' and bindings['source_rows']==79 and bindings['proof_spans']==34 and
         bindings['complete_programs']==13 and bindings['formal_modules']==6,
         'Topic G public build or portable bindings changed.')
    catalogue = load('papers/catalogue.json')
    entries = [r for r in catalogue['new_editions'] if r['topic']=='G']
    need(entries==admission['catalogue_entries'] and len(entries)==3 and
         catalogue['current_topic_editions']['G']==[r['id'] for r in entries] and
         [r['source_contracts'] for r in entries]==[[],['L009'],['L092']] and
         [r['physical_pages'] for r in entries]==[12,8,22], 'Topic G catalogue changed.')
    for row in entries:
        inputs = re.findall(r'\\input\{([^}]+)\}',(ROOT/row['tex']).read_text())
        need(row['tex_inputs']==[base+x for x in inputs] and row['review_record']==audit+'admission.json',
             'Topic G catalogue omits a TeX input or review.')
    canonical = set(load('audit/completion.json')['publication_summary']['canonical_contract_ids'])
    prefixes = tuple('topic-'+t+'/v2/' for t in ['e','a','b','c','d','affine','f','g'])
    for row in catalogue['new_editions']:
        if row['id'].startswith(prefixes):
            canonical.update(row.get('source_contracts',[]))
    admitted = set(load('audit/intake.json')['admitted_principal_contracts'])
    remaining = admission['remaining_contracts_for_canonical_topic_editions']
    need(canonical<=admitted and len(admitted)==admission['project_total_preserved']==27 and
         len(canonical)==admission['canonical_complete_contract_count_at_this_admission']==24 and
         len(remaining)==len(set(remaining))==3 and set(remaining)==admitted-canonical=={'F010','L008','N016'},
         'Topic G completion summary exceeds its fixed edition boundary.')
    need(admission['existing_principal_contracts']==2 and
         admission['source_corrections_and_exclusions_preserved'] is True and
         admission['whole_common_charged_once_within_topic'] and not admission['cross_topic_discount'] and
         all(admission[k]==0 for k in ['new_source_credit','new_principal_credit','new_question_credit']) and
         scope['new_source_credit']==scope['new_question_credit']==0 and
         all(admission[k] is None for k in ['compression_ratio','retained_classification_full_cost','source_graphics_cost']),
         'Topic G invents credit, a ratio or an external cost.')
    return 79,40


def check_topic_f_measurement():
    base = 'audit/topic-f/v2/measurement/'
    admission = load(base+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_TOPIC_F_MEASUREMENT',
         'Topic F numerical comparison lacks acceptance.')
    check_bindings(admission['artifacts'])
    pins = admission['packet_manifests']
    need(set(pins)=={'inputs','input_review','input_adoption','packet','arithmetic_review','root_adoption'},
         'Topic F measurement archive inventory changed.')
    for folder,pin in pins.items():
        need(digest((ROOT/base/folder/'manifest.json').read_bytes())==pin,
             'Changed Topic F measurement archive: '+folder)
        for row in load(base+folder+'/manifest.json')['exports']:
            check_bindings([dict(row,path=base+folder+'/'+row['path'])])
    result = load(base+'packet/measurement.json')
    counts = load(base+'inputs/author_counts.json')
    recount = load(base+'input_review/recount.json')
    need(counts['documents']==recount['documents'] and
         all(counts[k]==recount['raw_files'][k] for k in recount['raw_files']),
         'Topic F inputs disagree with the independent recount.')
    spec = importlib.util.spec_from_file_location('topic_f_independent_arithmetic',
                                                 ROOT/base/'arithmetic_review/arithmetic.py')
    checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
    checked = checker.check(result,counts)
    controls = checker.controls(result,counts)
    need(len(checked)==30 and len(controls)==21 and all(r['rejected'] for r in controls),
         'Topic F arithmetic coordinates or corruption controls changed.')
    input_review = load(base+'input_review/review.json')
    input_adoption = load(base+'input_adoption/review.json')
    review = load(base+'arithmetic_review/review.json')
    adoption = load(base+'root_adoption/review.json')
    need(input_review['status']=='ACCEPTED_INPUT_BOUNDARY_NO_FACTORS' and
         input_review['author_manifest']['sha256']==pins['inputs'] and
         input_review['corrections_requested']==[] and
         input_adoption['status']=='ROOT_ACCEPTED_TOPIC_F_INPUTS_WITH_EXPLICIT_EXTRACTION_BOUNDARY' and
         input_adoption['author_manifest_sha256']==pins['inputs'] and
         input_adoption['independent_manifest_sha256']==pins['input_review'] and
         review['status']=='ACCEPTED_INDEPENDENT_NUMERICAL_AND_READER_REVIEW' and
         review['author_manifest']['sha256']==pins['packet'] and
         review['corrections_requested']==[] and
         adoption['status']=='ROOT_ACCEPTED_TOPIC_F_NUMERICAL_MEASUREMENT' and
         adoption['input_manifests']['numerical']==pins['packet'] and
         adoption['input_manifests']['numerical_review']==pins['arithmetic_review'] and
         adoption['corrections_requested']==[], 'Topic F acceptance refers to other inputs.')
    expected_inputs = {k:pins[k] for k in ['inputs','input_review','input_adoption']}
    need(result['input_manifests']==review['input_manifests']==expected_inputs and
         all(adoption['input_manifests'][k]==v for k,v in expected_inputs.items()),
         'Topic F numerical calculation bypasses accepted input boundaries.')
    fresh = load(base+'root_adoption/fresh_arithmetic.json')
    need(fresh['status']=='PASS_INDEPENDENT_NUMERICAL_REVIEW' and
         fresh['primary']==result['primary']==review['primary']==adoption['primary']==admission['primary'] and
         fresh['coordinate_count']==admission['policy_coordinates']==30 and
         fresh['exact_fractions']==admission['exact_fractions']==120 and
         fresh['combined_fractions']==result['combined_fractions']==admission['combined_fractions']==90 and
         fresh['conditional_fractions']==result['conditional_fractions']==admission['conditional_fractions']==30 and
         len(fresh['controls'])==21 and all(r['rejected'] for r in fresh['controls']),
         'Topic F admission changed independently verified fractions.')
    mapping = load(base+'input_adoption/public_mapping.json')
    immutable = load(base+'inputs/manifest.json')['immutable_inputs']
    need([{k:r[k] for k in ['path','bytes','sha256']} for r in mapping['routes']]==immutable,
         'Topic F public mapping omits a measured input.')
    public = [dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'])
              for r in mapping['routes'] if r['public_path'] is not None]
    check_bindings(public)
    private = [r for r in mapping['routes'] if r['public_path'] is None]
    need(len(public)==15 and len(private)==1 and private[0]['path']=='sources/regular_4pm2025.pdf' and
         mapping['no_primary_export'] is True, 'Topic F source input boundary changed.')
    proof = load('audit/topic-f/v2/admission.json')
    scope = load('papers/topic-f/v2/scope.json')
    boundary = load(base+'inputs/source_contract_boundary.json')
    need(digest((ROOT/'audit/topic-f/v2/admission.json').read_bytes())==admission['proof_admission_sha256'] and
         admission['source_ids']==proof['source_ids']==result['source_ids']==['L014'] and
         admission['source_records']==proof['source_rows']==boundary['row_count']==25 and
         boundary['source_rows']==scope['contracts'] and boundary['proof_spans']==scope['proof_spans'] and
         admission['principal_contracts']==boundary['principal_contracts']==1 and
         admission['project_total_preserved']==27, 'Topic F measurement changed scientific coverage.')
    need(admission['pdf_metric_cells']==recount['pdf_metric_cells']==120 and
         admission['raw_metric_cells']==sum(recount[k] for k in
             ['raw_program_metric_cells','raw_driver_metric_cells','raw_formal_metric_cells'])==60 and
         admission['required_uniform_proof_programs']==0 and admission['complete_validation_programs']==3 and
         admission['separate_drivers']==2 and admission['separate_formal_files']==1 and
         admission['scoped_Lean_declarations']==5 and
         admission['unknown_external_costs']==dict.fromkeys(['retained_CP_fulltext','retained_external',
             'graphics_layout','historical_software']) and
         admission['paired_dependency_audit_complete'] is False and
         admission['source_specific_formalization'] is False and
         admission['new_source_credit']==admission['new_question_credit']==admission['new_formal_credit']==0,
         'Topic F numerical summary invents a cost, proof or credit.')
    return 120,120


def check_representation_proofs():
    base = 'papers/topic-representation/v2/'
    audit = 'audit/topic-representation/v2/'
    admission = load(audit+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_REPRESENTATION_COMMON_PROOFS',
         'Unreviewed representation edition.')
    check_bindings(admission['artifacts'])
    packets = [(base,'author',46), (audit+'independent_review/','independent',25),
               (audit+'review_role_delta/','role_correction',2), (audit+'root_adoption/','root',5)]
    for prefix,key,count in packets:
        manifest = load(prefix+'manifest.json')
        need(digest((ROOT/prefix/'manifest.json').read_bytes())==admission['manifests'][key] and
             len(manifest['exports'])==count, 'Changed frozen representation packet.')
        check_bindings([dict(r,path=prefix+r['path']) for r in manifest['exports']])
    scope = load(base+'scope.json')
    original = load(audit+'independent_review/review.json')
    corrected = load(audit+'review_role_delta/review.json')
    delta = load(audit+'review_role_delta/correction.json')
    adoption = load(audit+'root_adoption/review.json')
    expected = json.loads(json.dumps(original))
    expected['review_roles']['current_edition_author'] = 'enumeration_volume'
    need(corrected==expected and original['review_roles']['current_edition_author']=='rewrite_termination' and
         delta['json_pointer']=='/review_roles/current_edition_author' and
         delta['old']=='rewrite_termination' and delta['new']=='enumeration_volume' and
         delta['only_field_change'] and not delta['mathematics_scope_bindings_or_verdict_changed'] and
         delta['old_review_sha256']==digest((ROOT/audit/'independent_review/review.json').read_bytes()) and
         delta['corrected_review_sha256']==adoption['corrected_independent_review_sha256']==
             digest((ROOT/audit/'review_role_delta/review.json').read_bytes()),
         'Representation review role correction is not the exact declared single-field change.')
    need(corrected['status']=='ACCEPTED_COMPLETE_WRITTEN_CONTRACT_WITH_SCOPED_FORMAL_EVIDENCE' and
         corrected['author_manifest_sha256']==admission['manifests']['author'] and
         adoption['status']=='ROOT_ACCEPTED_COMPLETE_REPRESENTATION_EDITION_WITH_EXPLICIT_FORMAL_SCOPE' and
         adoption['manifests']=={k:admission['manifests'][k] for k in ['author','independent','role_correction']} and
         corrected['requested_author_corrections']==adoption['root_mathematical_corrections_requested']==[],
         'Representation scientific acceptance refers to a different edition.')
    need(scope['source_ids']==admission['source_ids']==adoption['source_ids']==['F010'] and scope['intake_closed'] and
         scope['source']['authors']==corrected['source_authors']==adoption['source_authors']==
             ['Antonio Díaz Ramos','Rémi Molinier','Antonio Viruel'] and
         scope['source']['edition']==corrected['source_edition']==adoption['source_edition']=='arXiv:2511.02410v2, 2025-12-16' and
         scope['source']['primary']['sha256']==corrected['source_sha256']==
             'a8ff604a96a57ab8baf20aaa808a90308c01237ab0607a1062207fcb49f736e7',
         'Representation source edition or attribution changed.')
    baseline = load(base+'baseline_contract.json')
    need([r['inherited_record'] for r in scope['contracts']]==baseline['principal_blocks'] and
         [r['id'] for r in scope['contracts']]==admission['source_row_ids'] and
         len(scope['contracts'])==admission['source_rows']==6 and
         len(scope['proof_spans'])==admission['proof_spans']==13,
         'Representation source blocks or proof contexts changed.')
    for row in scope['contracts']:
        need(row['current_spans'] and all(k in scope['proof_spans'] for k in row['current_spans']),
             'Representation source result lacks its proof contexts.')
    for row in scope['proof_spans'].values():
        text = (ROOT/base/row['path']).read_text()
        start,end = row['start_codepoint'],row['end_codepoint_exclusive']
        need(0<=start<end<=len(text) and digest(text[start:end].encode())==row['sha256_utf8'],
             'Representation proof passage changed.')
    rows = {r['id']:r for r in scope['contracts']}
    need(rows['F010.Example5.1']['status']=='corrected_example' and
         rows['F010.Example5.2']['status']=='qualified_base_case' and
         scope['source_qualifications']==corrected['qualifications']==adoption['source_qualifications'] and
         len(scope['source_qualifications'])==3 and
         scope['exclusions']==corrected['preserved_exclusions']==adoption['exclusions'] and len(scope['exclusions'])==5,
         'Representation qualifications or exclusions changed.')
    hyp = scope['precise_hypotheses']
    need(hyp['finite'] and hyp['normal_subgroup_required'] and hyp['main_nontrivial_rank']=='[G:H]+3' and
         hyp['trivial_rank']==1 and hyp['connected_main_construction'] and
         hyp['arbitrary_input_cleaning_need_not_be_connected'] and not hyp['rank_two_universal_claim'],
         'Representation construction hypotheses or component limits changed.')
    programs = ['phase177_hexagon_check.g','phase188_gadget_check.g']
    drivers = ['phase188_verify.py','phase193_public_check.py']
    need([r['original'] for r in scope['program_inventory']]==programs+drivers and
         admission['complete_programs']==2 and admission['required_mathematical_programs']==0 and
         admission['separate_operational_drivers']==2, 'Representation whole program inventory changed.')
    for row in scope['program_inventory']:
        check_bindings([dict(path=base+row['copy'],bytes=row['bytes'],sha256=row['sha256'])])
        need(row['role']==('bounded_validation' if row['original'] in programs else 'historical_operational_driver') and
             row['universal_proof_premise'] is False, 'Representation bounded validation promoted to a proof premise.')
    printed = re.findall(r'\\VerbatimInput\[[^\]]*\]\{programs/([^}]+)\}',(ROOT/base/'program-appendix.tex').read_text())
    need(printed==programs and not scope['validation_boundary']['uniform_written_proof_depends_on_finite_results'],
         'Representation whole-program appendix or proof role changed.')
    fresh = load(audit+'independent_review/fresh_replay/report.json')
    public = load(audit+'publication_replay/render.json')
    for replay in [fresh,public]:
        need(replay['status']=='PASS' and replay['source_blocks']==6 and replay['proof_spans']==13 and
             len(replay['controls'])==11 and all(r['rejected'] for r in replay['controls']) and
             replay['code_inclusion']['files']==programs and
             [(r['document'],r['pages'],r['per_page_text_identical'],r['diagnostics']) for r in replay['render']]==
             [('umbrella',5,True,[]),('finite-normal-pairs',5,True,[]),('program-appendix',4,True,[])],
             'Representation replay, complete code or render evidence changed.')
    finite = fresh['bounded_validation']
    local = load(audit+'independent_review/local_cases.json')
    need([r['file'] for r in finite['runs']]==programs and all(r['pass_result'] for r in finite['runs']) and
         len(finite['controls'])==3 and all(r['rejected'] for r in finite['controls']) and
         (finite['small_colored_graphs'],finite['normal_pairs'],finite['completed_pairs'])==(25,7,4) and
         finite['family_n']==[2,3,4,5] and finite['universal_proof'] is False and
         local['status']=='PASS' and local['uniform_proof'] is False and
         local['models']['all_tips']['kernel_order']==6 and local['models']['recursive_n2']['degrees']==[1,2,2,1],
         'Representation finite evidence or correction changed.')
    formal = load(base+'formal/scope.json')
    compiled = load(audit+'independent_review/fresh_replay/formal/report.json')
    names = [n for m in formal['modules'] for n in m['declarations']]
    reports = [r for m in compiled['modules'] for r in m['axioms']]
    need(compiled['status']=='PASS' and len(names)==len(set(names))==len(reports)==12 and
         [r['name'] for r in reports]==names and [m['source'] for m in compiled['modules']]==formal['modules'] and
         all(set(r['axioms'])<={'propext','Classical.choice','Quot.sound'} for r in reports) and
         len(compiled['countermodels'])==4 and formal['not_formalized']==adoption['formal_scope']['unformalized'] and
         len(formal['not_formalized'])==6 and formal['source_specific_claims'] is False and
         formal['new_declarations']==admission['new_lean_declarations']==8 and
         formal['reused_declarations']==admission['reused_lean_declarations']==4 and
         admission['end_to_end_source_formalization'] is False and
         [r['declaration'] for r in scope['formal_statement_map']]==names,
         'Representation partial formal scope or compiled evidence changed.')
    catalogue = load('papers/catalogue.json')
    entries = [r for r in catalogue['new_editions'] if r['topic']=='Representation']
    need(entries==admission['catalogue_entries'] and len(entries)==2 and
         catalogue['current_topic_editions']['Representation']==[r['id'] for r in entries] and
         [r['source_contracts'] for r in entries]==[[],['F010']] and
         [r['physical_pages'] for r in entries]==[5,5] and admission['scientific_pages']==10 and
         admission['complete_validation_pages']==4, 'Representation catalogue or page counts changed.')
    for row in entries:
        inputs = re.findall(r'\\input\{([^}]+)\}',(ROOT/row['tex']).read_text())
        need(row['tex_inputs']==[base+x for x in inputs] and row['review_record']==audit+'admission.json',
             'Representation catalogue omits an input or review.')
    build = load(audit+'publication_replay/catalogue.json')['papers']
    need(len(build)==3 and all(r['status']=='compiled' and r['diagnostics']==[] for r in build) and
         all(r['per_page_text_identical'] and r['physical_pages']==5 for r in build[:2]),
         'Representation public catalogue build failed.')
    canonical = set(load('audit/completion.json')['publication_summary']['canonical_contract_ids'])
    prefixes = tuple('topic-'+t+'/v2/' for t in ['e','a','b','c','d','affine','f','g','representation'])
    for row in catalogue['new_editions']:
        if row['id'].startswith(prefixes):canonical.update(row.get('source_contracts',[]))
    admitted = set(load('audit/intake.json')['admitted_principal_contracts'])
    need(canonical<=admitted and len(admitted)==admission['project_total_preserved']==27 and
         len(canonical)==admission['canonical_complete_contract_count_at_this_admission']==25 and
         set(admission['remaining_contracts_for_canonical_topic_editions'])==admitted-canonical=={'L008','N016'},
         'Representation completion summary exceeds the fixed edition boundary.')
    costs = scope['cost_boundary']
    need(costs['full_common_paper_charged_once'] and costs['full_application_charged'] and not costs['cross_topic_discount'] and
         not costs['prior_own_proof_bank_as_unpriced_logical_premise'] and
         all(costs[k] is None for k in ['ratio','external_proof_cost','source_graphics_cost']) and
         all(admission[k] is None for k in ['compression_ratio','external_proof_cost','source_graphics_cost']) and
         all(admission[k]==scope[k]==corrected[k]==adoption[k]==0 for k in ['new_source_credit','new_question_credit']),
         'Representation invents source/question credit or a compression ratio.')
    return 6,12


def check_affine_dag():
    base = 'audit/topic-affine/v2/dag/'
    admission = load(base+'admission.json')
    need(admission['status']=='PASS_ROOT_REVIEWED_AFFINE_PAIRED_DAG', 'Affine graph lacks acceptance.')
    check_bindings(admission['artifacts'])
    pins = admission['packet_manifests']
    need(set(pins)=={'logical_previous','logical','logical_review','logical_root_adoption',
                     'costs_previous','costs','independent_cost_review'}, 'Affine graph packet inventory.')
    need(pins['logical']=='f46a2579e8ea3035710b92285ddd134fdc1384177cecc976f100a681519b6382' and
         pins['costs']=='7a1cd77556e3addc9a9453f010d9ddfa1b94f816d0a648060d00e0874a363216' and
         pins['independent_cost_review']=='ef627885e37ee4197c1820245f5b413ccfe089f9c9e3b9cd65d8e65d65785b77',
         'Affine accepted graph/cost/review editions changed.')
    exports=0
    for folder,pin in pins.items():
        need(digest((ROOT/base/folder/'manifest.json').read_bytes())==pin, 'Affine frozen manifest '+folder)
        for row in load(base+folder+'/manifest.json')['exports']:
            check_bindings([dict(row,path=base+folder+'/'+row['path'])]);exports+=1
    need(exports==admission['preserved_frozen_exports']==110,'Affine frozen export inventory.')
    for key,path in [('proof','audit/topic-affine/v2/admission.json'),
                     ('measurement','audit/topic-affine/v2/measurement/admission.json')]:
        need(digest((ROOT/path).read_bytes())==admission[key+'_admission_sha256'], 'Affine input edition '+key)
    logical_adoption=load(base+'logical_root_adoption/review.json')
    reviewed=load(base+'independent_cost_review/review.json')
    need(logical_adoption['status']=='ROOT_ACCEPTED_AFFINE_LOGICAL_V2_WITH_EXPLICIT_REUSE' and
         logical_adoption['input_manifests']['author']==pins['logical'] and
         logical_adoption['requested_corrections']==[] and
         reviewed['status']=='ACCEPTED_INDEPENDENT_AFFINE_PASSAGE_COST_REVIEW' and
         reviewed['accepted_author_manifest']==pins['costs'] and reviewed['remaining_corrections']==[],
         'Affine review targets or unresolved corrections.')
    graph=load(base+'logical/logical_graph.json'); coverage=load(base+'logical/coverage.json')
    spec=importlib.util.spec_from_file_location('affine_logical_public_review', ROOT/base/'logical_review/check_independent.py')
    logical=importlib.util.module_from_spec(spec);spec.loader.exec_module(logical)
    logical_result=logical.inspect(graph,coverage,load('papers/topic-affine/v2/scope.json'))
    mapping=load(base+'publication_mapping.json')
    need(mapping['public_input_count']==len(mapping['graph_inputs'])==44 and
         mapping['separate_primary_input_count']==len(mapping['separate_primary_inputs'])==6,
         'Affine primary/public input boundary.')
    bound={(r['namespace'],r['path']):r for r in graph['immutable_inputs']}
    for r in mapping['graph_inputs']:
        need({k:v for k,v in r.items() if k!='public_path'}==bound[r['namespace'],r['path']], 'Affine public input identity.')
        check_bindings([dict(r,path=r['public_path'])])
    for r in mapping['separate_primary_inputs']:
        need({k:v for k,v in r.items() if k!='availability'}==bound[r['namespace'],r['path']] and
             r['namespace']=='research' and r['path'].startswith('sources/'), 'Affine separate primary input.')
    need({(r['namespace'],r['path']) for r in mapping['graph_inputs']+mapping['separate_primary_inputs']}==set(bound),
         'Affine graph input omitted.')
    locators=set()
    for loc in ([s for n in graph['nodes'] for s in n['locators']]+
                [s for e in graph['edges'] for s in e['target_evidence']]+list(graph['accepted_scope_spans'].values())):
        if loc['namespace']!='public':continue
        text=(ROOT/loc['path']).read_text();start,stop=loc['start_codepoint'],loc['end_codepoint_exclusive']
        need(0<=start<stop<=len(text) and digest(text[start:stop].encode())==loc['sha256_utf8'] and
             text.count('\n',0,start)+1==loc['first_line'] and text.count('\n',0,stop-1)+1==loc['last_line'],
             'Affine public proof locator changed.')
        locators.add((loc['path'],start,stop))
    partition=load(base+'costs/partition.json'); weights=load(base+'costs/weights.json')
    measured=load('audit/topic-affine/v2/measurement/packet/independent/recount.json')['documents']
    owners=partition['owners'];costs=weights['owner_costs']
    variants=['raw_untrimmed','raw_selected','calibrated_selected'];forms=['NFC','NFKC']
    units=['whitespace_tokens','alphanumeric_units','characters_without_whitespace',
           'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
    need(set(costs)==set(owners) and len(owners)==194 and set(partition['documents'])==set(measured),
         'Affine complete ownership inventory changed.')
    def total(names):
        names=set(names)
        return {v:{f:{u:sum(costs[n][v][f][u] for n in names) for u in units} for f in forms} for v in variants}
    spans=selected=0
    for name,doc in partition['documents'].items():
        local={n for n,o in owners.items() if o['document']==name}
        need(doc['pdf_sha256']==measured[name]['pdf_sha256'] and doc['pages']==measured[name]['pages'], 'Affine measured document changed.')
        need(set(doc['variants'])==set(variants), 'Affine extraction policy omitted.')
        for variant,data in doc['variants'].items():
            end=0
            for span in data['spans']:
                need(span['start']==end and span['end']>end and span['owner'] in local and
                     span['category']==owners[span['owner']]['category'], 'Affine passage gap or overlap.')
                end=span['end'];spans+=1;selected+=variant=='calibrated_selected'
            need(end==data['length'], 'Affine trailing text omitted.')
        expected={v:{f:{u:measured[name]['variants'][v][f][u] for u in units} for f in forms} for v in variants}
        need(total(local)==weights['document_costs'][name]==expected,'Affine full document not conserved.')
    nodes={n['id']:n for n in graph['nodes']};interfaces=weights['node_interfaces']
    need(set(nodes)==set(interfaces),'Affine interface inventory.')
    for name,entry in interfaces.items():
        paid=entry['owners'];unknown=nodes[name]['side'] in ['external','verification']
        need(paid==sorted(set(paid)) and set(paid)<=set(owners) and
             entry['known_weight']==(None if unknown else total(paid)) and (not unknown or not paid) and
             entry['expanded_dependency_cost'] is None and not entry['charged_again'], 'Affine interface cost or unknown boundary.')
    route_count=0
    def route(names,record):
        nonlocal route_count
        names=set(names);paid={o for n in names for o in interfaces[n]['owners']}
        expected=total(n for n in paid if owners[n]['document']!='CODE')
        program_ids=names & weights['raw_program_alternative'].keys()
        for v in variants:
            for f in forms:
                for u in units:
                    expected[v][f][u]+=sum(weights['raw_program_alternative'][n]['metrics'][f][u] for n in program_ids)
        docs={owners[n]['document'] for n in paid}
        need(record['logical_nodes']==sorted(names) and record['owners']==sorted(paid) and
             record['known_extracted_subtotal']==total(paid) and
             record['by_document']=={d:total(n for n in paid if owners[n]['document']==d) for d in sorted(docs)} and
             record['raw_program_alternative_subtotal']==expected and
             record['unknown_inputs']==sorted(n for n in names if interfaces[n]['known_weight'] is None) and
             record['expanded_dependency_cost'] is None and record['graphics_cost'] is None,
             'Affine dependency union, raw alternative or unknown cost changed.')
        route_count+=1
    for name,closure in logical_result['individual_closures'].items():route(closure,weights['individual_node_closures'][name])
    rows={r['id']:r for r in weights['source_contract_closures']}
    need(set(rows)=={r['id'] for r in coverage['rows']} and len(rows)==33,'Affine source rows changed.')
    for row in coverage['rows']:
        r=rows[row['id']]
        route(row['historical_closure'],r['historical']);route(row['new_closure'],r['replacement'])
        route(set(row['retained_context_closure'])|set(row['qualification_context_nodes']),r['retained_and_qualification_context'])
    for name,closure in graph['new_output_closures'].items():route(closure,weights['new_application_closures'][name])
    route(graph['full_record_closure'],weights['full_record_closure'])
    for name,closure in graph['additional_current_outputs'].items():route(closure,weights['additional_current_outputs'][name])
    import unicodedata
    replacement=load('audit/topic-affine/v2/measurement/packet/inputs/replacement_input_spec.json')
    for key,source_key,count in [('raw_program_alternative','complete_mathematical_programs',6),
                                 ('raw_auxiliary_files','complete_auxiliary_scripts',3),
                                 ('raw_formal_files','complete_formal_files',3)]:
        records=weights[key];accepted={r['path']:r for r in replacement[source_key]}
        need(len(records)==count and {r['binding']['path'] for r in records.values()}==set(accepted),'Affine whole raw files omitted.')
        for r in records.values():
            binding=r['binding'];need(binding==accepted[binding['path']],'Affine whole-file binding or role changed.')
            folder,rest=binding['path'].split('/',1);path=mapping['private_prefixes'][folder]+'/'+rest
            check_bindings([dict(binding,path=path)]);text=(ROOT/path).read_text()
            for form in forms:
                s=unicodedata.normalize(form,text);collapsed=' '.join(s.split())
                values=[len(s.split()),len(re.findall(r'[^\W_]+',s)),sum(not c.isspace() for c in s),len(collapsed),len(collapsed.encode())]
                need(r['metrics'][form]==dict(zip(units,values)),'Affine independent complete raw-file metrics.')
    acquisition=load(base+'costs/acquisition.json');paid=set()
    need([r['stage'] for r in acquisition['stages']]==['U_Affine','CODE','AF1'],'Affine acquisition order.')
    for stage in acquisition['stages']:
        local={n for n,o in owners.items() if o['document']==stage['stage']}
        need(not paid&local and stage['complete_owner_ids']==sorted(local) and stage['new_cost']==total(local),
             'Affine full common, program or application charge omitted.')
        paid|=local
        need(stage['cumulative_owner_ids']==sorted(paid) and stage['cumulative_cost']==total(paid),'Affine cumulative cost.')
    need(acquisition['historical_full_document_cost']==total(n for n,o in owners.items() if o['document']=='L012') and
         not acquisition['cross_topic_discount'] and acquisition['expanded_external_proof_cost'] is None and
         acquisition['graphics_cost'] is None,'Affine acquisition boundary.')
    spec=importlib.util.spec_from_file_location('affine_public_diagram_review',ROOT/base/'independent_cost_review/reader_check.py')
    diagrams=importlib.util.module_from_spec(spec);spec.loader.exec_module(diagrams)
    diagrams.check_interfaces(weights,load(base+'independent_cost_review/semantic_reading.json')['owner_interface_snapshot'])
    diagrams.check_graphs(graph,weights,load(base+'costs/graphs.json'),
                          {side:(ROOT/base/'costs'/(side+'_graph.svg')).read_text() for side in ['historical','new']})
    need(weights['unchanged_complete_document_measurement']==load('audit/topic-affine/v2/measurement/packet/results.json') and
         admission['primary']==load('audit/topic-affine/v2/measurement/admission.json')['primary'], 'Affine full ratios changed.')
    dims=dict(source_contracts=1,source_rows=33,logical_nodes=len(nodes),typed_edges=len(graph['edges']),
              exclusive_owners=len(owners),document_metric_cells=len(measured)*30,owner_metric_cells=len(costs)*30,
              all_variant_spans=spans,selected_text_spans=selected,individual_node_closures=len(nodes),
              source_row_unions=len(rows)*3,all_prerequisite_unions=route_count,policy_coordinates=30,
              required_programs=6,separate_operational_drivers=2,separate_diagnostic_programs=1,
              separate_Lean_files=3,scoped_Lean_declarations=9)
    need(all(admission[k]==v for k,v in dims.items()) and (spans,selected,route_count)==(642,190,222),
         'Affine graph admission contradicts complete data.')
    fresh=load(base+'publication_replay/report.json')
    need(fresh['status']=='PASS_INDEPENDENT_AFFINE_COST_REVIEW_REPLAY' and
         (fresh['owner_metric_cells'],fresh['routes'],fresh['arithmetic_controls'],fresh['reader_controls'])==(5820,222,17,11),
         'Affine fresh independent evidence missing.')
    need(all(admission[k] is None for k in ['expanded_external_proof_cost','historical_software_cost','graphic_cost',
              'node_count_ratio','minimum_proof_complexity']) and not admission['complete_costs_changed'] and
         not admission['source_specific_full_formalization'] and not admission['real_browser_layout_test'] and
         all(admission[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),
         'Affine graph invents costs or credit.')
    return len(measured)*30,route_count


def check_chamber_proofs():
    import sys
    base = 'papers/topic-chamber/v2/'
    audit = 'audit/topic-chamber/v2/'
    admission = load(audit+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_CHAMBER_COMMON_PROOFS',
         'Unreviewed chamber edition.')
    check_bindings(admission['artifacts'])
    for prefix,key,count,pin in [
        (base,'author',68,'087fc503dd4d3f11df74cf751f251c3b585dd9f1ec9aefbb94a8dc3af4124e63'),
        (audit+'independent_review/','independent',24,'cacdc46a81c130da2b76adc09a55548afc0a9998ee558a7b27a00a97844dadbe'),
        (audit+'root_adoption/','root',4,'406ffbeefee18c723568f779cc66db656d02e3e6a1a776ab19cdf3c73e544c9d')]:
        manifest = load(prefix+'manifest.json')
        need(digest((ROOT/prefix/'manifest.json').read_bytes())==admission['manifests'][key]==pin and
             len(manifest['exports'])==count, 'Changed frozen chamber packet.')
        check_bindings([dict(r,path=prefix+r['path']) for r in manifest['exports']])
    scope = load(base+'scope.json'); formal = load(base+'formal/scope.json')
    inventory = load(base+'program_inventory.json'); questions = load(base+'question_map.json')
    reviewed = load(audit+'independent_review/review.json')
    adopted = load(audit+'root_adoption/review.json')
    fresh = load(audit+'independent_review/fresh_replay/report.json')
    # Reuse the accepted scientific scope checker without its private-source entrypoint.
    saved_path = sys.path[:]
    saved_local_cases = sys.modules.pop('local_cases',None)
    try:
        sys.path.insert(0,str(ROOT/audit/'independent_review'))
        spec = importlib.util.spec_from_file_location('chamber_scientific_scope',ROOT/audit/'independent_review/check.py')
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        mod.semantic(scope,formal,inventory,questions,fresh)
        need(mod.local_cases()==load(audit+'independent_review/local_cases.json'),
             'Chamber independent finite interface models changed.')
    finally:
        sys.path[:] = saved_path
        sys.modules.pop('local_cases',None)
        if saved_local_cases is not None:sys.modules['local_cases'] = saved_local_cases
    need(reviewed['status']=='ACCEPTED_WITH_DECLARED_RETAINED_INPUTS_AND_PARTIAL_FORMAL_SCOPE' and
         adopted['status']=='ROOT_ACCEPTED_CHAMBER_EDITION_WITH_EXPLICIT_RETAINED_INPUTS' and
         reviewed['author_manifest_sha256']==admission['manifests']['author'] and
         adopted['input_manifests']=={k:admission['manifests'][k] for k in ['author','independent']} and
         reviewed['corrections_requested']==adopted['corrections_requested']==[] and
         reviewed['review_roles']['current_edition_author']=='rewrite_termination' and
         reviewed['review_roles']['independent_reviewer']=='enumeration_review',
         'Chamber scientific acceptance or reviewer roles changed.')
    need([r['id'] for r in scope['rows']]==admission['source_row_ids'] and
         len(scope['rows'])==admission['source_rows']==27 and len(scope['proof_spans'])==22 and
         admission['source_ids']==adopted['source_ids']==['L008','N016'] and
         scope['principal_count_unchanged']==admission['existing_principal_contracts']==2 and
         not scope['whole_manuscript_all_assertions_claim'], 'Chamber source boundary changed.')
    coverage = load(audit+'independent_review/coverage_review.json')
    need([{k:v for k,v in r.items() if k not in ['review_status','independent_note']} for r in coverage['rows']]==scope['rows'],
         'Chamber review lost a source row or exclusion.')
    proof = load(audit+'independent_review/proof_reading.json')
    need(set(proof['spans'])==set(scope['proof_spans']), 'Chamber proof review incomplete.')
    for key,row in scope['proof_spans'].items():
        text = (ROOT/base/row['path']).read_text()
        start = text.index(row['start_anchor'])
        end = text.index(row['end_anchor'],start+len(row['start_anchor'])) if row['end_anchor'] else len(text)
        data = text[start:end].encode()
        need(len(data)==row['bytes'] and digest(data)==row['sha256'] and proof['spans'][key]['binding']==row,
             'Chamber written proof passage changed.')
    for row in inventory['programs']+formal['modules']:
        check_bindings([dict(row,path=base+row['path'])])
    printed = re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}',(ROOT/base/'programs.tex').read_text())
    need(printed==['programs/chiral_cover.g','programs/reflection_models.py'] and
         [r['path'] for r in inventory['programs'] if r['printed']]==printed and
         digest((ROOT/base/'programs/chiral_cover.g').read_bytes())==
             '59bf1cd96626df42e1e1baed82b88538416f336443c1a4076dfbb5f09bdcc69e' and
         (admission['required_mathematical_programs'],admission['diagnostic_programs'],
          admission['historical_drivers'],admission['current_drivers'])==(1,1,2,1),
         'Chamber complete program roles changed.')
    for row in fresh['programs']+fresh['controls']+fresh['formal']:
        need(digest((ROOT/audit/'independent_review/fresh_replay'/(row['label']+'.log')).read_bytes())==row['log_sha256'],
             'Chamber computational or formal log changed.')
    finite = re.sub(r'\s+','',(ROOT/audit/'independent_review/fresh_replay/finite_cover.log').read_text())
    expected = {'P':'[324,[6,9,6],[54,54],9,false]','T':'[324,[6,9,2],[162,18],9,true]',
                'Td':'[324,[2,9,6],[18,162],9,true]','R':'[972,[6,9,6],[162,162],27,true]',
                'Q':'[2916,[6,9,6],[162,162],9,true]','Qd':'[2916,[6,9,6],[162,162],9,true]'}
    need(all('ROW'+k+v in finite for k,v in expected.items()) and
         'DISTINGUISH(b*c^-1)^2*a*c^2*a^-1ORDERS[1,3]' in finite,
         'Chamber six-group evidence or distinguishing word changed.')
    for row in formal['modules']:
        name = Path(row['path']).stem
        log = (ROOT/audit/'independent_review/fresh_replay'/(name+'.log')).read_text()
        axioms = re.findall(r'depends on axioms:\s*\[([^]]*)\]',log)
        need(len(axioms)==row['reports'] and all(set(x.strip() for x in s.split(',') if x.strip())<=
             {'propext','Classical.choice','Quot.sound'} for s in axioms) and
             'warning:' not in log and 'sorryAx' not in log, 'Chamber scoped Lean evidence changed.')
    need((admission['fresh_lean_declarations'],admission['new_lean_declarations'],admission['reused_lean_declarations'])==(14,7,7) and
         not admission['end_to_end_source_formalization'] and not formal['end_to_end_application_formalized'],
         'Chamber formal scope overstated.')
    for q in questions['questions']:
        for key in ['accepted_record','review']:
            if q.get(key):check_bindings([q[key]])
    check_bindings(questions['separate_prior_baselines'])
    need(reviewed['allrank_finite_multiplicity_remains_unresolved'] and
         admission['allrank_finite_multiplicity_remains_unresolved'] and
         all(q['proof_premise_here'] is False for q in questions['questions']),
         'Chamber separate question used as a premise or open finite question closed.')
    catalogue = load('papers/catalogue.json')
    entries = [r for r in catalogue['new_editions'] if r['topic']=='Chamber']
    need(entries==admission['catalogue_entries'] and len(entries)==3 and
         catalogue['current_topic_editions']['Chamber']==[r['id'] for r in entries] and
         [r['source_contracts'] for r in entries]==[[],['L008'],['N016']] and
         [r['physical_pages'] for r in entries]==[6,3,6] and
         admission['scientific_pages']==15 and admission['program_appendix_pages']==3,
         'Chamber catalogue or scientific page counts changed.')
    for row in entries:
        inputs = re.findall(r'\\input\{([^}]+)\}',(ROOT/row['tex']).read_text())
        need(row['tex_inputs']==[base+x for x in inputs] and row['review_record']==audit+'admission.json',
             'Chamber catalogue lost an input or review.')
    rebuilt = load(audit+'publication_replay/catalogue.json')['papers']
    need(len(rebuilt)==4 and all(r['status']=='compiled' and r['diagnostics']==[] for r in rebuilt) and
         [(r['physical_pages'],r['per_page_text_identical']) for r in rebuilt[:3]]==[(6,True),(3,True),(6,True)],
         'Chamber public catalogue rebuild failed.')
    appendix = load(audit+'publication_replay/appendix.json')
    need(appendix['pages']==3 and appendix['per_page_text_identical'] and appendix['complete_programs']==printed and
         appendix['diagnostics']==[], 'Chamber appendix public rebuild failed.')
    canonical = set(load('audit/completion.json')['publication_summary']['canonical_contract_ids'])
    for row in catalogue['new_editions']:
        if row['id'].startswith('topic-') and '/v2/' in row['id']:canonical.update(row.get('source_contracts',[]))
    admitted = set(load('audit/intake.json')['admitted_principal_contracts'])
    need(canonical==admitted and len(canonical)==admission['canonical_complete_contract_count_at_this_admission']==
         admission['project_total_preserved']==27 and admission['remaining_contracts_for_canonical_topic_editions']==[],
         'Chamber completion count exceeds admitted contracts.')
    need(all(admission[k] is None for k in ['compression_ratio','full_retained_proof_cost','historical_program_cost','source_graphics_cost']) and
         scope['retained_input_full_expansion_cost'] is None and scope['compression_factor'] is None and
         all(admission[k]==reviewed[k]==adopted[k]==0 for k in ['new_source_credit','new_question_credit']) and
         adopted['whole_common_cost_required'] and not adopted['cross_topic_discount'],
         'Chamber invents costs, new credits or a cross-topic discount.')
    return 27,14


def check_topic_g_measurement():
    base = 'audit/topic-g/v2/measurement/'
    admission = load(base+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_TOPIC_G_MEASUREMENT',
         'Topic G numerical comparison lacks acceptance.')
    check_bindings(admission['artifacts'])
    pins = admission['packet_manifests']
    need(set(pins)=={'original_inputs','inputs','input_review','input_adoption',
                    'packet','arithmetic_review','root_adoption'},
         'Topic G measurement archive inventory changed.')
    for folder,pin in pins.items():
        need(digest((ROOT/base/folder/'manifest.json').read_bytes())==pin,
             'Changed Topic G measurement archive: '+folder)
        check_bindings([dict(r,path=base+folder+'/'+r['path'])
                        for r in load(base+folder+'/manifest.json')['exports']])
    counts = load(base+'inputs/author_counts.json')
    recount = load(base+'input_review/recount.json')
    result = load(base+'packet/measurement.json')
    need(counts['documents']==recount['documents'] and
         all(counts[k]==v for k,v in recount['raw_files'].items()),
         'Topic G primitive counts disagree with the independent recount.')
    spec = importlib.util.spec_from_file_location('topic_g_independent_arithmetic',
                                                 ROOT/base/'arithmetic_review/check.py')
    checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
    expected,sensitivity,fractions = checker.calculate(recount,counts['identification_cover_sensitivity'])
    checker.verify(result,expected,sensitivity)
    bars = checker.chart((ROOT/base/'packet/complete_costs.svg').read_text(),result['primary'])
    checker.reader((ROOT/base/'packet/measurement.tex').read_text(),result)
    with (ROOT/base/'arithmetic_review/fractions.csv').open(newline='') as stream:
        recorded = list(csv.DictReader(stream))
    need(recorded==[{k:str(v) for k,v in row.items()} for row in fractions] and
         len(fractions)==admission['all_exact_fractions']==270 and bars==9,
         'Topic G exact fractions or actual graph geometry changed.')
    input_review = load(base+'input_review/review.json')
    input_adoption = load(base+'input_adoption/review.json')
    review = load(base+'arithmetic_review/review.json')
    adoption = load(base+'root_adoption/review.json')
    accepted_inputs = {k:pins[k] for k in ['inputs','input_review','input_adoption']}
    need(input_review['status']=='ACCEPTED_INDEPENDENT_TOPIC_G_MEASUREMENT_INPUTS_V2' and
         input_review['author_manifest']['sha256']==pins['inputs'] and
         input_review['preserved_original']['sha256']==pins['original_inputs'] and
         input_adoption['status']=='ROOT_ACCEPTED_TOPIC_G_INPUTS_V2_WITH_EXPLICIT_EXTRACTION_BOUNDARY' and
         input_adoption['input_manifests']=={'author':pins['inputs'],'independent':pins['input_review'],
                                           'preserved_original':pins['original_inputs']} and
         review['status']=='ACCEPTED_INDEPENDENT_TOPIC_G_NUMERICAL_COMPARISON' and
         review['accepted_author_packet']['sha256']==pins['packet'] and
         review['accepted_inputs']==result['input_manifests']==accepted_inputs and
         adoption['status']=='ROOT_ACCEPTED_G_COMPLETE_NUMERICAL_COMPARISON' and
         adoption['manifests']=={'author':pins['packet'],'independent':pins['arithmetic_review']} and
         adoption['input_manifests']==accepted_inputs and
         all(d['corrections_requested']==[] for d in [input_adoption,review,adoption]),
         'Topic G numerical acceptance refers to different inputs.')
    fresh = load(base+'root_adoption/fresh_independent_replay.json')
    need(fresh['status']=='PASS_INDEPENDENT_TOPIC_G_NUMERICAL_AND_READER_CHECK' and
         fresh['primary']==result['primary']==review['primary']==adoption['primary']==admission['primary'] and
         fresh['metric_coordinates']==admission['policy_coordinates']==30 and
         fresh['combined_fractions']==admission['combined_fractions']==90 and
         fresh['conditional_fractions']==admission['conditional_fractions']==60 and
         fresh['article_only_fractions']==admission['article_only_fractions']==120 and
         fresh['all_exact_fractions']==270 and fresh['bar_rectangles_checked']==9 and
         len(fresh['arithmetic_controls'])==17 and len(fresh['presentation_controls'])==2 and
         all(r['rejected'] for r in fresh['arithmetic_controls']+fresh['presentation_controls']),
         'Topic G independent numerical evidence changed.')
    mapping = load(base+'recount_mapping.json')
    routes = mapping['routes']; by_private = {r['private_path']:r for r in routes}
    public = [dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'])
              for r in routes if r['public_path'] is not None]
    private = [r for r in routes if r['public_path'] is None]
    need(len(routes)==len(by_private)==35 and len(public)==33 and len(private)==2 and
         {r['source_id'] for r in private}=={'L009','L092'} and mapping['primary_exported'] is False,
         'Topic G recount mapping changed its public/original boundary.')
    check_bindings(public)
    replacement = load(base+'inputs/replacement_input_spec.json')
    policy = load(base+'inputs/policy.json')
    measured = list(policy['source_roster'].values())+list(policy['replacement_roster'].values())
    for kind in ['complete_programs','complete_operational_drivers','complete_formal_files']:
        measured += replacement[kind]
    measured += [policy[k] for k in ['author','current_edition','root_adoption',
                                    'accepted_scope','program_inventory']]
    measured += [replacement['appendix_tex']]
    for row in measured:
        mapped = by_private.get(row['path'])
        need(mapped is not None and all(mapped[k]==row[k] for k in ['bytes','sha256']),
             'Topic G recount omits a frozen input: '+row['path'])
    need(set(by_private)-{r['path'] for r in measured}=={'topic_G_current_edition/formal/scope.json'},
         'Topic G recount has unexplained inputs.')
    need(by_private['topic_G_current_edition/formal/scope.json']['public_path']==
         'papers/topic-g/v2/formal/scope.json' and
         load('papers/topic-g/v2/formal/scope.json')==replacement['formal_scope'],
         'Topic G formal scope differs from its measured boundary.')
    scope = load('papers/topic-g/v2/scope.json')
    boundary = load(base+'inputs/source_contract_boundary.json')
    need(digest((ROOT/'audit/topic-g/v2/admission.json').read_bytes())==admission['proof_admission_sha256'] and
         admission['source_ids']==boundary['source_ids']==result['source_ids']==['L009','L092'] and
         admission['source_records']==boundary['row_count']==len(scope['rows'])==79 and
         boundary['source_rows']==scope['rows'] and boundary['proof_spans']==scope['proof_spans'] and
         admission['proof_spans']==len(scope['proof_spans'])==34 and
         all(boundary[k]==scope[k] for k in ['complete_application_closure','qualification','source_bindings']) and
         admission['principal_contracts']==boundary['principal_contracts']==2 and
         admission['project_total_preserved']==27,
         'Topic G measurement changed scientific coverage.')
    need(admission['pdf_metric_cells']==recount['pdf_metric_cells']==180 and
         admission['raw_metric_cells']==recount['raw_metric_cells']==220 and
         admission['required_finite_programs']==4 and admission['witness_certificate_bridges']==2 and
         admission['validation_programs']==7 and admission['complete_programs']==13 and
         admission['separate_drivers']==3 and admission['separate_formal_files']==6 and
         admission['scoped_Lean_declarations']==40 and
         admission['unknown_external_costs']==dict.fromkeys(['retained_BDL_full_proof',
             'retained_Kantor_full_proof','other_external_proofs','historical_programs','graphics_formula_layout']) and
         admission['paired_dependency_audit_complete'] is False and
         admission['source_specific_formalization'] is False and
         admission['original_input_not_current'] is True and
         admission['new_source_credit']==admission['new_question_credit']==admission['new_formal_credit']==0,
         'Topic G numerical summary invents costs, proof coverage or credits.')
    return 180,270


def check_representation_measurement():
    base = 'audit/topic-representation/v2/measurement/'
    admission = load(base+'admission.json')
    need(admission['status']=='PASS_ROOT_ADMITTED_REPRESENTATION_MEASUREMENT',
         'Representation numerical comparison lacks acceptance.')
    check_bindings(admission['artifacts'])
    pins = admission['packet_manifests']
    need(set(pins)=={'inputs','input_review','input_adoption','packet','arithmetic_review','root_adoption'},
         'Representation numerical archive inventory changed.')
    for folder,pin in pins.items():
        need(digest((ROOT/base/folder/'manifest.json').read_bytes())==pin,
             'Changed representation measurement archive: '+folder)
        check_bindings([dict(r,path=base+folder+'/'+r['path'])
                        for r in load(base+folder+'/manifest.json')['exports']])
    counts = load(base+'inputs/author_counts.json')
    recount = load(base+'input_review/independent_replay.json')
    result = load(base+'packet/results.json')
    boundary = load(base+'inputs/source_contract_boundary.json')
    bindings = load(base+'packet/input_bindings.json')
    need(counts['documents']==recount['documents'] and
         all(counts[k]==v for k,v in recount['raw_files'].items()),
         'Representation primitive counts disagree with the independent recount.')
    spec = importlib.util.spec_from_file_location('representation_independent_arithmetic',
                                                 ROOT/base/'arithmetic_review/check.py')
    checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
    expected,fractions = checker.calculate(counts)
    checker.verify(result,expected,counts,boundary,bindings)
    bars = checker.chart((ROOT/base/'packet/complete_costs.svg').read_text(),result['primary'])
    checker.reader((ROOT/base/'packet/measurement.tex').read_text(),result)
    for file in ['packet/comparisons.csv','arithmetic_review/fractions.csv']:
        with (ROOT/base/file).open(newline='') as stream:
            recorded = list(csv.DictReader(stream))
        need(recorded==[{k:str(v) for k,v in row.items()} for row in fractions],
             'Representation exact CSV fractions differ: '+file)
    input_review = load(base+'input_review/review.json')
    input_adoption = load(base+'input_adoption/review.json')
    review = load(base+'arithmetic_review/review.json')
    adoption = load(base+'root_adoption/review.json')
    accepted_inputs = {k:pins[k] for k in ['inputs','input_review','input_adoption']}
    need(input_review['status']=='ACCEPTED_INDEPENDENT_REPRESENTATION_MEASUREMENT_INPUTS' and
         input_review['author_manifest_sha256']==pins['inputs'] and
         input_adoption['status']=='ROOT_ACCEPTED_REPRESENTATION_MEASUREMENT_INPUTS' and
         input_adoption['input_manifests']=={'author':pins['inputs'],'independent':pins['input_review']} and
         review['status']=='ACCEPTED_INDEPENDENT_REPRESENTATION_NUMERICAL_AND_READER_REVIEW' and
         review['numerical_manifest_sha256']==pins['packet'] and
         adoption['status']=='ROOT_ACCEPTED_REPRESENTATION_COMPLETE_NUMERICAL_COMPARISON' and
         adoption['manifests']=={'author':pins['packet'],'independent':pins['arithmetic_review']} and
         review['input_manifests']==adoption['input_manifests']==bindings['accepted_manifest_sha256']==accepted_inputs and
         all(d['corrections_requested']==[] for d in [input_adoption,review,adoption]),
         'Representation acceptance refers to different numerical inputs.')
    fresh = load(base+'root_adoption/fresh_independent_replay.json')
    utf8 = expected['calibrated_selected','NFC','utf8_bytes_with_collapsed_whitespace']['comparisons']['written_papers']
    need(fresh['status']=='PASS_INDEPENDENT_REPRESENTATION_NUMERICAL_REVIEW' and
         fresh['primary']==result['primary']==review['primary']==adoption['primary']==admission['primary'] and
         fresh['calibrated_NFC_UTF8_written']==review['UTF8_reversal']==adoption['UTF8_reversal']==admission['UTF8_reversal']==utf8 and
         utf8['numerator']<utf8['denominator'] and
         fresh['coordinates']==admission['policy_coordinates']==30 and
         fresh['combined_fractions']==admission['combined_fractions']==90 and
         fresh['conditional_fractions']==admission['conditional_fractions']==30 and
         fresh['all_exact_fractions']==admission['all_exact_fractions']==len(fractions)==120 and
         fresh['bar_rectangles_checked']==bars==9 and
         len(fresh['controls'])==22 and len(fresh['presentation_controls'])==3 and
         all(r['rejected'] for r in fresh['controls']+fresh['presentation_controls']),
         'Representation exact arithmetic or its unit-sensitive reversal changed.')
    mapping = load(base+'recount_mapping.json')
    routes = mapping['routes']; by_private = {r['private_path']:r for r in routes}
    public = [dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'])
              for r in routes if r['public_path'] is not None]
    private = [r for r in routes if r['public_path'] is None]
    need(len(routes)==len(by_private)==17 and len(public)==16 and len(private)==1 and
         private[0]['source_id']=='F010' and mapping['primary_exported'] is False,
         'Representation recount changed its public/original boundary.')
    check_bindings(public)
    replacement = load(base+'inputs/replacement_input_spec.json')
    policy = load(base+'inputs/policy.json')
    measured = list(policy['source_roster'].values())+list(policy['replacement_roster'].values())
    for kind in ['complete_validation_programs','complete_operational_drivers','complete_formal_files']:
        measured += replacement[kind]
    measured += [policy[k] for k in ['author','independent_review','role_delta','root_adoption','accepted_scope']]
    measured += [replacement['appendix_tex']]
    for row in measured:
        mapped = by_private.get(row['path'])
        need(mapped is not None and all(mapped[k]==row[k] for k in ['bytes','sha256']),
             'Representation recount omits a frozen input: '+row['path'])
    need(set(by_private)-{r['path'] for r in measured}=={'topic_Representation_volume/formal/scope.json'} and
         by_private['topic_Representation_volume/formal/scope.json']['public_path']==
         'papers/topic-representation/v2/formal/scope.json' and
         load('papers/topic-representation/v2/formal/scope.json')==replacement['formal_scope'],
         'Representation formal scope differs from its measured boundary.')
    original_mapping = load(base+'input_adoption/public_mapping.json')
    need(bindings['published_artifacts']==original_mapping['artifacts'],
         'Representation numeric input routing differs from the accepted mapping.')
    for row in bindings['published_artifacts']:
        need(digest((ROOT/row['path']).read_bytes())==row['sha256'],
             'Changed measured representation artifact: '+row['path'])
    scope = load('papers/topic-representation/v2/scope.json')
    need(digest((ROOT/'audit/topic-representation/v2/admission.json').read_bytes())==admission['proof_admission_sha256'] and
         admission['source_ids']==['F010'] and
         admission['source_blocks']==boundary['row_count']==len(scope['contracts'])==6 and
         boundary['source_rows']==scope['contracts'] and
         all(boundary[k]==scope[k] for k in ['proof_spans','precise_hypotheses','source_qualifications',
                                            'exclusions','validation_boundary','inherited_source_block_order']) and
         boundary['attribution']==scope['source'] and
         admission['proof_contexts']==len(scope['proof_spans'])==13 and
         admission['principal_contracts']==boundary['principal_contracts']==1 and
         admission['project_total_preserved']==27,
         'Representation measurement changed scientific coverage or attribution.')
    need(admission['pdf_metric_cells']==recount['pdf_metric_cells']==120 and
         admission['raw_metric_cells']==recount['raw_metric_cells']==60 and
         admission['complete_validation_programs']==2 and admission['uniform_finite_proof_premises']==0 and
         admission['separate_drivers']==2 and admission['separate_formal_files']==2 and
         admission['scoped_Lean_declarations']==12 and admission['generic_declarations']==8 and
         admission['reused_local_declarations']==4 and
         admission['unknown_external_costs']==dict.fromkeys(['retained_external_proofs',
             'historical_programs','graphics_formula_layout','operational_engineering']) and
         admission['paired_dependency_audit_complete'] is False and
         admission['source_specific_formalization'] is False and
         admission['new_source_credit']==admission['new_question_credit']==admission['new_formal_credit']==0,
         'Representation numerical summary invents costs, proof coverage or credits.')
    return 120,120


def check_chamber_measurement():
    base = 'audit/topic-chamber/v2/measurement/'
    admission = load(base+'admission.json')
    need(admission['status']=='ROOT_ADMITTED_CHAMBER_MEASUREMENT',
         'Chamber numerical admission missing.')
    check_bindings(admission['artifacts'])
    check_bindings(admission['measured_public_inputs'])
    need(digest((ROOT/'audit/topic-chamber/v2/admission.json').read_bytes())==
         admission['proof_admission_sha256'], 'Chamber scientific input changed.')
    pins = admission['packet_manifests']
    need(set(pins)=={'inputs','input_review','input_adoption','packet','arithmetic_review'},
         'Chamber measurement archive inventory changed.')
    for folder,pin in pins.items():
        need(digest((ROOT/base/folder/'manifest.json').read_bytes())==pin,
             'Changed Chamber measurement archive: '+folder)
        check_bindings([dict(r,path=base+folder+'/'+r['path'])
                        for r in load(base+folder+'/manifest.json')['exports']])
    counts = load(base+'inputs/input_counts.json')
    recount = load(base+'input_review/recount.json')
    for k,d in counts['documents'].items():
        need(d['variants']==recount['documents'][k]['variants'],
             'Chamber independent primitive PDF counts disagree.')
    for k,v in recount['raw_files'].items():
        need(counts[k]==v,'Chamber complete raw files disagree.')
    spec = importlib.util.spec_from_file_location('chamber_independent_arithmetic',
                                                 ROOT/base/'arithmetic_review/check.py')
    checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
    expected = checker.expected_rows(counts)
    result = load(base+'packet/results.json')
    review = load(base+'arithmetic_review/review.json')
    need(result['coordinates']==expected and result['primary']==expected[22]==admission['primary'],
         'Chamber complete sums or exact fractions changed.')
    need(review['status']=='ROOT_ACCEPTED_CHAMBER_NUMERICAL_COMPARISON' and
         review['numerical_manifest_sha256']==pins['packet'] and review['primary']==result['primary'],
         'Chamber distinct numerical review not bound.')
    need(checker.bars((ROOT/base/'packet/complete_costs.svg').read_text(),result['primary'])==9,
         'Chamber actual plot bars changed.')
    need((admission['original_manuscripts'],admission['source_rows'],admission['proof_contexts'],
          admission['coordinates'],admission['exact_fractions'])==(2,27,22,30,150) and
         all(admission[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']) and
         admission['external_and_graphic_costs'] is None,
         'Chamber measurement changes scope or invents a cost.')
    return 180,150


def check_available_text_comparisons():
    base = 'audit/available-text/v1/'
    admission = load(base+'admission.json')
    need(admission['status']=='ROOT_ADOPTED_COMPLETE_AVAILABLE_TEXT_COMPARISONS',
         'Available authored-text comparisons lack adoption.')
    check_bindings(admission['artifacts'])
    for folder,pin in admission['packets'].items():
        need(digest((ROOT/base/folder/'manifest.json').read_bytes())==pin,
             'Available-text archive changed: '+folder)
        check_bindings([dict(r,path=base+folder+'/'+r['path'])
                        for r in load(base+folder+'/manifest.json')['exports']])
    for row in admission['proof_admissions'].values():
        need(digest((ROOT/row['path']).read_bytes())==row['sha256'],
             'B/C principal-result scope changed.')
    spec = importlib.util.spec_from_file_location('available_text_independent_arithmetic',
                                                 ROOT/base/'arithmetic_review/check.py')
    checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
    old = {}
    for topic,(path,pin) in checker.PREVIOUS.items():
        need(digest((ROOT/path).read_bytes())==pin,'Historical PDF-only result changed.')
        old[topic] = load(path)
    expected = checker.expected_rows(old,load(base+'inputs/counts.json'))
    result = load(base+'packet/results.json')
    primary = checker.check_result(result,expected)
    need(primary==admission['primary'],'Available-text primary comparison changed.')
    need(checker.csv_check((ROOT/base/'packet/comparisons.csv').read_text(),expected)==360,
         'Available-text exact CSV fractions changed.')
    for topic,row in primary.items():
        need(checker.bars((ROOT/base/('packet/'+topic+'-costs.svg')).read_text(),topic,row)==9,
             'Available-text actual graph bars changed.')
    checker.reader((ROOT/base/'packet/measurement.tex').read_text(),primary)
    review = load(base+'arithmetic_review/review.json')
    need(review['status']=='ACCEPTED_NEW_B_C_COMPLETE_AVAILABLE_TEXT_COMPARISONS' and
         review['author_manifest_sha256']==admission['packets']['packet'] and
         digest((ROOT/base/'root_replay.json').read_bytes())==admission['root_replay_sha256'] and
         admission['original_manuscripts']==8 and admission['historical_PDF_comparisons_unchanged'] and
         all(admission[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),
         'Available-text review, count or scope changed.')
    return 360


def check_complete_corpus_programme():
    base = 'audit/corpus/v1/'
    admission = load(base+'admission.json')
    need(admission['status']=='ROOT_ADOPTED_COMPLETE_CORPUS_PROGRAMME',
         'Complete corpus programme lacks adoption.')
    check_bindings(admission['artifacts'])
    need(digest((ROOT/base/'packet/manifest.json').read_bytes())==admission['author_manifest_sha256'] and
         digest((ROOT/base/'root_replay.json').read_bytes())==admission['root_replay_sha256'],
         'Corpus programme or its evidence replay changed.')
    entries = load(base+'packet/inventory.json')['entries']
    by_id = {r['original_id']:r for r in entries}
    previous = {r['id']:r for r in load('audit/source_registry.json')['entries']}
    need(len(entries)==len(by_id)==161 and set(by_id)==set(previous) and
         all(r['title']==previous[k]['title'] for k,r in by_id.items()),
         'Original manuscript identity set changed.')
    need(all(r['target_remains_active'] and r['unique_original_count']==1 for r in entries),
         'An original was excluded or counted more than once.')
    accessible = {k for k,r in by_id.items() if r['source_access']['accessible']}
    admitted = {k for k,r in by_id.items() if r['proof']['principal_contract_admitted']}
    need(len(accessible)==104 and len(admitted)==27 and admitted<=accessible and
         len(accessible-admitted)==77 and len(set(by_id)-accessible)==57,
         'Corpus access/proof partition changed.')
    batches = load(base+'packet/prioritized_batches.json')['batches']
    pending = [k for batch in batches for k in batch['original_ids']]
    need(len(pending)==len(set(pending))==134 and set(pending)==set(by_id)-admitted,
         'An unfinished original was dropped from the programme.')
    need(admission['all_originals_remain_targets'] and admission['source_retrieval_continues_within_fixed_titles'] and
         not admission['fresh_exhaustive_unavailability_claim'] and
         admission['new_source_credit']==admission['new_question_credit']==0 and
         admission['compression_factor'] is None,
         'Corpus inventory invents mathematical credit or excludes retrieval targets.')
    return 161,104,77,57


def check_additional_original_recoveries():
    current = load('audit/corpus/current.json')
    check_bindings([current['base_inventory']]+current['added_admissions'])
    entries = load(current['base_inventory']['path'])['entries']
    accessible = {r['original_id'] for r in entries if r['source_access']['accessible']}
    historical = {r['original_id'] for r in entries if r['proof']['principal_contract_admitted']}
    need(set(current['historical_admitted_ids'])==historical,
         'Additive programme changed the historical admission set.')
    additions = set()
    for record in current['added_admissions']:
        a = load(record['path']); additions.add(a['source_id'])
        need(a['status']=='ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT' and
             a['principal_originals_added']==1 and a['source_rows']==32 and
             a['new_question_credit']==0 and not a['whole_source_formalized'] and
             a['compression_factor'] is None and a['measurement_status']=='pending',
             'Additional admission changed proof, question or measurement scope.')
        check_bindings(a['artifacts'])
        for key in ['author','review']:
            row = a[key]; need(digest((ROOT/row['path']).read_bytes())==row['sha256'],
                              'Additional author/review manifest changed.')
            parent = Path(row['path']).parent
            check_bindings([dict(r,path=str(parent/r['path'])) for r in load(row['path'])['exports']])
        review = load(str(Path(a['review']['path']).parent/'review.json'))
        if a['source_id']=='F015':
            need(review['status']=='ROOT_ACCEPTED_COMPLETE_CORRECTED_F015_PRINCIPAL_CONTRACT' and
                 review['accepted_author_manifest_sha256']==a['author']['sha256'] and
                 review['clarifications_resolved'] and a['formal']['new']==0 and
                 review['independent_120_cell_check']['unordered_pair_orbits']==35,
                 'Matching review or correction scope changed.')
        else:
            need(a['source_id']=='L028' and review['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT' and
                 review['author_manifest_sha256']==a['author']['sha256'] and
                 review['scope']['connected_symbols_only'] and not review['scope']['duality_quotiented'] and
                 a['formal']['new']==7,'Chiral enumeration scope changed.')
            check_bindings([a['root_replay']])
            replay = load(a['root_replay']['path'])
            need(replay['status']=='PASS' and len(replay['controls_rejected'])==10,
                 'Chiral enumeration independent replay changed.')
    need(additions=={'F015','L028'} and not additions&historical,
         'A new original was counted twice.')
    admitted = historical|additions
    need(len(admitted)==current['admitted_principal_originals']==29 and
         set(current['admitted_original_ids'])==admitted and
         set(current['accessible_pending_original_ids'])==accessible-admitted and
         len(current['accessible_pending_original_ids'])==current['accessible_pending_complete_recovery']==75 and
         len(current['retrieval_original_ids'])==current['pending_source_retrieval']==57 and
         set(current['retrieval_original_ids'])=={r['original_id'] for r in entries}-accessible and
         current['all_originals_remain_active'] and not current['all_conjectures_resolved'] and
         not current['all_original_proofs_recovered'] and current['currently_measured_originals']==27 and
         set(current['measurement_pending_original_ids'])==additions,
         'Current original partition or completion scope changed.')
    catalogue = load('papers/expansion_catalogue.json')
    need(len(catalogue['entries'])==4 and set(catalogue['original_ids'])==additions and
         {k for r in catalogue['entries'] for k in r['source_contracts']}==additions,
         'Additional canonical paper catalogue changed.')
    for row in catalogue['entries']:
        need((ROOT/row['tex']).is_file() and (ROOT/row['pdf']).is_file() and
             row['measurement_status']=='pending','Missing additional manuscript.')
    return 29,75


def check_consolidated_measurement_overview():
    base = 'audit/overview/v1/'
    a = load(base+'admission.json')
    need(a['status']=='ROOT_ADMITTED_CONSOLIDATED_NUMERICAL_OVERVIEW',
         'Consolidated comparison lacks root admission.')
    check_bindings(a['artifacts'])
    for key in ['author_manifest','independent_manifest','public_replay']:
        check_bindings([a[key]])
    for key in ['author_manifest','independent_manifest']:
        parent = Path(a[key]['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(a[key]['path'])['exports']])
    locations = load(base+'public_locations.json')
    inputs = load(base+'packet/inputs.json')['bindings']
    need(set(locations)==set(inputs) and len(inputs)==20,'Overview input set changed.')
    check_bindings([dict(row,path=locations[k]) for k,row in inputs.items()])
    spec = importlib.util.spec_from_file_location('independent_overview_recount',ROOT/base/'independent_review/check.py')
    checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
    result = load(base+'packet/results.json')
    fractions = checker.arithmetic(result,checker.expected(ROOT))
    svg,pdf = checker.graphs(ROOT/base/'packet',result)
    need(fractions==a['independent_exact_fractions']==57 and
         svg==a['actual_SVG_bars']==84 and pdf==a['actual_PDF_bars']==84 and
         a['distinct_originals']==27 and a['topic_count']==10 and
         set(a['original_ids'])=={r['original_id'] for r in load('audit/corpus/v1/packet/inventory.json')['entries'] if r['proof']['principal_contract_admitted']} and
         a['additional_measurements_pending']==['F015','L028'] and
         a['pooled_factor'] is None and a['no_cross_topic_common_discount'] and
         all(a[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),
         'Overview cost, source or scope changed.')
    need(load(a['public_replay']['path'])['status']=='PASS_PUBLIC_ONLY_PORTABLE_REPLAY',
         'Overview portable replay missing.')
    return fractions,svg,pdf


def check_diagonal_admission_and_latest_programme():
    latest = load('audit/corpus/updates/diagonal.json')
    check_bindings([latest['previous_snapshot']]+latest['added_admissions'])
    previous = load(latest['previous_snapshot']['path'])
    a = load('audit/topic-diagonal/v1/admission.json')
    need(a['source_id']=='N007' and a['principal_originals_added']==1 and
         a['status']=='ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT' and
         a['source_rows']==32 and a['proof_spans']==13 and
         a['new_question_credit']==a['N006_whole_original_credit']==0 and
         not a['whole_source_formalized'] and a['compression_factor'] is None and
         a['measurement_status']=='pending', 'Diagonal admission scope changed.')
    check_bindings(a['artifacts'])
    for key in ['author','review','public_replay','public_review_replay']:
        check_bindings([a[key]])
    for key in ['author','review']:
        row = a[key]; parent = Path(row['path']).parent
        exports = load(row['path'])['exports']
        need(len(exports)==row['exports'],'Diagonal export count changed.')
        check_bindings([dict(r,path=str(parent/r['path'])) for r in exports])
    review = load(str(Path(a['review']['path']).parent/'review.json'))
    need(review['status']=='ACCEPT_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT' and
         review['author_manifest_sha256']==a['author']['sha256'] and
         not review['whole_geometry_formalized'],'Diagonal distinct review changed.')
    replay = load(a['public_replay']['path'])
    independent = load(a['public_review_replay']['path'])
    need(replay['status']=='PASS' and replay['formal_declarations']==8 and
         len(replay['controls_rejected'])==5 and independent['status']=='PASS' and
         independent['independent_quotient_model']=={
             'raw_group':96,'kernel':2,'faithful_group':48,'chambers':48},
         'Diagonal public checks changed.')
    need(set(latest['admitted_original_ids'])==set(previous['admitted_original_ids'])|{'N007'} and
         set(latest['accessible_pending_original_ids'])==set(previous['accessible_pending_original_ids'])-{'N007'} and
         latest['retrieval_original_ids']==previous['retrieval_original_ids'] and
         latest['admitted_principal_originals']==len(latest['admitted_original_ids'])==30 and
         latest['accessible_pending_complete_recovery']==len(latest['accessible_pending_original_ids'])==74 and
         latest['accessible_originals']==104 and latest['originals']==161 and
         latest['pending_source_retrieval']==57 and latest['currently_measured_originals']==27 and
         set(latest['measurement_pending_original_ids'])=={'F015','L028','N007'} and
         latest['all_originals_remain_active'] and not latest['all_original_proofs_recovered'] and
         not latest['all_conjectures_resolved'],'Latest original partition changed.')
    catalogue = load('papers/catalogue_diagonal.json')
    check_bindings([catalogue['previous_catalogue']])
    need(catalogue['entries'][:4]==load(catalogue['previous_catalogue']['path'])['entries'] and
         len(catalogue['entries'])==6 and set(catalogue['original_ids'])=={'F015','L028','N007'} and
         {k for r in catalogue['entries'] for k in r['source_contracts']}==set(catalogue['original_ids']),
         'Latest paper catalogue changed.')
    for row in catalogue['entries']:
        need((ROOT/row['tex']).is_file() and (ROOT/row['pdf']).is_file(),'Missing added manuscript.')
    return 30,74


def check_current_programme_pointer():
    current = load('audit/corpus/latest.json')
    check_bindings([current['snapshot']])
    need({k:v for k,v in current.items() if k!='snapshot'}==load(current['snapshot']['path']),
         'Current programme differs from its admitted snapshot.')
    check_bindings([current['base_inventory']]+current['added_admissions'])
    entries = load(current['base_inventory']['path'])['entries']
    originals = {r['original_id'] for r in entries}
    accessible = {r['original_id'] for r in entries if r['source_access']['accessible']}
    historical = {r['original_id'] for r in entries if r['proof']['principal_contract_admitted']}
    additions = [load(r['path'])['source_id'] for r in current['added_admissions']]
    need(len(additions)==len(set(additions)) and not set(additions)&historical,
         'Current programme counts an original twice.')
    admitted = historical|set(additions)
    need(set(current['admitted_original_ids'])==admitted and
         current['admitted_principal_originals']==len(admitted) and admitted<=accessible and
         set(current['accessible_pending_original_ids'])==accessible-admitted and
         current['accessible_pending_complete_recovery']==len(accessible-admitted) and
         set(current['retrieval_original_ids'])==originals-accessible and
         current['originals']==len(originals)==161 and current['accessible_originals']==len(accessible) and
         current['all_originals_remain_active'],'Current programme partition changed.')
    catalogue = load('papers/latest_catalogue.json')
    check_bindings([catalogue['previous_catalogue']])
    need(set(catalogue['original_ids'])==set(additions) and
         {k for r in catalogue['entries'] for k in r['source_contracts']}==set(additions),
         'Current additional catalogue loses a recovered original.')
    return len(admitted),len(accessible-admitted)


def check_graph_application_extensions():
    paths = {
        'L128': 'audit/topic-a/extensions/diagram-symmetries/v1',
        'L068': 'audit/topic-c/extensions/livingstone/v1',
    }
    for source, base in paths.items():
        a = load(base+'/admission.json')
        need(a['source_id']==source and a['principal_originals_added']==1 and
             a['status']=='ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT' and
             a['new_question_credit']==0 and not a['whole_source_formalized'] and
             a['compression_factor'] is None and a['measurement_status']=='pending' and
             a['charge_full_common_paper'] and a['charge_common_once_within_topic'] and
             not a['cross_topic_overlap_discount'], 'Graph application admission scope.')
        check_bindings(a['artifacts'])
        for key in ['author','review','public_replay','public_review_replay']:
            check_bindings([a[key]])
        for key in ['author','review']:
            row = a[key]; parent = Path(row['path']).parent
            exports = load(row['path'])['exports']
            need(len(exports)==row['exports'],'Graph application export count.')
            check_bindings([dict(r,path=str(parent/r['path'])) for r in exports])
        r = load(a['public_replay']['path']); q = load(a['public_review_replay']['path'])
        review = load(str(Path(a['review']['path']).parent/'review.json'))
        need(r['status']==q['status']=='PASS' and
             review['author_manifest_sha256']==a['author']['sha256'], 'Graph application review binding.')
        if source=='L128':
            need(a['source_rows']==14 and a['proof_spans']==7 and a['formal']['new']==6 and
                 len(r['formal_axiom_reports'])==6 and r['finite_groups']==79 and
                 r['finite_involution_triples']==32628 and len(r['controls_rejected'])==3 and
                 q['coordinate_models']==13 and len(q['controls_rejected'])==10 and
                 review['status']=='ACCEPTED_INDEPENDENT_COMPLETE_L128_APPLICATION_REVIEW' and
                 not review['open_requests'], 'Diagram-symmetry evidence scope.')
        else:
            need(a['source_rows']==17 and a['proof_spans']==9 and a['formal']['new']==0 and
                 a['formal']['reused']==3 and not a['literal_Q_recovered'] and
                 a['literal_P_recovered'] and a['corrected_Q_recovered'] and
                 len(r['Lean_axioms'])==3 and len(r['incidence_rows'])==12 and
                 all(z['rejected'] for z in r['controls']) and len(r['controls'])==3 and
                 review['status']=='ACCEPT_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT' and
                 not review['remaining_math_corrections'], 'Livingstone evidence scope.')
    latest = load('audit/corpus/updates/diagram-symmetries-and-livingstone.json')
    check_bindings([latest['previous_snapshot']]+latest['added_admissions'])
    previous = load(latest['previous_snapshot']['path'])
    need(set(latest['admitted_original_ids'])==set(previous['admitted_original_ids'])|set(paths) and
         set(latest['accessible_pending_original_ids'])==set(previous['accessible_pending_original_ids'])-set(paths) and
         latest['retrieval_original_ids']==previous['retrieval_original_ids'] and
         latest['admitted_principal_originals']==len(latest['admitted_original_ids'])==32 and
         latest['accessible_pending_complete_recovery']==len(latest['accessible_pending_original_ids'])==72 and
         latest['accessible_originals']==104 and latest['originals']==161 and
         latest['pending_source_retrieval']==57 and latest['currently_measured_originals']==27 and
         set(latest['measurement_pending_original_ids'])=={'F015','L028','N007','L128','L068'},
         'Graph application snapshot partition.')
    c = load('papers/catalogue_graph_extensions.json')
    check_bindings([c['previous_catalogue']])
    need(c['entries'][:6]==load(c['previous_catalogue']['path'])['entries'] and
         len(c['entries'])==9 and set(c['original_ids'])=={'F015','L028','N007','L128','L068'} and
         {x for r in c['entries'] for x in r['source_contracts']}==set(c['original_ids']),
         'Graph application catalogue.')
    for row in c['entries']:
        need((ROOT/row['tex']).is_file() and (ROOT/row['pdf']).is_file(),'Missing graph application paper.')
    return 32,72


def check_two_additional_measurements():
    base = 'audit/additional-measurements/v1'
    a = load(base+'/admission.json')
    need(a['status']=='ROOT_ADMITTED_COMPLETE_MEASUREMENTS' and
         a['source_ids']==['F015','L028'] and a['newly_measured_originals']==2 and
         a['new_principal_credit']==a['new_question_credit']==0 and
         not a['full_formalization_claim'] and a['whole_common_charged'] and
         not a['cross_topic_discount'] and all(v is None for v in a['unknown_costs'].values()),
         'Two additional measurement scope.')
    check_bindings(a['artifacts']+a['scientific_admissions']+[a['earlier_overview']])
    for row in a['packets'].values():
        check_bindings([row]); parent=Path(row['path']).parent
        exports=load(row['path'])['exports']
        need(len(exports)==row['exports'],'Additional measurement export count.')
        check_bindings([dict(r,path=str(parent/r['path'])) for r in exports])
    for key in ['public_replay','public_independent_replay']:
        check_bindings([a[key]])
    r=load(a['public_replay']['path']); q=load(a['public_independent_replay']['path'])
    need(r['status']=='PASS' and len(r['exact_regenerated_files'])==6 and r['reader_pages_equal']==2 and
         len(r['checks']['semantic_controls'])==12 and q['status']=='PASS_DISTINCT_ARITHMETIC_AND_GRAPH_REVIEW' and
         q['exact_fractions']==q['csv_rows']==240 and q['actual_svg_bars']==q['actual_pdf_bars']==12 and
         len(q['controls_rejected'])==5 and q['stacking_checked'], 'Additional numerical/plot replay.')
    need(q['primary']==a['primary'],'Additional primary factors differ from review.')
    for topic,nums in [('Matching',(37951,16732,17168,4998,4408)),
                       ('ChiralEnumeration',(29599,8831,23171,11940,11090))]:
        source,common,app,printed,raw=nums;row=a['primary'][topic]
        need(row['document_costs']==dict(source=source,common=common,application=app,program=printed) and
             row['raw_costs']['complete_programs']==raw, 'Additional whole costs.')
        for name,denom in [('written',common+app),('including_printed_programs',common+app+printed),
                           ('including_raw_programs',common+app+raw),('conditional_application',app)]:
            f=row['comparisons'][name]
            need(f['numerator']==source and f['denominator']==denom, 'Additional complete denominator.')
    latest=load('audit/corpus/updates/two-additional-measurements.json')
    check_bindings([latest['previous_snapshot']]+latest['added_measurements'])
    previous=load(latest['previous_snapshot']['path'])
    need(latest['admitted_original_ids']==previous['admitted_original_ids'] and
         latest['accessible_pending_original_ids']==previous['accessible_pending_original_ids'] and
         latest['retrieval_original_ids']==previous['retrieval_original_ids'] and
         latest['admitted_principal_originals']==32 and latest['currently_measured_originals']==29 and
         set(latest['measurement_pending_original_ids'])=={'L068','L128','N007'} and
         set(latest['measured_original_ids'])==set(latest['historical_admitted_ids'])|{'F015','L028'},
         'Measurement snapshot changes scientific scope.')
    c=load('papers/catalogue_two_measurements.json');check_bindings([c['previous_catalogue']])
    previous_c=load(c['previous_catalogue']['path'])
    need(len(c['entries'])==len(previous_c['entries'])==9,'Measurement catalogue loses a manuscript.')
    for row,old in zip(c['entries'],previous_c['entries']):
        want=dict(old)
        if row['topic'] in ['Matching','ChiralEnumeration']:
            want.update(measurement_status='admitted',measurement_admission=base+'/admission.json')
        need(row==want,'Measurement catalogue changes scientific identity.')
    return 240


def check_current_measurement_pointer():
    current=load('audit/corpus/latest.json');check_bindings(current['added_measurements'])
    extra=[x for row in current['added_measurements'] for x in load(row['path'])['source_ids']]
    historical=set(current['historical_admitted_ids']);measured=historical|set(extra)
    need(len(extra)==len(set(extra)) and not set(extra)&historical and
         set(current['measured_original_ids'])==measured and measured<=set(current['admitted_original_ids']) and
         current['currently_measured_originals']==len(measured) and
         set(current['measurement_pending_original_ids'])==set(current['admitted_original_ids'])-measured,
         'Current measurement partition duplicates or drops an original.')
    return len(measured)



def check_high_rank_symmetric_extension():
    base='audit/topic-b/extensions/high-rank/v1'
    a=load(base+'/admission.json')
    need(a['status']=='ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT' and
         a['source_id']=='L040' and a['topic']=='B' and a['principal_originals_added']==1 and
         a['source_rows']==35 and a['proof_spans']==25 and a['principal_targets']==5 and
         a['new_question_credit']==0 and not a['whole_source_formalized'] and
         a['compression_factor'] is None and a['measurement_status']=='pending' and
         a['charge_full_common_paper'] and a['charge_common_once_within_topic'] and
         not a['cross_topic_overlap_discount'] and not a['literal_branching_clause_recovered'] and
         a['corrected_general_presentation'], 'High-rank recovery scope.')
    check_bindings(a['artifacts']+[a['existing_common_binding']])
    for k in ['author','review','public_replay','public_review_replay']:check_bindings([a[k]])
    for k in ['author','review']:
        row=a[k];parent=Path(row['path']).parent;exports=load(row['path'])['exports']
        need(len(exports)==row['exports'],'High-rank complete export count.')
        check_bindings([dict(z,path=str(parent/z['path'])) for z in exports])
    review=load(base+'/independent_review/review.json')
    need(review['status']=='INDEPENDENTLY_ACCEPTED_WITH_EXPLICIT_RETAINED_INPUTS_AND_CORRECTION' and
         review['author_manifest_sha256']==a['author']['sha256'] and not review['blocking_findings'],
         'High-rank distinct mathematical review.')
    r=load(a['public_replay']['path']);q=load(a['public_review_replay']['path'])
    need(r['status']==q['status']=='PASS' and len(r['programs'])==4 and
         r['formal']['declarations']==8 and r['formal']['hypothesis_countermodels']==6 and
         [z['pages'] for z in r['render']]==[10,11,7] and
         all(z['per_page_text_identical'] and z['diagnostics']==[] for z in r['render']) and
         len(r['integrity_controls'])==11 and len(q['semantic_controls'])==14 and
         q['author_exports']==46, 'High-rank fresh checks.')
    current=load('audit/corpus/updates/high-rank-symmetric.json')
    check_bindings([current['previous_snapshot']]+current['added_admissions'])
    old=load(current['previous_snapshot']['path'])
    need(set(current['admitted_original_ids'])==set(old['admitted_original_ids'])|{'L040'} and
         set(current['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'L040'} and
         current['retrieval_original_ids']==old['retrieval_original_ids'] and
         current['admitted_principal_originals']==33 and current['accessible_pending_complete_recovery']==71 and
         current['currently_measured_originals']==29 and
         current['measured_original_ids']==old['measured_original_ids'] and
         set(current['measurement_pending_original_ids'])=={'L040','L068','L128','N007'},
         'High-rank original partition.')
    c=load('papers/catalogue_high_rank.json');check_bindings([c['previous_catalogue']])
    prior=load(c['previous_catalogue']['path'])
    need(c['entries'][:-2]==prior['entries'] and len(c['entries'])==11 and
         [z['topic'] for z in c['entries'][-2:]]==['B','B'] and
         [z['role'] for z in c['entries'][-2:]]==['umbrella_addition','application'] and
         set(c['original_ids'])==set(prior['original_ids'])|{'L040'},'High-rank catalogue.')
    return 33,71


def check_diagonal_measurement():
    base='audit/diagonal-measurement/v1'
    a=load(base+'/admission.json')
    need(a['status']=='ROOT_ADMITTED_COMPLETE_MEASUREMENTS' and
         a['source_ids']==['N007'] and a['newly_measured_originals']==1 and
         a['new_principal_credit']==a['new_question_credit']==0 and
         not a['full_formalization_claim'] and a['whole_common_charged'] and
         not a['cross_topic_discount'] and all(v is None for v in a['unknown_costs'].values()),
         'Diagonal numerical scope.')
    check_bindings(a['artifacts']+a['scientific_admissions']+[a['earlier_overview']])
    for row in a['packets'].values():
        check_bindings([row]); parent=Path(row['path']).parent
        exports=load(row['path'])['exports']
        need(len(exports)==row['exports'],'Diagonal measurement export count.')
        check_bindings([dict(r,path=str(parent/r['path'])) for r in exports])
    for k in ['public_replay','public_independent_replay']:check_bindings([a[k]])
    r=load(a['public_replay']['path']);q=load(a['public_independent_replay']['path'])
    need(r['status']=='PASS' and len(r['exact_regenerated_files'])==6 and r['reader_pages_equal']==2 and
         len(r['checks']['semantic_controls'])==13 and q['status']=='PASS_DISTINCT_ARITHMETIC_AND_GRAPH_REVIEW' and
         q['exact_fractions']==q['csv_rows']==120 and q['actual_svg_bars']==q['actual_pdf_bars']==6 and
         len(q['controls_rejected'])==5 and q['stacking_checked'] and q['primary']==a['primary'],
         'Diagonal distinct arithmetic, graph and fresh reader checks.')
    row=a['primary']['Diagonal'];source,common,app,printed,raw=22888,10968,11771,3161,2856
    need(row['document_costs']==dict(source=source,common=common,application=app,program=printed) and
         row['raw_costs']==dict(programs=raw,drivers=8600,formal=2587),'Complete diagonal costs.')
    for name,denom in [('written',common+app),('including_printed_programs',common+app+printed),
                       ('including_raw_programs',common+app+raw),('conditional_application',app)]:
        f=row['comparisons'][name]
        need(f['numerator']==source and f['denominator']==denom,'Diagonal complete denominator.')
    current=load('audit/corpus/updates/diagonal-measurement.json')
    check_bindings([current['previous_snapshot']]+current['added_measurements'])
    old=load(current['previous_snapshot']['path'])
    need(current['admitted_original_ids']==old['admitted_original_ids'] and
         current['accessible_pending_original_ids']==old['accessible_pending_original_ids'] and
         current['retrieval_original_ids']==old['retrieval_original_ids'] and
         current['currently_measured_originals']==30 and
         set(current['measured_original_ids'])==set(old['measured_original_ids'])|{'N007'} and
         set(current['measurement_pending_original_ids'])=={'L040','L068','L128'},
         'Diagonal numerical admission changes no scientific status.')
    c=load('papers/catalogue_diagonal_measurement.json');check_bindings([c['previous_catalogue']])
    old_c=load(c['previous_catalogue']['path'])
    need(len(c['entries'])==len(old_c['entries'])==11,'Diagonal measurement catalogue completeness.')
    for row,prior in zip(c['entries'],old_c['entries']):
        want=dict(prior)
        if row['topic']=='Diagonal':want.update(measurement_status='admitted',measurement_admission=base+'/admission.json')
        need(row==want,'Diagonal measurement changes scientific identity.')
    return 120


def check_ac_extension_measurements():
    base='audit/ac-extensions-measurement/v1';a=load(base+'/admission.json')
    need(a['status']=='ROOT_ADMITTED_COMPLETE_UPDATED_TOPIC_MEASUREMENTS' and
         a['source_ids']==['L068','L128'] and a['newly_measured_originals']==2 and
         a['original_manuscripts']==12 and a['independent_topics']==2 and
         a['new_principal_credit']==a['new_question_credit']==0 and
         not a['full_formalization_claim'] and a['whole_common_charged'] and
         not a['cross_topic_discount'] and all(x is None for x in a['unknown_costs'].values()),
         'Expanded A/C measurement scope.')
    check_bindings(a['artifacts']+a['scientific_admissions']+a['earlier_measurements'])
    for row in a['packets'].values():
        check_bindings([row]);parent=Path(row['path']).parent;exports=load(row['path'])['exports']
        need(len(exports)==row['exports'],'Expanded A/C export count.')
        check_bindings([dict(x,path=str(parent/x['path'])) for x in exports])
    check_bindings([a['public_replay'],a['public_independent_replay']])
    r=load(a['public_replay']['path']);q=load(a['public_independent_replay']['path'])
    need(r['status']=='PASS' and r['exact_generated_files']==6 and r['exact_reader_page_texts']==2 and
         len(r['arithmetic']['semantic_controls'])==18 and
         q['status']=='PASS_DISTINCT_NUMERICAL_REVIEW' and q['coordinates']==60 and
         q['exact_fractions']==q['csv_rows']==540 and q['svg_bars']==q['pdf_bars']==12 and
         q['baselines_and_stacking'] and len(q['independent_controls'])==9 and q['primary']==a['primary'],
         'Expanded A/C independent arithmetic and actual plots.')
    covered=[]
    for topic,source,common,apps,printed,raw,count in [('A',213803,49059,87019,54210,52807,7),
                                                    ('C',118433,30437,61248,20933,19937,5)]:
        x=a['primary'][topic]
        need(x['source_sum']==source and x['common_theory']==common and x['applications']==apps and
             x['printed_program_cost']==printed and x['raw_program_alternative']==raw and
             x['original_manuscripts']==count and len(x['individual'])==count,'Complete A/C costs.')
        for kind,den in [('written',common+apps),('including_printed_programs',common+apps+printed),
                         ('including_raw_programs',common+apps+raw)]:
            need(x['whole'][kind]['numerator']==source and x['whole'][kind]['denominator']==den,
                 'Whole enlarged topic denominator.')
        need(x['conditional_acquisition']==dict(full_common=common,full_printed_programs=printed,
             full_raw_programs=raw,printed_and_raw_are_alternatives=True),'Full conditional acquisition.')
        covered.extend(y['source'] for y in x['individual'])
    need(len(set(covered))==12 and sorted(covered)==a['compared_original_ids'],'Unique compared originals.')
    cur=load('audit/corpus/updates/ac-extensions-measurement.json');check_bindings([cur['previous_snapshot']]+cur['added_measurements'])
    old=load(cur['previous_snapshot']['path'])
    need(cur['currently_measured_originals']==32 and cur['measurement_pending_original_ids']==['L040'] and
         set(cur['measured_original_ids'])==set(old['measured_original_ids'])|{'L068','L128'} and
         all(cur[k]==old[k] for k in ['admitted_original_ids','accessible_pending_original_ids','retrieval_original_ids']),
         'Measurement update preserves scientific and retrieval status.')
    cat=load('papers/catalogue_ac_measurement.json');check_bindings([cat['previous_catalogue']]);oldcat=load(cat['previous_catalogue']['path'])
    need(len(cat['entries'])==len(oldcat['entries'])==11,'Expanded measurement catalogue extent.')
    for row,prior in zip(cat['entries'],oldcat['entries']):
        want=dict(prior)
        if row['topic'] in ['A','C']:want.update(measurement_status='admitted',measurement_admission=base+'/admission.json')
        need(row==want,'A/C measurement changes scientific identity.')
    return 540


def check_b5_measurement():
    base='audit/b5-measurement/v1';a=load(base+'/admission.json')
    need(a['status']=='ROOT_ADMITTED_COMPLETE_FIVE_ORIGINAL_TOPIC_MEASUREMENT' and
         a['source_ids']==['L040'] and a['newly_measured_originals']==1 and
         a['original_manuscripts']==5 and a['independent_topics']==1 and
         a['new_principal_credit']==a['new_question_credit']==0 and
         not a['full_formalization_claim'] and a['whole_common_charged'] and
         not a['cross_topic_discount'] and all(x is None for x in a['unknown_costs'].values()),
         'B5 measurement scope.')
    check_bindings(a['artifacts']+a['scientific_admissions']+a['earlier_measurements'])
    for row in a['packets'].values():
        check_bindings([row]);parent=Path(row['path']).parent;exports=load(row['path'])['exports']
        need(len(exports)==row['exports'],'B5 export count.')
        check_bindings([dict(x,path=str(parent/x['path'])) for x in exports])
    check_bindings([a['public_replay'],a['public_independent_replay']])
    r=load(a['public_replay']['path']);q=load(a['public_independent_replay']['path'])
    need(r['status']=='PASS' and r['exact_generated_files']==6 and r['exact_reader_page_texts']==2 and
         len(r['arithmetic']['semantic_controls'])==18 and q['status']=='PASS_DISTINCT_NUMERICAL_REVIEW' and
         q['coordinates']==30 and q['main_fractions']==240 and q['direct_cover_sensitivity_fractions']==120 and
         q['csv_rows']==360 and q['svg_bars']==q['pdf_bars']==6 and
         q['baselines_and_stacking'] and len(q['independent_controls'])==11 and
         q['primary']==a['primary']['B'],'B5 distinct arithmetic and actual plots.')
    x=a['primary']['B'];source=124906;common=42547;apps=76243;printed=13170;raw=12330
    need(x['source_sum']==source and x['common_components']==dict(U_B_previous=14124,U_B_high_rank=28423) and
         x['common_theory']==common and x['applications']==apps and
         x['printed_program_cost']==printed and x['raw_program_alternative']==raw and
         x['original_manuscripts']==len(x['individual'])==5,'Whole B5 costs.')
    for kind,den in [('written',common+apps),('including_printed_programs',common+apps+printed),
                     ('including_raw_programs',common+apps+raw)]:
        need(x['whole'][kind]['numerator']==source and x['whole'][kind]['denominator']==den,'B5 denominator.')
    need(x['conditional_acquisition']==dict(full_common=common,full_printed_programs=printed,
         full_raw_programs=raw,printed_and_raw_are_alternatives=True),'B5 conditional prepayment.')
    need(sorted(y['source'] for y in x['individual'])==a['compared_original_ids']==
         ['L030','L040','N001','N003','N008'],'B5 unique original roster.')
    cur=load('audit/corpus/updates/b5-measurement.json');check_bindings([cur['previous_snapshot']]+cur['added_measurements'])
    old=load(cur['previous_snapshot']['path'])
    need(cur['currently_measured_originals']==33 and cur['measurement_pending_original_ids']==[] and
         set(cur['measured_original_ids'])==set(old['measured_original_ids'])|{'L040'} and
         all(cur[k]==old[k] for k in ['admitted_original_ids','accessible_pending_original_ids','retrieval_original_ids']),
         'B5 measurement preserves scientific programme.')
    cat=load('papers/catalogue_b5_measurement.json');check_bindings([cat['previous_catalogue']]);oldcat=load(cat['previous_catalogue']['path'])
    need(len(cat['entries'])==len(oldcat['entries'])==11,'B5 catalogue extent.')
    for row,prior in zip(cat['entries'],oldcat['entries']):
        want=dict(prior)
        if row['topic']=='B':want.update(measurement_status='admitted',measurement_admission=base+'/admission.json')
        need(row==want,'B5 measurement changes scientific identity.')
    return 360


def check_wreath_recovery():
    base='audit/topic-diagonal/v2';a=load(base+'/admission.json')
    need(a['status']=='ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT' and
         a['source_id']=='N006' and a['topic']=='Diagonal' and a['principal_originals_added']==1 and
         a['source_rows']==27 and a['source_pages']==22 and a['affirmative_sporadic_cases']==10 and
         a['new_question_credit']==0 and not a['whole_source_formalized'] and
         a['compression_factor'] is None and a['measurement_status']=='pending' and
         a['new_common_pages']==8 and a['application_pages']==[8,5,4] and
         a['formal_declarations']==17 and a['reused_formal_declarations']==8 and
         a['new_formal_declarations']==9 and a['source_exceptions_outside_contract']==['Fi22','Fi24prime'] and
         a['charge_full_common_paper'] and a['charge_common_once_within_topic'] and
         not a['cross_topic_overlap_discount'] and a['unknown_retained_proof_cost'] is None,'N006 recovery boundary.')
    check_bindings(a['artifacts'])
    for k in ['author','review','root_adoption','root_primary_replay','public_replay','source_contract',
              'previous_science','previous_measurement','current_common','replaced_common',
              'retained_N007_application','retained_N007_program']:check_bindings([a[k]])
    m=load(a['author']['path']);parent=Path(a['author']['path']).parent
    need(len(m['exports'])==a['author']['exports']==161 and m['source_id']=='N006' and m['originals']==1,
         'N006 export files are not original manuscripts.')
    check_bindings([dict(x,path=str(parent/x['path'])) for x in m['exports']])
    review=load(str(Path(a['review']['path']).parent/'review.json'))
    need(review['status']=='ACCEPTED_COMPLETE_CORRECTED_N006_PRINCIPAL_CONTRACT' and
         not review['findings']['remaining_mathematical_defects'] and
         review['findings']['all_ten_affirmative_cases'] and review['findings']['lamplighter_missing_square_corrected'],
         'Complete corrected N006 distinct review.')
    r=load(a['public_replay']['path']);q=load(a['root_primary_replay']['path'])
    need(r['status']==q['status']=='PASS' and r['bound_exports']==161 and r['scientific_bindings']==32 and
         q['primary_files_verified'] and q['exact_input_bindings']==121 and
         not r['distinct_review']['primary_files_verified'] and
         r['distinct_review']['exact_input_bindings']==118 and
         r['distinct_review']['source_rows']==27 and r['distinct_review']['affirmative_cases']==10 and
         r['distinct_review']['fresh_evidence']['fresh_formal_declarations']==17 and
         len(r['distinct_review']['semantic_controls'])==9 and
         [x['pages'] for x in r['render']]==[8,8,5,4] and
         all(x['per_page_text_identical'] for x in r['render']) and
         not r['expensive_program_replay'] and not r['expensive_formal_replay'],
         'N006 public replay and separately verified primary boundary.')
    contract=load(a['source_contract']['path'])
    need(contract['status']=='ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT' and
         contract['originals']==1 and contract['rows_count']==len(contract['rows'])==27 and
         contract['new_question_credit']==0 and contract['measurement'] is None,'N006 source contract.')
    cur=load('audit/corpus/updates/wreath-products.json');check_bindings([cur['previous_snapshot']]+cur['added_admissions'])
    old=load(cur['previous_snapshot']['path'])
    need(cur['admitted_principal_originals']==34 and cur['accessible_pending_complete_recovery']==70 and
         set(cur['admitted_original_ids'])==set(old['admitted_original_ids'])|{'N006'} and
         set(cur['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'N006'} and
         cur['currently_measured_originals']==33 and cur['measured_original_ids']==old['measured_original_ids'] and
         cur['measurement_pending_original_ids']==['N006'] and cur['retrieval_original_ids']==old['retrieval_original_ids'],
         'N006 one-original admission preserves access and measurement partition.')
    cat=load('papers/catalogue_wreath.json');check_bindings([cat['previous_catalogue']]);prior=load(cat['previous_catalogue']['path'])
    need(cat['entries'][:11]==prior['entries'] and len(cat['entries'])==15 and
         set(cat['original_ids'])==set(prior['original_ids'])|{'N006'} and
         cat['common_supersession']['source_ids']==['N007','N006'] and
         cat['common_supersession']['whole_common_charged_once'],'N006 catalogue and enlarged common acquisition.')
    for x in cat['entries'][11:]:
        need(x['topic']=='Diagonal' and x['measurement_status']=='pending' and
             x['admission']==base+'/admission.json' and (ROOT/x['tex']).is_file() and (ROOT/x['pdf']).is_file(),
             'N006 canonical current manuscript.')
    return 34,70


def check_overview33():
    base = 'audit/overview/v2/'
    a = load(base+'admission.json')
    need(a['status']=='ROOT_ADMITTED_CONSOLIDATED_NUMERICAL_OVERVIEW33',
         'Current overview lacks root admission.')
    check_bindings(a['artifacts']+[a['previous_overview']])
    for key in ['author_manifest','independent_manifest','author_replay','independent_replay']:
        check_bindings([a[key]])
    for key in ['author_manifest','independent_manifest']:
        parent = Path(a[key]['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(a[key]['path'])['exports']])
    spec = importlib.util.spec_from_file_location('overview33_distinct',ROOT/base/'independent_review/check.py')
    checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
    data = load(base+'packet/results.json')
    fractions = checker.arithmetic(data,checker.expected(ROOT))
    bars = checker.graphs(ROOT/base/'packet',data)
    checker.csv_check(ROOT/base/'packet',data)
    need(fractions==a['exact_comparisons']==72 and
         bars==a['actual_SVG_bars']==a['actual_PDF_bars']==127 and
         a['topic_count']==13 and a['distinct_originals']==33 and
         set(a['original_ids'])==set(load('audit/corpus/latest.json')['measured_original_ids']) and
         a['unmeasured_originals']==['N006'] and a['pooled_factor'] is None and
         a['no_cross_topic_common_discount'] and
         all(a[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),
         'Current overview scope changed.')
    need(load(a['independent_replay']['path'])['status']=='PASS_DISTINCT_OVERVIEW33' and
         load(a['author_replay']['path'])['status']=='PASS', 'Current overview replay missing.')
    latest = load('audit/overview/latest.json')
    check_bindings([latest['admission'],latest['reader']])
    need(latest['admission']['path']==base+'admission.json' and
         latest['reader']['path']==base+'packet/summary.pdf' and
         latest['measured_originals']==33 and latest['topics']==13 and
         latest['unmeasured_recovery']==['N006'], 'Current overview pointer changed.')
    return fractions,bars


def check_fischer_answers():
    base = 'answers/fischer-extensions/v1/'
    a = load(base+'admission.json')
    need(a['status']=='ROOT_ADMITTED_TWO_EXPLICIT_POSSIBLE_EXCEPTION_CASES' and
         a['source_original']=='N006' and a['case_answers_admitted']==2 and
         a['new_original_credit']==a['new_numbered_conjectures_claimed']==0 and
         not a['global_conjecture_count_recomputed'] and not a['priority_claim'] and
         not a['full_Lean_verification'] and a['compression_factor'] is None,
         'Fischer answer scope changed.')
    check_bindings(a['artifacts']+[a['cases'],a['known_cases_admission']]+a['packet_manifests'])
    for row in a['packet_manifests']:
        parent = Path(row['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(row['path'])['exports']])
    ledger = load(a['cases']['path'])
    need(ledger['source_id']=='N006' and ledger['case_answers_admitted']==2 and
         ledger['new_numbered_conjectures_claimed']==ledger['new_original_credit']==0 and
         not ledger['priority_claim'] and not ledger['simple_socle_claim'] and
         not ledger['full_Lean_verification'] and not ledger['global_conjecture_count_recomputed'] and
         ledger['compression_factor'] is None and ledger['external_classification_proof_cost'] is None,
         'Fischer ledger overclaims scope.')
    expected = [('Fi22:2',[6,13],[6,6,13]),('Fi24prime:2',[6,35],[6,6,35])]
    need(len(ledger['resolved_cases'])==2,'Fischer case count.')
    for row,(group,polytope,triangle) in zip(ledger['resolved_cases'],expected):
        need(row['group']==group and row['regular_polytope_type']==polytope and
             row['nonlinear_hypertope_triangle']==triangle and row['Lean_declarations']==0,
             'Fischer case geometry changed.')
        check_bindings([row[k] for k in ['proof','source','author_manifest','distinct_review','replay']])
        report = load(row['replay']['path'])
        need(report['status']=='PASS' and report['proper_IP_pairs']==98 and
             report['elementary_full_subset_pairs']==30 and report.get('all_flag_families',report.get('anchored_flag_families'))==6 and
             report['Lean_declarations']==0 and not report['priority_claim'],
             'Fischer distinct replay missing.')
    need(ledger['independent_verification']==dict(markings=4,proper_subset_intersections=196,
         elementary_full_subset_pairs=60,anchored_flag_families=12,author_controls=22,
         distinct_review_scope_controls=16), 'Fischer verification counts changed.')
    return 2


def check_historical_overview33():
    """Run the unchanged historical check against its exact admitted pointers."""
    from types import FunctionType
    current = load('audit/overview/v3/admission.json')
    check_bindings([current['historical33_pointer']])
    original_load = load
    historical_paths = {
        'audit/corpus/latest.json': 'audit/corpus/updates/wreath-products.json',
        'audit/overview/latest.json': 'audit/overview/v2/latest_at_admission.json',
    }
    def historical_load(path):
        return original_load(historical_paths.get(str(path), path))
    context = dict(check_overview33.__globals__, load=historical_load)
    old_check = FunctionType(check_overview33.__code__, context,
                             check_overview33.__name__, check_overview33.__defaults__)
    return old_check()


def check_unified_b_science_and_new_measurements():
    base = 'audit/topic-b/v3/'
    a = load(base+'admission.json')
    need(a['status']=='ROOT_ADMITTED_UNIFIED_B_COMPLETE_CORRECTED_CONTRACTS' and
         a['originals']==['N001','N003','N008','L030','L040'] and
         [a[k] for k in ['source_rows','proof_contexts','transfer_pairs','complete_programs',
                        'reused_partial_Lean_declarations']]==[65,56,18,4,14] and
         a['whole_common_charged_once'] and not a['full_formalization'] and
         all(a[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),
         'Unified B scientific scope changed.')
    check_bindings(a['artifacts']+a['prior_admissions'])
    need(a['author_manifest']['sha256']=='21aeba398dfda4766d3ff441032672ddde2efdac14fef8f67258c971dd827965' and
         a['independent_manifest']['sha256']=='f4199f6f7dc0e6b41e921df1bbb88f71ad2b779e8dc90dcbc450ebf41736c937',
         'Unified B accepted editions changed.')
    for key in ['author_manifest','independent_manifest','public_author_replay','public_distinct_replay']:
        check_bindings([a[key]])
    for key in ['author_manifest','independent_manifest']:
        row=a[key];parent=Path(row['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(row['path'])['exports']])
    m=load(base+'independent_review/mathematical_review.json')
    need(m['status']=='ACCEPTED_FULL_DECLARED_TRANSFER' and
         not m['remaining_mathematical_corrections_requested'] and
         len(m['actual_eliminations'])==5 and len(m['not_eliminated'])==4,
         'Unified B mathematical review missing.')
    own=load(a['public_author_replay']['path']);distinct=load(a['public_distinct_replay']['path'])
    need(own['status']==distinct['status']=='PASS' and own['unchanged_source_rows']==65 and
         len(own['controls'])==8 and len(distinct['semantic_controls'])==11 and
         distinct['inherited_transfer_pairs']==18 and distinct['proof_contexts']==56 and
         distinct['new_Lean_declarations']==0,'Unified B published replays changed.')
    s=load('papers/topic-b/v3/scope.json')
    for node,row in s['proof_contexts'].items():
        text=(ROOT/'papers/topic-b/v3'/row['path']).read_text()
        fragment=text[row['start_codepoint']:row['end_codepoint_exclusive']]
        need(sha256(fragment.encode()).hexdigest()==row['sha256_utf8'],
             'Unified B complete proof context changed: '+node)
    total=0
    for topic,folder,pin,review_pin,nf,nb in [
        ('B','audit/b-unified-measurement/v1/','5b04d4bb4b10cf085bb57a591d91d4e01e0508b4c684bb9b78d1942111095a05','b409816ba7e38fa47669630ac2a59a193438a40cb39d02995587e2d8537e055d',360,15),
        ('Diagonal','audit/diagonal-measurement/v2/','53bfa0d55a9c834014f53a74798cee0b9e65ed1f7a42b184891889362a172fce','cb9f98d5139380a1f32f7d845d50a429f74248933c45f7870fbac5817d92b35e',160,7)]:
        ad=load(folder+'admission.json');check_bindings(ad['artifacts']+ad['scientific_admissions'])
        need(ad['status']=='ROOT_ADMITTED_COMPLETE_TOPIC_NUMERICAL_COMPARISON' and
             ad['topic']==topic and ad['author_manifest']['sha256']==pin and
             ad['independent_manifest']['sha256']==review_pin and ad['exact_fractions']==nf and
             all(ad[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),
             'New complete numerical acceptance changed.')
        for key in ['author_manifest','independent_manifest','public_author_replay','public_distinct_replay']:
            check_bindings([ad[key]])
        spec=importlib.util.spec_from_file_location('new_distinct_'+topic,ROOT/folder/'independent_review/check.py')
        checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
        packet=ROOT/folder/'packet';checker.manifest(packet,pin)
        rows,counts=checker.derive(packet);data=load(folder+'packet/results.json')
        primary=checker.validate(data,rows);checker.csvs(packet,rows,counts)
        svg=checker.svg_rectangles((packet/'costs.svg').read_bytes());pdf,height=checker.pdf_rectangles(packet/'costs.pdf')
        if topic=='B':checker.vectors(svg,pdf,height,primary)
        else:checker.vector_costs(svg,pdf,height,primary)
        need(ad['primary']==primary and len(svg)==len(pdf)==nb and
             load(ad['public_author_replay']['path'])['status']=='PASS' and
             load(ad['public_distinct_replay']['path'])['exact_fractions']==nf,
             'New complete arithmetic or replay changed.')
        total+=nf
    current=load('audit/corpus/latest.json')
    need(current['currently_measured_originals']==34 and current['measurement_pending_original_ids']==[] and
         current['admitted_principal_originals']==34 and current['accessible_pending_complete_recovery']==70 and
         current['pending_source_retrieval']==57,'Current34 partition changed.')
    return total


def check_overview34():
    base='audit/overview/v3/'
    a=load(base+'admission.json')
    check_bindings(a['artifacts']+[a['previous_overview'],a['historical33_pointer']]+a['current_measurement_admissions'])
    for key in ['author_manifest','independent_manifest','author_replay','independent_replay']:
        check_bindings([a[key]])
    for key in ['author_manifest','independent_manifest']:
        parent=Path(a[key]['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(a[key]['path'])['exports']])
    need(a['author_manifest']['sha256']=='cef9498931b3abd646babe4cdbdb8e15ee87cf5a52c25febee7ff9e3239a83e0' and
         a['independent_manifest']['sha256']=='684a41119279ffa79bd36bc2038473d70f9d432637a596de41089b09b1428045',
         'Current34 accepted editions changed.')
    spec=importlib.util.spec_from_file_location('overview34_distinct',ROOT/base/'independent_review/check.py')
    checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
    data=load(base+'packet/results.json');nf=checker.arithmetic(data,checker.expected(ROOT))
    nb=checker.graphs(ROOT/base/'packet',data);checker.csv_check(ROOT/base/'packet',data)
    need(a['status']=='ROOT_ADMITTED_CONSOLIDATED_NUMERICAL_OVERVIEW34' and
         nf==a['exact_comparisons']==72 and nb==a['actual_SVG_bars']==a['actual_PDF_bars']==133 and
         a['topic_count']==13 and a['distinct_originals']==34 and a['unmeasured_originals']==[] and
         set(a['original_ids'])==set(load('audit/corpus/latest.json')['measured_original_ids']) and
         a['pooled_factor'] is None and a['no_cross_topic_common_discount'] and
         all(a[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),
         'Current34 overview accounting changed.')
    need(load(a['independent_replay']['path'])['status']=='PASS_DISTINCT_OVERVIEW34' and
         load(a['author_replay']['path'])['status']=='PASS','Current34 published replays changed.')
    latest=load('audit/overview/latest.json');check_bindings([latest['admission'],latest['reader']])
    need(latest['admission']['path']==base+'admission.json' and
         latest['reader']['path']==base+'packet/summary.pdf' and latest['measured_originals']==34 and
         latest['topics']==13 and latest['unmeasured_recovery']==[],'Current34 overview pointer changed.')
    return nf,nb


def check_nonfirm_hnn_correction():
    base='corrections/nonfirm-hnn/v1/'
    a=load(base+'admission.json')
    need(a['status']=='ROOT_ADMITTED_EXPLICIT_N005_NONFIRM_HNN_CORRECTION' and
         a['source_id']=='N005' and a['edition']=='arXiv:2505.24662v1' and
         a['source_sha256']=='9ac31adc29a5cc66a4b412e0adae7fb47152568db89d1207ee2c34f134ee1427' and
         a['proof_pages']==4 and a['all_written_proofs_reviewed'] and
         a['full_infinite_group_identification_written'] and
         a['finite_programs_role']=='validation only' and
         all(a[k]==0 for k in ['new_original_credit','new_numbered_conjecture_credit','new_formal_credit']) and
         not any(a[k] for k in ['input_firm','input_residually_connected',
              'firm_or_RC_restricted_theorem_refuted','full_Lean_verified',
              'historical_priority_claim','whole_N005_recovered']) and
         a['compression_factor'] is None,'N005 correction scope changed.')
    check_bindings(a['artifacts'])
    for key in ['author_manifest','independent_manifest','author_replay','independent_replay','written_proof']:
        check_bindings([a[key]])
    need(a['author_manifest']['sha256']=='5bff3149addbbb166d729758b7a6c65dd6b97645a5691f72f608838322190d3a' and
         a['independent_manifest']['sha256']=='9da54b35015e0905ed51f7c89967a5955979b26a33df1debf5d11de9807313e3',
         'N005 accepted proof and review editions changed.')
    for key in ['author_manifest','independent_manifest']:
        parent=Path(a[key]['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(a[key]['path'])['exports']])
    q=load(base+'independent_review/review.json')
    need(q['status']=='ROOT_ACCEPTED_LITERAL_N005_NONFIRM_COUNTEREXAMPLE' and
         q['author_manifest_sha256']==a['author_manifest']['sha256'] and
         q['complete_written_proof_accepted'] and q['author_proof_pages_read_and_viewed']==4 and
         q['fresh_author_literal_flags']==1336 and q['fresh_author_controls']==4 and
         q['independent_finite_reconstruction']['product_identities']==729,
         'N005 complete distinct mathematical reading missing.')
    r=load(a['author_replay']['path']);d=load(a['independent_replay']['path'])
    need(r['status']=='PASS' and r['exports']==10 and not r['source_verified'] and
         len(r['finite_validation']['controls']['controls'])==4 and
         d['status']=='PASS_DISTINCT_N005_S4' and d['group_order']==24 and
         d['standard_parabolics']==9 and d['all_parabolic_product_identities']==729 and
         d['pair_intersections']==[1,1,1] and d['triple_intersection']==0 and
         not d['author_program_imported'],'N005 finite validation scope changed.')
    check_bindings([d['log']])
    marker='PASS_N005_S4_DISTINCT:order=24;parabolics=9;product-identities=729;pair-intersections=[1,1,1];triple=0'
    text=(ROOT/d['log']['path']).read_text()
    need(marker in re.sub(r'\s','',text) and 'Error' not in text,'N005 independent replay marker missing.')
    current=load('audit/corpus/latest.json')
    need('N005' in current['accessible_pending_original_ids'] and
         'N005' not in current['admitted_original_ids'],'Correction silently credited as whole-source recovery.')
    return 1



def run_historical34_check(function):
    """Replay an unchanged earlier checker against its exact admitted pointers."""
    import types
    redirects = {
        'audit/corpus/latest.json': 'audit/corpus/updates/before-gluing-and-erratum.json',
        'papers/latest_catalogue.json': 'papers/catalogue_unified_and_orbit.json',
    }
    scope = dict(function.__globals__)
    scope['load'] = lambda p: load(redirects.get(str(p), p))
    preserved = types.FunctionType(function.__code__, scope, function.__name__,
                                   function.__defaults__, function.__closure__)
    return preserved()


def check_gluing_scientific_admission():
    base='audit/topic-gluing/v1/'
    a=load(base+'admission.json')
    check_bindings(a['artifacts']+a['packets'])
    pins=[
      '7e025d845c102f7ab976f60049bb33d15a249ee7a0a776c754d4c9c17bd58e26',
      '636505ba05e2b26c5396d7ff03427b3aa9397bdd40abc55f14dcc0a1d88fbc21',
      '8e2f60d6d5c98679f6e1a863be0d920ec2bf1c51a10ba410dd1a1f76d732e8b8',
      '7e0842741f856bc581e1f24bbdf5938149d92dc71120d96b741f08b5477d8530',
      'd2580bee35571112385023c22da038ae00d5cdeaac0e02eabe9d495c4b73c3ec',
      '45715d640f28ac3663058d946cb41d08f3a41eb716f9dc2fa37384b03fba4ece']
    need([p['sha256'] for p in a['packets']]==pins,'L010 accepted packet editions changed.')
    for p in a['packets']:
        parent=Path(p['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(p['path'])['exports']])
    need(a['status']=='ROOT_ADMITTED_COMPLETE_PRINCIPAL_CONTRACT' and a['source_id']=='L010' and
         a['principal_originals_added']==1 and a['source_pages']==15 and a['source_rows']==23 and
         a['common_pages']==[5,6] and a['application_pages']==[5] and
         a['source_sha256']=='77b983a8367b12849920f4365891d8df39286e4a71329ccea34a20a4bddb5cf8' and
         a['partial_Lean_declarations']==10 and a['new_partial_Lean_declarations']==4 and
         a['reused_partial_Lean_declarations']==6 and a['new_question_credit']==0 and
         not a['whole_source_formalized'] and not a['historical_priority_claim'] and
         a['compression_factor'] is None and a['measurement_status']=='pending' and
         a['charge_full_common_paper'] and a['charge_common_once_within_topic'] and
         not a['cross_topic_overlap_discount'] and a['validation_programs']==3 and
         not a['finite_validation_is_uniform_proof_premise'],'L010 scope changed.')
    source=load('papers/topic-gluing/v1/application/source_map.json')
    rows=source['records'];ids={r['id'] for r in rows}
    need(len(rows)==len(ids)==23 and
         {r['id'] for r in rows if r['status']=='retained_input'}==set(a['retained_inputs'])=={'L010.P2.2','L010.P2.3'} and
         {r['id'] for r in rows if r['status']=='excluded_ancillary'}=={'L010.sequence'} and
         {r['id'] for r in rows if r['status']=='historically_answered'}=={'L010.C4.1.answer','L010.Table6.X'} and
         source['new_question_credit']==0,'L010 source dispositions changed.')
    q=load(base+'complete-review/review.json')
    need(q['status']=='ACCEPTED_PRINCIPAL_RESULTS_WITH_EXPLICIT_RETAINED_INPUTS' and
         len(q['mathematical_checks'])==8 and all(r['verdict']=='ACCEPTED' for r in q['mathematical_checks']) and
         q['render']['all11_pages_visually_read'] and q['render']['per_page_text_identical'] and
         q['formal']['new_fresh_compilation'] and q['formal']['false_weakenings_rejected']==4 and
         not q['formal']['end_to_end'] and q['remaining_mathematical_corrections']==[],
         'L010 complete proof review missing.')
    narrow=load(base+'second-example-review/review.json')
    need(narrow['roles']['argument_author']=='root' and narrow['roles']['reviewer']=='enumeration_review' and
         narrow['reading']['sha256']=='0b7ee9461c37cc85495523159ae0f3ea440080cc6872c5c22cac4e15707ba7ed' and
         narrow['status']=='ACCEPTED_BOUNDED_ROOT_CONTRIBUTION','L010 root contribution lacks distinct review.')
    for name,pages in [('parallel_author_replay',6),('application_author_replay',5)]:
        r=load(base+'complete-review/'+name+'.json')
        need(r['status']=='PASS' and r['render']['pages']==pages and r['render']['per_page_text_equal'],
             'L010 fresh replay/render changed.')
    return 1


def check_programme_with_access_additions():
    need(run_historical34_check(check_current_programme_pointer)==(34,70),
         'Historical34 programme no longer replays.')
    current=load('audit/corpus/latest.json')
    check_bindings([current['snapshot'],current['base_inventory'],current['previous_snapshot']]+
                   current['access_additions']+current['added_admissions'])
    need({k:v for k,v in current.items() if k!='snapshot'}==load(current['snapshot']['path']),
         'Current programme differs from its snapshot.')
    entries=load(current['base_inventory']['path'])['entries']
    originals={r['original_id'] for r in entries}
    old_access={r['original_id'] for r in entries if r['source_access']['accessible']}
    historical={r['original_id'] for r in entries if r['proof']['principal_contract_admitted']}
    access_ids=[]
    for row in current['access_additions']:
        a=load(row['path']);check_bindings(a['artifacts'])
        need(a['status']=='ROOT_ADMITTED_SOURCE_ACCESS_ADDITION' and a['accessible_added_ids']==['L084'] and
             a['source_pages']==2 and a['source_sha256']=='63789bad8fa35c53feee35275bf1f85dd52a54df905c768dd5257240b7f7ddb6' and
             all(a[k]==0 for k in ['new_original_intake','new_principal_credit','new_question_credit']),
             'Source access credited as a mathematical recovery.')
        access_ids.extend(a['accessible_added_ids'])
    need(len(access_ids)==len(set(access_ids)) and not set(access_ids)&old_access and
         set(access_ids)<=originals,'Source addition duplicates or enlarges the intake.')
    accessible=old_access|set(access_ids)
    additions=[load(r['path'])['source_id'] for r in current['added_admissions']]
    need(len(additions)==len(set(additions)) and not set(additions)&historical,'Duplicate recovered original.')
    admitted=historical|set(additions)
    need(set(current['admitted_original_ids'])==admitted and admitted<=accessible and
         set(current['accessible_pending_original_ids'])==accessible-admitted and
         set(current['retrieval_original_ids'])==originals-accessible and
         current['originals']==len(originals)==161 and current['accessible_originals']==len(accessible)==105 and
         current['admitted_principal_originals']==len(admitted)==35 and
         current['accessible_pending_complete_recovery']==len(accessible-admitted)==70 and
         current['pending_source_retrieval']==len(originals-accessible)==56 and
         current['measurement_pending_original_ids']==['L010'] and current['currently_measured_originals']==34 and
         current['all_originals_remain_active'] and not current['all_original_proofs_recovered'] and
         not current['all_conjectures_resolved'],'Current105/35 programme partition changed.')
    q=load('audit/corpus/access/erratum-2006/root_review.json')
    need(q['full_text_read'] and q['pages_viewed']==[1,2] and q['original_distinct_from_2004_article'] and
         not q['mathematical_reproof'] and not q['source_bytes_public'] and q['new_principal_credit']==0,
         'L084 complete source review changed.')
    c=load('papers/latest_catalogue.json');check_bindings([c['previous_catalogue']])
    previous=load(c['previous_catalogue']['path'])
    need(c['entries'][:-3]==previous['entries'] and len(c['entries'])==len(previous['entries'])+3 and
         set(c['original_ids'])==set(additions) and
         {k for r in c['entries'] for k in r['source_contracts']}==set(additions),
         'Latest catalogue loses a recovered original or common paper.')
    for row in c['entries']:
        need((ROOT/row['tex']).is_file() and (ROOT/row['pdf']).is_file(),'Missing current paper.')
    return len(admitted),len(accessible-admitted)



def check_current_programme_after_access_updates():
    """Preserve the earlier edition, then validate the full current partition."""
    import types
    old_function=check_programme_with_access_additions
    scope=dict(old_function.__globals__)
    scope['load']=lambda p: load('audit/corpus/updates/before-halle-preprint.json'
                                  if str(p)=='audit/corpus/latest.json' else p)
    replay=types.FunctionType(old_function.__code__,scope,old_function.__name__,
                              old_function.__defaults__,old_function.__closure__)
    need(replay()==(35,70),'Historical105 programme no longer replays.')
    current=load('audit/corpus/latest.json')
    check_bindings([current['snapshot'],current['base_inventory'],current['previous_snapshot']]+
                   current['access_additions']+current['added_admissions'])
    need({k:v for k,v in current.items() if k!='snapshot'}==load(current['snapshot']['path']),
         'Current programme differs from its admitted snapshot.')
    entries=load(current['base_inventory']['path'])['entries']
    originals={r['original_id'] for r in entries}
    baseline_access={r['original_id'] for r in entries if r['source_access']['accessible']}
    historical={r['original_id'] for r in entries if r['proof']['principal_contract_admitted']}
    newly_accessible=[]
    for row in current['access_additions']:
        a=load(row['path']);check_bindings(a['artifacts'])
        need(a['status']=='ROOT_ADMITTED_SOURCE_ACCESS_ADDITION' and a['source_pages']>0 and
             len(a['source_sha256'])==64 and all(a[k]==0 for k in
             ['new_original_intake','new_principal_credit','new_question_credit']),
             'Access update credited as mathematical recovery.')
        newly_accessible.extend(a['accessible_added_ids'])
    need(len(newly_accessible)==len(set(newly_accessible)) and
         not set(newly_accessible)&baseline_access and set(newly_accessible)<=originals,
         'Access update duplicates or enlarges the fixed intake.')
    accessible=baseline_access|set(newly_accessible)
    additions=[load(r['path'])['source_id'] for r in current['added_admissions']]
    need(len(additions)==len(set(additions)) and not set(additions)&historical,
         'Current recovery duplicates an original.')
    admitted=historical|set(additions)
    need(admitted<=accessible and set(current['admitted_original_ids'])==admitted and
         set(current['accessible_pending_original_ids'])==accessible-admitted and
         set(current['retrieval_original_ids'])==originals-accessible and
         current['originals']==len(originals)==161 and
         current['accessible_originals']==len(accessible) and
         current['admitted_principal_originals']==len(admitted) and
         current['accessible_pending_complete_recovery']==len(accessible-admitted) and
         current['pending_source_retrieval']==len(originals-accessible) and
         current['all_originals_remain_active'],'Current full original partition changed.')
    base='audit/corpus/access/halle-preprint/'
    a=load(base+'admission.json');q=load(base+'root_review.json');t=load(base+'recovery_targets.json')
    need(a['accessible_added_ids']==['L100'] and a['source_pages']==22 and
         a['source_sha256']=='3bd275e4bd344dea8a75fd2c4aeafd69cbe2ca975b3b58933dc7fe4105c5e11e' and
         a['derived_pdf_sha256']=='13f207232f40ca0e00674b9e9de02a91e98226b325ddd428320c661e6131ff84' and
         q['status']=='ACCEPTED_COMPLETE_L100_PREPRINT_SOURCE' and
         q['complete_pages_read']==list(range(1,23)) and q['all22_pages_visually_read'] and
         q['raster_hashes_checked'] and not q['source_extraction_usable'] and
         not q['mathematical_reproof'] and not q['new_numerical_comparison'] and
         q['admitted_principal_originals']==0 and q['new_question_credit']==0 and
         t['status']=='ACCESSIBLE_AWAITING_COMPLETE_RECOVERY' and
         all(r['proof_status']=='pending' for r in t['principal_targets']) and
         t['complexity_ratio'] is None,'L100 edition, source review or pending scope changed.')
    c=load('papers/latest_catalogue.json');check_bindings([c['previous_catalogue']])
    need(set(c['original_ids'])==set(additions) and
         {k for r in c['entries'] for k in r['source_contracts']}==set(additions),
         'Current catalogue loses a recovered original.')
    for row in c['entries']:
        need((ROOT/row['tex']).is_file() and (ROOT/row['pdf']).is_file(),'Missing current manuscript.')
    return len(admitted),len(accessible-admitted)


def check_affine_twist_correction():
    base='corrections/affine-twist/v1/'
    a=load(base+'admission.json')
    need(a['status']=='ROOT_ADMITTED_LITERAL_N005_AFFINE_TWIST_CORRECTION' and
         a['source_id']=='N005' and a['edition']=='arXiv:2505.24662v1' and
         a['source_sha256']=='9ac31adc29a5cc66a4b412e0adae7fb47152568db89d1207ee2c34f134ee1427' and
         a['proof_pages']==3 and a['all_written_proofs_reviewed'] and
         a['uniform_parameters']=='all positive integers' and
         a['exact_source_parabolics_proved'] and a['retained_affine_Coxeter_realization'] and
         a['finite_programs_role']=='validation only' and a['required_finite_premises']==[] and
         all(a[k]==0 for k in ['new_original_credit','new_numbered_conjecture_credit','new_formal_credit']) and
         not any(a[k] for k in ['full_Lean_verified','historical_priority_claim','whole_N005_recovered']) and
         a['compression_factor'] is None,'Affine twist correction scope changed.')
    check_bindings(a['artifacts'])
    for key in ['author_manifest','independent_manifest','author_replay','independent_replay','written_proof']:
        check_bindings([a[key]])
    need(a['author_manifest']['sha256']=='372ef96e589021c9f4eadeddfa55e7e4426b3c490c65ac4f174e73288d035be0' and
         a['independent_manifest']['sha256']=='36cff7ebd18c7a351ddce91298e0c85fbb84112e1a8ca88aa8303206d95a51aa',
         'Affine twist accepted proof or distinct review edition changed.')
    for key in ['author_manifest','independent_manifest']:
        parent=Path(a[key]['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(a[key]['path'])['exports']])
    q=load(base+'independent_review/review.json')
    need(q['status']=='ROOT_ACCEPTED_LITERAL_N005_AFFINE_TWIST_CORRECTION' and
         q['author_manifest_sha256']==a['author_manifest']['sha256'] and
         q['author_proof_pages_read_and_viewed']==3 and q['complete_written_proof_accepted'] and
         q['exact_source_parabolics_proved'] and q['retained_affine_Coxeter_realization'] and
         q['fresh_author_controls']==4 and q['required_finite_premises']==[] and
         len(q['mathematical_review'])==7,'Affine twist complete proof review missing.')
    r=load(a['author_replay']['path']);d=load(a['independent_replay']['path'])
    t=r['reports']['literal']; controls=r['reports']['controls']['controls']
    need(r['status']=='PASS' and r['exports']==13 and not r['source_verified'] and
         r['manifest_sha256']==a['author_manifest']['sha256'] and
         t['status']=='PASS' and t['base_order']==96 and t['outer_order']==8 and
         t['whole_order']==768 and t['actual_base_intersection_orders']==[2,6,1] and
         t['IP_pairs']==64 and t['proper_product_triples']==343 and
         len(controls)==4 and all(c['rejected'] for c in controls),
         'Affine twist author validation changed.')
    need(d['status']=='PASS_DISTINCT_N005_TWIST' and not d['author_program_imported'] and
         d['base_order']==96 and d['diagram_order']==8 and d['whole_order']==768 and
         d['literal_parabolic_orders']==[8,4,12] and d['subgroup_intersection_pairs']==64 and
         d['proper_product_identities']==343 and d['input_residue_order']==8 and
         d['input_child_generated_order']==4,'Affine twist distinct finite reconstruction changed.')
    check_bindings([d['log']])
    marker='PASS_DISTINCT_TWIST:base=96;diagram=8;whole=768;literal=[8,4,12];IP=64;products=343;input-residue=8/4'
    text=(ROOT/d['log']['path']).read_text()
    need(marker in re.sub(r'\s','',text) and 'Error' not in text,'Affine twist distinct replay marker missing.')
    current=load('audit/corpus/latest.json')
    need('N005' in current['accessible_pending_original_ids'] and
         'N005' not in current['admitted_original_ids'],'Example correction credited as whole-source recovery.')
    return 1


def check_historical_overview34():
    """Replay the complete unchanged comparison at its admitted pointers."""
    from types import FunctionType
    base='audit/overview/v4/'
    a=load(base+'admission.json')
    check_bindings([a['historical_corpus_pointer'],a['historical_overview_pointer']])
    pointers={'audit/corpus/latest.json':base+'previous_corpus_pointer.json',
              'audit/overview/latest.json':base+'previous_overview_pointer.json'}
    scope=dict(check_overview34.__globals__,load=lambda path:load(pointers.get(str(path),path)))
    replay=FunctionType(check_overview34.__code__,scope,check_overview34.__name__,
                        check_overview34.__defaults__,check_overview34.__closure__)
    return replay()


def check_gluing_numerical_comparison():
    base='audit/gluing-measurement/v1/'
    a=load(base+'admission.json');check_bindings(a['artifacts']+a['scientific_admissions'])
    need(a['status']=='ROOT_ADMITTED_COMPLETE_TOPIC_NUMERICAL_COMPARISON' and
         a['source_ids']==['L010'] and a['exact_fractions']==120 and a['coordinates']==30 and
         a['whole_common_papers']==['U1','U2'] and a['whole_common_charged_once'] and
         not a['cross_topic_discount'] and a['complete_validation_programs']==3 and
         a['finite_program_premises']==0 and a['partial_Lean_declarations']==10 and
         not a['full_source_formalized'] and not a['complete_proof_step_DAG'] and
         all(a[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),
         'Gluing numerical scope changed.')
    pins={'input_manifest':'7f7cc0dc06b772ca150535d53d0a4d20799255da6e447dffa8e88a25f32d5306',
          'input_review_manifest':'0b82b7ba065bacb6ccfac7515667503617c57ec0db1f810a064dcf23468be9c1',
          'author_manifest':'d52e82dc1b613ae9cb9f43937bc514f7818b3da92a58c3ffd87eccfbb611bc80',
          'independent_manifest':'8239745069c688b960566bbf091e1d7bfce20cb32a92c19b68731340a443387c'}
    for key,pin in pins.items():
        row=a[key];check_bindings([row]);need(row['sha256']==pin,'Gluing accepted edition changed.')
        parent=Path(row['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(row['path'])['exports']])
    spec=importlib.util.spec_from_file_location('gluing_distinct_numbers',ROOT/base/'independent_review/check.py')
    checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
    packet=ROOT/base/'packet';data=load(base+'packet/results.json');recount=load(base+'input_review/recount.json')
    nf=checker.arithmetic(data,recount);need(checker.csvs(packet,data)==360,'Complete Gluing CSV rows.')
    checker.acquisition(packet,data);groups=checker.svg_groups(packet/'costs.svg','cost-')
    rects={k:checker.rect(p[0]) for k,p in groups.items()};primary=data['primary']
    need(checker.bar_geometry(rects,primary['costs'],primary['raw_costs'])==9 and
         checker.compare_pdf_bars(packet,groups,primary['costs'],primary['raw_costs'])==9 and
         checker.document_graph(packet,data)==8 and primary==a['primary'] and nf==120,
         'Gluing complete arithmetic or actual figures changed.')
    for key in ['public_author_replay','public_distinct_replay']:check_bindings([a[key]])
    need(load(a['public_author_replay']['path'])['status']=='PASS_AUTHOR_CHECK_PENDING_DISTINCT_REVIEW' and
         load(a['public_distinct_replay']['path'])['status']=='PASS_DISTINCT_GLUING_NUMERICAL' and
         load(base+'independent_review/review.json')['status']=='ROOT_ACCEPTED_GLUING_NUMERICAL_COMPARISON',
         'Gluing public replay or distinct acceptance missing.')
    catalogue=load('papers/latest_catalogue.json');previous=load('papers/catalogue_gluing.json')
    check_bindings([load('audit/overview/v4/admission.json')['current_catalogue']])
    need(catalogue==load('papers/catalogue_gluing_measured.json') and
         catalogue['entries'][:-3]==previous['entries'][:-3],
         'Gluing measurement catalogue changed older manuscripts.')
    for row,old in zip(catalogue['entries'][-3:],previous['entries'][-3:]):
        want=dict(old,measurement_status='admitted',measurement_admission=base+'admission.json')
        need(row==want,'Gluing measurement changes mathematical identity.')
    return nf


def check_overview35():
    base='audit/overview/v4/';a=load(base+'admission.json')
    check_bindings(a['artifacts']+a['current_measurement_admissions']+[a['previous_overview'],
                   a['historical_corpus_pointer'],a['historical_overview_pointer']])
    for key,pin in [('author_manifest','37ba7781a0f9c99e8cd210e3a72215c20d3ef7cd8640302ef7a2244d871a13bd'),
                    ('independent_manifest','59e80e2346db293abe72f67ad5bfa35d536cf6b0ddf0b6d60899dc5a01c13451')]:
        row=a[key];check_bindings([row]);need(row['sha256']==pin,'Current35 accepted edition changed.')
        parent=Path(row['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(row['path'])['exports']])
    spec=importlib.util.spec_from_file_location('overview35_distinct',ROOT/base/'independent_review/check.py')
    checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
    packet=ROOT/base/'packet';data=load(base+'packet/results.json');old=checker.prior_checker(ROOT)
    need(checker.bindings(packet,ROOT)==8,'All eight overview inputs.')
    nf=checker.arithmetic(data,ROOT,old);nb=checker.graphs(packet,data,old);checker.csv_check(packet,data)
    need(a['status']=='ROOT_ADMITTED_CONSOLIDATED_NUMERICAL_OVERVIEW35' and
         nf==a['exact_comparisons']==76 and nb==a['actual_SVG_bars']==a['actual_PDF_bars']==139 and
         a['topic_count']==14 and a['distinct_originals']==35 and a['unmeasured_originals']==[] and
         set(a['original_ids'])==set(load('audit/corpus/latest.json')['measured_original_ids']) and
         a['pooled_factor'] is None and a['no_cross_topic_common_discount'] and
         all(a[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),
         'Current35 overview scope or accounting changed.')
    for key in ['author_replay','independent_replay']:check_bindings([a[key]])
    need(load(a['author_replay']['path'])['status']=='PASS' and
         load(a['independent_replay']['path'])['status']=='PASS_DISTINCT_OVERVIEW35',
         'Current35 public replays missing.')
    latest=load('audit/overview/latest.json');check_bindings([latest['admission'],latest['reader']])
    need(latest['admission']['path']==base+'admission.json' and latest['reader']['path']==base+'packet/summary.pdf'
         and latest['measured_originals']==35 and latest['topics']==14 and latest['unmeasured_recovery']==[],
         'Current35 overview pointer changed.')
    return nf,nb


def check_l019_bounded_corrections():
    import sys,tempfile
    base='corrections/rank-extension/v1/';a=load(base+'admission.json')
    check_bindings(a['artifacts']+a['packets']+[a['statements']])
    need(a['status']=='ROOT_ADMITTED_TWO_BOUNDED_L019_CORRECTIONS' and
         a['source_id']=='L019' and a['source_edition']=='arXiv:2212.12723v2, 11 January 2023' and
         a['source_sha256']=='e64ed65af04d61964b124f864535477e46f100c4dd2f5f35e612c3bc4c52fff1' and
         a['statement_ids']==['L019.P2.4','L019.T6.4'] and a['complete_written_pages']==5 and
         a['all_computations_validation_only'] and not a['whole_source_formalized'] and
         not a['historical_priority_claim'] and not a['main_stability_theorem_disproved'] and
         not a['transitive_T6_4_disproved'] and a['compression_factor'] is None and
         all(a[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),
         'L019 bounded correction scope changed.')
    pins=['3f1c343fde1a9cbf9a89e9bbb8c4f1006cdc23e5ce40442750fdf50aeff266e7',
          '2805482fe0e80686e532626e86610f40d6318bafd4fb3faefd2dd27a563d4bda',
          '2e182cee7ea5e9148694c8a43244caeebfa1f4bca6993c4dde5cee19bf83ff70',
          '1d81232c2b81bad2571fdaa602ee20e44867dbede25a1f622367ed0c8b1399ea']
    need([p['sha256'] for p in a['packets']]==pins,'L019 accepted editions changed.')
    for row in a['packets']:
        parent=Path(row['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(row['path'])['exports']])
    ledger=load(a['statements']['path'])
    need([r['id'] for r in ledger['statements']]==a['statement_ids'] and
         not ledger['main_stability_theorem_disproved'] and not ledger['transitive_T6_4_disproved'] and
         all(not r['new_open_conjecture_answer'] and not r['full_source_recovery'] for r in ledger['statements']),
         'L019 correction classified as whole recovery or open conjecture.')
    eq=load(base+'endpoint_review/review.json');rq=load(base+'rank_extension_review/review.json')
    need(eq['status']=='ROOT_ACCEPTED_LITERAL_ENDPOINT_CONVERSE_COUNTEREXAMPLE' and
         eq['full_proof_read'] and eq['fresh_proof_pages_viewed']==[1,2] and
         rq['status']=='ROOT_ACCEPTED_LITERAL_INTRANSITIVE_RANK_EXTENSION_COUNTEREXAMPLE' and
         rq['full_written_proof_read'] and rq['fresh_proof_pages_viewed']==[1,2,3] and
         len(rq['mathematical_checks'])==7 and all(r['verdict']=='ACCEPTED' for r in rq['mathematical_checks']),
         'L019 complete written review missing.')
    for folder,label in [('endpoint','endpoint'),('rank_extension','rank')]:
        report=load(base+'public_'+label+'_author.json')
        need(report['status']=='PASS' and len(report['rejected_damaged_examples'])==3,
             'L019 published author checks missing.')
        with tempfile.TemporaryDirectory(prefix='human-compression-l019-') as tmp:
            out=Path(tmp)/'report.json'
            proc=subprocess.run([sys.executable,'-B','-O',str(ROOT/base/(folder+'_review')/'check.py'),
                                 '--packet',str(ROOT/base/folder),'--out',str(out)],
                                capture_output=True,text=True)
            need(proc.returncode==0 and out.is_file(),'L019 distinct finite model failed.')
            fresh=json.loads(out.read_text());need(fresh==load(base+'public_'+label+'_distinct.json'),
                                                 'L019 distinct replay differs.')
    e=load(base+'public_endpoint_distinct.json');r=load(base+'public_rank_distinct.json')
    need((e['old_order'],e['new_order'],e['old_failures'],e['new_failures'])==(4,8,12,0) and
         (r['old_order'],r['new_order'],r['old_intersections'],r['new_intersections'],
          r['old_failures'],r['new_failures'],r['actual_subgroup_formulas'],r['end_intersections'])==
         (480,2880,256,1024,0,72,5,3) and
         r['witness']['left_labels']==[1,2] and r['witness']['right_labels']==[3,4] and
         r['witness']['intersection_order']==2 and r['witness']['common_order']==1 and
         r['alpha_identity'] and r['both_endpoints_moved'],'L019 literal finite witnesses changed.')
    current=load('audit/corpus/latest.json')
    need('L019' in current['accessible_pending_original_ids'] and
         'L019' not in current['admitted_original_ids'] and 'L019' not in current['measured_original_ids'],
         'Bounded L019 corrections credited as whole original.')
    return 2


def check_l019_partial_formal_obstruction():
    base='corrections/rank-extension/formal/v1/';a=load(base+'admission.json')
    check_bindings(a['artifacts']+[a['author_manifest'],a['independent_manifest'],
                   a['written_correction'],a['public_replay']])
    need(a['status']=='ROOT_ADMITTED_PARTIAL_L019_LEAN_OBSTRUCTION' and
         a['source_id']=='L019' and a['new_partial_Lean_declarations']==10 and
         a['actual_generated_subgroups'] and a['kernel_checked_finite_identities'] and
         not a['old_input_C_formalized'] and not a['source_hypotheses_formalized'] and
         not a['full_source_theorem_formalized'] and a['trusted_cached_upstream_oleans'] and
         not a['historical_priority_claim'] and a['new_source_credit']==a['new_question_credit']==0 and
         a['compression_factor'] is None,'Partial L019 formal scope inflated.')
    for key,pin in [('author_manifest','6f18adac317a26aeeec070473c61d4b6f54ee95c55a4976d3a6ddbf823474cae'),
                    ('independent_manifest','f7a647884533e98f18c30ba2f38303affe9a0bb2e8a49c47029b096c900b7825')]:
        row=a[key];need(row['sha256']==pin,'L019 formal accepted edition changed.')
        parent=Path(row['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(row['path'])['exports']])
    review=load(base+'independent_review/review.json');report=load(a['public_replay']['path'])
    need(review['status']=='ROOT_ACCEPTED_PARTIAL_L019_PERMUTATION_OBSTRUCTION' and
         review['complete_Lean_source_read'] and review['all_ten_declarations_freshly_compiled'] and
         review['standard_axioms_only'] and not review['distinct_checker_imports_author'] and
         len(review['rejected_mutations'])==3,'L019 formal review missing.')
    raw=(ROOT/base/'packet/RankExtensionObstruction.lean').read_text()
    need(digest(raw.encode())=='f6aebf8e966c8a25efb533fc7db4c12e746da3c634d30402b1a2608690bc09e7' and
         not re.search(r'\b(sorry|admit|axiom|native_decide)\b',raw),'L019 Lean source changed.')
    logged=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",
                      (ROOT/base/'public_lean.log').read_text(),re.S)
    rows=[dict(declaration=n,axioms=re.findall(r'[A-Za-z][\w.]*',ax)) for n,ax in logged]
    need(report['status']=='PASS_DISTINCT_FRESH_L019_FORMAL' and report['declarations']==10 and
         report['axiom_reports']==rows and len(rows)==10 and
         all(set(r['axioms'])<={'propext','Classical.choice','Quot.sound'} for r in rows) and
         rows[-1]['declaration']=='RankExtensionObstruction.delta_not_C' and
         not report['full_source_theorem_formalized'],'L019 scoped fresh axiom reports missing.')
    pointer=load('corrections/rank-extension/latest.json');check_bindings([pointer['written'],pointer['formal']])
    need(pointer['formal']['path']==base+'admission.json' and pointer['partial_Lean_declarations']==10 and
         not pointer['whole_source_recovered'] and not pointer['main_stability_theorem_disproved'] and
         not pointer['full_source_theorem_formalized'] and pointer['new_question_credit']==0,
         'L019 current correction pointer inflated.')
    return 10


def check_l019_historical_formal_pointer():
    """Keep the earlier scoped formal check at its exact admitted pointer."""
    from types import FunctionType
    base='corrections/rank-extension/transitive/v1/'
    a=load(base+'admission.json');check_bindings([a['previous_pointer']])
    pointers={'corrections/rank-extension/latest.json':base+'previous_pointer.json'}
    scope=dict(check_l019_partial_formal_obstruction.__globals__,
               load=lambda path:load(pointers.get(str(path),path)))
    replay=FunctionType(check_l019_partial_formal_obstruction.__code__,scope,
                        check_l019_partial_formal_obstruction.__name__,
                        check_l019_partial_formal_obstruction.__defaults__,
                        check_l019_partial_formal_obstruction.__closure__)
    return replay()


def check_l019_transitive_correction():
    import sys,tempfile
    base='corrections/rank-extension/transitive/v1/';a=load(base+'admission.json')
    check_bindings(a['artifacts']+a['packets']+[a['previous_pointer']])
    pins=['553e01b6f2d9d9675b6b855339ed5d1985be3bce7451baa075fddb3ca9b06cb2',
          '7c4bffb5cc042d5bf1fbbbe9eae4894093cfc98cbeafa0d40d0e6364a3a7d953',
          'abdb25d913624194ec675dd789a82b5fe7e6aa6ac15e2b2f3601b5820866c060',
          '1d254280500c3128e9ad75c4680225e4e5286c5c0daa212ece05c236425dd37b']
    need([r['sha256'] for r in a['packets']]==pins,'Transitive L019 accepted editions changed.')
    for row in a['packets']:
        parent=Path(row['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(row['path'])['exports']])
    need(a['status']=='ROOT_ADMITTED_TRANSITIVE_L019_CORRECTION_AND_PARTIAL_LEAN' and
         a['source_id']=='L019' and a['statement_id']=='L019.T6.4' and
         a['source_sha256']=='e64ed65af04d61964b124f864535477e46f100c4dd2f5f35e612c3bc4c52fff1' and
         a['complete_written_pages']==4 and a['new_partial_Lean_declarations']==16 and
         a['transitive_input'] and (a['input_rank'],a['input_degree'])==(5,11) and
         a['transitive_T6_4_disproved'] and not a['main_stability_theorem_disproved'] and
         not a['old_input_C_formalized'] and not a['source_hypotheses_formalized'] and
         not a['full_source_theorem_formalized'] and not a['whole_source_recovered'] and
         a['all_finite_computations_validation_only'] and not a['historical_priority_claim'] and
         a['compression_factor'] is None and
         all(a[k]==0 for k in ['new_corrected_statement_credit','new_source_credit','new_question_credit']),
         'Transitive L019 scope inflated.')
    review=load(base+'written_review/review.json')
    need(review['status']=='ROOT_ACCEPTED_TRANSITIVE_COUNTEREXAMPLE_TO_LITERAL_L019_T6_4' and
         review['full_written_proof_read'] and review['fresh_proof_pages_viewed']==[1,2,3,4] and
         len(review['mathematical_checks'])==6 and all(r['verdict']=='ACCEPTED' for r in review['mathematical_checks']),
         'Complete transitive written review missing.')
    author=load(base+'public_author.json')
    need(author['status']=='PASS' and author['original_failures']==0 and author['extended_failures']==96 and
         author['original_intersection_checks']==1024 and author['extended_intersection_checks']==4096 and
         len(author['rejected_damaged_examples'])==4,'Transitive author replay incomplete.')
    with tempfile.TemporaryDirectory(prefix='human-compression-l019-transitive-') as tmp:
        out=Path(tmp)/'report.json'
        proc=subprocess.run([sys.executable,'-B','-O',str(ROOT/base/'written_review/check.py'),
                             '--out',str(out)],capture_output=True,text=True)
        need(proc.returncode==0 and out.is_file(),'Distinct tuple model failed.')
        fresh=json.loads(out.read_text());expected=load(base+'public_distinct.json')
        fresh.pop('elapsed_seconds');expected.pop('elapsed_seconds')
        need(fresh==expected,'Distinct transitive result changed.')
    need(fresh['status']=='PASS' and fresh['computed_proper_pair_intersections']==961 and
         fresh['whole_group_pair_intersections_by_containment']==63 and
         fresh['old_total_intersection_identities']==1024 and fresh['subgroup_formulas']==7 and
         fresh['end_intersections']==6 and fresh['all_literal_split_hypotheses'] and
         fresh['input_transitive'] and fresh['output_failure_labels']==[[2,3],[3,4,5]] and
         fresh['common_labels']==[3] and fresh['witness_intersection_order']==4 and
         fresh['common_label_subgroup_order']==2 and not fresh['source_main_stability_range_satisfied'],
         'Actual transitive witness changed.')
    formal=load(base+'formal_review/review.json');report=load(base+'public_formal.json')
    need(formal['status']=='ROOT_ACCEPTED_PARTIAL_TRANSITIVE_L019_LEAN_OBSTRUCTION' and
         formal['complete_Lean_source_read'] and formal['all_sixteen_declarations_freshly_compiled'] and
         formal['standard_axioms_only'] and not formal['author_checker_imported'] and
         len(formal['rejected_mutations'])==4,'Transitive formal review missing.')
    raw=(ROOT/base/'formal/TransitiveExtensionObstruction.lean').read_text()
    need(digest(raw.encode())=='af42f0159de8b96de73f81b366f31bfa6942876e942ba9ab2fcaae425d032c6e' and
         not re.search(r'\b(sorry|admit|axiom|native_decide)\b',raw),'Transitive Lean source changed.')
    logged=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",
                      (ROOT/base/'public_lean.log').read_text(),re.S)
    rows=[dict(declaration=n,axioms=re.findall(r'[A-Za-z][\w.]*',ax)) for n,ax in logged]
    need(report['status']=='PASS_DISTINCT_FRESH_L019_TRANSITIVE_FORMAL' and report['declarations']==16 and
         report['axiom_reports']==rows and len(rows)==16 and
         all(set(r['axioms'])<={'propext','Classical.choice','Quot.sound'} for r in rows) and
         rows[-1]['declaration']=='TransitiveExtensionObstruction.delta_not_C' and
         not report['full_source_theorem_formalized'],'Transitive fresh axiom reports incomplete.')
    pointer=load('corrections/rank-extension/latest.json')
    check_bindings([pointer['written'],pointer['formal'],pointer['transitive']])
    need(pointer['transitive']['path']==base+'admission.json' and
         pointer['corrected_statements']==['L019.P2.4','L019.T6.4'] and pointer['written_pages']==9 and
         pointer['partial_Lean_declarations']==26 and pointer['transitive_T6_4_disproved'] and
         not pointer['main_stability_theorem_disproved'] and not pointer['whole_source_recovered'] and
         not pointer['full_source_theorem_formalized'] and pointer['new_question_credit']==0,
         'Current L019 statement or formal count inflated.')
    current=load('audit/corpus/latest.json')
    need('L019' in current['accessible_pending_original_ids'] and
         'L019' not in current['admitted_original_ids'],'Transitive correction counted as a recovered original.')
    return 16


def check_restriction_kernel_theory():
    base = 'audit/restriction-kernels/v1/'
    a = load(base + 'admission.json')
    need(a['status'] == 'ROOT_ADMITTED_RESTRICTION_KERNEL_CRITERIA' and
         a['written_pages'] == 5 and a['named_written_results'] == 8 and
         a['partial_Lean_declarations'] == 3 and
         a['new_principal_original_credit'] == a['new_question_credit'] == 0 and
         a['compression_factor'] is None and
         not any(a[k] for k in ['full_string_criteria_formalized',
             'finite_computations_are_uniform_proof_premises', 'historical_priority_claim',
             'whole_L019_recovered', 'main_stability_recovered_or_disproved']),
         'Restriction-kernel theory scope changed.')
    check_bindings(a['artifacts'])
    for key, pin, count in [
        ('author_manifest', '79e1e922dc4da4290d498d516b79f45fa5e5944059d1fd6c728fef806f653b1b', 14),
        ('independent_manifest', 'b21e1cc53451a5057500274411d47d71d63a8c6ebe51e593bf6d088d740f0dc2', 8)]:
        row = a[key]
        check_bindings([row])
        need(row['sha256'] == pin, 'Restriction-kernel reviewed edition changed.')
        manifest = load(row['path'])
        need(len(manifest['exports']) == count, 'Incomplete theory packet.')
        parent = Path(row['path']).parent
        check_bindings([dict(x, path=str(parent / x['path'])) for x in manifest['exports']])
    review = load(base + 'independent_review/review.json')
    replay = load(a['public_replay']['path'])
    need(review['status'] == 'PASS_DISTINCT_ROOT_WRITTEN_AND_SCOPED_FORMAL_REVIEW' and
         review['all_written_proofs_read'] and review['fresh_written_pages_viewed'] == [1, 2, 3, 4, 5],
         'Complete written review missing.')
    need(replay['status'] == 'PASS_DISTINCT_ROOT' and replay['independent_python_subgroups'] == 30 and
         replay['independent_kernel_cases'] == 600 and replay['positive_cases'] == 480 and
         replay['negative_cases'] == 120 and not replay['author_program_imported'] and
         not replay['GAP_used_for_distinct_finite_check'] and replay['standard_axioms_only'] and
         not replay['complete_string_criteria_formalized'], 'Distinct kernel replay changed.')
    scope = load(base + 'author/scope.json')
    need(replay['formal_declarations'] == scope['declarations'] and len(scope['declarations']) == 3,
         'Kernel declaration inventory changed.')
    source = (ROOT / base / 'author/RestrictionKernelCriterion.lean').read_text()
    need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b', source),
         'Unapproved kernel formal trust boundary.')
    original = (ROOT / base / 'author/restriction_kernels.tex').read_text()
    publication = (ROOT / a['tex']['path']).read_text()
    old_date = r'\date{Private theorem development; independent review pending}'
    need(original.count(old_date) == 1 and original.replace(old_date, r'\date{}') == publication,
         'Publication changed beyond the reviewed title date.')
    from pypdf import PdfReader
    def body(path):
        pages = [p.extract_text() for p in PdfReader(ROOT / path).pages]
        return len(pages), re.sub(r'\s+', '', ''.join('\n'.join(t.splitlines()[:-1]) for t in pages))
    old_n, old_text = body(base + 'author/restriction_kernels.pdf')
    new_n, new_text = body(a['paper']['path'])
    banner = re.sub(r'\s+', '', 'Private theorem development; independent review pending')
    need(old_n == new_n == 5 and old_text.replace(banner, '') == new_text,
         'Publication mathematical PDF text changed.')
    return len(scope['declarations'])



def run_historical35_check(function):
    """Keep earlier checks unchanged at their exact pre-Operations pointers."""
    from types import FunctionType
    base='audit/topic-operations/v1/'
    a=load(base+'admission.json')
    check_bindings([a[k] for k in ['historical_corpus_pointer','historical_overview_pointer','historical_catalogue_pointer']])
    routes={'audit/corpus/latest.json':base+'previous_corpus_pointer.json',
            'audit/overview/latest.json':base+'previous_overview_pointer.json',
            'papers/latest_catalogue.json':base+'previous_catalogue.json'}
    scope=dict(function.__globals__,load=lambda path:load(routes.get(str(path),path)))
    return FunctionType(function.__code__,scope,function.__name__,function.__defaults__,function.__closure__)()


def check_operations_science_and_measurement():
    base='audit/topic-operations/v1/';a=load(base+'admission.json')
    check_bindings(a['artifacts']+a['packets'])
    pins={'input_manifest':'3b0d503dcdd3fe778a05213523fa248109b06f6639df31a6ddbc9196cd1b8b03',
          'input_review_manifest':'edb9e44fe49f5cd32ce66a909cef4e0324861d3026d9863417d23417768960d7',
          'numerical_manifest':'c211bfc7a4ae9e0855874aa0584b0f8dfa85c855390e59fa49659b5b517ef978',
          'numerical_review_manifest':'d301b71e5743aa9e5d29a048d6553db644295a6fa4081d5686ab0e42a9f578f5'}
    for key,pin in pins.items():check_bindings([a[key]]);need(a[key]['sha256']==pin,'Operations accepted measurement edition changed.')
    for row in a['packets']:
        parent=Path(row['path']).parent;exports=load(row['path'])['exports']
        if isinstance(exports,dict):exports=[dict(r,path=p) for p,r in exports.items()]
        check_bindings([dict(r,path=str(parent/r['path'])) for r in exports])
    need(a['status']=='ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_AND_NUMERICAL_COMPARISON' and
         a['source_id']=='N005' and a['source_ids']==['N005','N006','N007'] and
         a['principal_originals_added']==1 and a['previously_admitted_source_ids']==['N006','N007'] and
         a['source_rows']=={'N005':81,'N006':27,'N007':32} and a['source_pages']==60 and
         a['source_sha256']=='9ac31adc29a5cc66a4b412e0adae7fb47152568db89d1207ee2c34f134ee1427' and
         a['common_pages']==[21] and a['application_pages']=={'N005':[18],'N006':[8,5,4],'N007':[5]} and
         a['full_program_files']==23 and a['required_program_files']==17 and a['validation_files']==6 and
         a['required_decoders']==2 and a['scientific_documents']==6 and a['scientific_pages']==61 and
         a['partial_Lean_declarations']==17 and a['new_N005_Lean_declarations']==0 and
         a['complete_printed_program_factor'] is None and a['whole_common_charged_once'] and
         not any(a[k] for k in ['whole_source_formalized','historical_priority_claim','source_PDFs_redistributed','cross_topic_overlap_discount']) and
         all(a[k]==0 for k in ['original_intake_added','new_question_credit','new_formal_credit']),
         'Operations scientific or numerical scope changed.')
    migration=load('papers/topic-operations/v1/integrated/source_migration.json')
    need(len(migration['records'])==81 and len({r['source_record']['id'] for r in migration['records']})==81 and
         a['questions']==migration['questions'] and migration['questions'][0]['status']=='NOT_SOLVED_BY_THIS_PACKET' and
         migration['questions'][1]['status']=='NOT_CLAIMED','Operations source or open-question accounting changed.')
    need(load(base+'integrated_review/review.json')['status']=='ROOT_ACCEPTED_COMPLETE_INTEGRATED_EDITION_WITH_DECLARED_SCOPE' and
         load(base+'measurement/independent_review/review.json')['status']=='ROOT_ACCEPTED_COMPLETE_OPERATIONS_NUMBERS',
         'Operations distinct scientific/numerical acceptance missing.')
    replay=load(base+'public_replay.json')
    need(replay['status']=='PASS_PUBLISHED_OPERATIONS_EDITION' and replay['source_recount'] and
         replay['N005_programs_replayed'] and not replay['N006_GAP_and_Lean_repeated'] and
         [r['pages'] for r in replay['rendered_documents']]==[21,18,4,5,8,5,4,2] and
         all(r['whole_page_text_equal'] for r in replay['rendered_documents']),
         'Operations complete public input/program/render replay missing.')
    spec=importlib.util.spec_from_file_location('operations_distinct_numbers',ROOT/base/'measurement/independent_review/check.py')
    q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
    packet=ROOT/base/'measurement/packet';rows,counts=q.derive(packet);data=load(base+'measurement/packet/results.json')
    primary=q.validate(data,rows);q.csvs(packet,rows,counts)
    svg=q.svg_rectangles((packet/'costs.svg').read_bytes());pdf,height=q.pdf_rectangles(packet/'costs.pdf')
    q.vector_costs(svg,pdf,height,primary);q.acquisition_vectors(packet,primary)
    need(primary==a['primary'] and a['exact_fractions']==200 and len(rows)==40,'Operations complete arithmetic changed.')
    return 1,200


def check_programme36():
    base='audit/topic-operations/v1/';a=load(base+'admission.json')
    old=load(base+'previous_corpus_pointer.json');current=load('audit/corpus/latest.json')
    check_bindings([current['snapshot'],current['base_inventory'],current['previous_snapshot']]+
                   current['added_admissions']+current['added_measurements']+current['access_additions'])
    need({k:v for k,v in current.items() if k!='snapshot'}==load(current['snapshot']['path']),
         'Current36 corpus does not match its complete snapshot.')
    expected_admitted=set(old['admitted_original_ids'])|{'N005'}
    need(current['originals']==161 and current['accessible_originals']==106 and current['admitted_principal_originals']==36 and
         current['accessible_pending_complete_recovery']==70 and current['pending_source_retrieval']==55 and
         current['currently_measured_originals']==36 and current['measurement_pending_original_ids']==[] and
         set(current['admitted_original_ids'])==set(current['measured_original_ids'])==expected_admitted and
         set(current['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'N005'} and
         current['retrieval_original_ids']==old['retrieval_original_ids'] and current['access_additions']==old['access_additions'] and
         current['all_originals_remain_active'] and not current['all_conjectures_resolved'] and not current['all_original_proofs_recovered'],
         'Current36 original partition changed.')
    need(current['added_admissions'][:-1]==old['added_admissions'] and
         current['added_admissions'][-1]['path']==base+'admission.json' and
         current['added_measurements']==[r for r in old['added_measurements'] if r['path']!='audit/diagonal-measurement/v2/admission.json']+[current['added_admissions'][-1]],
         'Current36 double-counts an earlier original or loses a comparison.')
    need(check_current_measurement_pointer()==36,'Every admitted original has its current measured comparison.')
    c=load('papers/latest_catalogue.json');prior=load(base+'previous_catalogue.json')
    need(c==load('papers/catalogue_operations_measured.json') and len(c['entries'])==len(prior['entries'])+6 and
         set(c['original_ids'])==set(prior['original_ids'])|{'N005'},'Current Operations catalogue incomplete.')
    for actual,earlier in zip(c['entries'],prior['entries']):
        expected=dict(earlier)
        if earlier['topic']=='Diagonal':expected.update(historical_manuscript_preserved=True,current_edition='papers/topic-operations/v1',current_scientific_admission=base+'admission.json',current_measurement_admission=base+'admission.json')
        need(actual==expected,'Operations catalogue alters an older mathematical edition.')
    for r in c['entries'][-6:]:need(r['topic']=='Operations' and r['measurement_status']=='admitted' and r['measurement_admission']==base+'admission.json' and (ROOT/r['tex']).is_file() and (ROOT/r['pdf']).is_file(),'Missing complete current Operations document.')
    need(c['common_supersession']['current_common']=='papers/topic-operations/v1/integrated/common-theory.pdf' and
         c['common_supersession']['whole_common_charged_once'],'Operations common paper missing from current catalogue.')
    return 36,70



def check_overview36():
    base='audit/overview/v5/';a=load(base+'admission.json')
    check_bindings(a['artifacts']+a['current_measurement_admissions']+[a['previous_overview'],a['current_corpus'],a['current_catalogue'],a['scientific_admission']])
    for key,pin in [('author_manifest','ea43de7db427900f65f06f94c73cbf81414b61910e1fdf760242fe56597a3b1d'),
                    ('independent_manifest','b75678a723dff7b4ebe499ae5fa3c4fbbf4c11f83b900366ce0e700f32e7f560')]:
        row=a[key];check_bindings([row]);need(row['sha256']==pin,'Current36 accepted edition changed.')
        parent=Path(row['path']).parent
        check_bindings([dict(r,path=str(parent/r['path'])) for r in load(row['path'])['exports']])
    spec=importlib.util.spec_from_file_location('overview36_distinct',ROOT/base/'independent_review/check.py')
    q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
    packet=ROOT/base/'packet';data=load(base+'packet/results.json');old=q.prior_checker(ROOT)
    need(q.bindings(packet,ROOT)==10,'All ten current36 numerical inputs.')
    nf=q.arithmetic(data,ROOT,old);nb=q.graphs(packet,data,old);q.csv_check(packet,data)
    need(a['status']=='ROOT_ADMITTED_CONSOLIDATED_NUMERICAL_OVERVIEW36' and
         nf==a['exact_comparisons']==77 and nb==a['actual_SVG_bars']==a['actual_PDF_bars']==142 and
         a['CSV_rows']==50 and a['topic_count']==14 and a['distinct_originals']==36 and
         a['unmeasured_originals']==[] and a['unchanged_topic_records']==13 and
         set(a['original_ids'])==set(load('audit/corpus/latest.json')['measured_original_ids']) and
         a['pooled_factor'] is None and a['no_cross_topic_common_discount'] and
         all(a[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),
         'Current36 overview scope or accounting changed.')
    for key in ['author_replay','independent_replay']:check_bindings([a[key]])
    need(load(a['author_replay']['path'])['status']=='PASS' and
         load(a['independent_replay']['path'])['status']=='PASS_DISTINCT_OVERVIEW36' and
         load(base+'independent_review/review.json')['status']=='ROOT_ACCEPTED_COMPLETE_OVERVIEW36',
         'Current36 complete distinct acceptance/public replay missing.')
    pointer=load('audit/overview/latest.json');check_bindings([pointer['admission'],pointer['reader']])
    need(pointer['admission']['path']==base+'admission.json' and pointer['reader']['path']==base+'packet/summary.pdf' and
         pointer['measured_originals']==36 and pointer['topics']==14 and pointer['unmeasured_recovery']==[],
         'Current36 overview pointer changed.')
    return nf,nb


def check_l020_case_three_correction():
    base = 'corrections/rank-augmentation/v1/'
    admission = load(base + 'admission.json')
    need(admission['status'] == 'ROOT_ADMITTED_L020_CASE_THREE_CORRECTION' and
         admission['source_statement'] == 'L020.Theorem4.1(3)' and
         admission['written_pages'] == 3 and admission['partial_Lean_declarations'] == 13 and
         admission['new_principal_original_credit'] == admission['new_question_credit'] == 0 and
         admission['compression_factor'] is None and
         not any(admission[k] for k in ['whole_source_recovered', 'cases_one_two_decided',
             'high_rank_stability_disproved', 'end_to_end_source_disproof_formalized',
             'historical_priority_claim']), 'L020 correction scope inflated.')
    check_bindings(admission['artifacts'])
    for directory, pin, count in [
        ('written', '95447aed8d01e873306eb55b463b13ab037c709a752ffcb3bcca172c70534bfd', 9),
        ('formal', '0ccc90e1df556584071527d0b1271d26379e60e1a5839133e274ba7013dcf57e', 11),
        ('independent_review', 'a7bff99650e4a219ed2e0d8487e37f3cd8f870c5ad1a143d27fc64172ca14a63', 12)]:
        manifest_path = base + directory + '/manifest.json'
        need(digest((ROOT / manifest_path).read_bytes()) == pin, 'Changed reviewed L020 packet.')
        rows = load(manifest_path)['exports']
        need(len(rows) == count, 'Incomplete L020 packet.')
        check_bindings([dict(r, path=base + directory + '/' + r['path']) for r in rows])
    written = load(base + 'written/scope.json')
    review = load(base + 'independent_review/review.json')
    need(len(written['hypotheses']) == 10 and len(written['proof_contexts']) == 5 and
         review['all_three_written_pages_read'] and review['all_thirteen_formal_declarations_read'] and
         review['source_theorem_pages'] == [5, 6] and review['source_proof_defect_page'] == 16 and
         not review['whole_original_read'], 'Missing exact L020 review scope.')
    fresh = load(base + 'public_replay.json')
    need(fresh == load(base + 'independent_review/distinct_report.json') and
         fresh['status'] == 'PASS_DISTINCT_ROOT' and fresh['old_IP_pairs'] == 64 and
         fresh['old_group_order'] == fresh['last_end_order'] == 6402373705728000 and
         fresh['tree_edges'] == 17 and fresh['middle_group_order'] == 6 and
         fresh['first_end_order'] == fresh['end_intersection_order'] == 48 and
         fresh['exact_disjoint_label_witness'] and not fresh['author_program_imports'] and
         fresh['standard_axioms_only'], 'Distinct L020 computation changed.')
    formal = load(base + 'formal/scope.json')
    need(fresh['formal_declarations'] == formal['declarations'] and len(formal['declarations']) == 13,
         'Actual output formal inventory changed.')
    author_formal = load(base + 'independent_review/formal_author_replay.json')
    need(author_formal['status'] == 'PASS' and len(author_formal['rejected_mutations']) == 4 and
         set(author_formal['actual_permutation_bridge']) == {'a', 'b', 'c', 't'} and
         not author_formal['old_input_C_formalized'] and not author_formal['source_hypotheses_formalized'],
         'Formal bridge or mutation evidence missing.')
    raw = (ROOT / base / 'formal/RankAugmentationObstruction.lean').read_text()
    need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b', raw), 'Changed L020 formal trust boundary.')
    source = (ROOT / base / 'written/case_three.tex').read_text()
    changes = load(base + 'publication_changes.json')['changes']
    need(len(changes) == 2, 'Unexpected publication changes.')
    for change in changes:
        need(source.count(change['old']) == 1, 'Missing reviewed publication anchor.')
        source = source.replace(change['old'], change['new'])
    need(source == (ROOT / base / 'case_three.tex').read_text(), 'Unreviewed mathematical publication edit.')
    edition = load(base + 'publication_edition.json')
    need(edition['status'] == 'PASS_REVIEW_STATUS_ONLY_PUBLICATION_EDITION' and
         edition['pages'] == 3 and edition['mathematical_text_identical_after_recorded_status_changes'] and
         edition['fresh_pages_viewed'] == [1, 2, 3] and not edition['diagnostics'], 'Public render not reviewed.')
    current = load('audit/corpus/latest.json')
    need('L020' in current['accessible_pending_original_ids'] and
         'L020' not in current['admitted_original_ids'], 'Bounded correction counted as a complete original.')
    return 13


def run_historical36_check(function):
    """Earlier checks retain their exact pre-contraction pointers and code."""
    from types import FunctionType
    base = 'audit/topic-rank-contraction/v1/'
    a = load(base + 'admission.json')
    check_bindings([a[k] for k in ['historical_corpus_pointer', 'historical_overview_pointer', 'historical_catalogue_pointer']])
    routes = {'audit/corpus/latest.json': base + 'previous_corpus_pointer.json',
              'audit/overview/latest.json': base + 'previous_overview_pointer.json',
              'papers/latest_catalogue.json': base + 'previous_catalogue.json'}
    scope = dict(function.__globals__, load=lambda path: load(routes.get(str(path), path)))
    original = check_current_measurement_pointer
    scope[original.__name__] = FunctionType(original.__code__, scope, original.__name__, original.__defaults__, original.__closure__)
    return FunctionType(function.__code__, scope, function.__name__, function.__defaults__, function.__closure__)()


def check_rank_contraction_admission():
    base = 'audit/topic-rank-contraction/v1/'
    a = load(base + 'admission.json')
    check_bindings(a['artifacts'] + a['packets'])
    pins = ['79d9cdf2723db2ba8e7729f1333fa918f241265db95e98d5e681b632fe01f489',
            'f0e7e0aa152bc7f71114916d8fbbbdff861e518cea98cba52dea4c454d56ad8f',
            '7eb6e66ff1fdd291624a52ef86f2d54906c8a723aad6f9e6f99fbf9593782330',
            '9e3d09defb11e1a289ea63308608724d7aabea2154777b2d240419c455d73316']
    for row, pin in zip(a['packets'], pins):
        need(row['sha256'] == pin, 'Changed accepted rank-contraction edition.')
        parent = Path(row['path']).parent
        check_bindings([dict(x, path=str(parent / x['path'])) for x in load(row['path'])['exports']])
    need(a['status'] == 'ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_AND_NUMERICAL_COMPARISON' and
         a['source_ids'] == ['L037'] and a['principal_originals_added'] == 1 and
         a['source_rows'] == 22 and a['proof_contexts'] == 20 and
         (a['source_pages'], a['common_pages'], a['application_pages'], a['printed_program_pages']) == (6, 3, 5, 1) and
         a['partial_Lean_declarations'] == 4 and a['full_program_files'] == a['finite_certificate_programs'] == 1 and
         a['uniform_required_programs'] == 0 and a['whole_common_charged_once'] and
         not any(a[k] for k in ['whole_source_formalized', 'cross_topic_overlap_discount', 'old_topic_B_free_premise',
             'source_conjecture_5_1_solved', 'historical_priority_claim', 'source_PDFs_redistributed']) and
         a['new_question_credit'] == a['original_intake_added'] == 0,
         'Rank-contraction scope changed.')
    need(load(base + 'science_review/review.json')['complete_corrected_principal_recovery_accepted'] and
         load(base + 'measurement/independent_review/review.json')['status'] == 'ROOT_ACCEPTED_COMPLETE_L037_NUMBERS',
         'Rank-contraction distinct acceptance missing.')
    fresh = load(base + 'public_science_replay.json')
    need(fresh['status'] == 'PASS' and fresh['lean_declarations'] == 4 and fresh['axioms'] == 'standard only' and
         fresh['matrix_unordered_IP'] == 172 and fresh['A11_unordered_IP'] == 6240 and
         len(fresh['rejected_GAP_mutations']) == 4 and len(fresh['rejected_Lean_weakenings']) == 3 and
         [r['pages'] for r in fresh['render']] == [3, 5, 1] and
         all(r['per_page_text_equal'] for r in fresh['render']) and fresh['full_program_text_included'],
         'Rank-contraction public scientific replay incomplete.')
    need(load(base + 'public_distinct_science.json')['status'] == 'PASS_DISTINCT_PYTHON' and
         load(base + 'public_inputs_replay.json')['pdf_cells'] == 120 and
         load(base + 'public_inputs_replay.json')['raw_cells'] == 30,
         'Rank-contraction independent finite or full input replay missing.')
    spec = importlib.util.spec_from_file_location('rank_contraction_distinct_numbers', ROOT / base / 'measurement/independent_review/check.py')
    q = importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
    packet = ROOT / base / 'measurement/packet'; data = load(base + 'measurement/packet/results.json')
    coords = q.check(packet, data); csvs = q.csvs(packet, coords); vectors = q.vector_rectangles(packet)
    need(data['primary'] == a['primary'] and len(coords) == a['metric_coordinates'] == 30 and
         a['exact_fractions'] == 120 and sum(csvs.values()) == a['CSV_rows'] == 360 and
         vectors['SVG_rectangles'] == vectors['PDF_rectangles'] == a['actual_vector_rectangles_each'] == 9,
         'Rank-contraction complete numeric comparison changed.')
    return 1, 120


def check_programme37():
    base = 'audit/topic-rank-contraction/v1/'
    old = load(base + 'previous_corpus_pointer.json'); current = load('audit/corpus/latest.json')
    check_bindings([current['snapshot'], current['base_inventory'], current['previous_snapshot']] +
                   current['added_admissions'] + current['added_measurements'] + current['access_additions'])
    need({k:v for k,v in current.items() if k != 'snapshot'} == load(current['snapshot']['path']),
         'Current37 pointer differs from complete snapshot.')
    expected = set(old['admitted_original_ids']) | {'L037'}
    need(current['originals'] == 161 and current['accessible_originals'] == 106 and
         current['admitted_principal_originals'] == current['currently_measured_originals'] == 37 and
         current['accessible_pending_complete_recovery'] == 69 and current['pending_source_retrieval'] == 55 and
         set(current['admitted_original_ids']) == set(current['measured_original_ids']) == expected and
         set(current['accessible_pending_original_ids']) == set(old['accessible_pending_original_ids']) - {'L037'} and
         current['retrieval_original_ids'] == old['retrieval_original_ids'] and
         current['access_additions'] == old['access_additions'] and current['measurement_pending_original_ids'] == [] and
         current['all_originals_remain_active'] and not current['all_conjectures_resolved'] and not current['all_original_proofs_recovered'],
         'Current37 original partition changed.')
    need(current['added_admissions'][:-1] == old['added_admissions'] and
         current['added_measurements'][:-1] == old['added_measurements'] and
         current['added_admissions'][-1] == current['added_measurements'][-1] and
         current['added_admissions'][-1]['path'] == base + 'admission.json' and
         check_current_measurement_pointer() == 37, 'Current37 new original or measurement duplicated.')
    c = load('papers/latest_catalogue.json'); prior = load(base + 'previous_catalogue.json')
    need(c == load('papers/catalogue_rank_contraction_measured.json') and
         c['entries'][:-3] == prior['entries'] and set(c['original_ids']) == set(prior['original_ids']) | {'L037'},
         'Current37 catalogue alters or omits an old edition.')
    for row in c['entries'][-3:]:
        need(row['topic'] == 'RankContraction' and row['measurement_status'] == 'admitted' and
             row['measurement_admission'] == base + 'admission.json' and
             (ROOT / row['tex']).is_file() and (ROOT / row['pdf']).is_file(), 'Current37 complete documents missing.')
    return 37, 69


def check_overview37():
    base = 'audit/overview/v6/'
    a = load(base + 'admission.json')
    check_bindings(a['artifacts'] + a['current_measurement_admissions'] +
                   [a[k] for k in ['previous_overview', 'current_corpus', 'current_catalogue', 'scientific_admission']])
    for key, pin in [('author_manifest', 'be15a2ef573f2694fa72eb9b9df77f7644937fbfc16aa6f1842013965dfa4a84'),
                     ('independent_manifest', '0e5a23375a4097ff8156295d6c580fdcda509fcdcc5049be266c5742de7a583f')]:
        row = a[key]; check_bindings([row]); need(row['sha256'] == pin, 'Changed accepted overview37 edition.')
        parent = Path(row['path']).parent
        check_bindings([dict(x, path=str(parent / x['path'])) for x in load(row['path'])['exports']])
    spec = importlib.util.spec_from_file_location('overview37_distinct', ROOT / base / 'independent_review/check.py')
    q = importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
    packet = ROOT / base / 'packet'; data = load(base + 'packet/results.json')
    need(q.bindings(packet, ROOT) == 9, 'Missing complete overview37 input.')
    nf = q.arithmetic(data, ROOT); nb = q.graphs(packet, data, q.prior_checker(ROOT)); q.csv_check(packet, data)
    need(a['status'] == 'ROOT_ADMITTED_CONSOLIDATED_NUMERICAL_OVERVIEW37' and
         nf == a['exact_comparisons'] == 81 and nb == a['actual_SVG_bars'] == a['actual_PDF_bars'] == 147 and
         a['CSV_rows'] == 52 and a['topic_count'] == 15 and a['distinct_originals'] == 37 and
         a['unmeasured_originals'] == [] and a['unchanged_topic_records'] == 14 and
         set(a['original_ids']) == set(load('audit/corpus/latest.json')['measured_original_ids']) and
         a['pooled_factor'] is None and a['no_cross_topic_common_discount'] and
         all(a[k] == 0 for k in ['new_source_credit', 'new_question_credit', 'new_formal_credit']),
         'Overview37 accounting or scope changed.')
    need(load(a['author_replay']['path'])['status'] == 'PASS' and
         load(a['independent_replay']['path'])['status'] == 'PASS_DISTINCT_OVERVIEW37' and
         load(base + 'independent_review/review.json')['status'] == 'ROOT_ACCEPTED_COMPLETE_OVERVIEW37',
         'Overview37 distinct acceptance or public replay missing.')
    pointer = load('audit/overview/latest.json'); check_bindings([pointer['admission'], pointer['reader']])
    need(pointer['admission']['path'] == base + 'admission.json' and pointer['reader']['path'] == base + 'packet/summary.pdf' and
         pointer['measured_originals'] == 37 and pointer['topics'] == 15 and pointer['unmeasured_recovery'] == [],
         'Overview37 current pointer differs.')
    return nf, nb


def run_historical37_check(function):
    """Retain the reviewed thirty-seven-original pointers for earlier checks."""
    from types import FunctionType
    base = 'audit/topic-locally-projective/v1/'
    routes = {'audit/corpus/latest.json': base + 'previous_corpus_pointer.json',
              'audit/overview/latest.json': base + 'previous_overview_pointer.json',
              'papers/latest_catalogue.json': base + 'previous_catalogue.json'}
    rows = {r['path']: r for r in load(base + 'admission.json')['artifacts']}
    check_bindings([rows[p] for p in routes.values()])
    scope = dict(function.__globals__, load=lambda path: load(routes.get(str(path), path)))
    original = check_current_measurement_pointer
    scope[original.__name__] = FunctionType(original.__code__, scope, original.__name__, original.__defaults__, original.__closure__)
    return FunctionType(function.__code__, scope, function.__name__, function.__defaults__, function.__closure__)()


def check_locally_projective_and_mathieu_admissions():
    pins = {
        'locally-projective': ['7bfce9d4a4c0acd3c898d852501550178d5d9a442cccd1603baddb0fdaa1fb85',
            'b7535f010d143e18e13c3eb27acd1d0ac2f7b6a4a83b2ed22e464c85038b52c5',
            '24994f8e6a30131dde603cd4c78b2ad96b369742b795216d932e595a76c066ac',
            '0d548c296855637641592e539c4401895ac38c4c094eaf6f6aa8923f57e058a4',
            '2f9ded604bd5ca6b4b9b882c5b694124eacb653102b9f44e823f04ac731c519a'],
        'mathieu': ['e70770940fe3db852b77a3e400bf913263eec6f1114e89d311f6d4e07b0dad57',
            '50f4c08a990f3d6e43f4544fe5daa8e819649a62f5fbe47f7f89b9b8aa3b463d',
            '13aa42fa08b4a6517945c91c08c51ee3eaec87f572662dad991fe9b519cd6676',
            'dba5b09e539f6149ca16f251c28d1bb5e31354202041e35035e29a0333304f0e',
            'bbef6f90211122f5b5db138bfadd8bb1538bd88f1d6dd7b41dd175e268512de2',
            'e33647116d0bd471cba28eb43448090153f7a6dde8b3e366fbaaa30670a50467',
            '1f7256e911cc3bf0797672e4237a7ef8fe6e6b24cbcca30d13142c82c7dc2d36',
            'b163f3c5bf37ef0406016be81e036c1b7f52a7d5be3245d43f2586081ca88307']}
    for slug, ids in [('locally-projective', ['L084', 'L095']), ('mathieu', ['L073'])]:
        base = 'audit/topic-' + slug + '/v1/'
        a = load(base + 'admission.json')
        check_bindings(a['artifacts'] + a['packets'] + a['public_replays'])
        need([r['sha256'] for r in a['packets']] == pins[slug], 'Changed accepted finite-classification packets.')
        for row in a['packets']:
            parent = Path(row['path']).parent
            check_bindings([dict(r, path=str(parent / r['path'])) for r in load(row['path'])['exports']])
        need(a['status'] == 'ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_AND_NUMERICAL_COMPARISON' and
             a['source_ids'] == ids and a['principal_originals_added'] == len(ids) and
             a['whole_common_charged_once'] and not any(a[k] for k in ['cross_topic_overlap_discount',
                 'sibling_application_free_premise', 'source_PDFs_redistributed', 'whole_source_formalized',
                 'historical_priority_claim']) and
             a['formal_declarations'] == a['new_question_credit'] == a['original_intake_added'] == 0 and
             all(a[k] is None for k in ['retained_external_proof_cost', 'full_runtime_cost',
                 'full_graphics_cost', 'full_formalization_cost']), 'Finite-classification scope or attribution changed.')
        spec = importlib.util.spec_from_file_location('distinct_' + slug.replace('-', '_'),
            ROOT / base / 'measurement/independent_review/check.py')
        q = importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
        packet = ROOT / base / 'measurement/packet'; data = load(base + 'measurement/packet/results.json')
        need(data['primary'] == a['primary'] and a['metric_coordinates'] == 30, 'Changed complete primary comparison.')
        migration = load(base + 'public_migration_replay.json')
        distinct = load(base + 'public_distinct_numeric.json')
        if slug == 'locally-projective':
            rows = q.expected(q.inputs(packet)); primary = q.validate(data, rows)
            sizes = q.csvs(packet, rows); rectangles = q.graphs(packet, primary)
            need(sum(sizes.values()) == a['CSV_rows'] == 510 and a['exact_fractions'] == 150 and
                 rectangles == a['actual_vector_rectangles_each'] == 16, 'Complete locally projective arithmetic.')
            need(load(base + 'science_review/review.json')['status'] == 'PASS_DISTINCT_ROOT_MODULAR_MIGRATION' and
                 load(base + 'erratum_review/review.json')['status'] == 'PASS_DISTINCT_ROOT_REVIEW_COMPLETE_L084_CONTRACT' and
                 load('papers/topic-locally-projective/v1/packet/accepted/L095_root/review.json')['complete_principal_recovery_accepted'] and
                 load(base + 'measurement/independent_review/review.json')['status'] == 'ROOT_ACCEPTED_COMPLETE_LOCALLY_PROJECTIVE_NUMBERS',
                 'Locally projective independent acceptance missing.')
            need((a['source_rows'], a['source_pages'], a['whole_common_pages'], a['application_pages'],
                  a['complete_printed_program_pages'], a['required_program_files'], a['mandatory_data_bytes']) ==
                 (52, [2, 15], 12, [2, 3], 6, 6, 39150) and
                 (a['source_table_rows'], a['corrected_quotient_classes'], a['containment_edges'],
                  a['maximal_quotients'], a['section_regular_quotients']) == (145, 137, 349, 26, 66) and
                 not a['missing_historical_g_txt_used'] and not a['unseen_journal_collated'],
                 'Locally projective complete corrected contract changed.')
            need(migration['status'] == 'AUTHOR_MIGRATION_SCOPE_RENDER_PASS' and
                 migration['migrated_environments'] == dict(byte_identical=15, one_placement_phrase=1,
                     explicit_source_application_restatement=2) and
                 [r['pages'] for r in migration['renders']] == [7, 2, 3, 5, 6] and
                 all(r['diagnostics'] == [] for r in migration['renders']) and
                 not migration['finite_computation_repeated'] and
                 distinct['status'] == 'PASS_DISTINCT_LOCALLY_PROJECTIVE_NUMBERS', 'Locally projective publication replay changed.')
        else:
            inputs = q.inputs(packet); rows = q.derive(inputs); primary = q.validate(data, rows, inputs)
            size = q.csvs(packet, rows, inputs); rectangles = q.vector_check(packet, primary); q.acquisition_graph(packet, primary)
            need(size == a['CSV_rows'] == 640 and a['exact_fractions'] == 120 and
                 rectangles == a['actual_vector_rectangles_each'] == 21, 'Complete Mathieu arithmetic.')
            need(load(base + 'science_review/review.json')['status'] == 'PASS_DISTINCT_ROOT_COMPLETE_CORRECTED_L073' and
                 load(base + 'modular_review/review.json')['status'] == 'PASS_DISTINCT_ROOT_L073_MODULAR_MIGRATION' and
                 load(base + 'measurement/independent_review/review.json')['status'] == 'ROOT_ACCEPTED_COMPLETE_L073_NUMBERS',
                 'Mathieu independent acceptance missing.')
            need((a['source_rows'], a['source_pages'], a['whole_common_pages'], a['application_pages'],
                  a['complete_printed_program_pages'], a['required_program_files'], a['mandatory_data_bytes']) ==
                 (14, [9], 2, [5, 10, 9], 11, 7, 83965) and
                 (a['rank_two_classes'], a['rank_three_classes'], a['source_table_rows']) == (81, 431, 431) and
                 not any(a[k] for k in ['historical_geo_numbering_recovered', 'all_literal_source_labels_valid',
                     'predecessor_counted_as_original']), 'Mathieu exact correction contract changed.')
            need(migration['status'] == 'PASS' and migration['whole_bound_files'] == 44 and
                 migration['complete_application_pages'] == 24 and
                 [r['pages'] for r in migration['render']['documents'].values()] == [2, 5] and
                 all(r['diagnostics'] == [] for r in migration['render']['documents'].values()) and
                 not migration['science_programs_or_Lean_reexecuted'] and distinct['status'] == 'PASS_DISTINCT_L073_NUMBERS',
                 'Mathieu publication replay changed.')
    return 3, 270


def check_programme40():
    base = 'audit/topic-locally-projective/v1/'
    old = load(base + 'previous_corpus_pointer.json'); current = load('audit/corpus/latest.json')
    check_bindings([current['snapshot'], current['base_inventory'], current['previous_snapshot']] +
                   current['added_admissions'] + current['added_measurements'] + current['access_additions'])
    need({k: v for k, v in current.items() if k != 'snapshot'} == load(current['snapshot']['path']),
         'Current40 pointer differs from its complete snapshot.')
    added = {'L073', 'L084', 'L095'}; expected = set(old['admitted_original_ids']) | added
    need(current['originals'] == 161 and current['accessible_originals'] == 106 and
         current['admitted_principal_originals'] == current['currently_measured_originals'] == 40 and
         current['accessible_pending_complete_recovery'] == 66 and current['pending_source_retrieval'] == 55 and
         set(current['admitted_original_ids']) == set(current['measured_original_ids']) == expected and
         set(current['accessible_pending_original_ids']) == set(old['accessible_pending_original_ids']) - added and
         current['retrieval_original_ids'] == old['retrieval_original_ids'] and
         current['access_additions'] == old['access_additions'] and current['measurement_pending_original_ids'] == [] and
         current['all_originals_remain_active'] and not current['all_conjectures_resolved'] and
         not current['all_original_proofs_recovered'], 'Current40 original partition changed.')
    paths = ['audit/topic-locally-projective/v1/admission.json', 'audit/topic-mathieu/v1/admission.json']
    need(current['added_admissions'][:-2] == old['added_admissions'] and
         current['added_measurements'][:-2] == old['added_measurements'] and
         current['added_admissions'][-2:] == current['added_measurements'][-2:] and
         [r['path'] for r in current['added_admissions'][-2:]] == paths and
         check_current_measurement_pointer() == 40, 'Current40 new original or measurement duplicated.')
    c = load('papers/latest_catalogue.json'); prior = load(base + 'previous_catalogue.json')
    need(c == load('papers/catalogue_locally_projective_and_mathieu_measured.json') and
         c['entries'][:-10] == prior['entries'] and set(c['original_ids']) == set(prior['original_ids']) | added,
         'Current40 catalogue alters an old edition.')
    for row in c['entries'][-10:]:
        need(row['topic'] in ['LocallyProjective', 'MathieuCensus'] and row['measurement_status'] == 'admitted' and
             row['measurement_admission'] in paths and (ROOT / row['tex']).is_file() and (ROOT / row['pdf']).is_file(),
             'Current40 complete document missing.')
    return 40, 66


def check_overview40():
    base = 'audit/overview/v7/'
    a = load(base + 'admission.json')
    check_bindings(a['artifacts'] + a['current_measurement_admissions'] + a['scientific_admissions'] +
                   [a[k] for k in ['previous_overview', 'current_corpus', 'current_catalogue']])
    for key, pin in [('author_manifest', '66edf6c8ad5d0b1ce23bc152546beaac6c98c523097fcc12ded1d4543d806cfd'),
                     ('independent_manifest', '0a5c71a7426c89828c087ecdbce26bcd46b6d8f721217cc30addb7fd01569235')]:
        row = a[key]; check_bindings([row]); need(row['sha256'] == pin, 'Changed accepted overview40 edition.')
        parent = Path(row['path']).parent
        check_bindings([dict(r, path=str(parent / r['path'])) for r in load(row['path'])['exports']])
    spec = importlib.util.spec_from_file_location('overview40_distinct', ROOT / base / 'independent_review/check.py')
    q = importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
    packet = ROOT / base / 'packet'; data = load(base + 'packet/results.json')
    need(q.bindings(packet, ROOT) == 14, 'Missing accepted overview40 input.')
    nf = q.arithmetic(data, ROOT); nb = q.graphs(packet, data, q.prior_checker(ROOT)); q.csv_check(packet, data)
    need(a['status'] == 'ROOT_ADMITTED_CONSOLIDATED_NUMERICAL_OVERVIEW40' and
         nf == a['exact_comparisons'] == 90 and nb == a['actual_SVG_bars'] == a['actual_PDF_bars'] == 165 and
         a['CSV_rows'] == 57 and a['topic_count'] == 17 and a['distinct_originals'] == 40 and
         a['unmeasured_originals'] == [] and a['unchanged_topic_records'] == 15 and
         set(a['original_ids']) == set(load('audit/corpus/latest.json')['measured_original_ids']) and
         a['pooled_factor'] is None and a['no_cross_topic_common_discount'] and
         a['mandatory_data_separate_in_both_new_computational_routes'] and
         all(a[k] == 0 for k in ['new_source_credit', 'new_question_credit', 'new_formal_credit']),
         'Overview40 complete accounting or scope changed.')
    need(load(a['author_replay']['path'])['status'] == 'PASS' and
         load(a['independent_replay']['path'])['status'] == 'PASS_DISTINCT_OVERVIEW40' and
         load(base + 'independent_review/review.json')['status'] == 'ROOT_ACCEPTED_COMPLETE_OVERVIEW40',
         'Overview40 acceptance or public replay missing.')
    pointer = load('audit/overview/latest.json'); check_bindings([pointer['admission'], pointer['reader']])
    need(pointer['admission']['path'] == base + 'admission.json' and pointer['reader']['path'] == base + 'packet/summary.pdf' and
         pointer['measured_originals'] == 40 and pointer['topics'] == 17 and pointer['unmeasured_recovery'] == [],
         'Overview40 current pointer differs.')
    return nf, nb


def run_historical40_check(function):
    """Keep forty-original checks bound to their reviewed historical pointers."""
    from types import FunctionType
    base = 'audit/topic-rank-augmentation/v1/'
    routes = {'audit/corpus/latest.json': base + 'previous_corpus_pointer.json',
              'audit/overview/latest.json': base + 'previous_overview_pointer.json',
              'papers/latest_catalogue.json': base + 'previous_catalogue.json'}
    rows = {r['path']: r for r in load(base + 'admission.json')['artifacts']}
    check_bindings([rows[p] for p in routes.values()])
    scope = dict(function.__globals__, load=lambda path: load(routes.get(str(path), path)))
    original = check_current_measurement_pointer
    scope[original.__name__] = FunctionType(original.__code__, scope, original.__name__, original.__defaults__, original.__closure__)
    return FunctionType(function.__code__, scope, function.__name__, function.__defaults__, function.__closure__)()


def check_rank_augmentation_admission():
    base = 'audit/topic-rank-augmentation/v1/'; a = load(base + 'admission.json')
    pins = ['fa57821c117ba7814cf3f652587beb93b0f346d79a37d0e9a91cc76b36c657a0',
            '7432603519e9e854f5044de3349e6b2707685110f889bdfe4e1e249e6e751504',
            '8e9fa6a10c70c244c143df572643b305b4fad14912dd88111da7082189c9db05',
            '8a7a1728b5f6809e77d13f516f682f0f8902c1a26fd44e115c0b48c382194d03',
            'fb6b56fa264b35faec3ac8151023cf5ad083d25e5e9eed0ffce68f5e0ce9e439',
            '32dae3ac7ef573d886c774f513136d7e29ebd3e7e119a9761e6ab7a50e1c1588',
            'b4232452cba25cae64bef0091a4adc947d8f679418fe73f1d439b5966ff587b7',
            '444797a88e089d973c1c9df3e82558903c12326c42843ca62c591e8b7c92c59e']
    check_bindings(a['artifacts'] + a['packets'] + a['public_replays'] + [a['existing_correction']])
    need([r['sha256'] for r in a['packets']] == pins, 'Changed reviewed augmentation editions.')
    for r in a['packets']:
        parent = Path(r['path']).parent
        check_bindings([dict(e, path=str(parent / e['path'])) for e in load(r['path'])['exports']])
    need(a['status'] == 'ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_AND_NUMERICAL_COMPARISON' and
         a['source_ids'] == ['L020'] and a['principal_originals_added'] == 1 and a['source_rows'] == 19 and
         a['source_pages'] == [19] and a['whole_common_pages'] == 5 and a['application_pages'] == [3, 3] and
         a['complete_printed_program_pages'] == 3 and a['declared_program_files'] == 3 and
         a['raw_program_bytes'] == 11533 and a['formal_declarations'] == 15 and
         a['new_formal_declarations'] == 2 and a['previous_obstruction_formal_declarations'] == 13 and
         a['new_question_credit'] == a['original_intake_added'] == 0 and
         a['whole_common_charged_once'] and not any(a[k] for k in ['whole_source_formalized',
             'cross_topic_overlap_discount', 'sibling_application_free_premise', 'earlier_counterproof_free',
             'old_B_common_free', 'old_two_page_appendix_added', 'source_PDFs_redistributed', 'historical_priority_claim']),
         'Augmentation source, proof, formal or cost boundary changed.')
    need(all(a[k] is None for k in ['retained_external_proof_cost', 'full_runtime_cost', 'full_graphics_cost',
                                   'full_formalization_cost']), 'Unknown augmentation costs became zero.')
    science = load(base + 'science_review/review.json'); appendix = load(base + 'program_review/review.json')
    need(science['status'] == 'PASS_DISTINCT_ROOT_CORRECTED_PRINCIPAL_L020' and
         science['complete_source_pages_read_and_viewed'] == 19 and science['complete_corrected_principal_recovery_accepted'] and
         appendix['status'] == 'ACCEPTED_UNCHANGED_COMPLETE_PROGRAM_APPENDIX' and appendix['whole_files'] == 3 and
         appendix['whole_raw_bytes'] == 11533 and appendix['whole_text_printed_exactly_once'],
         'Complete scientific or appendix acceptance missing.')
    need(load(base + 'measurement/input_review/review.json')['status'] == 'ACCEPTED_UNCHANGED_DISTINCT_L020_MEASUREMENT_INPUTS' and
         load(base + 'measurement/independent_review/review.json')['status'] == 'ACCEPTED_UNCHANGED_DISTINCT_L020_NUMBERS',
         'Distinct augmentation extraction/numerical review missing.')
    spec = importlib.util.spec_from_file_location('augmentation_distinct_numbers', ROOT / base / 'measurement/independent_review/check.py')
    q = importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
    packet = ROOT / base / 'measurement/packet'; items = q.inputs(packet); rows = q.derive(items)
    primary = q.validate(load(base + 'measurement/packet/results.json'), rows, items)
    need(primary == a['primary'] and q.csvs(packet, rows, items) == a['CSV_rows'] == 440 and
         q.vector_check(packet, primary) == a['actual_vector_rectangles_each'] == 15 and
         q.acquisition_graph(packet, primary)['edges'] == 8 and a['exact_fractions'] == 120 and
         a['metric_coordinates'] == len(rows) == 30, 'Augmentation arithmetic, vectors or full dependencies changed.')
    fresh = load(base + 'public_science_replay.json'); code = load(base + 'public_program_replay.json')
    need(fresh['status'] == 'PASS' and fresh['source_old_IP_pairs'] == 192 and fresh['new_Lean_declarations'] == 2 and
         fresh['inherited_obstruction_declarations_not_recompiled_here'] == 13 and fresh['axioms'] == 'standard only' and
         len(fresh['rejected_GAP_controls']) == 4 and len(fresh['rejected_Lean_weakenings']) == 3 and
         code['status'] == 'PASS_COMPLETE_PROGRAM_APPENDIX' and code['whole_files'] == code['pages'] == 3 and
         code['per_page_text_equal'] and not code['mathematics_replayed'] and
         load(base + 'public_distinct_numeric.json')['status'] == 'PASS_DISTINCT_L020_NUMBERS',
         'Declared fresh augmentation replays missing.')
    return 1, 120


def check_programme41():
    base = 'audit/topic-rank-augmentation/v1/'; old = load(base + 'previous_corpus_pointer.json')
    current = load('audit/corpus/latest.json')
    check_bindings([current['snapshot'], current['base_inventory'], current['previous_snapshot']] +
                   current['added_admissions'] + current['added_measurements'] + current['access_additions'])
    need({k: v for k, v in current.items() if k != 'snapshot'} == load(current['snapshot']['path']),
         'Current41 pointer differs from its complete snapshot.')
    expected = set(old['admitted_original_ids']) | {'L020'}
    need(current['status'] == 'CURRENT_PROGRAMME_41_ADMITTED_ORIGINALS_106_ACCESSIBLE' and
         current['originals'] == 161 and current['accessible_originals'] == 106 and
         current['admitted_principal_originals'] == current['currently_measured_originals'] == 41 and
         current['accessible_pending_complete_recovery'] == 65 and current['pending_source_retrieval'] == 55 and
         set(current['admitted_original_ids']) == set(current['measured_original_ids']) == expected and
         set(current['accessible_pending_original_ids']) == set(old['accessible_pending_original_ids']) - {'L020'} and
         current['retrieval_original_ids'] == old['retrieval_original_ids'] and current['access_additions'] == old['access_additions'] and
         current['measurement_pending_original_ids'] == [] and current['all_originals_remain_active'] and
         not current['all_conjectures_resolved'] and not current['all_original_proofs_recovered'],
         'Current41 original partition or completion boundary changed.')
    need(current['added_admissions'][:-1] == old['added_admissions'] and
         current['added_measurements'][:-1] == old['added_measurements'] and
         current['added_admissions'][-1] == current['added_measurements'][-1] and
         current['added_admissions'][-1]['path'] == base + 'admission.json' and
         check_current_measurement_pointer() == 41, 'Original or measurement added twice.')
    c = load('papers/latest_catalogue.json'); prior = load(base + 'previous_catalogue.json')
    need(c == load('papers/catalogue_rank_augmentation_measured.json') and c['entries'][:-4] == prior['entries'] and
         set(c['original_ids']) == set(prior['original_ids']) | {'L020'}, 'Current41 catalogue changes an older edition.')
    for row in c['entries'][-4:]:
        need(row['topic'] == 'RankAugmentation' and row['measurement_status'] == 'admitted' and
             row['measurement_admission'] == base + 'admission.json' and (ROOT / row['tex']).is_file() and
             (ROOT / row['pdf']).is_file(), 'Complete augmentation dependency absent.')
    return 41, 65


def check_overview41():
    base = 'audit/overview/v8/'; a = load(base + 'admission.json')
    check_bindings(a['artifacts'] + a['current_measurement_admissions'] +
                   [a[k] for k in ['previous_overview', 'current_corpus', 'current_catalogue', 'scientific_admission']])
    for key, pin in [('author_manifest', '3df08f128c5924f599f58a4299a6934914f56a96a3f27b756b63bd05aa2cff55'),
                     ('independent_manifest', 'd3bb0a8655ad7d4202d2ff7128ed1c9256feb6ae5a1658a468197f3f18c1f19e')]:
        row = a[key]; check_bindings([row]); need(row['sha256'] == pin, 'Changed reviewed overview41 edition.')
        parent = Path(row['path']).parent
        check_bindings([dict(r, path=str(parent / r['path'])) for r in load(row['path'])['exports']])
    spec = importlib.util.spec_from_file_location('overview41_distinct', ROOT / base / 'independent_review/check.py')
    q = importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
    packet = ROOT / base / 'packet'; data = load(base + 'packet/results.json')
    need(q.bindings(packet, ROOT) == 13, 'Missing exact overview41 input.')
    nf = q.arithmetic(data, ROOT); nb = q.graphs(packet, data, q.prior_checker(ROOT)); q.csv_check(packet, data)
    need(a['status'] == 'ROOT_ADMITTED_CONSOLIDATED_NUMERICAL_OVERVIEW41' and nf == a['exact_comparisons'] == 94 and
         nb == a['actual_SVG_bars'] == a['actual_PDF_bars'] == 172 and a['CSV_rows'] == 59 and
         a['topic_count'] == 18 and a['distinct_originals'] == 41 and a['unmeasured_originals'] == [] and
         a['unchanged_topic_records'] == 17 and set(a['original_ids']) == set(load('audit/corpus/latest.json')['measured_original_ids']) and
         a['pooled_factor'] is None and a['no_cross_topic_common_discount'] and a['complete_counterproof_charged'] and
         a['programme_counts_from_separate_snapshot'] and
         all(a[k] == 0 for k in ['new_source_credit', 'new_question_credit', 'new_formal_credit']),
         'Overview41 scope, counts or full cost boundary changed.')
    need(load(a['author_replay']['path'])['status'] == 'PASS' and
         load(a['independent_replay']['path'])['status'] == 'PASS_DISTINCT_OVERVIEW41' and
         load(base + 'independent_review/review.json')['status'] == 'ROOT_ACCEPTED_COMPLETE_OVERVIEW41',
         'Complete overview41 independent acceptance missing.')
    pointer = load('audit/overview/latest.json'); check_bindings([pointer['admission'], pointer['reader'], pointer['counts_source']])
    need(pointer['admission']['path'] == base + 'admission.json' and pointer['reader']['path'] == base + 'packet/summary.pdf' and
         pointer['measured_originals'] == 41 and pointer['topics'] == 18 and pointer['unmeasured_recovery'] == [],
         'Current overview41 pointer differs.')
    return nf, nb



def run_historical41_check(function):
    """Preserve all reviewed forty-one-original checks under their original pointers."""
    from types import FunctionType
    base = 'audit/topic-mixes/v1/'
    routes = {'audit/corpus/latest.json': base + 'previous_corpus_pointer.json',
              'audit/overview/latest.json': base + 'previous_overview_pointer.json',
              'papers/latest_catalogue.json': base + 'previous_catalogue.json'}
    rows = {r['path']: r for r in load(base + 'admission.json')['artifacts']}
    check_bindings([rows[p] for p in routes.values()])
    scope = dict(function.__globals__, load=lambda path: load(routes.get(str(path), path)))
    original = check_current_measurement_pointer
    scope[original.__name__] = FunctionType(original.__code__, scope, original.__name__, original.__defaults__, original.__closure__)
    return FunctionType(function.__code__, scope, function.__name__, function.__defaults__, function.__closure__)()


def check_mixes_admission():
    base = 'audit/topic-mixes/v1/'; a = load(base + 'admission.json')
    pins = ['794ae902e7e06a7eacc7af6da5ed853a39182b8e94efb4695de253902b8c454a',
            '488d97e76d1bc640886f16bf83e65668657aa51a31ff61ce3c5c143ae8e06690',
            'cf6f5e47347a0f905a2f4a566439b3d3562164a5827ef8e7467fa2bb37c28b96',
            '3f02f43dd6e0037cfded61d4b3096b69a8412eeba669ec5714ea1190a24990a8',
            '77597436ddeeadc12ae94c20aa1355b52d51251a48d894192afebb5491775010',
            '280555bfa0f45388bea391b35ef92c44bdaf9f0b22af79fca6dff469a733b7d0',
            '8e0d5c0f1c3212cf96a02361aad84aec5c26b464c8c7c0f98cb1b984dbf28b52']
    check_bindings(a['artifacts'] + a['packets'] + a['public_replays'])
    need([r['sha256'] for r in a['packets']] == pins, 'Changed reviewed Mixes editions.')
    for r in a['packets']:
        parent = Path(r['path']).parent
        check_bindings([dict(e, path=str(parent / e['path'])) for e in load(r['path'])['exports']])
    need(a['status'] == 'ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_AND_NUMERICAL_COMPARISON' and
         a['source_ids'] == ['F005'] and a['principal_originals_added'] == 1 and a['source_rows'] == 38 and
         a['principal_background_rows'] == 35 and a['unanswered_final_problems'] == 3 and
         a['source_pages'] == [21] and a['whole_common_pages'] == 5 and a['application_pages'] == [8, 4] and
         a['complete_printed_program_pages'] == [4, 3] and a['declared_program_files'] == 3 and
         a['required_program_files'] == 1 and a['validation_program_files'] == 2 and
         a['separate_driver_files'] == 3 and a['separate_formal_files'] == 1 and a['formal_declarations'] == 2 and
         a['new_question_credit'] == a['original_intake_added'] == 0 and a['whole_common_charged_once'] and
         not any(a[k] for k in ['whole_source_formalized', 'cross_topic_overlap_discount',
                               'prior_correction_free', 'source_PDFs_redistributed', 'historical_priority_claim']),
         'Mixes source, correction, formal or cost boundary changed.')
    need(all(a[k] is None for k in ['retained_external_proof_cost', 'full_runtime_cost',
                                   'full_graphics_cost', 'full_formalization_cost']), 'Unknown Mixes costs became zero.')
    science = load(base + 'science_review/review.json')
    need(science['status'] == 'ROOT_ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_F005' and
         science['written_recovery_accepted'] and science['corrected_principal_and_background_rows'] == 35 and
         len(science['accepted_literal_counterexample_targets']) == 5 and
         len(science['accepted_qualified_counterexample_targets']) == 2 and
         science['unresolved_literal_correspondence'] == [], 'Complete corrected Mixes scientific acceptance missing.')
    need(load(base + 'measurement/input_review/review.json')['status'] == 'ROOT_ACCEPTED_UNCHANGED_COMPLETE_F005_MEASUREMENT_INPUTS' and
         load(base + 'measurement/review/review.json')['status'] == 'ROOT_ACCEPTED_COMPLETE_F005_NUMERICAL_COMPARISON',
         'Distinct complete Mixes input and numerical reviews missing.')
    spec = importlib.util.spec_from_file_location('mixes_distinct_numbers', ROOT / base / 'measurement/review/check.py')
    q = importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
    packet = ROOT / base / 'measurement/packet'
    counts = load(base + 'measurement/input_review/independent_counts.json')
    rows = q.derive(counts); result = load(base + 'measurement/packet/results.json')
    q.validate(result, rows, counts, load(base + 'measurement/inputs/policy.json'), science)
    need(result['primary'] == a['primary'] and len(rows) == a['metric_coordinates'] == 30 and
         a['exact_fractions'] == a['CSV_rows'] == 120 and
         q.actual_vectors(packet / 'complete_costs.svg', packet / 'complete_costs.pdf', rows[2]) == 14,
         'Complete Mixes arithmetic or actual graph changed.')
    fresh = load(base + 'public_distinct_numbers.json')
    need(fresh['status'] == 'PASS_DISTINCT_F005_NUMERICAL_REVIEW' and len(fresh['independent_controls']) == 15 and
         fresh['actual_SVG_rectangles'] == fresh['actual_PDF_rectangles'] == 14 and
         fresh['author_modules_imported'] is False, 'Distinct public-copy numerical replay missing.')
    return 1, 120


def check_accessible106_programme():
    base = 'audit/corpus/accessible106/'; scope = load(base + 'admission.json')
    check_bindings(scope['artifacts'] + [scope['previous_snapshot']])
    current = load('audit/corpus/latest.json'); previous = load('audit/topic-mixes/v1/previous_corpus_pointer.json')
    check_bindings([current[k] for k in ['snapshot', 'base_inventory', 'previous_snapshot',
                                       'active_catalogue', 'scope_admission', 'scope_archive']] +
                   current['added_admissions'] + current['added_measurements'] + current['access_additions'])
    need({k: v for k, v in current.items() if k != 'snapshot'} == load(current['snapshot']['path']),
         'Current accessible106 pointer differs from snapshot.')
    active = set(previous['admitted_original_ids']) | set(previous['accessible_pending_original_ids'])
    archived = set(previous['retrieval_original_ids']); admitted = set(previous['admitted_original_ids']) | {'F005'}
    need(current['status'] == 'CURRENT_PROGRAMME_42_ADMITTED_OF_106_ACTIVE_ORIGINALS' and
         current['originals'] == current['accessible_originals'] == len(active) == 106 and
         current['historical_originals'] == 161 and current['archived_unavailable_originals'] == len(archived) == 55 and
         set(current['active_original_ids']) == active and set(current['archived_original_ids']) == archived and
         not active & archived and len(active | archived) == 161 and
         current['admitted_principal_originals'] == current['currently_measured_originals'] == len(admitted) == 42 and
         set(current['admitted_original_ids']) == set(current['measured_original_ids']) == admitted and
         current['accessible_pending_complete_recovery'] == 64 and
         set(current['accessible_pending_original_ids']) == active - admitted and
         current['pending_source_retrieval'] == 0 and current['retrieval_original_ids'] == [] and
         current['source_retrieval_in_scope'] is False and current['all_originals_remain_active'] and
         current['all_historical_originals_remain_active'] is False and
         current['measurement_pending_original_ids'] == [] and
         not current['all_original_proofs_recovered'] and not current['all_conjectures_resolved'],
         'User-requested active106 partition or remaining obligations changed.')
    catalogue = load(base + 'catalogue.json'); archive = load(base + 'archived_unavailable.json')
    need(len(catalogue['entries']) == len({e['original_id'] for e in catalogue['entries']}) == 106 and
         {e['original_id'] for e in catalogue['entries']} == active and
         len(archive['entries']) == len({e['original_id'] for e in archive['entries']}) == 55 and
         {e['original_id'] for e in archive['entries']} == archived and
         all(not e['active'] and not e['retrieval_scheduled'] and e['reason'] for e in archive['entries']),
         'Individual active or archived original lost or duplicated.')
    for e in catalogue['entries']:
        need(e['active'] and e['original_count'] == 1 and e['source_access']['accessible'] and
             e['source_access']['usable_representations'] and not e['source_access']['pending_retrieval'],
             'Active original lacks usable source evidence.')
        need((e['current_principal_recovery']['status'] == 'ADMITTED_AND_MEASURED') == (e['original_id'] in admitted),
             'Individual original recovery status differs.')
        check_bindings(e['current_principal_recovery']['latest_admission_references'])
    need(scope['active_originals'] == 106 and scope['archived_originals'] == 55 and
         scope['principal_credit_added'] == scope['question_credit_added'] == scope['measurement_factor_changes'] == scope['singletons_excluded'] == 0,
         'Scope change creates mathematical credit or excludes a singleton.')
    singleton = load(base + 'singleton_topics.json')
    need(singleton['excluded_originals'] == [] and singleton['measured_singleton_topics'] == len(singleton['entries']) == 10 and
         all(e['exclusion_applied'] is False for e in singleton['entries']), 'Unapproved singleton exclusion.')
    old_catalogue = load('audit/topic-mixes/v1/previous_catalogue.json')
    new_catalogue = load('papers/latest_catalogue.json')
    need(new_catalogue == load('papers/catalogue_accessible106.json') and
         new_catalogue['entries'][:-5] == old_catalogue['entries'] and
         new_catalogue['active_originals'] == 106 and
         set(new_catalogue['original_ids']) == set(old_catalogue['original_ids']) | {'F005'} and
         check_current_measurement_pointer() == 42, 'Catalogue changes older proofs or double-counts original.')
    for row in new_catalogue['entries'][-5:]:
        need(row['topic'] == 'Mixes' and row['measurement_status'] == 'admitted' and
             (ROOT / row['tex']).is_file() and (ROOT / row['pdf']).is_file(), 'Complete Mixes paper missing.')
    return 42, 64



def check_accessible106_independent_review():
    base = 'audit/corpus/accessible106/'; a = load(base + 'review_admission.json')
    check_bindings(a['artifacts'] + [a['scope_admission'], a['independent_manifest'], a['public_replay']])
    need(a['independent_manifest']['sha256'] == '10211d9436896d92cb4c2e4406817ec6d2fc32bd1e409cae57f42cb2a505c5f4',
         'Changed independently reviewed scope edition.')
    parent = Path(a['independent_manifest']['path']).parent
    check_bindings([dict(r, path=str(parent / r['path'])) for r in load(a['independent_manifest']['path'])['exports']])
    review = load(base + 'independent_review/review.json'); replay = load(base + 'public_review_replay.json')
    check_bindings([review['catalogue'], review['scope_admission']])
    need(review['status'] == 'INDEPENDENTLY_ACCEPTED_ACCESSIBLE_106_SCOPE' and
         review['verified']['source_bindings'] == 112 and review['verified']['post_baseline_contracts'] == 15 and
         review['verified']['canonical_baseline_contracts'] == 27 and
         review['verified']['current_application_route_records'] == 25 and review['semantic_controls_rejected'] == 18 and
         review['remaining_required_scope_corrections'] == [] and
         replay['status'] == 'PASS' and len(replay['semantic_controls_rejected']) == 18 and
         replay['counts'] == dict(active=106, archive=55, admitted_and_measured=42, pending=64,
                                 new_contract_routes=15, singletons_retained=10),
         'Independent scope review or exact source/contract partition missing.')
    return 106, 55


def check_overview42():
    base = 'audit/overview/v9/'; a = load(base + 'admission.json')
    check_bindings(a['artifacts'] + a['current_measurement_admissions'] +
                   [a[k] for k in ['previous_overview', 'current_corpus', 'current_catalogue',
                                   'scientific_admission', 'scope_admission', 'scope_review_admission']])
    for key, pin in [('author_manifest', 'd1959483e7df6e257aaadebf2548b7e73817fc0cb69a3924b068a497284154e3'),
                     ('independent_manifest', '9c75a6c9323468c64257ee9137bb73d11e6d3738df7f7ab3dfd705afc8910a6b')]:
        row = a[key]; check_bindings([row]); need(row['sha256'] == pin, 'Changed reviewed overview42 edition.')
        parent = Path(row['path']).parent
        check_bindings([dict(r, path=str(parent / r['path'])) for r in load(row['path'])['exports']])
    spec = importlib.util.spec_from_file_location('overview42_distinct', ROOT / base / 'independent_review/check.py')
    q = importlib.util.module_from_spec(spec); spec.loader.exec_module(q)
    packet = ROOT / base / 'packet'; data = load(base + 'packet/results.json')
    need(q.bindings(packet, ROOT) == 14, 'Missing exact overview42 input.')
    nf = q.arithmetic(data, ROOT); nb = q.graphs(packet, data, q.prior_checker(ROOT)); q.csv_check(packet, data)
    need(a['status'] == 'ROOT_ADMITTED_CONSOLIDATED_NUMERICAL_OVERVIEW42' and nf == a['exact_comparisons'] == 98 and
         nb == a['actual_SVG_bars'] == a['actual_PDF_bars'] == 179 and a['CSV_rows'] == 61 and
         a['topic_count'] == 19 and a['distinct_originals'] == 42 and a['unmeasured_originals'] == [] and
         a['active_catalogue_originals'] == 106 and a['archived_unavailable_originals'] == 55 and
         a['unchanged_topic_records'] == 18 and
         set(a['original_ids']) == set(load('audit/corpus/latest.json')['measured_original_ids']) and
         a['pooled_factor'] is None and a['no_cross_topic_common_discount'] and
         a['complete_exceptional_application_charged'] and a['programme_counts_from_separate_snapshot'] and
         all(a[k] == 0 for k in ['new_source_credit', 'new_question_credit', 'new_formal_credit']),
         'Overview42 scope, counts or complete costs changed.')
    replay = load(a['author_replay']['path']); distinct = load(a['independent_replay']['path'])
    need(replay['status'] == 'PASS' and len(replay['exact_rebuilt_outputs']) == 12 and replay['reader_pages'] == 6 and
         distinct['status'] == 'PASS_DISTINCT_OVERVIEW42' and len(distinct['controls_rejected']) == 15 and
         load(base + 'independent_review/review.json')['status'] == 'ROOT_ACCEPTED_COMPLETE_OVERVIEW42',
         'Overview42 independent acceptance or fresh replay missing.')
    pointer = load('audit/overview/latest.json'); check_bindings([pointer['admission'], pointer['reader'], pointer['counts_source']])
    need(pointer['admission']['path'] == base + 'admission.json' and pointer['reader']['path'] == base + 'packet/summary.pdf' and
         pointer['measured_originals'] == 42 and pointer['topics'] == 19 and pointer['unmeasured_recovery'] == [] and
         pointer['active_catalogue_originals'] == 106 and pointer['archived_unavailable_originals'] == 55,
         'Current overview42 pointer differs.')
    return nf, nb


def check_symmetric_measurement_policy():
    base = 'audit/measurement_policy/v1/'
    policy = load(base + 'policy.json')
    check_bindings([policy[k] for k in ['previous_overview', 'previous_topic_table',
                                      'written_table', 'replacement_cost_inventory']])
    old = list(csv.DictReader((ROOT / policy['previous_topic_table']['path']).open()))
    written = list(csv.DictReader((ROOT / policy['written_table']['path']).open()))
    costs = list(csv.DictReader((ROOT / policy['replacement_cost_inventory']['path']).open()))
    fields = ['topic', 'title', 'originals', 'representation', 'sources', 'common',
              'applications', 'written', 'written_factor']
    need(written == [{k: r[k] for k in fields} for r in old] and
         len(written) == len(costs) == 19 and sum(int(r['originals']) for r in written) == 42,
         'Symmetry correction changes the established manuscript comparisons.')
    for original, row in zip(old, costs):
        need(all(row[k] == original[k] for k in ['topic', 'printed_programs', 'raw_programs', 'mandatory_data']) and
             row['original_program_cost'] == row['symmetric_program_inclusive_factor'] == 'unknown' and
             row['additional_optional_validation_printed'] == ('5173' if row['topic'] == 'E' else ''),
             'Symmetry correction drops a cost or invents source software costs.')
    current = policy['current_measurement']
    need(policy['status'] == 'CURRENT_SYMMETRIC_MEASUREMENT_POLICY' and
         current['retained_written_values_unchanged'] and
         current['symmetric_validation_inclusive_factors'] is None and
         current['all_embedded_validation_listings_screened'] is False and
         current['pooled_factor'] is None and current['active_originals'] == 106 and
         current['pending_originals'] == 64 and
         set(current['withdrawn_fields']) == {'printed_factor', 'raw_factor', 'including_optional_validation'} and
         all(current[k] == 0 for k in ['new_original_credit', 'new_question_credit', 'new_formal_credit']),
         'Symmetric measurement policy invents credit or a complete source software inventory.')
    manifest = load(base + 'review/manifest.json')
    check_bindings([dict(r, path=base + 'review/' + r['path']) for r in manifest['exports']])
    review = load(base + 'review/review.json')
    need(review['new_credits'] == 0 and review['expanded_F']['symmetric_program_inclusive_ratio'] is None and
         review['expanded_F']['source_validation_cost'] is None and review['role_disclosure'],
         'Bounded audit loses its unknown source cost or reviewer role disclosure.')
    pointer = load('audit/overview/latest.json')
    check_bindings([pointer['measurement_policy'], pointer['measurement_policy_reader']])
    need(pointer['measurement_policy']['path'] == base + 'policy.json' and
         pointer['software_inclusive_factors_status'] == 'WITHDRAWN_AS_ASYMMETRIC' and
         pointer['written_factors_status'] == 'UNCHANGED_MANUSCRIPT_LENGTHS',
         'Current overview does not expose the measurement correction.')
    return len(written)


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
    a_cells, a_fractions = check_topic_a_measurement()
    check_topic_dag()
    a_dag_cells = check_topic_a_dag()
    b_clauses, b_declarations = check_topic_b_proofs()
    b_cells, b_fractions = check_topic_b_measurement()
    b_dag_cells = check_topic_b_dag()
    c_rows, c_declarations = check_topic_c_proofs()
    c_cells, c_fractions = check_topic_c_measurement()
    c_dag_cells, c_closures = check_topic_c_dag()
    d_rows, d_declarations = check_topic_d_proofs()
    d_support_declarations = check_topic_d_support_formal()
    d_cells, d_fractions = check_topic_d_measurement()
    d_dag_cells, d_closures = check_topic_d_dag()
    affine_rows, affine_declarations = check_affine_proofs()
    affine_cells, affine_fractions = check_affine_measurement()
    affine_dag_cells, affine_routes = check_affine_dag()
    f_rows, f_declarations = check_topic_f_proofs()
    f_cells, f_fractions = check_topic_f_measurement()
    g_rows, g_declarations = check_topic_g_proofs()
    g_cells, g_fractions = check_topic_g_measurement()
    representation_rows, representation_declarations = check_representation_proofs()
    representation_cells, representation_fractions = check_representation_measurement()
    chamber_rows, chamber_declarations = check_chamber_proofs()
    chamber_cells, chamber_fractions = check_chamber_measurement()
    available_text_fractions = check_available_text_comparisons()
    corpus_originals, corpus_accessible, corpus_pending, corpus_retrieval = check_complete_corpus_programme()
    current_admitted, current_pending = check_additional_original_recoveries()
    overview_fractions, overview_svg, overview_pdf = check_consolidated_measurement_overview()
    latest_admitted, latest_pending = check_diagonal_admission_and_latest_programme()
    graph_admitted, graph_pending = check_graph_application_extensions()
    extra_measure_fractions = check_two_additional_measurements()
    high_rank_admitted, high_rank_pending = check_high_rank_symmetric_extension()
    diagonal_fractions = check_diagonal_measurement()
    ac_extension_fractions = check_ac_extension_measurements()
    b5_fractions = check_b5_measurement()
    wreath_admitted, wreath_pending = check_wreath_recovery()
    overview33_fractions, overview33_bars = check_historical_overview33()
    unified_fractions = run_historical34_check(check_unified_b_science_and_new_measurements)
    overview34_fractions, overview34_bars = check_historical_overview34()
    gluing_fractions = run_historical35_check(check_gluing_numerical_comparison)
    overview35_fractions, overview35_bars = run_historical35_check(check_overview35)
    print(f"PASS: historical fourteen-topic overview has {overview35_fractions} exact comparisons and {overview35_bars} actual bars per format for 35 originals; Gluing preserves {gluing_fractions} fractions.")
    fischer_cases = check_fischer_answers()
    nonfirm_corrections = run_historical35_check(check_nonfirm_hnn_correction)
    twist_corrections = run_historical35_check(check_affine_twist_correction)
    l019_corrections = check_l019_bounded_corrections()
    l019_formal = check_l019_historical_formal_pointer()
    l019_transitive = check_l019_transitive_correction()
    restriction_kernel_declarations = check_restriction_kernel_theory()
    l020_formal = run_historical40_check(check_l020_case_three_correction)
    print(f"PASS: historical L020 case(3) correction preserves its complete counterexample and {l020_formal} scoped Lean declarations.")
    print(f"PASS: complete restriction-kernel criteria and {restriction_kernel_declarations} generic Lean lemmas; no additional original, question or compression credit.")
    print(f"PASS: transitive L019 counterexample has a complete written input proof and {l019_transitive} fresh scoped Lean declarations; main stability and whole-source recovery remain separate.")
    print(f"PASS: {l019_formal} fresh scoped Lean declarations verify the actual rank-extension output obstruction; input C-property and source hypotheses remain written.")
    print(f"PASS: {l019_corrections} bounded L019 corrections have complete written proofs and independent finite models; full source and main stability remain separate.")
    active_measured = check_current_measurement_pointer()
    gluing_added = check_gluing_scientific_admission()
    historical_admitted, historical_pending = run_historical35_check(check_current_programme_after_access_updates)
    operations_added, operations_fractions = check_operations_science_and_measurement()
    run_historical36_check(check_programme36)
    overview36_fractions, overview36_bars = run_historical36_check(check_overview36)
    contraction_added, contraction_fractions = check_rank_contraction_admission()
    run_historical37_check(check_programme37)
    overview37_fractions, overview37_bars = run_historical37_check(check_overview37)
    finite_added, finite_fractions = check_locally_projective_and_mathieu_admissions()
    run_historical40_check(check_programme40)
    overview40_fractions, overview40_bars = run_historical40_check(check_overview40)
    augmentation_added, augmentation_fractions = check_rank_augmentation_admission()
    run_historical41_check(check_programme41)
    overview41_fractions, overview41_bars = run_historical41_check(check_overview41)
    mixes_added, mixes_fractions = check_mixes_admission()
    active_admitted, active_pending = check_accessible106_programme()
    check_accessible106_independent_review()
    overview42_fractions, overview42_bars = check_overview42()
    symmetric_topics = check_symmetric_measurement_policy()
    policy_review_binding = load('audit/overview/latest.json')['measurement_policy_review']
    check_bindings([policy_review_binding])
    policy_review = load(policy_review_binding['path'])
    need(policy_review['status'] == 'ACCEPTED_FINAL_SYMMETRIC_POLICY_PRESENTATION' and
         len(policy_review['files']) == 4 and policy_review['role_disclosure'],
         'Final bounded policy review missing.')
    check_bindings([dict(r, path='audit/measurement_policy/v1/' + Path(r['path']).name)
                    for r in policy_review['files']])
    need(digest((ROOT / 'audit/measurement_policy/v1/review/manifest.json').read_bytes()) ==
         policy_review['prior_frozen_review']['sha256'], 'Bounded policy audit changed.')
    print(f"PASS: {symmetric_topics} unchanged manuscript comparisons; asymmetric software-inclusive factors withdrawn, source software costs remain unknown.")
    print(f"PASS: active106 catalogue, 55 archived, 42 admitted/measured and 64 pending; no singleton exclusions.")
    print(f"PASS: nineteen-topic overview has {overview42_fractions} exact comparisons and {overview42_bars} actual bars per format; Mixes adds one corrected principal recovery.")
    print(f"PASS: historical eighteen-topic overview: {overview41_fractions} exact comparisons and {overview41_bars} actual vector bars per format for 41 originals.")
    print(f"PASS: augmentation adds {augmentation_added} corrected principal original and {augmentation_fractions} exact comparisons; all six local pages paid.")
    print(f"PASS: historical seventeen-topic overview: {overview40_fractions} exact comparisons and {overview40_bars} actual vector bars per format for 40 originals.")
    print(f"PASS: locally projective and Mathieu topics add {finite_added} originals and {finite_fractions} exact comparisons; 40 measured originals, no new formal or question credit.")
    print(f"PASS: historical fifteen-topic overview: {overview37_fractions} exact comparisons and {overview37_bars} actual vector bars per format for 37 originals.")
    print(f"PASS: rank contraction adds {contraction_added} original and {contraction_fractions} exact comparisons, with four scoped Lean lemmas.")
    print(f"PASS: historical fourteen-topic overview: {overview36_fractions} exact comparisons and {overview36_bars} bars per format for36 originals.")
    print(f"PASS: Operations adds {operations_added} original with {operations_fractions} exact fractions; {active_admitted} admitted/measured and {active_pending} accessible pending.")
    print(f"PASS: {gluing_added} gluing original admitted with complete written proofs; L084 and L100 source acquisitions remain separate from recovery.")
    print(f'PASS: N006 corrected full contract; {wreath_admitted} recovered originals, {wreath_pending} accessible pending; measurement separate.')
    print(f'PASS: historical thirteen-topic overview has {overview34_fractions} exact comparisons and {overview34_bars} bars in each vector format for34 originals.')
    print(f'PASS: unified B scientific transfer and enlarged orbit comparison preserve {unified_fractions} new-edition fractions; historical33 overview is separately checked.')
    print(f'PASS: {nonfirm_corrections} explicit nonfirm HNN correction; no whole-source, numbered-conjecture or Lean credit.')
    print(f'PASS: {twist_corrections} uniform affine twisting correction; literal quotient subgroups proved, finite validation supplementary, no whole-source or Lean credit.')
    print(f'PASS: {fischer_cases} Fischer possible-exception cases have separate accepted proofs and exact certificates; no new original, priority or full Lean claim.')
    print(f'PASS: complete B5 comparison preserves {b5_fractions} exact fractions; {active_measured} originals measured.')
    print(f'PASS: expanded A/C topics preserve {ac_extension_fractions} exact fractions for twelve originals; two are newly measured.')
    print(f'PASS: diagonal measurement adds {diagonal_fractions} exact fractions; {active_measured} originals now measured.')
    print(f'PASS: high-rank extension preserves {high_rank_admitted} admitted originals and {high_rank_pending} accessible pending; measurement remains separate.')
    print(f'PASS: graph application extensions preserve {graph_admitted} admitted originals and {graph_pending} accessible pending; no new question credits.')
    print(f'PASS: two additional comparisons preserve {extra_measure_fractions} fractions; {active_measured} unique originals have current measurements.')
    check_project_lean_runner(lean)
    contracts, completion_bindings = check_completion()
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
    print('Trust: 99 reports without native axioms; one legacy report has four recorded native axioms.')
    print('Lean evidence: prior 96-module run and four separately checked additions.')
    print('PASS: Topic E has 150 independent metric cells and separate overall/conditional denominators.')
    print(f'PASS: Topic A has {a_cells} independent metric cells and {a_fractions} checked fractions; common costs are explicit.')
    print('PASS: Topic E paired proof graphs preserve all 90 source/application/program cost coordinates.')
    print(f'PASS: Topic A paired proof graphs preserve all {a_dag_cells} complete-document cost coordinates.')
    print(f'PASS: Topic B preserves {b_clauses} source clauses and {b_declarations} separately checked Lean declarations.')
    print(f'PASS: Topic B has {b_cells} independent metric cells and {b_fractions} conditional fractions; historical PDF-only N001 cost stays unknown; current available-text measurements are checked separately.')
    print(f'PASS: Topic B paired proof graphs preserve all {b_dag_cells} complete-document coordinates and 64 prerequisite closures.')
    print(f'PASS: Topic C preserves {c_rows} contract rows, {c_declarations} scoped Lean declarations and the full Janko census.')
    print(f'PASS: Topic C has {c_cells} independent PDF metric cells and {c_fractions} conditional fractions; written and required-program costs are separate, historical PDF-only L108 cost stays unknown; current available-text measurements are separate.')
    print(f'PASS: Topic C paired proof graphs preserve all {c_dag_cells} complete-document coordinates and {c_closures} prerequisite unions; historical PDF-only L108 cost stays unknown; current available-text measurements are separate.')
    print(f'PASS: Topic D preserves {d_rows} source rows, {d_declarations} scoped Lean declarations and the full Hall-Janko census; measurements remain separate.')
    print(f'PASS: Topic D generic support counting has {d_support_declarations} independently compiled declarations; source-specific instances remain separate.')
    print(f'PASS: Topic D has {d_cells} independent PDF metric cells and {d_fractions} exact combined/conditional fractions; complete programs and separate drivers are explicit.')
    print(f'PASS: Topic D paired dependencies conserve {d_dag_cells} complete-document metric cells and {d_closures} prerequisite unions; whole-paper factors remain unchanged.')
    print(f'PASS: affine papers preserve {affine_rows} source rows, {affine_declarations} scoped Lean declarations and all six complete programs.')
    print(f'PASS: affine comparison has {affine_cells} independent PDF metric cells and {affine_fractions} exact combined/conditional fractions; the whole common paper is charged.')
    print(f'PASS: affine dependencies conserve {affine_dag_cells} complete-document metric cells and {affine_routes} prerequisite unions; full ratios remain unchanged.')
    print(f'PASS: Topic F preserves {f_rows} source records, {f_declarations} scoped Lean declarations, complete uniform written proofs and all three validation programs; measurements remain separate.')
    print(f'PASS: Topic F has {f_cells} independent PDF metric cells and {f_fractions} exact combined/conditional fractions; the whole common paper and validation costs are explicit.')
    print(f'PASS: Topic G preserves {g_rows} source records, {g_declarations} scoped Lean declarations, complete common theory and both corrected applications with all thirteen programs; measurements remain separate.')
    print(f'PASS: Topic G has {g_cells} independent PDF metric cells and {g_fractions} exact combined/individual and cover-sensitivity fractions; the complete written replacement is longer overall.')
    print(f'PASS: representation preserves {representation_rows} source blocks, {representation_declarations} scoped Lean declarations and two whole validation programs; measurement remains separate.')
    print(f'PASS: representation has {representation_cells} independent PDF metric cells and {representation_fractions} exact combined/individual fractions; its small written saving reverses under UTF-8 counting.')
    print(f'PASS: chamber papers preserve {chamber_rows} scope rows, {chamber_declarations} scoped Lean declarations and the complete finite-cover program; all 27 admitted contracts have current common theory and applications, with measurement and full formalization separate.')
    print(f'PASS: chamber measurement has {chamber_cells} independent PDF cells and {chamber_fractions} exact fractions; the complete written comparison is slightly below one.')
    print(f'PASS: additional available-text comparisons retain all eight B/C originals and check {available_text_fractions} exact fractions; historical PDF-only unknowns remain separate.')
    print(f'PASS: the complete programme retains {corpus_originals} originals: {corpus_accessible} accessible, {corpus_pending} awaiting full recovery and {corpus_retrieval} retrieval targets at this snapshot.')
    print(f'PASS: additive admissions recover {current_admitted} unique originals; {current_pending} accessible originals remain pending. F015/L028 measurements remain pending.')
    print(f'PASS: consolidated ten-topic comparison checks {overview_fractions} exact fractions and {overview_svg}/{overview_pdf} actual SVG/PDF bars for27 original manuscripts.')
    print(f'PASS: diagonal construction and quotient review admitted; latest totals are {latest_admitted} recovered and {latest_pending} accessible pending originals, with all161 targets retained.')
    print(f'PASS: current programme pointer binds {active_admitted} admitted and {active_pending} accessible pending originals.')
    print('PASS: project Lean runner preserves both checker interfaces and explicitly partial validation coverage.')
    print(f'PASS: {contracts} admitted contracts and {completion_bindings} bound artifacts in the completion audit.')
    print('Historical computations require the pinned intake checkout.')

if __name__=='__main__':
    main()
