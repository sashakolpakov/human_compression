# Exhaustive S5/S6 maximal-length independent involutory string markings, modulo
# simultaneous conjugation. A centralizer orbit at each extension preserves
# every already chosen generator, so this prunes no conjugacy class of tuples.
SizeScreen([100000,100000]);;
ReadCase:=function(n)
 local G,inv,target,solutions,nodes,recursor,AllIP,Independent,sol;
 G:=SymmetricGroup(n);target:=n-1;solutions:=[];nodes:=List([0..target],x->0);
 inv:=Filtered(Elements(G),x->Order(x)=2);
 Independent:=function(gs)
  local H,i;
  H:=Subgroup(G,gs);
  return ForAll([1..Length(gs)],i->Subgroup(G,gs{Difference([1..Length(gs)],[i])})<>H);
 end;
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
  if Length(gs)=target then
   if H<>G or not Independent(gs) then return;fi;
   types:=List([1..target-1],i->Order(gs[i]*gs[i+1]));
   if types<>List([1..target-1],i->3) then Error("non-Coxeter maximal marking");fi;
   if ForAny(gs,x->SignPerm(x)<>-1) then Error("nonodd maximal marking");fi;
   if Size(Centralizer(G,Subgroup(G,gs{[2..target]})))<>1 then Error("tail centralizer");fi;
   if Size(Centralizer(G,DerivedSubgroup(Subgroup(G,gs{[2..target]}))))<>1 then Error("derived tail centralizer");fi;
   if not AllIP(gs) then Error("independent maximal string lacks IP");fi;
   Add(solutions,gs);return;
  fi;
  cand:=Filtered(inv,x->not x in H and ForAll(gs{[1..Maximum(0,Length(gs)-1)]},y->x*y=y*x));
  reps:=List(OrbitsDomain(stab,cand,OnPoints),o->o[1]);
  for x in reps do
   new:=Concatenation(gs,[x]);J:=Subgroup(G,new);
   if Independent(new) then recursor(new,Centralizer(stab,x),J);fi;
  od;
 end;
 recursor([],G,TrivialSubgroup(G));
 Print("N=",n," nodes=",nodes," complete_maximal_markings=",Length(solutions),"\n");
 Print("MARKINGS=",solutions,"\n");
 for sol in solutions do
  Print("EXTREMAL|",n,"|",List(sol,x->List([1..n],i->i^x)),"\n");
 od;
 if Length(solutions)=0 then Error("missing standard marking");fi;
end;;
ReadCase(5);ReadCase(6);
Print("PASS_EXTREMAL_S5_S6\n");QUIT;
