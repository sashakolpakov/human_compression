#!/usr/bin/env python3
"""Bounded, read-only affine publication integration review.

Frozen mathematical review is retained, not repeated. Corruptions are isolated
temporary files or in-memory metadata overrides, never checkout mutations.
"""
import argparse, ast, copy, hashlib, importlib.util, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.dont_write_bytecode=True
BASE='7118bdc803c1679baea1f8378c470df2ce84e847'
AUTHOR='88d909a728b375c275bf7658004e33286d14aad15ad0480c13bbe3fc9aa0d83f'
REVIEW='44d41e8f2038f129e93437efbc3e2558e26e18328593b13726d33dd2eda325b1'
PAPER='papers/topic-affine/v2/'
AUDIT='audit/topic-affine/v2/'
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def tree(n):return ast.dump(n,include_attributes=False)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh report');root=a.public_root.resolve();study=a.study_root.resolve()
    admission=load(root/AUDIT/'admission.json');verifier=root/'scripts/verify_snapshot.py'
    spec=importlib.util.spec_from_file_location('affine_publication_snapshot',verifier);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    need(v.check_affine_proofs()==(33,9),'positive affine check')
    catalogue_result=v.check_catalogue();copies=[]
    for priv,pub,h,count in [('topic_Affine_volume',PAPER,AUTHOR,88),('topic_Affine_volume_independent_review',AUDIT+'independent_review/',REVIEW,53)]:
        original=study/priv;current=root/pub;need(sha((current/'manifest.json').read_bytes())==h,'independent manifest pin')
        need((original/'manifest.json').read_bytes()==(current/'manifest.json').read_bytes(),'identical manifest relocation')
        m=load(current/'manifest.json');need(len(m['exports'])==count,'complete export count')
        for b in m['exports']:
            n=Path(b['path']);need(not n.is_absolute() and '..' not in n.parts,'safe frozen path')
            data=(current/n).read_bytes();need(data==(original/n).read_bytes() and len(data)==b['bytes'] and sha(data)==b['sha256'],'unchanged frozen export '+str(n))
        copies.append({'private':priv,'public':pub,'exports':count,'byte_identical':True})
    for b in admission['artifacts']:
        n=Path(b['path']);need(not n.is_absolute() and '..' not in n.parts,'safe admission path')
        data=(root/n).read_bytes();need(len(data)==b['bytes'] and sha(data)==b['sha256'],'exact admitted byte binding')
    need(len(admission['artifacts'])==144,'complete 144-file admission')
    oldtext=subprocess.check_output(['git','show',BASE+':scripts/verify_snapshot.py'],cwd=root,text=True)
    funcs=lambda s:{n.name:n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
    old,new=funcs(oldtext),funcs(verifier.read_text());need(set(new)-set(old)=={'check_affine_proofs'} and set(old)<=set(new),'only affine checker added')
    preserved=[n for n in old if n!='main'];need(all(tree(old[n])==tree(new[n]) for n in preserved),'all old checker ASTs unchanged')
    stripped=copy.deepcopy(new['main']);before={tree(n) for n in old['main'].body};extra=[n for n in stripped.body if tree(n) not in before]
    need(len(extra)==2 and any('check_affine_proofs' in tree(n) for n in extra) and any('affine_declarations' in tree(n) for n in extra),'only new call and result line')
    stripped.body=[n for n in stripped.body if tree(n) in before];need(tree(stripped)==tree(old['main']),'old main statements/order preserved')
    for n in ['scripts/build_papers.py','research/case_study/formal/lakefile.lean','audit/intake.json','audit/source_registry.json']:
        need(subprocess.check_output(['git','show',BASE+':'+n],cwd=root)==(root/n).read_bytes(),'unchanged baseline '+n)
    cat=load(root/'papers/catalogue.json');prior=json.loads(subprocess.check_output(['git','show',BASE+':papers/catalogue.json'],cwd=root))
    affine=[r for r in cat['new_editions'] if r['topic']=='Affine'];need(affine==admission['catalogue_entries'] and len(affine)==2,'two scientific paper catalogue records')
    cleaned=copy.deepcopy(cat);cleaned['new_editions']=[r for r in cleaned['new_editions'] if r['topic']!='Affine'];del cleaned['current_topic_editions']['Affine'];need(cleaned==prior,'all previous catalogue routes unchanged')
    need([(r['application_id'],r['source_contracts'],r['physical_pages']) for r in affine]==[('U_Affine',[],7),('Affine1',['L012'],9)],'exact common/application/source/page mapping')
    need(admission['source_ids']==['L012'] and admission['source_rows']==33 and admission['fresh_lean_declarations']==9 and admission['new_lean_declarations']==2 and admission['reused_lean_declarations']==7,'exact public source and formal summary')
    need(admission['project_total_preserved']==27 and admission['new_source_credit']==admission['new_question_credit']==0 and admission['compression_ratio'] is None,'no new credit or ratio')
    need(not admission['end_to_end_source_formalization'],'formal scope retained')
    build=load(root/AUDIT/'publication_replay/catalogue_text_check.json');need(build=={'status':'PASS','papers':[{'id':r['id'],'pages':r['physical_pages'],'exact_page_text':True} for r in affine],'scope':'Direct isolated catalogue compilation and exact text equality; full mathematical replay is in the independent review.'},'fresh isolated public builder evidence')
    added=subprocess.check_output(['git','diff','--cached','--name-only','--diff-filter=ACMR',BASE,'--','*.md'],cwd=root,text=True);need(not added.strip(),'no local Markdown published')
    docs=['README.rst','audit/completion.rst',PAPER+'PUBLICATION.rst',PAPER+'README.rst',AUDIT+'independent_review/README.rst'];links=[]
    for n in docs:
        for raw in re.findall(r'<([^>]+)>`_',(root/n).read_text(),re.S):
            url=''.join(raw.split())
            if re.match(r'^[a-zA-Z]+:',url) or url.startswith('#'):continue
            need(((root/n).parent/url.split('#')[0]).exists(),'public reader link '+n+' -> '+url);links.append({'document':n,'target':url})
    controls=[]
    with tempfile.TemporaryDirectory(prefix='affine-publication-controls-') as td:
        temp=Path(td)
        for n in {b['path'] for b in admission['artifacts']}|{AUDIT+'admission.json','papers/catalogue.json'}:
            dest=temp/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/n,dest)
        v.ROOT=temp
        for name,n in [('proof_bytes',PAPER+'sections/04-periods.tex'),('program_bytes',PAPER+'programs/phase250_base384_census.g'),('review_bytes',AUDIT+'independent_review/review.json')]:
            f=temp/n;data=f.read_bytes();f.write_bytes(data+b'\n')
            try:v.check_affine_proofs()
            except (ValueError,KeyError) as e:controls.append({'name':name,'mode':'temporary file mutation','rejected':True,'reason':str(e)})
            else:raise ValueError('accepted corrupt frozen bytes '+name)
            f.write_bytes(data)
    v.ROOT=root;actual=v.load
    for name in ['invent_ratio','new_source','wrong_source','wrong_formal_count','wrong_new_formal_count','wrong_page_count','full_formal','omit_row','omit_program','custom_axiom','omit_tex_input','wrong_catalogue_source']:
        overrides={};ad=copy.deepcopy(admission);sc=actual(PAPER+'scope.json');catalogue=actual('papers/catalogue.json')
        if name=='invent_ratio':ad['compression_ratio']=2
        elif name=='new_source':ad['new_source_credit']=1
        elif name=='wrong_source':ad['source_ids']=['L035']
        elif name=='wrong_formal_count':ad['fresh_lean_declarations']=99
        elif name=='wrong_new_formal_count':ad['new_lean_declarations']=99
        elif name=='wrong_page_count':ad['scientific_pages']=99
        elif name=='full_formal':ad['end_to_end_source_formalization']=True
        elif name=='omit_row':sc['source_rows'].pop();overrides[PAPER+'scope.json']=sc
        elif name=='omit_program':sc['programs'].pop();overrides[PAPER+'scope.json']=sc
        elif name=='custom_axiom':
            fresh=actual(AUDIT+'independent_review/fresh_replay/report.json');fresh['axiom_reports'][0][1]='[sorryAx]';overrides[AUDIT+'independent_review/fresh_replay/report.json']=fresh
        elif name=='omit_tex_input':
            next(r for r in catalogue['new_editions'] if r['id']=='topic-affine/v2/umbrella')['tex_inputs'].pop();ad['catalogue_entries'][0]['tex_inputs'].pop();overrides['papers/catalogue.json']=catalogue
        else:
            next(r for r in catalogue['new_editions'] if r['id']=='topic-affine/v2/mixed-prime-polyhedra')['source_contracts']=['L035'];ad['catalogue_entries'][1]['source_contracts']=['L035'];overrides['papers/catalogue.json']=catalogue
        overrides[AUDIT+'admission.json']=ad
        v.load=lambda path:copy.deepcopy(overrides[path]) if path in overrides else actual(path)
        try:v.check_affine_proofs()
        except (ValueError,KeyError) as e:controls.append({'name':name,'mode':'in-memory semantic guard isolation','rejected':True,'reason':str(e)})
        else:controls.append({'name':name,'rejected':False})
        finally:v.load=actual
    need(all(r['rejected'] for r in controls),'all semantic controls rejected: '+str(controls))
    files=['scripts/verify_snapshot.py','papers/catalogue.json','README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/work_queue.json',PAPER+'PUBLICATION.rst',AUDIT+'admission.json',AUDIT+'root_integration.json',AUDIT+'publication_replay/catalogue_text_check.json']
    whitespace=subprocess.run(['git','diff','--cached','--check',BASE],cwd=root,text=True,capture_output=True)
    exceptions=re.findall(r'^([^:\n]+):(\d+): trailing whitespace\.$',whitespace.stdout,re.M)
    expected_suffixes=['census384.stdout','kernel64.stdout','kernel66.stdout','phase2_cubic_kernel_check.log']
    need(len(exceptions)==7 and all(any(n.endswith(s) for s in expected_suffixes) for n,line in exceptions),'exact seven preserved frozen log whitespace exceptions')
    report={'status':'PASS_BOUNDED_AFFINE_PUBLICATION_REVIEW','baseline_commit':BASE,'copies':copies,'admission_artifacts':144,'source_rows':33,'formal_declarations':9,'new_formal_declarations':2,'reused_formal_declarations':7,'catalogue_result':catalogue_result,'old_non_main_ASTs_preserved':len(preserved),'main_changes':'Only affine call and result line','previous_catalogue_and_builds_preserved':True,'checked_local_links':links,'controls':controls,'frozen_log_whitespace_exceptions':[{'path':n,'line':int(line)} for n,line in exceptions],'bound_public_files':[{'path':n,'bytes':(root/n).stat().st_size,'sha256':sha((root/n).read_bytes())} for n in files],'full_math_source_program_or_Lean_review_repeated':False,'local_Markdown_published':False,'public_mutation_by_reviewer':False,'project_principal_total':27,'new_source_credit':0,'new_question_credit':0,'compression_ratio':None}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','source_rows','formal_declarations','old_non_main_ASTs_preserved','catalogue_result']}))
if __name__=='__main__':main()
