"""Independent integer-permutation closure and literal coset-incidence checks."""
import sys
if sys.flags.optimize: raise SystemExit('optimized execution unsupported')
import argparse,itertools,json,time
from pathlib import Path

def need(v,message):
    if not v: raise ValueError(message)
def mul(a,b): return tuple(b[x] for x in a)
def closure(gens,one):
    seen={one}; queue=[one]
    for a in queue:
        for b in gens:
            c=mul(a,b)
            if c not in seen: seen.add(c);queue.append(c)
    return seen
def order(g):
    import math
    seen=set();answer=1
    for a in range(len(g)):
        if a not in seen:
            b=a;n=0
            while b not in seen: seen.add(b);b=g[b];n+=1
            answer=math.lcm(answer,n)
    return answer
def validate(row,M):
    gens=[tuple(x-1 for x in p) for p in row['permutations']];n=len(gens[0]);one=tuple(range(n))
    need(len(gens)==4 and all(sorted(g)==list(one) for g in gens),'malformed permutations')
    need(all(order(g)==2 for g in gens),'noninvolutory mark')
    need([[order(mul(a,b)) for b in gens] for a in gens]==M,'pair matrix')
    sub={m:closure([gens[i] for i in range(4) if m>>i&1],one) for m in range(16)}
    need(len(sub[15])==row['order'],'group order')
    failed=[]
    for a in range(16):
        for b in range(16):
            if sub[a]&sub[b]!=sub[a&b]: failed.append([a,b,len(sub[a]&sub[b]),len(sub[a&b])])
    result={'type':row['type'],'node':row['node'],'order':row['order'],'local_orders':[len(sub[15^(1<<i)]) for i in range(4)],'intersection_failures':failed,'flag_failures':[]}
    if failed: return result
    # A right coset consists of the actual products h*g with h in the parabolic.
    # No GAP coset action or quotient representation is used here.
    elements=sorted(sub[15]); ids={g:i for i,g in enumerate(elements)}
    for k in range(4):
        available=set(range(len(elements))); cosets=[]; p=sub[15^(1<<k)]
        while available:
            g=elements[min(available)]; c={ids[mul(h,g)] for h in p}
            need(c<=available,'cosets do not partition');available-=c;cosets.append(c)
        base=[{ids[g] for g in sub[15^(1<<i)]} for i in range(4)]
        for J in range(16):
            if J>>k&1: continue
            actual=sum(all(c&base[i] for i in range(4) if J>>i&1) for c in cosets)
            expected=len(sub[15^J])//len(sub[15^(J|1<<k)])
            if actual!=expected:result['flag_failures'].append([J,k,actual,expected])
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    rows=json.loads(a.input.read_text());results=[];start=time.monotonic()
    for row in rows:
        M=row.get('matrix')
        if M is None:
            from run import TYPES
            shape,labels,_,_=TYPES[row['type']];M=[[1 if i==j else 2 for j in range(4)] for i in range(4)]
            edges={'square':[(0,1),(1,2),(2,3),(3,0)],'string':[(0,1),(1,2),(2,3)],'star':[(0,1),(0,2),(0,3)]}[shape]
            for (i,j),v in zip(edges,labels):M[i][j]=M[j][i]=v
        r=validate(row,M);results.append(r)
        if row.get('expected_reject',False):need(r['intersection_failures'] or r['flag_failures'],'negative unexpectedly passes')
        else:need(not r['intersection_failures'] and not r['flag_failures'],'positive rejected')
        print(row['type'],row['node'],row['order'],'PASS',flush=True)
    a.out.write_text(json.dumps({'status':'PASS','seconds':time.monotonic()-start,'rows':results},indent=2)+'\n')
if __name__=='__main__':main()
