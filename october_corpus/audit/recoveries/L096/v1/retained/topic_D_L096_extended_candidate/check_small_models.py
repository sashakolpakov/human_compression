#!/usr/bin/env python3
"""Direct incidence/eligible-flag oracle; no orbit or subgroup algorithm import."""
import argparse,itertools,json
from pathlib import Path

def direct(types,inc):
    type_ids=sorted(set(types));parts=[[v for v,t in enumerate(types) if t==i] for i in type_ids]
    flags=[]
    for choices in itertools.product(*[[None]+p for p in parts]):
        f=tuple(v for v in choices if v is not None)
        if all(inc[u][v] for u,v in itertools.combinations(f,2)):flags.append(f)
    shadows=[{f:frozenset(v for v in p if all(inc[v][u] for u in f)) for f in flags} for p in parts]
    results=[];tests=0;failures=[]
    for ti,p in enumerate(parts):
        byshadow={}
        for f,s in shadows[ti].items():byshadow.setdefault(s,[]).append(f)
        good=True
        for x in range(len(types)):
            for f in flags:
                tests+=1;s=shadows[ti][(x,)]&shadows[ti][f]
                if not s:continue
                if not any(all(inc[v][u] for v in c for u in (x,)+f) for c in byshadow.get(s,[])):
                    good=False;failures.append({'type':ti+1,'x':x,'flag':f,'intersection':sorted(s)});break
            if not good:break
        results.append(good)
    return {'type_results':results,'flags':len(flags),'tests':tests,'negative_witnesses':failures}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--log',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    raw=Path(a.log).read_text().replace('\\\n','');models=[json.loads(x[6:]) for x in raw.splitlines() if x.startswith('MODEL|')]
    if len(models)!=6 or 'RANK_TWO_COMPARISONS|105' not in raw or 'PASS_SMALL_MODEL_EXPORT' not in raw:raise ValueError('incomplete model receipt')
    checks=[]
    for m in models:
        inc=m['incidence'];d=direct(inc['types'],inc['incidence']);r=m['local_result']
        if r['flag_transitive'] and d['type_results']!=r['type_results']:raise ValueError((m['name'],d,r))
        checks.append({'name':m['name'],'direct':d,'flag_transitive':r['flag_transitive'],'orbit_truth_agrees':r['flag_transitive']})
    # The earlier accepted closure counterexample is reproduced literally.
    types=[1]*4+[2]*2+[3]*2;mat=[[i==j for j in range(8)] for i in range(8)]
    for i in [4,5]:
        for j in [6,7]:mat[i][j]=mat[j][i]=True
    for v,ns in [(4,[0,1,2]),(5,[0,1,3]),(6,[0,1,2]),(7,[0,1,3])]:
        for u in ns:mat[v][u]=mat[u][v]=True
    d=direct(types,mat)
    if d['type_results'][0]:raise ValueError('lost witness flag compatibility')
    # Nonempty proper two-point intersections reject the cubic bipartite graph;
    # the identity double coset must not incorrectly reject the square.
    lookup={x['name']:x['direct']['type_results'] for x in checks}
    if lookup['cube_bipartite_graph']!=[False,False] or lookup['square']!=[True,True]:raise ValueError('rank-two distinction')
    if next(x for x in checks if x['name']=='non_flag_transitive_triangle')['flag_transitive']:raise ValueError('missing flag recognition')
    out={'status':'PASS','method':'literal incidence enumeration of every flag and eligible witness; no subgroup-orbit implementation imported','models':checks,'closure_counterexample':d,'rank_two_shortcut_vs_full_search_base_residues':105,'controls':['non_flag_transitive_coset_system','closure_without_flag_counterexample','noncomplete_fourcycle_rejected','identity_pair_not_treated_as_distinct'],'scope':'small diagnostic validation, not a second independent catalogue review'}
    Path(a.out).write_text(json.dumps(out,indent=2)+'\n');print('PASS',sum(x['direct']['tests'] for x in checks),'direct tests')
if __name__=='__main__':main()
