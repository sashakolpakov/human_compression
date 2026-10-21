#!/usr/bin/env python3
"""Replay complete L016 packet, without treating diagnostics as uniform proofs."""
import argparse,hashlib,json,os,re,shutil,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent

def need(x,msg):
    if not x:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def run(cmd,cwd=None,env=None):
    r=subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,capture_output=True,text=True,timeout=180)
    return r.returncode,r.stdout+r.stderr

def bindings(study):
    s=json.loads((P/'scope.json').read_text())
    for x in s['local_bindings']:need(sha(P/x['path'])==x['sha256'],'Changed local '+x['path'])
    for x in s['external_bindings']:need(sha(study/x['path'])==x['sha256'],'Changed external '+x['path'])
    for x in s['proof_contexts']:
        text=(P/x['path']).read_text()[x['start']:x['end']]
        need(hashlib.sha256(text.encode()).hexdigest()==x['sha256'],'Changed context '+x['id'])
    if(P/'manifest.json').exists():
        for x in json.loads((P/'manifest.json').read_text())['exports']:
            need(sha(P/x['path'])==x['sha256'],'Changed frozen '+x['path'])
    return s

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--study-root',type=Path,default=P.parent);ap.add_argument('--render',action='store_true')
    ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex')
    ap.add_argument('--lean',type=Path,default=Path('/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'))
    ap.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'));a=ap.parse_args()
    need(not a.out.exists(),'Fresh output directory required');a.out.mkdir(parents=True);a.out=a.out.resolve()
    scope=bindings(a.study_root)
    for name,marker in [('base_certificate.g','SOURCE_BASE96_MARKED_IDENTIFICATION_PASS'),('validate_base.g','BASE_DIAGNOSTICS_ALL256_IP_INTEGER_VOLTAGES_PASS')]:
        rc,txt=run([a.gap,'-q','-T',P/name],P);(a.out/(name+'.log')).write_text(txt)
        need(rc==0 and marker in txt and 'Error,'not in txt and 'Syntax warning'not in txt,'GAP failure '+name)
    rc,txt=run([sys.executable,'-B','-O',P/'validate_covers.py','--out',a.out/'models.json']);(a.out/'models.log').write_text(txt)
    need(rc==0 and 'COVER_DIAGNOSTICS_PASS'in txt,'Cover diagnostic failure')
    models=json.loads((a.out/'models.json').read_text())
    need(models['L3.5']['cover']['diamonds']=={'2':8,'4':16},'Missing actual defect')
    controls=[]
    mutations=[('universal_order','base_certificate.g','Size(U)=96','Size(U)=192'),
      ('wrong_integer_sign','validate_base.g','return -1','return 1'),
      ('thin_false_conclusion','validate_covers.py',"qm['diamonds']=={2:8,4:16}","qm['diamonds']=={2:24}"),
      ('deleted_voltage','validate_covers.py','if i==1:y[5]^=x[2]','if i==1:y[5]^=0'),
      ('wrong_potential','validate_covers.py','return x[5]^x[4]^(x[0]&x[1])','return x[5]^x[4]'),
      ('wrong_sample_face_formula','validate_covers.py','[4,12*m,12*m,4]','[4,6*m,6*m,4]')]
    for label,n,old,new in mutations:
        raw=(P/n).read_text();need(raw.count(old)==1,'Mutation anchor '+label)
        f=a.out/(label+Path(n).suffix);f.write_text(raw.replace(old,new))
        cmd=[a.gap,'-q','-T',f]if n.endswith('.g')else[sys.executable,'-B','-O',f,'--out',a.out/(label+'.json')]
        rc,txt=run(cmd,P);(a.out/(label+'.log')).write_text(txt)
        need(rc!=0 or 'Error,'in txt,'Accepted mathematical mutation '+label);controls.append(label)
    pins=json.loads((P/'dependency_manifest.json').read_text());libs=[]
    for x in pins['packages']:
        d=a.packages/x['name'];rc,txt=run(['git','-C',d,'rev-parse','HEAD'])
        need(rc==0 and txt.strip()==x['rev'],'Package pin '+x['name'])
        rc,txt=run(['git','-C',d,'diff','--quiet','HEAD','--']);need(rc==0,'Changed package '+x['name'])
        if(d/'.lake/build/lib/lean').is_dir():libs.append(str(d/'.lake/build/lib/lean'))
    rc,txt=run([a.lean,'--version']);need(rc==0 and 'version 4.32.2,'in txt,'Lean version')
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(libs);env.pop('LEAN_SRC_PATH',None)
    reports=[]
    for spec in scope['formal']:
        src=(a.study_root if spec.get('external')else P)/spec['path'];raw=src.read_text()
        clean=re.sub(r'/\-.*?\-/|--[^\n]*','',raw,flags=re.S)
        need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b',clean),'Formal placeholder')
        rc,txt=run([a.lean,'--root='+str(src.parent),'-o',a.out/(src.stem+'.olean'),src],env=env)
        (a.out/(src.stem+'.log')).write_text(txt);need(rc==0 and 'warning:'not in txt,'Formal failure '+src.name)
        decls=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",txt,re.S)
        need([x[0]for x in decls]==spec['declarations'],'Declaration inventory')
        for name,axs in decls:
            need(set(re.findall(r'[A-Za-z][\w.]*',axs))<={'propext','Classical.choice','Quot.sound'},'Extra axiom')
        reports+=decls
    raw=(P/'CoverFibers.lean').read_text();formal_controls=[]
    for label,old,new in [
      ('no_base_condition','(hbase : ∀ x, orbit A (π q) x → orbit B (π q) x → orbit C (π q) x)','(hbase : True)'),
      ('no_C_in_B','(hCB : C ≤ B)','(hCB : C ≤ C)'),
      ('omit_voltage_equation','simp only [lift, map_add, hz]','simp only [lift, map_add]')]:
        need(old in raw,'Formal mutation anchor');f=a.out/(label+'.lean');f.write_text(raw.replace(old,new))
        rc,txt=run([a.lean,'--root='+str(a.out),f],env=env);(a.out/(label+'.log')).write_text(txt)
        need(rc!=0 and 'error'in txt and 'outside of the root'not in txt,'Unrejected proof weakening '+label);formal_controls.append(label)
    renders=[];code_inclusion=False
    if a.render:
        from pypdf import PdfReader
        rd=a.out/'render';rd.mkdir()
        for x in scope['programs']:shutil.copy2(P/x['path'],rd/x['path'])
        for name,pages in scope['pdf_pages'].items():
            shutil.copy2(P/(name+'.tex'),rd/(name+'.tex'))
            for k in range(2):
                rc,txt=run([a.xelatex,'-halt-on-error','-interaction=nonstopmode',name+'.tex'],rd)
                (a.out/(name+f'_render{k}.log')).write_text(txt);need(rc==0,'Render failure '+name)
            need(not re.search('Overfull|Missing character|LaTeX Warning|Font Warning',txt),'Render diagnostic '+name)
            old=[p.extract_text()for p in PdfReader(P/(name+'.pdf')).pages]
            new=[p.extract_text()for p in PdfReader(rd/(name+'.pdf')).pages]
            need(len(old)==pages and old==new,'Per-page render text '+name)
            renders.append({'name':name,'pages':pages,'per_page_text_equal':True})
        text=''.join(re.sub(r'\n\d+\s*$','',p.extract_text())for p in PdfReader(rd/'programs.pdf').pages)
        norm=lambda t:''.join(t.split())
        for x in scope['programs']:need(norm((P/x['path']).read_text())in norm(text),'Incomplete printed program '+x['path'])
        code_inclusion=True
    result={'status':'PASS','source_rows':len(scope['source_rows']),'proof_contexts':len(scope['proof_contexts']),
      'required_programs':1,'optional_validation_programs':2,'diagnostic_samples':[1,2,3,5],
      'literal_thin_counterexample':models['L3.5'],'program_mutations_rejected':controls,
      'formal_declarations':len(reports),'new_formal_declarations':4,'reused_formal_declarations':2,
      'formal_mutations_rejected':formal_controls,'axioms':'standard only','renders':renders,
      'whole_program_inclusion':code_inclusion,'uniform_proof':'written, not inferred from diagnostic samples',
      'full_Lean':False,'source_credit':0,'question_credit':0,'compression_factor':None,
      'optional_validation_policy':'symmetric inclusion or symmetric exclusion; no ours-only code compression factor'}
    dump(a.out/'report.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
