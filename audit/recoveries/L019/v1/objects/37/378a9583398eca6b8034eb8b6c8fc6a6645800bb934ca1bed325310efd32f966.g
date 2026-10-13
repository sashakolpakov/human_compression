# Finite boundary diagnostic: exact rank n/2 anchored even C-markings
# inside the full even wreath action with k-point blocks. No classification
# assertion is made from an incomplete or capped execution.
SizeScreen([100000,100000]);;
RunAnchoredWreath:=function(n,k)
 local m,gens,j,a,i,p,W,E,inv,tailinv,stab0,target,nodes,solutions,
      AllIP,visit,chosen,orbits,reps,H,solution;
 m:=QuoInt(n,k);gens:=[];
 for j in [0..m-1] do
  for i in [1..k-1] do Add(gens,(j*k+i,j*k+i+1));od;
 od;
 for j in [0..m-2] do
  p:=();for a in [1..k] do p:=p*(j*k+a,(j+1)*k+a);od;Add(gens,p);
 od;
 W:=Group(gens);E:=Intersection(W,AlternatingGroup(n));
 inv:=Filtered(Elements(E),x->Order(x)=2);
 tailinv:=Filtered(inv,x->1^x=1);stab0:=Stabilizer(W,1);
 target:=QuoInt(n,2);nodes:=List([0..target],x->0);solutions:=[];
 AllIP:=function(gs)
  local groups,mask,other,common,inds,l;
  if Length(gs)<=2 then return true;fi;
  groups:=[];
  for mask in [0..2^Length(gs)-1] do
   inds:=Filtered([1..Length(gs)],l->QuoInt(mask,2^(l-1)) mod 2=1);
   Add(groups,Subgroup(E,gs{inds}));
  od;
  for mask in [0..Length(groups)-1] do
   for other in [0..mask] do
    common:=Sum(Filtered([0..Length(gs)-1],l->QuoInt(mask,2^l) mod 2=1 and QuoInt(other,2^l) mod 2=1),l->2^l);
    if Intersection(groups[mask+1],groups[other+1])<>groups[common+1] then return false;fi;
   od;
  od;return true;
 end;
 visit:=function(gs,stab,H)
  local len,cand,reps,x,next,J;
  len:=Length(gs);nodes[len+1]:=nodes[len+1]+1;
  if len=target then
   if IsTransitive(H,[1..n]) then
    Add(solutions,ShallowCopy(gs));
    Print("SOLUTION|",n,"|",k,"|",Size(H),"|",List(gs,x->List([1..n],i->i^x)),"\n");
   fi;return;
  fi;
  if Index(E,H)<2^(target-len) then return;fi;
  if len=0 then cand:=Filtered(inv,x->1^x<>1);
  else cand:=Filtered(tailinv,x->not x in H and x*gs[len]<>gs[len]*x and ForAll(gs{[1..len-1]},y->x*y=y*x));fi;
  reps:=List(OrbitsDomain(stab,cand,OnPoints),o->o[1]);
  for x in reps do
   next:=Concatenation(gs,[x]);J:=Subgroup(E,next);
   if AllIP(next) then visit(next,Centralizer(stab,x),J);fi;
  od;
 end;
 visit([],stab0,TrivialSubgroup(E));
 Print("COMPLETE_ANCHORED_EVEN_WREATH|",n,"|",k,"|",Size(W),"|",Size(E),"|",Length(inv),"|",Length(tailinv),"|",nodes,"|",Length(solutions),"\n");
end;;
