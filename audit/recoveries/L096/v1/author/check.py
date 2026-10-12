#!/usr/bin/env python3
"""Bounded current L096 replay, using unchanged complete accepted populations."""
from pathlib import Path
import argparse, collections, copy, hashlib, importlib.util, json, re
import shutil, subprocess, sys

HERE = Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text())
def need(v, s):
    if not v: raise ValueError(s)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def binding(root, row):
    p = root / row['path']
    need(p.is_file() and p.stat().st_size == row['bytes'] and sha(p) == row['sha256'],
         'whole file binding: ' + row['path'])
def proof(s): return re.findall(r'\\begin\{proof\}(.*?)\\end\{proof\}', s, re.S)

def validate_table(text, profiles):
    rows = []
    for p in profiles:
        g = r'$\mathrm{HS}$' if p['group'] == 'HS' else '$' + p['group'][0] + '_{' + p['group'][1:] + '}$'
        rows.append(' & '.join([g,p['label'],str(p['page']),
                    ','.join(map(str,p['type_sizes'])),
                    '--' if p['borel'] is None else str(p['borel']),
                    ', '.join(str(r['active_row']) for r in p['candidate_fibre'])]) + r' \\')
    actual = [s.strip() for s in text.splitlines() if s.startswith('$')]
    need(actual == rows, 'all 116 complete printed profile rows')

def validate_scope(source, reconciliation, inventory):
    need(len(source['main_and_count_clauses']) == 73, '73 full source dispositions')
    need(len({r['id'] for r in source['main_and_count_clauses']}) == 73, 'unique main identifiers')
    need(len(reconciliation['claims']) == len(source['historical_label_claims']) == 232,
         'all 232 historical occurrences')
    need(source['historical_label_claims'] == reconciliation['claims'], 'complete claim transfer')
    need(reconciliation['counts'] == {
        'CONFIRMED_ON_EVERY_COMPATIBLE_CLASS': 229,
        'ORDINAL_UNVERIFIED_CORRECTED_PROFILE_CLASSIFICATION': 3}, 'exact corrected naming boundary')
    need(source['literal_original_replacement_equivalence'] is False
         and source['full_source_recovered'] is False
         and source['complete_corrected_principal_recovery_proposed'] is True,
         'corrected contract versus literal equivalence')
    need(source['mathematical_principal_obligations_unresolved'] == [], 'complete proposed mathematical contract')
    need(reconciliation['literal_historical_name_equivalence'] is False, 'no invented historical equivalence')
    need(len(reconciliation['profiles']) == 116, 'all documentary profiles')
    need(len({(p['group'],p['label']) for p in reconciliation['profiles']}) == 116,
         'unique source-profile identifiers')
    for c in reconciliation['claims']:
        if c['group'] == 'J1':
            need(c['label'] == '4.1' and c['candidate_decisions'] == []
                 and c['status'] == 'ORDINAL_UNVERIFIED_CORRECTED_PROFILE_CLASSIFICATION',
                 'unverified J1 ordinal remains unassigned')
        else:
            need(c['candidate_decisions'] and all(x['agrees'] for x in c['candidate_decisions']),
                 'every compatible representative has the claimed property')
    j = reconciliation['J1_complete_profile_classification']
    need(len(j) == 3 and [(r['member'],r['active_row']) for r in j] ==
         [('j1.rk3',1),('j1.rk4',1),('j1.rk4',2)], 'entire J1 population')
    need(j[1]['type_sizes'] == [266,1463,1463,2926] and j[1]['IP'] is True
         and j[2]['type_sizes'] == [266,266,1463,2926] and j[2]['WIP'] is False,
         'exact two mathematical rank-four profiles')
    need(inventory['inherited_occurrences'] == 870 and inventory['role_categories_disjoint'] is False,
         'whole inherited boundary and overlapping roles')
    need(inventory['measurement_factor'] is None, 'no numerical factor')
    paths = collections.defaultdict(list)
    for r in inventory['all_occurrences']: paths[r['path']].append(r['role'])
    for name in ['label_invariants.g','parse_invariants.py','reconcile_labels.py']:
        need(any(x.startswith('required_') for x in paths['corpus106_L096_recovery/'+name]),
             'whole required current program: '+name)
    for name in ['topic_D_L096_M22_extension/prior_inputs.g',
                 'topic_D_L096_J3_extension/archive_data/inputs.g']:
        need('required_complete_data_for_new_label_invariant' in paths[name], 'whole new group data')

