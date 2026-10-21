# Independent local check: only the saved permutations are imported.
# No author local_geometry.g or verify.g is used.
if not IsBound(WitnessPath) then Error("explicit WitnessPath required");fi;
Read(WitnessPath);;
LoadPackage("primgrp");;
G:=PrimitiveGroup(3510,2);;
if PRIMINDX[3510]<>34 then Error("degree3510 index mismatch");fi;
Print("PRIMITIVE_ROUTE ",PRIMINDX[3510]," ",PRIMGrp(3510,2){[1..8]},"\n");;
P:=Group(Fi22r);;
Print("FRESH_GROUP_HAS_SIZE ",HasSize(P),"\n");;
if Size(P)<>129123503308800 or P<>G then Error("generated named group mismatch");fi;
# The actual finite sets of all proper standard subgroups are constructed.
# Flags are tested as pairwise intersections of literal left coset sets.
Analyze:=function(m)
 local ix,subs,A,B,i,j,k,ps,C,D,y,z,w,ny,nz,pairs,flags,counts;
 if Length(Set(m))<>3 or not ForAll(m,g->g^2=() and g<>()) then Error("marks");fi;
 ix:=Filtered(Combinations([1,2,3]),x->Length(x)<3);
 subs:=List(ix,x->Set(Elements(Group(m{x},()))));
 pairs:=0;
 for A in [1..7] do for B in [1..7] do
  if Intersection(subs[A],subs[B])<>subs[Position(ix,Intersection(ix[A],ix[B]))] then Error("literal IP sets");fi;
  pairs:=pairs+1;
 od;od;
 counts:=[];
 for i in [1..3] do
  j:=Difference([1..3],[i])[1];k:=Difference([1..3],[i])[2];
  ps:=List([1..3],v->Set(Elements(Group(m{Difference([1..3],[v])}))));
  C:=Set(List(ps[i],g->Set(List(ps[j],h->g*h))));
  D:=Set(List(ps[i],g->Set(List(ps[k],h->g*h))));
  flags:=0;
  for y in C do for z in D do
   w:=Intersection(y,z);
   if Length(w)>0 then
    flags:=flags+1;
    if Length(Intersection(w,ps[i]))<>1 then Error("incident flag lacks unique common representative");fi;
   fi;
  od;od;
  # With trivial Borel each element of P_i gives exactly one flag anchored at P_i.
  if flags<>Length(ps[i]) then Error("anchored chamber count");fi;
  Add(counts,[Length(C),Length(D),flags]);
 od;
 return rec(properIP:=pairs,anchored:=counts);
end;;
r:=Fi22r;;s:=[r[1],r[2],r[2]^r[3]];;
if Group(s)<>P then Error("halved generation");fi;
if List([[1,2],[1,3],[2,3]],ij->Order(r[ij[1]]*r[ij[2]]))<>[6,2,13] then Error("string type");fi;
if List([[1,2],[1,3],[2,3]],ij->Order(s[ij[1]]*s[ij[2]]))<>[6,6,13] then Error("triangle type");fi;
x:=Analyze(r);;y:=Analyze(s);;
Print("STRING ",x,"\nTRIANGLE ",y,"\n");;
Print("INDEPENDENT_LITERAL_COSETS PASS 98properIP 6all-flag-families 30full-subset-identities\n");;
QUIT;
