import sys
if sys.flags.optimize: raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import ast,copy,json
from collections import Counter,deque
from pathlib import Path

def need(ok,msg):
    if not ok: raise ValueError(msg)
def mul(p,q): return tuple(q[x-1] for x in p)
def closure(gens,n=21):
    one=tuple(range(1,n+1));seen={one};todo=[one]
    for a in todo:
        for g in gens:
            b=mul(a,g)
            if b not in seen: seen.add(b);todo.append(b)
    return frozenset(seen)
def cosets(group,sub):
    rest=set(group);lookup={};reps=[]
    while rest:
        g=min(rest);i=len(reps);reps.append(g)
        row={mul(h,g) for h in sub}
        need(row<=rest,'literal disjoint cosets')
        for x in row: lookup[x]=i
        rest-=row
    return lookup,reps
def orbit(start,gens):
    seen={start};todo=[start]
    for a in todo:
        for g in gens:
            b=g(a)
            if b not in seen:seen.add(b);todo.append(b)
    return seen

def validate(data,source_rows):
    gg,records,classes,witnesses=data
    gg=[tuple(x) for x in gg];G=closure(gg);one=tuple(range(1,22))
    need(len(G)==20160 and len(records)==60,'ambient order and saved candidate count')
    groups={};coset_cache={};actual=[];neighbourpairs=0;transitivity=[]
    def group(gs):
        key=tuple(tuple(x) for x in gs)
        if key not in groups:groups[key]=closure(key)
        return groups[key]
    for r in records:
        A,B,H=map(group,r[:3]);need(A<=G and B<=G and H==A&B,'actual subgroup intersection')
        need([len(A),len(B),len(H)]==r[3],'actual subgroup orders')
        degrees=[len(A)//len(H),len(B)//len(H)]
        need(degrees==r[4] and min(degrees)>1,'firm local degrees')
        need(closure([tuple(x) for x in r[0]+r[1]])==G,'literal connectivity')
        twos=[]
        for K,kg in [(A,r[0]),(B,r[1])]:
            cm,reps=cosets(K,H);base=cm[one]
            action=lambda g:(lambda i:cm[mul(reps[i],g)])
            hg=[tuple(x) for x in r[2]]
            # A finite transitive action is primitive iff the orbit of a point
            # stabilizer on each nontrivial block candidate generates all points.
            # This equivalent literal closure tests every possible second point.
            n=len(reps);perms=[tuple(cm[mul(a,tuple(g))] for a in reps) for g in kg]
            for second in range(n):
                if second==base:continue
                part=list(range(n))
                def root(i):
                    while part[i]!=i:i=part[i]
                    return i
                def unite(a,b):
                    a,b=root(a),root(b)
                    if a!=b:part[b]=a;return True
                    return False
                unite(base,second);changed=True
                while changed:
                    changed=False
                    blocks={}
                    for i in range(n):blocks.setdefault(root(i),[]).append(i)
                    for block in blocks.values():
                        for p in perms:
                            for j in block[1:]:changed=unite(p[block[0]],p[j]) or changed
                need(len({root(i) for i in range(n)})==1,'primitive local block closure')
            twos.append(int(orbit(next(i for i in range(n) if i!=base),[action(g) for g in hg])==set(range(n))-{base}))
        need(twos==r[8],'literal local two-transitivity')
        if A not in coset_cache:coset_cache[A]=cosets(G,A)
        cm,_=coset_cache[A];_,ar=cosets(A,H)
        neigh=[{cm[mul(b,a)] for b in B} for a in ar]
        base=ar.index(one);counts=[len(neigh[base]&N) for i,N in enumerate(neigh) if i!=base]
        need(sorted(counts)==sorted(r[5]),'actual common-neighbour multiset')
        allcounts=[len(neigh[i]&neigh[j]) for i in range(len(neigh)) for j in range(i+1,len(neigh))]
        neighbourpairs+=len(allcounts)
        digon=len(B)//len(H)==len(G)//len(A);ip=digon or all(x==1 for x in allcounts)
        need([int(digon),int(ip)]==r[6:8],'literal complete-bipartite/IP2 classification')
        actual.append((A,B,H));transitivity.append(twos)
    surviving=[i+1 for i,r in enumerate(records) if r[7]]
    need(len(surviving)==31 and sorted(sum(classes,[]))==surviving,'exact survivor partition')
    need(len(classes)==7 and len({tuple(sorted(records[c[0]-1][3][:2])) for c in classes})==7,'seven distinct unordered type sizes')
    required=sorted((i,c[0]) for c in classes for i in c[1:])
    need(sorted((w[0],w[1]) for w in witnesses)==required and len(witnesses)==24,'complete exact witness coverage')
    maps={}
    for source,target,swap,images in witnesses:
        key=tuple(tuple(x) for x in images)
        if key not in maps:
            phi={one:one};todo=[one]
            for a in todo:
                for g,h in zip(gg,key):
                    b,y=mul(a,g),mul(phi[a],h)
                    if b in phi:need(phi[b]==y,'literal automorphism relation')
                    else:phi[b]=y;todo.append(b)
            need(set(phi)==G and set(phi.values())==G,'literal automorphism bijection');maps[key]=phi
        phi=maps[key];p=actual[source-1][:2];q=actual[target-1][:2]
        need(sorted(swap)==[1,2],'literal type permutation')
        need(all(frozenset(phi[x] for x in p[i])==q[swap[i]-1] for i in range(2)),'simultaneous actual subgroup images')
    profile=sorted((tuple(records[c[0]-1][3]),tuple(records[c[0]-1][4]),tuple(len(G)//x for x in records[c[0]-1][3][:2])) for c in classes)
    expected=sorted((tuple(x['parabolic_orders']+[x['intersection']]),tuple(x['local_degrees']),tuple(x['type_sizes'])) for x in source_rows)
    need(profile==expected,'source seven-row orders/degrees/type sizes')
    need(all(all(transitivity[i-1]) for i in surviving),'all survivors local2T')
    return {'candidate_pairs':len(records),'survivors':len(surviving),'classes':len(classes),'neighbour_pairs':neighbourpairs,'witnesses':len(witnesses),'distinct_literal_automorphisms':len(maps),'group_order':len(G),'local_primitivity_checks':120}

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--data',type=Path,required=True);ap.add_argument('--rows',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh report')
    txt=a.data.read_text();need('PASS_LITERAL_EXPORT' in txt,'clean export marker')
    data=ast.literal_eval(txt.split('LITERAL_DATA ',1)[1].split('PASS_LITERAL_EXPORT',1)[0].strip())
    report=validate(data,json.loads(a.rows.read_text())['rows'])
    report.update(status='PASS_INDEPENDENT_LITERAL_L100_CANDIDATE_CHECKS',new_subgroup_enumerations=0)
    a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
