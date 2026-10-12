#!/usr/bin/env python3
"""Optional bounded validation; no uniform classification premise."""
import argparse,json,subprocess,tempfile
from pathlib import Path

def require(c,m):
 if not c:raise ValueError(m)
def run(exe):
 samples=sorted(set([2,8,32,512,2**27,2**32-1,2**32,2**32+1,10**10]+[10**10-((10**10-8)%24)-24*i for i in range(100)]))
 p=subprocess.run([str(exe)],input='\n'.join(map(str,samples))+'\n',text=True,capture_output=True,check=True)
 rows=[list(map(int,x.split())) for x in p.stdout.splitlines()]
 require(len(rows)==len(samples),'probe row count')
 for n,(m,v,z) in zip(samples,rows):
  require(n==m and v==n*n+n+1 and z==pow(2,n+1,v),'GMP/Python disagreement')
 survivors=[m for m in range(8,10**6+1,24) if m&(m-1) and pow(2,m+1,m*m+m+1)==1]
 require(not survivors,'unsieved million-bound survivor')
 # A polynomial equal to a sieve prime must not be discarded as composite.
 equality=[m for m in range(8,10001,24) if m*m+m+1 in {73,3817}]
 require(8 in equality,'prime-polynomial equality control')
 # The upper endpoint is not a member of the residue progression.
 last=8+24*((10**10-8)//24)
 require(last<=10**10<last+24 and (10**10-8)//24+1==416666667,'inclusive endpoint')
 require(max(v.bit_length() for _,v,_ in rows)==67,'67-bit modulus boundary')
 return {'status':'PASS','GMP_Python_samples':len(rows),'modulus_max_bits':67,'unsieved_upper':10**6,'unsieved_survivors':survivors,'last_admissible_m':last,'equal_prime_m8_retained':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--probe',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run(a.probe);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
