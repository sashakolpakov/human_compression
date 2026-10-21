#!/usr/bin/env python3
"""Compare the packed C enumerator with independent coordinate arithmetic."""
import argparse,collections,hashlib,itertools,json,random,subprocess,time
from pathlib import Path


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--exe',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    if a.out.exists():raise RuntimeError('fresh output required')
    a.out.mkdir(parents=True);rng=random.Random(710531);cases=[]
    for n in [1,2,7,63,64,65,105,253]:
        for k in [0,1,5]:
            rows=[[rng.randrange(3)for _ in range(n)]for _ in range(k)]
            path=a.out/f'basis_{n}_{k}.txt';path.write_text(f'{n} {k}\n'+''.join(''.join(map(str,r))+'\n'for r in rows))
            counts=collections.Counter()
            for coeff in itertools.product(range(3),repeat=k):
                word=[sum(c*rows[i][j]for i,c in enumerate(coeff))%3 for j in range(n)]
                counts[sum(x!=0 for x in word)]+=1
            r=subprocess.run([str(a.exe),str(path)],check=True,capture_output=True,text=True)
            result=json.loads(r.stdout)
            if result['weight_counts']!=[counts[i]for i in range(n+1)]or result['coefficient_vectors']!=3**k:raise RuntimeError('oracle mismatch')
            cases.append({'n':n,'k':k,'vectors':3**k})
    start=time.monotonic();r=subprocess.run([str(a.exe),'/private/tmp/lcd_bases01/105_benchmark16.txt'],check=True,capture_output=True,text=True);elapsed=time.monotonic()-start
    benchmark=json.loads(r.stdout);(a.out/'benchmark.json').write_text(r.stdout)
    report={'status':'PASS_INDEPENDENT_COORDINATE_ORACLE','cases':cases,'executable_sha256':hashlib.sha256(a.exe.read_bytes()).hexdigest(),'benchmark_vectors':3**16,'benchmark_seconds':elapsed,'estimate_full_rank20_seconds':elapsed*81,'note':'Benchmark basis is only a16dimensional subcode; not a source-code enumerator.'}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
