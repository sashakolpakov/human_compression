import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not accepted')
from pathlib import Path
import hashlib,json,subprocess,time
W=Path(__file__).resolve().parent;S=W.parents[1];src=S/'reboot_20261013/F004_recovery_work/enumerate_ends_v2.g';t=src.read_text();a=t.index('CheckString:=function');b=t.index('MakePool:=function');functions=t[a:b]
(W/'partial_functions.g').write_text(functions)
body=r'''
G:=SymmetricGroup(4);;invs:=Filtered(Elements(G),x->Order(x)=2);;
FullIP:=function(t,selected)
 local subs,Hs,i,j;
 subs:=Combinations(selected);Hs:=List(subs,I->Group(Concatenation([()],t{I})));
 for i in [1..Length(subs)] do for j in [1..Length(subs)] do
  if Intersection(Hs[i],Hs[j])<>Group(Concatenation([()],t{Intersection(subs[i],subs[j])})) then return false;fi;
 od;od;return true;
end;;
cases:=0;;accepted:=0;;rejected:=0;;disconnected:=0;;
for selected in Filtered(Combinations([1..4]),I->Length(I)>0) do
 for marks in Tuples(invs,Length(selected)) do
  if Length(Set(marks))=Length(marks) then
   t:=[];;for i in [1..Length(selected)] do t[selected[i]]:=marks[i];od;
   string:=true;;for i in selected do for j in selected do
    if AbsInt(i-j)>1 and t[i]*t[j]<>t[j]*t[i] then string:=false;fi;
   od;od;
   if string then
    H:=Group(marks);;
    got:=PartialC(t,selected,H);;want:=FullIP(t,selected);;
    if got<>want then Error("partial criterion mismatch");fi;
    cases:=cases+1;;if got then accepted:=accepted+1;else rejected:=rejected+1;fi;
    if Length(selected)>1 and Length(selected)<>Maximum(selected)-Minimum(selected)+1 then disconnected:=disconnected+1;fi;
   fi;
  fi;
 od;
od;
if cases=0 or accepted=0 or rejected=0 or disconnected=0 then Error("nonvacuous oracle");fi;
Print("PARTIAL_CRITERION_ALL_CASES ",cases," ACCEPTED ",accepted," REJECTED ",rejected," DISCONNECTED ",disconnected,"\n");
Print("COMPLETE_PARTIAL_ORACLE\n");QUIT;
'''
p=W/'partial_oracle.g';p.write_text(functions+body);start=time.monotonic();r=subprocess.run(['/opt/homebrew/bin/gap','-q','-b',str(p)],capture_output=True,timeout=60);(W/'partial_oracle.stdout').write_bytes(r.stdout);(W/'partial_oracle.stderr').write_bytes(r.stderr)
if r.returncode or r.stderr or r.stdout.count(b'COMPLETE_PARTIAL_ORACLE')!=1:raise ValueError('oracle failed')
report=dict(status='PASS_INDEPENDENT_FULL_SUBSET_COMPARISON',seconds=time.monotonic()-start,source=str(src),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),exact_extracted_functions_sha256=hashlib.sha256(functions.encode()).hexdigest(),stdout=r.stdout.decode(),subprocess_returncode=r.returncode,census_credit=0)
(W/'partial_oracle_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
