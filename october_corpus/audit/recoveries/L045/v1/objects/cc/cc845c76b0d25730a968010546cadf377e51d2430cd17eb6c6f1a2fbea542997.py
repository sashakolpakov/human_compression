"""Independent roster orders and every printed numerical table entry."""
import sys
if sys.flags.optimize: raise RuntimeError('unoptimized review')
import json, math, re
from pathlib import Path
P=Path(__file__).resolve().parents[2]/'corpus106_L045_finite_lie_v1'
def need(x,s):
    if not x:raise ValueError(s)
rows=json.loads((P/'cases.json').read_text());checks=[]
for row in rows:
    a=row['parameters'];s=a[0]
    if s in ['L','U']:
        n,q=a[1:];e=1 if s=='L' else -1
        order=q**(n*(n-1)//2)*math.prod(q**i-e**i for i in range(2,n+1))//math.gcd(n,q-e)
    elif s in ['S','O']:
        n,q=a[1:];m=n//2
        order=q**(m*m)*math.prod(q**(2*i)-1 for i in range(1,m+1))//math.gcd(2,q-1)
    elif s in ['O+','O-']:
        n,q=a[1:];m=n//2;e=1 if s=='O+' else -1
        order=q**(m*(m-1))*(q**m-e)*math.prod(q**(2*i)-1 for i in range(1,m))//math.gcd(4,q**m-e)
    elif s=='G':
        q=a[2];order=q**6*(q**6-1)*(q*q-1)
    else:
        need(a==['T'],'only the Tits residue');order=17971200
    need(order==row['group_order'],'standard group order '+row['id'])
    checks.append(dict(id=row['id'],parameters=a,standard_order=order))
printed=[list(map(int,m)) for m in re.findall(r'&([0-9]+)&([0-9]+)&([0-9]+)&([0-9]+)\\\\',(P/'table.tex').read_text())]
need(printed==[row['orders'] for row in rows],'all 140 printed entries')
out=dict(status='PASS_INDEPENDENT_ORDER_AND_TABLE_CHECK',standard_order_checks=checks,printed_numeric_entries=140,
         scope='Supplementary formula and typography checks; named group identity remains the explicit acquired constructor/catalogue premise.')
(Path(__file__).parent/'independent.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
