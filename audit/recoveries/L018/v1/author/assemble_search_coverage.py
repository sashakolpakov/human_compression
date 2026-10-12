#!/usr/bin/env python3
"""Reconstruct exact per-parameter completed receipts; never promote UNKNOWN."""
from pathlib import Path
import json,hashlib
BASE=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
FILES={
 'squares':['packing_square_batch01.json','packing_square_refine02.json','packing_square_valleys01.json','packing_odd_valleys_840_21_01.json','packing_twenty_valleys_840_20_01.json'],
 'rectangles':['packing_rectangle_batch01.json','packing_rectangle_refine02.json','packing_rectangle_refine03.json','packing_rectangle_valleys01.json','packing_rectangle_valleys02.json']}
CPP={sha(p):p.name for p in BASE.glob('exact_packing*.cpp')}
roster=json.loads((BASE/'arithmetic_candidates.json').read_text());out={}
for kind,files in FILES.items():
 key='square_candidates'if kind=='squares'else'rectangle_candidates'
 wanted={(r['width'],r['height'],r['pieces'])for r in roster[key]}
 best={};bindings=[]
 for name in files:
  path=BASE/name
  if not path.exists():continue
  d=json.loads(path.read_text());c=d['cpp_sha256']
  if c not in CPP:raise ValueError(('unrecognized source hash',name,c))
  bindings.append({'path':name,'sha256':sha(path),'cpp':CPP[c],'cpp_sha256':c})
  for idx,r in enumerate(d.get('results',[d])):
   k=(r['width'],r['height'],r['pieces'])
   if k not in wanted:raise ValueError(('extra parameter',name,k))
   if r['status']=='FEASIBLE':raise ValueError(('target witness requires inspection',name,k))
   if r['status'] not in ['INFEASIBLE','UNKNOWN']:raise ValueError(('unexpected status',name))
   if r['status']=='INFEASIBLE' and k not in best:
    best[k]={'width':k[0],'height':k[1],'pieces':k[2],'receipt':name,'row':idx,'cpp':CPP[c],'nodes':r['nodes'],'seconds':r['seconds']}
 out[kind]={'total':len(wanted),'completed_exclusions':len(best),'unresolved':[list(k)for k in sorted(wanted-best.keys())],'receipts':bindings,'exact_per_case_route':[best[k]for k in sorted(best)]}
out['status']='COMPLETE_BOTH_FINITE_RANGES_PENDING_SCIENTIFIC_REVIEW'if all(not d['unresolved']for d in out.values())else'PARTIAL_EXACT_COVERAGE_WITH_EXPLICIT_UNRESOLVED'
out['arithmetic_roster_sha256']=sha(BASE/'arithmetic_candidates.json')
(BASE/'search_coverage.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:{j:v for j,v in d.items()if j in ['total','completed_exclusions','unresolved']}for k,d in out.items()if isinstance(d,dict)})
