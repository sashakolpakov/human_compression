"""Replay the bounded L046 character and subgroup-incidence component."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Optimized Python is not accepted')
from pathlib import Path
import argparse, hashlib, json, os, re, subprocess, time
def need(b,m):
    if not b:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(root,rows):
    for r in rows:
        p=root/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'Changed binding '+str(p))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args()
    B=Path(__file__).resolve().parent;S=a.study.resolve();O=a.out.resolve();need(B!=O and B not in O.parents,'External output required');O.mkdir(exist_ok=False,parents=True)
    m=json.loads((B/'manifest.json').read_text());verify(B,m['exports']);d=json.loads((B/'dependencies.json').read_text());verify(S,d['bindings'])
    for r in d['installed_software']:
        p=Path(r['path']);need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'Installed table/software changed')
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);runs={}
    for script,marker in [('character_probe.g','COMPLETE ON CHARACTER AND INVERSION PROBE'),('incidence_control.g','COMPLETE ALL SUBGROUP INCIDENCE CONTROLS')]:
        before=time.monotonic();r=subprocess.run(['/opt/homebrew/bin/gap','-q','-b',str(B/script)],capture_output=True,text=True,env=env,timeout=60)
        (O/(script+'.stdout')).write_text(r.stdout);(O/(script+'.stderr')).write_text(r.stderr)
        need(r.returncode==0 and not r.stderr and marker in r.stdout,'Exact GAP completion '+script);need(r.stdout==(B/'expected'/f'{script}.stdout').read_text(),'Changed exact mathematical output '+script)
        runs[script]={'seconds':time.monotonic()-before,'exit_code':r.returncode,'stderr_empty':True}
    text=(O/'character_probe.g.stdout').read_text();inversions={int(n):list(map(int,[c,i,o])) for n,c,i,o in re.findall(r'^INVERSION (\d+) (\d+) (\d+) (\d+)$',text,re.M)}
    need({n:inversions[n] for n in [8,16,20,31]}=={8:[2,2,0],16:[4,4,0],20:[2,0,2],31:[2,0,2]},'Exact four obstructions')
    need('TOM_ON_AVAILABLE false' in text,'Do not conceal missing ON incidence input')
    control=(O/'incidence_control.g.stdout').read_text();tests=re.findall(r'CONTROL (\d+) SUBGROUP_CLASSES (\d+) TYPES (\d+) DIRECT_PAIRS (\d+) GENERATED\s*\[([^]]*)\] PASS',control)
    need(len(tests)==5,'Five complete subgroup controls');need(sum(int(r[3])for r in tests)==5170,'Direct pair inventory')
    pages=None
    if a.render:
        from pypdf import PdfReader
        N=O/'native';N.mkdir()
        for i in [1,2]:
            p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(N),'generating_pairs.tex'],cwd=B,capture_output=True,text=True,env=env,timeout=60)
            (N/f'build{i}.stdout').write_text(p.stdout);(N/f'build{i}.stderr').write_text(p.stderr);need(p.returncode==0 and not p.stderr,'Native build')
        old=PdfReader(B/'generating_pairs.pdf');new=PdfReader(N/'generating_pairs.pdf');pages=len(new.pages);need(pages==len(old.pages)==4,'Four pages');need([p.extract_text()for p in old.pages]==[p.extract_text()for p in new.pages],'Native text unchanged')
        need('Overfull' not in(N/'generating_pairs.log').read_text(),'No overflow')
    report={'status':'PASS_BOUNDED_L046_COMMON_COUNTING_AND_INVERSION','runs':runs,'subgroup_classes_checked':sum(int(r[1])for r in tests),'literal_pairs_checked':5170,'ON_inversion_obstructions':{str(n):inversions[n]for n in [8,16,20,31]},'native_pages':pages,'ON_generating_census_completed':False,'whole_original_credit':0,'new_question_credit':0,'new_measurements':0,'new_Lean_declarations':0}
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
