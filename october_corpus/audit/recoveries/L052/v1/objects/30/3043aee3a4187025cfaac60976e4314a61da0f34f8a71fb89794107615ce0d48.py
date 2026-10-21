"""Independent finite permutation, subgroup and incidence verification."""
import sys
if sys.flags.optimize: raise RuntimeError('unoptimized execution required')
import argparse,json,itertools
from pathlib import Path

def need(ok,msg):
    if not ok:raise ValueError(msg)
def perm(a):
    need(isinstance(a,list) and 0<len(a)<=255 and all(type(i)is int for i in a) and sorted(a)==list(range(1,len(a)+1)),'literal permutation')
    return bytes(i-1 for i in a)
def ident(n):return bytes(range(n))
def mul(a,b):return a.translate(b+bytes(range(len(b),256)))
def inv(a):
    r=bytearray(len(a))
    for i,j in enumerate(a):r[j]=i
    return bytes(r)
def power(a,n):
    if n<0:return power(inv(a),-n)
    r=ident(len(a))
    for _ in range(n):r=mul(r,a)
    return r
def closure(gs,n):
    todo=[ident(n)];seen=set(todo);tables=[g+bytes(range(n,256))for g in gs]
    for g in todo:
        for t in tables:
            h=g.translate(t)
            if h not in seen:seen.add(h);todo.append(h)
    return frozenset(seen)
def subgroups(mark,rotation):
    n=len(mark[0]);rank=len(mark)
    out=[]
    for mask in range(1<<rank):
        inds=[i for i in range(rank)if mask>>i&1]
        gs=[mul(inv(mark[i]),mark[j])for i,j in itertools.combinations(inds,2)]if rotation else[mark[i]for i in inds]
        out.append(closure(gs,n))
    return out
def ip(ss):
    for i,s in enumerate(ss):
        for j,t in enumerate(ss):need(s&t==ss[i&j],'full subgroup intersection')

def geometry(group,pars):
    n=len(next(iter(group)));types=[]
    for H in pars:
        unseen=set(group);cosets=[]
        while unseen:
            g=ident(n)if ident(n)in unseen else min(unseen)
            coset=frozenset(mul(h,g)for h in H);need(coset<=unseen,'coset partition');unseen-=coset;cosets.append(coset)
        types.append(cosets)
    vertices=[(i,j)for i,C in enumerate(types)for j in range(len(C))];adj={v:set()for v in vertices}
    for (i,j),(k,l)in itertools.combinations(vertices,2):
        if i!=k and types[i][j]&types[k][l]:adj[(i,j)].add((k,l));adj[(k,l)].add((i,j))
    flags=[()]
    for v in vertices:flags +=[f+(v,)for f in tuple(flags)if all(x[0]<v[0]and v in adj[x]for x in f)]
    rank=len(pars);panels={};disconnected=[];short=[]
    for f in flags:
        V=set(v for v in vertices if all(v in adj[x]for x in f))
        if len(f)<rank and not V:short.append(f)
        if len(f)==rank-1:panels[len(V)]=panels.get(len(V),0)+1
        if len(f)<=rank-2:
            left=set(V);sizes=[]
            while left:
                todo=[left.pop()]
                for x in todo:
                    add=left&adj[x];left-=add;todo+=sorted(add)
                sizes.append(len(todo))
            if len(sizes)>1:disconnected.append(sorted(sizes))
    return {'type_counts':list(map(len,types)),'edges':sum(map(len,adj.values()))//2,'flags':[sum(len(f)==i for f in flags)for i in range(rank+1)],'short_maximal':len(short),'panels':panels,'disconnected':len(disconnected),'component_sizes':sorted(set(map(tuple,disconnected)))},adj,types

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    data=json.loads(a.input.read_text());rows=data['tables'];need([x['id']for x in rows]==['T1.'+str(i)for i in range(1,13)]+['T2.'+str(i)for i in range(1,12)],'exact table roster')
    result=[];totalpairs=0
    for row in rows:
        x,y,z=map(perm,row['rotation']);n=len(x);need(len(y)==n and len(z)==n,'equal permutation degree');e=ident(n);p=row['p'];aa=row['a'];bb=row['b']
        if row['id'].startswith('T2'):
            rels=[power(x,3),power(y,3),power(z,p),power(mul(inv(x),z),2),power(mul(inv(y),z),2),power(mul(inv(x),y),3),mul(power(mul(mul(x,inv(y)),x),aa),power(mul(x,y),bb))]
        else:
            u=x;v=mul(inv(x),y);w=mul(inv(y),z)
            rels=[power(u,6),power(v,3),power(w,p),power(mul(u,v),2),power(mul(v,w),2),power(mul(mul(u,v),w),2),mul(power(mul(v,power(u,-2)),aa),power(mul(inv(v),power(u,2)),bb))]
        need(all(r==e for r in rels),'literal presentation relators')
        ss=subgroups([e,x,y,z],True);ip(ss);totalpairs+=256
        need(len(ss[-1])==row['rotation_order'],'literal full rotation order');need(list(map(len,ss))==row['icplus_orders'],'all literal subgroup orders')
        entry={'id':row['id'],'rotation_order':len(ss[-1]),'subset_pairs':256}
        if row['id'].startswith('T1.'):
            pars=[ss[m]for m in [14,13,11,7]];checks=[]
            for i,j,k in itertools.combinations(range(4),3):
                product={mul(h,t)for h in pars[i]for t in pars[k]}
                need(pars[j]<=product,'ordered incidence transitivity')
                checks.append([i,j,k,len(pars[j]),len(product)])
            entry['poset_tests']=checks
        result.append(entry)
    examples=[]
    for row in data['examples']:
        rr=list(map(perm,row['generators']));rank=len(rr);ss=subgroups(rr,False);ip(ss);totalpairs+=(1<<rank)**2
        need(len(ss[-1])==row['order'],'example full order')
        ex={'id':row['id'],'order':len(ss[-1]),'ip':list(map(len,ss))}
        if rank==3 or row['id']=='4.5':
            info,adj,types=geometry(ss[-1],[ss[((1<<rank)-1)^(1<<i)]for i in range(rank)])
            expect={'4.4':([3,3,3],27,[1,9,27,27],{3:27},0),'4.5':([15,6,6,15],381,[1,42,381,1080,720],{2:720,4:360},36)}[row['id']]
            need((info['type_counts'],info['edges'],info['flags'],info['panels'],info['disconnected'])==expect,'complete actual incidence invariant');need(info['short_maximal']==0,'all flags extend')
            if row['id']=='4.5':
                for flag,vertices,degree in [([(0,0),(3,0)],8,4),([(1,0),(2,0)],20,2)]:
                    V=set.intersection(*(adj[v]for v in flag));need(len(V)==vertices and all(len(adj[v]&V)==degree for v in V),'specified base residue')
            ex['incidence']=info
        else:
            rot=[ident(len(rr[0]))]+[mul(rr[0],r)for r in rr[1:]];tt=subgroups(rot,True)
            need(tt[-1]==ss[-1],'rotation is whole group');need(len(tt[7]&tt[14])==8 and len(tt[6])==4 and rr[1]in(tt[7]&tt[14])-tt[6],'literal IC+ witness')
            ex['ICplus_failure']=[8,4]
        examples.append(ex)
    report={'status':'PASS_LITERAL_TABLES_AND_EXAMPLES','tables':result,'examples':examples,'subset_pairs':totalpairs}
    a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'table_rows':len(rows),'examples':len(examples),'subset_pairs':totalpairs}))
if __name__=='__main__':main()
