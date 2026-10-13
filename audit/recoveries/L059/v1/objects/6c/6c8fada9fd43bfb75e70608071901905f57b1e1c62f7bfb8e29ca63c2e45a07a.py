from pathlib import Path
import re,json,collections,sys,hashlib
if sys.flags.optimize:raise RuntimeError('optimized Python unsupported')
W=Path(__file__).resolve().parent;results={};source={}
for p in (W/'current_c4_census').glob('*.done'):
    results[p.stem]=p.with_suffix('.g');source[p.stem]='complete_subgroup_classes'
for p in (W/'current_c4_descent').glob('*.receipt.json'):
    r=json.loads(p.read_text())
    if r['status']=='PASS':results[r['name']]=p.parent/(r['name']+'.g');source[r['name']]='maximal_subgroup_descent'
expected={f"{r['n']:03d}_{r['i']:03d}" for r in json.loads((W/'current_c4_census_scope.json').read_text())['selected']}
if set(results)!=expected:raise ValueError({'missing':sorted(expected-results.keys()),'extra':sorted(results.keys()-expected)})
mc=collections.Counter();nc=collections.Counter();rows=[]
for name,p in sorted(results.items()):
    s=p.read_text()
    ms=[''.join(re.findall(r'"([^"]*)"',x)) for x in re.findall(r'maxcode := \[(.*?)\]',s,re.S)]
    ns=[''.join('Y' if t=='true' else 'N' for t in re.findall('true|false',x)) for x in re.findall(r'normcode := \[(.*?)\]',s,re.S)]
    if len(ms)!=len(ns) or any(len(x)!=4 for x in ns):raise ValueError(name)
    mc.update(ms);nc.update(ns)
    rows.append({'graph':name,'markings':len(ms),'max':dict(collections.Counter(ms)),'norm':dict(collections.Counter(ns)),'certificate':str(p.relative_to(W)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'method':source[name]})
targetmax={'2TXX2T':11,'2TXXM':1,'X2TXX':26,'2TXMM':1,'2TXXX':19,'XX2T2T':1,'XXMM':17,'2T2TMM':5,'X2T2TX':11,'2T2TXX':38,'XXXX':1503,'2T2T2T2T':10}
targetnorm={'YNNN':466,'NNYN':4,'YNNY':525,'NYNN':4,'NNYY':3,'NYNY':3,'YYNN':2,'YYYY':1,'YNYN':2,'NNNN':365,'NNNY':268}
report={'status':'COMPLETE_CURRENT_QUARTIC_SCOPE','graphs':len(rows),'markings':sum(mc.values()),'max':dict(mc),'norm':dict(nc),'source_max':targetmax,'source_norm':targetnorm,'max_difference':{k:mc[k]-targetmax.get(k,0) for k in mc.keys()|targetmax.keys() if mc[k]!=targetmax.get(k,0)},'norm_difference':{k:nc[k]-targetnorm.get(k,0) for k in nc.keys()|targetnorm.keys() if nc[k]!=targetnorm.get(k,0)},'rows':rows,'historical_identity':'pending; this report does not infer identity from agreement'}
(W/'quartic_census_summary.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
