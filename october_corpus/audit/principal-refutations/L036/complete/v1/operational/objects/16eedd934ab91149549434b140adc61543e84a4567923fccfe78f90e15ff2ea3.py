"""Independent exact arithmetic for the five fixed character-library exports."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction
import argparse
import copy
import hashlib
import json

GROUPS=['M11','M23','M24','J1','Ru']
SOURCE_COUNTS={'M11':37,'M23':170,'M24':5074,'J1':669,'Ru':1511}


def need(ok,message):
    if not ok:raise ValueError(message)


def integer(x,message,minimum=0):
    need(type(x) is int and x>=minimum,message)
    return x


def quotient(n,d,message):
    integer(n,message+' numerator')
    integer(d,message+' denominator',1)
    need(n%d==0,message+' divisibility')
    return n//d


def exact_integer(x,message):
    need(x.denominator==1,message)
    return x.numerator


def centralizers(order,values,label):
    integer(order,label+' group order',2)
    need(type(values) is list and len(values)>1,label+' class array')
    need(values[0]==order,label+' identity centralizer')
    sizes=[quotient(order,c,label+' centralizer') for c in values]
    need(sum(sizes)==order,label+' conjugacy classes exhaust the group')
    return sizes


def one(parent):
    need(type(parent) is list and len(parent)==5,'Parent record shape')
    name,order,cents,square,maxima=parent
    need(name in GROUPS,'Fixed named parent')
    centralizers(order,cents,name)
    n=len(cents)
    need(type(square) is list and len(square)==n and square[0]==1,'Square map domain and identity')
    need(all(type(i) is int and 1<=i<=n for i in square),'Square map range')
    need(type(maxima) is list and maxima,'Complete supplied maximal list')
    names=[]
    characters=[]
    indices=[]
    for row in maxima:
        need(type(row) is list and len(row)==4,'Maximal record shape')
        label,m,mc,fusion=row
        need(type(label) is str and label and label not in names,'Distinct maximal table identifiers')
        names.append(label)
        centralizers(m,mc,label)
        index=quotient(order,m,'Maximal index')
        need(index>1,'Proper maximal subgroup')
        indices.append(index)
        need(type(fusion) is list and len(fusion)==len(mc) and fusion[0]==1,'Fusion domain and identity')
        need(all(type(i) is int and 1<=i<=n for i in fusion),'Fusion range')
        sums=[Fraction(0) for _ in cents]
        for cm,f in zip(mc,fusion):
            quotient(cents[f-1],cm,'Embedded centralizer')
            sums[f-1]+=Fraction(1,cm)
        chi=[exact_integer(c*s,'Integral fixed-point character') for c,s in zip(cents,sums)]
        need(chi[0]==index and all(0<=x<=index for x in chi),'Coset character degree and bounds')
        need(sum(Fraction(x,c) for x,c in zip(chi,cents))==1,'Transitive coset action')
        characters.append(chi)
    psi=[sum(row[i] for row in characters) for i in range(n)]
    need(psi[0]==sum(indices),'Total conjugation-set degree')
    orbit_count=exact_integer(sum(Fraction(x,c) for x,c in zip(psi,cents)),'Integral subgroup-orbit count')
    need(orbit_count==len(maxima),'One orbit for each supplied maximal class')
    pairs=[]
    for i,x in enumerate(psi):
        twice=x*x-2*x+psi[square[i]-1]
        need(twice>=0 and twice%2==0,'Fixed unordered pairs are nonnegative integers')
        pairs.append(twice//2)
    count=exact_integer(sum(Fraction(x,c) for x,c in zip(pairs,cents)),'Integral unordered-pair orbit count')
    rank=exact_integer(sum(Fraction(x*x,c) for x,c in zip(psi,cents)),'Integral ordered-pair orbit count')
    indicator=exact_integer(sum(Fraction(psi[s-1],c) for s,c in zip(square,cents)),'Integral square-map average')
    need(2*count==rank-2*orbit_count+indicator,'Equivalent Burnside formulas')
    matrix=[]
    for i,a in enumerate(characters):
        matrix.append([exact_integer(sum(Fraction(x*y,c) for x,y,c in zip(a,b,cents)),
                                     'Integral coset-pair orbit count') for b in characters[i:]])
    return dict(name=name,order=order,maximal_classes=len(maxima),maximal_table_names=names,
                indices=indices,permutation_characters=characters,total_fixed_points=psi,
                fixed_unordered_pairs=pairs,degree=psi[0],subgroup_orbits=orbit_count,
                ordered_pair_orbits=rank,square_map_average=indicator,unordered_pair_orbits=count,
                triangular_coset_pair_orbits=matrix,
                source_Table1_count=SOURCE_COUNTS[name],source_comparison='agrees' if count==SOURCE_COUNTS[name] else 'differs')


def calculate(data):
    need(type(data) is list and len(data)==len(GROUPS),'Exactly five supplied parents')
    need([x[0] for x in data]==GROUPS,'Exact source group order')
    return [one(row) for row in data]


def parse(raw):
    """Keep raw bytes separately; accept only whitespace outside two unique markers."""
    begin=b'BEGIN_L036_CHARACTER_INPUTS\n'
    end=b'END_L036_CHARACTER_INPUTS\n'
    need(raw.count(begin)==raw.count(end)==1,'Unique output markers')
    prefix,body=raw.split(begin)
    payload,suffix=body.split(end)
    need(not prefix.strip() and not suffix.strip(),'No unbound diagnostic output')
    return json.loads(payload.decode('ascii'))


def damaged_controls(data):
    mutations=[('identity_centralizer',lambda d:d[0][2].__setitem__(0,d[0][2][0]+1)),
               ('fusion_out_of_range',lambda d:d[0][4][0][3].__setitem__(0,len(d[0][2])+1)),
               ('square_out_of_range',lambda d:d[0][3].__setitem__(0,len(d[0][2])+1)),
               ('duplicate_maximal_identifier',lambda d:d[0][4].append(copy.deepcopy(d[0][4][0]))),
               ('wrong_parent_order',lambda d:d[0].__setitem__(1,d[0][1]+1))]
    rejected=[]
    for name,mutate in mutations:
        bad=copy.deepcopy(data)
        mutate(bad)
        try:calculate(bad)
        except ValueError:rejected.append(name)
        else:raise ValueError('Accepted damaged data: '+name)
    return rejected


def main(a):
    raw=a.input.read_bytes()
    need(len(raw)<=8*2**20,'Acquired output cap')
    need(hashlib.sha256(raw).hexdigest()==a.expected_sha,'Exact actual raw output')
    need(a.out.is_absolute() and not a.out.exists(),'Fresh absolute output')
    data=parse(raw)
    result=dict(status='PASS_EXACT_L036_CHARACTER_ARITHMETIC',groups=calculate(data),
                controls=damaged_controls(data),input_sha256=a.expected_sha,
                conclusion_scope='Five Out=1 totals, conditional on explicit complete library/classification premises.',
                outer_cases_accepted=False,suborbit_tables_accepted=False,whole_source_accepted=False)
    a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],counts={r['name']:r['unordered_pair_orbits'] for r in result['groups']},
                          controls=result['controls'],whole_source_accepted=False)))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--expected-sha',required=True)
    p.add_argument('--out',type=Path,required=True)
    main(p.parse_args())
