"""Independent cycle-syntax parser and right-action permutation oracle."""
import sys
if sys.flags.optimize:
    raise SystemExit("Run without Python optimization.")
import json
import math
import re


def need(condition, message):
    if not condition:
        raise ValueError(message)


def source_parameters():
    first = [(s,n,q) for n,q in [(4,2),(4,3),(4,4),(5,2),(6,2)] for s in ["L","U"]]
    first += [("S",n,q) for n,q in [(4,3),(4,4),(6,2),(6,3),(8,2)]]
    first += [("O",7,3)] + [(s,n,2) for n in [8,10] for s in ["O+","O-"]] + [("O+",8,3)]
    second = [(s,n,q) for n,q in [(5,3),(6,3),(8,2)] for s in ["L","U"]]
    second += [("S",n,q) for n,q in [(6,4),(8,3),(8,4)]] + [(s,12,2) for s in ["O+","O-"]]
    return first, second, [("G",2,3),("G",2,4),("T",)]


def roster(rows):
    first, second, exceptional = source_parameters()
    actual = [tuple(r["parameters"]) for r in rows]
    need(len(rows)==35 and len(set(actual))==35 and set(actual)==set(first+second+exceptional), "exact 21+11+3 source roster")
    need([r["id"] for r in rows]==[f"case{i:02}" for i in range(1,36)], "literal case labels")
    for r in rows:
        p=tuple(r["parameters"])
        page=7 if p in first else 8 if p in second else 6
        need(r["source_clause"].endswith(f"physical page {page}"), "exact source route")
        need(type(r["case_number"]) is int and r["case_number"]>=1, "constructor seed")
        need(r["relative_pair"]==f'candidates/{r["id"]}/pair.g', "exact saved pair path")
    return {"classical_initial":21,"classical_remaining":11,"exceptional":3,"parameter_entries":35}


def split_top(text):
    depth=0;start=0;out=[]
    for i,c in enumerate(text):
        if c in "([": depth+=1
        elif c in ")]": depth-=1
        elif c=="," and depth==0:
            out.append(text[start:i]);start=i+1
        need(depth>=0,"balanced cycle/list syntax")
    need(depth==0,"closed cycle/list syntax")
    out.append(text[start:])
    return out


def permutation(text, n):
    text=re.sub(r"\s+","",text)
    need(re.fullmatch(r"(?:\((?:\d+(?:,\d+)*)?\))+",text) is not None,"literal permutation grammar")
    p=list(range(n));seen=set()
    for c in re.findall(r"\(([^)]*)\)",text):
        if not c: continue
        points=[int(x)-1 for x in c.split(",")]
        need(len(points)==len(set(points)) and all(0<=x<n and x not in seen for x in points),"disjoint valid literal cycles")
        seen.update(points)
        for a,b in zip(points,points[1:]+points[:1]): p[a]=b
    need(sorted(p)==list(range(n)),"literal bijection")
    return tuple(p)


def parse_pair(path):
    text=path.read_text()
    need(text.startswith("HC_SavedPair:=rec(") and text.strip().endswith(");;"),"saved record envelope")
    body=text[len("HC_SavedPair:=rec("):text.rindex(");;")]
    fields={}
    for item in split_top(body):
        name,sep,value=item.partition(":=")
        need(sep and name.strip() not in fields,"unique record fields")
        fields[name.strip()]=value.strip()
    need(set(fields)=={"parameters","ambient_generators","degree","group_order","orders","trial","x","t"},"exact record schema")
    out={k:json.loads(fields[k]) for k in ["parameters","degree","group_order","orders","trial"]}
    n=out["degree"]
    need(type(n) is int and n>0,"literal degree")
    out.update({k:permutation(fields[k],n) for k in ["x","t"]})
    s=fields["ambient_generators"]
    need(s.startswith("[") and s.endswith("]"),"ambient list")
    out["ambient_generators"]=[permutation(p,n) for p in split_top(s[1:-1])]
    return out


def mul(p,q):
    return tuple(q[i] for i in p)


def power(p,k):
    if k<0:
        inverse=[0]*len(p)
        for a,b in enumerate(p): inverse[b]=a
        return power(tuple(inverse),-k)
    result=tuple(range(len(p)))
    while k:
        if k&1: result=mul(result,p)
        p=mul(p,p);k//=2
    return result


def order(p):
    seen=set();result=1
    for i in range(len(p)):
        if i in seen: continue
        j=i;length=0
        while j not in seen:
            seen.add(j);length+=1;j=p[j]
        result=math.lcm(result,length)
    return result


def word(x,t):
    result=tuple(range(len(x)))
    for k in [1,2,3]: result=mul(mul(result,power(x,k)),t)
    return result


def verify_literal(base, rows):
    report=[]
    for row in rows:
        p=parse_pair(base/row["relative_pair"])
        for k in ["parameters","degree","group_order","orders"]: need(p[k]==row[k],"literal metadata "+k)
        x,t=p["x"],p["t"]
        need(order(t)==2,"literal involution")
        actual=[order(x),order(mul(power(x,-1),t)),order(word(x,t)),order(word(power(x,-1),t))]
        need(actual==row["orders"] and min(actual[:2])>2 and actual[2]!=actual[3],"independent literal word orders")
        report.append({"id":row["id"],"parameters":row["parameters"],"degree":p["degree"],"orders":actual,"parsed_generators":len(p["ambient_generators"])})
    return report
