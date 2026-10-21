# Exact verification of the degree-six exceptions and all rank-three polytopes.
LogTo("research/leemans/commuting_pairs_exception_check.log");
start:=Runtime();;
PairAction:=function(pair,aut)
  return Set(pair,x->Image(aut,x));
end;;
for G in [SymmetricGroup(6),AlternatingGroup(6)] do
  inv:=Filtered(Elements(G),x->Order(x)=2);;
  aut:=AutomorphismGroup(G);;
  pairs:=[];;
  for i in [1..Length(inv)] do
    for j in [i+1..Length(inv)] do
      if inv[i]*inv[j]=inv[j]*inv[i] then Add(pairs,Set([inv[i],inv[j]])); fi;
    od;
  od;
  orbs:=OrbitsDomain(aut,pairs,PairAction);;
  Print("Group order ",Size(G)," automorphism order ",Size(aut),
        " involutions ",Length(inv)," commuting unordered pairs ",Length(pairs),
        " pair orbits ",Length(orbs),"\n");
  found:=[];; candidates:=0;; generated:=0;;
  for orb in orbs do
    pair:=orb[1];; a:=pair[1];; c:=pair[2];;
    stabilizer:=Stabilizer(aut,pair,PairAction);;
    middles:=OrbitsDomain(stabilizer,inv,function(x,phi) return Image(phi,x); end);;
    for midorb in middles do
      b:=midorb[1];; candidates:=candidates+1;;
      if Size(Group(a,b,c))=Size(G) then
        generated:=generated+1;
        left:=Group(a,b);; right:=Group(b,c);;
        if Size(Intersection(left,right))=2 then
          type:=SortedList([Order(a*b),Order(b*c)]);;
          Add(found,rec(generators:=[a,b,c],type:=type));
          Print("Polyhedron type ",type," generators ",[a,b,c],"\n");
        fi;
      fi;
    od;
  od;
  Print("Middle orbits tested ",candidates," generating ",generated,
        " polytopes up to isomorphism and duality ",Length(found),"\n");
  if Size(G)=720 then
    if Length(orbs)<>5 or SortedList(List(found,x->x.type))<>[[5,6],[6,6]] then
      Error("Sym(6) census disagreement");
    fi;
  else
    if Length(orbs)<>1 or Length(found)<>0 then Error("Alt(6) census disagreement"); fi;
  fi;
od;
Print("GAP ",GAPInfo.Version," CPU milliseconds ",Runtime()-start,"\nPASS\n");
LogTo();
QUIT;
