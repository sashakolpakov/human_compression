#!/usr/bin/env python3
"""Bounded independent publication audit; no repeated Lean/kernel compilation."""
from pathlib import Path
import argparse,ast,copy,hashlib,importlib.util,json,re,subprocess,tempfile
BASE='2d631760842796450899761f8763b0e9a9ff4b77'
PIN='26d9f31411049a760b3cd475428147800713acbb56646084211bc6847dd1cde3'
A='audit/topic-d/v2/support-formal/'
P='papers/topic-d/v2/support-formal/'
MAPPING=[(P,'topic_D_global_support_formal',20),
         (A+'first_supplement/','topic_D_support_formal',13),
         (A+'independent_review/','topic_D_global_support_independent_review',15)]
def need(ok,message):
    if not ok:raise ValueError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--public-root',type=Path,required=True)
    ap.add_argument('--study-root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'Fresh output required')
    root=a.public_root;admission=read(root/A/'admission.json')
    need(sha(root/A/'admission.json')==PIN,'Admission changed')
    copies=[]
    for pub,private,n in MAPPING:
        x=root/pub;y=a.study_root/private
        need((x/'manifest.json').read_bytes()==(y/'manifest.json').read_bytes(),'Exact manifest copy '+private)
        manifest=read(y/'manifest.json');need(len(manifest['exports'])==n,'Exact export count '+private)
        for row in manifest['exports']:
            xx=x/row['path'];yy=y/row['path']
            need(xx.read_bytes()==yy.read_bytes() and xx.stat().st_size==row['bytes'] and sha(xx)==row['sha256'],
                 'Exact frozen export '+private+'/'+row['path'])
        copies.append(dict(private=private,public=pub,exports=n,manifest_sha256=sha(x/'manifest.json')))
    for row in admission['artifacts']+admission['retained_public_bindings']:
        p=root/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Exact public binding '+row['path'])
    need(len(admission['artifacts'])==53 and len(admission['retained_public_bindings'])==4,'Complete declared bindings')
    for row in admission['retained_public_bindings']:
        need((root/row['path']).read_bytes()==(a.study_root/row['original_private_path']).read_bytes(),'Retained input mapping')
    old=subprocess.check_output(['git','show',BASE+':scripts/verify_snapshot.py'],cwd=root,text=True)
    new=(root/'scripts/verify_snapshot.py').read_text()
    def funcs(t):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(t).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    before,after=funcs(old),funcs(new);unchanged=set(before)-{'main'}
    need(len(unchanged)==24 and all(before[k]==after[k] for k in unchanged),'All 24 prior non-main verifier ASTs unchanged')
    need(set(after)-set(before)=={'check_topic_d_support_formal'},'Only declared new verifier function')
    changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=root,text=True).splitlines()
    protected=[p for p in changed if (p.startswith(('papers/','research/')) and not p.startswith(P))
               or p in ['audit/topic-d/v2/admission.json','audit/completion.json','audit/source_registry.json']
               or p.startswith(('audit/topic-a/','audit/topic-b/','audit/topic-c/','audit/topic-e/'))]
    need(not protected,'Earlier scientific/proof/measurement bytes changed')
    for base in [root/P,root/A]:
        for p in base.rglob('*'):
            if p.is_file():need(p.suffix.lower() not in {'.pdf','.png','.jpg','.jpeg','.md','.olean'},'Unplanned primary/raster/cache artifact')
    docs=[root/'README.rst',root/'audit/completion.rst',root/A/'README.rst',root/P/'README.rst',root/A/'independent_review/README.rst',root/A/'first_supplement/README.rst']
    links=[]
    for doc in docs:
        for target in re.findall(r'<([^<>]+)>`_',doc.read_text()):
            if '://' in target or target.startswith('#'):continue
            need((doc.parent/target.split('#')[0]).exists(),'Broken relative link '+str(doc)+':'+target)
            links.append(dict(document=str(doc.relative_to(root)),target=target))
    spec=importlib.util.spec_from_file_location('support_public_verifier',root/'scripts/verify_snapshot.py')
    v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    need(v.check_topic_d_support_formal()==28,'New standard verifier returns 28')
    original=v.load;controls=[]
    cases=[
      ('double_count_first_twelve','admission.json',lambda x:x.update(declaration_reports=40)),
      ('incorrect_first_module_count','admission.json',lambda x:x.update(first_module_reports=99)),
      ('incorrect_global_module_count','admission.json',lambda x:x.update(global_module_reports=99)),
      ('claim_divisor_bridge','admission.json',lambda x:x.update(divisor_poset_and_number_theoretic_mobius_bridge_verified=True)),
      ('claim_end_to_end_source','admission.json',lambda x:x.update(end_to_end_source_formalization=True)),
      ('claim_source_instances','admission.json',lambda x:x.update(source_specific_hypotheses_verified=True)),
      ('inflate_source_credit','admission.json',lambda x:x.update(new_source_credit=1)),
      ('invent_factor','admission.json',lambda x:x.update(compression_ratio=2)),
      ('missing_rejected_mutation','independent_review/fresh_report.json',lambda x:x['Lean_mutations'].pop()),
      ('custom_axiom','independent_review/fresh_report.json',lambda x:x['modules'][0]['axioms'][0]['axioms'].append('UnprovedCustomAxiom')),
      ('wrong_compiled_source','independent_review/fresh_report.json',lambda x:x['modules'][0]['source'].update(sha256='0'*64)),
      ('review_not_accepted','independent_review/review.json',lambda x:x.update(status='PENDING')),
      ('missing_retained_binding','admission.json',lambda x:x['retained_public_bindings'].pop())]
    for name,path,change in cases:
        full=A+path;mut=copy.deepcopy(original(full));change(mut)
        v.load=lambda p,full=full,mut=mut:copy.deepcopy(mut) if p==full else original(p)
        try:v.check_topic_d_support_formal()
        except (ValueError,KeyError) as error:controls.append(dict(name=name,rejected=True,reason=str(error),mode='Parsed-object mutation; all public files unchanged'))
        else:raise ValueError('Accepted mutation '+name)
        finally:v.load=original
    with tempfile.TemporaryDirectory(prefix='support-public-binding-') as d:
        f=Path(d)/'proof.lean';f.write_text('example : True := True.intro\n');row=dict(path=f.name,bytes=f.stat().st_size,sha256=sha(f));f.write_text('axiom bad : False\n');oldroot=v.ROOT;v.ROOT=Path(d)
        try:v.check_bindings([row])
        except ValueError as error:controls.append(dict(name='changed_bound_proof_bytes',rejected=True,reason=str(error),mode='Temporary file only'))
        else:raise ValueError('Changed source bytes accepted')
        finally:v.ROOT=oldroot
    bindings={str(p.relative_to(root)):sha(p) for p in docs+[root/'audit/work_queue.json',root/'scripts/verify_snapshot.py',root/A/'root_integration.json']}
    report=dict(status='PASS_BOUNDED_INDEPENDENT_D_SUPPORT_PUBLICATION_REVIEW',baseline_commit=BASE,admission_sha256=PIN,
        frozen_packet_copies=copies,exact_copied_exports=48,public_artifact_bindings=53,retained_public_bindings=4,
        previous_non_main_verifier_ASTs_unchanged=24,standard_verifier_result=28,protected_files_changed=protected,
        checked_relative_links=len(links),controls=controls,reader_bindings=bindings,
        new_Lean_compilation_in_this_review=False,full_mathematical_review_repeated=False,
        full_formal_review_retained='cf448c43799ca312e9041f7f7bb6edc250be87669b7bb3d0e4bda8df959d0130',
        count_interpretation='28 reports contain the unchanged first 12 once plus 16 further reports. Neither 28 independent theorems nor 12+28 distinct reports is asserted.',
        source_specific_applications_formalized=False,new_source_credit=0,new_question_credit=0,compression_ratio=None,public_files_modified=False)
    a.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','exact_copied_exports','public_artifact_bindings','retained_public_bindings','previous_non_main_verifier_ASTs_unchanged','standard_verifier_result','checked_relative_links']}))
if __name__=='__main__':main()
