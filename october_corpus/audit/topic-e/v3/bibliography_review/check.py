#!/usr/bin/env python3
import argparse,hashlib,json,re,copy
from pathlib import Path
from pypdf import PdfReader
H=Path(__file__).resolve().parent
PINS={'old':'533612648b17120fada68d10141d4852d9b90b93ccf3bcca4f6163975bcad640','new':'25f63875e8c717c6ca7f6064625d8407f516b78ad1639db1382c78355c0491cd','review':'79665aca7c42d2153c32f4dd367bec1fcb3aa7ee9f249ac18a1bc350be7010be'}
TEXT=['umbrella.tex','chiral-projective-lines.tex','chiral-projective-groups.tex','retained_inputs.json']
def need(b,m):
 if not b:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def bind(p,r):need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'binding '+str(p))
def exact(old,new):
 for p in TEXT:need(old[p].count(b'435')==1 and old[p].replace(b'435',b'493')==new[p],'one exact locator '+p)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--old',type=Path,required=True);ap.add_argument('--new',type=Path,required=True);ap.add_argument('--prior-review',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir()
 for key,path in [('old',a.old),('new',a.new),('review',a.prior_review)]:
  need(sha(path/'manifest.json')==PINS[key],'exact manifest '+key)
  for r in load(path/'manifest.json')['exports']:bind(path/r['path'],r)
 old={r['path']:(a.old/r['path']).read_bytes() for r in load(a.old/'manifest.json')['exports']};new={k:(a.new/k).read_bytes()for k in old}
 exact(old,new);changed=sorted(k for k in old if old[k]!=new[k]);expected=set(TEXT+['proof_map.json','umbrella.pdf','chiral-projective-lines.pdf','chiral-projective-groups.pdf']);need(set(changed)==expected,'exact changed files')
 env=re.compile(rb'\\begin\{(theorem|lemma|proposition|corollary|proof|definition)\}.*?\\end\{\1\}',re.S);count=0
 for k in old:
  if k.endswith('.tex') and 'programs'not in k:
   x=[m.group()for m in env.finditer(old[k])];y=[m.group()for m in env.finditer(new[k])];need(x==y,'mathematical environments '+k);count+=len(x)
 need(count==68,'68 mathematical environments')
 x=load(a.old/'proof_map.json');y=load(a.new/'proof_map.json');keys=[]
 for key,row in x['contexts'].items():
  b=''.join((a.new/row['path']).read_text().splitlines(keepends=True)[row['start_line']-1:row['end_line']]).encode();r=dict(row,bytes=len(b),sha256=hashlib.sha256(b).hexdigest());need(y['contexts'][key]==r,'exact span '+key)
  if row!=r:keys.append(key)
 need(set(keys)=={'chiral-projective-groups.5','chiral-projective-lines.3'},'two spans');yy=copy.deepcopy(y);yy['contexts']=x['contexts'];need(yy==x,'unchanged span metadata')
 pages=[]
 for name,expected_page in [('umbrella',20),('chiral-projective-lines',2),('chiral-projective-groups',4)]:
  o=[p.extract_text() for p in PdfReader(a.old/(name+'.pdf')).pages];n=[p.extract_text()for p in PdfReader(a.new/(name+'.pdf')).pages];need([t.replace('435','493')for t in o]==n,'exact page text '+name);changedp=[i for i,(v,w) in enumerate(zip(o,n),1)if v!=w];need(changedp==[expected_page],'one changed page');pages.append({'document':name,'pages':len(n),'changed_pages':changedp})
 controls=[]
 for name,k,mut in [('extra_text','umbrella.tex',lambda b:b+b' extra'),('wrong_page','chiral-projective-lines.tex',lambda b:b.replace(b'493',b'492')),('missed_occurrence','retained_inputs.json',lambda b:b.replace(b'493',b'435'))]:
  v=dict(new);v[k]=mut(v[k])
  try:exact(old,v)
  except ValueError:controls.append({'name':name,'rejected':True})
  else:raise ValueError('accepted corruption '+name)
 r={'status':'PASS','pins':PINS,'old_exports':98,'new_exports':116,'unchanged_old_exports':90,'changed_old_exports':changed,'identical_mathematical_environments':count,'changed_contexts':keys,'PDFs':pages,'controls':controls,'full_scientific_replay_repeated':False,'measurement_or_credit_claim':False}
 (a.out/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
