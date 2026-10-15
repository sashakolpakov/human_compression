"""Check the printed marking by a complete ordered Cayley-edge transport."""
import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,re
W=Path(__file__).resolve().parent;P=W.parent/'small_square_v1'
def need(v,m):
    if not v:raise ValueError(m)
def pin(p):
    p=p.resolve();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def mul(a,b):return tuple(b[a[i]]for i in range(len(a)))
def main():
    inputs=[pin(p)for p in [P/'square.tex',W/'fresh01/quotients.json',Path(__file__),Path(sys.executable)]]
    cycles=[[(1,3),(2,4),(5,6),(7,11),(8,12),(9,10)],[(1,5),(2,6),(3,4),(7,8),(9,11),(10,12)],[(1,2),(3,4),(5,9),(6,10),(7,12),(8,11)],[(1,6),(2,5),(3,7),(4,8),(9,10),(11,12)]]
    tex=(P/'square.tex').read_text();printed=[]
    for i,row in enumerate(cycles,1):
        literal=''.join('('+r'\ '.join(map(str,p))+')'for p in row)
        need(re.search(r't_'+str(i)+r'&='+re.escape(literal),tex) is not None,'literal printed cycles')
        p=list(range(12))
        for a,b in row:p[a-1],p[b-1]=b-1,a-1
        printed.append(tuple(p))
    positive=next(r for r in json.loads((W/'fresh01/quotients.json').read_text())if not r['expected_reject'])
    fresh=[tuple(x-1 for x in p)for p in positive['permutations']]
    one=tuple(range(12));target_one=tuple(range(len(fresh[0])));mapping={one:target_one};queue=[one];edges=0
    for x in queue:
        for a,b in zip(printed,fresh):
            xx=mul(x,a);yy=mul(mapping[x],b)
            if xx not in mapping:mapping[xx]=yy;queue.append(xx)
            need(mapping[xx]==yy,'well-defined generator-edge image');edges+=1
    need(len(mapping)==len(set(mapping.values()))==1920,'bijective ordered marked map')
    need([pin(Path(r['path']))for r in inputs]==inputs,'stable inputs')
    report=dict(status='PASS_PRINTED_WITNESS_ORDERED_ISOMORPHISM',inputs=inputs,order=len(mapping),generator_edges=edges,arrays_equal=printed==fresh,printed_arrays=[[x+1 for x in p]for p in printed],fresh_node=positive['node'])
    (W/'printed_witness.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['inputs','printed_arrays']}))
if __name__=='__main__':main()
