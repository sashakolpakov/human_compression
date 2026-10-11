#!/usr/bin/env python3
"""Exact mathematical columns of the revised BLT timing table; no timing claim."""
import argparse,json,math,pathlib
from fractions import Fraction

def need(ok,msg):
    if not ok:raise RuntimeError('PHASE282_REJECT '+msg)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh output')
    rows=[]
    for family,params in [('PSL3',[2,3,4,5,7,8,9,11,13,16,17,19]),('PSU3',[2,3,4,5,7,8,9,11]),('Alt',range(5,11)),('Sym',range(5,11))]:
        for q in params:
            if family=='PSL3':
                order=q**3*(q**3-1)*(q*q-1)//math.gcd(3,q-1)
                inv=q*q*(q*q+q+1) if q%2 else (q**3-1)*(q+1)
            elif family=='PSU3':
                order=q**3*(q**3+1)*(q*q-1)//math.gcd(3,q+1)
                inv=q*q*(q*q-q+1) if q%2 else (q**3+1)*(q-1)
            else:
                order=math.factorial(q)//(2 if family=='Alt' else 1)
                inv=sum(math.factorial(q)//(2**k*math.factorial(k)*math.factorial(q-2*k))
                        for k in range(1,q//2+1) if family=='Sym' or k%2==0)
            ratio=Fraction(inv,order)
            rows.append(dict(family=family,q=q,order=order,involutions=inv,ratio=str(ratio),decimal=float(ratio)))
    need(len(rows)==32,'all revised source rows')
    need(next(r for r in rows if (r['family'],r['q'])==('PSL3',17))['involutions']==88723,'PSL3(17) exact count')
    a.out.write_text(json.dumps(dict(status='PASS',rows=rows,scope='Exact group orders and involution counts; neither original timings nor a chiral census.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',rows=len(rows))))
if __name__=='__main__':main()
