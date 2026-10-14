"""Compare the fixed survey data with already accepted exact results."""
import sys
if sys.flags.optimize:raise RuntimeError('unoptimized execution required')
from pathlib import Path
from fractions import Fraction
import json,re,hashlib
W=Path(__file__).resolve().parent;S=W.parents[1]
def need(b,s):
 if not b:raise ValueError(s)
def load(p):return json.loads((S/p).read_text())
def pin(p):
 b=(S/p).read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
tables=json.loads((W/'survey_tables03.json').read_text())['tables'];rows=[];pins=[]
remaining_path='corpus106_L071_remaining_censuses_v1/census_comparison.json';q=load(remaining_path);pins.append(pin(remaining_path));remaining={r['group']:r for r in q['rows']}
for t in (tables[0],tables[2],tables[4]):
 for row in t['rows']:
  group=row['group'];old=remaining.get(group);row['dispositions']={}
  for rankstr,count in row['rank_counts'].items():
   rank=int(rankstr);mode='unrecovered_source_data' if t['table']in(1,3)else 'retained_cited_historical_census';calc=None
   if old is not None:
    z=next((x for x in old['nonzero_ranks']if x[0]==rank),None)
    if z:need(z[1]+z[2]==2*z[3],'duality arithmetic');calc=z[3]
    else:calc=0
    mode='acquired_complete_L071_census'
   elif group.startswith('S') and group[1:].isdigit():
    n=int(group[1:]);k=n-rank
    if rank>=n:mode='acquired_independent_length_bound';calc=0
    elif 1<=k<=6 and n>=2*k+3:mode='acquired_L019_stability';calc=[1,1,7,9,35,48][k-1]
   elif group.startswith('A') and group[1:].isdigit():
    n=int(group[1:]);maxr={5:3,9:4,10:5,11:6}.get(n,(n-1)//2 if n>=12 else -1)
    if n in (6,7,8) or rank>maxr:mode='acquired_L044_bound';calc=0
   if calc is not None:need(calc==count,f'source mismatch {group} rank{rank}: {calc}!={count}')
   row['dispositions'][rankstr]={'mode':mode,'value':count,'verified_value':calc}
  if old is not None and 'source_order'in row:
   row['verified_order']=old['order'];row['order_correction']=row['source_order']!=old['order']
   if row['order_correction']:need(group=='M22' and row['source_order']==443510 and old['order']==443520,'unexpected group order correction')
for n,folder in [(11,'L071_A11_restored01'),(12,'L071_A12_restored01'),(13,'L071_A13_restart01'),(14,'L071_A14_full_rank01')]:
 path=f'reboot_20261013/{folder}/alternating_summary.json';x=load(path);pins.append(pin(path));need(x['complete'],'incomplete alternating run')
 row=next(z for z in tables[2]['rows']if z['degree']==n)
 for r,val in row['rank_counts'].items():
  c=x['ordered_alternating_counts'].get(r,0);s=x['self_dual_alternating_counts'].get(r,0);need((c+s)%2==0,'dual integral');v=(c+s)//2;need(v==val,'alternating survey mismatch')
  row['dispositions'][r]={'mode':'acquired_L071_complete_census_with_duality','ordered':c,'self_dual':s,'value':val,'verified_value':v}
p='reboot_20261013/double_coset/Co3_01/stdout.log';raw=(S/p).read_text();pins.append(pin(p));need(raw.count('COMPLETE_EXHAUSTION')==1,'Co3 completion')
pattern=r'RANK\s+(\d+)\s+ordered\s+(\d+)\s+self\s+(\d+)\s+dual_classes\s+(\d+)\s+connected_ordered'
co={int(r):(int(c),int(s),int(d))for r,c,s,d in re.findall(pattern,raw)};need(set(co)==set(range(1,39)),'Co3 full ranks')
row=next(z for z in tables[4]['rows']if z['group']=='Co3')
for r,val in row['rank_counts'].items():
 c,s,d=co[int(r)];need(c+s==2*d and d==val,'Co3 count');row['dispositions'][r]={'mode':'acquired_L071_complete_census_with_duality','ordered':c,'self_dual':s,'value':val,'verified_value':d}
need(all(c==s==d==0 for r,(c,s,d)in co.items()if r>5),'Co3 upper rank')
# Reuse complete retained lists; only the reversal matching is new here.
p='reboot_20261013/L120_recovery_work/duality_work/duality.stdout';raw=(S/p).read_text();pins.append(pin(p));need(raw.count('PASS_RETAINED_LIST_DUALITY')==1,'duality completion')
for p in ['reboot_20261013/L120_recovery_work/duality_work/duality.g','reboot_20261013/L120_recovery_work/duality_work/s5_arrays.g','reboot_20261013/L120_recovery_work/duality_work/s5_arrays.json','topic_B_L044_small_maxima_v1/author_validation/A10/records.g','topic_B_L047_candidate_v2/author_programs/primitive_markings.stdout.log']:
 pins.append(pin(p))
seen=[]
for g,r,c,f,d in re.findall(r'DUAL\|(A10|S5)\|(\d+)\|(\d+)\|(\d+)\|(\d+)',raw):
 c,f,d=map(int,(c,f,d));need(c+f==2*d,'retained reversal quotient')
 row=next(x for t in (tables[0],tables[2])for x in t['rows']if x['group']==g)
 need(row['rank_counts'][r]==d,'retained reversal source comparison')
 row['dispositions'][r]={'mode':'acquired_complete_list_new_reversal_matching','ordered':c,'self_dual':f,'value':d,'verified_value':d};seen.append((g,int(r)))
need(set(seen)=={('A10',3),('A10',4),('A10',5),('S5',3),('S5',4)},'all intended retained lists')
# Topic D's accepted full Aut(S6) endpoint-orbit enumeration already includes endpoint reversal.
public=S.parents[1]/'math_compression';p=public/'papers/topic-d/v2/author_replay/small/degree_six/finite.log';b=p.read_bytes();pins.append({'namespace':'public','path':str(p.relative_to(public)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
lines=b.decode().splitlines();need('SUMMARY|720|1440|75|495|9|5|80|2|2|128|128'in lines and 'PASS'in lines,'acquired complete S6 receipt')
row=next(x for x in tables[0]['rows']if x['group']=='S6');need(row['rank_counts']['3']==2,'S6 source rank3')
row['dispositions']['3']={'mode':'acquired_TopicD_complete_AutS6_endpoint_orbits','value':2,'verified_value':2}

# The source formulas and the independent orbit-multiplicity count are both exact integers.
def formula(N,even):
 n=N//2
 lam=lambda k:((k+2)*(k+2))//4
 def psi(k):return sum(l//2+1 for l in range(max(0,2*k-n)))
 if even:
  mu=Fraction(-2*(n//2))
  for k in range(2,n+1,2):
   gamma=Fraction(k*k,8)+Fraction(3*k,4)+1;delta=Fraction(k*k,8)+Fraction(k,4)
   mu+=gamma*((n-k+2)//2)+delta*((n-k+1)//2)
  ans=(mu+sum(lam(k)-psi(k)-1 for k in range(2,n+1,2)))/2
 else:ans=-Fraction(3*n,2)+sum(lam(k)*(Fraction(n-k,2)+1)for k in range(1,n+1))-Fraction(sum(psi(k)for k in range(n//2+1,n+1)),2)
 need(ans.denominator==1,'formula integrality');return int(ans)
def direct(N,even):
 out=0
 for t in range(N//4+1):
  for x in range(N//2+1):
   for y in range(x,(N-4*t-2*x)//2+1):
    for z in range((N-4*t-2*x-2*y)//2+1):
     if t==0 and sum(a>0 for a in (x,y,z))<2:continue
     if even and not(x%2==y%2==z%2):continue
     out+=1
 return out
controls=[]
for N in range(1,51):
 for even in (False,True):
  f=formula(N,even);d=direct(N,even);need(f==d,f'orbit formula N{N}')
  controls.append({'degree':N,'even':even,'permutation_conjugacy':d})
for row in tables[1]['rows']:
 row['dispositions']={}
 for n in row['degrees']:
  s,a=(5,1)if n==6 else (formula(n,False),formula(n,True))
  need((s,a)==(row['symmetric'],row['alternating']),f'table2 N{n}')
  row['dispositions'][str(n)]={'mode':'acquired_L066_formula_and_six_point_fusion','verified':[s,a]}
out={'status':'PASS_ALL_ASSERTED_SURVEY_TABLE_COMPARISONS','numeric_tables':tables,'formula_controls':controls,'bindings':pins,'no_new_census':True,'remaining_finite_reports':'Unrecovered source-only experimental cells are explicit unpaid obligations. Cited historical sporadic classifications remain separately attributed inputs. No source table is used as its own proof.'}
(W/'survey_table_comparison03.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'bindings':len(pins),'checked_rank_cells':sum(v['verified_value'] is not None for t in (tables[0],tables[2],tables[4])for row in t['rows']for v in row['dispositions'].values()),'retained_rank_cells':sum(v['verified_value'] is None for t in (tables[0],tables[2],tables[4])for row in t['rows']for v in row['dispositions'].values()),'formula_controls':len(controls)}))
