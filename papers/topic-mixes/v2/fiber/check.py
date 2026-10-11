#!/usr/bin/env python3
"""Bound replay of the corrected mix criteria: literal programs, scoped algebra and complete TeX."""
import argparse,hashlib,json,os,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(v,m):
    if not v:raise RuntimeError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def run(cmd,cwd=None,env=None):
    r=subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,capture_output=True,text=True,timeout=180)
    return r.returncode,r.stdout+r.stderr

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--study-root',type=Path,default=ROOT.parent);p.add_argument('--render',action='store_true')
    p.add_argument('--gap',default='/opt/homebrew/bin/gap');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex')
    p.add_argument('--lean',type=Path,default=Path('/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'))
    p.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'));a=p.parse_args()
    need(not a.out.exists(),'Fresh output directory required');a.out.mkdir(parents=True);a.out=a.out.resolve()
    scope=json.loads((ROOT/'scope.json').read_text())
    for x in scope['local_bindings']:need(sha(ROOT/x['path'])==x['sha256'],'Changed local input '+x['path'])
    for x in scope['external_bindings']:need(sha(a.study_root/x['path'])==x['sha256'],'Changed external input '+x['path'])
    for x in scope['proof_contexts']:
        s=(ROOT/x['path']).read_text()[x['start']:x['end']]
        need(hashlib.sha256(s.encode()).hexdigest()==x['sha256'],'Changed proof context '+x['id'])
    if (ROOT/'manifest.json').exists():
        for x in json.loads((ROOT/'manifest.json').read_text())['exports']:
            need(sha(ROOT/x['path'])==x['sha256'],'Changed frozen export '+x['path'])
    programs=[];controls=[]
    marker='COPRIME_CERTIFICATE_PASS'
    rc,txt=run([a.gap,'-q','-b','-x','240',ROOT/'check_coprime.g']);(a.out/'coprime.log').write_text(txt)
    need(rc==0 and 'Error,' not in txt and 'Syntax warning' not in txt and marker in txt,'Required GAP certificate failed')
    programs.append('check_coprime.g')
    rc,txt=run([sys.executable,'-B','-O',ROOT/'check_single_base.py','--out',a.out/'single_base.json'])
    (a.out/'single_base.log').write_text(txt);need(rc==0,'Six-coordinate validation failed')
    model=json.loads((a.out/'single_base.json').read_text());need(model['status']=='PASS','Missing model result')
    need(sum(x['all_subset_ip_checks'] for x in model['factor_reports'])==184320,'Incomplete input intersections')
    programs.append('check_single_base.py')
    for name,n,old,new in [
      ('wrong_middle_order','check_coprime.g','[79200,1440,1440,30,60]','[79200,1440,1440,60,60]'),
      ('wrong_witness','check_coprime.g','not(a[2] in C)','a[2] in C'),
      ('wrong_middle_vector','check_single_base.py','v=(1,1,2,2,1,2)','v=(1,1,2,2,2,1)'),
      ('wrong_end_space','check_single_base.py','(1,0,0,0,0,2)','(1,0,0,0,2,0)'),
      ('wrong_root','check_single_base.py','good==81','good==80'),
      ('wrong_path_witness','check_single_base.py','walk(0,wb)==1','walk(0,wb)==2')]:
        raw=(ROOT/n).read_text();need(raw.count(old)==1,'Control anchor '+name)
        f=a.out/(name+Path(n).suffix);f.write_text(raw.replace(old,new))
        cmd=[a.gap,'-q','-b','-x','240',f] if n.endswith('.g') else [sys.executable,'-B','-O',f,'--out',a.out/(name+'.json')]
        rc,txt=run(cmd);(a.out/(name+'.log')).write_text(txt)
        need((rc!=0 or 'Error,' in txt) and marker not in txt,'Mathematical corruption accepted '+name);controls.append(name)
    pins=json.loads((ROOT/'dependency_manifest.json').read_text());libs=[]
    for x in pins['packages']:
        d=a.packages/x['name'];rc,txt=run(['git','-C',d,'rev-parse','HEAD']);need(rc==0 and txt.strip()==x['rev'],'Package pin '+x['name'])
        rc,txt=run(['git','-C',d,'diff','--quiet','HEAD','--']);need(rc==0,'Modified package '+x['name'])
        if (d/'.lake/build/lib/lean').is_dir():libs.append(str(d/'.lake/build/lib/lean'))
    rc,txt=run([a.lean,'--version']);need(rc==0 and 'version 4.32.2,' in txt,'Lean version')
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(libs);env.pop('LEAN_SRC_PATH',None)
    src=ROOT/'FiberIntersections.lean';raw=src.read_text()
    proof_text=re.sub(r'/\-.*?\-/|--[^\n]*','',raw,flags=re.S)
    need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b',proof_text),'Unpermitted proof placeholder/evaluator')
    rc,txt=run([a.lean,'--root='+str(ROOT),'-o',a.out/'FiberIntersections.olean',src],env=env);(a.out/'lean.log').write_text(txt)
    need(rc==0 and 'warning:' not in txt,'Lean failed or warned')
    reports=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",txt,re.S)
    need([x[0] for x in reports]==scope['declarations'],'Wrong declaration inventory')
    for name,axs in reports:need(set(re.findall(r'[A-Za-z][\w.]*',axs))<={'propext','Classical.choice','Quot.sound'},'Nonstandard axiom')
    formal_controls=[]
    for name,old,new in [
      ('no_base_intersection',"(hbase : ∀ x', inOrbit A x x' → inOrbit B x x' → inOrbit C x x')","(hbase : True)"),
      ('no_fiber_intersection',"inDiagonal C x y x y') :",'True) :'),
      ('no_C_in_B','(hCB : C ≤ B)','(hCB : C ≤ C)')]:
        need(old in raw,'Formal control anchor '+name);f=a.out/(name+'.lean');f.write_text(raw.replace(old,new))
        rc,txt=run([a.lean,'--root='+str(a.out),f],env=env);(a.out/(name+'.log')).write_text(txt)
        need(rc!=0 and 'error' in txt and 'outside of the root' not in txt,'Formal weakening accepted/not typechecked '+name);formal_controls.append(name)
    renders=[];code_inclusion=False
    if a.render:
        from pypdf import PdfReader
        rd=a.out/'render';rd.mkdir()
        for n in programs:shutil.copy2(ROOT/n,rd/n)
        for n in ["single_base_obstruction.tex","rooted_two_orbit_tests.tex"]:shutil.copy2(ROOT/n,rd/n)
        for name,pages in scope['pdf_pages'].items():
            shutil.copy2(ROOT/(name+'.tex'),rd/(name+'.tex'))
            for k in range(2):
                rc,txt=run([a.xelatex,'-halt-on-error','-interaction=nonstopmode',name+'.tex'],rd)
                (a.out/(name+f'_render{k}.log')).write_text(txt);need(rc==0,'Render failed '+name)
            need(not re.search('Overfull|Missing character|LaTeX Warning|Font Warning',txt),'Render diagnostic '+name)
            old=[p.extract_text() for p in PdfReader(ROOT/(name+'.pdf')).pages]
            new=[p.extract_text() for p in PdfReader(rd/(name+'.pdf')).pages]
            need(len(old)==pages and old==new,'Per-page text differs '+name);renders.append({'document':name,'pages':pages,'per_page_text_equal':True})
        code=''.join(re.sub(r'\n\d+\s*$','',p.extract_text()) for p in PdfReader(rd/'programs.pdf').pages)
        norm=lambda s:''.join(s.split())
        for n in programs:need(norm((ROOT/n).read_text()) in norm(code),'Whole program missing from appendix '+n)
        code_inclusion=True
    report={'status':'PASS','source_rows':len(scope['source_rows']),'proof_contexts':len(scope['proof_contexts']),
      'programs':programs,'required_finite_programs':1,'bounded_validation_programs':1,'regular_input_IP_pairs':512,
      'single_base_input_IP_pairs':184320,'two_mixed_roots':[model['good_base'],model['bad_base']],
      'rejected_program_controls':controls,'Lean_declarations':len(reports),'axioms':'standard only',
      'rejected_Lean_proof_weakenings':formal_controls,'renders':renders,'whole_program_inclusion':code_inclusion,
      'complete_source_questions_solved':False,'full_source_credit':0,'question_credit':0,
      'end_to_end_Lean':False,'principal_recovery':'AUTHOR_COMPLETE_PENDING_DISTINCT_REVIEW',
      'cor610':'criterion with specified roots; no literal equality or counterexample claim',
      'medial_convention':'middle-color components; conflicting printed chain type explicitly qualified',
      'compression_factor':None}
    dump(a.out/'report.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
