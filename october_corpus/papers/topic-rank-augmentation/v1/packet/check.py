#!/usr/bin/env python3
"""Complete bound replay; finite source examples, diagnostics, scoped algebra and TeX."""
import argparse,hashlib,json,os,re,shutil,subprocess
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
    markers={'check_examples.g':'PASS three source examples; old_IP_pairs=192; all output defects witnessed',
             'check_models.g':'PASS bounded common-theorem diagnostics'}
    programs=[]
    for n,m in markers.items():
        rc,txt=run([a.gap,'-q','-b','-x','240',ROOT/n]);(a.out/(n+'.log')).write_text(txt)
        need(rc==0 and 'Error,' not in txt and 'Syntax warning' not in txt and m in txt,'GAP program failed '+n)
        programs.append(n)
        if n=='check_models.g':need('[[280,17,16,17],[51,9,4,7],[28,11,8,8]]' in ''.join(txt.split()),'Incomplete bounded diagnostic domain')
    controls=[]
    for name,n,old,new in [
      ('wrong_example_witness','check_examples.g','(2,3,4) in Intersection(H,K)','(1,2,3) in Intersection(H,K)'),
      ('incomplete_example_table','check_examples.g','[9,12,288,40320,72,[-1,1,-1],64]','[9,12,288,40320,36,[-1,1,-1],64]'),
      ('false_positive_conclusion','check_models.g','Need(full,"four/five point positive theorem")','Need(not full,"four/five point positive theorem")'),
      ('damaged_matching_group','check_models.g','N:=Group([(3,4),(2,5),(1,6)])','N:=Group([(3,4),(2,5),(1,5)])')]:
        raw=(ROOT/n).read_text();need(raw.count(old)==1,'Control anchor '+name)
        f=a.out/(name+'.g');f.write_text(raw.replace(old,new));rc,txt=run([a.gap,'-q','-b','-x','240',f]);(a.out/(name+'.log')).write_text(txt)
        need((rc!=0 or 'Error,' in txt) and markers[n] not in txt,'Control accepted '+name);controls.append(name)
    pins=json.loads((ROOT/'dependency_manifest.json').read_text());libs=[]
    for x in pins['packages']:
        d=a.packages/x['name'];rc,txt=run(['git','-C',d,'rev-parse','HEAD']);need(rc==0 and txt.strip()==x['rev'],'Package pin '+x['name'])
        rc,txt=run(['git','-C',d,'diff','--quiet','HEAD','--']);need(rc==0,'Modified package '+x['name'])
        if (d/'.lake/build/lib/lean').is_dir():libs.append(str(d/'.lake/build/lib/lean'))
    rc,txt=run([a.lean,'--version']);need(rc==0 and 'version 4.32.2,' in txt,'Lean version')
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(libs);env.pop('LEAN_SRC_PATH',None)
    src=ROOT/'SupportedIntersections.lean';raw=src.read_text()
    need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b',raw),'Unpermitted proof placeholder/evaluator')
    rc,txt=run([a.lean,'--root='+str(ROOT),'-o',a.out/'SupportedIntersections.olean',src],env=env);(a.out/'lean.log').write_text(txt)
    need(rc==0 and 'warning:' not in txt,'Lean failed or warned')
    reports=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",txt,re.S)
    need([x[0] for x in reports]==scope['declarations'],'Wrong declaration inventory')
    for name,axs in reports:need(set(re.findall(r'[A-Za-z][\w.]*',axs))<={'propext','Classical.choice','Quot.sound'},'Nonstandard axiom')
    formal_controls=[]
    for name,old,new in [
      ('no_base_inclusion','(hBK : B ≤ K)','(hBK : B ≤ B)'),
      ('no_factorization','h = n * b','n * b = n * b'),
      ('no_complementarity','(hNB : N ⊓ B = ⊥)','(hNB : N ⊓ B = N ⊓ B)')]:
        need(old in raw,'Formal control anchor '+name);f=a.out/(name+'.lean');f.write_text(raw.replace(old,new))
        rc,txt=run([a.lean,'--root='+str(a.out),f],env=env);(a.out/(name+'.log')).write_text(txt)
        need(rc!=0 and 'error' in txt and 'outside of the root' not in txt,'Formal weakening accepted/not typechecked '+name);formal_controls.append(name)
    renders=[];code_inclusion=False
    if a.render:
        from pypdf import PdfReader
        rd=a.out/'render';rd.mkdir()
        for n in markers:shutil.copy2(ROOT/n,rd/n)
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
        for n in markers:need(norm((ROOT/n).read_text()) in norm(code),'Whole program missing from appendix '+n)
        code_inclusion=True
    report={'status':'PASS','source_rows':len(scope['source_rows']),'proof_contexts':len(scope['proof_contexts']),
      'programs':programs,'required_finite_programs':1,'generic_diagnostic_programs':1,'source_old_IP_pairs':192,
      'bounded_models':{'scanned':359,'transitive':37,'sufficient':28,'C':32},'rejected_GAP_controls':controls,
      'new_Lean_declarations':len(reports),'inherited_obstruction_declarations_not_recompiled_here':13,
      'axioms':'standard only','rejected_Lean_weakenings':formal_controls,'renders':renders,'whole_program_inclusion':code_inclusion,
      'complete_19page_original_census_recomputed':False,'full_source_credit':0,'question_credit':0,
      'end_to_end_Lean':False,'status_of_principal_recovery':'AUTHOR_COMPLETE_PENDING_DISTINCT_REVIEW',
      'correction_and_formal_parent_manifests_preserved':True,'compression_factor':None}
    dump(a.out/'report.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
