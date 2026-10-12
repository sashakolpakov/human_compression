#!/usr/bin/env python3
"""Extract and certify exact row bases from our explicitly constructed graphs."""
import hashlib,itertools,json
from pathlib import Path
from check_graph_codes import graph105,steiner_blocks,rank_mod


def rref(rows,p=3):
    rows=[[x%p for x in row]for row in rows];k=0;pivots=[]
    for j in range(len(rows[0])):
        pivot=next((i for i in range(k,len(rows))if rows[i][j]),None)
        if pivot is None:continue
        rows[k],rows[pivot]=rows[pivot],rows[k];inv=pow(rows[k][j],-1,p)
        rows[k]=[x*inv%p for x in rows[k]]
        for i in range(len(rows)):
            if i!=k:
                c=rows[i][j];rows[i]=[(x-c*y)%p for x,y in zip(rows[i],rows[k])]
        pivots.append(j);k+=1
        if k==len(rows):break
    return rows[:k],pivots


def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    if a.out.exists():raise RuntimeError('fresh output required')
    a.out.mkdir(parents=True);blocks,_=steiner_blocks();graphs={105:graph105()}
    for j,n in [(0,253),(1,176),(2,120)]:
        selected=[b for b in blocks if b&((1<<j)-1)==0]
        graphs[n]=[[int(x!=y and(x&y).bit_count()!=1)for y in selected]for x in selected]
    report={}
    for n,mat in graphs.items():
        for name,rows in [('adjacency',mat),('differences',[[(x-y)%3 for x,y in zip(row,mat[0])]for row in mat[1:]])]:
            basis,pivots=rref(rows)
            # Each pivot coordinate gives the unique coefficient of a row-basis vector.
            for row in rows:
                recovered=[sum((row[pivots[i]]%3)*basis[i][j]for i in range(len(basis)))%3 for j in range(n)]
                if recovered!=[x%3 for x in row]:raise RuntimeError('row span certificate')
            for i,row in enumerate(basis):
                if [row[j]for j in pivots]!=[int(i==j)for j in range(len(basis))]:raise RuntimeError('independence certificate')
            label=f'{n}_{name}';text=f'{n} {len(basis)}\n'+''.join(''.join(map(str,row))+'\n'for row in basis)
            (a.out/(label+'.txt')).write_text(text)
            report[label]={'length':n,'dimension':len(basis),'pivots':pivots,'sha256':hashlib.sha256(text.encode()).hexdigest()}
            if n==105 and name=='adjacency':
                (a.out/'105_benchmark16.txt').write_text(f'{n} 16\n'+''.join(''.join(map(str,row))+'\n'for row in basis[:16]))
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
