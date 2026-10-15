"""Literal intermediate flag stabilizers; no ambient or geometry census."""
import sys
if not __debug__: raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,importlib.util,itertools,json,time
from pathlib import Path
P=Path(__file__).resolve().parent; G=P.parent
OLD=G/'parabolic_component_v2'
sys.path.insert(0,str(OLD))
import atoms_v3 as A
import validate as V
need=A.need; read=A.read

def table():
    # Fixed preprint physical p15, Lemma 4.3; indices are its construction types.
    return {
      (1,):'2^4:A5',(2,):'2^4:A5',(3,):'A6',(4,):'A6',(5,):'2^4:S3',
      (1,2):'A5',(1,3):'A5',(1,4):'S4',(1,5):'2^3',
      (2,3):'A5',(2,4):'A5',(2,5):'2^4:3',(3,4):'3:S3',
      (3,5):'S4',(4,5):'S4',
      (1,2,3):'D10',(1,2,4):'S3',(1,2,5):'2^2',(1,3,4):'S3',
      (1,3,5):'2^2',(1,4,5):'2^2',(2,3,4):'S3',
      (2,3,5):'A4',(2,4,5):'A4',(3,4,5):'S3',
      (1,2,3,4):'2',(1,2,3,5):'2',(1,2,4,5):'2',
      (1,3,4,5):'2',(2,3,4,5):'3',(1,2,3,4,5):'1'}

def input_sets(C):
    m=read(G/'constructions_component_v1/expected/model_5.1.json')
    need(m['retained_types']==[1,2,3,4,5] and len(m['base_objects'])==5,'literal construction type order')
    objects=m['base_objects']
    # Every object, including the point and pair, is represented by its point mask.
    stabilizers=[{h for h,p in enumerate(C.es) if A.image(mask,p)==mask} for mask in objects]
    orders={tuple(x+1 for x in r['types']):r['stabilizer_order'] for r in m['flag_rows']}
    out={}
    for I in table():
        H=set.intersection(*(stabilizers[i-1] for i in I))
        need(len(H)==orders[I],'accepted actual flag order')
        out[I]=H
    return objects,out

def special(C,H,I):
    n=len(H); gs=C.generators(H)
    base=dict(atom=list(I),order=n,generators=[g+1 for g in gs])
    if n==10:
        for a in sorted(H):
            if C.order(a)!=5:continue
            for b in sorted(H):
                if C.order(b)==2 and C.conjugate(a,b)==C.inverse[a]:
                    words=[C.product(C.power(a,i),C.power(b,j)) for i in range(5) for j in range(2)]
                    need(len(set(words))==10 and set(words)==H,'exact dihedral ten words')
                    return base|dict(name='D10',method='dihedral_ten',generators=[a+1,b+1],normal_forms=[h+1 for h in words])
        raise ValueError('no D10 witness')
    need(n==48,'only two new atom methods')
    N={h for h in H if C.order(h)<=2}; need(len(N)==16,'sixteen involution translations')
    bs=C.generators(N);need(len(bs)==4 and all(C.product(x,y)==C.product(y,x) for x in bs for y in bs),'commuting binary basis')
    coords={C.one:(0,0,0,0)}
    for j,b in enumerate(bs):
        coords|={C.product(h,b):tuple(v[k]+(k==j) for k in range(4)) for h,v in list(coords.items())}
    need(len(coords)==16 and set(coords)==N,'binary coordinates exhaust N')
    r=next(h for h in sorted(H) if C.order(h)==3)
    need(all(C.conjugate(x,g) in N for x in N for g in gs),'actual radical normality')
    need(all(C.conjugate(x,r)!=x for x in N if x!=C.one),'fixed-point-free order-three action')
    action=[list(coords[C.conjugate(b,r)]) for b in bs]
    words=[C.product(h,C.power(r,i)) for h in coords for i in range(3)]
    need(len(set(words))==48 and set(words)==H,'actual split product')
    return base|dict(name='2^4:3',method='binary_four_by_three',normal_basis=[b+1 for b in bs],
                     complement_generator=r+1,action_columns=action,normal_forms=[h+1 for h in words])

