from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,time
from pypdf import PdfReader
if sys.flags.optimize:raise RuntimeError('normal Python required')
S=Path('/Users/sasha/medusa/research/leemans');P=S/'topic_B_L019_trivial_factor_v1';W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(p,m):
    if not p:raise RuntimeError(m)
def save(n,d):(W/n).write_text(json.dumps(d,indent=2)+'\n')
def verify(r,b):
    p=Path(r['path']);p=p if p.is_absolute() else b/p
    need(sha(p)==r['sha256'] and p.stat().st_size==r['bytes'],'binding '+str(p))
need(sha(P/'manifest.json')=='a2ff156dcdfbf958bf859fe22904324e50ead924b3596a53f09a0f9c4e23cf09','edition')
man=json.loads((P/'manifest.json').read_text());deps=json.loads((P/'dependencies.json').read_text());acq=json.loads((P/'acquired_packets.json').read_text())
for r in man['exports']:verify(r,P)
for r in deps+acq:verify(r,S)
native=W/'native';native.mkdir()
for name in ['trivial_factor.tex','build.py']:shutil.copy2(P/name,native/name)
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);receipts=[]
def run(name,args,cwd,env=env,success=True):
    t=time.monotonic();p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,timeout=90)
    (W/(name+'.stdout')).write_bytes(p.stdout);(W/(name+'.stderr')).write_bytes(p.stderr)
    receipts.append({'name':name,'args':args,'cwd':str(cwd),'returncode':p.returncode,'seconds':time.monotonic()-t})
    need((p.returncode==0)==success,name+' exit');return p
r=run('native',[sys.executable,str(native/'build.py')],native);need(not r.stderr,'native stderr')
pdf=native/'trivial_factor.pdf';need(len(PdfReader(pdf).pages)==3,'page count')
need([p.extract_text() for p in PdfReader(pdf).pages]==[p.extract_text() for p in PdfReader(P/'trivial_factor.pdf').pages],'native text differs')
log=(native/'trivial_factor.log').read_text();need(not any(x in log for x in ['Overfull','Underfull','LaTeX Warning']),'native warnings')
for mode in ['flag','environment']:
    d=W/('rejected_'+mode);d.mkdir();shutil.copy2(P/'build.py',d/'build.py');shutil.copy2(P/'trivial_factor.tex',d/'trivial_factor.tex')
    args=[sys.executable]+(['-O'] if mode=='flag' else [])+[str(d/'build.py')]
    e=dict(env,PYTHONOPTIMIZE='1') if mode=='environment' else env
    run(mode,args,d,e,False);need(sorted(x.name for x in d.iterdir())==sorted(['build.py','trivial_factor.tex']),'optimized build touched outputs')
for i in [35,36]:run('source'+str(i),['/opt/homebrew/bin/gs','-q','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110',f'-dFirstPage={i}',f'-dLastPage={i}',f'-sOutputFile={W}/source{i}.png',str(S/'sources/stability2024.pdf')],W)
save('receipts.json',receipts);save('report.json',{'status':'PASS_BOUNDED_TRIVIAL_FACTOR_INTEGRITY_AND_NATIVE','exports':len(man['exports']),'dependencies':len(deps),'acquired_manifest_bindings':len(acq),'native_pages':3,'optimization_rejections':2,'finite_classification_or_new_search':False,'whole_original_credit':0});print((W/'report.json').read_text())