def main():
    p=argparse.ArgumentParser();p.add_argument('--study-root',required=True,type=Path)
    p.add_argument('--public-root',type=Path,default=Path('/Users/sasha/medusa/math_compression'))
    p.add_argument('--out',required=True,type=Path);p.add_argument('--render',action='store_true')
    p.add_argument('--programs',action='store_true');a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True);need(not any(a.out.iterdir()),'fresh output')
    manifest_path=HERE/'manifest.json';own=0
    if manifest_path.exists():
        for r in read(manifest_path)['exports']: binding(HERE,r);own+=1
    deps=read(HERE/'dependencies.json');checked=set()
    def external(row):
        key=(row['path'],row['sha256'])
        if key not in checked:binding(a.study_root,row);checked.add(key)
    for packet in deps['direct_packets']:
        external(packet['manifest'])
        for row in packet['exports']:external(row)
    external(deps['prior_complete_dependency_ledger'])
    old=deps['all_prior_mathematical_components']
    for row in old['all_frozen_component_exports']:external(row)
    for census in old['retained_complete_censuses']:
        for row in census['complete_artifact_bindings']:external(row)
    for row in deps['old_topic_D_common']['old_topic_common_bindings']:binding(a.public_root,row)
    inventory=read(HERE/'whole_program_inventory.json')
    for row in inventory['all_occurrences']:
        if row['path'].startswith('corpus106_L096_recovery/'):
            local={**row,'path':row['path'].split('/',1)[1]};binding(HERE,local)
        else:external(row)
    unique={}
    for row in inventory['all_occurrences']:
        u=unique.setdefault(row['sha256'],{'sha256':row['sha256'],'bytes':row['bytes'],'paths':[],'roles':[]})
        need(u['bytes']==row['bytes'],'unique whole content size')
        if row['path'] not in u['paths']:u['paths'].append(row['path'])
        if row['role'] not in u['roles']:u['roles'].append(row['role'])
    need(sorted(unique.values(),key=lambda r:r['sha256'])==inventory['unique_contents'],
         'exact full-content deduplication retaining every role')
    source=read(HERE/'source_map.json');rec=read(HERE/'label_reconciliation.json')
    validate_scope(source,rec,inventory)
    validate_table((HERE/'label_table.tex').read_text(),rec['profiles'])
    old_source=read(a.study_root/'topic_D_L096_volume_v2/source_map.json')
    for oldr,newr in zip(old_source['main_and_count_clauses'],source['main_and_count_clauses']):
        for k in ['id','locator','source_assertion','disposition','current_result']:
            need(oldr.get(k)==newr.get(k),'unchanged accepted mathematical source route '+k)
    original_claims=read(a.study_root/'topic_D_L096_volume_v2/historical_label_claims.json')['claims']
    for c,oldr in zip(rec['claims'],original_claims):
        for k in ['group','rank','label','property_rank','claim','source_page','source_table','source_reference']:
            need(c[k]==oldr[k],'literal original occurrence '+k)
    # Reconstruct from every old class record, without invoking any old finite search.
    r=subprocess.run([sys.executable,'-B','-O',str(HERE/'reconcile_labels.py'),
                      '--study-root',str(a.study_root),'--out',str(a.out/'label_reconciliation.json')],
                     capture_output=True,text=True)
    need(r.returncode==0,r.stdout+r.stderr)
    need((a.out/'label_reconciliation.json').read_bytes()==(HERE/'label_reconciliation.json').read_bytes(),
         'all complete compatible families and 232 decisions regenerate')
    from parse_invariants import parse
    parsed=parse((HERE/'records/label_invariants.log').read_text())
    need(parsed==read(HERE/'label_invariants.json'),'complete bounded stdout binding')
    execution=read(HERE/'records/label_execution.json')
    for row in execution['inputs']:external(row)
    for name in ['program','stdout','parsed']:
        row=execution[name];binding(HERE,{**row,'path':row['path'].split('/',1)[1]})
    finite_run=None
    if a.programs:
        r=subprocess.run(['/opt/homebrew/bin/gap','-q',str(HERE/'label_invariants.g')],
                         cwd=a.study_root,capture_output=True,text=True)
        (a.out/'label_program.stdout').write_text(r.stdout);(a.out/'label_program.stderr').write_text(r.stderr)
        need(r.returncode==0 and not r.stderr.strip(),'bounded GAP execution')
        need(parse(r.stdout)==parsed,'same seven exact new mathematical invariants')
        finite_run='SEVEN_NEW_BOUNDED_CASES_ONLY'
    migration=read(HERE/'migration.json');environments=0
    for row in migration['files']:
        external(row['source']);binding(HERE,row['target'])
        before=(a.study_root/row['source']['path']).read_text();after=(HERE/row['target']['path']).read_text()
        need(proof(before)==proof(after),'all complete inherited proofs unchanged')
        if row['literal_identical']:need(before==after,'literal inherited source')
        environments+=len(proof(before))
    binding(HERE,{**migration['old_common_pdf_exact'],'path':'umbrella.pdf'})
    # Primary assets remain private. Verify those supplied; do not require them for copies.
    ledger=read(HERE/'source_ledger.json');private_checked=0
    for row in [ledger['primary'],ledger['primary_text_private']]+[
            q for r in ledger['auxiliary_primary_records'] for q in [r['whole_original_file'],r['private_conversion']]]:
        if (a.study_root/row['path']).exists():external(row);private_checked+=1
    controls=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError):controls.append(name);return
        raise ValueError('negative control accepted: '+name)
    for name,mut in [
        ('drop a named occurrence',lambda v:v['claims'].pop()),
        ('invent literal name equivalence',lambda v:v.__setitem__('literal_historical_name_equivalence',True)),
        ('replace universal candidate agreement',lambda v:v['claims'][0]['candidate_decisions'][0].__setitem__('agrees',False)),
        ('omit a source profile',lambda v:v['profiles'].pop()),
        ('omit the negative J1 class',lambda v:v['J1_complete_profile_classification'].pop()),
        ('replace J1 mathematical profile',lambda v:v['J1_complete_profile_classification'][1].__setitem__('type_sizes',[266,266,1463,2926])),
    ]:
        v=copy.deepcopy(rec);mut(v);reject(name,lambda v=v:validate_scope(source,v,inventory))
    for name,mut in [
        ('omit principal disposition',lambda v:v['main_and_count_clauses'].pop()),
        ('duplicate principal identifier',lambda v:v['main_and_count_clauses'][1].__setitem__('id',v['main_and_count_clauses'][0]['id'])),
        ('literal source recovery substituted',lambda v:v.__setitem__('full_source_recovered',True)),
        ('hide corrected contract',lambda v:v.__setitem__('complete_corrected_principal_recovery_proposed',False)),
    ]:
        v=copy.deepcopy(source);mut(v);reject(name,lambda v=v:validate_scope(v,rec,inventory))
    for name,mut in [
        ('omit whole required GAP file',lambda v:v.__setitem__('all_occurrences',[r for r in v['all_occurrences'] if not r['path'].endswith('/label_invariants.g')])),
        ('omit whole J3 input',lambda v:v.__setitem__('all_occurrences',[r for r in v['all_occurrences'] if r['path']!='topic_D_L096_J3_extension/archive_data/inputs.g'])),
        ('collapse overlapping roles into disjoint costs',lambda v:v.__setitem__('role_categories_disjoint',True)),
        ('invent a factor',lambda v:v.__setitem__('measurement_factor',1)),
    ]:
        v=copy.deepcopy(inventory);mut(v);reject(name,lambda v=v:validate_scope(source,rec,v))
    text=(HERE/'records/label_invariants.log').read_text()
    for name,t in [('lost complete terminator',text.replace('LABEL_INVARIANTS_PASS','')),
                   ('duplicate finite row',text.replace('LABEL_INVARIANTS_PASS','M22_SWAP|3|1320|false\nLABEL_INVARIANTS_PASS')),
                   ('wrong inner normalizer bound',text.replace('J3_SWAP|10|2448','J3_SWAP|10|1224')),
                   ('wrong residue girth',text.replace('M22_RESIDUE|11|360|30|8','M22_RESIDUE|11|360|30|6'))]:
        reject(name,lambda t=t:parse(t))
    table=(HERE/'label_table.tex').read_text()
    reject('wrong printed profile type size',lambda:validate_table(table.replace('176,15400,176','176,15401,176',1),rec['profiles']))
    reject('wrong printed compatible entry',lambda:validate_table(table.replace('720 & 1','720 & 2',1),rec['profiles']))
    renders=[]
    if a.render:
        from pypdf import PdfReader
        stage=a.out/'render';stage.mkdir()
        for f in HERE.rglob('*.tex'):
            if 'private_auxiliary' in f.parts:continue
            q=stage/f.relative_to(HERE);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,q)
        for n in ['umbrella','shadow_applications','named_geometries']:
            for _ in range(3):
                r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error',n+'.tex'],cwd=stage,capture_output=True,text=True)
                need(r.returncode==0,'render '+n)
            log=(stage/(n+'.log')).read_text();need(not any(x in log for x in ['Warning:','Overfull','Underfull']),'clean render '+n)
            before=[p.extract_text() for p in PdfReader(HERE/(n+'.pdf')).pages]
            after=[p.extract_text() for p in PdfReader(stage/(n+'.pdf')).pages]
            need(before==after,'all exact rendered pages '+n);renders.append({'name':n,'pages':len(after),'exact_page_text':True})
    report={'status':'PASS_AUTHOR_COMPLETE_CORRECTED_PRINCIPAL_CANDIDATE',
            'exports_verified':own,'external_bindings_verified':len(checked),
            'source_dispositions':73,'positive_named_occurrences':232,
            'complete_printed_profile_rows':116,
            'direct_profile_confirmations':229,'unverified_historical_ordinals':3,
            'complete_J1_profile_classes':3,'new_finite_cases':7,
            'inherited_proof_environments_unchanged':environments,
            'whole_file_occurrences':len(inventory['all_occurrences']),
            'unique_whole_contents':len(inventory['unique_contents']),
            'private_primary_bindings_if_supplied':private_checked,
            'controls':controls,'render':renders,'new_finite_run':finite_run,
            'old_census_or_shadow_rerun':False,'new_formal_run':False,
            'literal_table_name_equivalence':False,'whole_original_credit':False}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
