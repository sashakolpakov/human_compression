import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,json,os,subprocess,time
from pathlib import Path

def need(ok,why):
    if not ok:raise ValueError(why)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(p,row):need(p.is_file() and p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],'binding '+str(p))

def run(cmd,out,cap,cwd=None,env=None):
    out.mkdir();started=time.monotonic();status='ACTIVE'
    (out/'command.json').write_text(json.dumps({'command':cmd,'cap_seconds':cap,'cwd':str(cwd) if cwd else None},indent=2)+'\n')
    try:
        with (out/'stdout').open('wb') as a,(out/'stderr').open('wb') as b:
            p=subprocess.run(cmd,cwd=cwd,env=env,stdout=a,stderr=b,timeout=cap)
        status=p.returncode
    except subprocess.TimeoutExpired:status='TIMEOUT'
    receipt={'command':cmd,'returncode':status,'seconds':time.monotonic()-started,'stdout_sha256':digest(out/'stdout'),'stderr_sha256':digest(out/'stderr')}
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    need(status==0 and not (out/'stderr').read_bytes(),'child failed '+str(out))
    return receipt

def main():
    p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args()
    packet=Path(__file__).resolve().parent;study=a.study.resolve();out=a.out.resolve()
    need(study==Path('/Users/sasha/medusa/research/leemans'),'fixed author execution namespace; public relocation needs its own adapter')
    need(not out.exists(),'output exists')
    manifest=json.loads((packet/'manifest.json').read_text());exports=manifest['exports'];deps=json.loads((packet/'dependencies.json').read_text())
    for r in exports:verify(packet/r['path'],r)
    for r in deps:
        q=Path(r['path']);verify(q if q.is_absolute() else study/q,r)
    out.mkdir(parents=True);receipts=[]
    receipts.append(run(['/opt/homebrew/bin/gap','-q','-b',str(packet/'export_input.g')],out/'input',30))
    import constructions as c
    need(c.load_input(out/'input/stdout')==c.load_input(packet/'expected_input/stdout'),'fixed input export')
    receipts.append(run([sys.executable,str(packet/'constructions.py'),'--input',str(out/'input/stdout'),'--out',str(out/'literal')],out/'literal_receipt',120))
    for name in ['model.json','model_5.1.json','model_5.2.json','choice_maps.json','truncations.json','report.json']:
        need(json.loads((out/'literal'/name).read_text())==json.loads((packet/'expected'/name).read_text()),'scientific output '+name)
    receipts.append(run([sys.executable,str(packet/'controls.py'),'--model-dir',str(out/'literal'),'--out',str(out/'controls')],out/'controls_receipt',30))
    controls=json.loads((out/'controls/report.json').read_text());need(len(controls['damages_rejected'])==11 and len(controls['partition_oracle_cases'])==15,'controls coverage')
    guards=[]
    for name in ['constructions.py','controls.py','check.py']:
        for mode in ['argument','environment']:
            env=dict(os.environ);cmd=[sys.executable]
            if mode=='argument':cmd+=['-O']
            else:env['PYTHONOPTIMIZE']='1'
            cmd += [str(packet/name),'--help']
            r=subprocess.run(cmd,capture_output=True,env=env,timeout=10)
            need(r.returncode!=0 and b'normal Python required' in r.stderr,'optimization guard')
            guards.append({'file':name,'mode':mode,'returncode':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()})
    (out/'guards.json').write_text(json.dumps(guards,indent=2)+'\n')
    native=None
    if a.render:
        native_dir=out/'native';native_dir.mkdir()
        cmd=['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(native_dir),str(packet/'constructions.tex')]
        for i in range(2):receipts.append(run(cmd,out/('native_pass'+str(i+1)),30,cwd=packet))
        log=(native_dir/'constructions.log').read_text();need(not any(x in log for x in ['Warning','Overfull','Underfull']),'native warnings')
        from pypdf import PdfReader
        actual=PdfReader(native_dir/'constructions.pdf');expected=PdfReader(packet/'constructions.pdf')
        need(len(actual.pages)==len(expected.pages)==4,'native page count')
        need([x.extract_text() for x in actual.pages]==[x.extract_text() for x in expected.pages],'native full text')
        receipts.append(run(['/opt/homebrew/bin/gs','-q','-dNOPAUSE','-dBATCH','-sDEVICE=png16m','-r120','-sOutputFile='+str(native_dir/'page-%02d.png'),str(native_dir/'constructions.pdf')],out/'raster',30))
        for i in range(1,5):need(digest(native_dir/f'page-{i:02d}.png')==digest(packet/'native'/f'page-{i:02d}.png'),'native raster')
        native={'pages':4,'texts_equal':True,'rasters_equal':True}
    for r in exports:verify(packet/r['path'],r)
    for r in deps:
        q=Path(r['path']);verify(q if q.is_absolute() else study/q,r)
    report={'status':'PASS_L100_TWO_PROJECTIVE_CONSTRUCTIONS_COMPONENT','exports':len(exports),'dependencies':len(deps),'models':2,'truncation_routes':8,'normalizer_isomorphisms':24,'source_table_entries':20,'damages':11,'partition_oracles':15,'optimization_guards':len(guards),'native':native,'receipts':receipts,'subgroup_census_runs':0,'whole_source_credit':0}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],len(exports),len(deps))
if __name__=='__main__':main()
