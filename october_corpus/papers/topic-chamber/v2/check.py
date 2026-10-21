#!/usr/bin/env python3
"""Fresh replay of the chamber/cover edition. No primary source is downloaded."""
import argparse,hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PACKAGES=['mathlib','plausible','proofwidgets','batteries','aesop','importGraph','LeanSearchClient','Qq']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(p,s):
    if not p:raise RuntimeError(s)
def write(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--study-root',type=Path)
    ap.add_argument('--public-root',type=Path)
    ap.add_argument('--gap',default='/opt/homebrew/bin/gap')
    ap.add_argument('--lean',default='/Users/sasha/.elan/bin/lean')
    ap.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex')
    ap.add_argument('--bindings-only',action='store_true')
    ap.add_argument('--skip-formal',action='store_true')
    ap.add_argument('--render',action='store_true')
    a=ap.parse_args();out=a.out.resolve();need(not out.exists(),'fresh output required');out.mkdir(parents=True);start=time.monotonic()
    scope=json.loads((ROOT/'scope.json').read_text());inventory=json.loads((ROOT/'program_inventory.json').read_text());formal=json.loads((ROOT/'formal/scope.json').read_text())
    def bound(root,row):
        p=root/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'changed bound file '+row['path']);return p
    inputs={}
    for row in inventory['programs']+formal['modules']:
        p=bound(ROOT,row);inputs[row['path']]=sha(p)
    need(scope['counts']=={'L008':9,'N016':18,'proof_spans':22},'scope counts')
    need(len(scope['rows'])==27 and len({r['id'] for r in scope['rows']})==27,'scope rows')
    for key,row in scope['proof_spans'].items():
        t=(ROOT/row['path']).read_text();start_at=t.index(row['start_anchor']);end=t.index(row['end_anchor'],start_at+len(row['start_anchor'])) if row['end_anchor'] else len(t);data=t[start_at:end].encode()
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'changed proof span '+key)
    for row in scope['rows']:need(all(k in scope['proof_spans'] for k in row['new_proof_spans']),'unbound proof locator')
    checked=[]
    if a.study_root:
        for row in scope['source_bindings']+scope['prior_bindings']:
            bound(a.study_root,row);checked.append(row['path'])
    if a.public_root:
        q=json.loads((ROOT/'question_map.json').read_text())
        for row in q['questions']:
            for k in ['accepted_record','review']:
                if row.get(k):bound(a.public_root,row[k])
        for row in q['separate_prior_baselines']:bound(a.public_root,row)
    if (ROOT/'manifest.json').exists():
        for row in json.loads((ROOT/'manifest.json').read_text())['exports']:bound(ROOT,row)
    binding=dict(status='PASS',source_rows=27,principal_contracts=2,proof_spans=22,program_files=len(inventory['programs']),formal_modules=3,source_and_prior_files_checked=len(checked))
    write(out/'bindings.json',binding)
    if a.bindings_only:print(json.dumps(binding));return
    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    def run(label,argv,negative=False,timeout=600):
        r=subprocess.run(argv,cwd=out,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
        log=out/(label+'.log');log.write_text(r.stdout)
        failed=r.returncode!=0 or any(x in r.stdout for x in ['Error,','Syntax error','error:','FAIL '])
        need(failed if negative else not failed,('negative control accepted: ' if negative else 'command failed: ')+label)
        return dict(label=label,status='REJECTED' if negative else 'PASS',returncode=r.returncode,log_sha256=sha(log))
    g=ROOT/'programs/chiral_cover.g'
    need(sha(g)=='59bf1cd96626df42e1e1baed82b88538416f336443c1a4076dfbb5f09bdcc69e','old required program changed')
    results=[run('finite_cover',[a.gap,'-q','-b',str(g)])]
    log=(out/'finite_cover.log').read_text()
    need(len(re.findall(r'^ROW ',log,re.M))==6,'six group rows')
    compact=re.sub(r'\s+','',log)
    expected={'P':'[324,[6,9,6],[54,54],9,false]','T':'[324,[6,9,2],[162,18],9,true]','Td':'[324,[2,9,6],[18,162],9,true]','R':'[972,[6,9,6],[162,162],27,true]','Q':'[2916,[6,9,6],[162,162],9,true]','Qd':'[2916,[6,9,6],[162,162],9,true]'}
    for k,v in expected.items():need('ROW'+k+v in compact,'finite row '+k)
    need('CHIRALITY facet=vertex=<b^3> ORDER 3' in log,'local chirality output')
    need('DISTINGUISH (b*c^-1)^2*a*c^2*a^-1 ORDERS [1,3]' in log,'word output')
    need('PASS GAP ' in log and 'six exact groups, all maps, IP, regularity, duality, witness' in log,'full GAP completion')
    results.append(run('reflection_models',[sys.executable,'-B','-O',str(ROOT/'programs/reflection_models.py')]))
    models=json.loads((out/'reflection_models.log').read_text());need(models['status']=='PASS' and len(models['models'])==4 and len(models['controls'])==3 and all(c['detected'] for c in models['controls']),'finite reflection diagnostics')
    controls=[]
    for label,old,new in [('wrong_R_order','R:=[972,','R:=[973,'),('wrong_word_order','=[1,3],"nonisomorphism witness"','= [1,1],"nonisomorphism witness"')]:
        t=g.read_text();need(t.count(old)==1,'GAP mutation anchor');p=out/(label+'.g');p.write_text(t.replace(old,new));controls.append(run(label,[a.gap,'-q','-b',str(p)],negative=True))
    lean=[]
    if not a.skip_formal:
        env['ELAN_TOOLCHAIN']='leanprover/lean4:v4.32.2';env['LEAN_PATH']=':'.join([str(out)]+[str(a.packages/p/'.lake/build/lib/lean') for p in PACKAGES])
        version=subprocess.run([a.lean,'--version'],env=env,capture_output=True,text=True,check=True).stdout.strip();need('version 4.32.2' in version,'Lean version')
        pins=json.loads((ROOT/'formal/dependency_manifest.json').read_text());actual=[]
        for package in pins['packages']:
            rev=subprocess.run(['git','-C',str(a.packages/package['name']),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip();need(rev==package['rev'],'package revision '+package['name']);actual.append(dict(name=package['name'],revision=rev))
        write(out/'formal_pins.json',dict(lean=version,packages=actual))
        for row in formal['modules']:
            source=ROOT/row['path'];p=out/source.name;shutil.copyfile(source,p);t=p.read_text();need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',t,re.M),'formal shortcut')
            result=run(p.stem,[a.lean,'-o',str(out/(p.stem+'.olean')),str(p)],timeout=240);text=(out/(p.stem+'.log')).read_text();need('warning:' not in text and 'sorryAx' not in text,'Lean warning or unproved claim')
            reports=re.findall(r'depends on axioms:\s*\[([^]]*)\]',text);need(len(reports)==row['reports'],'axiom report count')
            need(all(set(x.strip() for x in ax.split(',') if x.strip())<={'propext','Classical.choice','Quot.sound'} for ax in reports),'extra axiom');lean.append(dict(module=p.name,reports=len(reports),**result))
        source=(ROOT/'formal/TwoOrbitReflection.lean').read_text()
        for label,old,new in [('missing_inversion','(ha : θ a = a⁻¹)','(ha : True)'),('missing_swap','(θ x.1, !x.2)','(θ x.1, x.2)'),('missing_generation','(hgen : Subgroup.closure (Set.range α) = ⊤)','(hgen : True)')]:
            need(old in source,'Lean mutation anchor');p=out/(label+'.lean');p.write_text(source.replace(old,new,1));controls.append(run(label,[a.lean,str(p)],negative=True,timeout=240))
    renders=[]
    if a.render:
        from pypdf import PdfReader
        for stem in ['umbrella','testing-chirality','minimal-regular-covers','programs']:
            for i in range(2):
                r=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory',str(out),stem+'.tex'],cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
                (out/(stem+'.render'+str(i)+'.log')).write_text(r.stdout);need(r.returncode==0,'render failed '+stem)
            text=(out/(stem+'.log')).read_text();need(not any(s in text for s in ['Missing character:','Overfull \\hbox','Overfull \\vbox','LaTeX Font Warning:','undefined references']),'render diagnostic '+stem)
            pages=[p.extract_text() or '' for p in PdfReader(out/(stem+'.pdf')).pages];need(not any(ord(c)<32 and c not in '\n\t\r' for t in pages for c in t),'PDFcontrolglyph')
            equal=None
            if (ROOT/(stem+'.pdf')).exists():
                equal=pages==[p.extract_text() or '' for p in PdfReader(ROOT/(stem+'.pdf')).pages];need(equal,'bound PDF text differs '+stem)
            if stem=='programs':
                alltext='\n'.join(re.sub(r'(?m)^\s*\d+\s*$','',t) for t in pages);squeezed=re.sub(r'\s+','',alltext)
                for f in ['programs/chiral_cover.g','programs/reflection_models.py']:
                    need(re.sub(r'\s+','',(ROOT/f).read_text()) in squeezed,'printed complete program differs '+f)
            renders.append(dict(stem=stem,pages=len(pages),same_per_page_text=equal,pdf_sha256=sha(out/(stem+'.pdf'))))
    report=dict(status='PASS',seconds=round(time.monotonic()-start,3),binding=binding,inputs=inputs,programs=results,finite_assumption_controls=models['controls'],controls=controls,formal=lean,total_formal_reports=sum(r['reports'] for r in lean),renders=renders,scope='All source-specific geometry and retained classifications remain written or retained. The finite example uses trusted exact GAP; Lean is limited to the declared general interfaces.')
    write(out/'report.json',report);print(json.dumps(dict(status='PASS',out=str(out),seconds=report['seconds'],formal_reports=report['total_formal_reports'],controls=len(controls))))
if __name__=='__main__':main()
