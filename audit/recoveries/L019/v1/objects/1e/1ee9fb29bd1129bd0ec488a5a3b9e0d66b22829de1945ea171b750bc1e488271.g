# Bounded diagnostic only. No classification is inferred from a timeout.
# Exact target: natural S10 rank6, anchor1, fractured, nonpure first mark,
# and every necessary supported even-prefix kernel condition.
SizeScreen([100000,100000]);;
n:=10;; target:=6;; E:=SymmetricGroup(n);;
inv:=[];;
for j in [1..QuoInt(n,2)] do
 p:=Product(List([1..j],i->(2*i-1,2*i)));
 Append(inv,AsList(ConjugacyClass(E,p)));
od;
inv:=Set(inv);; tailinv:=Filtered(inv,x->1^x=1);;
nodes:=List([0..target],x->0);; solutions:=[];;
rejected:=rec(orbit:=0,endcriterion:=0,evenkernel:=0);;

PartitionOf:=function(gs)
 local H,parts;
 H:=Group(Concatenation([()],gs));
 parts:=List(Orbits(H,[1..n]),Set);Sort(parts);return parts;
end;;

OrbitEssential:=function(gs)
 local parts,j,others;
 parts:=PartitionOf(gs);
 for j in [1..Length(gs)] do
  others:=gs{Filtered([1..Length(gs)],i->i<>j)};
  if PartitionOf(others)=parts then return false;fi;
 od;
 return true;
end;;

# Retained terminal oracle: all pairs of all generated subsets.
AllIP:=function(gs)
 local groups,mask,other,common,inds,l;
 groups:=[];
 for mask in [0..2^Length(gs)-1] do
  inds:=Filtered([1..Length(gs)],l->QuoInt(mask,2^(l-1)) mod 2=1);
  Add(groups,Subgroup(E,gs{inds}));
 od;
 for mask in [0..Length(groups)-1] do
  for other in [0..mask] do
   common:=Sum(Filtered([0..Length(gs)-1],l->QuoInt(mask,2^l) mod 2=1
                  and QuoInt(other,2^l) mod 2=1),l->2^l);
   if Intersection(groups[mask+1],groups[other+1])<>groups[common+1] then return false;fi;
  od;
 od;
 return true;
end;;

Visit:=function(gs,stab,H,ends)
 local len,cand,reps,x,next,J,rootOrbit,evenSupported,newEnds,good,i;
 len:=Length(gs);nodes[len+1]:=nodes[len+1]+1;
 if len=target then
  if Size(H)=Factorial(n) then
   if not AllIP(gs) then Error("terminal full-subset IP disagrees");fi;
   Add(solutions,ShallowCopy(gs));
   Print("SOLUTION|",List(gs,x->List([1..n],i->i^x)),"\n");
  fi;
  return;
 fi;
 if Index(E,H)<2^(target-len) then return;fi;
 if len=0 then cand:=Filtered(inv,x->1^x<>1 and NrMovedPoints(x)>2);
 else cand:=Filtered(tailinv,x->not x in H and x*gs[len]<>gs[len]*x
                      and ForAll(gs{[1..len-1]},y->x*y=y*x));fi;
 reps:=List(OrbitsDomain(stab,cand,OnPoints),o->o[1]);
 for x in reps do
  next:=Concatenation(gs,[x]);
  if not OrbitEssential(next) then rejected.orbit:=rejected.orbit+1;continue;fi;
  newEnds:=List([1..len+1],i->Subgroup(E,next{[i..len+1]}));J:=newEnds[1];
  good:=true;
  if len>=2 then
   for i in [len-1,len-2..1] do
    if Intersection(ends[i],newEnds[i+1])<>ends[i+1] then good:=false;break;fi;
   od;
  fi;
  if not good then rejected.endcriterion:=rejected.endcriterion+1;continue;fi;
  rootOrbit:=Orbit(H,1);evenSupported:=Group(());
  if Length(rootOrbit)>=3 then evenSupported:=Intersection(J,AlternatingGroup(rootOrbit));fi;
  if not IsSubgroup(H,evenSupported) then rejected.evenkernel:=rejected.evenkernel+1;continue;fi;
  if len=0 then Print("FIRST_BEGIN|",NrMovedPoints(x),"\n");fi;
  Visit(next,Centralizer(stab,x),J,newEnds);
  if len=0 then Print("FIRST_END|",NrMovedPoints(x),"|",nodes,"|",rejected,"\n");fi;
 od;
end;;

Visit([],Stabilizer(E,1),TrivialSubgroup(E),[]);;
Print("COMPLETE_FRACTURED_CRITICAL_SYMMETRIC|",n,"|",target,"|",Length(inv),
      "|",Length(tailinv),"|",nodes,"|",Length(solutions),"|",rejected,"\n");
QUIT;
