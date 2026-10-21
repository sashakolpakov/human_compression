"""Verify exported subgroup witnesses without loading TomLib or its enumerator.
This checks validity, not completeness or pairwise inequivalence of the catalogue.
"""
from pathlib import Path
import hashlib, json, os, shutil, subprocess
BASE = Path(__file__).resolve().parent
GAP = os.environ.get('GAP') or shutil.which('gap')
if not GAP:
    raise SystemExit('GAP was not found. Install GAP on PATH or set GAP to its executable path.')
header = r'''
KnownMaximalSubgroups:=[];;
VerifyWitness:=function(G,H,K,expected,need2T,needIP)
 local T,hh,a,b,x,c;
 T:=Intersection(H,K);
 if [Size(H),Size(K),Size(T)]<>expected then Error("order mismatch");fi;
 if not IsSubgroup(G,H) or not IsSubgroup(G,K) then Error("ambient containment");fi;
 if Size(ClosureGroup(H,K))<>Size(G) then Error("not connected");fi;
 if not ForAny(KnownMaximalSubgroups,M->Size(M)=Size(H) and RepresentativeAction(G,M,H,OnPoints)<>fail) then Error("global anchor not maximal");fi;
 if not IsPrimitive(Action(H,RightCosets(H,T),OnRight)) or not IsPrimitive(Action(K,RightCosets(K,T),OnRight)) then Error("local action not primitive");fi;
 if need2T then
  if Transitivity(Action(H,RightCosets(H,T),OnRight))<2 or Transitivity(Action(K,RightCosets(K,T),OnRight))<2 then Error("local action not two-transitive");fi;
 fi;
 if needIP then
  x:=First(GeneratorsOfGroup(K),x->not x in T);
  hh:=RightTransversal(H,T);
  a:=Set(List(hh,h->RightCoset(K,h)));
  b:=Set(List(hh,h->RightCoset(K,h*x)));
  c:=Length(Intersection(a,b));
  if c<>1 and Size(H)*Size(K)<>Size(G)*Size(T) then Error("IP2 fails");fi;
 fi;
end;;
'''
def group(gens):
    return 'Group([' + ','.join('PermList('+json.dumps(g)+')' for g in gens) + '])'
lines=[header]
files=[]
for name in ['J2','Sz8']:
    path=BASE/f'classification_{name}_representatives.json'
    data=json.loads(path.read_text()); files.append({'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    lines.append('G:='+group(data['ambient_generators'])+';;')
    lines.append(f'if Size(G)<>{data["order"]} then Error("ambient order");fi;')
    lines.append('KnownMaximalSubgroups:=List(ConjugacyClassesMaximalSubgroups(G),Representative);;')
    for row in data['representatives']:
        lines.append('H:='+group(row['H_generators'])+';; K:='+group(row['K_generators'])+';;')
        lines.append('VerifyWitness(G,H,K,'+json.dumps(row['orders'])+','+str(data['require_2transitive']).lower()+','+str(data['require_IP2']).lower()+');')
    lines.append(f'Print("WITNESS_PASS {name} {len(data["representatives"])}\\n");')
lines.append('QUIT;')
program='\n'.join(lines)
run=subprocess.run([GAP,'--quitonbreak','-q'],input=program,text=True,capture_output=True,timeout=120)
result={'purpose':'Independent validity check of exported permutation generators; no subgroup catalogue enumeration or TomLib load. Completeness and pairwise inequivalence not checked here.','returncode':run.returncode,'inputs':files,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'generated_gap_program_sha256':hashlib.sha256(program.encode()).hexdigest(),'stdout':run.stdout,'stderr':run.stderr,'pass':run.returncode==0 and 'WITNESS_PASS J2 8' in run.stdout and 'WITNESS_PASS Sz8 29' in run.stdout and 'Error' not in run.stderr}
(BASE/'classification_witness_check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'pass':result['pass'],'returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr},indent=2))
raise SystemExit(0 if result['pass'] else 1)
