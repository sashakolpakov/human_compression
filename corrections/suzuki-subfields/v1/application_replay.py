"""Public adapter for unchanged Suzuki controls and complete native manuscripts."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,shutil,subprocess,time
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--policy',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 S=a.study.resolve();O=a.out.resolve();policy=load(a.policy)
 need(not O.exists()and not O.is_relative_to(S),'Fresh external output');O.mkdir(parents=True)
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';started=time.monotonic();results=[];commands=[];guards=[]
 def run(label,cmd,cwd,out,cap=60):
  t=time.monotonic()
  try:r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=cap)
  except subprocess.TimeoutExpired as e:
   (out/(label+'.stdout')).write_bytes(e.stdout or b'');(out/(label+'.stderr')).write_bytes(e.stderr or b'');raise
  (out/(label+'.stdout')).write_bytes(r.stdout);(out/(label+'.stderr')).write_bytes(r.stderr)
  commands.append(dict(label=label,command=cmd,returncode=r.returncode,seconds=time.monotonic()-t))
  need(r.returncode==0 and not r.stderr,'Clean completed '+label);return r
 from pypdf import PdfReader
 texts=lambda p:[page.extract_text()for page in PdfReader(p).pages]
 for c in policy['components']:
  sid=c['source_id'];P=S/c['author']['packet'];D=O/sid;D.mkdir();stem=c['manuscript_stem'];program=P/c['program']
  need(sid in ['L110','L114','L115'],'Known separately reviewed application')
  need(c['argument_style'] in ['positional','named_out'],'Explicit unchanged CLI')
  args=(['--out'] if c['argument_style']=='named_out' else [])+[str(D/'control.json')]
  run(sid+'_controls',[sys.executable,'-B',str(program)]+args,None,D)
  control=load(D/'control.json');need(control==load(P/c['expected']),'Exact unchanged scientific output '+sid)
  damages=[]
  if sid=='L115':
   spec=importlib.util.spec_from_file_location('unchanged_L115_control',program);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
   for n,f in [(9,(1<<9)|1),(15,(1<<15)|1)]:
    try:module.run(n,f)
    except ValueError as e:
     need(str(e)in ['Frobenius identity','Rabin irreducibility'],'Exact reducible-field rejection');damages.append(dict(n=n,modulus=f,rejection=str(e)))
    else:raise ValueError('Reducible polynomial accepted')
  if sid=='L114':
   for label in ['scalar','matrix','action']:
    row=load(P/'retained/certificate.json')
    if label=='scalar':row['rank3']['order13_scalar']^=1
    elif label=='matrix':row['rank3']['order41_matrix'][0]^=1
    else:row['rank3']['action_exponent']=279
    f=D/('damaged_'+label+'.json');f.write_text(json.dumps(row));target=D/(label+'_forbidden.json')
    q=subprocess.run([sys.executable,'-B',str(program),'--out',str(target),'--certificate',str(f)],env=env,capture_output=True,timeout=30)
    (D/(label+'.stdout')).write_bytes(q.stdout);(D/(label+'.stderr')).write_bytes(q.stderr)
    need(q.returncode!=0 and not target.exists(),'Damaged fixed witness rejected '+label)
    damages.append(dict(kind=label,rejected=True))
  for p in [P/'check.py',program]:
   for mode in ['argument','environment']:
    target=D/(p.stem+'_'+mode);ee=dict(env)
    if mode=='environment':ee['PYTHONOPTIMIZE']='1'
    q=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(p),'--out',str(target)],env=ee,capture_output=True,timeout=15)
    (D/(p.stem+'_'+mode+'.stderr')).write_bytes(q.stderr)
    need(q.returncode!=0 and b'Use ordinary Python'in q.stderr and not target.exists(),'Original pre-output guard');guards.append([sid,p.name,mode])
  N=D/'native';N.mkdir();shutil.copyfile(P/(stem+'.tex'),N/(stem+'.tex'))
  expected=texts(P/(stem+'.pdf'));need(len(expected)==c['manuscript_pages'],'Complete source-specific manuscript')
  for i in range(2):run(sid+'_latex'+str(i),['pdflatex','-halt-on-error','-interaction=nonstopmode',stem+'.tex'],N,D)
  need(texts(N/(stem+'.pdf'))==expected,'Exact native page texts '+sid)
  need(not any(x in(N/(stem+'.log')).read_text()for x in ['Warning','Overfull','Underfull']),'Clean native log '+sid)
  run(sid+'_render',['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png',stem+'.pdf'],N,D)
  rasters=sorted(N.glob('page-*.png'));need(len(rasters)==c['manuscript_pages'],'Complete native raster inventory')
  results.append(dict(source_id=sid,control_status=control['status'],control_sha256=sha(D/'control.json'),native_pages=len(expected),native_text_identical=True,native_raster_sha256=[sha(p)for p in rasters],damage_controls=damages,author_scientific_code_unchanged=True))
 for mode in ['argument','environment']:
  target=O/('adapter_'+mode);ee=dict(env)
  if mode=='environment':ee['PYTHONOPTIMIZE']='1'
  q=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(Path(__file__).resolve()),'--out',str(target)],env=ee,capture_output=True,timeout=15)
  need(q.returncode!=0 and b'Unoptimized Python required'in q.stderr and not target.exists(),'Adapter pre-output guard');guards.append(['adapter',mode])
 report=dict(status='PASS_PUBLIC_SUZUKI_APPLICATION',components=results,native_pages=sum(x['native_pages']for x in results),optimization_guards=guards,commands=commands,runtime_text_patching=False,private_fallback=False,old_censuses_repeated=False,independent_GAP_repeated=False,general_proofs_verified_by_program=False,whole_original_credit=0,new_measurements=0,new_question_credit=0,new_Lean=0,seconds=time.monotonic()-started)
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
