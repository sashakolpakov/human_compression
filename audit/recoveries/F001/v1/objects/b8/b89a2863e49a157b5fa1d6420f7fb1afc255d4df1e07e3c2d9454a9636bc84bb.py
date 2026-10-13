from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,time
from pypdf import PdfReader
P=Path(__file__).resolve().parent

def need(v,m):
 if not v:raise ValueError(m)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--render',action='store_true');a.add_argument('--study-root',type=Path)
 a.add_argument('--gap',default=shutil.which('gap') or '/opt/homebrew/bin/gap');a.add_argument('--pdflatex',default=shutil.which('pdflatex') or '/opt/homebrew/bin/pdflatex');args=a.parse_args()
 need(not args.out.exists(),'fresh output');args.out.mkdir(parents=True)
 count=0
 if (P/'manifest.json').exists():
  for r in json.loads((P/'manifest.json').read_text())['exports']:
   p=P/r['path'];need(p.stat().st_size==r['bytes'] and h(p)==r['sha256'],'export '+r['path']);count+=1
 if args.study_root:
  for r in json.loads((P/'provenance.json').read_text())['source_bindings']:
   p=args.study_root/r['path'];need(p.stat().st_size==r['bytes'] and h(p)==r['sha256'],'source '+r['path'])
 job=args.out/'job';job.mkdir()
 for n in ['checks.g','deleted_permutation.g']:shutil.copy2(P/n,job/n)
 start=time.monotonic()
 with (args.out/'stdout.log').open('wb') as out,(args.out/'stderr.log').open('wb') as err:
  p=subprocess.Popen([args.gap,'-q','-b','deleted_permutation.g'],cwd=job,stdout=out,stderr=err)
  try:rc=p.wait(timeout=300)
  except subprocess.TimeoutExpired:p.kill();p.wait();raise ValueError('timeout: no certificate')
 text=(args.out/'stdout.log').read_text();need(rc==0 and not (args.out/'stderr.log').read_bytes() and text.rstrip().endswith('COMPLETE_COUNTEREXAMPLE_CHECK'),'complete exact check')
 pages=None
 if args.render:
  native=args.out/'native';native.mkdir();shutil.copy2(P/'orthogonal_rank_bound.tex',native)
  for n in range(2):
   r=subprocess.run([args.pdflatex,'-interaction=nonstopmode','-halt-on-error','orthogonal_rank_bound.tex'],cwd=native,capture_output=True);(native/('pass%d.stdout'%n)).write_bytes(r.stdout);need(r.returncode==0,'render')
  log=(native/'orthogonal_rank_bound.log').read_text();need(not any(t in log for t in ['Overfull','undefined','LaTeX Warning']),'render diagnostics')
  texts=lambda p:[x.extract_text() for x in PdfReader(p).pages]
  current=texts(native/'orthogonal_rank_bound.pdf');need(current==texts(P/'orthogonal_rank_bound.pdf'),'whole page text');pages=len(current)
 report={'status':'PASS','exports':count,'seconds':round(time.monotonic()-start,6),'rank':6,'dimension':5,'field_order':7,'group_orders':[5040,5040],'full_subset_intersection_pairs_per_marking':4096,'connected_type':[3,3,3,3,3],'native_pages':pages,'whole_original_credit':0,'new_question_credit':0,'new_Lean_credit':0,'source_scope':'F001 literalLemma4.1 only; principalTheorem1.1 not refuted/recovered'}
 (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
