# Exact normalizer-torsor census for rank-two A4/C3 amalgams.
# GAP 4.15; computations are permutation group operations.
# All subgroup classes are obtained independently, not imported from paper counts.
SetInfoLevel(InfoWarning,0);
for q in [13,27] do
  G:=PSL(2,q);;
  cls:=ConjugacyClassesSubgroups(G);;
  all:=Concatenation(List(cls,AsList));;
  hs:=Filtered(all,H->Size(H)=12 and StructureDescription(H)="A4");;
  H:=hs[1];;
  T:=First(List(ConjugacyClassesSubgroups(H),Representative),X->Size(X)=3);;
  candidates:=Filtered(all,K->K<>H and IsSubgroup(K,T) and Size(K) in [6,12]
    and Size(Intersection(H,K))=3 and Size(ClosureGroup(H,K))=Size(G)
    and Length(DoubleCosets(K,T,T))=2);;
  N:=Normalizer(G,T);;
  M:=Intersection(N,Normalizer(G,H));;
  orb:=Orbits(M,candidates,OnPoints);;
  ordered:=List(orb,x->x[1]);;
  # Compare global G orbits of unordered parabolic pairs.
  pairAction:=function(pair,g) return Set(List(pair,x->x^g)); end;;
  unordered:=[];;
  for K in ordered do
    pair:=Set([H,K]);;
    if not ForAny(unordered,p->RepresentativeAction(G,p,pair,pairAction)<>fail) then Add(unordered,pair); fi;
  od;
  A:=AutomorphismGroup(G);;
  autoAction:=function(pair,a) return Set(List(pair,x->Image(a,x))); end;;
  isomorphic:=[];;
  for pair in unordered do
    if not ForAny(isomorphic,p->RepresentativeAction(A,p,pair,autoAction)<>fail) then Add(isomorphic,pair); fi;
  od;
  Print("q=",q," |G|=",Size(G)," subgroup_classes=",Length(cls)," subgroups=",Length(all),"\n");
  Print("|H|=",Size(H)," |T|=",Size(T)," |N_G(T)|=",Size(N)," |N_G(H,T)|=",Size(M),"\n");
  Print("candidates=",Length(candidates)," ordered_anchor_orbits=",Length(ordered)," unordered_G_orbits=",Length(unordered)," unordered_AutG_orbits=",Length(isomorphic),"\n");
  for typ in ["C6","S3","A4"] do
    Print(typ," candidates=",Number(candidates,x->StructureDescription(x)=typ)," ordered_anchor=",Number(ordered,x->StructureDescription(x)=typ)," unordered_G=",Number(unordered,p->(typ="A4" and ForAll(p,x->StructureDescription(x)="A4")) or (typ<>"A4" and ForAny(p,x->StructureDescription(x)=typ)))," unordered_AutG=",Number(isomorphic,p->(typ="A4" and ForAll(p,x->StructureDescription(x)="A4")) or (typ<>"A4" and ForAny(p,x->StructureDescription(x)=typ))),"\n");
  od;
  Print("representatives=",List(isomorphic,p->List(p,GeneratorsOfGroup)),"\n");
od;
QUIT;
