#!/usr/bin/env python3
"""Separate coordinate oracle and dual calculation; imports no author Python."""
from pathlib import Path
import argparse,collections,hashlib,itertools,json,random,subprocess,importlib.util

def need(x,m):
 if not x:raise ValueError(m)
def code(rows,n):
 return [tuple(sum(t[i]*rows[i][j]for i in range(len(rows)))%3 for j in range(n))for t in itertools.product(range(3),repeat=len(rows))]
def histogram(words,n):
 c=collections.Counter(sum(x!=0 for x in w)for w in words);return[c[i]for i in range(n+1)]
def polynomial_transform(counts,n,k):
 # Direct repeated multiplication by (1+2z) and (1-z), no binomial formula.
 out=[0]*(n+1)
 for weight,c in enumerate(counts):
  if not c:continue
  poly=[1]
  for a,b in [(1,2)]*(n-weight)+[(1,-1)]*weight:
   nxt=[0]*(len(poly)+1)
   for j,v in enumerate(poly):nxt[j]+=a*v;nxt[j+1]+=b*v
   poly=nxt
  for j,v in enumerate(poly):out[j]+=c*v
 need(all(v%(3**k)==0 for v in out),'integral transform');return[v//(3**k)for v in out]
def main():
 p=argparse.ArgumentParser();p.add_argument('--author-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh out');a.out.mkdir(parents=True)
 src=a.author_root/'enumerate_ternary.c';exe=a.out/'enumerate_ternary';proc=subprocess.run(['/usr/bin/clang','-std=c11','-O2','-Wall','-Wextra','-Werror',str(src),'-o',str(exe)],capture_output=True,text=True);(a.out/'compile.txt').write_text(proc.stdout+proc.stderr);need(proc.returncode==0,'clean independent C compile')
 spec=importlib.util.spec_from_file_location('actual_dual_function_under_test',a.author_root/'run_enumerators.py');actual_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(actual_module)
 rng=random.Random(605015);cases=[]
 for n in[1,3,8,62,64,66,127,128,129,255,1023,1024]:
  for k in[0,1,4]:
   rows=[[rng.randrange(3)for _ in range(n)]for _ in range(k)];f=a.out/f'oracle_{n}_{k}.txt';f.write_text(f'{n} {k}\n'+''.join(''.join(map(str,row))+'\n'for row in rows));res=subprocess.run([str(exe),str(f)],check=True,capture_output=True,text=True);actual=json.loads(res.stdout);expected=histogram(code(rows,n),n);need(actual['weight_counts']==expected and actual['coefficient_vectors']==3**k,'coordinate oracle');cases.append({'n':n,'coefficient_rows':k,'vectors':3**k,'actual_rank_assumed':False})
 invalid={'zero_n':'0 0\n','too_long':'1025 0\n','too_many_rows':'4 40\n','bad_field':'3 1\n013\n','short_row':'3 1\n01\n','extra':'2 0\n0\n'};controls=[]
 for key,value in invalid.items():
  f=a.out/(key+'.txt');f.write_text(value);res=subprocess.run([str(exe),str(f)],capture_output=True,text=True);need(res.returncode!=0,'bad input rejected '+key);controls.append(key)
 duals=[]
 for n in range(1,8):
  for k in range(min(4,n)+1):
   # Explicit systematic rows certify independence; direct orthogonal enumeration.
   rows=[[int(i==j)if j<k else rng.randrange(3)for j in range(n)]for i in range(k)];words=code(rows,n);w=histogram(words,n)
   orth=[z for z in itertools.product(range(3),repeat=n)if all(sum(z[j]*r[j]for j in range(n))%3==0 for r in rows)]
   d=histogram(orth,n);need(polynomial_transform(w,n,k)==d,'full exact dual coordinate oracle');need(actual_module.dual_counts(w,n,k)==d,'actual author dual function against direct orthogonal enumeration');duals.append({'n':n,'k':k,'codewords':len(words),'dualwords':len(orth)})
 # Truth table of the very same Boolean expressions, checked in coordinates.
 truth=[]
 for x,y in itertools.product(range(3),repeat=2):
  a1=int(x==1);a2=int(x==2);b1=int(y==1);b2=int(y==2);az=1-a1-a2;bz=1-b1-b2
  one=(az&b1)|(a1&bz)|(a2&b2);two=(az&b2)|(a2&bz)|(a1&b1);need(one+2*two==(x+y)%3 and not(one&two),'plane identity');truth.append([x,y,one+2*two])
 r={'status':'PASS_BOUNDED_INDEPENDENT_METHOD_ORACLES','author_c_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'private_executable_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'coordinate_cases':cases,'dual_cases':duals,'truth_table':truth,'rejected_inputs':controls,'full_author_enumerations_restarted':False,'author_python_used_for_expected_values':False,'actual_author_function_under_test':'run_enumerators.dual_counts','full_rank23_run_certified':False};(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'coordinate_cases':len(cases),'dual_cases':len(duals),'truth_table_rows':9,'controls':len(controls)}))
if __name__=='__main__':main()
