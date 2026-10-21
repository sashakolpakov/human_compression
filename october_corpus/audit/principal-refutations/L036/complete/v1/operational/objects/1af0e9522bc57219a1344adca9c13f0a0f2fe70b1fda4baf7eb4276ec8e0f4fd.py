"""Literal join to acquired subgroup arrays, independent of discovery parsing."""
import argparse, hashlib, itertools, json, re
from pathlib import Path

W=Path(__file__).resolve().parent;B=W.parent;D=B/'data_intake'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def read(p):return json.loads(p.read_text())
def verify_pin(row):
 b=Path(row['path']).read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'acquired source pin')

def m11_generators(text):
 # This token parser accepts only the saved literal array grammar, without
 # evaluating GAP or importing discovery's regular-expression parser.
 need(text.count('verifiedSubgroups:=')==1,'one literal subgroup array')
 s=text.split('verifiedSubgroups:=')[1].split(';;')[0]
 tokens=re.findall(r'Group|[0-9]+|[(),\[\]]|\S',s);i=0
 def eat(token):
  nonlocal i
  need(i<len(tokens) and tokens[i]==token,'expected '+token);i+=1
 def perm():
  nonlocal i
  p=list(range(11));seen=set();cycles=0
  while i<len(tokens) and tokens[i]=='(':
   cycles+=1;eat('(');cycle=[]
   if tokens[i]!=')':
    while True:
     need(tokens[i].isdigit(),'cycle integer');cycle.append(int(tokens[i])-1);i+=1
     if tokens[i]!=',':break
     eat(',')
   eat(')')
   need(all(0<=a<11 for a in cycle) and len(set(cycle))==len(cycle) and not seen.intersection(cycle),'disjoint literal cycles')
   seen.update(cycle)
   for a,b in zip(cycle,cycle[1:]+cycle[:1]):p[a]=b
  need(cycles>0,'literal permutation required');return p
 eat('[');groups=[]
 while tokens[i]!=']':
  eat('Group');eat('(')
  if tokens[i]=='[':
   eat('[');gens=[]
   while tokens[i]!=']':
    gens.append(perm())
    if tokens[i]!=',':break
    eat(',')
   eat(']')
  else:gens=[perm()]
  eat(')');groups.append(gens)
  if tokens[i]!=',':break
  eat(',')
 eat(']');need(i==len(tokens) and len(groups)==39,'complete literal array')
 return groups

def source_join(records, assertions):
 ledger=read(B/'structural_labels_plan/pilot_ledger.json')['rows']
 need(len(ledger)==len(assertions)==len(records)==24,'exact pilot roster')
 source={(r['table'],r['row']):r for r in ledger};need(len(source)==24,'unique source rows')
 m11=m11_generators((B/'numeric_work/m11_literal02/groups.g').read_text())
 # Enumerate the 60 even permutations of five points directly, not a group
 # closure or any ambient subgroup census. The retained array uses this order.
 a5=[list(p) for p in itertools.permutations(range(5)) if sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2==0]
 need(len(a5)==60,'literal alternating model')
 a5rows=read(B/'method_v1/author_check/controls/A5_subgroups.json')
 maps={};tables={}
 for name,prefix in [('alt5','a5'),('m11','m11')]:
  comparison=read(D/f'{prefix}_numeric_comparison.json')
  verify_pin(comparison['source_table']);verify_pin(comparison['computation'])
  maps[name]=comparison['mapping_source_to_computation']
  table=read(D/f'parsed/{name}/table.json')
  tables[name]={r['row']:r for r in table['rows']}
 checked=[]
 for a in assertions:
  key=a['table'],a['row'];r=records[key];l=source[key];literal=tables[key[0]][key[1]]
  need({k:a[k] for k in l}==l and r['source']==l,'native ledger join')
  need(l['actual_record']==maps[key[0]][str(key[1])],'accepted source-row bijection')
  need(l['order']==literal['order'] and ''.join(l['flat_literal'].split())==''.join(literal['structure_literal'].split()),'literal source label/order')
  if key[0]=='alt5':expected=[a5[i] for i in a5rows[l['actual_record']-1]['h']]
  else:expected=m11[l['actual_record']-1]
  need(r['permutation_generators']==expected,'exact acquired actual subgroup generators')
  checked.append(dict(table=key[0],row=key[1],actual_record=l['actual_record'],generators=len(expected),native_page=l['page']))
 return dict(status='PASS',literal_array_joins=len(checked),m11_array_entries_parsed=len(m11),a5_even_permutations=len(a5),rows=checked,ambient_censuses=0)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 assertions=read(W/'native_assertions.json')['assertions'];records={(s['table'],s['row']):read(W/f"discovery01/{s['table']}_{s['row']}.json") for s in assertions}
 result=source_join(records,assertions);need(not a.out.exists(),'fresh report');a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
