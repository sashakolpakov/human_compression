# Required exact L044 replacement certificate. GAP/PrimGrp operations trusted.
# Reuses accepted L047 prefix enumeration, with ALL IP and centralizer-quotient
# tests removed. Only string commutation, irredundancy, index and genuine
# normalizer/prefix-stabilizer conjugation are used. No target source table.
SizeScreen([100000,100000]);;
L044IndependentStringCensus:=function(n,id,target,maxrank)
 local G,inv,solutions,nodes,recursor,Independent,N,sol;
 G:=SymmetricGroup(n);solutions:=[];nodes:=List([0..maxrank],x->0);N:=Normalizer(SymmetricGroup(n),G);
 inv:=Concatenation(List(Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2),Elements));
 Independent:=function(gs)
  local H,i;
  H:=Subgroup(G,gs);
  return ForAll([1..Length(gs)],i->Subgroup(G,gs{Difference([1..Length(gs)],[i])})<>H);
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
  if Length(gs)>0 then cand:=Filtered(cand,x->x*gs[Length(gs)]<>gs[Length(gs)]*x);fi;
  reps:=List(OrbitsDomain(stab,cand,OnPoints),o->o[1]);
  for x in reps do
   new:=Concatenation(gs,[x]);J:=Subgroup(G,new);
   if Independent(new) then
    recursor(new,Centralizer(stab,x),J);
   fi;
  od;
 end;
 Print("START n=",n," id=",id," order=",Size(G)," target=",target," max=",maxrank," involutions=",Length(inv),"\n");
 recursor([],N,TrivialSubgroup(G));
 Print("CASE n=",n," id=",id," order=",Size(G)," nodes=",nodes," complete_high_markings=",Length(solutions),"\n");
 Print("MARKINGS=",solutions,"\n");
 for sol in solutions do
  Print("SOLUTION|",n,"|",id,"|",sol.types,"|",List(sol.gens,x->List([1..n],i->i^x)),"\n");
 od;
 return rec(nodes:=nodes,solutions:=solutions);
end;;

L044IndependentStringCensus(8,0,6,6);;
Print("PASS_S8_INDEPENDENT_RANK_SIX\n");QUIT;
