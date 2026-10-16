"""Small literal arithmetic witnesses; not a subgroup-classification verifier."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
import json,copy

def need(ok,message):
    if not ok:raise ValueError(message)
def values(e):
    q=2**(2*e+1);t=2**(e+1)
    return q+t+1,q-t+1

def check(d):
    need(d['lemma3_5']=={'q':32768,'s':8,'other_subfield':32,'factorization':[7,31,151],'quotient':4681},'Exact divisor witness')
    r=d['lemma3_5'];need(r['q']-1==7*31*151 and (r['q']-1)//(r['s']-1)==r['quotient'],'Small factorization')
    need(r['q']==r['s']**5==r['other_subfield']**3,'Two maximal field indices')
    need(all(7%a for a in [2]),'Seven is prime')
    need(d['lemma3_6ii']=={'s':8,'q':32,'small_factors':[13,5],'large_factors':[41,25]},'Exact divisibility witness')
    r=d['lemma3_6ii'];need(r['q']%r['s']==0 and values(1)==tuple(r['small_factors']) and values(2)==tuple(r['large_factors']),'Actual torus integers')
    need(all(t%13 for t in r['large_factors']),'Neither compatible factor available')
    need(d['lemma3_6iii']['period_four_residues']==[[0,1],[3,0],[1,0],[0,3]],'Exact residue table')
    need([[a%5,b%5] for a,b in [values(e) for e in range(4)]]==d['lemma3_6iii']['period_four_residues'],'Four direct residues')
    need(values(1)[0]==13 and 13%5!=0 and 3%4==3,'Printed variable fails at q8')
    need(d['lemma3_9ii']=={'q':8,'d':5,'p':13,'proposed_odd_order':65,'available_odd_torus_orders':[5,7,13]},'Exact incompatible extension witness')
    r=d['lemma3_9ii'];need((r['q']**2+1)//r['d']==r['p'] and r['d']*r['p']==65,'Printed prime condition')
    need(all(t%65 for t in r['available_odd_torus_orders']),'No torus supports order65')
    return dict(status='PASS_FOUR_LITERAL_ARITHMETIC_WITNESSES',group_premises='Classical field-subgroup/maximality and torus partition are explicit mathematical premises, not tested here',new_principal_refutations=0,new_conjecture_credit=0)
def controls(d):
    tests=[]
    for key,field in [('lemma3_5','quotient'),('lemma3_6ii','q'),('lemma3_9ii','proposed_odd_order')]:
        x=copy.deepcopy(d);x[key][field]+=1;tests.append((key,x))
    x=copy.deepcopy(d);x['lemma3_6iii']['period_four_residues'][0][0]=1;tests.append(('residue_table',x))
    rejected=[]
    for name,x in tests:
        try:check(x)
        except ValueError:rejected.append(name)
        else:raise ValueError('Damage survived: '+name)
    return rejected
if __name__=='__main__':
    from pathlib import Path
    d=json.loads(Path(__file__).with_name('arithmetic.json').read_text());r=check(d);r['rejected_damages']=controls(d);print(json.dumps(r,sort_keys=True))
