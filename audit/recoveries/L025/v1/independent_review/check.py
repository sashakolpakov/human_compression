"""Independent L025 finite and scope review. No author mathematical imports."""
from pathlib import Path
from collections import Counter, deque
from itertools import combinations
import argparse,copy,hashlib,json,re

HERE=Path(__file__).resolve().parent
PIN='6d1c8b7cf3465831a8ec9d5c14cb858123f97e6f4d86a14bb5fe0883c616627c'
def need(v,m):
    if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def simple(A):
    n=len(A);need(n>0,'nonempty')
    need(all(isinstance(v,int) and 0<=v<n and v!=u and u in A[v] for u in range(n) for v in A[u]),'simple symmetric')
def distances(A,v,banned=None):
    D={v:0};Q=deque([v])
    while Q:
        x=Q.popleft()
        for y in A[x]:
            if banned is not None and {x,y}==banned:continue
            if y not in D:D[y]=D[x]+1;Q.append(y)
    return D
def profile(A):
    simple(A);D=[distances(A,i) for i in range(len(A))]
    g=min((distances(A,u,{u,v}).get(v,10**9)+1 for u in range(len(A)) for v in A[u] if u<v),default=10**9)
    return dict(order=len(A),degree=sorted(set(map(len,A))),connected=all(len(d)==len(A) for d in D),
                girth=None if g>=10**9 else g,diameter=max(max(d.values()) for d in D)),D
def edge_counts(A,g):
    # One direction is fixed separately on each edge. No least-vertex algorithm.
    out=[]
    for u in range(len(A)):
        for v in sorted(A[u]):
            if u>=v:continue
            def walk(x,used,left):
                if left==1:return int(u in A[x])
                return sum(walk(y,used|{y},left-1) for y in A[x] if y not in used)
            out.append((u,v,walk(v,{u,v},g-1)))
    return out
def full_aut(A,D):
    # Backtracking all distance-preserving bijections; literal adjacency at leaves.
    n=len(A);m={};used=set();nodes=0
    def walk():
        nonlocal nodes
        nodes+=1
        if len(m)==n:
            need(all({m[y] for y in A[x]}==A[m[x]] for x in range(n)),'literal leaf')
            return 1
        choices=[]
        for x in range(n):
            if x in m:continue
            C=[y for y in range(n) if y not in used and len(A[x])==len(A[y]) and all(D[x][z]==D[y][m[z]] for z in m)]
            if not C:return 0
            choices.append((len(C),x,C))
        _,x,C=min(choices);total=0
        for y in C:m[x]=y;used.add(y);total+=walk();used.remove(y);del m[x]
        return total
    return dict(order=walk(),nodes=nodes)
def field(q):
    if q in (2,3,5):return lambda a,b:(a+b)%q,lambda a,b:a*b%q
    poly={4:7,8:11}[q]
    def mul(a,b):
        out=0
        while b:
            if b&1:out^=a
            b>>=1;a<<=1
            if a&q:a^=poly
        return out
    return lambda a,b:a^b,mul
def biaffine(q,matching=False):
    add,mul=field(q);A=[set() for _ in range(2*q*q)]
    def edge(u,v):A[u].add(v);A[v].add(u)
    for x in range(q):
        for y in range(q):
            for m in range(q):
                for b in range(q):
                    if y==add(mul(m,x),b):edge(q*x+y,q*q+q*m+b)
    if matching:
        for x in range(q):
            for y in range(q):edge(q*x+y,q*x+(y^1));edge(q*q+q*x+y,q*q+q*x+(y^2))
    return A
