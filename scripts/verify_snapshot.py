#!/usr/bin/env python3
"""Check tracked publication and pinned archive separately; ignore local Markdown.

Historical proof replay requires the intake checkout. This is an integrity
check, not a rerun of the mathematical proofs or their computations.
"""
import argparse
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
    print(f'PASS: Topic B preserves {b_clauses} source clauses and {b_declarations} separately checked Lean declarations; no measured ratio yet.')
    print('PASS: project Lean runner preserves both checker interfaces and explicitly partial validation coverage.')
    print(f'PASS: {contracts} admitted contracts and {completion_bindings} bound artifacts in the completion audit.')
    print('Historical computations require the pinned intake checkout.')

if __name__=='__main__':
    main()
