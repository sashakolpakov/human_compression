from pathlib import Path
import json, re, collections, hashlib, sys
if sys.flags.optimize:raise RuntimeError('optimized Python unsupported')
W=Path(__file__).resolve().parent
targetmax={'2T2TXX':315,'2T2T2T2T':4,'MMXX':587,'M2TXX':32,
 '2T2TMM':21,'M2T2TM':1,'2TMXX':32,'2TMM2T':1,'MMMM':88,'MM2T2T':1}
targetnorm={'YNYN':1,'YYYY':1,'YNNY':674,'NNNY':1,'YYNN':1,'YNNN':404}
def readrow(name,p):
    receipt=p.with_suffix('.receipt.json')
    if not receipt.exists():return None
    r=json.loads(receipt.read_text())
    if r['status']!='PASS':return {'graph':name,'status':r['status']}
    if hashlib.sha256(p.read_bytes()).hexdigest()!=r['witness_sha256']:raise ValueError('hash')
    s=p.read_text()
    mc=collections.Counter(''.join(re.findall(r'"([^"]*)"',x)) for x in re.findall(r'maxcode := \[(.*?)\]',s,re.S))
    nc=collections.Counter(''.join('Y' if t=='true' else 'N' for t in re.findall('true|false',x)) for x in re.findall(r'normcode := \[(.*?)\]',s,re.S))
    if sum(mc.values())!=sum(nc.values()):raise ValueError('count')
    return {'graph':name,'status':'PASS','markings':sum(mc.values()),'max':dict(mc),'norm':dict(nc),
            'certificate':str(p.relative_to(W)),'sha256':r['witness_sha256']}
def collect(rows,expected):
    mc=collections.Counter();nc=collections.Counter()
    for r in rows:
        if r['status']=='PASS':mc.update(r['max']);nc.update(r['norm'])
    return {'expected_graphs':expected,'available_graphs':len(rows),
            'statuses':dict(collections.Counter(r['status'] for r in rows)),
            'markings':sum(mc.values()),'max':dict(mc),'norm':dict(nc),'rows':rows}
sym=[]
for g in json.loads((W/'cubic_2048_bipartite.json').read_text()):
    p=(W/'cubic_markings'/(g['retained_id']+'.g')) if 'retained_id' in g else (W/'cubic_2048_markings'/(g['id']+'.g'))
    r=readrow(g['id'],p)
    if r:sym.append(r)
semi=[]
for g in json.loads((W/'cubic_markings/inputs.json').read_text()):
    if g['family']=='semisymmetric':
        r=readrow(g['id'],W/'cubic_markings'/(g['id']+'.g'))
        if r:semi.append(r)
sub=[]
for folder in ['subdivision_markings','nonbipartite_subdivisions']:
    for name in json.loads((W/folder/'queue.json').read_text()):
        original=W/folder/(name+'.g')
        retries=[p/(name+'.g') for p in sorted(W.glob('nonbipartite_retry[0-9][0-9]'))
                 if (p/(name+'.receipt.json')).exists()] if folder=='nonbipartite_subdivisions' else []
        if len(retries)>1:raise ValueError('multiple retry dispositions require explicit resolution')
        if retries:
            retry=retries[0]
            old=json.loads(original.with_suffix('.receipt.json').read_text())
            new=json.loads(retry.with_suffix('.receipt.json').read_text())
            if old['status']!='TIME_LIMIT_NO_CONCLUSION':raise ValueError('unexpected retry basis')
            if new['prior_capped_receipt_sha256']!=hashlib.sha256(original.with_suffix('.receipt.json').read_bytes()).hexdigest():raise ValueError('retry link')
            r=readrow(name,retry)
            r['prior_capped_receipt']=str(original.with_suffix('.receipt.json').relative_to(W))
            r['prior_capped_receipt_sha256']=new['prior_capped_receipt_sha256']
        else:r=readrow(name,original)
        if r:sub.append(r)
report={'symmetric_2048':collect(sym,714),'semisymmetric_768':collect(semi,43),'subdivisions_2048':collect(sub,796),
        'source_symmetric_max':targetmax,'source_symmetric_norm':targetnorm}
for field,target in [('max',targetmax),('norm',targetnorm)]:
    actual=report['symmetric_2048'][field]
    report['symmetric_2048'][field+'_difference']={k:actual.get(k,0)-target.get(k,0) for k in actual.keys()|target.keys() if actual.get(k,0)!=target.get(k,0)}
(W/'cubic_scopes_summary.json').write_text(json.dumps(report,indent=2)+'\n')
for k in ['symmetric_2048','semisymmetric_768','subdivisions_2048']:
    print(k,{a:b for a,b in report[k].items() if a!='rows'})
