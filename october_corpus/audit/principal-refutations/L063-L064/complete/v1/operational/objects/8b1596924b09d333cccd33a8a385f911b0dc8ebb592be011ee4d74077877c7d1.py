"""Verify the displayed thirty-point permutation by literal incidence."""
from pathlib import Path
import argparse,itertools,json,re
def check(source):
 d=json.loads(source.read_text());points=[list(x)for x in itertools.combinations(range(1,7),2)]
 lines=[]
 for triple in itertools.combinations(points,3):
  if sorted(sum(triple,[]))==list(range(1,7)):lines.append([list(x)for x in triple])
 lines.sort()
 if d['duads']!=points or d['synthemes']!=lines:raise ValueError('literal ordered objects')
 f=d['duality']
 if len(f)!=30 or any(type(x)is not int for x in f)or sorted(f)!=list(range(30)):raise ValueError('permutation')
 if any(f[f[i]]!=i for i in range(30)):raise ValueError('involution')
 if any((i<15)==(f[i]<15)for i in range(30)):raise ValueError('must reverse both types')
 edges={frozenset((i,15+j))for i,x in enumerate(points)for j,y in enumerate(lines)if x in y}
 if len(edges)!=45 or {frozenset(f[i]for i in e)for e in edges}!=edges:raise ValueError('all45incidences preserved')
 return {'status':'PASS_LITERAL_DUALITY','vertices':30,'edges':45,'type_reversed':True,'group_order_searches':0}
def check_table(source,tex):
 d=json.loads(source.read_text());rows=re.findall(r'([1-6]{2})&\$([1-6]{2}\|[1-6]{2}\|[1-6]{2})\$',tex.read_text())
 if len(rows)!=15 or len(set(a for a,b in rows))!=15:raise ValueError('fifteen unique displayed rows')
 for a,b in rows:
  i=d['duads'].index(list(map(int,a)));want='|'.join(''.join(map(str,x))for x in d['synthemes'][d['duality'][i]-15])
  if b!=want:raise ValueError('displayed witness differs')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path(__file__).with_name('duality.json'));p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=check(a.input)
 for kind in ['duplicate','type','edge','boolean']:
  d=json.loads(a.input.read_text())
  if kind=='duplicate':d['duality'][0]=d['duality'][1]
  elif kind=='type':d['duality']=list(range(30))
  elif kind=='edge':d['duality'][0],d['duality'][1]=d['duality'][1],d['duality'][0]
  else:d['duality'][0]=True
  bad=a.out.with_name(a.out.stem+'_'+kind+'.json');bad.write_text(json.dumps(d))
  try:check(bad)
  except ValueError:pass
  else:raise AssertionError('damaged witness accepted:'+kind)
 check_table(a.input,Path(__file__).with_name('doily.tex'))
 r.update(rejected_damages=4,displayed_rows=15);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
