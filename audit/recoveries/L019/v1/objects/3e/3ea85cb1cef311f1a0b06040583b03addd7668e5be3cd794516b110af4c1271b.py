import argparse
import json
from pathlib import Path
import sys
if sys.flags.optimize:
    raise SystemExit('optimized Python is unsupported')
from permutation_library import parse_marks, centralizer_fixing, multiply, need

def orbits(marks):
    unused=set(range(len(marks[0]))); result=[]
    while unused:
        seed=min(unused); seen={seed}; todo=[seed]
        while todo:
            a=todo.pop()
            for p in marks:
                if p[a] not in seen:
                    seen.add(p[a]);todo.append(p[a])
        unused-=seen;result.append(sorted(x+1 for x in seen))
    return result

def run(data):
    aa=data['a11_rank_six'];ss=data['s8_rank_six']
    need(len(aa)==4 and len(ss)==2,'incomplete literal roster')
    need([r['source_index'] for r in aa]==list(range(4)),'wrong A11 indices')
    need([r['source_index'] for r in ss]==list(range(2)),'wrong S8 indices')
    ee=data['small_extremal'];need([row['n'] for row in ee]==[5,6,6],'wrong small extremal roster')
    aout=[];sout=[];eout=[]
    for row in aa:
        tt=parse_marks(row,11,6)
        for rev in [False,True]:
            t=tt[::-1] if rev else tt
            # A new globally fixed point converts the unrestricted centralizer
            # to the already acquired exact point-fixing centralizer routine.
            cc=centralizer_fixing([p+(11,) for p in t[1:]],11)
            need(cc==[tuple(range(12))],'A11 suffix centralizer is not trivial')
            aout.append({'source_index':row['source_index'],'reverse':rev,
                         'centralizer_order':len(cc),'tail_orbits':orbits(t[1:])})
    for row in ss:
        t=parse_marks(row,8,6)
        for j in range(6):
            oo=orbits(t[:j]+t[j+1:])
            need(len(oo)>1,'S8 maximal omission is transitive')
            sout.append({'source_index':row['source_index'],'omitted':j,'orbits':oo})
    for index,row in enumerate(ee):
        n=row['n'];t=parse_marks(row,n,n-1);ident=tuple(range(n))
        for j in range(n-2):
            p=multiply(t[j],t[j+1]);need(p!=ident and multiply(multiply(p,p),p)==ident,'not a simplex type')
        oo=[orbits(t[:j]+t[j+1:]) for j in range(n-1)]
        if index<2:need(all(len(o)>1 for o in oo),'standard small action lacks fracture')
        else:need(len(oo[0])==1 and len(oo[-1])==1,'outer action qualification not demonstrated')
        eout.append({'source_index':index,'n':n,'omission_orbits':oo})
    return {'status':'PASS_INITIAL_FRACTURE_BOUNDARIES','a11':aout,'s8':sout,'small':eout,
            'scope':'Filtering complete acquired tuple lists, not a new census.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,default=Path(__file__).with_name('inputs.json'));ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();report=run(json.loads(args.input.read_text()))
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
if __name__=='__main__':main()
