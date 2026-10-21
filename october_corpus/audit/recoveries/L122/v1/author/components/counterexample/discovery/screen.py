"""Exploratory full correlation-group screen, not a frozen certificate."""
import json
from pathlib import Path
import pynauty

raw=Path('/private/tmp/L122_small81_candidates.jsonl').read_text()
decoder=json.JSONDecoder(); rows=[]
while raw.strip():
    raw=raw.lstrip(); row,end=decoder.raw_decode(raw);rows.append(row);raw=raw[end:]
seen=set();out=[]
for num,row in enumerate(rows):
    n=row['n']; size=3*n
    adj={v:[x-1 for x in row['adj'][v]]+[size+v//n] for v in range(size)}
    for i in range(3):adj[size+i]=list(range(i*n,(i+1)*n))
    graph=pynauty.Graph(size+3, adjacency_dict=adj, vertex_coloring=[set(range(size)),set(range(size,size+3))])
    canon=pynauty.certificate(graph)
    if canon in seen:continue
    seen.add(canon)
    gens,a,b,orbits,no=pynauty.autgrp(graph)
    row['aut_generators']=[[x+1 for x in g] for g in gens]
    row['aut_order']=round(a*10**b);row['candidate']=num
    out.append(row)
    print(num,row['gid'],n,row['aut_order'],flush=True)
Path('/private/tmp/L122_small81_screen.json').write_text(json.dumps(out))
with open('/private/tmp/L122_small81_autcheck.g','w') as f:
    f.write('results:=[];;\n')
    for row in out:
        size=3*row['n'];gens=repr(row['aut_generators'])
        f.write(f'A:=Group(List({gens},PermList));; pp:={list(range(size+1,size+4))};;\n')
        f.write('P:=SylowSubgroup(A,3);; good:=Filtered(ConjugacyClasses(P),c->Order(Representative(c))=3 and not ForAll(pp,x->x^Representative(c)=x));;\n')
        f.write(f'Print("CANDIDATE {row["candidate"]} gid {row["gid"]} A ",Size(A)," P ",Size(P)," GOOD ",Length(good),"\\n");;\n')
    f.write('QUIT;\n')
