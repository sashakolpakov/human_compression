# Exhaustive connected string C-markings in the bounded primitive residuals.
# Search symmetries only conjugate the entire fixed prefix; every pruning test
# is necessary for an independent string C-marking. Accepted tuples get full IP.
SizeScreen([100000,100000]);;
L047Census:=function(n,id,target,maxrank)
 local G,inv,solutions,nodes,recursor,AllIP,Independent,N,pp,sol;
 G:=SymmetricGroup(n);solutions:=[];nodes:=List([0..maxrank],x->0);N:=Normalizer(SymmetricGroup(n),G);
 inv:=Concatenation(List(Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2),Elements));
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
  local cand,reps,x,new,J,types,i,tail,mid,cent,q;
  nodes[Length(gs)+1]:=nodes[Length(gs)+1]+1;
  if H=G then
   if Length(gs)>=target and AllIP(gs) then
    types:=List([1..Length(gs)-1],i->Order(gs[i]*gs[i+1]));
    Add(solutions,rec(types:=types,gens:=gs));
   fi;return;
  fi;
  if Length(gs)>=maxrank or Index(G,H)<2^Maximum(0,target-Length(gs)) then return;fi;
  q:=Maximum(0,target-Length(gs)-1);
  if q>0 and Length(gs)>0 then
   cent:=Centralizer(G,H);
   if Index(cent,Centre(H))<2^q then return;fi;
  fi;
  cand:=Filtered(inv,x->not x in H and ForAll(gs{[1..Maximum(0,Length(gs)-1)]},y->x*y=y*x));
  if Length(gs)>0 then cand:=Filtered(cand,x->x*gs[Length(gs)]<>gs[Length(gs)]*x);fi;
  reps:=List(OrbitsDomain(stab,cand,OnPoints),o->o[1]);
  for x in reps do
   new:=Concatenation(gs,[x]);J:=Subgroup(G,new);
   if Independent(new) then
    tail:=Subgroup(G,new{[2..Length(new)]});
    mid:=Subgroup(G,gs{[2..Length(gs)]});
    if Intersection(H,tail)=mid then recursor(new,Centralizer(stab,x),J);fi;
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
end;;
for l047spec in [[8,0,6,6]] do
 CallFuncList(L047Census,l047spec);
od;
Print("PASS_PRIMITIVE_MARKINGS\n");QUIT;
