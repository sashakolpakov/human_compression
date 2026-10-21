"""Literal C2 x C2 counterexample to the printed inverse-image step."""
import json

def need(value, message):
    if not value:
        raise ValueError(message)

G=frozenset(range(4))
lines=[frozenset((0,a)) for a in (1,2,3)]

def cosets(H):
    return sorted({frozenset(h ^ g for h in H) for g in G},key=lambda c:tuple(sorted(c)))

def incidence(H,K):
    left,right=cosets(H),cosets(K)
    edges=[(i,j) for i,c in enumerate(left) for j,d in enumerate(right) if c&d]
    return dict(vertices=len(left)+len(right),edges=len(edges),
                left_degrees=[sum(i==a for a,b in edges) for i in range(len(left))],
                right_degrees=[sum(j==b for a,b in edges) for j in range(len(right))])

def check():
    need(all(len(h)==2 and 0 in h and all(a^b in h for a in h for b in h) for h in lines),'three maximal subgroups')
    rows=[]
    for H in lines:
        omega=cosets(H)
        phi={g:tuple(omega.index(frozenset(x^g for x in c)) for c in omega) for g in G}
        kernel=frozenset(g for g,p in phi.items() if p==(0,1))
        need(kernel==H,'coset kernel')
        for K in lines:
            if K==H:continue
            image={phi[k] for k in K}
            orbit={phi[k][0] for k in K}
            preimage=frozenset(g for g,p in phi.items() if p in image)
            stabilizer=frozenset(g for g,p in phi.items() if p[0]==0)
            need(len(orbit)==2 and preimage==G and stabilizer==H,'printed counterexample')
            bad,good=incidence(preimage,stabilizer),incidence(K,stabilizer)
            need(bad==dict(vertices=3,edges=2,left_degrees=[2],right_degrees=[1,1]),'nonfirm printed graph')
            need(good==dict(vertices=4,edges=4,left_degrees=[2,2],right_degrees=[2,2]),'firm corrected graph')
            rows.append(dict(H=sorted(H),K=sorted(K),orbit_size=2,printed_first_subgroup=sorted(preimage),printed_graph=bad,corrected_graph=good))
    need(len(rows)==6,'all distinct ordered line pairs')
    return dict(status='PASS_ORDER_FOUR_ALGORITHM_COUNTEREXAMPLE',group_order=4,ordered_pairs=6,rows=rows,
                source_credit=0,general_proof='scope.tex; requires distinct review',new_Lean=0)

if __name__=='__main__':print(json.dumps(check(),indent=2))
