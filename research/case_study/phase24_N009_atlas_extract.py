#!/usr/bin/env python3
"""Parse a primary Atlas snapshot as data; do not execute downloaded GAP text."""
import hashlib,json,re
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
plan=json.loads((ROOT/'phase24_N009_atlas_fetch_plan.json').read_text())
records=[]
for p in plan:
 order=int(re.search(r'\*(\d+)',p['label'])[1])
 if order&(order-1):continue
 path=ROOT/'sources'/Path(p['path']).name
 raw=path.read_bytes();soup=BeautifulSoup(raw,'html.parser')
 blocks=[x.get_text() for x in soup.find_all('pre')]
 block=next(x for x in blocks if re.search(r's0\s*:=\s*\(',x) and 'Sym(' not in x)
 perms=[]
 for i in range(3):
  expr=re.search(rf's{i}\s*:=\s*(.*?);;',block,re.S)[1]
  assert re.fullmatch(r'[\s\d,()]+',expr),expr
  cycles=[[int(z) for z in a.split(',')] for a in re.findall(r'\(([^()]*)\)',expr)]
  degree=max([z for c in cycles for z in c],default=0);perm=list(range(1,degree+1))
  flat=[z for c in cycles for z in c]
  assert len(flat)==len(set(flat)), 'Displayed cycles must be disjoint'
  for c in cycles:
   assert len(c)==len(set(c))
   for j,v in enumerate(c):perm[v-1]=c[(j+1)%len(c)]
  assert sorted(perm)==list(range(1,degree+1));perms.append(perm)
 fp=next(x for x in blocks if 'FreeGroup(' in x)
 rels=re.search(r'rels\s*:=\s*\[(.*?)\]',fp,re.S)[1]
 words=[]
 for expr in rels.split(','):
  assert re.fullmatch(r'\s*s[012](?:\s*\*\s*s[012])*\s*',expr),expr
  words.append([int(x)+1 for x in re.findall(r's([012])',expr)])
 # Canonical name independently appears in the page itself.
 assert p['label'] in soup.get_text()
 records.append(dict(label=p['label'],order=order,type=[int(x) for x in re.search(r'\{([^}]+)\}',p['label'])[1].split(',')],url=p['url'],primary_snapshot=path.name,primary_sha256=hashlib.sha256(raw).hexdigest(),permutations=perms,relator_words=words))
out=ROOT/'phase24_N009_atlas_library.json';out.write_text(json.dumps(records,indent=2)+'\n')
lines=['# Parsed mathematical data from Hartley Atlas, with primary URLs/hashes in JSON.','atlas24:=[];;']
for p in records:
 lines.append('Add(atlas24,rec(label:='+json.dumps(p['label'])+',order:='+str(p['order'])+',typ:='+str(p['type'])+',gens:=List('+str(p['permutations'])+',PermList),words:='+str(p['relator_words'])+'));;')
(ROOT/'phase24_N009_atlas_library.g').write_text('\n'.join(lines)+'\n')
print(json.dumps({'records':len(records),'library_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
