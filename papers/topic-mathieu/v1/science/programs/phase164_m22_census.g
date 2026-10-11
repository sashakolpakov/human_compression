# Author census candidate for L073. No source geometry/table data are read.
# Run in a fresh working directory: the exact witnesses are written locally.
LoadPackage("tomlib");;
SizeScreen([100000,24]);;
tom:=TableOfMarks("M22");;G:=UnderlyingGroup(tom);;
ids:=MaximalSubgroupsTom(tom)[1];;ns:=Length(OrdersTom(tom));;inc:=SubsTom(tom);;
derived:=Filtered([1..ns-1],i->not ForAny([i+1..ns-1],j->i in inc[j]));;
if derived<>SortedList(ids) then Error("maximal catalogue mismatch");fi;
maxReps:=List(ids,i->RepresentativeTom(tom,i));;
AA:=AutomorphismGroup(G);;A:=Normalizer(SymmetricGroup(LargestMovedPoint(G)),G);;
if Index(A,Centralizer(A,G))<>Size(AA) then Error("incomplete automorphism image");fi;
M:=Concatenation(List(maxReps,H->Orbit(G,H,OnPoints)));;
if Length(Set(M))<>Length(M) then Error("overlapping maximal classes");fi;
AH:=ActionHomomorphism(A,M,OnPoints);;AP:=Image(AH);;ms:=List(M,Size);;
Print("INPUT G_ORDER ",Size(G)," TOM_CLASSES ",ns," MAXIMAL_ORDERS ",List(maxReps,Size)," OBJECTS ",Length(M)," AUT_ORDER ",Size(AP),"\n");
meetCache:=[];;rowCache:=[];;
Meet:=function(i,j)
 local a,b;
 a:=Minimum(i,j);b:=Maximum(i,j);
 if not IsBound(meetCache[a]) then meetCache[a]:=[];fi;
 if not IsBound(meetCache[a][b]) then meetCache[a][b]:=Intersection(M[a],M[b]);fi;
 return meetCache[a][b];
end;;
CosetRow:=function(i,j)
 if not IsBound(rowCache[i]) then rowCache[i]:=[];fi;
 if not IsBound(rowCache[i][j]) then
  rowCache[i][j]:=Set(List(RightTransversal(M[j],Meet(i,j)),x->RightCoset(M[i],x)));
 fi;
 return rowCache[i][j];
end;;
PairSignature:=function(t) return [SortedList(ms{t}),Size(Meet(t[1],t[2]))];end;;
pairReps:=[];;pairSigs:=[];;pairTried:=0;;
for singleOrbit in Orbits(AP,[1..Length(M)]) do
 a:=singleOrbit[1];S:=Stabilizer(AP,a);
 for orb in Orbits(S,Difference([1..Length(M)],[a])) do
  t:=Set([a,orb[1]]);sig:=PairSignature(t);pairTried:=pairTried+1;
  bucket:=Filtered([1..Length(pairReps)],j->pairSigs[j]=sig);
  if not ForAny(bucket,j->RepresentativeAction(AP,t,pairReps[j],OnSets)<>fail) then
   Add(pairReps,t);Add(pairSigs,sig);
  fi;
 od;
od;
Print("PAIR_TOTAL TESTED ",pairTried," CLASSES ",Length(pairReps),"\n");
Recognize:=function(t)
 local P,Q,R,B;
 P:=Meet(t[1],t[2]);Q:=Meet(t[1],t[3]);R:=Meet(t[2],t[3]);
 if Size(ClosureGroup(P,Q))<>ms[t[1]] then return fail;fi;
 if Size(ClosureGroup(P,R))<>ms[t[2]] then return fail;fi;
 if Size(ClosureGroup(Q,R))<>ms[t[3]] then return fail;fi;
 B:=Intersection(P,Q);
 if Length(Intersection(CosetRow(t[1],t[2]),CosetRow(t[1],t[3])))<>Index(R,B) then return fail;fi;
 if not ForAll([P,Q,R],H->Index(H,B)>1) then Error("recognition failed firmness implication");fi;
 return rec(borel:=B,signature:=[SortedList(ms{t}),SortedList(List([P,Q,R],Size)),Size(B)]);
end;;
triples:=[];;tripleSigs:=[];;borels:=[];;tried:=0;;acceptedBeforeFusion:=0;;
for pidx in [1..Length(pairReps)] do
 pair:=pairReps[pidx];S:=Stabilizer(AP,pair,OnSets);localTried:=0;localAccepted:=0;
 for orb in Orbits(S,Difference([1..Length(M)],pair)) do
  t:=Set(Concatenation(pair,[orb[1]]));tried:=tried+1;localTried:=localTried+1;
  result:=Recognize(t);
  if result=fail then continue;fi;
  acceptedBeforeFusion:=acceptedBeforeFusion+1;localAccepted:=localAccepted+1;
  bucket:=Filtered([1..Length(triples)],j->tripleSigs[j]=result.signature);
  if ForAny(bucket,j->RepresentativeAction(AP,t,triples[j],OnSets)<>fail) then continue;fi;
  Add(triples,t);Add(tripleSigs,result.signature);Add(borels,result.borel);
 od;
 Print("PAIR_STAGE ",pidx," TESTED ",localTried," ACCEPTED ",localAccepted," GLOBAL_CLASSES ",Length(triples),"\n");
od;
PrintTo("phase164_m22_witnesses.g","# Independently generated witnesses, not source input.\nG:=",G,";\nA:=",A,";\nmaximalClassRepresentatives:=",maxReps,";\nM22Pairs:=",List(pairReps,t->M{t}),";\nM22Triples:=",List(triples,t->M{t}),";\n");
Print("TRIPLE_TOTAL TESTED ",tried," ACCEPTED_BEFORE_FUSION ",acceptedBeforeFusion," CLASSES ",Length(triples),"\n");
Print("BOREL_ORDER_COUNTS ",Collected(List(borels,Size)),"\n");
Print("M22_EXHAUSTIVE_FINISHED\n");
QUIT;
