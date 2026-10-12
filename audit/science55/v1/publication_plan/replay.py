"""Reconstruct exact logical frozen packets privately from distributed public routes."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, shutil, subprocess, sys
HERE=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def need(t,m):
 if not t:raise ValueError(m)
def safe(name):
 p=PurePosixPath(name);need(not p.is_absolute()and '..'not in p.parts and str(p)==name,'unsafe path');return p
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def reconstruct(repo,out):
 plan=load(HERE/'copy_plan.json')
 for r in plan['files']:
  src=repo/safe(r['public_path']);need(src.stat().st_size==r['bytes']and sha(src)==r['sha256'],'public payload '+str(src))
  dst=out/safe(r['packet'])/safe(r['logical_path']);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 for p in plan['packets']:
  root=out/p['id'];m=load(root/'manifest.json');need(len(m['exports'])==p['exports'],'whole packet count')
  for e in m['exports']:
   src=root/safe(e['path']);need(src.stat().st_size==e['bytes']and sha(src)==e['sha256'],'logical replay '+str(src))
 return plan
def render(repo,out):
 from pypdf import PdfReader
 cat=load(HERE/'native_catalogue.json');results=[]
 for row in cat['acquired_documents']+cat['new_documents']:
  d=out/row['id'];d.mkdir(parents=True);parent=Path(row['tex']).parent
  for name in [row['tex']]+row['tex_inputs']:
   relative=Path(name).relative_to(parent);q=d/relative;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((repo/name).read_bytes())
  cmd=['/opt/homebrew/bin/'+row['compiler'],'-no-shell-escape','-recorder','-interaction=nonstopmode','-halt-on-error',Path(row['tex']).name]
  for i in range(2):
   run=subprocess.run(cmd,cwd=d,capture_output=True,text=True);(d/f'pass{i+1}.txt').write_text(run.stdout+run.stderr);need(run.returncode==0,'native compiler '+row['id'])
  log=(d/(Path(row['tex']).stem+'.log')).read_text();bad=[x for x in log.splitlines()if any(z in x for z in ['Overfull','undefined','Missing character','Missing glyph'])];need(not bad,'native diagnostics '+row['id'])
  pp=lambda p:[x.extract_text()for x in PdfReader(p).pages]
  fresh=pp(d/Path(row['pdf']).name);saved=pp(repo/row['pdf']);need(fresh==saved and len(saved)==row['physical_pages'],'all exact native page texts')
  results.append(dict(id=row['id'],compiler=row['compiler'],pages=len(saved),page_text_sha256=[hashlib.sha256(x.encode()).hexdigest()for x in saved],text_equal=True,diagnostics=[]))
 return results
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 plan=reconstruct(a.repo,a.out/'packets');d=a.out/'packets/N014_author'
 run=subprocess.run([sys.executable,'-B','-O',str(d/'check.py'),'--out',str(a.out/'N014_bounded')],capture_output=True,text=True);(a.out/'N014_stdout.txt').write_text(run.stdout+run.stderr);need(run.returncode==0,'bounded N014 assembly replay')
 # L024 has no operational author runner; inspect the exact accepted certificate
 # and distinct receipts without repeating the matrix/character computations.
 l=a.out/'packets/L024_author';lr=a.out/'packets/L024_review'
 need('STATUS=PASS'in(l/'schur_example_report.txt').read_text(),'saved whole required certificate receipt')
 need(load(lr/'review.json')['status']=='ACCEPTED_CORRECTED_PRINCIPAL_RECOVERY','distinct L024 verdict')
 need(load(lr/'replay.json')['status']=='PASS','distinct saved L024 replay')
 for oid in ['N014','L024']:
  ad=load(a.out/('packets/'+oid+'_adoption/adoption.json'));need(ad['status'].startswith('ROOT_ACCEPTED')and ad['measurement']is None and not ad['theorem_sets_equivalent'],'root accepted scope')
 report=dict(status='PASS_PUBLIC_ROUTE_RECONSTRUCTION',mapped_files=len(plan['files']),packets=len(plan['packets']),N014=load(a.out/'N014_bounded/report.json'),L024='exact accepted author and distinct receipt checked; no finite rerun',new_scientific_computation=False,Lean_replayed=False)
 if a.render:report['render']=render(a.repo,a.out/'render')
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
