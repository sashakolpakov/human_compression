"""Finite input inventory only: exact retained subgroups, no new census."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,collections,hashlib,json,math,time
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent;D=G/'palette_serialization_v1/derived'
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def order(p):
    seen=set();r=1
    for x in range(len(p)):
        if x in seen:continue
        y=x;k=0
        while y not in seen:seen.add(y);y=p[y];k+=1
        r=math.lcm(r,k)
    return r
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir();start=time.monotonic()
    raw=read(D/'group_elements.json');elements=[tuple(v-1 for v in p)for p in raw['elements']];orders=[order(p)for p in elements];need(len(elements)==20160 and len(set(elements))==20160,'exact acquired ambient list')
    diagrams=read(G/'source_join_component_v2/literal_diagrams01/diagrams.json')['records'];comparison=read(G/'source_join_component_v2/diagram_comparison01.json')['rows'];lookup={r['candidates'][0]['catalogue_index']:r for r in comparison}
    atoms={};routes=[];inputs=[pin(D/'group_elements.json'),pin(G/'source_join_component_v2/literal_diagrams01/diagrams.json'),pin(G/'source_join_component_v2/diagram_comparison01.json')]
    def atom(xs,role):
        xs=tuple(sorted(xs));need(xs and len(xs)==len(set(xs))and all(1<=i<=20160 for i in xs),'exact nonempty acquired set')
        if xs not in atoms:
            k=len(atoms)+1;atoms[xs]=dict(atom=k,element_positions=list(xs),order=len(xs),element_order_counts=dict(sorted(collections.Counter(orders[i-1]for i in xs).items())),roles=[])
        atoms[xs]['roles'].append(role);return atoms[xs]['atom']
    for d in diagrams:
        i=d['index'];m=read(D/f'model{i}.json');inputs.append(pin(D/f'model{i}.json'));label=lookup[i]['label'];H=[set(x)for x in m['parabolics']]
        need(len(H)==m['rank'],'one actual parabolic per type');borel=set.intersection(*H)
        br=atom(borel,dict(label=label,catalogue=i,role='BOREL'));row=dict(label=label,catalogue=i,borel_atom=br,parabolics=[])
        for t,(h,k)in enumerate(zip(H,d['local_action_kernels']),1):
            need(k['type']==t and set(k['element_positions'])<=h and k['order']==len(k['element_positions']),'actual contained local kernel')
            node=[x for x,y in lookup[i]['candidates'][0]['source_node_to_catalogue_type'].items()if y==t];need(len(node)==1,'literal source node association')
            hr=atom(h,dict(label=label,catalogue=i,role='PARABOLIC',type=t,node=node[0]));kr=atom(k['element_positions'],dict(label=label,catalogue=i,role='LOCAL_KERNEL',type=t,node=node[0]))
            row['parabolics'].append(dict(type=t,source_node=node[0],type_size=m['type_sizes'][t-1],parabolic_atom=hr,kernel_atom=kr))
        routes.append(row)
    result=dict(status='EXACT_RETAINED_PARABOLIC_INPUT_INVENTORY',models=29,parabolic_positions=sum(len(r['parabolics'])for r in routes),borel_positions=29,atoms=list(atoms.values()),routes=routes,inputs=inputs,seconds=time.monotonic()-start,structural_names_proved=False,target_censuses=0,source_credit=0)
    (a.out/'inventory.json').write_text(json.dumps(result,indent=2)+'\n')
    print('COMPLETE_INPUT_INVENTORY',len(atoms),'atoms',collections.Counter((r['order'],tuple(r['element_order_counts'].items()))for r in atoms.values()),flush=True)
if __name__=='__main__':main()
