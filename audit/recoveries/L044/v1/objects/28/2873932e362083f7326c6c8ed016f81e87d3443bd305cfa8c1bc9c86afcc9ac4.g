# Required exact L044 replacement certificate. GAP/PrimGrp operations trusted.
# Reuses accepted L047 prefix enumeration, with ALL IP and centralizer-quotient
# tests removed. Only string commutation, irredundancy, index and genuine
# normalizer/prefix-stabilizer conjugation are used. No target source table.
SizeScreen([100000,100000]);;
L044IndependentStringCensus:=function(n,id,target,maxrank)
 local G,inv,solutions,nodes,recursor,Independent,N,sol;
 if id=0 then G:=AlternatingGroup(n);else G:=PrimitiveGroup(n,id);fi;solutions:=[];nodes:=List([0..maxrank],x->0);N:=Normalizer(SymmetricGroup(n),G);
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

L044Need:=function(ok,message)
 if not ok then Error(message);fi;
end;;
L044Independent:=function(gs)
 local H;
 H:=Group(gs);
 return ForAll([1..Length(gs)],i->Group(gs{Difference([1..Length(gs)],[i])})<>H);
end;;
L044String:=function(gs)
 return ForAll([1..Length(gs)],i->ForAll([i+2..Length(gs)],j->gs[i]*gs[j]=gs[j]*gs[i]));
end;;
L044LiteralCounterexample:=function()
 local images,gs,G,omissions,noncomm,orders,control;
 images:=[
 [1,3,2,4,5,7,6,8],
 [4,2,3,1,5,7,6,8],
 [1,4,3,2,7,6,5,8],
 [1,7,3,5,4,6,2,8],
 [2,1,4,3,6,5,8,7]];
 gs:=List(images,PermList);G:=Group(gs);
 L044Need(Size(G)=1344 and IsTransitive(G,[1..8]) and IsPrimitive(G,[1..8]),"literal degree-eight primitive action");
 L044Need(ForAll(gs,t->Order(t)=2 and SignPerm(t)=1),"five even involutions");
 omissions:=List([1..5],i->Size(Group(gs{Difference([1..5],[i])})));
 L044Need(omissions=[192,192,192,96,168] and L044Independent(gs),"literal omission orders");
 noncomm:=List([1..5],i->Filtered([1..5],j->gs[i]*gs[j]<>gs[j]*gs[i]));
 L044Need(noncomm[1]=[3,4,5],"noncommuting degree-three obstruction");
 orders:=Filtered(PermutationsList(gs),L044String);
 L044Need(Length(orders)=0,"no string ordering");
 L044Need(G=PrimitiveGroup(8,3),"optional catalogue identification");
 control:=[(1,2),(2,3),(3,4)];
 L044Need(L044Independent(control) and L044String(control) and Size(Group(control))=24,"positive Coxeter control");
 L044Need(not L044Independent(Concatenation(control,[control[1]])),"duplicate-generator negative control");
 L044Need(not L044String(gs),"far-commutation negative control");
 L044Need(not IsTransitive(Group(gs{[1..4]}),[1..8]),"missing-translation negative control");
 L044Need(not IsPrimitive(Group((1,2,3,4,5,6,7,8)),[1..8]),"imprimitive-action negative control");
 Print("COUNTEREXAMPLE|order=",Size(G),"|primitive=true|omissions=",omissions,"|noncommuting_neighbors=",noncomm,"|string_orderings=",Length(orders),"\n");
 Print("CONTROLS|positive_coxeter=1|negative=4\n");
end;;

L044FiniteIndependentStrings:=function()
 local n,id,G,target,omega,classes,H,endpoint,disposition,residual,expected,caseid,R,control,M;
 residual:=[];
 for n in [8..25] do
  for id in [1..NrPrimitiveGroups(n)] do
   G:=PrimitiveGroup(n,id);
   if Size(G)>=Factorial(n)/2 then continue;fi;
   target:=n-3;omega:=Length(FactorsInt(Size(G)));
   if omega<target then disposition:="order_chain";
   else
    classes:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);
    H:=Subgroup(G,Concatenation(List(classes,Elements)));
    if H<>G then disposition:="not_involution_generated";
    else
     endpoint:=Maximum(List(classes,c->1+Length(FactorsInt(QuoInt(Size(G),Size(c))))));
     if endpoint<target then disposition:="endpoint_centralizer_chain";
     else Add(residual,[n,id]);disposition:="complete_independent_string_search";fi;
    fi;
   fi;
   Print("SCREEN|",n,"|",id,"|",Size(G),"|",target,"|",disposition,"\n");
  od;
 od;
 expected:=[[8,3],[8,5],[9,7],[16,11]];
 L044Need(residual=expected,"complete primitive frontier");
 for caseid in expected do
  G:=PrimitiveGroup(caseid[1],caseid[2]);
  R:=L044IndependentStringCensus(caseid[1],caseid[2],caseid[1]-3,Length(FactorsInt(Size(G))));
  L044Need(Length(R.solutions)=0,"forbidden independent string exists");
 od;
 for n in [26..63] do
  M:=n*Product([0..LogInt(n,2)-1],j->n-2^j);
  L044Need(M<2^(n-3),"exact Maroti integer comparison");
 od;
 control:=L044IndependentStringCensus(6,1,3,3);
 L044Need(Length(control.solutions)>0,"positive census control");
 Print("PASS_L044_PRIMITIVE_STRINGS|actions=4|integer_cases=38|positive_A5=",Length(control.solutions),"|negative_controls=4\n");
end;;
L044LiteralCounterexample();
L044FiniteIndependentStrings();
QUIT;

