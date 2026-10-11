#!/usr/bin/env python3
"""Review G measurement publication wiring, preserving accepted source audits.

No source/font extraction or scientific program/Lean execution. The frozen
independent arithmetic is run only to check its public routing. Corruptions
alter parsed records while actual disk-byte guards remain enabled.
"""
import argparse,ast,copy,hashlib,importlib.util,json,re,subprocess,tempfile
from pathlib import Path
BASE='b6c0a3cc45c556e3ec0b744df408227c8f922139'
CANDIDATE='b81214837d0efd8d3f8cab413d2a7c70025fbd7dd57b04de4de78d9480328cd9'
P='audit/topic-g/v2/measurement/'
EXPORTS={'README.rst','candidate_binding.json','check_integration.py','integration_result.json','review.json','visual_review.json','whitespace_review.json','adapter_controls.json'}
LATER={P+'publication_review/'+p for p in EXPORTS|{'manifest.json'}}|{P+'root_publication_acceptance.json',P+'root_publication_replay.json','provenance/publication_manifest.json'}
def need(b,s):
    if not b:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def changes(changed,bound):
    need(bound<=changed,'candidate path omitted')
    need(changed<=bound|LATER,'unexpected changed path '+str(sorted(changed-bound-LATER)))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output path')
    repo,study=a.repo.resolve(),a.study.resolve();cdir=study/'topic_G_measurement_publication_candidate';cp=cdir/'candidate.json'
    need(sha(cp)==CANDIDATE,'candidate pin');candidate=load(cp);need(candidate['base_commit']==BASE,'baseline')
    need(set(candidate['expected_later_additions'])=={P+'publication_review/',P+'root_publication_acceptance.json',P+'root_publication_replay.json','provenance/publication_manifest.json'},'candidate later declarations')
    # The candidate's review-directory placeholder is refined to the exact
    # nine files above. It is never treated as a prefix-wide permission.
    bound={r['path'] for r in candidate['files']};need(len(bound)==len(candidate['files'])==88,'candidate cardinality')
    for r in candidate['files']:
        p=repo/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'candidate byte '+r['path'])
    changed=set(subprocess.check_output(['git','diff','--name-only',BASE,'--'],cwd=repo,text=True).splitlines());changes(changed,bound)
    future=repo/P/'publication_review/manifest.json'
    if future.exists():
        own=Path(__file__).parent/'manifest.json';need(own.exists() and sha(own)==sha(future),'exact accepted future review')
        mf=load(future);need({r['path'] for r in mf['exports']}==EXPORTS,'future export names')
        for r in mf['exports']:
            p=future.parent/r['path'];need(sha(p)==r['sha256'] and p.stat().st_size==r['bytes'],'future review bytes')
    script=repo/'scripts/verify_snapshot.py';old=subprocess.check_output(['git','show',BASE+':scripts/verify_snapshot.py'],cwd=repo,text=True)
    trees=[ast.parse(old),ast.parse(script.read_text())];defs=lambda t:{x.name:x for x in t.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))};before,after=map(defs,trees)
    prior=load(cdir/'prior_guard_asts.json');names=[]
    for name,n in before.items():
        if name=='main':continue
        need(ast.dump(n,include_attributes=False)==ast.dump(after[name],include_attributes=False)==prior[name],'changed prior guard '+name);names.append(name)
    need(len(names)==36 and set(after)-set(before)=={'check_topic_g_measurement'},'one new guard')
    nondef=lambda t:[ast.dump(x,include_attributes=False) for x in t.body if not isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))]
    need(nondef(trees[0])==nondef(trees[1]),'changed top-level verifier configuration')
    calls=lambda n:[x.func.id for x in ast.walk(n) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id.startswith('check_')]
    c0,c1=calls(before['main']),calls(after['main']);need([x for x in c1 if x!='check_topic_g_measurement']==c0 and c1.count('check_topic_g_measurement')==1,'old main checks changed')
    setup=load(cdir/'setup.json');admission=load(repo/P/'admission.json');copies=[];total=0
    for row in setup['packets']:
        x,y=study/row['source'],repo/P/row['folder'];need(sha(x/'manifest.json')==sha(y/'manifest.json')==row['pin']==admission['packet_manifests'][row['folder']],'exact archive manifest')
        exports=load(x/'manifest.json')['exports'];need(len(exports)==row['exports'],'archive export count')
        for e in exports:
            p,q=x/e['path'],y/e['path'];need(p.read_bytes()==q.read_bytes() and sha(q)==e['sha256'] and q.stat().st_size==e['bytes'],'exact frozen copy')
        total+=len(exports);copies.append(row)
    need(total==69 and len(copies)==7 and len(admission['artifacts'])==76,'archive closure')
    for e in admission['artifacts']:
        p=repo/e['path'];need(sha(p)==e['sha256'] and p.stat().st_size==e['bytes'],'admission export')
    mapping=load(repo/P/'recount_mapping.json');routes=mapping['routes'];need(len(routes)==35,'mapping')
    for row in routes:
        p=repo/row['public_path'] if row['public_path'] else study/row['private_path'];need(sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'mapped input '+row['private_path'])
        if row['public_path']:
            committed=subprocess.check_output(['git','show',BASE+':'+row['public_path']],cwd=repo)
            need(p.read_bytes()==committed,'scientific byte changed from baseline')
    need(sum(x['public_path']is not None for x in routes)==33 and sum(x['public_path']is None for x in routes)==2,'public/primary boundary')
    need(not any(x.startswith('papers/') for x in changed-bound),'unreviewed scientific change')
    spec=importlib.util.spec_from_file_location('g_publication_integration',script);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    positive=m.check_topic_g_measurement();need(positive==(180,270),'new guard result')
    old_result=m.check_topic_g_proofs();need(old_result==(79,40),'prior science guard')
    original=m.load;controls=[]
    def control(name,target,change):
        def patched(path):
            d=original(path)
            if str(path)==target:d=copy.deepcopy(d);change(d)
            return d
        m.load=patched
        try:m.check_topic_g_measurement()
        except (ValueError,RuntimeError) as e:controls.append(dict(name=name,rejected=True,reason=str(e),mechanism='Parsed record mutation; actual file hashes remain enabled.'))
        else:raise ValueError('accepted mutation '+name)
        finally:m.load=original
    control('artifact_hash',P+'admission.json',lambda d:d['artifacts'][0].update(sha256='0'*64))
    control('old_input_as_current',P+'admission.json',lambda d:d['packet_manifests'].update(inputs=d['packet_manifests']['original_inputs']))
    control('mislabel_old_input',P+'admission.json',lambda d:d.update(original_input_not_current=False))
    control('incorrect_late_fraction',P+'packet/measurement.json',lambda d:d['coordinates'][-1]['combined']['written'].update(numerator=1))
    control('drop_whole_common',P+'packet/measurement.json',lambda d:d['coordinates'][0].update(written_denominator=1))
    control('conditional_not_prepaid',P+'packet/measurement.json',lambda d:d['boundary'].update(conditional='Only application'))
    control('printed_and_raw_both_charged',P+'packet/measurement.json',lambda d:d['coordinates'][0]['combined']['including_raw_programs'].update(denominator=d['coordinates'][0]['written_denominator']+d['coordinates'][0]['document_costs']['CODE']+d['coordinates'][0]['raw_costs']['complete_programs']))
    control('wrong_cover_sensitivity',P+'packet/measurement.json',lambda d:d['cover_sensitivity']['article_only_coordinates'][0].update(L009_article_only=1))
    control('cover_removed_from_primary',P+'packet/measurement.json',lambda d:d['cover_sensitivity'].update(primary_includes_cover=False))
    control('discard_validations',P+'packet/measurement.json',lambda d:d['boundary'].update(complete_programs=6,validation_programs=0))
    control('wrong_formal_count',P+'admission.json',lambda d:d.update(scoped_Lean_declarations=80))
    control('full_formalization',P+'admission.json',lambda d:d.update(source_specific_formalization=True))
    control('invent_paired_DAG_acceptance',P+'admission.json',lambda d:d.update(paired_dependency_audit_complete=True))
    control('unknown_BDL_zero',P+'admission.json',lambda d:d['unknown_external_costs'].update(retained_BDL_full_proof=0))
    control('unknown_Kantor_zero',P+'admission.json',lambda d:d['unknown_external_costs'].update(retained_Kantor_full_proof=0))
    control('cross_topic_discount',P+'packet/measurement.json',lambda d:d['boundary'].update(cross_topic_discount=True))
    control('new_question_credit',P+'admission.json',lambda d:d.update(new_question_credit=1))
    control('new_source_credit',P+'admission.json',lambda d:d.update(new_source_credit=1))
    control('false_sawtooth',P+'packet/measurement.json',lambda d:d['boundary'].update(sawtooth_claim=True))
    control('missing_route',P+'recount_mapping.json',lambda d:d['routes'].pop())
    control('unsafe_public_route',P+'recount_mapping.json',lambda d:d['routes'][0].update(public_path='/tmp/unreviewed.pdf'))
    control('wrong_public_route',P+'recount_mapping.json',lambda d:d['routes'][0].update(public_path='README.rst'))
    control('source_pdf_exported',P+'recount_mapping.json',lambda d:d.update(primary_exported=True))
    control('wrong_primary_bytes',P+'recount_mapping.json',lambda d:d['routes'][-1].update(sha256='0'*64))
    control('erased_source_qualification',P+'inputs/source_contract_boundary.json',lambda d:d.update(qualification='All assertions recovered'))
    control('missing_source_record',P+'inputs/source_contract_boundary.json',lambda d:d['source_rows'].pop())
    control('different_scientific_admission',P+'admission.json',lambda d:d.update(proof_admission_sha256='0'*64))
    control('promote_accepted_bad_control',P+'root_adoption/fresh_independent_replay.json',lambda d:d['arithmetic_controls'][0].update(rejected=False))
    need(m.check_topic_g_measurement()==positive,'restored guard')
    boundary_controls=[]
    for path in [P+'unreviewed_extra.json',P+'publication_review/unlisted.json','papers/topic-g/v2/extra.tex']:
        try:changes(bound|{path},bound)
        except ValueError as e:boundary_controls.append(dict(path=path,rejected=True,reason=str(e)))
        else:raise ValueError('unlisted future addition accepted')
    links=[]
    for name in ['README.rst','audit/completion.rst',P+'README.rst']:
        text=(repo/name).read_text();refs=re.findall(r'<([^<>]+)>`_',text)+re.findall(r'^\.\. image::\s*(\S+)',text,re.M)
        for ref in refs:
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',ref):continue
            target=ref.split('#')[0]
            if target:need(((repo/name).parent/target).exists(),'broken local link '+name+' '+target);links.append(dict(document=name,target=target))
    adapter_path=repo/P/'replay_inputs.py';spec=importlib.util.spec_from_file_location('g_public_adapter_review',adapter_path);adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
    need(adapter.ROOT==repo,'adapter repository root');adapter_controls=[]
    for path in ['/tmp/file','../secret','sources/../../secret']:
        try:adapter.relative(path)
        except ValueError as e:adapter_controls.append(dict(control='unsafe route '+path,rejected=True,reason=str(e)))
        else:raise ValueError('unsafe adapter route accepted')
    with tempfile.TemporaryDirectory(prefix='g-adapter-publication-review-') as td:
        temp=Path(td);bad=temp/'bad.pdf';bad.write_bytes(b'not an accepted source PDF')
        proc=subprocess.run(['python3','-B','-O',str(adapter_path),'--linear-source-pdf',str(bad),'--steiner-source-pdf',str(bad),'--out',str(temp/'result')],capture_output=True,text=True)
        need(proc.returncode!=0 and 'Changed recount input sources/linear_triality2026_published.pdf' in proc.stderr and not (temp/'result').exists(),'bad supplied source rejected before extraction')
        adapter_controls.append(dict(control='wrong supplied primary bytes',rejected=True,reason='Rejected at source hash before invoking extraction; no output directory created.'))
    public_out=a.out.parent/(a.out.stem+'_arithmetic');need(not public_out.exists(),'fresh public arithmetic path')
    cmd=['python3','-B','-O',str(repo/P/'arithmetic_review/check.py'),'--inputs',str(repo/P/'inputs'),'--input-review',str(repo/P/'input_review'),'--input-adoption',str(repo/P/'input_adoption'),'--numbers',str(repo/P/'packet'),'--out',str(public_out)]
    run=subprocess.run(cmd,cwd=repo,capture_output=True,text=True);need(run.returncode==0,'public arithmetic command failed '+run.stderr);replay=load(public_out/'report.json')
    need(replay['all_exact_fractions']==270 and replay['bar_rectangles_checked']==9,'public arithmetic extent')
    report=dict(status='PASS_BOUNDED_G_MEASUREMENT_PUBLICATION_INTEGRATION',baseline=BASE,candidate_sha256=CANDIDATE,candidate_files=88,changed_files_at_replay=len(changed),allowed_exact_later_paths=sorted(LATER),prefix_wildcards=False,prior_guards_unchanged=names,prior_main_calls_preserved=True,new_guard_result=positive,old_scientific_guard_result=old_result,archive_packets=copies,exact_exports=total,admission_artifacts=76,public_routes_unchanged_from_baseline=33,private_primary_hash_routes=2,controls=controls,boundary_controls=boundary_controls,adapter_controls=adapter_controls,relative_links=links,public_command=dict(argv=cmd,returncode=run.returncode,stdout=run.stdout,report_sha256=sha(public_out/'report.json')),primary=admission['primary'],source_or_font_reextraction=False,scientific_GAP_or_Lean_replay=False,public_edits=False,independence='Reviewer authored Topic G science and independently reviewed prior numbers. This review only checks root-authored publication integration; distinct scientific/input acceptance and root numerical adoption remain authoritative.')
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status=report['status'],controls=len(controls),boundary_controls=len(boundary_controls),archives=len(copies),exports=total,links=len(links),result=positive)))
if __name__=='__main__':main()