def validate(C,H,r):
    if r['method'] not in ['dihedral_ten','binary_four_by_three']:
        V.validate_atom(C,H,r);return
    need(len(H)==r['order'] and C.closure([x-1 for x in r['generators']])==H,'actual special generating list')
    if r['method']=='dihedral_ten':
        a,b=[x-1 for x in r['generators']]
        need(r['name']=='D10' and len(H)==10 and C.order(a)==5 and C.order(b)==2 and C.conjugate(a,b)==C.inverse[a],'D10 defining relations')
        words=[C.product(C.power(a,i),C.power(b,j)) for i in range(5) for j in range(2)]
    else:
        bs=[x-1 for x in r['normal_basis']]; z=r['complement_generator']-1
        need(r['name']=='2^4:3' and len(H)==48 and len(bs)==4 and set(bs)<=H and z in H and C.order(z)==3,'literal E16/C3 factors')
        need(all(C.order(b)==2 for b in bs) and all(C.product(x,y)==C.product(y,x) for x in bs for y in bs),'binary basis relations')
        coords={C.one:(0,0,0,0)}
        for j,b in enumerate(bs):coords|={C.product(h,b):tuple(v[k]+(k==j) for k in range(4)) for h,v in list(coords.items())}
        need(len(coords)==16 and set(coords)<=H,'actual distinct sixteen coordinate words')
        need(all(C.conjugate(h,z) in coords for h in coords),'C3 normalizes translations')
        need([list(coords[C.conjugate(b,z)]) for b in bs]==r['action_columns'],'literal action columns')
        need(all(C.conjugate(h,z)!=h for h in coords if h!=C.one),'no nonzero fixed translation')
        words=[C.product(h,C.power(z,i)) for h in coords for i in range(3)]
    need([x+1 for x in words]==r['normal_forms'] and len(words)==len(set(words))==len(H) and set(words)==H,'all actual normal forms once')

def compare_source(records):
    need(len(records)==31 and {tuple(r['source_types']) for r in records}==set(table()),'all31 exact nonempty types')
    for r in records:need(r['certificate']['name']==table()[tuple(r['source_types'])],'exact source structural name')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh output');a.out.mkdir();start=time.monotonic();C=A.Context();objects,sets=input_sets(C);records=[]
    for I,H in sets.items():
        cert=special(C,H,I) if len(H) in [10,48] else A.certify(C,dict(atom=list(I),element_positions=[x+1 for x in sorted(H)]))
        validate(C,H,cert)
        records.append(dict(source_types=list(I),element_positions=[h+1 for h in sorted(H)],certificate=cert))
        print('FLAG',I,len(H),cert['name'],flush=True)
    compare_source(records)
    damages=[]
    def reject(name,f):
        try:f()
        except (ValueError,KeyError,IndexError,TypeError,StopIteration):damages.append(name);return
        raise ValueError('damaged certificate accepted '+name)
    for method in sorted({r['certificate']['method'] for r in records}):
        row=next(r for r in records if r['certificate']['method']==method and len(r['element_positions'])>1)
        bad=copy.deepcopy(row['certificate']);bad['generators']=[C.one+1]
        reject('wrong-generator-'+method,lambda row=row,bad=bad:validate(C,sets[tuple(row['source_types'])],bad))
    for n in [10,48]:
        row=next(r for r in records if len(r['element_positions'])==n);bad=copy.deepcopy(row['certificate']);bad['normal_forms'][0]=bad['normal_forms'][1]
        reject('duplicate-normal-form-'+str(n),lambda row=row,bad=bad:validate(C,sets[tuple(row['source_types'])],bad))
    row=next(r for r in records if len(r['element_positions'])==48);bad=copy.deepcopy(row['certificate']);bad['action_columns'][0]=[0,0,0,0]
    reject('wrong-actual-action',lambda:validate(C,sets[tuple(row['source_types'])],bad))
    wrong=copy.deepcopy(records);wrong[0]['source_types']=wrong[1]['source_types'];reject('duplicate-source-types',lambda:compare_source(wrong))
    wrong=copy.deepcopy(records);wrong[0]['certificate']['name']='A6';reject('wrong-source-name',lambda:compare_source(wrong))
    reject('missing-source-types',lambda:compare_source(records[:-1]))
    out=dict(status='PASS_LITERAL_INTERMEDIATE_FLAG_STRUCTURES',base_objects=objects,source_type_order=['line','point','hyperoval H3','hyperoval H4','point pair'],records=records,damage_controls=damages,target_censuses=0,source_credit=0,seconds=time.monotonic()-start)
    (a.out/'report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['records','base_objects']}))
if __name__=='__main__':main()
