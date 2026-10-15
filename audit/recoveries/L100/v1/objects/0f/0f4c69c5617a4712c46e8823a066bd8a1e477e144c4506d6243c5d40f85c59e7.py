"""Independent all-subgroup/all-panel-family check on tiny multiplication tables.

No GAP import, legacy function call or augmentation recurrence is used here.
Every panel subset is tested by literal coset incidence and subgroup sets.
"""
import argparse, collections, functools, hashlib, itertools, json, pathlib, time
if not __debug__: raise SystemExit('optimized execution forbidden')
def powerset(xs):
    xs=tuple(xs)
    for n in range(len(xs)+1): yield from itertools.combinations(xs,n)
class Literal:
    def __init__(self,mul):
        self.mul=mul;self.n=len(mul);self.whole=frozenset(range(self.n))
        assert all(len(r)==self.n and set(r)==set(range(self.n)) for r in mul)
        self.one=next(e for e in range(self.n) if all(mul[e][x]==mul[x][e]==x for x in range(self.n)))
        self.inv=[next(y for y in range(self.n) if mul[x][y]==mul[y][x]==self.one) for x in range(self.n)]
        assert all(mul[mul[a][b]][c]==mul[a][mul[b][c]] for a,b,c in itertools.product(range(self.n),repeat=3))
        todo=collections.deque([frozenset([self.one])]); known=set(todo)
        while todo:
            h=todo.popleft()
            for x in self.whole-h:
                k=self.closure(h|{x})
                if k not in known:known.add(k);todo.append(k)
        self.subgroups=known
    @functools.lru_cache(None)
    def closure(self,gens):
        got={self.one};todo=[self.one]
        for a in todo:
            for b in gens:
                c=self.mul[a][b]
                if c not in got:got.add(c);todo.append(c)
        return frozenset(got)
    def conj(self,h,g):return frozenset(self.mul[self.mul[self.inv[g]][x]][g] for x in h)
    def key(self,h):return tuple(sorted(h))
    def subkey(self,h,ambient):return min(self.key(self.conj(h,g)) for g in ambient)
    def maximal(self,h,k):return h<k and not any(h<l<k for l in self.subgroups)
    def cosets(self,h,k):return sorted({frozenset(self.mul[a][x] for a in h) for x in k},key=self.key)
    def familykey(self,fam,normalizer):
        return min(tuple(sorted(self.key(self.conj(h,g)) for h in fam)) for g in normalizer)
    def helly(self,pars,k):
        # Enumerate all pairwise incident flags, including proper partial flags.
        cos=[self.cosets(h,k) for h in pars]
        def visit(pos,chosen,meet):
            if pos==len(cos):return True
            if not visit(pos+1,chosen,meet):return False
            for c in cos[pos]:
                if all(c&d for d in chosen):
                    new=meet&c
                    if not new:return False
                    if not visit(pos+1,chosen+[c],new):return False
            return True
        return visit(0,[],k)
    def ip2(self,p,q,k):
        left=self.cosets(p,k);right=self.cosets(q,k)
        ns=[{j for j,b in enumerate(right) if a&b} for a in left]
        if all(len(n)==len(right) for n in ns):return True
        return all(len(a&b)<=1 for a,b in itertools.combinations(ns,2))
    def two(self,b,p):
        cos=self.cosets(b,p);idx={c:i for i,c in enumerate(cos)};todo=set(range(len(cos)));orbits=0
        while todo:
            i=min(todo);o={idx[frozenset(self.mul[x][g] for x in cos[i])] for g in b}
            assert o<=todo
            todo-=o;orbits+=1
        return orbits==2
    def valid(self,b,fam):
        subsets=list(powerset(range(len(fam))))
        joins={s:self.closure(frozenset().union(b,*(fam[i] for i in s))) for s in subsets}
        for s,t in itertools.combinations(subsets,2):
            if joins[s]&joins[t]!=joins[tuple(sorted(set(s)&set(t)))]:return False
        for s in subsets:
            if not s:continue
            if not any(self.maximal(joins[tuple(j for j in s if j!=i)],joins[s]) for i in s):return False
            if len(s)==2:
                if not self.ip2(fam[s[0]],fam[s[1]],joins[s]):return False
            if len(s)>=3:
                pars=[joins[tuple(j for j in s if j!=i)] for i in s]
                if not self.helly(pars,joins[s]):return False
        return True
