#!/usr/bin/env python3
"""Portable authored replay. Finite diagnostics do not establish uniform proofs."""
import argparse,hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
from migration_check import audit as migration_audit
ROOT=Path(__file__).resolve().parent

def need(ok,m):
    if not ok:raise RuntimeError('L126_REJECT '+m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def run(out,label,argv,cwd,env=None,success=True):
    start=time.monotonic();r=subprocess.run(list(map(str,argv)),cwd=cwd,env=env,capture_output=True,text=True,timeout=300)
    (out/(label+'.stdout')).write_text(r.stdout);(out/(label+'.stderr')).write_text(r.stderr)
    need((r.returncode==0)==success,label+' exit '+str(r.returncode)+' '+(r.stdout+r.stderr)[-700:])
    if success:need(not re.search(r'Error,|error:',r.stdout+r.stderr),label+' reported error')
    return {'label':label,'seconds':round(time.monotonic()-start,3),'returncode':r.returncode,'expected_success':success}

def scope():
    m=ROOT/'manifest.json'
    if m.exists():
        for e in read(m)['exports']:
            p=ROOT/e['path'];need(p.is_file() and not p.is_symlink() and len(p.read_bytes())==e['bytes'] and sha(p)==e['sha256'],'export '+e['path'])
    migration_audit(ROOT)
    c=read(ROOT/'source_contract.json');old=read(ROOT/'provenance/phase197_source_contract.json')
    need([r['id'] for r in c['rows']]==[r['id'] for r in old['rows']],'all31 previous source rows')
    need(len(c['rows'])==31 and c['principal_credit']==0,'author admission scope')
    need(c['status']=='AUTHOR_COMPLETE_CORRECTED_CONTRACT_PENDING_INDEPENDENT_REVIEW','complete declared contract')
    need(all(x['status']!='OPEN_AUTHOR_OBLIGATION_PRINTED_HYPOTHESES' for x in c['rows']),'no unfinished declared clause')
    for r in c['rows']:need((ROOT/r['current_proof']).is_file(),'proof route '+r['id'])
    for e in read(ROOT/'migration.json')['unchanged_old_sections']:
        need(e['byte_identical'] and e['old_sha256']==e['new_sha256']==sha(ROOT/e['new']),'unchanged old proof '+e['new'])
    for e in read(ROOT/'program_inventory.json')['files']:
        need(sha(ROOT/e['path'])==e['sha256'] and len((ROOT/e['path']).read_bytes())==e['bytes'],'whole program '+e['path'])
    for e in read(ROOT/'program_inventory.json')['mandatory_data']:
        need(sha(ROOT/e['path'])==e['sha256'] and len((ROOT/e['path']).read_bytes())==e['bytes'],'whole mandatory data '+e['path'])
    for e in read(ROOT/'formal/scope.json')['modules']:
        need(sha(ROOT/e['path'])==e['sha256'],'formal scope bytes '+e['path'])
    for e in read(ROOT/'proof_map.json')['contexts']:
        t=(ROOT/e['path']).read_text();need(hashlib.sha256(t[e['start']:e['end']].encode()).hexdigest()==e['sha256'],'exact proof context '+e['id'])
    return {'source_rows':31,'retained_F010_blocks':6,'retained_original_F010_sections':8,'unchanged_original_F010_sections':5,'status':c['status'],'programs':10,'required_programs':1,'optional_validation':9,'mandatory_data_files':1}

def programs(out,stage):
    p=stage/'programs';runs=[]
    runs.append(run(out,'required_graph',[sys.executable,'-B','-O',stage/'certificate/check.py','--out',out/'required_graph.json'],stage))
    cert=read(out/'required_graph.json');need(cert['status']=='PASS' and len(cert['controls'])==7,'required complete graph certificate')
    runs.append(run(out,'optional_graph_backends',[sys.executable,'-B','-O',stage/'certificate/diagnostic.py','--out',out/'optional_graph_backends.json'],stage))
    runs.append(run(out,'finite_models',[sys.executable,'-B','-O',p/'phase197_finite_models.py','--output',out/'models.json','--gap-output',out/'models.g'],stage))
    text='P197Data := '+json.dumps(str(out/'models.g'))+';; Read('+json.dumps(str(p/'phase197_finite_groups.g'))+');'
    runs.append(run(out,'finite_groups',['/opt/homebrew/bin/gap','-q','-T','-c',text],stage))
    groups=read(out/'finite_groups.stdout');cases=read(out/'models.json')['cases']
    need(len(cases)==len(groups['rows'])==21,'21 finite models')
    need([(r['name'],[r['typed'],r['correlations']]) for r in groups['rows']]==[(r['name'],r['expected_groups']) for r in cases],'full exact group comparisons')
    runs.append(run(out,'free_words',[sys.executable,'-B','-O',p/'phase197_free_basis_check.py','--output',out/'free_words.json'],stage))
    need([r['reduced_words'] for r in read(out/'free_words.json')['words']]==[23437,22409],'bounded free word coverage')
    runs.append(run(out,'projective',[sys.executable,'-B','-O',p/'phase196_cross_ratio_check.py','--output',out/'projective.json'],stage))
    runs.append(run(out,'panels',[sys.executable,'-B','-O',p/'panel_permutations.py','--out',out/'panels.json'],stage))
    for name in ['phase177_hexagon_check','phase188_gadget_check','ordered_arms']:
        runs.append(run(out,name,['/opt/homebrew/bin/gap','-q','-T',p/(name+'.g')],stage))
    runs.append(run(out,'bad_prefix',[sys.executable,'-B','-O',p/'phase197_free_basis_check.py','--alter-prefix','--output',out/'bad_prefix.json'],stage,success=False))
    runs.append(run(out,'bad_petersen',[sys.executable,'-B','-O',p/'phase197_finite_models.py','--alter-petersen','--output',out/'bad_petersen.json','--gap-output',out/'bad_petersen.g'],stage,success=False))
    runs.append(run(out,'bad_panel',[sys.executable,'-B','-O',p/'panel_permutations.py','--alter-first','--out',out/'bad_panel.json'],stage,success=False))
    need('last-occurrence cut criterion' in (out/'bad_prefix.stderr').read_text(),'prefix rejection reason')
    need('altered Petersen cross-incidence' in (out/'bad_petersen.stderr').read_text(),'Petersen rejection reason')
    need('labeled panel adjacency' in (out/'bad_panel.stderr').read_text(),'panel rejection reason')
    return {'runs':runs,'program_files':10,'required':1,'mandatory_data_files':1,'optional_validation':9,'negative_controls':10,'uniform_proofs_from_samples':False}

def formal(out,stage,packages,lean):
    f=stage/'formal';dep=read(f/'dependency_manifest.json');libs=[]
    for row in dep['packages']:
        p=packages/row['name'];rev=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()
        need(rev==row['rev'],'dependency revision '+row['name'])
        need(subprocess.run(['git','-C',str(p),'diff','--quiet','HEAD','--']).returncode==0,'unmodified dependency source '+row['name'])
        lib=p/'.lake/build/lib/lean'
        if lib.is_dir():libs.append(str(lib))
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(libs);env['ELAN_TOOLCHAIN']=dep['lean']
    version=subprocess.check_output([str(lean),'--version'],text=True);need('version 4.32.2' in version,'Lean version')
    expected={'RecognizableRestriction':8,'CompletedHexagonCounterexample':4,'BasisPermutation':3,'ShadowFiberKernel':7}
    reports={};runs=[]
    for name,count in expected.items():
        p=f/(name+'.lean');t=p.read_text();need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*(axiom|constant)\s',t,re.M),'formal forbidden shortcut '+name)
        runs.append(run(out,name,[lean,'-o',out/(name+'.olean'),p],stage,env))
        rows=re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",(out/(name+'.stdout')).read_text())
        need(len(rows)==count,'actual axiom reports '+name)
        reports[name]={}
        for n,b in rows:
            axioms={x.strip() for x in b.split(',') if x.strip()};need(axioms<= {'propext','Classical.choice','Quot.sound'},'standard axioms '+n);reports[name][n]=sorted(axioms)
    return {'declarations':sum(expected.values()),'modules':reports,'runs':runs,'source_dependencies_checked':True,'cached_dependency_objects_trusted':True,'application_geometry_formalized':False,'new_panel_theorem_formalized':False}

def render(out,stage,xelatex):
    from pypdf import PdfReader
    v=stage/'volume';rows=[]
    for name in ['umbrella','finite-normal-pairs','representations-by-incidence','program-appendix']:
        d=out/name;d.mkdir()
        for n in [1,2]:run(out,name+'_render'+str(n),[xelatex,'-recorder','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(d),name+'.tex'],v)
        log=(d/(name+'.log')).read_text();bad=[s for s in log.splitlines() if re.search(r'Missing character:|Overfull|undefined references|undefined on input',s)]
        need(not bad,'render diagnostics '+name+str(bad))
        pdf=d/(name+'.pdf');texts=[p.extract_text() or '' for p in PdfReader(pdf).pages]
        old=v/(name+'.pdf');match=None
        if old.exists():match=texts==[p.extract_text() or '' for p in PdfReader(old).pages];need(match,'exact rendered page text '+name)
        rows.append({'name':name,'pages':len(texts),'sha256':sha(pdf),'page_text_sha256':[hashlib.sha256(t.encode()).hexdigest() for t in texts],'matched_frozen_page_text':match})
    return rows

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--programs',action='store_true');a.add_argument('--study-root',type=Path);a.add_argument('--formal',action='store_true');a.add_argument('--render',action='store_true');a.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'));a.add_argument('--lean',type=Path,default=Path('/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'));a.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');args=a.parse_args()
    out=args.out.resolve();need(not out.exists(),'fresh output');out.mkdir(parents=True);s=scope();stage=out/'source';stage.mkdir()
    for sub in ['volume','programs','formal','certificate']:shutil.copytree(ROOT/sub,stage/sub)
    report={'status':'PASS_AUTHOR_COMPLETE_EDITION_REPLAY','scope':s,'independent_acceptance':False}
    if args.study_root:
        from pypdf import PdfReader
        recs=read(ROOT/'scope.json')['source_editions'];checked=[]
        for rec in recs:
            binding=rec.get('primary',rec);path=binding.get('path',binding.get('pdf'));p=args.study_root/path
            need(p.is_file() and sha(p)==binding['sha256'],'exact primary '+path)
            need(len(PdfReader(p).pages)==13,'whole 13-page primary '+path);checked.append(path)
        report['exact_primary_files']=checked
    if args.programs:report['programs']=programs(out,stage)
    if args.formal:report['formal']=formal(out,stage,args.packages,args.lean)
    if args.render:report['render']=render(out,stage,args.xelatex)
    scope();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'source_rows':31}))
if __name__=='__main__':main()
