"""Filter the complete acquired A10 rank-five list; no new census."""
import argparse,json,sys
from pathlib import Path
if sys.flags.optimize:raise SystemExit('optimized Python is unsupported')
from permutation_library import need,parse_marks,anchors,closure

def orbit(marks,a):
 seen={a};todo=[a]
 while todo:
  x=todo.pop()
  for p in marks:
   y=p[x]
   if y not in seen:seen.add(y);todo.append(y)
 return seen

def run(data):
 rows=data['representatives'];need(len(rows)==10,'incomplete census')
 need([r['source_index'] for r in rows]==list(range(10)),'wrong census indices')
 need(len({tuple(tuple(p) for p in r['permutations']) for r in rows})==10,'duplicate tuple')
 entries=[];survivors=[]
 expected={(1,0,10):[5040,5040,360,60],(2,1,1):[5040,5040,360,60],(4,1,1):[40320,10080,720,120],(7,0,10):[40320,10080,720,120]}
 for row in rows:
  marks=parse_marks(row,10,5)
  for rev in [0,1]:
   t=marks if rev==0 else marks[::-1];entry={'source_index':row['source_index'],'orientation':rev,'anchors':[a+1 for a in anchors(t)],'accepted':[]}
   for a in anchors(t):
    other=next(x for x in range(10) if x!=a)
    if orbit(t[1:],other)!=set(range(10))-{a}:continue
    extended=[p+(10,) for p in t];leaf=list(range(11));leaf[a],leaf[10]=10,a
    U=closure(extended[:4]);V=closure([tuple(leaf)]+extended[:3]);M=closure(extended[:3]);I=U&V
    need(M<=I,'middle inclusion');sizes=[len(U),len(V),len(I),len(M)];key=(row['source_index'],rev,a+1)
    need(key in expected and sizes==expected[key],'unexpected obstruction')
    need(len(I)==6*len(M),'index six')
    d={'source_index':row['source_index'],'orientation':rev,'anchor':a+1,'orders':sizes,'intersection_index':6}
    entry['accepted'].append(d);survivors.append(d)
   entries.append(entry)
 need(len(entries)==20 and len(survivors)==4,'wrong exhaustive filter')
 need({(r['source_index'],r['orientation'],r['anchor']) for r in survivors}==set(expected),'missing survivor')
 return {'status':'PASS_A10_ATTACHMENT_OBSTRUCTIONS','input_rows':10,'orientations':20,'entries':entries,'survivors':survivors,'new_census':False}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,default=Path(__file__).with_name('a10_inputs.json'));ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();report=run(json.loads(args.input.read_text()));args.out.write_text(json.dumps(report,indent=2)+'\n');print('PASS_A10_ATTACHMENT_OBSTRUCTIONS 20 orientations 4 exact index-six obstructions')
