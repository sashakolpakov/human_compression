"""Literal point conjugacy and reversal, with exact interval receipt checks."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse, ast, json
from pathlib import Path

def need(ok, message):
    if not ok:
        raise ValueError(message)

def rooted(t, root):
    n=len(t[0]);queue=[root];indices={root:0}
    for v in queue:
        for g in t:
            if g[v] not in indices:
                indices[g[v]]=len(queue);queue.append(g[v])
    need(len(queue)==n,'transitive tuple')
    return tuple(tuple(indices[g[v]] for v in queue) for g in t)

def key(t):
    return min(rooted(t,v) for v in range(len(t[0])))

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--degree',type=int,required=True)
    p.add_argument('--rank-limit',type=int,required=True);a=p.parse_args()
    n=a.degree;limit=a.rank_limit
    need(n>=5 and n!=6 and 3<=limit<n,'natural alternating target and rank interval')
    text=a.input.read_text();lines=[s.strip() for s in text.splitlines() if s.strip()]
    end='COMPLETE_ALTERNATING_INTERVAL_VALIDATION'
    need(text.count(end)==1 and lines[-1]==end,'terminal complete interval validation')
    tuples=[]
    for line in lines:
        if not line.startswith('SOLUTION|'):continue
        raw=ast.literal_eval(line.split('|',1)[1]);need(type(raw)is list and 3<=len(raw)<=limit,'literal tuple')
        need(all(type(g)is list and len(g)==n and all(type(x)is int for x in g)and sorted(g)==list(range(1,n+1))for g in raw),'permutation arrays')
        t=tuple(tuple(x-1 for x in g)for g in raw)
        need(len(set(t))==len(t),'distinct marked involutions')
        need(all(any(g[x]!=x for x in range(n))and all(g[g[x]]==x for x in range(n))for g in t),'nonidentity involutions')
        need(all(all(g[h[x]]==h[g[x]]for x in range(n))for i,g in enumerate(t)for j,h in enumerate(t)if abs(i-j)>1),'literal string relations')
        tuples.append(t)
    checks=sum((len(t)-1)*(len(t)-2)//2 for t in tuples)
    tail=[f'DEGREE|{n}',f'RANK_LIMIT|{limit}',f'VALIDATED_TUPLES|{len(tuples)}',f'INTERVAL_CHECKS|{checks}',end]
    need(lines[-5:]==tail and len(lines)==len(tuples)+5,'exact complete receipt and no extra lines')
    rows=[];mappings=[]
    for r in range(3,limit+1):
        ts=[t for t in tuples if len(t)==r];keys=[key(t)for t in ts]
        need(len(keys)==len(set(keys)),'distinct ordered point-conjugacy classes')
        locate={k:i for i,k in enumerate(keys)};rev=[locate[key(tuple(reversed(t)))]for t in ts]
        need(all(rev[rev[i]]==i for i in range(len(ts))),'reversal involution')
        selfdual=sum(i==j for i,j in enumerate(rev));fused=len({min(keys[i],keys[j])for i,j in enumerate(rev)})
        need(fused==(len(ts)+selfdual)//2,'orbit count')
        rows.append(dict(rank=r,ordered=len(ts),self_dual=selfdual,with_duality=fused));mappings.append(dict(rank=r,reversal=rev))
    report=dict(status='PASS_LITERAL_ALTERNATING_INTERVAL_CLASSES',degree=n,rank_limit=limit,tuples=len(tuples),interval_checks=checks,rows=rows,reversal_maps=mappings,
        attribution='Exact rooted coloured traversal from accepted L019/S10/S11; the input terminal marker now records the separately reviewed interval IP criterion.')
    a.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='reversal_maps'}))

if __name__=='__main__':main()
