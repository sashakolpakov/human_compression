"""Literal point-conjugacy and reversal; independent of GAP's tuple fusion."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse, ast, collections, json
from pathlib import Path

def need(ok, message):
    if not ok:
        raise ValueError(message)

def rooted(t, root):
    n=11; queue=[root]; indices={root:0}
    for v in queue:
        for g in t:
            if g[v] not in indices:
                indices[g[v]]=len(queue);queue.append(g[v])
    need(len(queue)==n,'transitive tuple')
    return tuple(tuple(indices[g[v]] for v in queue) for g in t)

def key(t):
    return min(rooted(t,v) for v in range(11))

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    text=a.input.read_text();need(text.count('COMPLETE_S11_VALIDATION')==1,'terminal full IP validation')
    need(text.rstrip().endswith('COMPLETE_S11_VALIDATION'),'final terminal marker')
    tuples=[]
    for line in text.splitlines():
        if not line.startswith('SOLUTION|'):continue
        raw=ast.literal_eval(line.split('|',1)[1]);need(type(raw) is list,'literal tuple')
        need(all(type(g) is list and len(g)==11 and all(type(x) is int for x in g) and sorted(g)==list(range(1,12)) for g in raw),'permutation arrays')
        t=tuple(tuple(x-1 for x in g) for g in raw)
        need(all(any(g[x]!=x for x in range(11)) and all(g[g[x]]==x for x in range(11)) for g in t),'nonidentity involutions')
        need(all(all(g[h[x]]==h[g[x]] for x in range(11)) for i,g in enumerate(t) for j,h in enumerate(t) if abs(i-j)>1),'literal string relations')
        tuples.append(t)
    rows=[];mappings=[]
    for r in sorted(set(map(len,tuples))):
        ts=[t for t in tuples if len(t)==r];keys=[key(t) for t in ts];need(len(keys)==len(set(keys)),'distinct ordered conjugacy classes')
        locate={k:i for i,k in enumerate(keys)};rev=[locate[key(tuple(reversed(t)))] for t in ts]
        need(all(rev[rev[i]]==i for i in range(len(ts))),'reversal involution')
        selfdual=sum(i==j for i,j in enumerate(rev));fused=len({min(keys[i],keys[j]) for i,j in enumerate(rev)})
        need(fused==(len(ts)+selfdual)//2,'orbit count')
        rows.append(dict(rank=r,ordered=len(ts),self_dual=selfdual,with_duality=fused))
        mappings.append(dict(rank=r,reversal=rev))
    subset_pairs=sum(4**len(t) for t in tuples)
    need('SUBSET_PAIRS|'+str(subset_pairs)+'\n' in text,'literal subset count')
    report=dict(status='PASS_LITERAL_S11_CLASSES',tuples=len(tuples),subset_pairs=subset_pairs,rows=rows,reversal_maps=mappings,
                attribution='Rooted coloured traversal reused from accepted L019 balanced-pairs canonical argument; minimum over every point gives unrooted point conjugacy.')
    a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='reversal_maps'}))

if __name__=='__main__':main()