def source_positive_only(A,g):
    # Literal source loop condition is <=g-1 (Magma `le`), not `ne`.
    P=[[u,v] for u in range(len(A)) for v in A[u] if u<v]
    while P and len(P[0])<=g-1:
        P=[p+[v] for p in P for v in A[p[-1]] if v not in p and (len(p)<g-1 or v in A[p[0]])]
    C=Counter()
    for p in P:
        p=p+[p[0]]
        for i in range(g):C[tuple(sorted((p[i],p[i+1])))]+=1
    return sorted(set(v//g for v in C.values())),len(C)
def group_check(A,data):
    n=len(A);identity=tuple(range(n));gens=[tuple(g) for g in data['automorphism_generators']]
    def comp(g,h):return tuple(h[g[x]] for x in range(n))
    def valid(g):return sorted(g)==list(range(n)) and all({g[v] for v in A[u]}==A[g[u]] for u in range(n))
    need(all(valid(g) for g in gens),'G generators')
    Q=[identity];G={identity}
    for g in Q:
        for h in gens:
            x=comp(g,h)
            if x not in G:G.add(x);Q.append(x)
    E={g for g in G if comp(g,g)==identity};need(len(G)==48 and len(E)==16,'E16 order')
    need(all(comp(a,b)==comp(b,a) and comp(a,b) in E for a in E for b in E),'elementary abelian')
    c=tuple(data['complement_generator']);cc=comp(c,c)
    need(c in G and c!=identity and comp(cc,c)==identity,'C3')
    need({comp(comp(c,e),cc) for e in E}==E,'normal E')
    need(E|{comp(e,c) for e in E}|{comp(e,cc) for e in E}==G,'whole semidirect')
    need(sum(comp(e,c)==comp(c,e) for e in E)==4,'action fixed space')
    return dict(order=48,elementary_abelian_kernel=16,complement=3,fixed_elements=4)
def scope(r):
    need(r['decision']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY','decision')
    need(r['author_manifest_sha256']==PIN,'pin')
    need(r['external_completeness']==['four_30_vertex_5_5_cages','F012_degree4_lower32'],'external premises')
    need(r['required_programs']==['finite/verify.py','finite/direct_graphs.py'],'required programs')
    need(r['whole_written_pages']==[7,5,3],'whole prose')
    need(r['finite_isomorphism_identity']=='H_and_G_distinct','graph distinction')
    need(r['new_original_registration']==r['new_question_credit']==r['new_Lean_declarations']==0,'credit boundary')
    need(r['source_executable_listing_pages']==[7,15],'source software boundary')
    need(r['full_source_formalized'] is False and r['external_censuses_rerun'] is False,'trust boundary')
    need(r['numerical_factor'] is None,'unmeasured')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--study-root',type=Path);a=ap.parse_args();need(not a.out.exists(),'fresh output')
    if (HERE/'manifest.json').exists():
        for r in json.loads((HERE/'manifest.json').read_text())['exports']:
            p=HERE/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'own binding')
    need(sha(a.author/'manifest.json')==PIN,'author manifest')
    M=json.loads((a.author/'manifest.json').read_text())
    for r in M['exports']:
        p=a.author/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'author binding '+r['path'])
    r=json.loads((HERE/'review.json').read_text());scope(r)
    source=json.loads((a.author/'source_map.json').read_text());need(len(source['rows'])==len({r['id'] for r in source['rows']})==41,'source41')
    need(source['rows']==json.loads((HERE/'source_dispositions.json').read_text()),'reviewed exact dispositions')
    graphs=[('H',biaffine(4,True)),('G',[set(v) for v in json.loads((a.author/'finite/inputs/source_G.json').read_text())])]
    for i in range(4):
        lines=(a.author/f'finite/inputs/cage-k5.g5-0{i}.dr').read_text().splitlines()
        need(lines[0]=='n30','cage format');graphs.append((f'cage{i}',[set(map(int,re.findall(r'\d+',x))) for x in lines[1:]]))
    expected=[(1920,{12:80}),(48,{12:80}),(120,{12:45,14:30}),(20,{12:50,13:20,14:5}),(30,{12:60,14:15}),(96,{12:24,13:48,16:3})]
    rows=[]
    for (name,A),(order,hist) in zip(graphs,expected):
        pr,D=profile(A);need(pr['degree']==[5] and pr['girth']==5 and pr['connected'],'six profiles')
        C=edge_counts(A,5);need(dict(Counter(x[2] for x in C))==hist,'all edge counts')
        au=full_aut(A,D);need(au['order']==order,'distinct full aut order')
        rows.append(dict(name=name,profile=pr,edges=len(C),cycle_histogram=hist,automorphisms=au))
    gp=group_check(graphs[1][1],json.loads((a.author/'finite/inputs/G_group.json').read_text()))
    models=[]
    for q in (2,3,4,5):
        A=biaffine(q);pr,_=profile(A);g=8 if q==2 else 6;lam=1 if q==2 else (q-1)**2*(q-2)
        need(pr['girth']==g and pr['degree']==[q],'biaffine profile')
        need({x[2] for x in edge_counts(A,g)}=={lam},'biaffine all edges');models.append([q,len(A),g,lam])
    A=biaffine(8,True);pr,_=profile(A);need(pr['girth']==5,'uniform matching model')
    C=edge_counts(A,5);need(all(c==(56 if (u<64)==(v<64) else 28) for u,v,c in C),'q8 matching counts')
    add,mul=field(4);H=graphs[0][1]
    def map_ok(m):return sorted(m)==list(range(32)) and all({m[v] for v in H[u]}==H[m[u]] for u in range(32))
    corrected=[16+4*mul(x,x)+mul(2,mul(y,y)) for x in range(4) for y in range(4)]
    corrected += [4*mul(2,mul(x,x))+mul(2,mul(y,y)) for x in range(4) for y in range(4)]
    printed=[16+4*x+mul(2,y) for x in range(4) for y in range(4)]
    printed += [4*mul(2,x)+mul(2,y) for x in range(4) for y in range(4)]
    need(map_ok(corrected) and not map_ok(printed),'semilinear repair positive/negative')
    need({c for _,_,c in C}=={28,56},'q8 is not edge-girth-regular after matching')
    K=[set(range(4))-{i} for i in range(4)]+[{4+(i^b) for b in (1,2,4)} for i in range(8)]
    need(dict(Counter(x[2] for x in edge_counts(K,3)))=={2:6,0:12},'counterexample all edges')
    need(source_positive_only(K,3)==([2],6),'literal le loop and positive-only false acceptance')
    need(source_positive_only(graphs[1][1],5)==([12],80),'literal routine positive graph')
    controls=[]
    for key,val in [('external_completeness',[]),('required_programs',[]),('whole_written_pages',[7]),('finite_isomorphism_identity','H_equals_G'),
                    ('new_original_registration',1),('new_question_credit',1),('new_Lean_declarations',1),('source_executable_listing_pages',[]),
                    ('full_source_formalized',True),('external_censuses_rerun',True),('numerical_factor',1)]:
        bad=copy.deepcopy(r);bad[key]=val
        try:scope(bad)
        except ValueError:controls.append(key)
        else:raise ValueError('missed control '+key)
    malformed=0
    for A in ([{0}],[{1},set()],[{2},set()]):
        try:simple(A)
        except (ValueError,IndexError):malformed+=1
    need(malformed==3,'malformed controls')
    checked_sources=0
    if a.study_root:
        for b in json.loads((a.author/'dependencies.json').read_text())['private_primary_sources']:
            p=a.study_root/b['path'];need(p.stat().st_size==b['bytes'] and sha(p)==b['sha256'],'source binding');checked_sources+=1
        t=(a.study_root/'sources/catalogue_L025.txt').read_text();need('while #c2 ne 0 and #Rep(c2) le g-1 do' in t,'literal le')
        part=t.split('gr:=Graph<32|')[1].split(']>;')[0]
        literal=[set(int(x)-1 for x in re.findall(r'\d+',v)) for v in re.findall(r'\{([^}]+)\}',part)]
        need(literal==graphs[1][1],'source exact adjacency')
    result=dict(status='PASS_DISTINCT_COMPLETE_PRINCIPAL_REVIEW',author_exports=len(M['exports']),source_dispositions=41,
        private_sources_checked=checked_sources,six_graphs=rows,G_structure=gp,biaffine_models=models,
        q8_matching_edges=len(C),literal_source_algorithm_semantics_checked=True,
        rejected_scope_controls=controls,malformed_controls=3,
        actual_mathematical_negative_controls=['unsquared_duality','q8_matching_not_egr','positive_only_source_counter'],
        mathematical_author_imports=False,
        external_censuses_rerun=False,Lean_rerun=False,new_original_registration=0)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
