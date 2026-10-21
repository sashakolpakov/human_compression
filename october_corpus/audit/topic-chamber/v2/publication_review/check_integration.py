#!/usr/bin/env python3
"""Check root-authored publication wiring; do not rerun scientific GAP or Lean.

Parsed-record mutations leave every actual disk-byte check enabled. The
scientific author performs this limited integration review, relying on the
separate accepted scientific review and root adoption for mathematics.
"""
import argparse, ast, copy, hashlib, importlib.util, json, re, subprocess
from pathlib import Path

BASE='8625c78da1fb57f50b4c6c7f792f294356d01c3c'
CANDIDATE_SHA='decb8c3d95705df685ee9b829c58d56eefbb545ba859f98000f4ad745a0a769b'
B='papers/topic-chamber/v2/'
A='audit/topic-chamber/v2/'
EXPORTS={'README.rst','candidate_binding.json','check_integration.py','integration_result.json','review.json','visual_review.json','whitespace_review.json'}
LATER={A+'publication_review/'+p for p in EXPORTS|{'manifest.json'}}|{A+'root_publication_acceptance.json',A+'root_publication_replay.json','provenance/publication_manifest.json'}

def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def change_set(changed,bound):
    need(bound<=changed,'candidate file absent from baseline change set')
    need(changed<=bound|LATER,'unreviewed change '+str(sorted(changed-bound-LATER)))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh output required');repo,study=a.repo.resolve(),a.study.resolve()
    cp=study/'topic_Chamber_publication_candidate/candidate.json';need(sha(cp)==CANDIDATE_SHA,'candidate pin')
    candidate=load(cp);need(candidate['base_commit']==BASE and set(candidate['allowed_post_candidate_paths'])==LATER,'candidate exact future boundary')
    bound={r['path'] for r in candidate['public_files']};need(len(bound)==len(candidate['public_files'])==110,'candidate count')
    for r in candidate['public_files']:
        p=repo/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'changed candidate '+r['path'])
    changed=set(subprocess.check_output(['git','diff','--name-only',BASE,'--'],cwd=repo,text=True).splitlines());change_set(changed,bound)
    future=repo/A/'publication_review/manifest.json'
    if future.exists():
        own=Path(__file__).resolve().parent/'manifest.json';need(own.exists() and sha(own)==sha(future),'future review must be exact frozen review')
        mf=load(future);need({r['path'] for r in mf['exports']}==EXPORTS,'future export boundary')
        for r in mf['exports']:
            p=future.parent/r['path'];need(sha(p)==r['sha256'] and p.stat().st_size==r['bytes'],'future review export')
    old=subprocess.check_output(['git','show',BASE+':scripts/verify_snapshot.py'],cwd=repo,text=True)
    script=repo/'scripts/verify_snapshot.py';trees=[ast.parse(old),ast.parse(script.read_text())]
    defs=lambda t:{n.name:n for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    before,after=map(defs,trees);prior=load(study/'topic_Chamber_publication_candidate/prior_guard_asts.json');unchanged=[]
    for name,n in before.items():
        if name=='main':continue
        need(ast.dump(n,include_attributes=False)==ast.dump(after[name],include_attributes=False)==prior[name],'old guard changed '+name);unchanged.append(name)
    need(len(unchanged)==len(set(prior)-{'main'})==35 and set(after)-set(before)=={'check_chamber_proofs'},'guard inventory')
    other=lambda t:[ast.dump(n,include_attributes=False) for n in t.body if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    need(other(trees[0])==other(trees[1]),'module configuration changed')
    calls=lambda n:[x.func.id for x in ast.walk(n) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id.startswith('check_')]
    c0,c1=calls(before['main']),calls(after['main']);need([x for x in c1 if x!='check_chamber_proofs']==c0 and c1.count('check_chamber_proofs')==1,'main checks changed')
    admission=load(repo/A/'admission.json');setup=load(study/'topic_Chamber_publication_candidate/setup.json');copies=[];total=0
    need(sha(repo/A/'admission.json')=='f925d6afd3baf1261089efbeac761aed55f6787ce250f5408d36f33a5773d505','admission pin')
    for p in setup['packets']:
        x,y=study/p['source'],repo/p['destination'];need(sha(x/'manifest.json')==sha(y/'manifest.json')==p['pin']==admission['manifests'][p['role']],'copied manifest')
        rows=load(x/'manifest.json')['exports'];need(len(rows)==p['exports'],'packet count')
        for r in rows:
            orig,dest=x/r['path'],y/r['path'];need(orig.read_bytes()==dest.read_bytes() and sha(dest)==r['sha256'] and dest.stat().st_size==r['bytes'],'copied export '+str(dest))
        total+=len(rows);copies.append(p)
    need(total==96 and len(copies)==3,'copy closure')
    for r in admission['artifacts']:
        p=repo/r['path'];need(sha(p)==r['sha256'] and p.stat().st_size==r['bytes'],'admission binding '+r['path'])
    need(len(admission['artifacts'])==99,'admission closure')
    oldcat=json.loads(subprocess.check_output(['git','show',BASE+':papers/catalogue.json'],cwd=repo,text=True));cat=load(repo/'papers/catalogue.json')
    newentries=[r for r in cat['new_editions'] if r['topic']=='Chamber'];need(len(newentries)==3,'new catalogue entries')
    restored=copy.deepcopy(cat);restored['new_editions']=[r for r in cat['new_editions'] if r['topic']!='Chamber'];restored['current_topic_editions'].pop('Chamber')
    need(restored==oldcat,'prior catalogue changed')
    spec=importlib.util.spec_from_file_location('chamber_publication_guard_review',script);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    positive=m.check_chamber_proofs();need(positive==(27,14),'new guard result')
    previous={name:getattr(m,name)() for name in ['check_affine_dag']}
    original_load=m.load;controls=[]
    def control(name,target,change):
        def patched(path):
            d=original_load(path)
            if str(path)==target:d=copy.deepcopy(d);change(d)
            return d
        m.load=patched
        try:m.check_chamber_proofs()
        except (ValueError,RuntimeError) as e:controls.append({'name':name,'rejected':True,'reason':str(e),'mechanism':'Parsed-record mutation; actual file hashes remain checked.'})
        else:raise ValueError('accepted mutation '+name)
        finally:m.load=original_load
    def status(d,id,value):next(r for r in d['rows'] if r['id']==id).update(status=value)
    control('changed_artifact',A+'admission.json',lambda d:d['artifacts'][0].update(sha256='0'*64))
    control('changed_author_pin',A+'admission.json',lambda d:d['manifests'].update(author='0'*64))
    control('lost_infinite_qualification',B+'scope.json',lambda d:status(d,'H02','recovered'))
    control('ancillary_software_promoted',B+'scope.json',lambda d:status(d,'H09','recovered'))
    control('lost_identity_word_correction',B+'scope.json',lambda d:status(d,'R07','recovered'))
    control('question_as_principal_result',B+'scope.json',lambda d:status(d,'R17','recovered'))
    control('full_formalization_invented',B+'formal/scope.json',lambda d:d.update(end_to_end_application_formalized=True))
    control('missing_reused_Lean_reports',B+'formal/scope.json',lambda d:d['modules'][0].update(reports=0))
    control('diagnostic_used_as_premise',B+'program_inventory.json',lambda d:d['programs'][1].update(required_mathematical_premise=True))
    control('old_code_unknown_as_zero',B+'program_inventory.json',lambda d:d.update(historical_code_cost=0))
    control('lost_operational_driver',B+'program_inventory.json',lambda d:d.update(current_drivers=0))
    control('later_question_as_premise',B+'question_map.json',lambda d:d['questions'][0].update(proof_premise_here=True))
    control('allrank_finite_question_closed',A+'admission.json',lambda d:d.update(allrank_finite_multiplicity_remains_unresolved=False))
    control('changed_proof_span',B+'scope.json',lambda d:next(iter(d['proof_spans'].values())).update(sha256='0'*64))
    control('missing_reviewed_source_row',A+'independent_review/coverage_review.json',lambda d:d['rows'].pop())
    control('self_review_disguised',A+'independent_review/review.json',lambda d:d['review_roles'].update(independent_reviewer='rewrite_termination'))
    control('missing_catalogue_input','papers/catalogue.json',lambda d:next(r for r in d['new_editions'] if r['topic']=='Chamber')['tex_inputs'].pop())
    control('failed_render_accepted',A+'publication_replay/appendix.json',lambda d:d.update(per_page_text_identical=False))
    control('source_count_inflated_to_161',A+'admission.json',lambda d:d.update(canonical_complete_contract_count_at_this_admission=161))
    control('new_source_credit',A+'admission.json',lambda d:d.update(new_source_credit=1))
    control('factor_invented',A+'admission.json',lambda d:d.update(compression_ratio=2))
    control('graphics_unknown_as_zero',A+'admission.json',lambda d:d.update(source_graphics_cost=0))
    control('common_theory_uncharged',A+'root_adoption/review.json',lambda d:d.update(whole_common_cost_required=False))
    control('cross_topic_discount',A+'root_adoption/review.json',lambda d:d.update(cross_topic_discount=True))
    need(m.check_chamber_proofs()==positive,'restored guard')
    boundary_controls=[]
    for extra in [A+'unreviewed_extra.json',A+'publication_review/not_declared.json',B+'extra_theorem.tex']:
        try:change_set(bound|{extra},bound)
        except ValueError as e:boundary_controls.append({'path':extra,'rejected':True,'reason':str(e)})
        else:raise ValueError('undeclared extra accepted')
    links=[]
    for name in ['README.rst','audit/completion.rst',B+'PUBLICATION.rst']:
        for href in re.findall(r'<([^<>]+)>`_', (repo/name).read_text()):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',href):continue
            target=href.split('#')[0]
            if target:need(((repo/name).parent/target).exists(),'broken link '+name+' '+target);links.append({'document':name,'target':target})
    # Run the documented standalone public command in a fresh directory. It only
    # verifies supplied bytes and scope; it does not run GAP, Lean or XeLaTeX.
    run_dir=a.out.parent/(a.out.stem+'_public_bindings');need(not run_dir.exists(),'fresh binding directory')
    run=subprocess.run(['python3','-B','-O',str(repo/B/'check.py'),'--out',str(run_dir),'--bindings-only'],cwd=repo,capture_output=True,text=True)
    need(run.returncode==0,'documented command failed '+run.stderr)
    binding=load(run_dir/'bindings.json');need(binding['status']=='PASS' and binding['source_rows']==27 and binding['proof_spans']==22,'public bindings result')
    report={'status':'PASS_BOUNDED_INDEPENDENT_CHAMBER_PUBLICATION_INTEGRATION','baseline':BASE,'candidate_sha256':CANDIDATE_SHA,'candidate_files':110,'changed_files_at_replay':len(changed),'exact_allowed_later_paths':sorted(LATER),'prefix_wildcards':False,'prior_nonmain_guards_unchanged':unchanged,'prior_main_calls_preserved':True,'prior_check_results':previous,'new_check_result':positive,'copied_packets':copies,'exact_exports':total,'admission_artifacts':99,'old_catalogue_preserved':True,'negative_controls':controls,'boundary_controls':boundary_controls,'relative_links':links,'public_command':{'argv':run.args,'returncode':run.returncode,'stdout':run.stdout,'result':binding},'scope':{'source_rows':27,'existing_principal_contracts':2,'canonical_total':27,'scientific_pages':15,'program_pages':3,'formal_reports':14,'new_formal_reports':7,'reused_formal_reports':7,'end_to_end_formalization':False,'programs':{'required':1,'diagnostic':1,'historical_drivers':2,'current_driver':1},'new_credit':0,'measurement':None},'independence':'Integration author root. Reviewer rewrite_termination authored the science; separate scientific acceptance by enumeration_review and adoption by root remain authoritative. This review does not independently re-adjudicate its own mathematics.','GAP_or_Lean_replay':False,'small_accepted_interface_models_executed_by_guard':True,'source_reextraction':False,'public_edits':False}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'controls':len(controls),'boundary_controls':len(boundary_controls),'exports':total,'links':len(links),'result':positive}))
if __name__=='__main__':main()
