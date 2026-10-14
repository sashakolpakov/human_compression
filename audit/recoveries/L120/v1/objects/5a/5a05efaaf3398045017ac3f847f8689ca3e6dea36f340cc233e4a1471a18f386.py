"""Exact individual interfaces for the two nonnumeric survey tables."""
import sys
if sys.flags.optimize: raise RuntimeError('unoptimized execution required')
import json,re,hashlib,math
from pathlib import Path
W=Path(__file__).resolve().parent;S=W.parents[1]
def need(b,s):
    if not b:raise ValueError(s)
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def comp(a,b):return [b[x-1]for x in a]
def order(p):
    seen=set();o=1
    for x in range(1,len(p)+1):
        if x in seen:continue
        y=x;c=0
        while y not in seen:seen.add(y);c+=1;y=p[y-1]
        o=math.lcm(o,c)
    return o
def marking(r):
    odd=r%2;end=r+odd;n=2*end+1;top=lambda j:j;bottom=lambda j:end+1+j
    edges=[[]for _ in range(r)]
    edges[0]=[(bottom(0),bottom(1))]+[(top(j),bottom(j))for j in range(2,end+1)]
    for i in range(1,r):edges[i]=[(top(i),top(i+1)),(bottom(i),bottom(i+1))]
    if odd:edges[r-2]+=[(top(r),top(r+1)),(bottom(r),bottom(r+1))]
    marks=[]
    for pairs in edges:
        need(len({x for e in pairs for x in e})==2*len(pairs),'matching');p=list(range(1,n+1))
        for a,b in pairs:p[a-1]=b;p[b-1]=a
        need(len(pairs)%2==0,'even involution');marks.append(p)
    for i in range(r):
        need(order(marks[i])==2,'involution')
        for j in range(i+2,r):need(comp(marks[i],marks[j])==comp(marks[j],marks[i]),'distant commutation')
    actual=[order(comp(a,b))for a,b in zip(marks,marks[1:])]
    expected=([10]+[3]*(r-4)+[6,4])if odd else ([10]+[3]*(r-2))
    need(actual==expected,'exact diagram type')
    return {'rank':r,'degree':n,'edges':edges,'marks':marks,'type':actual}
src=W/'survey-final.tex';raw=src.read_text();blocks=re.findall(r'\\begin\{table\}(.*?)\\end\{table\}',raw,re.S)
need(len(blocks)==6,'source table count')
diags=re.findall(r'\\xymatrix@-1\.7pc\{(.*?)\}\$',blocks[3],re.S)
need(len(diags)==2,'two literal diagram bodies')
families=[]
for odd in (False,True):
    families.append({'row':int(odd)+1,'rank_condition':'odd r>=5'if odd else 'even r>=4','degree':'2r+3'if odd else '2r+1','type':'[10,3^(r-4),6,4]'if odd else '[10,3^(r-2)]','diagram_body_sha256':hashlib.sha256(diags[int(odd)].encode()).hexdigest(),'vertices':{'top':'1..r+1'if odd else '1..r','bottom':'0..r+1'if odd else '0..r'},'edges':{'label0':'bottom0--bottom1 and topj--bottomj for every j>=2','labels1_to_r_minus1':'topi--top(i+1) and bottomi--bottom(i+1)','additional_last_edges':'label r-2 joins top r to top(r+1) and bottom r to bottom(r+1)'if odd else 'none'},'proof_input':'Fernandes--Leemans--Mixer (2012), Theorem1.1, explicitly cited in survey Theorem4.6. This interface retains the published infinite generation/intersection theorem; finite checks below verify the literal transcription only.','qualification':'The odd-rank family is not silently substituted by the other L038 maximal-rank seed.'if odd else 'The even-rank family is also the actual retained L038 seed.'})
controls=[marking(r)for r in range(4,26)]
p=S/'topic_B_L047_candidate_v2/author_programs/small_transitive.stdout.log';records=[]
for line in p.read_text().splitlines():
    if not line.startswith('SOLUTION|'):continue
    _,n,i,t,g=line.split('|');records.append({'degree':int(n),'catalogue_index':int(i),'type':json.loads(t),'marks':json.loads(g)})
table6=[]
for line in blocks[5].splitlines():
    if not re.match(r'^\s*\d+&\d+&',line):continue
    cols=line.strip().removesuffix('\\\\').split('&');need(len(cols)==5,'five finite columns')
    n,i,o=map(int,[cols[0],cols[1],cols[3]])
    typ=list(map(int,re.search(r'\\\{([\d,]+)\\\}',cols[4])[1].split(',')))
    matches=[x for x in records if x['degree']==n and x['catalogue_index']==i and x['type']==typ]
    need(matches,'literal acquired tuple for every printed row')
    for x in matches:
        need(all(sorted(g)==list(range(1,n+1))for g in x['marks']),'permutation arrays')
        need([order(comp(a,b))for a,b in zip(x['marks'],x['marks'][1:])]==typ,'literal finite type')
    alltypes=sorted(set(tuple(x['type'])for x in records if x['degree']==n and x['catalogue_index']==i))
    table6.append({'row':len(table6)+1,'degree':n,'catalogue_index':i,'structure_source_tex':cols[2],'order':o,'printed_type':typ,'matching_acquired_tuples':matches,'all_ordered_types_for_group':alltypes,'proof_input':'Complete accepted L047 transitive classification, actual small_transitive.g census and all literal representatives. Abstract identification and full intersection property are acquired there, not inferred from order.','qualification':'For degree6/index11 the complete ordered list also contains [2,4,3] and reversals; the printed table does not exhaust ordered Schlaefli types.'if (n,i)==(6,11)else 'Printed group and type agree with the acquired literal representatives.'})
need(len(table6)==4,'four exact finite rows')
out={'status':'PASS_EXACT_TABLE_INTERFACES','bindings':[pin(src),pin(p)],'table4':families,'table4_literal_controls':controls,'table6':table6,'scope':'Interfaces to acquired or explicitly attributed theorems. No new complete census or infinite construction proof is claimed by these finite controls.'}
(W/'table_interfaces01.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'infinite_families':len(families),'literal_rank_controls':len(controls),'finite_rows':len(table6)}))
