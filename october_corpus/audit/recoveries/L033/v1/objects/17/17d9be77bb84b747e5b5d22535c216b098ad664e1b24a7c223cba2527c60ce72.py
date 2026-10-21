"""Independent exact 27-point obstruction, without GAP or author helpers."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json

def need(v,m):
    if not v:raise ValueError(m)
def pin(p):
    p=p.resolve();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def verify(path):
    records=json.loads(path.read_text());need(len(records)==1,'one marked tuple')
    row=records[0];gs=[tuple(x-1 for x in p)for p in row['permutations']]
    need(len(gs)==4 and all(sorted(g)==list(range(27))for g in gs),'four literal permutations')
    one=tuple(range(27))
    def mul(g,h):return tuple(h[g[i]]for i in range(27))
    def power(g,n):
        ans=one
        for _ in range(n):ans=mul(ans,g)
        return ans
    def order(g):
        h=one
        for n in range(1,100):
            h=mul(h,g)
            if h==one:return n
        raise ValueError('bounded word order')
    matrix=[[1,3,2,5],[3,1,5,2],[2,5,1,3],[5,2,3,1]]
    need(all(order(g)==2 for g in gs),'mark involutions')
    need([[1 if i==j else order(mul(gs[i],gs[j]))for j in range(4)]for i in range(4)]==matrix,'exact square matrix')
    subgroups=[]
    for mask in range(16):
        q=[one];seen={one};active=[g for i,g in enumerate(gs)if (mask>>i)&1]
        for h in q:
            for g in active:
                x=mul(h,g)
                if x not in seen:
                    seen.add(x);q.append(x)
                    need(len(seen)<=10000,'bounded literal closure')
        subgroups.append(seen)
    need(len(subgroups[15])==9720,'actual order')
    maximal=[subgroups[15^(1<<i)]for i in range(4)]
    need(list(map(len,maximal))==[120]*4,'actual local orders')
    failures=[]
    for i in range(16):
        for j in range(16):
            actual=subgroups[i]&subgroups[j]
            if actual!=subgroups[i&j]:failures.append([i,j,len(actual),len(subgroups[i&j])])
    need(len(failures)==12 and [7,11,12,6]in failures,'exact stated intersection obstruction')
    words=[]
    for omitted in range(4):
        x=one
        for i,g in enumerate(gs):
            if i!=omitted:x=mul(x,g)
        words.append(power(x,5))
    z=words[0]
    need(all(x==z for x in words) and z!=one and power(z,2)==one,'nontrivial common involution')
    need(all(mul(z,g)==mul(g,z)for g in gs),'centrality')
    common=set.intersection(*maximal)
    need(common=={one,z},'exact common maximal-parabolic intersection')
    return dict(degree=27,order=len(subgroups[15]),local_orders=list(map(len,maximal)),all_subgroup_orders=list(map(len,subgroups)),intersection_failures=failures,all_four_words_equal=True,common_maximal_intersection_order=len(common),central_involution=[x+1 for x in z])
def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);args=a.parse_args()
    W=Path(__file__).resolve().parent;P=W.parent/'divisor_v1'
    need(args.out.is_absolute()and not args.out.exists(),'fresh absolute output');args.out.mkdir()
    paths=[P/'negative.json',W/'fresh01/negative.json',Path(__file__),Path(sys.executable)]
    inputs=[pin(p)for p in paths]
    results=[verify(p)for p in paths[:2]]
    # Different compact labels are allowed: compare invariant conclusions,
    # with actual marked-isomorphism evidence supplied by the separate replay.
    keys=['degree','order','local_orders','all_subgroup_orders','intersection_failures','all_four_words_equal','common_maximal_intersection_order']
    need(all(results[0][k]==results[1][k]for k in keys),'fresh and frozen invariants')
    for row in inputs:need(pin(Path(row['path']))==row,'unchanged input')
    r=dict(status='PASS_INDEPENDENT_LITERAL_9720_OBSTRUCTION',inputs=inputs,results=results,author_helpers_imported=False,normal_quotient_searches=0,whole_original_credit=0)
    (args.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k not in ['inputs','results']}))
if __name__=='__main__':main()
