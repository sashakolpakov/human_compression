"""Small exact models of the actual formula and failed omissions; not proof substitutes."""
from fractions import Fraction
from itertools import product

def need(ok,msg):
 if not ok:raise ValueError(msg)
def mu_top(n,le):
 result={n-1:1}
 for i in reversed(range(n-1)):result[i]=-sum(result[j] for j in range(i+1,n) if le(i,j))
 return result

def countermodels():
 # Diamond support poset, whose two middle elements are interchanged.
 le=lambda x,y:x==y or x==0 or y==3
 mu=mu_top(4,le);support=[1,2,3,3];act=lambda a,x:x^(a&1)
 transport=lambda a,l:3-l if a and l in [1,2] else l
 need(all(support[act(a,x)]==transport(a,support[x]) for a in range(2) for x in range(4)),'equivariant support')
 need({x for x in range(4) if le(support[x],1)}=={0} and act(1,0)==1,'sublevel genuinely not invariant')
 fixed_sums=[sum(mu[l]*sum(act(a,x)==x and le(support[x],l) for x in range(4)) for l in range(4)) for a in range(2)]
 need(fixed_sums==[2,0] and Fraction(sum(fixed_sums),2)==1,'actual exact-top orbit count')
 # Equivariant base map to the regular two-point action; stabilizer at 0 is trivial.
 p=lambda x:x%2
 need(all(p(act(a,x))==act(a,p(x)) for a in range(2) for x in range(4)),'base map equivariance')
 fiber_count=sum(mu[l]*sum(p(x)==0 and le(support[x],l) for x in range(4)) for l in range(4))
 need(fiber_count==1,'actual representative-fiber formula')
 # The two-chain has top Möbius coefficients -1,1.
 need(mu_top(2,lambda x,y:x<=y)=={1:1,0:-1},'two-chain coefficients')
 wrong_exact=-1;wrong_all_ones=2
 need(wrong_exact!=0 and wrong_all_ones!=0,'support at bottom gives zero exact-top count')
 # A regular C2 action at constant top has one orbit, whereas unaveraged fixed sum is two.
 need(Fraction(2,2)==1 and 2!=1,'division by group order is essential')
 # C2 swaps bottom/top points: the subset is not invariant; the resulting expression is 1/2.
 invalid_average=Fraction(1,2)
 need(invalid_average.denominator==2,'missing exact-support invariance gives nonintegral result')
 # Check the incidence indicator for all naturally ordered finite posets with a top, up to five points.
 posets=0;indicator_cases=0
 for n in range(1,6):
  candidates=[(i,j) for i in range(n) for j in range(i+1,n-1)]
  for bits in product([False,True],repeat=len(candidates)):
   pairs={(i,i) for i in range(n)}|{(i,n-1) for i in range(n)}|{p for p,b in zip(candidates,bits) if b}
   if any((i,j) in pairs and (j,k) in pairs and (i,k) not in pairs for i in range(n) for j in range(n) for k in range(n)):continue
   order=lambda i,j:(i,j) in pairs;coeff=mu_top(n,order);posets+=1
   for i in range(n):need(sum(coeff[j] for j in range(n) if order(i,j))==int(i==n-1),'actual Möbius indicator');indicator_cases+=1
 return [dict(model='diamond with noninvariant individual sublevels',fixed_sums=fixed_sums,exact_top_orbits=1,fiber_representative_count=fiber_count),
  dict(omitted='actual incidence Möbius coefficients',false_indicator=wrong_all_ones,correct=0),
  dict(omitted='sublevel counts replaced by exact-level counts',false_indicator=wrong_exact,correct=0),
  dict(omitted='Burnside denominator',false_count=2,correct=1),
  dict(omitted='invariance of the exact-top subset',false_average=str(invalid_average),restricted_action_defined=False),
  dict(validation='finite poset indicators',posets=posets,indicator_cases=indicator_cases)]
