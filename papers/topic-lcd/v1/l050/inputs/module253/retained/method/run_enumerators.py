#!/usr/bin/env python3
"""Run complete enumerations and derive dual enumerators by MacWilliams identity."""
import argparse,hashlib,json,math,subprocess,time
from pathlib import Path


def dual_counts(weights,n,k):
    q=3**k;answer=[]
    for j in range(n+1):
        total=0
        for i,coefficient in enumerate(weights):
            if not coefficient:continue
            value=sum((-1)**s*2**(j-s)*math.comb(i,s)*math.comb(n-i,j-s)
                      for s in range(max(0,j-(n-i)),min(i,j)+1))
            total+=coefficient*value
        if total%q or total<0:raise RuntimeError('MacWilliams integrality or positivity')
        answer.append(total//q)
    if sum(answer)!=3**(n-k)or answer[0]!=1:raise RuntimeError('dual size')
    return answer


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--exe',type=Path,required=True);ap.add_argument('--bases',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    if a.out.exists():raise RuntimeError('fresh output required')
    a.out.mkdir(parents=True);inputs=json.loads((a.bases/'report.json').read_text());results={}
    order=['105_adjacency','105_differences','120_adjacency','120_differences','176_adjacency','253_adjacency','253_differences']
    for label in order:
        basis=a.bases/(label+'.txt');raw=basis.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=inputs[label]['sha256']:raise RuntimeError('changed basis')
        print('Running '+label,flush=True);start=time.monotonic()
        with(a.out/(label+'.json')).open('w')as stdout,(a.out/(label+'.log')).open('w')as stderr:
            r=subprocess.run([str(a.exe),str(basis)],stdout=stdout,stderr=stderr)
        if r.returncode:raise RuntimeError('enumerator failed '+label)
        elapsed=time.monotonic()-start;result=json.loads((a.out/(label+'.json')).read_text())
        n,k=inputs[label]['length'],inputs[label]['dimension'];weights=result['weight_counts']
        if result['length']!=n or result['basis_rows']!=k or result['coefficient_vectors']!=3**k or sum(weights)!=3**k or weights[0]!=1:raise RuntimeError('complete enumeration count')
        if any(x%2 for x in weights[1:]):raise RuntimeError('nonzero scalar pairs')
        dual=dual_counts(weights,n,k);distance=next(i for i in range(1,n+1)if weights[i]);dual_distance=next(i for i in range(1,n+1)if dual[i])
        results[label]={'n':n,'k':k,'d':distance,'minimum_words':weights[distance],'dual_d':dual_distance,'dual_minimum_words':dual[dual_distance],'seconds':elapsed,'basis_sha256':inputs[label]['sha256'],'enumeration_sha256':hashlib.sha256((a.out/(label+'.json')).read_bytes()).hexdigest(),'dual_weight_counts':dual}
        (a.out/'progress.json').write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps({k:v for k,v in results[label].items()if k!='dual_weight_counts'}),flush=True)
    report={'status':'ALL_SEVEN_COMPLETE_ENUMERATIONS','executable_sha256':hashlib.sha256(a.exe.read_bytes()).hexdigest(),'results':results,'limits':'Exact finite computational results; independent enumeration/source-value review and full proof/formal attribution remain separate.'}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
