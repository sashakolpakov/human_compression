"""Optional small-field corroboration of the uniform signed-vector proof.
No group classification, map census or proof premise. Prime fields only.
"""
from pathlib import Path
import argparse,itertools,json
def need(x,m):
    if not x:raise ValueError(m)
def check(p):
    dot=lambda x,y:sum(a*b for a,b in zip(x,y))%p
    neg=lambda x:tuple(-a%p for a in x)
    canon=lambda x:min(x,neg(x))
    points=list(itertools.product(range(p),repeat=3))
    bynorm={a:[] for a in range(p)}
    for v in points:bynorm[dot(v,v)].append(v)
    cases=isotropic=0
    for B in points:
        x,y,z=B
        if 0 in B or dot(B,B)!=1:continue
        vi=(0,-z%p,y);vj=(z,0,-x%p);vk=(-y%p,x,0)
        need(all(dot(B,u)==0 for u in [vi,vj,vk]),'orthogonality')
        need(all(dot(u,v)!=0 for u,v in itertools.combinations([vi,vj,vk],2)),'nonzero pair dots')
        expected={canon(vj),canon((z,0,x))}
        avj=(z,0,x);c=dot(B,avj)
        expected.add(canon(tuple((2*c*b-a)%p for b,a in zip(B,avj))))
        need(len(expected)==3,'three forced signed vectors')
        actual={canon(v) for v in bynorm[dot(vj,vj)]
                if dot(v,vi) in {dot(vj,vi),-dot(vj,vi)%p}
                and dot(v,vk) in {dot(vj,vk),-dot(vj,vk)%p}}
        need(actual==expected,'all signed-vector solutions, no sampling')
        # The prescribed positive-positive branch has its unique solution vj.
        positive=[v for v in bynorm[dot(vj,vj)] if dot(v,vi)==dot(vj,vi) and dot(v,vk)==dot(vj,vk)]
        need(positive==[vj],'unique aligned branch')
        cases+=1;isotropic+=dot(vj,vj)==0
    return {'field':p,'norm_one_nonzero_coordinate_cases':cases,
            'isotropic_vertex_vector_cases':isotropic,'all_solution_sets_exactly_three':True}
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    rows=[check(p) for p in [3,5,7,11,13]]
    need(sum(x['isotropic_vertex_vector_cases'] for x in rows)>0,'isotropic boundary included')
    p=7;B=(1,3,2);vi=(0,5,3);vj=(2,0,6);vk=(4,1,0)
    dot=lambda x,y:sum(a*b for a,b in zip(x,y))%p
    need(dot(B,B)==0,'degenerate weakening fixture')
    bad=[v for v in itertools.product(range(p),repeat=3)
         if dot(v,v)==dot(vj,vj) and dot(v,vi)==dot(vj,vi) and dot(v,vk)==dot(vj,vk)]
    need(len(bad)==7,'norm-zero weakening destroys unique aligned branch')
    result={'status':'PASS_OPTIONAL_WRITTEN_PROOF_DIAGNOSTIC','rows':rows,
            'negative_control':{'omitting_nonzero_B_norm_gives_aligned_solutions':7,
                                'claimed_unique_solution_rejected':True},
            'finite_proof_premise':False}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
