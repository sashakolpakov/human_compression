#!/usr/bin/env python3
"""Portable binding/roster/receipt/native replay; --programs repeats exact cases.

Default does NOT rerun the exhaustive searches: it independently reconstructs
arithmetic/color/source-example data and checks their complete frozen receipts.
--validate repeats small literal-program controls. --programs compiles all five
whole C++ sources and freshly repeats each unique selected parameter case.
"""
import argparse,copy,hashlib,json,subprocess,sys,shutil,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def require(c,m):
 if not c:raise ValueError(m)
def read(n):return json.loads((ROOT/n).read_text())
def run(cmd,out,cwd=ROOT,timeout=120):
 t=time.monotonic();r=subprocess.run(list(map(str,cmd)),cwd=cwd,capture_output=True,text=True,timeout=timeout)
 out.write_text(r.stdout+r.stderr);require(r.returncode==0,('command failed',cmd,r.returncode,str(out)));return time.monotonic()-t

def audit(roster,cover,receipts):
 total=0
 for kind,key in [('squares','square_candidates'),('rectangles','rectangle_candidates')]:
  want={(z['width'],z['height'],z['pieces']):z for z in roster[key]}
  sec=cover[kind];require(not sec['unresolved'],'unresolved scope')
  require(sec['total']==len(want)==sec['completed_exclusions'],'wrong scope size')
  seen=set()
  for z in sec['exact_per_case_route']:
   k=(z['width'],z['height'],z['pieces']);require(k in want and k not in seen,'extra or duplicate case');seen.add(k)
   d=receipts[z['receipt']];rows=d.get('results',[d]);require(0<=z['row']<len(rows),'invalid row');r=rows[z['row']]
   require((r['width'],r['height'],r['pieces'])==k,'wrong receipt parameter')
   require(r['status']=='INFEASIBLE' and r['placement']==[],'not a completed exclusion')
   require(r['shapes']==len(want[k]['shapes']),'wrong shape inventory')
   require(r['nodes']==z['nodes'] and r['seconds']==z['seconds'],'receipt mismatch')
   require(sha(ROOT/z['cpp'])==d['cpp_sha256'],'wrong complete program')
   require(r['nodes']>=1 and r['seconds']>=0,'invalid run observation')
  require(seen==set(want),'missing case');total+=len(seen)
 return total

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--render',action='store_true');ap.add_argument('--validate',action='store_true');ap.add_argument('--programs',action='store_true');a=ap.parse_args();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=False)
 started=time.monotonic();mf=read('manifest.json')
 for z in mf['exports']:require((ROOT/z['path']).stat().st_size==z['bytes'] and sha(ROOT/z['path'])==z['sha256'],('export mismatch',z['path']))
 if a.study_root:
  for z in read('dependencies.json')['external_bindings']:require((a.study_root/z['path']).stat().st_size==z['bytes'] and sha(a.study_root/z['path'])==z['sha256'],('source binding',z['path']))
 py=[sys.executable,'-B','-O'];run(py+['enumerate_candidates.py','--out',a.out/'arithmetic.json'],a.out/'arithmetic.log')
 roster=read('arithmetic_candidates.json');require(json.loads((a.out/'arithmetic.json').read_text())==roster,'roster reconstruction')
 for name in ['source_examples','coloring_certificate']:
  run(py+[name+'.py','--out',a.out/(name+'.json')],a.out/(name+'.log'))
  require(json.loads((a.out/(name+'.json')).read_text())==read(name+'.json'),name+' differs')
 coverage=read('search_coverage.json');names={z['receipt']for k in ['squares','rectangles']for z in coverage[k]['exact_per_case_route']};receipts={n:read(n)for n in names};cases=audit(roster,coverage,receipts)
 controls=[]
 for what in ['missing','duplicate','unknown','wrong_parameter','wrong_program','wrong_nodes','bad_scope','bad_shapes']:
  c=copy.deepcopy(coverage);rr=copy.deepcopy(receipts);s=c['squares'];z=s['exact_per_case_route'][0];d=rr[z['receipt']];r=d.get('results',[d])[z['row']]
  if what=='missing':s['exact_per_case_route'].pop()
  elif what=='duplicate':s['exact_per_case_route'].append(copy.deepcopy(z))
  elif what=='unknown':r['status']='UNKNOWN'
  elif what=='wrong_parameter':r['width']+=1
  elif what=='wrong_program':d['cpp_sha256']='0'*64
  elif what=='wrong_nodes':r['nodes']+=1
  elif what=='bad_scope':s['unresolved']=[[840,840,21]]
  elif what=='bad_shapes':r['shapes']+=1
  try:audit(roster,c,rr)
  except ValueError:controls.append(what)
  else:raise ValueError('control accepted: '+what)
 # Exact example and color checks use explicit conditions under optimized Python.
 import source_examples,coloring_certificate
 ex=source_examples.reconstruct();bad=[list(z)for z in ex['perimeter84']];bad[0][0]-=1
 try:source_examples.partial(84,84,1008,bad,True)
 except ValueError:controls.append('overlapping perimeter rejected')
 else:raise ValueError('bad perimeter accepted')
 colors=coloring_certificate.derive();require(len(colors['rotation26'])==26 and len(colors['interval_patterns21'])==6,'color scope')
 require(read('source_contract.json')['whole_original_adopted'] is False,'author self-adoption')
 native=[]
 if a.render:
  from pypdf import PdfReader
  for name,pages in [('equal_area_boundaries',5),('bounded_mondrian_partitions',3)]:
   d=a.out/name;d.mkdir();shutil.copyfile(ROOT/(name+'.tex'),d/(name+'.tex'))
   for i in range(2):run(['pdflatex','-interaction=nonstopmode','-halt-on-error',name+'.tex'],d/('build'+str(i)+'.log'),cwd=d)
   text=(d/'build1.log').read_text();require('Overfull'not in text and'Warning'not in text,'native diagnostics')
   r=PdfReader(d/(name+'.pdf'));require(len(r.pages)==pages,'native pages');require([p.extract_text()for p in r.pages]==read(name+'_page_texts.json'),'native page text mismatch');native.append({'name':name,'pages':pages})
 cp=[]
 if a.validate or a.programs:
  for f in ['exact_packing.cpp','exact_packing_sides.cpp','exact_packing_valleys.cpp','exact_packing_odd_valleys.cpp','exact_packing_twenty_valleys.cpp']:
   exe=a.out/Path(f).stem;run(['clang++','-O3','-std=c++17','-include','array',ROOT/f,'-o',exe],a.out/(f+'.compile.log'));cp.append(f)
 if a.validate:
  run(py+['validate_search_variant.py','--cpp','exact_packing_valleys.cpp','--binary',a.out/'exact_packing_valleys','--out',a.out/'grid_controls'],a.out/'grid_controls.log')
  run(py+['validate_specializations.py','--out',a.out/'special_controls'],a.out/'special_controls.log')
 fresh=[]
 if a.programs:
  unique={}
  for kind in ['squares','rectangles']:
   for z in coverage[kind]['exact_per_case_route']:unique.setdefault((z['width'],z['height'],z['pieces']),z)
  for k,z in sorted(unique.items()):
   cap=max(5.,4*z['seconds']+5);cmd=[a.out/Path(z['cpp']).stem,*map(str,k),str(cap)];r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,timeout=cap+30);require(r.returncode==0,'finite execution failure');d=json.loads(r.stdout)
   require(d['status']=='INFEASIBLE' and d['nodes']==z['nodes'] and(d['width'],d['height'],d['pieces'])==k,'fresh finite result mismatch');fresh.append(d)
   if len(fresh)%100==0:(a.out/'fresh_finite_partial.json').write_text(json.dumps(fresh)+'\n')
  (a.out/'fresh_finite.json').write_text(json.dumps(fresh,indent=2)+'\n')
 report={'status':'PASS','exports':len(mf['exports']),'source_rows':len(read('source_contract.json')['rows']),'square_cases':103,'rectangle_cases':11126,'case_routes':cases,'controls':controls,'native':native,'compiled_whole_programs':cp,'fresh_exhaustive_unique_cases':len(fresh),'saved_receipts_reused':not a.programs,'seconds':time.monotonic()-started,'scope':'Complete principal candidate, distinct scientific acceptance pending; no original/factor/question/Lean credit.'}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
