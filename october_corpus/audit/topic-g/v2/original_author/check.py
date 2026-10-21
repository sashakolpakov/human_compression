#!/usr/bin/env python3
"""Fresh whole-program and scoped Lean replay for the Topic G edition.

No source PDF is downloaded. No external classification or all-parameter
geometric proof is asserted to follow from this finite replay.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
REV='905b95818eb32af7874a58b427f50c1711a5e96c'
PACKAGES=['mathlib','plausible','proofwidgets','batteries','aesop','importGraph','LeanSearchClient','Qq']

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def need(p,s):
    if not p: raise RuntimeError(s)
def write(p,j): p.write_text(json.dumps(j,indent=2)+'\n')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--gap',default='/opt/homebrew/bin/gap')
    ap.add_argument('--lean',default='/Users/sasha/.elan/bin/lean')
    ap.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    ap.add_argument('--skip-formal',action='store_true')
    ap.add_argument('--render',action='store_true')
    ap.add_argument('--bindings-only',action='store_true')
    ap.add_argument('--study-root',type=Path)
    ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex')
    a=ap.parse_args();out=a.out.resolve();need(not out.exists(),'fresh output directory required');out.mkdir(parents=True)
    (out/'research/leemans').mkdir(parents=True)  # Original unital program's literal log path.
    run_started=time.monotonic(); inventory=json.loads((ROOT/'program_inventory.json').read_text());formal=json.loads((ROOT/'formal/scope.json').read_text())
    inputs={}
    for row in inventory['programs']+formal['modules']:
        p=ROOT/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'bound file changed: '+row['path'])
        inputs[row['path']]=sha(p);dst=out/p.name;shutil.copyfile(p,dst)
    scope=json.loads((ROOT/'scope.json').read_text())
    need(scope['counts']==dict(L009=44,L092=35,proof_spans=34),'scope size')
    for id,row in scope['proof_spans'].items():
        text=(ROOT/row['path']).read_text();start=text.index(row['start_anchor']) if row['start_anchor'] else 0
        end=text.index(row['end_anchor'],start+len(row['start_anchor'] or '')) if row['end_anchor'] else len(text)
        data=text[start:end].encode()
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'proof span changed: '+id)
    for row in scope['rows']:
        need(all(i in scope['proof_spans'] for i in row['new_proof_spans']),'unresolved proof locator')
    sources_checked=[]
    if a.study_root:
        for row in scope['source_bindings']:
            p=a.study_root/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'source changed '+row['id']);sources_checked.append(row['id'])
    if (ROOT/'manifest.json').exists():
        for row in json.loads((ROOT/'manifest.json').read_text())['exports']:
            p=ROOT/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'frozen export changed '+row['path'])
    binding_report=dict(status='PASS',source_rows=79,proof_spans=34,complete_programs=13,formal_modules=6,external_sources_checked=sources_checked)
    write(out/'bindings.json',binding_report)
    if a.bindings_only:
        print(json.dumps(binding_report));return
    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    def run(label,argv,marker=None,timeout=300,negative=False):
        r=subprocess.run(argv,cwd=out,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
        log=out/(label+'.log');log.write_text(r.stdout)
        if negative:
            need(r.returncode!=0 or 'Error,' in r.stdout or 'error:' in r.stdout,'negative control accepted: '+label)
        else:
            need(r.returncode==0 and 'Error,' not in r.stdout and 'Error, ' not in r.stdout,'command failed: '+label)
            if marker: need(marker in r.stdout,'missing success marker: '+label)
        return dict(label=label,returncode=r.returncode,log_sha256=sha(log),status='REJECTED' if negative else 'PASS')
    witness=out/'phase186_witt_witness.json'
    (out/'witt_driver.g').write_text('P186_OUTPUT:='+json.dumps(str(witness))+';;\nRead("phase186_witt_derived_check.g");\n')
    gap_jobs=[('witt','witt_driver.g','P186_WITT_DERIVED_AND_FULL_AUT_PASS'),
      ('exceptional','phase265_exceptional.g','PHASE265_CONTROLS_PASS'),
      ('deleted_pencil','phase265_residues.g','PHASE265_UH4_PASS'),
      ('mathieu_fibers','phase182_mathieu_fibers.g','P182_MATHIEU_EXTENSION_FIBERS_PASS'),
      ('frame_control','phase265_frame_control.g','PHASE265_FRAME_CONTROL_PASS'),
      ('plane_models','phase265_plane_models.g','PHASE265_ALL_NINE_MODELS_PASS'),
      ('hermitian_labels','phase186_hermitian_labels.g','P186_HERMITIAN_LABELS_PASS'),
      ('literal_unitals','hermitian_unital_check.g','PASS')]
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        fs=[pool.submit(run,label,[a.gap,'-q','-b',file],marker) for label,file,marker in gap_jobs]
        for f in fs: results.append(f.result())
    # These are separate literal incidence implementations, not quotient orbit heuristics.
    for label,file,extra in [('deleted_line','phase182_deleted_line_check.py',['--output',str(out/'deleted_line.json')]),
                            ('inversive','phase182_inversive_geometry_check.py',['--output',str(out/'inversive.json')]),
                            ('path_length','phase199_path_length.py',[])]:
        results.append(run(label,[sys.executable,'-B',file]+extra))
    results.append(run('witt_validation',[sys.executable,'-B','phase186_witt_validate.py',str(witness),'--output',str(out/'witt_validation.json')]))
    results.append(run('witt_formal_generation',[sys.executable,'-B','phase186_witt_lean_generate.py',str(witness),str(out/'Generated.lean')]))
    need((out/'Generated.lean').read_bytes()==(ROOT/'formal/WittDerivedPlanes.lean').read_bytes(),'generated certificate differs from bound source')
    # Fixed cases and control status checked independently of their printed PASS lines.
    j=json.loads((out/'deleted_line.json').read_text());need([x['q'] for x in j['cases']]==[4,8] and [x['residually_connected'] for x in j['cases']]==[False,True],'deleted-line outcome')
    j=json.loads((out/'inversive.json').read_text());need(j['object_counts']==[10,180,30,10] and j['literal_Lemma_5_residual_connectedness_counterexample'],'inversive outcome')
    v=json.loads((out/'witt_validation.json').read_text());need([x['v'] for x in v['cases']]==[11,12,22,23,24],'five Witt models');need(len(v['negative_controls'])==2 and all(x['status']=='REJECTED' for x in v['negative_controls']),'Witt controls')
    controls=list(v['negative_controls'])
    for name,file,old,new in [('wrong_exceptional_orbit','phase265_exceptional.g','Length(T)=2520','Length(T)=2521'),('wrong_deleted_pencil_diameter','phase265_residues.g','Length(P)=7','Length(P)=6')]:
        t=(out/file).read_text();need(t.count(old)==1,'mutation anchor');m=out/(name+'.g');m.write_text(t.replace(old,new,1));controls.append(run(name,[a.gap,'-q','-b',m.name],negative=True))
    lean_reports=[]
    if not a.skip_formal:
        env['ELAN_TOOLCHAIN']='leanprover/lean4:v4.32.2'
        env['LEAN_PATH']=':'.join([str(out)]+[str(a.packages/p/'.lake/build/lib/lean') for p in PACKAGES])
        revision=subprocess.run(['git','-C',str(a.packages/'mathlib'),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
        need(revision==REV,'unexpected mathlib revision')
        pins=json.loads((ROOT/'formal/dependency_manifest.json').read_text())
        version=subprocess.run([a.lean,'--version'],env=env,capture_output=True,text=True,check=True).stdout.strip()
        need('version 4.32.2' in version,'unexpected Lean version')
        packages=[]
        for package in pins['packages']:
            actual=subprocess.run(['git','-C',str(a.packages/package['name']),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
            need(actual==package['rev'],'unexpected package revision: '+package['name'])
            packages.append(dict(name=package['name'],revision=actual))
        write(out/'formal_pins.json',dict(status='PASS',lean=version,packages=packages))
        for row in formal['modules']:
            p=out/Path(row['path']).name;t=p.read_text()
            need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',t,re.M),'forbidden proof shortcut')
            result=run(p.stem,[a.lean,'-o',str(out/(p.stem+'.olean')),str(p)],timeout=240)
            log=(out/(p.stem+'.log')).read_text();need('error:' not in log and 'sorryAx' not in log,'formal failure')
            need(log.count('depends on axioms:')==row['reports'],'axiom report count')
            ax=re.findall(r'depends on axioms:\s*\[([^]]*)\]',log)
            need(all(set(x.strip() for x in s.split(',') if x.strip()) <= {'propext','Classical.choice','Quot.sound'} for s in ax),'unexpected axioms')
            lean_reports.append(dict(module=p.name,reports=row['reports'],**result))
        mutations=[('wrong_coordinate_incidence','WittDerivedPlanes.lean','(coordinate l 2) = 0','(coordinate l 2) = one4'),
         ('swapped_point_images','WittDerivedPlanes.lean','def pointMap22 : Fin 21 → Fin 21 :=\n  ![0, 1,','def pointMap22 : Fin 21 → Fin 21 :=\n  ![1, 0,'),
         ('alter_biplane_difference_set','CyclicBiplaneDelta.lean','{1, 3, 4, 5, 9}','{1, 3, 4, 5, 8}'),
         ('replace_singleton_by_pair','CyclicBiplaneDelta.lean','incident x a ∧ incident x b ↔ x = p','incident x a ∧ incident x b ↔ x = p ∨ x = p + 1')]
        for name,file,old,new in mutations:
            t=(out/file).read_text();need(t.count(old)==1,'formal mutation anchor');m=out/(name+'.lean');m.write_text(t.replace(old,new,1));controls.append(run(name,[a.lean,str(m)],negative=True,timeout=240))
    render=[]
    if a.render:
        from pypdf import PdfReader
        for name in ['umbrella','triangle-geometries','steiner-geometries','programs']:
            for iteration in range(2):
                r=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory',str(out),name+'.tex'],cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
                (out/(name+'.render'+str(iteration)+'.log')).write_text(r.stdout);need(r.returncode==0,'render failed: '+name)
            log=(out/(name+'.log')).read_text();need('Missing character:' not in log and 'Overfull \\hbox' not in log,'render diagnostic: '+name)
            texts=[p.extract_text() or '' for p in PdfReader(out/(name+'.pdf')).pages]
            need(not any(any(ord(c)<32 and c not in '\n\r\t' for c in t) for t in texts),'PDF control glyph')
            equal=None
            if (ROOT/(name+'.pdf')).exists():
                equal=texts==[p.extract_text() or '' for p in PdfReader(ROOT/(name+'.pdf')).pages]
                need(equal,'PDF text differs from bound edition: '+name)
            render.append(dict(document=name,pages=len(texts),same_text_as_bound=equal,pdf_sha256=sha(out/(name+'.pdf'))))
    report=dict(status='PASS',seconds=round(time.monotonic()-run_started,3),program_inputs=inputs,program_replays=results,controls=controls,formal_replays=lean_reports,distinct_formal_reports=sum(r['reports'] for r in lean_reports),renders=render,whole_program_counts=dict(mathematical=4,witness_or_certificate=2,validation=7),scope='Finite computations and explicitly scoped formal components only. The complete all-parameter proofs and retained classifications require mathematical review.')
    write(out/'report.json',report);print(json.dumps(dict(status='PASS',out=str(out),seconds=report['seconds'],formal_reports=report['distinct_formal_reports'],controls=len(controls))))
if __name__=='__main__':main()
