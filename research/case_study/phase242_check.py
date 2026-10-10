#!/usr/bin/env python3
"""Replay the bound uniform finite-cover family and independent finite witnesses."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FREEZES={'phase224_pyramid_export.json':'60253cfc8c886749476fd19bba5a9813221161f47e5aa8ea29401786bdb5772f','phase239_export.json':'6ee2cf7e548a4075c52ad54ba14a8753ce116001d5dd454718f4150efff4d135'}
def need(ok,s):
 if not ok:raise RuntimeError('PHASE242_REJECT '+s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(name,value):
 p=Path(name);need(not p.is_absolute() and '..' not in p.parts,'unsafe binding')
 p=ROOT/p
 digest=value['sha256'] if isinstance(value,dict) else value
 need(sha(p)==digest,'changed '+name)
 if isinstance(value,dict) and 'bytes' in value:need(p.stat().st_size==value['bytes'],'length '+name)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True)
 for opt in ['gap','lean','packages']:ap.add_argument('--'+opt,type=Path)
 ap.add_argument('--bindings-only',action='store_true');ap.add_argument('--verify-primary',action='store_true');a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output path')
 counts={}
 for name,digest in FREEZES.items():
  bind(name,digest);f=json.loads((ROOT/name).read_text());counts[name]=len(f['files'])
  for section in ['files','frozen_dependencies']:
   for p,v in f[section].items():bind(p,v)
 review=json.loads((ROOT/'phase242_manifest.json').read_text())
 for r in review['exports']+review['retained']:
  if not r['path'].startswith('sources/') or a.verify_primary:bind(r['path'],r)
 if a.verify_primary:
  for s in json.loads((ROOT/'phase239_sources.json').read_text())['sources']:bind(s['local_path'],s['sha256'])
 a.out.mkdir(parents=True);out=a.out.resolve()
 report={'status':'PASS_BINDINGS_ONLY','author_exports':counts,'review_exports':len(review['exports']),'primary_checked':a.verify_primary,'all_parameter_proof':'Written argument independently reviewed; finite samples do not establish universal quantifier.','all_n_cover_range':'n>=3, prime ell not dividing2n','infinite_minimal_range':'odd n>=3','full_Lean_application':False,'new_principal_source_credit':0,'general_finite_conjecture_solved':False,'matched_ratio':None}
 if not a.bindings_only:
  need(a.gap and a.lean and a.packages,'--gap --lean --packages required')
  version=subprocess.check_output([a.lean,'--version'],text=True).strip();need('version 4.32.2,' in version,'compiler pin')
  pins=json.loads((ROOT/'formal/dependency_manifest.json').read_text())
  for item in pins['packages']:
   path=a.packages/item['name'];rev=subprocess.check_output(['git','-C',path,'rev-parse','HEAD'],text=True).strip()
   need(rev==item['rev'],'dependency revision '+item['name'])
   need(subprocess.run(['git','-C',path,'diff','--quiet','HEAD','--']).returncode==0,'clean package '+item['name'])
  def run(label,cmd,timeout=240):
   r=subprocess.run([str(x) for x in cmd],cwd=ROOT,text=True,capture_output=True,timeout=timeout)
   (out/(label+'.stdout')).write_text(r.stdout);(out/(label+'.stderr')).write_text(r.stderr)
   need(r.returncode==0 and not r.stderr,label);return r.stdout
  author={}
  for phase in [224,239]:
   run('author'+str(phase),[sys.executable,'-B','-O',ROOT/f'phase{phase}_pyramid_check.py','--out',out/f'author{phase}','--gap',a.gap,'--lean',a.lean,'--packages',a.packages])
   author[phase]=json.loads((out/f'author{phase}'/'report.json').read_text());need(author[phase]['status']=='PASS','author status')
  need(sum(x['theorems'] for x in author[239]['Lean'].values())==13,'formal statement scope')
  text=run('independent_orientation',[a.gap,'-q','-T',ROOT/'phase242_orientation_check.g'],60)
  norm=' '.join(text.split());need('Error' not in norm and 'PHASE242_NATIVE_ORIENTATION_PASS' in norm and 'NO_CENTER_CONSTRAINT_REJECTED' in norm,'native orientation assertions')
  need('[ 61440, 12288, 12288, 24, 3072, 48, 3840, 16, 2, 16 ]' in norm,'native exact orders')
  surface=json.loads(run('independent_surface',[sys.executable,'-B','-O',ROOT/'phase242_surface_check.py'],60))
  need(surface['status']=='PHASE242_INDEPENDENT_SURFACE_PASS' and surface['first_Betti_dimension']==642,'independent surface assertions')
  need((out/'author224/surface_certificate.json').read_bytes()==(ROOT/'phase224_pyramid_surface_certificate.json').read_bytes(),'literal224 surface bytes')
  need((out/'author239/surface_certificate.json').read_bytes()==(ROOT/'phase239_surface_certificate.json').read_bytes(),'literal239 surface bytes')
  need((out/'author239/orientation_model.json').read_bytes()==(ROOT/'phase239_orientation_model.json').read_bytes(),'orientation input bytes')
  report.update(status='PASS_FRESH_AUTHOR_AND_INDEPENDENT_REPLAYS',Lean_declarations=13,new_Lean_declarations=4,reused_Lean_declarations=9,author224_controls=2,author239_controls=5,independent_controls=2,orientation_orders=[61440,12288,12288,24,3072,48,3840,16],surface_cells=[3840,7680,3200],complement_faces=[2704,3199,3199],compiler=version)
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
