#!/usr/bin/env python3
"""Check bound files, evidence spans, graph accounting and declared coverage. No mathematical validity oracle."""
from pathlib import Path
import argparse, collections, copy, hashlib, json

HERE=Path(__file__).resolve().parent
LOGICAL={'proof_use','retained_input_use','retained_algorithm_use','computational_use','branch_membership','output_assembly','definition_use'}
NONLOGICAL={'attribution_identity','conceptual_correspondence','repeated_proof'}

def demand(ok,msg):
    if not ok: raise ValueError(msg)

def validate(g,c):
    ns={n['id']:n for n in g['nodes']};es=g['edges']
    demand(len(ns)==len(g['nodes']),'duplicate node')
    expected=dict(nodes=len(ns),edges=len(es),contract_rows=len(c['rows']),
      node_categories=dict(collections.Counter(n['category'] for n in g['nodes'])),
      edge_categories=dict(collections.Counter(e['kind'] for e in es)))
    for key,value in expected.items():demand(g['checks'][key]==value,'stale embedded checks '+key)
    keys=[(e['source'],e['target'],e['kind']) for e in es]
    demand(len(keys)==len(set(keys)),'duplicate edge')
    incoming=collections.defaultdict(set);outgoing=collections.defaultdict(list);degree={n:0 for n in ns}
    for e in es:
        demand(e['source'] in ns and e['target'] in ns,'dangling edge')
        if e['kind'] in LOGICAL:incoming[e['target']].add(e['source'])
        if e['kind'] not in NONLOGICAL:
            outgoing[e['source']].append(e['target']);degree[e['target']]+=1
    def closure(t):
        seen=set();todo=[t]
        while todo:
            x=todo.pop()
            if x not in seen:seen.add(x);todo.extend(incoming[x])
        return sorted(seen)
    ready=[n for n,d in degree.items() if not d];order=[]
    while ready:
        n=ready.pop();order.append(n)
        for t in outgoing[n]:
            degree[t]-=1
            if not degree[t]:ready.append(t)
    demand(len(order)==len(ns),'logical/documentary cycle')
    demand(len(c['rows'])==55 and len({r['id'] for r in c['rows']})==55,'contract row loss')
    demand(set(g['source_order'])==set(r['source_id'] for r in c['rows']),'source coverage loss')
    for r in c['rows']:demand(r['new_nodes'] and all(x in ns for x in r['new_nodes']),'unresolved row')
    demand(('UA.Fiber','UA.Mix','proof_use') not in keys,'obsolete UA.Mix dependency')
    demand('UA.Fiber' in closure('A3.T6.1'),'missing actual structural Fiber use')
    for t in ['A5.main','A6.main']:
        for code in ['census','finite','data','driver']:demand('code.'+code in closure(t),'required program omitted')
    for t in g['new_main_outputs']:demand(g['new_output_closures'][t]==closure(t),'stale closure')
    demand(all(n['cost'] is None for n in ns.values()),'cost or zero external input invented')
    demand(g['measurement']['factor'] is None,'ratio introduced')
    return dict(nodes=len(ns),edges=len(es),contracts=6,rows=55)

def main():
    a=argparse.ArgumentParser();a.add_argument('--root',type=Path,default=HERE.parent);a.add_argument('--out',type=Path,required=True)
    args=a.parse_args();root=args.root.resolve();g=json.loads((HERE/'logical_graph.json').read_text());c=json.loads((HERE/'coverage.json').read_text())
    result=validate(g,c);bound={}
    for row in g['immutable_inputs']:
        p=Path(row['path']);demand(not p.is_absolute() and '..' not in p.parts,'unsafe input path')
        q=(root/p).resolve();demand(q.is_relative_to(root),'input leaves root')
        b=q.read_bytes();demand(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'input hash mismatch '+str(p))
        bound[str(p)]=row
    spans=0
    for n in g['nodes']:
        for loc in n['locators']:
            if 'start_codepoint' not in loc:continue
            path=loc['path'];demand(path in bound,'span lacks source binding')
            text=(root/path).read_text();st=loc['start_codepoint'];en=loc['end_codepoint_exclusive']
            demand(0<=st<en<=len(text),'span bounds')
            demand(hashlib.sha256(text[st:en].encode()).hexdigest()==loc['sha256_utf8'],'span mismatch')
            spans+=1
    controls=[]
    for label,change in [
      ('corrupt embedded tally',lambda x,y:x['checks'].__setitem__('edges',0)),
      ('drop required census program',lambda x,y:x['nodes'].__setitem__(slice(None),[n for n in x['nodes'] if n['id']!='code.census'])),
      ('give retained inputs zero cost',lambda x,y:x['nodes'][next(i for i,n in enumerate(x['nodes']) if n['category']=='external')].__setitem__('cost',0)),
      ('restore superseded Mix dependency',lambda x,y:x['edges'].append(dict(source='UA.Fiber',target='UA.Mix',kind='proof_use'))),
      ('lose one admitted contract row',lambda x,y:y['rows'].pop()),
      ('introduce a theorem cycle',lambda x,y:x['edges'].append(dict(source='UA.K',target='UA.K0',kind='proof_use'))),
    ]:
        x,y=copy.deepcopy(g),copy.deepcopy(c);change(x,y)
        if label!='corrupt embedded tally':
            x['checks'].update(nodes=len(x['nodes']),edges=len(x['edges']),contract_rows=len(y['rows']),
              node_categories=dict(collections.Counter(n['category'] for n in x['nodes'])),
              edge_categories=dict(collections.Counter(e['kind'] for e in x['edges'])))
        try:validate(x,y)
        except ValueError as exc:controls.append(dict(control=label,result='REJECTED',reason=str(exc)))
        else:raise ValueError('control accepted: '+label)
    report=dict(status='PASS',**result,bound_files=len(bound),exact_locator_spans=spans,negative_controls=controls,
       scope='File/span and declared graph/accounting validation; not an automated proof of every mathematical edge.',
       full_build_or_math_replay=False,graph_sha256=hashlib.sha256((HERE/'logical_graph.json').read_bytes()).hexdigest(),
       coverage_sha256=hashlib.sha256((HERE/'coverage.json').read_bytes()).hexdigest())
    demand(not args.out.exists(),'fresh output file required');args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
