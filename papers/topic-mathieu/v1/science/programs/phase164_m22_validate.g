# Post-enumeration witness verification. This does not prove exhaustiveness.
LoadPackage("tomlib");;
SizeScreen([100000,24]);;
Read("phase164_m22_witnesses.g");;
started:=Runtime();;
Check:=function(test,msg) if not test then Error(msg);fi;end;;
Check(Size(G)=443520,"wrong group order");;
tom:=TableOfMarks("M22");;R:=List(MaximalSubgroupsTom(tom)[1],i->RepresentativeTom(tom,i));;
allM:=Concatenation(List(R,H->Orbit(G,H,OnPoints)));;
AP:=Action(A,allM,OnPoints);;
Check(Size(AP)=Size(AutomorphismGroup(G)),"automorphism action incomplete");;
PairChecks:=0;;TripleChecks:=0;;HellyChecks:=0;;GenChecks:=0;;PanelChecks:=0;;
Signature:=function(t)
 return [SortedList(List(t,Size)),SortedList(List(Combinations(t,2),p->Size(Intersection(p)))),Size(Intersection(t))];
end;;
for family in [M22Pairs,M22Triples] do
 sets:=List(family,t->Set(List(t,H->Position(allM,H))));
 Check(ForAll(sets,s->not fail in s),"nonmaximal witness");
 sigs:=List(family,Signature);
 for i in [1..Length(family)] do
  t:=family[i];r:=Length(t);B:=Intersection(t);
  Check(Size(Group(Concatenation(List(t,GeneratorsOfGroup))))=Size(G),"disconnected global incidence");
  for j in [1..i-1] do
   if sigs[i]=sigs[j] then
    Check(RepresentativeAction(AP,sets[i],sets[j],OnSets)=fail,"duplicate automorphism/type orbit");
   fi;
  od;
  if r=2 then
   Check(ForAll(t,H->Index(H,B)>1),"rank-two panel not firm");PairChecks:=PairChecks+1;
  else
   for k in [1..3] do
    others:=Difference([1..3],[k]);j:=others[1];l:=others[2];
    P:=Intersection(t[k],t[j]);Q:=Intersection(t[k],t[l]);
    Check(Size(Group(Concatenation(GeneratorsOfGroup(P),GeneratorsOfGroup(Q))))=Size(t[k]),"disconnected vertex residue");GenChecks:=GenChecks+1;
    Rkl:=Intersection(t[j],t[l]);
    one:=Set(List(RightTransversal(t[j],P),g->RightCoset(t[k],g)));
    two:=Set(List(RightTransversal(t[l],Q),g->RightCoset(t[k],g)));
    Check(Length(Intersection(one,two))=Index(Rkl,B),"nontransitive chambers");HellyChecks:=HellyChecks+1;
    Check(Index(Rkl,B)>1,"rank-three panel not firm");PanelChecks:=PanelChecks+1;
   od;
   TripleChecks:=TripleChecks+1;
  fi;
 od;
od;
Print("WITNESSES_PAIRS ",PairChecks," TRIPLES ",TripleChecks," THREE_WAY_HELLY ",HellyChecks," RESIDUE_GENERATION ",GenChecks," FIRM_PANELS ",PanelChecks,"\n");
Print("BOREL_IDS ",Collected(List(M22Triples,t->IdGroup(Intersection(t)))),"\n");
Print("CPU_MILLISECONDS ",Runtime()-started,"\nM22_WITNESSES_VALIDATED\n");
QUIT;
