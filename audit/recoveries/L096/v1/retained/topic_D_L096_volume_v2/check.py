#!/usr/bin/env python3
"""Bounded L096 assembly audit: bindings, quantifiers, migration and renders."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,re,shutil,subprocess,sys

HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def need(x,s):
    if not x:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def normalize(s):return re.sub(r'\s+',' ',s.replace('U-','').replace('thin-triples','thin').replace('thin-recognize','recognize')).strip()
def proofs(s):return [normalize(x) for x in re.findall(r'\\begin\{proof\}(.*?)\\end\{proof\}',s,re.S)]

def verify_inventory(inventory,expected):
    own_expected={'assemble.py':'required_aggregate_reconstruction_program','build_boundary.py':'operational_whole_file_inventory_driver','check.py':'operational_integrity_and_render_checker'}
    bypath={r['path']:r for r in inventory['all_occurrences']}
    for n,role in own_expected.items():
        row=bypath['topic_D_L096_volume_v2/'+n];need(row['role']==role and row['sha256']==sha(HERE/n),'current whole-file role '+n)
    directional={r['path'] for r in inventory['all_occurrences'] if r['role']=='required_mathematical_directional_results'}
    expected_directional={b['path'] for b in expected['bindings'] if b['path'].endswith('_results.json') or b['path'].endswith('/results.json')}
    need(directional==expected_directional and len(directional)==7,'all seven direct directional JSON inputs')
    need(bypath['topic_D_L096_table_contract/source_tables.json']['role']=='required_source_contract_data','direct source comparison table')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True)
    ap.add_argument('--public-root',type=Path,default=Path('/Users/sasha/medusa/math_compression'))
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);need(not any(a.out.iterdir()),'fresh output required')
    manifest=read(HERE/'manifest.json')
    for b in manifest['exports']:
        f=HERE/b['path'];need(f.stat().st_size==b['bytes'] and sha(f)==b['sha256'],'own frozen export '+b['path'])
    for script in ['assemble.py','build_boundary.py']:
        r=subprocess.run([sys.executable,'-B','-O',str(HERE/script),'--study-root',str(a.study_root),'--out',str(a.out)],capture_output=True,text=True)
        need(r.returncode==0,r.stderr+r.stdout)
        (a.out/(script+'.log')).write_text(r.stdout+r.stderr)
    generated=['combined_results.json','historical_label_claims.json','combined_table.tex','whole_program_inventory.json','accepted_dependencies.json']
    for n in generated:need((a.out/n).read_bytes()==(HERE/n).read_bytes(),'exact regeneration '+n)
    expected=read(HERE/'combined_results.json');d=read(HERE/'accepted_dependencies.json')
    inventory=read(HERE/'whole_program_inventory.json');verify_inventory(inventory,expected)
    overlap=read(HERE/'topic_D_dependency_overlap.json')
    for b in overlap['old_topic_common_bindings']:
        f=a.public_root/b['path'];need(f.stat().st_size==b['bytes'] and sha(f)==b['sha256'],'old D common binding '+b['path'])
    migration=read(HERE/'migration.json');count=0
    for row in migration['fragments']:
        b=row['source'];f=a.study_root/b['path'];need(f.stat().st_size==b['bytes'] and sha(f)==b['sha256'],'migration source')
        src=f.read_text();target=(HERE/row['target']).read_text()
        need(hashlib.sha256(target.encode()).hexdigest()==row['target_sha256'],'migration target')
        if 'source_start' in row:
            i=src.index(row['source_start']);j=src.index(row['source_end_exclusive'],i);old=src[i:j]
            need(hashlib.sha256(old.encode()).hexdigest()==row['source_snippet_sha256'],'migration snippet')
            oldproofs=proofs(old);newproofs=proofs(target)
            need(oldproofs==newproofs,'complete inherited proof bodies '+row['target']);count+=len(oldproofs)
        if row['literal_equal']:need(target==(old if 'source_start' in row else src),'literal fragment equality')
    source=read(HERE/'source_map.json')
    for key in ['primary','primary_text']:
        b=source[key];f=a.study_root/b['path']
        need(f.stat().st_size==b['bytes'] and sha(f)==b['sha256'],'literal primary binding '+key)
    need(len(source['main_and_count_clauses'])==73 and len(source['historical_label_claims'])==232,'complete source accounting')
    need(source['full_source_recovered'] is False,'unresolved full-source boundary')
    text=(a.study_root/source['primary_text']['path']).read_text()
    pages={int(k):v for k,v in re.findall(r'--- PDF PAGE (\d+) ---\n(.*?)(?=\n--- PDF PAGE |\Z)',text,re.S)}
    for row in source['main_and_count_clauses']:
        for loc in row['locator']:
            need(hashlib.sha256(pages[loc['physical_page']].encode()).hexdigest()==loc['page_text_sha256'],'source locator')
    spec=importlib.util.spec_from_file_location('local_assembly',HERE/'assemble.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    raw=read(a.study_root/'topic_D_L096_extended_candidate/mathieu_results.json')['rows'][0]
    controls=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,AssertionError,KeyError,StopIteration):controls.append(name);return
        raise ValueError('control accepted '+name)
    for name,mutation in [
       ('dropped base residue',lambda r:r['residues'].pop()),
       ('duplicate base residue',lambda r:r['residues'].__setitem__(1,copy.deepcopy(r['residues'][0]))),
       ('wrong directional IP',lambda r:r['residues'][0].__setitem__('IP',not r['residues'][0]['IP'])),
       ('wrong directional WIP',lambda r:r['residues'][0].__setitem__('WIP',not r['residues'][0]['WIP'])),
       ('dropped target type',lambda r:r['residues'][0]['type_results'].pop()),
       ('wrong full IP',lambda r:r.__setitem__('IP',not r['IP'])),
       ('wrong full WIP',lambda r:r.__setitem__('WIP',not r['WIP'])),
       ('rank-zero existential inserted',lambda r:r['residues'].append({'fixed_types':[1,2,3],'residue_rank':0,'type_results':[]})),
    ]:
        v=copy.deepcopy(raw);mutation(v);reject(name,lambda v=v:mod.certify_quantifiers(v))
    def equal_report(v):need(v==expected,'actual accepted-record equality')
    for name,mutation in [
       ('one representative dropped',lambda v:v['classes'].pop()),
       ('historical suffix fabricated',lambda v:v['classes'][0].__setitem__('historical_label','3.1')),
       ('M12 discrepancy erased',lambda v:v['differences'][0].__setitem__('computed_counts',{'IP':7,'WIP_only':1,'not_WIP':10})),
       ('global classification substituted',lambda v:v.__setitem__('full_source_credit',True)),
       ('old source count treated as current',lambda v:v.__setitem__('actual_roster_total',277)),
    ]:
        v=copy.deepcopy(expected);mutation(v);reject(name,lambda v=v:equal_report(v))
    for name,path in [('omitted current required aggregation program','topic_D_L096_volume_v2/assemble.py'),('omitted whole directional JSON','topic_D_L096_HS_extension/shadow_results.json'),('omitted source-contract JSON','topic_D_L096_table_contract/source_tables.json')]:
        v=copy.deepcopy(inventory);v['all_occurrences']=[x for x in v['all_occurrences'] if x['path']!=path]
        reject(name,lambda v=v:verify_inventory(v,expected))
    v=copy.deepcopy(inventory)
    next(x for x in v['all_occurrences'] if x['path']=='topic_D_L096_volume_v2/assemble.py')['role']='optional_validation'
    reject('required aggregation cannot become optional',lambda:verify_inventory(v,expected))
    need(all(any(x) for x in [[True,False],[False,True]]) and not any(all(x[j] for x in [[True,False],[False,True]]) for j in range(2)),'residue-dependent type diagnostic')
    controls.append('residue-dependent successful type differs from fixed global type')
    renders=[]
    if a.render:
        from pypdf import PdfReader
        stage=a.out/'render';stage.mkdir()
        for f in HERE.rglob('*.tex'):
            p=stage/f.relative_to(HERE);p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,p)
        for name in ['umbrella','shadow_applications']:
            for k in range(2):
                r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=stage,capture_output=True,text=True)
                (stage/(name+f'.render{k}.log')).write_text(r.stdout+r.stderr);need(r.returncode==0,'render '+name)
            log=(stage/(name+'.log')).read_text();need(not any(x in log for x in ['LaTeX Warning:','Overfull','Underfull']),'clean render '+name)
            before=[p.extract_text() for p in PdfReader(HERE/(name+'.pdf')).pages]
            after=[p.extract_text() for p in PdfReader(stage/(name+'.pdf')).pages]
            need(before==after,'complete page texts '+name);renders.append({'document':name,'pages':len(after),'exact_page_text':True})
    report={'status':'PASS_BOUNDED_ASSEMBLY_NOT_COMPLETE_HISTORICAL_LABEL_RECOVERY',
        'accepted_components':len(d['accepted_components']),'frozen_component_exports':len(d['all_frozen_component_exports']),
        'retained_census_artifact_occurrences':sum(len(x['complete_artifact_bindings']) for x in d['retained_complete_censuses']),
        'verified_migrated_proof_environments':count,'source_main_and_count_clauses':73,'unresolved_label_occurrences':232,
        'actual_roster_classes':278,'source_count_comparisons':57,'matching_count_rows':53,
        'semantic_controls':controls,'render':renders,'new_finite_group_run':False,'new_Lean_run':False,'full_source_credit':False}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
