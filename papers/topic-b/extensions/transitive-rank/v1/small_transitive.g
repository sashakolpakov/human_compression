# Exhaustive degree-six/eight/nine imprimitive high-rank C-markings, modulo
# simultaneous conjugation. A centralizer orbit at each extension preserves
# every already chosen generator, so this prunes no conjugacy class of tuples.
SizeScreen([100000,100000]);;
ReadCase:=function(n,id)
 local G,inv,target,maxrank,solutions,nodes,recursor,AllIP,N,sol;
 G:=TransitiveGroup(n,id);target:=QuoInt(n,2)+1;maxrank:=n-2;solutions:=[];nodes:=List([0..maxrank],x->0);N:=Normalizer(SymmetricGroup(n),G);
 inv:=Filtered(Elements(G),x->Order(x)=2);
 AllIP:=function(gs)
  local H,m,k,v,i;
  H:=List([0..2^Length(gs)-1],m->Subgroup(G,gs{Filtered([1..Length(gs)],i->QuoInt(m,2^(i-1)) mod 2=1)}));
  for m in [0..Length(H)-1] do for k in [0..Length(H)-1] do
   v:=Sum(Filtered([0..Length(gs)-1],i->QuoInt(m,2^i) mod 2=1 and QuoInt(k,2^i) mod 2=1),i->2^i);
   if Intersection(H[m+1],H[k+1])<>H[v+1] then return false;fi;
  od;od;return true;
 end;
 recursor:=function(gs,stab,H)
  local cand,reps,x,new,J,types,i;
  nodes[Length(gs)+1]:=nodes[Length(gs)+1]+1;
  if H=G then
   if Length(gs)>=target then
    types:=List([1..Length(gs)-1],i->Order(gs[i]*gs[i+1]));
    Add(solutions,rec(types:=types,gens:=gs));
   fi;return;
  fi;
  if Length(gs)>=maxrank or Index(G,H)<2^Maximum(0,target-Length(gs)) then return;fi;
  cand:=Filtered(inv,x->not x in H and ForAll(gs{[1..Maximum(0,Length(gs)-1)]},y->x*y=y*x));
  reps:=List(OrbitsDomain(stab,cand,OnPoints),o->o[1]);
  for x in reps do
   new:=Concatenation(gs,[x]);J:=Subgroup(G,new);
   if AllIP(new) then recursor(new,Centralizer(stab,x),J);fi;
  od;
 end;
 recursor([],N,TrivialSubgroup(G));
 Print("CASE n=",n," id=",id," order=",Size(G)," structure=",StructureDescription(G)," nodes=",nodes," complete_high_markings=",Length(solutions),"\n");
 Print("MARKINGS=",solutions,"\n");
 for sol in solutions do
  Print("SOLUTION|",n,"|",id,"|",sol.types,"|",List(sol.gens,x->List([1..n],i->i^x)),"\n");
 od;

end;;
for n in [6,8,9] do
 for id in [1..NrTransitiveGroups(n)] do
  G0:=TransitiveGroup(n,id);
  if not IsPrimitive(G0,[1..n]) then ReadCase(n,id);fi;
 od;
od;
Print("PASS_SMALL_TRANSITIVE_IMPRIMITIVE\n");QUIT;
