#!/usr/bin/env python3
"""Replay the additive exceptional two-orbit packet without editing its inputs."""
import argparse,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(v,m):
    if not v:raise RuntimeError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def run(cmd,cwd=None):
    r=subprocess.run(list(map(str,cmd)),cwd=cwd,capture_output=True,text=True,timeout=180)
    return r.returncode,r.stdout+r.stderr

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--study-root',type=Path,default=ROOT.parent);p.add_argument('--render',action='store_true')
    p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args()
    need(not a.out.exists(),'Fresh output directory required');a.out.mkdir(parents=True);a.out=a.out.resolve()
    scope=json.loads((ROOT/'scope.json').read_text())
    for x in scope['local_bindings']:need(sha(ROOT/x['path'])==x['sha256'],'Changed local file '+x['path'])
    for x in scope['external_bindings']:need(sha(a.study_root/x['path'])==x['sha256'],'Changed external file '+x['path'])
    main_manifest=a.study_root/'topic_Mix_F005_recovery/manifest.json'
    for x in json.loads(main_manifest.read_text())['exports']:
        need(sha(main_manifest.parent/x['path'])==x['sha256'],'Changed main frozen export '+x['path'])
    for x in scope['proof_contexts']:
        raw=(ROOT/x['path']).read_text()[x['start']:x['end']]
        need(hashlib.sha256(raw.encode()).hexdigest()==x['sha256'],'Changed proof passage '+x['id'])
    if (ROOT/'manifest.json').exists():
        for x in json.loads((ROOT/'manifest.json').read_text())['exports']:
            need(sha(ROOT/x['path'])==x['sha256'],'Changed frozen export '+x['path'])
    rc,txt=run([sys.executable,'-B','-O',ROOT/'check_exceptional.py','--out',a.out/'model.json'])
    (a.out/'model.log').write_text(txt);need(rc==0,'Model validation failed')
    m=json.loads((a.out/'model.json').read_text())
    need(m['status']=='PASS' and m['input_path_intersections']==36864 and m['mix_path_intersections']==663552,
         'Incomplete actual flag intersection validation')
    controls=[];raw=(ROOT/'check_exceptional.py').read_text()
    for name,old,new in [
      ('lose_genuine_two_orbits','ap=compose(compose(d,a),d);bp=', 'ap=a;bp='),
      ('wrong_pair_of_roots','pairs=[(0,1)];qi=', 'pairs=[(0,0)];qi='),
      ('collapse_affine_center','b=((0,1),(1,-2))','b=((0,0),(1,-2))'),
      ('identify_vertex_fibers','BF1={((c,u),','BF1={((u,c),'),
      ('identify_two_intersections','A0&B0==C0 and','A0&B0==C1 and'),
      ('wrong_word_witness','for i in [1,2,1,2]:q=Q[q][i]','for i in [1,2,1]:q=Q[q][i]')]:
        need(raw.count(old)==1,'Control anchor '+name)
        f=a.out/(name+'.py');f.write_text(raw.replace(old,new))
        rc,txt=run([sys.executable,'-B','-O',f,'--out',a.out/(name+'.json')]);(a.out/(name+'.log')).write_text(txt)
        need(rc!=0 and 'RuntimeError:' in txt,'Semantic corruption accepted '+name);controls.append(name)
    rendered=[];inclusion=False
    if a.render:
        from pypdf import PdfReader
        rd=a.out/'render';rd.mkdir();shutil.copy2(ROOT/'check_exceptional.py',rd/'check_exceptional.py')
        for name,pages in scope['pdf_pages'].items():
            shutil.copy2(ROOT/(name+'.tex'),rd/(name+'.tex'))
            for k in range(2):
                rc,txt=run([a.xelatex,'-halt-on-error','-interaction=nonstopmode',name+'.tex'],rd)
                (a.out/(name+f'_render{k}.log')).write_text(txt);need(rc==0,'Render failed '+name)
            need(not re.search('Overfull|Missing character|LaTeX Warning|Font Warning',txt),'Render diagnostic '+name)
            old=[p.extract_text() for p in PdfReader(ROOT/(name+'.pdf')).pages]
            new=[p.extract_text() for p in PdfReader(rd/(name+'.pdf')).pages]
            need(len(old)==pages and old==new,'Per-page text changed '+name)
            rendered.append({'document':name,'pages':pages,'per_page_text_equal':True})
        code=''.join(re.sub(r'\n\d+\s*$','',p.extract_text()) for p in PdfReader(rd/'programs.pdf').pages)
        norm=lambda s:''.join(s.split())
        need(norm(raw) in norm(code),'Incomplete program appendix');inclusion=True
    report={'status':'PASS','main_packet_immutable':True,'source_rows_updated':['R23','R29'],
            'actual_class':[1,2],'genuine_flag_orbits':2,'genuine_medial_orbits':2,
            'input_flags':144,'regular_core_flags':2592,'path_intersections':36864+663552,
            'printed_conditions':{'Cor6.10':False,'Cor6.15(2)':False},
            'root0_intersection_order':3,'root1_intersection_order':2,'common_medial_intersection_order':1,
            'rejected_controls':controls,'renders':rendered,'complete_program_inclusion':inclusion,
            'new_Lean_declarations':0,'new_required_computational_premises':0,'bounded_validation_programs':1,
            'full_geometric_Lean_claim':False,'source_credit':0,'question_credit':0,'ratio':None,
            'status_of_math':'author complete; distinct review pending'}
    dump(a.out/'report.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
