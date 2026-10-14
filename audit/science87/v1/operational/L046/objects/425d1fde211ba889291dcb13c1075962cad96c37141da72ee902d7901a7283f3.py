"""Exact character arithmetic and maximal-subgroup union bounds."""
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import json

def need(ok,msg):
    if not ok:raise ValueError(msg)

def read_vectors(raw):
    tables={};current=None;maxes=None;complete=False
    for line in raw.splitlines():
        x=line.split()
        if not x:continue
        need(not complete,'record after terminal marker')
        if x[0]=='TABLE':
            need(current is None and len(x)==5,'bad table start');name=x[1]
            need(name not in tables,'duplicate table')
            current=dict(name=name,order=int(x[2]),type_count=int(x[3]),character_count=int(x[4]),types=[],vectors=[])
        elif x[0]=='TYPES':
            need(current is not None and not current['types'],'bad type row');current['types']=list(map(int,x[1:]))
        elif x[0]=='VECTOR':
            need(current is not None,'vector outside table');current['vectors'].append(list(map(int,x[1:])))
        elif x[0]=='ENDTABLE':
            need(current is not None and x[1]==current['name'],'wrong table end');t=current
            need(t['types']==sorted(set(t['types'])) and len(t['types'])==t['type_count'],'bad type set')
            need(len(t['vectors'])==t['character_count'] and all(len(v)==len(t['types'])+1 for v in t['vectors']),'incomplete character vectors')
            need(1 in t['types'] and 2 in t['types'],'missing identity/involution type')
            need(sum(v[0]**2 for v in t['vectors'])==t['order'],'character degree squares')
            need(all(v[0]>0 and v[1+t['types'].index(1)]==v[0] for v in t['vectors']),'identity character values')
            tables[t['name']]=t;current=None
        elif x[0]=='MAXCLASSES':
            need(current is None and maxes is None,'bad max classes');maxes=x[1:]
        elif line=='COMPLETE EXACT ORDER VECTORS':
            need(current is None and maxes is not None and not complete,'bad completion');complete=True
        else:raise ValueError('unknown vector record')
    need(complete and len(maxes)==13 and all(n in tables for n in maxes),'incomplete maximal coverage')
    expected=['L3(7).2','ONM2','J1','4_2.L3(4).2_1','ONM5','3^4:2^(1+4)D10','L2(31)','ONM8','4^3.L3(2)','M11','ONM11','A7','A7']
    need(maxes==expected,'maximal-class list differs from acquired classification')
    return tables,maxes

def all_count(t,p,q):
    if p not in t['types'] or q not in t['types']:return 0
    i,j,k=(1+t['types'].index(s) for s in [p,q,2])
    value=sum((Fraction(v[i]*v[j]*v[k],v[0]) for v in t['vectors']),Fraction())/t['order']
    need(value.denominator==1 and value>=0,'nonintegral character count');return int(value)

def derive(tables,maxes):
    G=tables['ON'];need(G['order']==460815505920,'wrong named ON order');aut=2*G['order']
    types=[s for s in G['types'] if s>2]
    need(types==[3,4,5,6,7,8,10,11,12,14,15,16,19,20,28,31],'wrong target types')
    rows=[]
    for p,q in combinations_with_replacement(types,2):
        x=all_count(G,p,q);bad=0;contributions=[]
        for name in maxes:
            h=tables[name];need(G['order']%h['order']==0,'subgroup order divisibility')
            y=all_count(h,p,q);term=(G['order']//h['order'])*y;bad+=term
            contributions.append(dict(table=name,order=h['order'],count=y,index=G['order']//h['order'],contribution=term))
        lo=max(0,-(-(x-bad)//aut));hi=x//aut;need(lo<=hi,'empty interval')
        rows.append(dict(p=p,q=q,all_pairs=x,maximal_upper_bad=bad,lower=lo,upper=hi,contributions=contributions))
    special=next(r for r in rows if(r['p'],r['q'])==(20,31))
    need(special['lower']==special['upper']==9118 and special['maximal_upper_bad']==0,'special exact count')
    need(len(rows)==136,'row coverage')
    sums={str(p):sum(r['lower']for r in rows if r['p']==p)for p in types}
    result=dict(group_order=G['order'],automorphism_order=aut,maximal_classes=maxes,rows=rows,
                lower_row_sums=sums,lower_total=sum(sums.values()),upper_total=sum(r['upper']for r in rows),
                positive_types=sum(r['lower']>0 for r in rows),exact_types=sum(r['lower']==r['upper']for r in rows))
    need(result['lower_total']==798370 and result['positive_types']==129 and result['exact_types']==20,'unexpected aggregate')
    return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--vectors',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=derive(*read_vectors(a.vectors.read_text()));a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ['lower_total','upper_total','positive_types','exact_types']}))
