"""Documentary adapter: exact numeric rows from fixed L120 TeX, no source export."""
import sys
if sys.flags.optimize:raise RuntimeError('unoptimized execution required')
from pathlib import Path
import re,json,hashlib
W=Path(__file__).resolve().parent
p=W/'survey-final.tex';raw=p.read_bytes();src=raw.decode()
blocks=re.findall(r'\\begin\{table\}(.*?)\\end\{table\}',src,re.S)
if len(blocks)!=6:raise ValueError('six tables')
def num(s):
 s=s.strip().replace(',','')
 if not re.fullmatch('[0-9]+',s):raise ValueError(s)
 return int(s)
tables=[]
for i,b in enumerate(blocks,1):
 table={'table':i,'source_block_sha256':hashlib.sha256(b.encode()).hexdigest(),'rows':[]}
 if i in (1,3):
  group='S' if i==1 else 'A';ranks=list(range(3,14 if i==1 else 9))
  for line in b.splitlines():
   m=re.fullmatch(r'\$'+group+r'_(?:\{(\d+)\}|(\d+))\$&(.*?)\\\\',line.strip())
   if m:
    vals=[num(s) for s in m[3].split('&')]
    if len(vals)!=len(ranks):raise ValueError('column count')
    table['rows'].append({'group':group+str(int(m[1] or m[2])),'degree':int(m[1] or m[2]),'rank_counts':dict(zip(map(str,ranks),vals))})
  if len(table['rows'])!=(10 if i==1 else 11):raise ValueError('row count')
 elif i==2:
  for line in b.splitlines():
   m=re.fullmatch(r'([\d,]+)\s*&\s*(\d+)\s*&\s*(\d+)\\\\',line.strip())
   if m:table['rows'].append({'degrees':list(map(int,m[1].split(','))),'symmetric':int(m[2]),'alternating':int(m[3])})
  if len(table['rows'])!=14:raise ValueError('pair rows')
 elif i==5:
  for line in b.splitlines():
   if not line.strip().startswith('$') or 'Order' in line:continue
   vals=line.strip().removesuffix('\\\\').split('&')
   if len(vals)!=5:continue
   group=vals[0].strip().strip('$').replace('\\prime',"'").replace('{','').replace('}','').replace('_','').replace('^','').replace(' ','')
   counts=[None if x.strip()=='Unknown' else num(x) for x in vals[2:]]
   table['rows'].append({'group':group,'source_order':num(vals[1]),'rank_counts':dict(zip(('3','4','5'),counts))})
  if len(table['rows'])!=15:raise ValueError(('sporadic rows',table['rows']))
 else:
  table['disposition']='Two attributed2012 infinite construction diagrams' if i==4 else 'Four acquired L047 finite imprimitive rows, retaining both ordered wreath types'
 tables.append(table)
x={'status':'LITERAL_NUMERIC_TRANSCRIPTION_NOT_CENSUS_PROOF','primary_tex_sha256':hashlib.sha256(raw).hexdigest(),'tables':tables}
extra=json.loads((W/'table_interfaces01.json').read_text());tables[3]['rows']=extra['table4'];tables[5]['rows']=extra['table6']
(W/'survey_tables03.json').write_text(json.dumps(x,indent=2)+'\n');print([(x['table'],len(x['rows']))for x in tables])
