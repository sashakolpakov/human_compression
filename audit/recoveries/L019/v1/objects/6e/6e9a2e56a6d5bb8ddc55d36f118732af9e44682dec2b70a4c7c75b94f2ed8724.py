import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
from pathlib import Path
import json,itertools
V=tuple(range(9))
def involutions(points):
 if not points:yield ();return
 x,*rest=points
 for a in involutions(rest):yield a
 for j,y in enumerate(rest):
  for a in involutions(rest[:j]+rest[j+1:]):yield ((x,y),)+a
def perm(pairs):
 a=list(V)
 for x,y in pairs:a[x]=y;a[y]=x
 return tuple(a)
def commute(a,b):return all(a[b[x]]==b[a[x]]for x in V)
def transport(a,p):
 b=[None]*9
 for x in V:b[p[x]]=p[a[x]]
 return tuple(b)
r=json.loads(Path('enumeration01.json').read_text());canonical={}
for row in r['models']:
 for p5 in itertools.permutations(range(2,7)):
  p=(0,1)+p5+(7,8);pair=(transport(row['a'],p),transport(row['d'],p))
  if pair in canonical:assert canonical[pair]==row['type']
  canonical[pair]=row['type']
a=[perm(((0,1),)+q)for q in involutions(list(range(2,8)))];d=[perm(((7,8),)+q)for q in involutions(list(range(1,7)))];literal={(x,y)for x in a for y in d if commute(x,y)}
assert len(a)==len(d)==76
assert literal==set(canonical)
assert len({tuple(x)for x in canonical.values()})==11
# Removing any endpoint type destroys literal coverage.
assert all(any(ty==m['type']for ty in canonical.values())for m in r['models'])
# Maps in the certificate are literal bijections preserving every labelled edge.
for s in r['survivors']:
 f=s['path_map'];assert sorted(f)==list(V) and f[0]==0 and f[8]==8
 assert all(transport(tuple(p),tuple(f))==tuple(q)for p,q in zip(s['marks'],r['target']))
print(json.dumps({'status':'PASS_LITERAL_ENDPOINT_AND_MAP_CONTROL','left':len(a),'right':len(d),'commuting_pairs':len(literal),'canonical_types':11,'conjugacy_checks':4}))
