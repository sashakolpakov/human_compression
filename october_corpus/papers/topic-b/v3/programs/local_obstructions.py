#!/usr/bin/env python3
"""Exact bounded local intersection obstructions for the L040 converse.

No classification package is used: every subgroup is enumerated in S_6 by
permutation multiplication. The model list is the complete list specified
in the written fracture-graph proof, not a search over arbitrary markings.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import deque
from pathlib import Path

IDENTITY = tuple(range(6))

def need(ok, message):
    if not ok:
        raise ValueError(message)

def mul(a, b):
    return tuple(b[a[i]] for i in range(6))

def trans(a,b):
    p=list(IDENTITY);p[a-1],p[b-1]=p[b-1],p[a-1];return tuple(p)

def product(*pairs):
    p=IDENTITY
    for a,b in pairs:p=mul(p,trans(a,b))
    return p

def models():
    out=[]
    for core_kind, core in [
        ('path', [product((1,2),(4,5)),product((2,3),(4,5)),trans(3,4)]),
        ('star', [product((1,3),(4,5)),product((2,3),(4,5)),trans(3,4)])]:
        for vertex in range(1,6):
            for twist in range(2 if vertex<4 else 1):
                p=mul(trans(vertex,6),product((4,5)) if twist else IDENTITY)
                out.append((f'{core_kind}_v{vertex}_twist{twist}',core+[p]))
    out.append(('parallel_opposite', [product((1,2),(3,4)),product((3,4),(5,6)),trans(2,3),trans(4,5)]))
    out.append(('parallel_same', [product((1,2),(5,6)),product((3,4),(5,6)),trans(2,5),trans(4,5)]))
    need(len(out)==18,'exact local model count')
    return out

def subgroup(gens,mask):
    seen={IDENTITY:[]};queue=deque([IDENTITY])
    while queue:
        p=queue.popleft()
        for i,g in enumerate(gens):
            if mask>>i&1:
                h=mul(p,g)
                if h not in seen:seen[h]=seen[p]+[i];queue.append(h)
    return seen

def word(gens,seq):
    p=IDENTITY
    for i in seq:p=mul(p,gens[i])
    return p

def record(name,gens):
    groups=[subgroup(gens,i) for i in range(16)]
    for I in range(16):
        for J in range(I+1,16):
            bad=set(groups[I]).intersection(groups[J]).difference(groups[I&J])
            if bad:
                w=min(bad)
                return {'name':name,'generators':[list(g) for g in gens],
                        'left':I,'right':J,'witness':list(w),
                        'left_word':groups[I][w],'right_word':groups[J][w],
                        'common_subgroup_order':len(groups[I&J]),
                        'actual_intersection_order':len(set(groups[I]).intersection(groups[J]))}
    raise ValueError('model unexpectedly has IP: '+name)

def verify(records):
    expected=models();need(len(records)==len(expected),'missing local case')
    for row,(name,gens) in zip(records,expected):
        need(row['name']==name and row['generators']==[list(g) for g in gens], 'model substitution')
        I,J=row['left'],row['right'];w=tuple(row['witness'])
        need(0<=I<16 and 0<=J<16,'bad support')
        need(all(I>>i&1 for i in row['left_word']), 'left word support')
        need(all(J>>i&1 for i in row['right_word']), 'right word support')
        need(word(gens,row['left_word'])==w==word(gens,row['right_word']), 'word identity')
        common=subgroup(gens,I&J)
        need(w not in common,'intersection witness belongs to required intersection')
        need(row['common_subgroup_order']==len(common),'common order')
        left=subgroup(gens,I);right=subgroup(gens,J)
        need(row['actual_intersection_order']==len(set(left).intersection(right)), 'intersection order')
    return len(records)

def run():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);args=parser.parse_args()
    out=Path(args.out);need(not out.exists() and not out.is_symlink(),'output must be fresh');out.mkdir(parents=True)
    rows=[record(name,gens) for name,gens in models()];verify(rows)
    controls=[]
    import copy
    for label,mutate in [
      ('omit_case',lambda r:r.pop()),
      ('identity_witness',lambda r:r[0].update(witness=list(IDENTITY),left_word=[],right_word=[])),
      ('alter_marking',lambda r:r[0]['generators'].__setitem__(0,list(IDENTITY))),
      ('wrong_support',lambda r:r[0].update(left=0)),
      ('false_common_order',lambda r:r[0].update(common_subgroup_order=999))]:
        altered=copy.deepcopy(rows);mutate(altered)
        try:verify(altered)
        except (ValueError,IndexError):controls.append({'control':label,'rejected':True})
        else:raise ValueError('mutation accepted: '+label)
    (out/'witnesses.json').write_text(json.dumps(rows,indent=2)+'\n')
    report={'status':'PASS','cases':len(rows),'controls':controls,
            'scope':'18 exact six-letter local IP obstructions; completeness of the local reduction is proved in TeX',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':run()
