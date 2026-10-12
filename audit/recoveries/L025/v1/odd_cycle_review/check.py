"""Distinct bounded review replay. No author arithmetic or graph code imported."""
from pathlib import Path
from collections import deque
from itertools import combinations
import argparse, copy, hashlib, json, math

HERE = Path(__file__).resolve().parent
AUTHOR_SHA = '483119cb4eba1d7044b3507a3c285e5acf40ac3c49eaf60108deb08dfa6dac4f'

def need(value, message):
    if not value:
        raise ValueError(message)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def graph(ell, paths):
    adj = [set() for _ in range(ell)]
    def edge(a,b):
        adj[a].add(b); adj[b].add(a)
    for a in range(ell):
        edge(a,(a+1)%ell)
    for start,end,length in paths:
        v=start
        for _ in range(length-1):
            u=len(adj); adj.append(set()); edge(v,u); v=u
        edge(v,end)
    return adj

def distances(adj, start, parity=False, banned=None):
    first=(start,0) if parity else start
    dist={first:0}; q=deque([first])
    while q:
        item=q.popleft(); v,p=item if parity else (item,0)
        for w in adj[v]:
            if banned is not None and frozenset((v,w))==banned:
                continue
            nxt=(w,1-p) if parity else w
            if nxt not in dist:
                dist[nxt]=dist[item]+1; q.append(nxt)
    return dist

def girths(adj):
    g=math.inf; odd=math.inf
    for v in range(len(adj)):
        odd=min(odd,distances(adj,v,True).get((v,1),math.inf))
        for w in adj[v]:
            if v<w:
                g=min(g,1+distances(adj,v,banned=frozenset((v,w))).get(w,math.inf))
    return g,odd

