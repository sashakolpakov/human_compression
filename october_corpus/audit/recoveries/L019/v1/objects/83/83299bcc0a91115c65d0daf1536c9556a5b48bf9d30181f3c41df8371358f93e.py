import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
import ast,json,argparse
from pathlib import Path
from permutation_library import parse_marks,anchors,closure,need

def orbit(t,a):
    seen={a};todo=[a]
    while todo:
        u=todo.pop()
        for p in t:
            v=p[u]
            if v not in seen:seen.add(v);todo.append(v)
    return seen

def kernel(t,j,a):
    n=len(t[0]);identity=tuple(range(n))
    prev=closure(t[:j-1]) if j>1 else {identity}
    current=closure(t[:j]);X=orbit(t[:j-1],a)
    K={p for p in current if all(p[x]==x for x in set(range(n))-X)}
    return len(K),len(K&prev),sorted(x+1 for x in X)

def run(here):
    a10=json.loads((here/'a10_inputs.json').read_text())['representatives']
    prim=json.loads((here/'primitive_inputs.json').read_text())['representatives']
    need(len(a10)==10 and [x['source_index']for x in a10]==list(range(10)),'complete A10 input')
    need(len(prim)==12 and [x['source_index']for x in prim]==list(range(12)),'complete primitive input')
    expected={(0,1,1):3,(1,0,10):4,(1,1,1):3,(2,0,10):3,
              (2,1,1):4,(3,0,10):3,(4,1,1):4,(7,0,10):4}
    actual={};results=[]
    for row in a10:
        marks=parse_marks(row,10,5)
        for rev,t in enumerate([marks,marks[::-1]]):
            for a in anchors(t):
                key=(row['source_index'],rev,a+1)
                need(key in expected,'unexpected A10 anchor')
                j=expected[key];K,M,X=kernel(t,j,a)
                need([K,M]==([60,10]if j==3 else[360,60]),'exact A10 supported kernel')
                actual[key]=j;results.append({'source_index':key[0],'orientation':rev,'anchor':a+1,'prefix_length':j,'kernel_order':K,'previous_intersection_order':M,'anchor_orbit':X})
    need(actual==expected,'all eight A10 anchors')
    primitive_anchors=[]
    for row in prim:
        marks=parse_marks(row,row['n'],len(row['permutations']))
        # Evenness is checked literally, by the parity of disjoint transpositions.
        even=all(sum(p[x]!=x for x in range(len(p)))%4==0 for p in marks)
        for rev,t in enumerate([marks,marks[::-1]]):
            for a in anchors(t):
                if not even:continue
                need(row['n']==6 and len(t)==3 and row['source_index']<=2,'proper primitive even anchor')
                need(len(closure(t))==60 and len(closure(t[1:]))==10,'A5 and D10 orders')
                other=next(x for x in range(6) if x!=a)
                need(orbit(t[1:],other)==set(range(6))-{a},'transitive five-point tail')
                kernels=[kernel(t,j,a)for j in range(1,4)]
                need(all(K==M for K,M,X in kernels),'A5 leaf conditions')
                primitive_anchors.append({'source_index':row['source_index'],'orientation':rev,'anchor':a+1,'kernels':kernels})
    need([(x['source_index'],x['orientation'])for x in primitive_anchors]==[(0,1),(1,0),(1,1),(2,0)],'four exact A5 orientations')
    imprimitive=[]
    for line in (here/'n8k4/stdout.log').read_text().splitlines():
        if not line.startswith('SOLUTION|'):continue
        p=ast.literal_eval(line.split('|')[-1]);t=parse_marks({'permutations':p},8,4)
        need(0 in anchors(t),'recorded anchor')
        last_omission=closure(t[:-1]);need(orbit(t[:-1],0)==set(range(8)),'transitive last omission')
        imprimitive.append({'permutations':p,'group_order':len(closure(t)),'last_omission_order':len(last_omission),'last_omission_orbit':list(range(1,9))})
    need([x['last_omission_order']for x in imprimitive]==[64,48] and all(x['group_order']==192 for x in imprimitive),'two imprimitive exclusions')
    return {'status':'PASS_LITERAL_SMALL_EVEN_ANCHORS','A10':results,'proper_primitive':primitive_anchors,'imprimitive8':imprimitive,'whole_original_credit':0,'new_census_in_this_checker':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    r=run(a.input_dir);a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
