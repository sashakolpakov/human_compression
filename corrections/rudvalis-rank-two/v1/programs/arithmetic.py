"""Exact orbit arithmetic and independent small permutation-action controls."""
import sys
if sys.flags.optimize:
    raise SystemExit('Ordinary Python required')
import argparse,itertools,json
from fractions import Fraction
from pathlib import Path

def need(ok, message):
    if not ok:
        raise ValueError(message)

def compose(a,b):
    return tuple(a[b[i]] for i in range(len(a)))

def closure(generators):
    e=tuple(range(len(generators[0]))); group={e}; todo=[e]
    while todo:
        a=todo.pop()
        for b in generators:
            c=compose(a,b)
            if c not in group:
                group.add(c);todo.append(c)
    return group

def action_check(group):
    n=len(next(iter(group))); pairs=set(itertools.combinations(range(n),2))
    remaining=set(pairs); orbits=[]
    while remaining:
        a,b=min(remaining)
        orbit={tuple(sorted((g[a],g[b]))) for g in group}
        need(orbit<=remaining,'disjoint complete orbits')
        remaining-=orbit;orbits.append(len(orbit))
    terms=[]
    for g in group:
        f=sum(g[i]==i for i in range(n))
        f2=sum(g[g[i]]==i for i in range(n))
        terms.append(f*f-2*f+f2)
    formula=Fraction(sum(terms),2*len(group))
    need(formula==len(orbits),'Burnside count equals independent set orbit partition')
    return dict(degree=n,group_order=len(group),pair_orbit_sizes=sorted(orbits),count=len(orbits))

def calculate():
    order=145926144000;subgroup=20*60;outer=1;index=order//subgroup
    need(order==subgroup*index,'exact group index')
    pairs=index*(index-1)//2
    ratio=Fraction(pairs,order*outer)
    need(ratio==Fraction(index-1,2*subgroup),'two independent bound formulas agree')
    lower=-(-ratio.numerator//ratio.denominator)
    need((lower-1)*ratio.denominator<ratio.numerator<=lower*ratio.denominator,'exact ceiling')
    need(lower==50669 and lower>1511,'contradiction to fixed source row')
    controls=[action_check(set(itertools.permutations(range(n)))) for n in [3,4,5]]
    controls.append(action_check(closure([(1,2,3,4,0)])))
    controls.append(action_check(closure([(1,2,3,0),(0,3,2,1)])))
    controls.append(action_check(closure([(1,2,0,3,4),(0,1,2,4,3)])))
    return dict(status='PASS_L036_ORBIT_BOUND',group_order=order,maximal_subgroup_order=subgroup,
                outer_order=outer,conjugates=index,unordered_pairs=pairs,
                exact_ratio=[ratio.numerator,ratio.denominator],lower_bound=lower,
                source_total=1511,small_action_controls=controls,
                retained_inputs=['Simplicity and order of Ru','Out(Ru)=1','Maximal subgroup (5:4)xA5'],
                exact_corrected_total=None,whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(not a.out.exists(),'fresh output');r=calculate();a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
