from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,time
p=argparse.ArgumentParser();p.add_argument('--model',required=True)
p.add_argument('--old',type=Path,required=True);p.add_argument('--new',type=Path,required=True)
p.add_argument('--out',type=Path,required=True);a=p.parse_args()
W=Path(__file__).resolve().parent;S=W.parent
a.out.mkdir(parents=True,exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bracket(s,marker):
    start=s.index('[',s.index(marker)+len(marker));depth=0
    for end in range(start,len(s)):
        if s[end]=='[':depth+=1
        elif s[end]==']':depth-=1
        if depth==0:return s[start:end+1]
    raise ValueError('unclosed list')
old=(a.old/'stdout.log').read_text();new=(a.new/'stdout.log').read_text()
for folder,raw in [(a.old,old),(a.new,new)]:
    r=json.loads((folder/'report.json').read_text())
    assert r['returncode']==0 and r.get('complete_marker',r.get('complete',False)) and r['unchanged']
    assert raw.count('COMPLETE_EXHAUSTION')==1
oldr=list(map(int,re.findall(r'COMPLETE_MARKS_RANK_(\d+)',old)))
newr=list(map(int,re.findall(r'COMPLETE_TUPLES_RANK_(\d+)',new)))
assert oldr==newr==list(range(1,max(oldr)+1))
def counts(raw,mark):
    return [re.sub(r'\s+',' ',x).strip() for x in
            re.findall(r'RANK \d+ ordered .*?(?='+mark+r')',raw,re.S)]
assert counts(old,'COMPLETE_MARKS_RANK_')==counts(new,'COMPLETE_TUPLES_RANK_')
lines=['ivs:='+bracket(old,'INVOLUTIONS_LITERAL')+';;','oldMarks:=[];;newMarks:=[];;']
for rank in oldr:
    lines.append(f'oldMarks[{rank}]:='+bracket(old,f'COMPLETE_MARKS_RANK_{rank} ')+';;')
    lines.append(f'newMarks[{rank}]:='+bracket(new,f'COMPLETE_TUPLES_RANK_{rank} ')+';;')
(a.out/'records.g').write_text('\n'.join(lines)+'\n')
shutil.copy2(W/(a.model+'_model.g'),a.out/'model.g')
shutil.copy2(S/'corpus106_F002_recovery_v1/checks.g',a.out/'checks.g')
code='''Read("model.g");;Read("records.g");;Read("checks.g");;
total:=0;;
for rank in [1..Length(oldMarks)] do
 oldTuples:=List(oldMarks[rank],ids->List(ids,i->ivs[i]));;
 if Length(oldTuples)<>Length(newMarks[rank]) then Error("count");fi;
 used:=[];;
 for t in newMarks[rank] do
  if Group(t)<>G or not FullIP(t) then Error("new marking generation or IP");fi;
  if not ForAll(t,x->Order(x)=2) then Error("involution");fi;
  for i in [1..rank] do for j in [i+2..rank] do
   if Comm(t[i],t[j])<>() then Error("string");fi;
  od;od;
  found:=false;;
  for j in [1..Length(oldTuples)] do
   if not j in used then
    h:=RepresentativeAction(A,t,oldTuples[j],OnTuples);;
    if h<>fail then
     if not h in A or List(t,x->x^h)<>oldTuples[j] then Error("transport witness");fi;
     Add(used,j);found:=true;break;
    fi;
   fi;
  od;
  if not found then Error("missing unused old orbit");fi;
 od;
 if Set(used)<>[1..Length(oldTuples)] then Error("coverage");fi;
 total:=total+Length(used);
 Print("RANK_ORBIT_BIJECTION ",rank," ",Length(used),"\n");
od;
Print("COMPLETE_LITERAL_ORBIT_BIJECTION_AND_FULL_IP ",total,"\n");QUIT;
'''
# Preserve GAP's literal newline escape inside string constants.
code=code.replace('"\n"','"\\n"')
(a.out/'compare.g').write_text(code)
pins=[{'path':str(x.resolve()),'sha256':sha(x)}for x in
      [Path(__file__),a.old/'stdout.log',a.new/'stdout.log',a.out/'records.g',a.out/'model.g',a.out/'checks.g',a.out/'compare.g']]
t=time.monotonic()
with(a.out/'stdout.log').open('wb')as so,(a.out/'stderr.log').open('wb')as se:
    q=subprocess.Popen(['/opt/homebrew/bin/gap','-q','-b','compare.g'],cwd=a.out,stdout=so,stderr=se)
    try:rc=q.wait(timeout=600);status='EXITED'
    except subprocess.TimeoutExpired:q.kill();q.wait();rc=None;status='TIMEOUT_NO_CERTIFICATE'
r={'status':status,'returncode':rc,'seconds':time.monotonic()-t,
   'complete_marker':'COMPLETE_LITERAL_ORBIT_BIJECTION_AND_FULL_IP'in(a.out/'stdout.log').read_text(),
   'all_rank_and_duality_counts_match':True,'pins':pins,
   'unchanged':all(sha(Path(x['path']))==x['sha256']for x in pins),'whole_original_credit':0}
(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items()if k!='pins'}))
