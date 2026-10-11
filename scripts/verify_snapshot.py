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
    active_admitted, active_pending = check_current_programme_pointer()
    print(f'PASS: graph application extensions preserve {graph_admitted} admitted originals and {graph_pending} accessible pending; no new question credits.')
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
    print(f'PASS: Topic B has {b_cells} independent metric cells and {b_fractions} conditional fractions; N001 and the overall factor remain unknown.')
    print(f'PASS: Topic B paired proof graphs preserve all {b_dag_cells} complete-document coordinates and 64 prerequisite closures.')
    print(f'PASS: Topic C preserves {c_rows} contract rows, {c_declarations} scoped Lean declarations and the full Janko census.')
    print(f'PASS: Topic C has {c_cells} independent PDF metric cells and {c_fractions} conditional fractions; written and required-program costs are separate, L108 remains unknown.')
    print(f'PASS: Topic C paired proof graphs preserve all {c_dag_cells} complete-document coordinates and {c_closures} prerequisite unions; L108 remains unknown.')
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
