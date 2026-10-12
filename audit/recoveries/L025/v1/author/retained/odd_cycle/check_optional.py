"""Optional small arithmetic checks; no finite premise for the written bound."""
from itertools import combinations
import json

def need(t,s):
 if not t:raise ValueError(s)
rows=[]
for ell in range(7,66,2):
 allowed=lambda x,y:(x-y)%ell in {2,4,ell-2,ell-4}
 inv=pow(2,-1,ell)
 need(all(allowed(i,j)==((inv*(i-j))%ell in {1,2,ell-1,ell-2}) for i in range(ell) for j in range(i)),'cycle-square relabeling')
 candidates=[0,2,4,ell-2,ell-4]
 cliques=[c for r in range(1,6) for c in combinations(candidates,r) if 0 in c and all(allowed(i,j) for i,j in combinations(c,2))]
 need(max(map(len,cliques))==3,'exact clique cap')
 rows.append(dict(ell=ell,rooted_clique_number=3))
for q in [8,16,32,64,128,256,512,1024]:need(7*(q*q-q+1)-3*(2*q*q-1)==(q-5)*(q-2)>0,'exact margin')
need(7*57//3==133 and (7*13+2)//3==31,'q8 excluded and q4 retained')
need(42*6==252 and 78*3==234 and 252>234,'q8 shell contradiction')
# Deliberate weakenings fail: odd cycle length five and clique cap two.
need(all((i-j)%5 in {1,2,3,4} for i,j in combinations(range(5),2)),'ell5 clique five control')
need(all((i-j)%7 in {2,3,4,5} for i,j in combinations([0,2,4],2)),'clique cap two control')
need((4-5)*(4-2)<0,'q4 not covered by uniform margin')
print(json.dumps(dict(status='PASS_OPTIONAL_DIAGNOSTIC',odd_cycle_cases=rows,integer_only=True,controls=['ell5 excluded','clique cap2 rejected','q4 uniform exclusion rejected'],mathematical_premise=False),indent=2))
