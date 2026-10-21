# Distinct verification of actual witness geometries. The caller reads only
# the literal frozen group/subgroup data before this file, never author code.
SizeScreen([100000,24]);;
Need:=function(x,msg) if not x then Error(msg);fi;end;;
Need(Size(G)=443520 and Size(A)=1774080,"ambient orders");;
Need(Index(A,Centralizer(A,G))=887040,"automorphism image order");;
Need(Length(M22Pairs)=81 and Length(M22Triples)=431,"whole witness lists");;
LoadPackage("tomlib");;
T:=TableOfMarks("M22");;
Need(UnderlyingGroup(T)=G,"same named catalogue model");;
maxima:=List(MaximalSubgroupsTom(T)[1],i->RepresentativeTom(T,i));;
CheckedMaximal:=function(H)
 return ForAny(maxima,K->Size(K)=Size(H) and IsConjugate(G,H,K));
end;;
K:=TrivialSubgroup(G);;
pairCount:=0;;tripleCount:=0;;residueCount:=0;;completionCount:=0;;panelCount:=0;;
for tuple in M22Pairs do
 Need(Length(Set(tuple))=2 and ForAll(tuple,CheckedMaximal),"actual maximal pair");;
 K:=Intersection(tuple);;
 Need(ClosureGroup(tuple[1],tuple[2])=G and ForAll(tuple,H->Index(H,K)>1),"pair geometry");;
 pairCount:=pairCount+1;
od;
for tuple in M22Triples do
 Need(Length(Set(tuple))=3 and ForAll(tuple,CheckedMaximal),"actual maximal triple");;
 B:=Intersection(tuple);;
 for i in [1..3] do
  others:=Difference([1..3],[i]);;j:=others[1];;k:=others[2];;
  U:=Intersection(tuple[i],tuple[j]);;V:=Intersection(tuple[i],tuple[k]);;
  Need(ClosureGroup(U,V)=tuple[i],"actual residue connectedness");;residueCount:=residueCount+1;
  P:=Intersection(tuple[j],tuple[k]);;
  left:=Orbit(tuple[j],RightCoset(tuple[i],()),OnRight);;
  right:=Orbit(tuple[k],RightCoset(tuple[i],()),OnRight);;
  completions:=Intersection(left,right);;
  actualOrbit:=Orbit(P,RightCoset(tuple[i],()),OnRight);;
  # Set equality is stronger than the author's cardinality equality check.
  Need(Set(actualOrbit)=Set(completions),"pair stabilizer transitive on actual completions");;
  completionCount:=completionCount+1;
  Need(Length(actualOrbit)=Index(P,B) and Index(P,B)>1,"actual panel");;panelCount:=panelCount+1;
 od;
 tripleCount:=tripleCount+1;
od;
Print("PASS_L073_DISTINCT_WITNESSES:pairs=",pairCount,";triples=",tripleCount,
 ";residues=",residueCount,";actual-completion-orbits=",completionCount,";panels=",panelCount,"\n");
QUIT;