def check_model(name,data):
    order,mul,reps,inc,rows=data;l=Literal(mul);assert l.n==order
    reps=list(map(frozenset,reps))
    assert len({l.subkey(h,l.whole) for h in reps})==len(reps)
    assert {l.subkey(h,l.whole) for h in reps}=={l.subkey(h,l.whole) for h in l.subgroups}
    inclusions=[tuple(map(frozenset,p)) for p in inc]
    assert all(k in reps and h in l.subgroups and l.maximal(h,k) for k,h in inclusions)
    for k in reps:
        want={l.subkey(h,k) for h in l.subgroups if l.maximal(h,k)}
        got=[l.subkey(h,k) for kk,h in inclusions if kk==k]
        assert len(got)==len(set(got)) and set(got)==want
    assert [frozenset(r[0]) for r in rows]==reps
    stats=collections.Counter();non2=[]
    for b0,panels0,levels,full in rows:
        b=frozenset(b0); panels=list(map(frozenset,panels0));normalizer=[g for g in l.whole if l.conj(b,g)==b]
        assert len(panels)==len(set(panels))
        assert set(panels)=={p for p in l.subgroups if l.maximal(b,p)}
        want=collections.defaultdict(set);wantfull=set()
        for fam in powerset(panels):
            if not fam:continue
            stats['literal_panel_subsets']+=1
            if not l.valid(b,fam):continue
            stats['literal_valid_families']+=1
            key=l.familykey(fam,normalizer);want[len(fam)].add(key)
            if l.closure(frozenset().union(b,*fam))==l.whole:
                wantfull.add(key)
                if any(not l.two(b,p) for p in fam):non2.append(dict(borel=sorted(b),rank=len(fam),panels=[sorted(p) for p in fam]))
        gotfull=[l.familykey(tuple(map(frozenset,fam)),normalizer) for fam in full]
        assert len(gotfull)==len(set(gotfull)) and set(gotfull)==wantfull,(name,'full',b)
        if not panels:assert levels==[]
        else:
            assert levels and levels[-1]==[]
            assert len(levels)>max(want,default=0)
        for rank,level in enumerate(levels,1):
            got=[]
            for indices in level:
                assert len(indices)==rank and len(set(indices))==rank
                assert all(0<=i<len(panels) for i in indices)
                got.append(l.familykey(tuple(panels[i] for i in indices),normalizer))
            assert len(got)==len(set(got)) and set(got)==want[rank],(name,b,rank,len(got),len(want[rank]))
            stats['inner_type_classes']+=len(got)
        stats['borels']+=1;stats['full_classes']+=len(wantfull)
    if name in ('C3','C3xC3'):assert non2
    return dict(name=name,order=order,all_subgroups=len(l.subgroups),counts=dict(stats),
                full_non_2T_literal_families=len(non2),non_2T_example=non2[:1])
def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=pathlib.Path,required=True)
    p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    b=a.input.read_bytes();models=json.loads(b);names=json.loads((a.input.parent/'fixtures.json').read_text())
    assert len(models)==len(names)==6
    reports=[check_model(n,m) for n,m in zip(names,models)]
    report=dict(status='PASS_LITERAL_ALL_FAMILY_COMPLETENESS_SMALL_MODELS',target_census=False,
                elapsed=time.monotonic()-start,input_sha256=hashlib.sha256(b).hexdigest(),models=reports)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
