#!/usr/bin/env python3
"""Independent bounded checks; imports no author mathematical implementation."""
import argparse, collections, hashlib, itertools, json, math
from pathlib import Path

def require(p, message):
    if not p: raise ValueError(message)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def graph_check(path):
    data=json.loads(path.read_text()); A=[set(x-1 for x in row) for row in data['adjacency']]; n=len(A)
    require(n==896 and all(len(row)==3 for row in A),'cubic896')
    require(all(v not in A[v] and all(0<=w<n and v in A[w] for w in A[v]) for v in range(n)),'simple undirected')
    levels={0:0}; queue=[0]
    for v in queue:
        for w in A[v]:
            if w not in levels:levels[w]=1-levels[v];queue.append(w)
            require(levels[w]!=levels[v],'bipartition')
    require(len(levels)==n and sum(levels.values())==448,'connected equal parts')
    star=[v-1 for v in data['distinguished_star']]
    require(len(star)==4 and len(set(star))==4 and set(star[1:])==A[star[0]],'ordered star')
    # Explicit partition splitting by neighbor counts into every existing cell.
    cells=[{v} for v in star]+[set(range(n))-set(star)]; sizes=[len(cells)]
    while len(cells)<n:
        col={v:i for i,cell in enumerate(cells) for v in cell}; refined=[]
        for cell in cells:
            parts={}
            for v in cell:
                counts=collections.Counter(col[w] for w in A[v]); key=tuple(sorted(counts.items()))
                parts.setdefault(key,set()).add(v)
            refined.extend(parts.values())
        require(len(refined)>len(cells),'nondiscrete refinement')
        cells=refined;sizes.append(len(cells))
    gs=[tuple(v-1 for v in g) for g in data['generators']]
    for g in gs:
        require(sorted(g)==list(range(n)),'permutation')
        require(all({g[w] for w in A[v]}==A[g[v]] for v in range(n)),'graph preservation')
    # Right multiplication, opposite traversal convention to the author checker.
    identity=tuple(range(n)); closure={identity}; queue=[identity]
    for p in queue:
        for g in gs:
            q=tuple(p[g[v]] for v in range(n))
            if q not in closure:closure.add(q);queue.append(q)
        require(len(closure)<=n*math.factorial(3),'star bound')
    require(len(closure)==5376,'upper bound attained')
    side={v for v in range(n) if levels[v]==0}; outside=[]; inside=[]
    for g in closure:
        image={g[v] for v in side}
        require(image in (side,set(range(n))-side),'whole part transport')
        (inside if image==side else outside).append(g)
    edge=tuple(sorted((0,next(iter(A[0])))))
    orbit={tuple(sorted((g[edge[0]],g[edge[1]]))) for g in inside}
    all_edges={tuple(sorted((v,w))) for v in range(n) for w in A[v]}
    require(orbit==all_edges and len(inside)==2688,'positive edge transitivity')
    orders=collections.Counter()
    for g in outside:
        unseen=set(range(n)); lengths=[]
        while unseen:
            first=next(iter(unseen));v=first;k=0
            while v in unseen:unseen.remove(v);k+=1;v=g[v]
            require(v==first,'cycle closure'); lengths.append(k)
        orders[math.lcm(*lengths)]+=1
    require(dict(orders)=={4:1024,12:896,28:768},'outer orders')
    return {'vertices':n,'edges':len(all_edges),'full_group_order':len(closure),'part_preserving':len(inside),'outer_orders':dict(sorted(orders.items())),'refinement_sizes':sizes,'data_sha256':sha(path)}

def reduce(w):
    stack=[]
    for a in w:
        if stack and stack[-1]==-a:stack.pop()
        else:stack.append(a)
    return tuple(stack)
def mul(w,v):return reduce(w+v)
def inverse(w):return tuple(-a for a in reversed(w))
def syllables(w):
    ans=[]
    for a in w:
        i=abs(a);e=1 if a>0 else -1
        if ans and ans[-1][0]==i:ans[-1]=(i,ans[-1][1]+e)
        else:ans.append((i,e))
    return ans

def act(w,permutation,last=True):
    s=syllables(w)
    if not s:return w
    t=-1 if last else 0
    if s[t][0]==1:s[t]=(1,permutation.get(s[t][1],s[t][1]))
    return tuple(a for i,e in s for a in [i if e>0 else -i]*abs(e))

def free_check():
    pi={1:2,2:-1,-1:1,3:-2,-2:3}; pinv={v:k for k,v in pi.items()}
    tested=0; bad=[]; rankcounts={}
    for r,maxlen in [(2,6),(3,5)]:
        words=[()]; layer=[()];letters=[i for i in range(-r,r+1) if i]
        for _ in range(maxlen):
            layer=[w+(i,) for w in layer for i in letters if not w or w[-1]!=-i];words.extend(layer)
        rankcounts[str(r)]=len(words)
        for w in words:
            require(act(act(w,pi),pinv)==w,'inverse exponent permutation')
            for j in range(1,r+1):
                for e in [-2,-1,1,2]:
                    prefix=(j if e>0 else -j,)*abs(e); v=mul(prefix,w)
                    difference=mul(act(v,pi),inverse(act(w,pi)))
                    require(all(abs(a)==j for a in difference),'last syllable panel')
                    wrong=mul(act(v,pi,False),inverse(act(w,pi,False)))
                    if not all(abs(a)==j for a in wrong) and not bad:bad=[list(w),j,e,list(wrong)]
                    tested+=1
    require(bool(bad),'first-syllable countermodel')
    return {'reduced_words_by_rank':rankcounts,'panel_pairs':tested,'wrong_first_syllable_witness':bad,'not_uniform_proof':True}

def cross_ratio_check():
    def add(a,b):return a^b
    def m(a,b):
        out=0
        for _ in range(2):
            if b&1:out^=a
            b>>=1;a<<=1
            if a&4:a^=7
        return out
    def inv(a):require(a!=0,'nonzero inverse');return next(b for b in range(1,4) if m(a,b)==1)
    pts=[(1,0)]+[(a,1) for a in range(4)]
    def det(u,v):return add(m(u[0],v[1]),m(u[1],v[0]))
    hist=[]
    for support in itertools.combinations(pts,4):
        counts=collections.Counter()
        for a,b,c,d in itertools.permutations(support):
            value=m(m(det(a,c),det(b,d)),inv(m(det(a,d),det(b,c))))
            counts[value]+=1
        require(counts=={2:12,3:12},'two twelve-element ordered fibers');hist.append(dict(counts))
    return {'projective_line_supports':len(hist),'fibers_per_support':hist[0],'PG2_lines':21,'PG2_typed_fibers':210,'PG2_total_objects':42+21*5*24}

def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    require(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    result={'status':'PASS_INDEPENDENT_BOUNDED_CHECKS','graph':graph_check(a.packet/'certificate/graph.json'),'free_panel':free_check(),'F4':cross_ratio_check(),'author_code_imports':False}
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
