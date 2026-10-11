#!/usr/bin/env python3
"""Check the exact four-location bibliography delta; mathematical files are inherited."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
DOCS=['umbrella','chiral-projective-lines','chiral-projective-groups']
TEXTS=[d+'.tex'for d in DOCS]+['retained_inputs.json']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def need(b,m):
 if not b:raise ValueError('E_BIBLIOGRAPHY_REJECT '+m)
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def texts(p):return [x.extract_text()or''for x in PdfReader(p).pages]
def verify(prior=None):
 original=ROOT/'provenance/original_manifest.json';review=ROOT/'provenance/independent_manifest.json'
 need(sha(original)=='533612648b17120fada68d10141d4852d9b90b93ccf3bcca4f6163975bcad640','original manifest')
 need(sha(review)=='79665aca7c42d2153c32f4dd367bec1fcb3aa7ee9f249ac18a1bc350be7010be','distinct review manifest')
 if(ROOT/'manifest.json').exists():
  for r in load(ROOT/'manifest.json')['exports']:
   p=ROOT/r['path'];need(p.stat().st_size==r['bytes']and sha(p)==r['sha256'],'current export '+r['path'])
 changed=set(TEXTS+['proof_map.json']+[d+'.pdf'for d in DOCS]);rows=load(original)['exports'];unchanged=[];envs={}
 oldproof=load(ROOT/'provenance/original_proof_map.json');expected=load(ROOT/'provenance/original_proof_map.json')
 for r in rows:
  p=ROOT/r['path']
  if r['path'] not in changed:need(p.stat().st_size==r['bytes']and sha(p)==r['sha256'],'unchanged export '+r['path']);unchanged.append(r['path'])
  elif r['path']in TEXTS:
   t=p.read_text();need(t.count('493')==1 and '435'not in t,'one literal new locator '+r['path']);old=t.replace('493','435');raw=old.encode();need(len(raw)==r['bytes']and hashlib.sha256(raw).hexdigest()==r['sha256'],'exact old text reconstruction '+r['path'])
   pat=r'\\begin\{(theorem|lemma|proposition|corollary|proof|definition)\}.*?\\end\{\1\}'
   ee=lambda s:[m.group()for m in re.finditer(pat,s,re.S)]
   need(ee(t)==ee(old),'mathematical environments changed');envs[r['path']]=len(ee(t))
  if prior:
   p0=prior/r['path'];need(p0.stat().st_size==r['bytes']and sha(p0)==r['sha256'],'complete original input '+r['path'])
 for row in expected['contexts'].values():
  raw=''.join((ROOT/row['path']).read_text().splitlines(keepends=True)[row['start_line']-1:row['end_line']]).encode();row.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
 need(load(ROOT/'proof_map.json')==expected,'exact span rebindings only')
 spans=[k for k in expected['contexts']if expected['contexts'][k]!=oldproof['contexts'][k]];need(set(spans)=={'chiral-projective-groups.5','chiral-projective-lines.3'},'exact two context changes')
 all_math=[]
 pat=r'\\begin\{(theorem|lemma|proposition|corollary|proof|definition)\}.*?\\end\{\1\}'
 for r in rows:
  if r['path'].endswith('.tex') and 'programs'not in r['path']:
   p=ROOT/r['path'];ss=p.read_text();before=ss.replace('493','435')if r['path']in TEXTS else ss
   ee=lambda s:[m.group()for m in re.finditer(pat,s,re.S)]
   need(ee(ss)==ee(before),'whole math environment equality');all_math.append({'path':r['path'],'environments':len(ee(ss)),'sha256':[hashlib.sha256(x.encode()).hexdigest()for x in ee(ss)]})
 pages=[]
 for d in DOCS:
  current=texts(ROOT/(d+'.pdf'));row={'document':d,'pages':len(current),'page_text_hashes':[hashlib.sha256(x.encode()).hexdigest()for x in current]}
  if prior:
   old=texts(prior/(d+'.pdf'));need(len(current)==len(old),'same pages');expectedtexts=[x.replace('435','493')for x in old];need(current==expectedtexts,'only locator in extracted pages '+d);row['changed_pages']=[i for i,(a,b)in enumerate(zip(old,current),1)if a!=b]
  pages.append(row)
 return {'all_mathematical_environments':all_math,'mathematical_environment_total':sum(r['environments']for r in all_math),'unchanged_original_exports':len(unchanged),'changed_original_exports':sorted(changed),'mathematical_environments_in_affected_files':envs,'rebound_contexts':spans,'PDFs':pages}
def render(out,xelatex):
 src=out/'src';src.mkdir(parents=True)
 for p in list(ROOT.glob('*.tex'))+list(ROOT.glob('sections/*.tex')):
  q=src/p.relative_to(ROOT);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
 rows=[]
 for d in DOCS:
  target=out/d;target.mkdir()
  for i in [1,2]:
   run=subprocess.run([xelatex,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(target.resolve()),d+'.tex'],cwd=src,capture_output=True,text=True,timeout=180)
   (target/f'pass{i}.stdout').write_text(run.stdout);(target/f'pass{i}.stderr').write_text(run.stderr);need(run.returncode==0,'fresh XeLaTeX '+d)
  diagnostics=[s for s in(target/(d+'.log')).read_text().splitlines()if re.search('Overfull|Underfull|Missing character|Missing glyph|Warning:',s)]
  need(not diagnostics,'final diagnostics '+d+str(diagnostics));rows.append({'document':d,'pdf':str(target/(d+'.pdf')),'diagnostics':diagnostics})
 return rows
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--prior-dir',type=Path);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args()
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);report=verify(a.prior_dir)
 if a.render:
  renders=render(a.out/'render',a.xelatex)
  for row in renders:need(texts(Path(row['pdf']))==texts(ROOT/(row['document']+'.pdf')),'fresh current PDF page equality');row['identical_page_text']=True
  report['fresh_renders']=renders
 report.update(status='PASS_BIBLIOGRAPHY_ONLY',GAP_rerun=False,Lean_rerun=False,source_scope_unchanged=True,no_ratio=True,no_new_credit=True)
 dump(a.out/'report.json',report);print(json.dumps(report))
if __name__=='__main__':main()