def local_oracle():
    # Actual small graphs, with shortest cycles found by independent BFS.
    path_cases=0; forks=0; clique_cases=0
    for ell in range(7,32,2):
        for length in (2,3,4):
            allowed=[]
            for d in range(1,ell):
                g,o=girths(graph(ell,[(0,d,length)])); path_cases+=1
                if g>=6 and o>=ell:
                    allowed.append(d)
            expected=set() if length==2 else ({3,ell-3} if length==3 else {2,4,ell-2,ell-4})
            need(set(allowed)==expected, 'external-path graph oracle')
        # C with x-a-z in its first shell: root positions -3,0,+3.
        a=graph(ell,[])
        a.extend([set(),set(),set()])
        for u,v in ((ell,ell-3),(ell+1,0),(ell+2,3),(ell,ell+1),(ell+1,ell+2)):
            a[u].add(v); a[v].add(u)
        need(girths(a)[1]==ell-2,'first-shell fork shorter odd cycle'); forks+=1
        # Every clique can be translated to contain zero; inspect actual root graph.
        neighbors={2,4,ell-2,ell-4}
        maxsize=1
        for n in range(1,5):
            for subset in combinations(neighbors,n):
                if all((x-y)%ell in neighbors for x,y in combinations(subset,2)):
                    maxsize=max(maxsize,n+1)
        need(maxsize==3,'second-shell root graph maximum clique'); clique_cases+=1
    arithmetic=0
    for ell in range(7,102,2):
        for k in range(2,129):
            need(ell*(k-1)+(ell*(k-2)**2+2)//3==(ell*(k*k-k+1)+2)//3,'ceiling identity')
            arithmetic+=1
    for q in range(3,257):
        lam=(q-1)**2*(q-2); d=(q-1)**3-lam
        need(d==(q-1)**2,'deficit')
        need(2*(q*q-q+1)+(2*d+q-1)//q==2*q*q-1,'general substitution')
        need(2*(q*q-q+1)+2*((d+q-1)//q)==2*q*q,'bipartite substitution')
        need(7*(q*q-q+1)-3*(2*q*q-1)==(q-5)*(q-2),'exclusion identity')
    need((7*57+2)//3==133 and (7*13+2)//3==31,'q8 and q4 boundary')
    return dict(actual_external_path_graphs=path_cases, actual_shell_forks=forks,
                rooted_clique_graphs=clique_cases, ceiling_pairs=arithmetic,
                biaffine_substitutions=254, mathematical_premise=False)

def validate_scope(r):
    need(r['decision']=='ACCEPTED_BOUNDED_WRITTEN_PROOF','decision')
    need(r['author_manifest_sha256']==AUTHOR_SHA,'author pin')
    need(r['whole_L025_accepted'] is False,'whole-source boundary')
    need(r['source_theorem_disproved'] is False,'proof gap is not theorem disproof')
    need(r['uniform_shell']['assumptions']==['finite','simple','regular','nonbipartite','girth_at_least_6'],'assumptions')
    need(r['uniform_shell']['ell_min']==7,'odd-girth endpoint')
    need(r['uniform_shell']['required_new_finite_programs']==[],'uniform written proof')
    need(r['q4']['role']=='retained_external_finite_completeness_premise','q4 trust')
    need(r['q4']['lower_bound']==32 and r['q4']['reexecuted'] is False,'q4 exact retained result')
    need(r['biaffine']['girth_six_range']=='prime_power_q_ge_3','q2 excluded from girth six')
    need(r['biaffine']['parent_interfaces_reviewed_here'] is False,'parent review separate')
    need(r['new_original_credit']==r['new_question_credit']==r['new_formal_declarations']==0,'no credit')
    need(r['software_inclusive_factor'] is None,'no factor')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--author',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True); ap.add_argument('--study-root',type=Path)
    a=ap.parse_args(); need(not a.out.exists(),'fresh report required')
    own=HERE/'manifest.json'
    if own.exists():
        for row in json.loads(own.read_text())['exports']:
            p=HERE/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'review export '+row['path'])
    mf=a.author/'manifest.json'; need(sha(mf)==AUTHOR_SHA,'immutable author manifest')
    m=json.loads(mf.read_text())
    for row in m['exports']:
        p=a.author/row['path']; need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'export '+row['path'])
    sources=json.loads((a.author/'dependencies.json').read_text())['private_primary_sources']
    if a.study_root:
        for row in sources:
            p=a.study_root/row['path']; need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'primary '+row['id'])
    r=json.loads((HERE/'review.json').read_text()); validate_scope(r)
    mutations=[('whole_source',('whole_L025_accepted',),True),('false_theorem',('source_theorem_disproved',),True),
        ('ell5',('uniform_shell','ell_min'),5),('drop_simple',('uniform_shell','assumptions'),['finite','regular','nonbipartite','girth_at_least_6']),
        ('finite_proof',('uniform_shell','required_new_finite_programs'),['oracle.py']),('q4_optional',('q4','role'),'optional'),
        ('q4_31',('q4','lower_bound'),31),('census_rerun',('q4','reexecuted'),True),
        ('q2_girth6',('biaffine','girth_six_range'),'prime_power_q_ge_2'),('parent_accepted',('biaffine','parent_interfaces_reviewed_here'),True),
        ('credit',('new_original_credit',),1),('software_factor',('software_inclusive_factor',),1)]
    rejected=[]
    for name,route,value in mutations:
        b=copy.deepcopy(r); d=b
        for key in route[:-1]:d=d[key]
        d[route[-1]]=value
        try:validate_scope(b)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted mutation '+name)
    # The cycle-square cap is false for ell=5; the q4 inequality does not exclude31.
    need(all((x-y)%5 in {1,2,3,4} for x,y in combinations(range(5),2)),'ell5 negative model')
    need((4-5)*(4-2)<=0,'q4 negative margin')
    report=dict(status='PASS_DISTINCT_BOUNDED_REVIEW',author_exports=len(m['exports']),
        source_bindings=len(sources) if a.study_root else 0,independent_oracle=local_oracle(),
        rejected_scope_controls=rejected,negative_boundary_controls=['ell5_clique5','q4_not_excluded'],
        imported_author_mathematics=False,source_census_reexecuted=False,
        whole_L025_accepted=False)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
