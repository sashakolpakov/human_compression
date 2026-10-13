from pathlib import Path
import argparse,hashlib,json,subprocess,time

p=argparse.ArgumentParser()
p.add_argument('--degree',type=int,required=True)
p.add_argument('--run',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
p.add_argument('--seconds',type=int,default=1200)
a=p.parse_args()
S=Path(__file__).resolve().parent.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report=json.loads((a.run/'report.json').read_text())
assert report['returncode']==0 and report['complete_marker'] and report['unchanged']
assert report['degree']==a.degree
log=a.run/'stdout.log';src=log.read_text()
assert src.count('COMPLETE_EXHAUSTION')==1
def bracket(after):
    start=src.index('[',src.index(after)+len(after));depth=0
    for end in range(start,len(src)):
        if src[end]=='[':depth+=1
        elif src[end]==']':depth-=1
        if depth==0:return src[start:end+1]
    raise ValueError('unclosed list')
a.out.mkdir(parents=True,exist_ok=False)
checks=S/'corpus106_F002_recovery_v1/checks.g'
(a.out/'checks.g').write_bytes(checks.read_bytes())
lines=['recordedInvolutions:='+bracket('INVOLUTIONS_LITERAL')+';;','recordedMarks:=[];;']
for rank in range(3,report['rank_limit']+1):
    lines.append(f'recordedMarks[{rank}]:='+bracket(f'COMPLETE_MARKS_RANK_{rank} ')+';;')
(a.out/'records.g').write_text('\n'.join(lines)+'\n')
code='''Read("checks.g");;Read("records.g");;
Ambient:=AlternatingGroup(degree);; total:=0;; altTotal:=0;;
if 2^(rankLimit+1)<=Size(Ambient) then Error("incomplete rank limit");fi;
for rank in [3..rankLimit] do
 counts:=[];;altCount:=0;;
 for ids in recordedMarks[rank] do
  t:=List(ids,i->recordedInvolutions[i]);;
  if Length(t)<>rank or not ForAll(t,x->Order(x)=2 and x in Ambient) then Error("marks");fi;
  for i in [1..rank] do for j in [i+2..rank] do
   if Comm(t[i],t[j])<>() then Error("string");fi;
  od;od;
  if not FullIP(t) then Error("full subset IP");fi;
  H:=Group(t);;
  if not IsTransitive(H,[1..degree]) then Error("transitivity");fi;
  Add(counts,Size(H));total:=total+1;
  if H=Ambient then altCount:=altCount+1;altTotal:=altTotal+1;fi;
 od;
 Print("VALIDATED_RANK ",rank," ALTERNATING ",altCount," GROUP_ORDERS ",Collected(counts),"\\n");
od;
if FullIP([recordedInvolutions[1],recordedInvolutions[2],recordedInvolutions[1]]) then Error("repetition control");fi;
Print("ALL_RECORDS_FULL_SUBSET_IP_PASS DEGREE ",degree," TOTAL ",total," ALTERNATING ",altTotal,"\\n");
Print("COMPLETE_VALIDATION\\n");QUIT;
'''
(a.out/'validate.g').write_text(code)
pins=[{'path':str(x.resolve()),'sha256':sha(x)} for x in
      [Path(__file__),checks,log,a.run/'report.json',a.out/'records.g',a.out/'validate.g']]
cmd=['/opt/homebrew/bin/gap','-q','-b','-c',
     f'degree:={a.degree};rankLimit:={report["rank_limit"]};Read("validate.g");']
start=time.monotonic()
with (a.out/'stdout.log').open('wb')as so,(a.out/'stderr.log').open('wb')as se:
    q=subprocess.Popen(cmd,cwd=a.out,stdout=so,stderr=se)
    (a.out/'pid').write_text(str(q.pid)+'\n')
    try:rc=q.wait(timeout=a.seconds);status='EXITED'
    except subprocess.TimeoutExpired:q.kill();q.wait();rc=None;status='TIMEOUT_NO_CERTIFICATE'
r={'status':status,'returncode':rc,'seconds':time.monotonic()-start,
   'complete_marker':'COMPLETE_VALIDATION' in (a.out/'stdout.log').read_text(),
   'pins':pins,'unchanged':all(sha(Path(x['path']))==x['sha256']for x in pins),
   'whole_original_credit':0,'GAP_exact_operations_are_software_premises':True}
(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items()if k!='pins'}))
